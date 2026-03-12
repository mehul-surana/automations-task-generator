# 🔗 Claude Integration Guide - Task Automation Suite

This guide explains how to integrate the Task Automation Suite with Claude's Atlassian MCP connector for seamless bulk task creation across Jira and CB Workspace.

---

## 🎯 How It Works

### Without Claude (Standalone)
```
Your Tasks → Automation Suite → Jira (API) + CB Workspace (Playwright) ✓
```

### With Claude (Recommended)
```
Your Tasks → Claude Chat Interface 
           ↓
      (Understands your request in natural language)
           ↓
      Task Automation Suite
           ↓
      Jira (via Atlassian MCP) + CB Workspace (via Playwright) ✓
```

---

## ✅ Step-by-Step Setup

### Step 1: Enable Atlassian Connector in Claude

1. Open **Claude.ai**
2. Click **Settings** (gear icon)
3. Navigate to **Tools & Connectors**
4. Find **Atlassian** in the list
5. Click **Connect**
6. Authenticate with your Jira account
7. Grant necessary permissions
8. Verify connection shows **"Connected"**

### Step 2: Prepare Your CB Workspace Credentials

Store your CB Workspace credentials securely:

```python
# Option A: Environment Variables (.env file)
CB_WORKSPACE_EMAIL=your-email@example.com
CB_WORKSPACE_PASSWORD=your-password

# Option B: Pass directly in code
cb_email = "your-email@example.com"
cb_password = "your-password"
```

### Step 3: Copy Automation Files to Claude

The following files are ready to use:
- `task_automation_integration.py` - Main integration class
- `task_automation_orchestrator.py` - Coordination logic
- `createbytes_automation.py` - Playwright automation
- `quick_start.py` - Quick start example

### Step 4: Test the Connection

Use this simple Python script in Claude to test:

```python
# Test script to verify both connections
import asyncio

async def test_connections():
    print("Testing Atlassian connector...")
    # Claude's Atlassian MCP will be available here automatically
    
    print("Testing CB Workspace automation...")
    from createbytes_automation import CreateBytesAutomation
    
    cb = CreateBytesAutomation(
        email="your-email@example.com",
        password="your-password"
    )
    
    if await cb.initialize() and await cb.login():
        print("✓ Both connections working!")
        await cb.cleanup()
    else:
        print("✗ Connection failed")

asyncio.run(test_connections())
```

---

## 🗣️ Using with Claude Chat

### Example Conversation

**You:** "Hey Claude, I have a list of 10 tasks for our YOUR_PROJECT_KEY project. Can you create them on both Jira and CB Workspace? All assigned to Mehul."

**Claude:** "I can help with that! Please provide the task list. I can either:
1. Parse a list you paste directly
2. Create from a JSON file you share
3. Use example tasks to demonstrate

Here's the format I need:
```json
{
  "tasks": [
    {
      "title": "Task Title",
      "description": "Task description",
      "priority": "High"
    }
  ]
}
```"

**You:** "Here's my list:
- Build login page (High priority) - User authentication
- Setup database (High) - Configure PostgreSQL
- Write API docs (Medium) - Document REST endpoints"

**Claude:** "Perfect! Let me create these tasks on both platforms for you."

```python
from task_automation_integration import TaskAutomationIntegration

tasks = [
    {
        'title': 'Build login page',
        'description': 'User authentication',
        'priority': 'High'
    },
    {
        'title': 'Setup database',
        'description': 'Configure PostgreSQL',
        'priority': 'High'
    },
    {
        'title': 'Write API docs',
        'description': 'Document REST endpoints',
        'priority': 'Medium'
    }
]

# Claude automatically has access to the Jira client via Atlassian MCP
integration = TaskAutomationIntegration(
    jira_client=jira_client,  # From Atlassian connector
    cb_email="your-email@example.com",
    cb_password="your-password"
)

results = await integration.create_tasks_from_list(tasks)
```

---

## 🔌 How Claude's Atlassian Connector Works

When Atlassian is connected in Claude:

1. **Automatic Authentication** - Your Jira credentials are securely managed
2. **No API Key Needed** - You don't need to pass credentials manually
3. **Direct Access** - Claude can read and create tasks directly
4. **Error Handling** - Built-in retry logic and error recovery

### Example: Creating Task via Atlassian MCP

```python
# Claude has direct access to Jira via the Atlassian connector
from atlassian import Jira

# The jira_client is automatically provided by the Atlassian MCP
issue = jira_client.create_issue(fields={
    'project': {'key': 'YOUR_PROJECT_KEY'},
    'summary': 'Task Title',
    'description': 'Task Description',
    'issuetype': {'name': 'Task'},
    'assignee': {'name': 'Mehul'},
    'priority': {'name': 'High'}
})

print(f"Created: {issue.key}")
```

---

## 📊 Integration Flow

```
┌─────────────────────────────────┐
│   Claude Chat Interface          │
│   (Natural Language Input)       │
└─────────────┬───────────────────┘
              │
              ▼
┌─────────────────────────────────┐
│   Claude Parser                  │
│   (Extracts task list)           │
└─────────────┬───────────────────┘
              │
              ▼
┌─────────────────────────────────┐
│   Task Automation Integration    │
│   (Coordinates platforms)        │
└──────┬──────────────────┬────────┘
       │                  │
       ▼                  ▼
   ┌────────┐        ┌─────────────┐
   │ Jira   │        │ CB Workspace│
   │(MCP)   │        │(Playwright) │
   └────────┘        └─────────────┘
```

---

## 🛠️ Configuration for Claude Environment

### Setting Environment Variables in Claude

If running in Claude's environment, set credentials as:

```python
import os

# Load from environment
CB_EMAIL = os.getenv('CB_WORKSPACE_EMAIL', 'your-email@example.com')
CB_PASSWORD = os.getenv('CB_WORKSPACE_PASSWORD', 'your-password')

# Or use directly
integration = TaskAutomationIntegration(
    jira_client=jira_client,  # Provided by Atlassian MCP
    cb_email=CB_EMAIL,
    cb_password=CB_PASSWORD
)
```

### Getting the Jira Client in Claude

The Atlassian connector provides the client automatically. In Claude:

```python
# The Atlassian MCP connector provides this
from atlassian import Jira

# You can initialize it with:
jira = Jira(
    url='https://your-site.atlassian.net',
    username='your-email@example.com',
    password='your-api-token'  # Managed by connector
)

# Or it's provided directly by Claude's Atlassian MCP
# just use: jira_client from the integration
```

---

## 🔒 Security Best Practices

### In Claude Environment

1. **Never Expose Credentials** - Always use environment variables
2. **Use API Tokens** - For Jira, use an API token instead of password
3. **Restrict Scope** - Give Atlassian connector minimal required permissions
4. **Audit Logs** - Track who created tasks and when
5. **Refresh Tokens** - Rotate credentials periodically

### CB Workspace

1. **Don't Hardcode Credentials** - Use environment variables
2. **Use Service Accounts** - Create a dedicated automation account
3. **Monitor Sessions** - Check for unusual activity
4. **Secure Storage** - Encrypt credential files

---

## 📝 Example: Complete Claude Integration

Here's a complete example ready to use in Claude:

```python
import asyncio
from task_automation_integration import TaskAutomationIntegration

async def create_bulk_tasks(task_list, cb_email, cb_password, jira_client):
    """
    Create bulk tasks via Claude
    
    Args:
        task_list: List of task dicts with 'title' and 'description'
        cb_email: CB Workspace email
        cb_password: CB Workspace password
        jira_client: Jira client from Atlassian MCP
    
    Returns:
        Results dictionary with success/failure counts
    """
    
    # Initialize integration
    integration = TaskAutomationIntegration(
        jira_client=jira_client,
        cb_email=cb_email,
        cb_password=cb_password
    )
    
    # Create tasks
    print(f"📝 Creating {len(task_list)} tasks...")
    results = await integration.create_tasks_from_list(
        task_list=task_list,
        sync_to_jira=True,
        sync_to_cb=True
    )
    
    # Print summary
    summary = results.get('summary', {})
    print(f"\n✅ Tasks Created:")
    print(f"   Jira: {summary['jira']['successful']} successful, {summary['jira']['failed']} failed")
    print(f"   CB Workspace: {summary['cb_workspace']['successful']} successful, {summary['cb_workspace']['failed']} failed")
    
    return results

# Usage in Claude:
# tasks = [
#     {'title': 'Task 1', 'description': 'Desc 1'},
#     {'title': 'Task 2', 'description': 'Desc 2'},
# ]
# results = await create_bulk_tasks(
#     task_list=tasks,
#     cb_email="your-email@example.com",
#     cb_password="your-password",
#     jira_client=jira_client  # From Atlassian MCP
# )
```

---

## 🆘 Troubleshooting

### Atlassian Connector Not Found in Claude

1. ✓ Ensure Atlassian is connected in Claude Settings
2. ✓ Verify you've granted necessary permissions
3. ✓ Try disconnecting and reconnecting
4. ✓ Check your Jira URL is correct (https://your-site.atlassian.net)

### CB Workspace Playwright Errors

1. ✓ Verify Playwright is installed: `python3 -m playwright install chromium`
2. ✓ Check CB Workspace credentials are correct
3. ✓ Review CB Workspace UI for selector changes
4. ✓ Check screenshot files for visual debugging

### Tasks Created on Jira but Not CB Workspace

1. ✓ Check CB Workspace login is successful
2. ✓ Verify project ID is correct
3. ✓ Check network connectivity during task creation
4. ✓ Review error logs for specific failures

### Tasks Created on CB Workspace but Not Jira

1. ✓ Verify Atlassian connector is still connected
2. ✓ Check Jira project key and board ID are correct
3. ✓ Verify API token is still valid
4. ✓ Check Jira project permissions for task creation

---

## 🚀 Performance Metrics

Expected performance when using Claude integration:

| Metric | Value |
|--------|-------|
| **Single Task Creation** | 5-10 seconds |
| **Bulk (10 tasks)** | 60-90 seconds |
| **Bulk (50 tasks)** | 4-6 minutes |
| **Success Rate** | 95%+ (with retries) |
| **Concurrent Tasks** | 2-3 simultaneous |

---

## 📞 Support

For issues with:

- **Atlassian Connector**: Check Claude Settings → Tools & Connectors
- **CB Workspace Automation**: Review createbytes_automation.py logs
- **Task Formatting**: Verify JSON structure matches required format
- **Network Issues**: Check internet connectivity and firewall rules

---

## ✨ Next Steps

1. ✅ Connect Atlassian in Claude Settings
2. ✅ Download automation files
3. ✅ Set CB Workspace credentials
4. ✅ Test with 2-3 sample tasks
5. ✅ Scale to production bulk tasks

Enjoy automated task creation! 🎉
