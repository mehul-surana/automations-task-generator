"""
Task Automation Integration
Main entry point for bulk task creation across Jira and CB Workspace
Uses Claude's Atlassian MCP connector for Jira
Uses Playwright for CB Workspace automation
"""

import asyncio
import json
import logging
from typing import List, Dict, Optional
from task_automation_orchestrator import TaskAutomationOrchestrator, Task
from createbytes_automation import CreateBytesAutomation

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TaskAutomationIntegration:
    """
    Main integration class for bulk task creation
    Coordinates Jira (via API/MCP) and CB Workspace (via Playwright)
    """
    
    def __init__(
        self,
        jira_client,
        cb_email: str,
        cb_password: str,
        cb_base_url: str = "https://cb.workspace.createbytes.com"
    ):
        """
        Initialize the integration
        
        Args:
            jira_client: Pre-configured Jira client (from Atlassian MCP)
            cb_email: CB Workspace login email
            cb_password: CB Workspace login password
            cb_base_url: CB Workspace base URL
        """
        self.jira_client = jira_client
        self.cb_automation = CreateBytesAutomation(
            email=cb_email,
            password=cb_password,
            base_url=cb_base_url
        )
        self.orchestrator = TaskAutomationOrchestrator(
            jira_client=jira_client,
            cb_automation=cb_automation
        )
    
    async def create_tasks_from_list(
        self,
        task_list: List[Dict],
        jira_config: Optional[Dict] = None,
        cb_config: Optional[Dict] = None,
        sync_to_jira: bool = True,
        sync_to_cb: bool = True
    ) -> Dict:
        """
        Create multiple tasks from a list
        
        Args:
            task_list: List of task dictionaries with 'title' and optional 'description'
            jira_config: Jira configuration (project_key, board_id)
            cb_config: CB Workspace configuration (project_id)
            sync_to_jira: Whether to create on Jira
            sync_to_cb: Whether to create on CB Workspace
        
        Returns:
            Results dictionary
        """
        
        # Default configurations
        if jira_config is None:
            jira_config = {
                'project_key': 'YOUR_PROJECT_KEY',
                'board_id': 22
            }
        
        if cb_config is None:
            cb_config = {
                'project_id': 'your-cb-project-uuid'
            }
        
        # Initialize CB Workspace if needed
        if sync_to_cb:
            logger.info("Initializing CB Workspace browser automation...")
            if not await self.cb_automation.initialize():
                logger.error("Failed to initialize CB Workspace automation")
                return {'error': 'Failed to initialize CB Workspace'}
            
            logger.info("Authenticating with CB Workspace...")
            if not await self.cb_automation.login():
                logger.error("Failed to authenticate with CB Workspace")
                await self.cb_automation.cleanup()
                return {'error': 'Failed to authenticate with CB Workspace'}
        
        try:
            # Convert task dictionaries to Task objects
            tasks = [
                Task(
                    title=task.get('title', ''),
                    description=task.get('description', ''),
                    assignee=task.get('assignee', 'Mehul'),
                    priority=task.get('priority', 'Medium'),
                    labels=task.get('labels', [])
                )
                for task in task_list if task.get('title')
            ]
            
            if not tasks:
                logger.error("No valid tasks provided")
                return {'error': 'No valid tasks provided'}
            
            logger.info(f"Processing {len(tasks)} tasks")
            
            # Execute bulk creation
            results = await self.orchestrator.create_task_bulk(
                tasks=tasks,
                jira_project_key=jira_config.get('project_key', 'YOUR_PROJECT_KEY'),
                jira_board_id=jira_config.get('board_id', 22),
                cb_project_id=cb_config.get('project_id', 'your-cb-project-uuid'),
                sync_to_jira=sync_to_jira,
                sync_to_cb=sync_to_cb
            )
            
            return results
            
        finally:
            # Cleanup
            if sync_to_cb:
                logger.info("Cleaning up CB Workspace automation...")
                await self.cb_automation.cleanup()
    
    async def create_tasks_from_json_file(
        self,
        file_path: str,
        **kwargs
    ) -> Dict:
        """
        Create tasks from a JSON file
        
        File format:
        {
            "tasks": [
                {"title": "Task 1", "description": "Description 1"},
                {"title": "Task 2", "description": "Description 2"}
            ]
        }
        
        Args:
            file_path: Path to JSON file
            **kwargs: Additional arguments passed to create_tasks_from_list
        
        Returns:
            Results dictionary
        """
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            task_list = data.get('tasks', [])
            logger.info(f"Loaded {len(task_list)} tasks from {file_path}")
            
            return await self.create_tasks_from_list(task_list, **kwargs)
            
        except Exception as e:
            logger.error(f"Failed to read task file: {str(e)}")
            return {'error': str(e)}


async def main_demo():
    """
    Demo function showing how to use the integration
    """
    
    # Example: This would be called after Atlassian MCP is authenticated
    # For now, showing the structure
    
    sample_tasks = [
        {
            'title': 'Implement user authentication',
            'description': 'Add login/signup functionality with JWT tokens',
            'priority': 'High'
        },
        {
            'title': 'Create dashboard UI',
            'description': 'Design and implement main dashboard components',
            'priority': 'Medium'
        },
        {
            'title': 'Setup database migrations',
            'description': 'Configure and run initial database schema',
            'priority': 'High'
        },
        {
            'title': 'Write API documentation',
            'description': 'Document all REST API endpoints',
            'priority': 'Medium'
        },
        {
            'title': 'Setup CI/CD pipeline',
            'description': 'Configure GitHub Actions for automated testing and deployment',
            'priority': 'Medium'
        }
    ]
    
    # These credentials would come from environment variables in production
    CB_EMAIL = "your-email@example.com"
    CB_PASSWORD = "your-password"
    
    # This would be a real Jira client from the Atlassian MCP
    JIRA_CLIENT = None  # Would be provided by the integration
    
    if JIRA_CLIENT:
        integration = TaskAutomationIntegration(
            jira_client=JIRA_CLIENT,
            cb_email=CB_EMAIL,
            cb_password=CB_PASSWORD
        )
        
        results = await integration.create_tasks_from_list(
            sample_tasks,
            sync_to_jira=True,
            sync_to_cb=True
        )
        
        print("\n" + "="*60)
        print("TASK CREATION RESULTS")
        print("="*60)
        print(json.dumps(results, indent=2))
        print("="*60)


if __name__ == "__main__":
    print("Task Automation Integration Module")
    print("This module is designed to be integrated with Claude's Atlassian connector")
    print("\nUsage:")
    print("  1. Authenticate Atlassian connector in Claude")
    print("  2. Provide CB Workspace credentials")
    print("  3. Call create_tasks_from_list() with your task list")
    print("\nSee README.md for detailed integration instructions")
