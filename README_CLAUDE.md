# 🚀 Task Automation Suite - Jira & CB Workspace Integration

A powerful, production-ready automation tool that synchronizes bulk task creation across **Jira** (via Atlassian MCP connector) and **CreateBytes Workspace** (via Playwright browser automation).

---

## ✨ Features

✅ **Dual-Platform Sync**: Create tasks on Jira and CB Workspace simultaneously  
✅ **Bulk Task Creation**: Process hundreds of tasks automatically  
✅ **Full Task Details**: Titles, descriptions, assignees, priorities, and labels  
✅ **Unified Assignments**: All tasks automatically assigned to "Mehul"  
✅ **Error Handling & Reporting**: Detailed logs and failure tracking  
✅ **Playwright Automation**: Resilient browser automation with smart retries  
✅ **Async/Await**: Non-blocking concurrent task creation  
✅ **Screenshot Debugging**: Automatic error screenshots for troubleshooting  

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│         Task Automation Integration                 │
│  (Main entry point - coordinates both platforms)    │
└────────┬──────────────────────────────┬─────────────┘
         │                              │
         ▼                              ▼
┌────────────────────────┐   ┌────────────────────────┐
│  Atlassian MCP         │   │  Playwright Browser    │
│  (Jira API)            │   │  (CB Workspace)        │
├────────────────────────┤   ├────────────────────────┤
│ • Create Issues        │   │ • Login Authentication │
│ • Assign Tasks         │   │ • Navigate to Board    │
│ • Set Priorities       │   │ • Click UI Elements    │
│ • Add Labels           │   │ • Fill Forms           │
│ • Move to Sprints      │   │ • Submit Tasks         │
└────────┬───────────────┘   └────────┬───────────────┘
         │                              │
         └──────────────┬───────────────┘
                        ▼
              ┌──────────────────────┐
              │   Orchestrator       │
              │  (Coordination &     │
              │   Error Handling)    │
              └──────────────────────┘
```

---

## 📋 Prerequisites

- **Python 3.8+**
- **Atlassian Cloud Account** with API access
- **CB Workspace Account** with credentials
- **Modern Browser** (Chrome/Chromium for Playwright)
- **Claude.ai** with Atlassian connector enabled

---

## 🔧 Setup & Installation

### Step 1: Install Dependencies

```bash
# Install Python packages
pip install -r requirements.txt

# Install Playwright browser engines
python3 -m playwright install chromium
```

### Step 2: Enable Atlassian Connector in Claude

1. Open Claude.ai
2. Click **Settings** → **Tools & Connectors**
3. Find and enable **Atlassian**
4. Authenticate with your Jira account
5. Verify connection is successful

### Step 3: Configure CB Workspace Credentials

Create a `.env` file in the same directory:

```bash
# .env
CB_WORKSPACE_EMAIL=your-email@example.com
CB_WORKSPACE_PASSWORD=your-password
CB_WORKSPACE_URL=https://cb.workspace.createbytes.com
```

Or pass credentials directly in code:

```python
CB_EMAIL = "your-email@example.com"
CB_PASSWORD = "your-password"
```

### Step 4: Verify Setup

```bash
# Test Playwright installation
python3 -m playwright install --with-deps

# Quick connectivity test (optional)
python3 -c "from playwright.async_api import async_playwright; print('Playwright ready!')"
```

---

## 📝 Usage Guide

### Option 1: Simple Task List (Recommended)

```python
import asyncio
from task_automation_integration import TaskAutomationIntegration

# Your tasks
tasks = [
    {
        'title': 'Build login page',
        'description': 'Create user authentication UI',
        'priority': 'High'
    },
    {
        'title': 'Setup database',
        'description': 'Configure PostgreSQL and migrations',
        'priority': 'High'
    },
    {
        'title': 'Write API docs',
        'description': 'Document all REST endpoints',
        'priority': 'Medium'
    }
]

async def main():
    # Initialize with your credentials
    integration = TaskAutomationIntegration(
        jira_client=jira_client,  # From Atlassian MCP
        cb_email="your-email@example.com",
        cb_password="your-password"
    )
    
    # Create tasks on both platforms
    results = await integration.create_tasks_from_list(
        task_list=tasks,
        sync_to_jira=True,
        sync_to_cb=True
    )
    
    print(results)

asyncio.run(main())
```

### Option 2: Load from JSON File

Create a `tasks.json` file:

```json
{
  "tasks": [
    {
      "title": "Task 1",
      "description": "Description for task 1",
      "priority": "High",
      "labels": ["backend", "urgent"]
    },
    {
      "title": "Task 2",
      "description": "Description for task 2",
      "priority": "Medium",
      "labels": ["frontend"]
    }
  ]
}
```

Then load and create:

```python
results = await integration.create_tasks_from_json_file(
    file_path='tasks.json'
)
```

### Option 3: Custom Configuration

```python
# Custom Jira and CB Workspace settings
results = await integration.create_tasks_from_list(
    task_list=tasks,
    jira_config={
        'project_key': 'YOUR_PROJECT_KEY',
        'board_id': 22
    },
    cb_config={
        'project_id': 'your-cb-project-uuid'
    },
    sync_to_jira=True,
    sync_to_cb=True
)
```

---

## 📊 Results Format

After task creation, you'll receive a detailed report:

```json
{
  "timestamp": "2024-03-13T10:30:45.123456",
  "summary": {
    "jira": {
      "successful": 5,
      "failed": 0
    },
    "cb_workspace": {
      "successful": 5,
      "failed": 0
    },
    "total_tasks_processed": 5
  },
  "details": {
    "jira_success": [
      {
        "title": "Build login page",
        "issue_key": "YOUR_PROJECT_KEY-123",
        "timestamp": "2024-03-13T10:30:45.123456"
      }
    ],
    "jira_failed": [],
    "cb_success": [
      {
        "title": "Build login page",
        "timestamp": "2024-03-13T10:30:46.789012"
      }
    ],
    "cb_failed": []
  }
}
```

---

## 🔑 Key Classes & Methods

### TaskAutomationIntegration

Main class for coordinating task creation across platforms.

**Methods:**
- `__init__(jira_client, cb_email, cb_password, cb_base_url)` - Initialize
- `create_tasks_from_list(task_list, jira_config, cb_config, sync_to_jira, sync_to_cb)` - Create tasks from list
- `create_tasks_from_json_file(file_path, **kwargs)` - Create tasks from JSON file

### CreateBytesAutomation

Handles Playwright-based browser automation for CB Workspace.

**Methods:**
- `initialize()` - Launch browser
- `login()` - Authenticate with CB Workspace
- `navigate_to_project(project_id)` - Navigate to kanban board
- `create_task(project_id, title, description, assignee, priority)` - Create single task
- `cleanup()` - Close browser and cleanup

### Task (Dataclass)

Represents a single task.

**Fields:**
- `title` (str) - Task title
- `description` (str) - Task description (optional)
- `assignee` (str) - Assignee name (default: "Mehul")
- `priority` (str) - Priority level (Low/Medium/High)
- `labels` (List[str]) - Task labels (optional)

---

## 🐛 Debugging & Troubleshooting

### Enable Verbose Logging

```python
import logging

# Set logging to DEBUG
logging.basicConfig(level=logging.DEBUG)
```

### Check Screenshots on Error

When Playwright encounters an error, it automatically saves a screenshot:
- `cb_login_error.png` - Login failed
- `cb_navigation_error.png` - Navigation failed
- `cb_add_task_button_error.png` - Can't find add task button
- `cb_submit_error.png` - Submit failed
- `cb_create_task_error.png` - General create task error

Check these in your working directory for visual debugging.

### Common Issues

| Issue | Solution |
|-------|----------|
| **Playwright not installing** | Run `python3 -m playwright install --with-deps` |
| **Login fails** | Verify credentials in `.env` file |
| **Can't find task button** | Check CB Workspace UI for element selectors |
| **Tasks not appearing on Jira** | Verify Atlassian connector is connected |
| **Session expires during bulk creation** | Increase wait times or reduce batch size |

---

## ⚙️ Advanced Configuration

### Increase Retry Attempts

In `createbytes_automation.py`, adjust timeouts:

```python
await self.page.wait_for_selector(selector, timeout=15000)  # 15 seconds
```

### Headful Mode (See Browser)

For debugging, run browser with UI:

```python
# In createbytes_automation.py
self.browser = await self.playwright.chromium.launch(headless=False)
```

### Batch Processing

For large task lists, process in batches:

```python
batch_size = 10
for i in range(0, len(tasks), batch_size):
    batch = tasks[i:i+batch_size]
    results = await integration.create_tasks_from_list(batch)
    # Log batch results
```

---

## 📁 File Structure

```
├── task_automation_integration.py    # Main integration class
├── task_automation_orchestrator.py   # Coordination & error handling
├── createbytes_automation.py         # Playwright automation
├── requirements.txt                  # Python dependencies
├── .env                              # CB Workspace credentials
└── README.md                         # This file
```

---

## 🔐 Security Notes

⚠️ **Never commit `.env` file to version control**

```bash
# Add to .gitignore
echo ".env" >> .gitignore
```

✅ **Best Practices:**
- Use environment variables for credentials
- Rotate API tokens regularly
- Use service accounts for automation
- Audit task creation logs periodically
- Implement IP whitelisting if available

---

## 🚀 Performance Tips

1. **Batch Creation**: Process 10-50 tasks per run for reliability
2. **Headless Mode**: Keep Playwright headless for speed (default)
3. **Error Recovery**: Failed tasks are logged and can be retried
4. **Async Processing**: Tasks are created concurrently for efficiency
5. **Network Optimization**: Ensure stable internet connection for Playwright

---

## 📞 Support & Issues

If you encounter issues:

1. Check the **Debugging & Troubleshooting** section above
2. Review **log output** for detailed error messages
3. Check **screenshots** in your working directory
4. Verify **credentials** are correct
5. Ensure **network connectivity** is stable
6. Try **one task at a time** to isolate problems

---

## 📝 License

This automation suite is designed for internal use with Jira and CreateBytes platforms.

---

## 🎯 Next Steps

1. ✅ Install dependencies: `pip install -r requirements.txt`
2. ✅ Enable Atlassian connector in Claude
3. ✅ Configure CB Workspace credentials in `.env`
4. ✅ Test with sample 3-5 tasks
5. ✅ Scale to bulk operations

Happy automating! 🎉
