#!/usr/bin/env python3
"""
Quick Start Example - Task Automation Suite
This script demonstrates how to use the task automation integration
"""

import asyncio
import json
import sys
from pathlib import Path

# Import the integration
from task_automation_integration import TaskAutomationIntegration

# Sample tasks to demonstrate the system
SAMPLE_TASKS = [
    {
        'title': 'Design user authentication flow',
        'description': 'Create wireframes and user journey for login/signup',
        'priority': 'High',
        'labels': ['design', 'frontend']
    },
    {
        'title': 'Implement JWT token system',
        'description': 'Backend authentication using JWT tokens with refresh logic',
        'priority': 'High',
        'labels': ['backend', 'security']
    },
    {
        'title': 'Create dashboard layout',
        'description': 'Build responsive dashboard UI with React components',
        'priority': 'Medium',
        'labels': ['frontend', 'ui']
    },
    {
        'title': 'Setup PostgreSQL database',
        'description': 'Configure database, run migrations, setup connection pooling',
        'priority': 'High',
        'labels': ['backend', 'database']
    },
    {
        'title': 'API documentation',
        'description': 'Write OpenAPI/Swagger documentation for all endpoints',
        'priority': 'Medium',
        'labels': ['documentation']
    },
    {
        'title': 'Setup CI/CD pipeline',
        'description': 'Configure GitHub Actions for automated testing and deployment',
        'priority': 'Medium',
        'labels': ['devops']
    },
    {
        'title': 'User profile page',
        'description': 'Build user profile view with edit capabilities',
        'priority': 'Medium',
        'labels': ['frontend', 'feature']
    },
    {
        'title': 'Email notification system',
        'description': 'Implement email notifications using SendGrid or similar',
        'priority': 'Low',
        'labels': ['backend', 'notifications']
    }
]


def load_from_json(file_path: str):
    """Load tasks from JSON file"""
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        return data.get('tasks', [])
    except Exception as e:
        print(f"❌ Error loading JSON file: {e}")
        return None


def print_sample_json():
    """Print sample JSON format"""
    sample = {
        'tasks': SAMPLE_TASKS
    }
    print(json.dumps(sample, indent=2))


async def run_automation(
    tasks,
    cb_email: str,
    cb_password: str,
    jira_client=None,
    sync_jira: bool = True,
    sync_cb: bool = True,
    dry_run: bool = False
):
    """
    Run the task automation
    
    Args:
        tasks: List of task dictionaries
        cb_email: CB Workspace email
        cb_password: CB Workspace password
        jira_client: Pre-configured Jira client (from Atlassian MCP)
        sync_jira: Whether to sync to Jira
        sync_cb: Whether to sync to CB Workspace
        dry_run: If True, just show what would be created without creating
    """
    
    if dry_run:
        print("\n📋 DRY RUN MODE - No tasks will be created\n")
        print("Tasks that would be created:")
        print("-" * 60)
        for i, task in enumerate(tasks, 1):
            print(f"\n{i}. {task['title']}")
            if task.get('description'):
                print(f"   Description: {task['description']}")
            if task.get('priority'):
                print(f"   Priority: {task['priority']}")
            if task.get('labels'):
                print(f"   Labels: {', '.join(task['labels'])}")
        print("\n" + "-" * 60)
        return
    
    # Note: In production, jira_client would be provided by Claude's Atlassian connector
    if not jira_client:
        print("⚠️  Note: Jira client not provided")
        print("   In Claude, the Atlassian connector would provide this automatically")
        print("   For now, we'll create tasks only on CB Workspace")
        sync_jira = False
    
    try:
        # Initialize integration
        print("\n🚀 Initializing Task Automation Suite...")
        integration = TaskAutomationIntegration(
            jira_client=jira_client,
            cb_email=cb_email,
            cb_password=cb_password
        )
        
        print(f"📝 Creating {len(tasks)} tasks...")
        print(f"   📌 Jira sync: {'✓' if sync_jira else '✗'}")
        print(f"   📌 CB Workspace sync: {'✓' if sync_cb else '✗'}")
        
        # Create tasks
        results = await integration.create_tasks_from_list(
            task_list=tasks,
            sync_to_jira=sync_jira,
            sync_to_cb=sync_cb
        )
        
        # Print results
        print_results(results)
        
        return results
        
    except Exception as e:
        print(f"❌ Error during task creation: {e}")
        import traceback
        traceback.print_exc()
        return None


def print_results(results):
    """Print formatted results"""
    print("\n" + "=" * 60)
    print("✅ TASK CREATION COMPLETE")
    print("=" * 60)
    
    if isinstance(results, dict) and 'summary' in results:
        summary = results['summary']
        
        # Jira results
        jira = summary.get('jira', {})
        print(f"\n📌 Jira Results:")
        print(f"   ✓ Successful: {jira.get('successful', 0)}")
        print(f"   ✗ Failed: {jira.get('failed', 0)}")
        
        # CB Workspace results
        cb = summary.get('cb_workspace', {})
        print(f"\n🔷 CB Workspace Results:")
        print(f"   ✓ Successful: {cb.get('successful', 0)}")
        print(f"   ✗ Failed: {cb.get('failed', 0)}")
        
        total = summary.get('total_tasks_processed', 0)
        print(f"\n📊 Total Tasks: {total}")
        
        # Print detailed failures if any
        details = results.get('details', {})
        
        failed_jira = details.get('jira_failed', [])
        if failed_jira:
            print(f"\n⚠️  Jira Failures:")
            for failure in failed_jira:
                print(f"   • {failure['title']}: {failure.get('error', 'Unknown error')}")
        
        failed_cb = details.get('cb_failed', [])
        if failed_cb:
            print(f"\n⚠️  CB Workspace Failures:")
            for failure in failed_cb:
                print(f"   • {failure['title']}: {failure.get('error', 'Unknown error')}")
    
    print("\n" + "=" * 60)


def print_usage():
    """Print usage instructions"""
    usage = """
╔════════════════════════════════════════════════════════════════╗
║   Task Automation Suite - Quick Start Example                 ║
╚════════════════════════════════════════════════════════════════╝

Usage:
  python3 quick_start.py [COMMAND] [OPTIONS]

Commands:
  sample              Run with sample tasks (default)
  file <path>         Load tasks from JSON file
  dry-run             Show what would be created without creating
  sample-json         Print sample JSON format

Options:
  --cb-email TEXT     CB Workspace email (required for real run)
  --cb-password TEXT  CB Workspace password (required for real run)
  --jira-only         Create only on Jira (requires Atlassian MCP)
  --cb-only           Create only on CB Workspace
  --dry-run           Don't actually create anything

Examples:
  # Dry run with sample tasks
  python3 quick_start.py --dry-run

  # Create sample tasks (you'll be prompted for credentials)
  python3 quick_start.py sample

  # Load from file
  python3 quick_start.py file tasks.json

  # Show sample JSON format
  python3 quick_start.py sample-json

Note:
  For production use with Jira, you'll need the Atlassian MCP 
  connector enabled in Claude, which will provide the jira_client.

════════════════════════════════════════════════════════════════
"""
    print(usage)


async def main():
    """Main entry point"""
    
    args = sys.argv[1:] if len(sys.argv) > 1 else []
    
    # Parse arguments
    command = args[0] if args else 'sample'
    tasks = None
    dry_run = '--dry-run' in args
    cb_only = '--cb-only' in args
    jira_only = '--jira-only' in args
    
    # Load tasks based on command
    if command == 'help' or command == '--help' or command == '-h':
        print_usage()
        return
    
    elif command == 'sample-json':
        print("\n📄 Sample JSON Format:\n")
        print_sample_json()
        return
    
    elif command == 'sample':
        print("\n📋 Using sample tasks...")
        tasks = SAMPLE_TASKS
    
    elif command == 'file':
        if len(args) < 2:
            print("❌ Error: Please provide file path")
            print("   Usage: python3 quick_start.py file <path>")
            return
        file_path = args[1]
        print(f"\n📂 Loading tasks from {file_path}...")
        tasks = load_from_json(file_path)
        if tasks is None:
            return
    
    else:
        print(f"❌ Unknown command: {command}")
        print_usage()
        return
    
    if not tasks:
        print("❌ No tasks to process")
        return
    
    # Run automation
    if dry_run:
        print(f"\n📋 DRY RUN - {len(tasks)} tasks")
        for task in tasks:
            print(f"  • {task['title']}")
        return
    
    # Get credentials
    print("\n🔐 CB Workspace Credentials Required")
    cb_email = input("Enter CB Workspace email: ").strip()
    cb_password = input("Enter CB Workspace password: ").strip()
    
    if not cb_email or not cb_password:
        print("❌ Email and password are required")
        return
    
    # Run automation
    await run_automation(
        tasks=tasks,
        cb_email=cb_email,
        cb_password=cb_password,
        jira_client=None,  # Would be provided by Atlassian MCP in Claude
        sync_jira=not cb_only and jira_only is False,
        sync_cb=not jira_only and cb_only is False,
        dry_run=dry_run
    )


if __name__ == '__main__':
    asyncio.run(main())
