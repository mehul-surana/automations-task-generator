"""
CreateBytes Workspace Automation
Browser automation using Playwright for task creation
"""

import asyncio
import logging
from typing import Optional, Tuple
from playwright.async_api import async_playwright, Page, Browser, BrowserContext

logger = logging.getLogger(__name__)


class CreateBytesAutomation:
    """
    Handles browser automation for CreateBytes Workspace
    Uses Playwright for reliable automation of the web interface
    """
    
    def __init__(
        self,
        email: str,
        password: str,
        base_url: str = "https://cb.workspace.createbytes.com"
    ):
        """
        Initialize CreateBytes automation
        
        Args:
            email: Login email
            password: Login password
            base_url: Base URL of CB Workspace
        """
        self.email = email
        self.password = password
        self.base_url = base_url
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self.playwright = None
        self.is_authenticated = False
    
    async def initialize(self) -> bool:
        """
        Initialize browser instance
        
        Returns:
            True if initialization successful
        """
        try:
            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.chromium.launch(headless=True)
            self.context = await self.browser.new_context()
            self.page = await self.context.new_page()
            
            logger.info("Playwright browser initialized successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize browser: {str(e)}")
            return False
    
    async def login(self) -> bool:
        """
        Authenticate with CreateBytes
        
        Returns:
            True if login successful
        """
        try:
            logger.info("Starting CreateBytes login...")
            
            # Navigate to login page
            await self.page.goto(f"{self.base_url}/login", wait_until="networkidle")
            await asyncio.sleep(1)
            
            # Check if already logged in
            if await self._is_logged_in():
                logger.info("Already authenticated with CreateBytes")
                self.is_authenticated = True
                return True
            
            # Fill login form
            logger.info(f"Logging in as {self.email}...")
            
            # Wait for and fill email field
            await self.page.wait_for_selector('input[type="email"]', timeout=10000)
            await self.page.fill('input[type="email"]', self.email)
            await asyncio.sleep(0.5)
            
            # Wait for and fill password field
            await self.page.wait_for_selector('input[type="password"]', timeout=10000)
            await self.page.fill('input[type="password"]', self.password)
            await asyncio.sleep(0.5)
            
            # Click login button
            login_button = await self.page.query_selector('button[type="submit"]')
            if not login_button:
                # Try alternative selectors
                login_button = await self.page.query_selector('button:has-text("Login")')
            
            if login_button:
                await login_button.click()
                await self.page.wait_for_load_state("networkidle", timeout=30000)
                await asyncio.sleep(2)
            else:
                logger.warning("Could not find login button, attempting alternative method...")
                await self.page.press('input[type="password"]', 'Enter')
                await self.page.wait_for_load_state("networkidle", timeout=30000)
                await asyncio.sleep(2)
            
            # Verify login
            if await self._is_logged_in():
                logger.info("✓ Successfully authenticated with CreateBytes")
                self.is_authenticated = True
                return True
            else:
                logger.error("Authentication verification failed")
                return False
                
        except Exception as e:
            logger.error(f"Login failed: {str(e)}")
            await self._take_screenshot("cb_login_error")
            return False
    
    async def navigate_to_project(self, project_id: str) -> bool:
        """
        Navigate to a project's kanban board
        
        Args:
            project_id: CreateBytes project ID
        
        Returns:
            True if navigation successful
        """
        try:
            kanban_url = f"{self.base_url}/projects/{project_id}/kanban"
            logger.info(f"Navigating to project: {kanban_url}")
            
            await self.page.goto(kanban_url, wait_until="networkidle", timeout=30000)
            await asyncio.sleep(2)
            
            # Verify we're on the kanban board
            if "kanban" in self.page.url:
                logger.info(f"✓ Successfully navigated to project kanban board")
                return True
            else:
                logger.error(f"Failed to navigate to kanban board. Current URL: {self.page.url}")
                await self._take_screenshot("cb_navigation_error")
                return False
                
        except Exception as e:
            logger.error(f"Navigation failed: {str(e)}")
            await self._take_screenshot("cb_navigation_error")
            return False
    
    async def create_task(
        self,
        project_id: str,
        title: str,
        description: str = "",
        assignee: str = "Mehul",
        priority: str = "Medium"
    ) -> bool:
        """
        Create a task on the kanban board
        
        Args:
            project_id: CreateBytes project ID
            title: Task title
            description: Task description
            assignee: Assignee name
            priority: Task priority (Low, Medium, High)
        
        Returns:
            True if task creation successful
        """
        try:
            # Navigate to project if not already there
            if f"projects/{project_id}" not in self.page.url:
                if not await self.navigate_to_project(project_id):
                    return False
            
            logger.info(f"Creating task: '{title}'")
            
            # Look for "Add Task" button
            add_task_button = None
            
            # Try various selectors for the add task button
            selectors = [
                'button:has-text("Add Task")',
                'button:has-text("Add New Task")',
                'button:has-text("+ Add Task")',
                '[data-testid="add-task-button"]',
                '.add-task-btn',
                'button[aria-label="Add task"]'
            ]
            
            for selector in selectors:
                try:
                    add_task_button = await self.page.query_selector(selector)
                    if add_task_button:
                        logger.info(f"Found add task button with selector: {selector}")
                        break
                except:
                    continue
            
            if not add_task_button:
                logger.warning("Could not find add task button, trying click by text...")
                try:
                    await self.page.click('text=Add Task')
                except:
                    logger.error("Could not find or click add task button")
                    await self._take_screenshot("cb_add_task_button_error")
                    return False
            else:
                await add_task_button.click()
            
            await asyncio.sleep(1)
            
            # Wait for modal/dialog to appear
            try:
                await self.page.wait_for_selector('[role="dialog"], .modal, .task-modal', timeout=10000)
            except:
                logger.warning("Modal not found with standard selectors, continuing...")
            
            await asyncio.sleep(1)
            
            # Fill task title
            title_selectors = [
                'input[placeholder*="title"]',
                'input[placeholder*="Task title"]',
                'input[placeholder*="Task name"]',
                'textarea[placeholder*="title"]',
                '[data-testid="task-title-input"]',
                '.task-title-input'
            ]
            
            title_filled = False
            for selector in title_selectors:
                try:
                    title_input = await self.page.query_selector(selector)
                    if title_input:
                        await title_input.click()
                        await title_input.fill("")
                        await title_input.type(title, delay=50)
                        logger.info(f"Filled title field: {title}")
                        title_filled = True
                        break
                except:
                    continue
            
            if not title_filled:
                # Try generic input approach
                inputs = await self.page.query_selector_all('input[type="text"], textarea')
                if inputs:
                    await inputs[0].click()
                    await inputs[0].fill("")
                    await inputs[0].type(title, delay=50)
                    logger.info(f"Filled title field (generic): {title}")
                    title_filled = True
            
            if not title_filled:
                logger.error("Could not fill task title")
                await self._take_screenshot("cb_title_fill_error")
                return False
            
            await asyncio.sleep(0.5)
            
            # Fill description if provided
            if description:
                desc_selectors = [
                    'textarea[placeholder*="description"]',
                    'textarea[placeholder*="Description"]',
                    '[data-testid="task-description-input"]',
                    '.task-description-input'
                ]
                
                desc_filled = False
                for selector in desc_selectors:
                    try:
                        desc_input = await self.page.query_selector(selector)
                        if desc_input:
                            await desc_input.click()
                            await desc_input.fill("")
                            await desc_input.type(description, delay=30)
                            logger.info(f"Filled description field")
                            desc_filled = True
                            break
                    except:
                        continue
                
                if not desc_filled:
                    logger.warning("Could not fill description, continuing...")
            
            await asyncio.sleep(0.5)
            
            # Look for and select assignee
            try:
                # Try to find assignee field
                assignee_selectors = [
                    'input[placeholder*="assignee"]',
                    'input[placeholder*="Assign"]',
                    '[data-testid="assignee-input"]',
                    '.assignee-input'
                ]
                
                for selector in assignee_selectors:
                    try:
                        assignee_input = await self.page.query_selector(selector)
                        if assignee_input:
                            await assignee_input.click()
                            await assignee_input.type(assignee, delay=50)
                            await asyncio.sleep(1)
                            
                            # Click on the dropdown option
                            try:
                                await self.page.click(f'text={assignee}')
                            except:
                                logger.warning(f"Could not find assignee option for {assignee}")
                            
                            logger.info(f"Set assignee to: {assignee}")
                            break
                    except:
                        continue
            except Exception as e:
                logger.warning(f"Could not set assignee: {str(e)}")
            
            await asyncio.sleep(0.5)
            
            # Set priority if available
            try:
                priority_selectors = [
                    'select[name*="priority"]',
                    '[data-testid="priority-select"]',
                    '.priority-select'
                ]
                
                for selector in priority_selectors:
                    try:
                        priority_select = await self.page.query_selector(selector)
                        if priority_select:
                            await priority_select.select_option(priority)
                            logger.info(f"Set priority to: {priority}")
                            break
                    except:
                        continue
            except Exception as e:
                logger.warning(f"Could not set priority: {str(e)}")
            
            await asyncio.sleep(0.5)
            
            # Submit the task
            submit_selectors = [
                'button:has-text("Save")',
                'button:has-text("Create")',
                'button:has-text("Add Task")',
                '[data-testid="task-save-button"]',
                '.task-save-btn'
            ]
            
            submit_clicked = False
            for selector in submit_selectors:
                try:
                    submit_button = await self.page.query_selector(selector)
                    if submit_button:
                        await submit_button.click()
                        logger.info(f"Clicked submit button: {selector}")
                        submit_clicked = True
                        break
                except:
                    continue
            
            if not submit_clicked:
                logger.error("Could not find or click submit button")
                await self._take_screenshot("cb_submit_error")
                return False
            
            # Wait for task creation confirmation
            await asyncio.sleep(2)
            
            logger.info(f"✓ Task created successfully: '{title}'")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create task: {str(e)}")
            await self._take_screenshot("cb_create_task_error")
            return False
    
    async def _is_logged_in(self) -> bool:
        """
        Check if user is logged in
        
        Returns:
            True if logged in
        """
        try:
            # Check if we're on a page that requires authentication
            # If URL contains /login or auth error, we're not logged in
            if "/login" in self.page.url:
                return False
            
            # Try to check for user profile indicator
            profile_indicators = [
                '.user-profile',
                '[data-testid="user-menu"]',
                '.navbar-user',
                'div:has-text("Mehul")',
                'div:has-text("Workspace")'
            ]
            
            for indicator in profile_indicators:
                try:
                    element = await self.page.query_selector(indicator)
                    if element:
                        return True
                except:
                    continue
            
            # If page loaded successfully and isn't login page, assume logged in
            return True
            
        except Exception as e:
            logger.warning(f"Could not verify login status: {str(e)}")
            return False
    
    async def _take_screenshot(self, name: str) -> None:
        """
        Take a screenshot for debugging
        
        Args:
            name: Screenshot name
        """
        try:
            if self.page:
                await self.page.screenshot(path=f"/home/claude/{name}.png")
                logger.info(f"Screenshot saved: {name}.png")
        except Exception as e:
            logger.warning(f"Could not take screenshot: {str(e)}")
    
    async def cleanup(self) -> None:
        """Close browser and cleanup resources"""
        try:
            if self.context:
                await self.context.close()
            if self.browser:
                await self.browser.close()
            if self.playwright:
                await self.playwright.stop()
            
            logger.info("Browser cleanup completed")
        except Exception as e:
            logger.error(f"Error during cleanup: {str(e)}")
