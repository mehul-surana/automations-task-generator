# 🚀 Task Automation Suite

A powerful, production-ready automation tool that synchronizes bulk task creation across **Jira** (via REST API) and **CreateBytes Workspace** (via Playwright browser automation).

![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License MIT](https://img.shields.io/badge/License-MIT-green.svg)
![Status Active](https://img.shields.io/badge/Status-Active-brightgreen.svg)

## ✨ Features

- 🎯 **Bulk Task Creation** - Create 10-100+ tasks simultaneously across both platforms
- 🔄 **Dual-Platform Sync** - Automatically creates tasks on Jira and CB Workspace in parallel
- 📝 **Full Task Details** - Support for titles, descriptions, priorities, assignees, and labels
- 🤖 **Browser Automation** - Reliable Playwright-based automation for CB Workspace
- 📊 **Comprehensive Reporting** - Detailed success/failure tracking with timestamps
- 🔧 **Easy Configuration** - Simple JSON-based task lists and environment variables
- ⚡ **Async Processing** - Non-blocking concurrent task creation for speed
- 📸 **Error Debugging** - Automatic screenshots on failures for troubleshooting
- 🔐 **Secure Credentials** - Environment-based credential management

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
│ • Set Priorities       │   │ • Fill Task Forms      │
│ • Add Labels           │   │ • Submit Tasks         │
│ • Move to Sprints      │   │ • Screenshot Errors    │
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

## 📋 Prerequisites

- **Python 3.8+**
- **Atlassian Cloud Account** with API access
- **CB Workspace Account** with credentials
- **Modern Browser** (Chrome/Chromium for Playwright)
- **Claude.ai** with Atlassian connector enabled (optional, for advanced features)

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/mehul-surana/task-automation-suite.git
cd task-automation-suite
```

### 2. Install Dependencies
```bash
# Install Python packages
pip install -r requirements.txt

# Install Playwright browser engines
python3 -m playwright install chromium
```

### 3. Configure Credentials
```bash
# Copy the template
cp .env.example .env

# Edit with your credentials
nano .env
```

Your `.env` file should contain:
```env
CB_WORKSPACE_EMAIL=your-email@example.com
CB_WORKSPACE_PASSWORD=your-password
CB_WORKSPACE_URL=https://cb.workspace.createbytes.com
CB_PROJECT_ID=your-cb-project-uuid

JIRA_PROJECT_KEY=YOUR_PROJECT_KEY
JIRA_BOARD_ID=22
```

### 4. Enable Atlassian Connector (Optional)
In Claude.ai:
- Settings → Tools & Connectors
- Find and enable **Atlassian**
- Authenticate with your Jira account

### 5. Test with Sample Tasks
```bash
# Dry run to see what would be created
python3 quick_start.py --dry-run

# View sample task format
python3 quick_start.py sample-json
```

### 6. Create Real Tasks
```bash
# Interactive mode with sample tasks
python3 quick_start.py sample

# Load from JSON file
python3 quick_start.py file tasks.json
```

## 📖 Usage

### Using the Quick Start Script

```bash
python3 quick_start.py [COMMAND] [OPTIONS]
```

**Commands:**
- `sample` - Run with built-in sample tasks
- `file <path>` - Load tasks from JSON file
- `dry-run` - Preview without creating tasks
- `sample-json` - Display sample JSON format
- `help` - Show help message

**Options:**
- `--dry-run` - Don't actually create anything
- `--cb-only` - Create only on CB Workspace
- `--jira-only` - Create only on Jira (requires Atlassian MCP)

### Programmatic Usage

```python
import asyncio
from task_automation_integration import TaskAutomationIntegration

async def main():
    # Initialize integration
    integration = TaskAutomationIntegration(
        jira_client=jira_client,  # From Atlassian MCP
        cb_email="your-email@example.com",
        cb_password="your-password"
    )
    
    # Your tasks
    tasks = [
        {
            'title': 'Build login page',
            'description': 'Create user authentication UI',
            'priority': 'High'
        },
        {
            'title': 'Setup database',
            'description': 'Configure PostgreSQL',
            'priority': 'High'
        }
    ]
    
    # Create tasks
    results = await integration.create_tasks_from_list(
        task_list=tasks,
        sync_to_jira=True,
        sync_to_cb=True
    )
    
    print(results)

asyncio.run(main())
```

### JSON Task Format

```json
{
  "tasks": [
    {
      "title": "Task Title",
      "description": "Optional task description",
      "priority": "High|Medium|Low",
      "assignee": "Mehul",
      "labels": ["tag1", "tag2"]
    }
  ]
}
```

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
    "jira_success": [...],
    "jira_failed": [],
    "cb_success": [...],
    "cb_failed": []
  }
}
```

## 📁 Project Structure

```
task-automation-suite/
├── task_automation_integration.py     # Main integration class
├── task_automation_orchestrator.py    # Orchestration engine
├── createbytes_automation.py          # Browser automation
├── quick_start.py                     # Quick start script
├── requirements.txt                   # Dependencies
├── .env.example                       # Environment template
├── sample_tasks.json                  # Sample tasks (15 examples)
├── README.md                          # This file
├── CLAUDE_INTEGRATION_GUIDE.md        # Claude integration guide
├── SETUP_SUMMARY.md                   # Setup quick reference
└── .gitignore                         # Git ignore rules
```

## 🔧 Configuration Options

### Custom Jira Configuration
```python
jira_config = {
    'project_key': 'YOUR_KEY',
    'board_id': 123
}
```

### Custom CB Workspace Configuration
```python
cb_config = {
    'project_id': 'your-project-id-here'
}
```

## 🐛 Troubleshooting

### Issue: Playwright Not Installing
```bash
python3 -m playwright install --with-deps
```

### Issue: CB Workspace Login Fails
- Verify email and password in `.env`
- Check CB Workspace URL is correct
- Try logging in manually first
- Check if 2FA is enabled

### Issue: Jira Tasks Not Creating
- Ensure Atlassian connector is connected in Claude
- Verify Jira project key and board ID
- Check API token is still valid
- Review error logs for specific issues

### Issue: CB Workspace UI Changed
CB Workspace uses custom element selectors. If the automation fails:
1. Check the error screenshot: `cb_*.png` files
2. Update selectors in `createbytes_automation.py`
3. Submit an issue with the screenshot

For more help, see `README.md` Troubleshooting section.

## 📈 Performance

Expected performance metrics:

| Operation | Time |
|-----------|------|
| Single task | 5-10 seconds |
| 10 tasks | 60-90 seconds |
| 50 tasks | 4-6 minutes |
| 100 tasks | 8-12 minutes |

## 🔐 Security

- ✅ Use environment variables for credentials
- ✅ Never commit `.env` file to version control
- ✅ Use API tokens instead of passwords
- ✅ Implement IP whitelisting if available
- ✅ Rotate credentials every 90 days
- ✅ Audit task creation logs periodically

## 📚 Documentation

- **[README.md](README.md)** - Complete feature documentation
- **[CLAUDE_INTEGRATION_GUIDE.md](CLAUDE_INTEGRATION_GUIDE.md)** - Claude integration
- **[SETUP_SUMMARY.md](SETUP_SUMMARY.md)** - Quick reference guide

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 🐛 Reporting Issues

Found a bug? Please create an issue with:
- Description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Screenshots (especially error screenshots from `cb_*.png`)
- Your environment (Python version, OS)

## 📝 License

This project is licensed under the MIT License - see LICENSE file for details.

## 🙏 Acknowledgments

- Built with [Playwright](https://playwright.dev/) for reliable browser automation
- Integrates with [Atlassian Jira Cloud API](https://developer.atlassian.com/cloud/jira)
- Designed for [CreateBytes Workspace](https://www.createbytes.com/)

## 📞 Support

- 📖 Check the [documentation](README.md)
- 🐛 Report issues on [GitHub Issues](../../issues)
- 💬 Join discussions on [GitHub Discussions](../../discussions)

## 🚀 Roadmap

- [ ] Support for additional task management platforms
- [ ] Web UI dashboard for monitoring
- [ ] Scheduled bulk task creation
- [ ] Template-based task generation
- [ ] Advanced filtering and organization
- [ ] Webhook integration for automated triggers

## ⭐ Give it a Star!

If you find this project helpful, please give it a star! It helps others discover the project.

---

**Made with ❤️ by Mehul Surana**

[GitHub](https://github.com/mehul-surana) | [Portfolio](https://mehulsurana.com)
