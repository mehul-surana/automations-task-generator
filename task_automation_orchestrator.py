"""
Task Automation Orchestrator
Coordinates task creation across Jira (via API) and CreateBytes (via Playwright)
"""

import asyncio
import logging
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class Task:
    """Represents a task to be created"""
    title: str
    description: str = ""
    assignee: str = "Mehul"
    priority: str = "Medium"
    labels: List[str] = None
    
    def __post_init__(self):
        if self.labels is None:
            self.labels = []
    
    def to_dict(self) -> Dict:
        return {
            'title': self.title,
            'description': self.description,
            'assignee': self.assignee,
            'priority': self.priority,
            'labels': self.labels
        }


class TaskAutomationOrchestrator:
    """
    Orchestrates task creation across multiple platforms
    """
    
    def __init__(self, jira_client=None, cb_automation=None):
        """
        Initialize the orchestrator
        
        Args:
            jira_client: Jira API client instance
            cb_automation: CreateBytes Playwright automation instance
        """
        self.jira_client = jira_client
        self.cb_automation = cb_automation
        self.results = {
            'jira_success': [],
            'jira_failed': [],
            'cb_success': [],
            'cb_failed': []
        }
    
    async def create_task_bulk(
        self,
        tasks: List[Task],
        jira_project_key: str = "YOUR_PROJECT_KEY",
        jira_board_id: int = 22,
        cb_project_id: str = "your-cb-project-uuid",
        sync_to_jira: bool = True,
        sync_to_cb: bool = True
    ) -> Dict:
        """
        Create multiple tasks across platforms
        
        Args:
            tasks: List of Task objects
            jira_project_key: Jira project key (e.g., "YOUR_PROJECT_KEY")
            jira_board_id: Jira board ID
            cb_project_id: CreateBytes project ID
            sync_to_jira: Whether to sync to Jira
            sync_to_cb: Whether to sync to CB Workspace
        
        Returns:
            Dictionary containing results for each platform
        """
        logger.info(f"Starting bulk task creation for {len(tasks)} tasks")
        logger.info(f"Jira sync: {sync_to_jira}, CB sync: {sync_to_cb}")
        
        tasks_to_process = tasks.copy()
        
        # Create tasks on Jira
        if sync_to_jira and self.jira_client:
            logger.info("Creating tasks on Jira...")
            await self._create_jira_tasks(
                tasks_to_process,
                jira_project_key,
                jira_board_id
            )
        
        # Create tasks on CB Workspace
        if sync_to_cb and self.cb_automation:
            logger.info("Creating tasks on CB Workspace...")
            await self._create_cb_tasks(
                tasks_to_process,
                cb_project_id
            )
        
        logger.info("Bulk task creation completed")
        return self._generate_report()
    
    async def _create_jira_tasks(
        self,
        tasks: List[Task],
        project_key: str,
        board_id: int
    ) -> None:
        """Create tasks on Jira"""
        for task in tasks:
            try:
                issue_dict = {
                    'project': {'key': project_key},
                    'summary': task.title,
                    'description': task.description,
                    'issuetype': {'name': 'Task'},
                    'assignee': {'name': task.assignee},
                    'priority': {'name': task.priority},
                }
                
                # Create issue
                issue = self.jira_client.create_issue(fields=issue_dict)
                logger.info(f"✓ Created Jira task: {issue.key} - {task.title}")
                self.results['jira_success'].append({
                    'title': task.title,
                    'issue_key': issue.key,
                    'timestamp': datetime.now().isoformat()
                })
                
            except Exception as e:
                logger.error(f"✗ Failed to create Jira task '{task.title}': {str(e)}")
                self.results['jira_failed'].append({
                    'title': task.title,
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                })
    
    async def _create_cb_tasks(
        self,
        tasks: List[Task],
        project_id: str
    ) -> None:
        """Create tasks on CB Workspace"""
        for task in tasks:
            try:
                success = await self.cb_automation.create_task(
                    project_id=project_id,
                    title=task.title,
                    description=task.description,
                    assignee=task.assignee,
                    priority=task.priority
                )
                
                if success:
                    logger.info(f"✓ Created CB Workspace task: {task.title}")
                    self.results['cb_success'].append({
                        'title': task.title,
                        'timestamp': datetime.now().isoformat()
                    })
                else:
                    raise Exception("Task creation returned False")
                    
            except Exception as e:
                logger.error(f"✗ Failed to create CB Workspace task '{task.title}': {str(e)}")
                self.results['cb_failed'].append({
                    'title': task.title,
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                })
    
    def _generate_report(self) -> Dict:
        """Generate a summary report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'jira': {
                    'successful': len(self.results['jira_success']),
                    'failed': len(self.results['jira_failed'])
                },
                'cb_workspace': {
                    'successful': len(self.results['cb_success']),
                    'failed': len(self.results['cb_failed'])
                },
                'total_tasks_processed': (
                    len(self.results['jira_success']) +
                    len(self.results['jira_failed']) +
                    len(self.results['cb_success']) +
                    len(self.results['cb_failed'])
                ) // 2  # Divide by 2 since each task is counted twice
            },
            'details': self.results
        }
        
        logger.info("\n" + "="*60)
        logger.info("TASK CREATION REPORT")
        logger.info("="*60)
        logger.info(f"Jira: {report['summary']['jira']['successful']} successful, {report['summary']['jira']['failed']} failed")
        logger.info(f"CB Workspace: {report['summary']['cb_workspace']['successful']} successful, {report['summary']['cb_workspace']['failed']} failed")
        logger.info("="*60)
        
        return report
    
    def reset_results(self) -> None:
        """Reset results tracking"""
        self.results = {
            'jira_success': [],
            'jira_failed': [],
            'cb_success': [],
            'cb_failed': []
        }
