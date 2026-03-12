"""
Web Server for Task Automation Suite
Provides a web UI to add and create tasks
"""

import asyncio
import json
import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from task_automation_integration import TaskAutomationIntegration
from task_automation_orchestrator import Task
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Global integration instance
integration = None

def init_integration():
    """Initialize the integration with credentials from .env"""
    global integration
    
    cb_email = os.getenv('CREATEBYTES_EMAIL')
    cb_password = os.getenv('CREATEBYTES_PASSWORD')
    
    if not cb_email or not cb_password:
        logger.error("Missing CB Workspace credentials in .env file")
        return False
    
    try:
        integration = TaskAutomationIntegration(
            jira_client=None,  # We'll use Jira API directly
            cb_email=cb_email,
            cb_password=cb_password
        )
        logger.info("✅ Integration initialized successfully")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to initialize integration: {e}")
        return False

@app.route('/')
def index():
    """Serve the main UI"""
    return render_template('index.html')

@app.route('/api/status', methods=['GET'])
def get_status():
    """Get application status and credentials"""
    return jsonify({
        'status': 'ready',
        'jira': {
            'project_key': os.getenv('JIRA_PROJECT_KEY', 'YOUR_PROJECT_KEY'),
            'board_id': os.getenv('JIRA_BOARD_ID', '22'),
            'url': os.getenv('JIRA_BASE_URL', 'https://your-site.atlassian.net'),
        },
        'createbytes': {
            'project_id': os.getenv('CREATEBYTES_PROJECT_ID', 'your-cb-project-uuid'),
            'url': os.getenv('CREATEBYTES_WORKSPACE_URL', 'https://cb.workspace.createbytes.com'),
        },
        'initialized': integration is not None
    })

@app.route('/api/create-tasks', methods=['POST'])
def create_tasks():
    """Create multiple tasks"""
    try:
        data = request.get_json()
        tasks_data = data.get('tasks', [])
        
        if not tasks_data:
            return jsonify({'error': 'No tasks provided'}), 400
        
        if not integration:
            return jsonify({'error': 'Integration not initialized. Check .env file'}), 500
        
        # Convert to Task objects
        tasks = [
            Task(
                title=t.get('title', ''),
                description=t.get('description', ''),
                assignee=t.get('assignee', 'Mehul'),
                priority=t.get('priority', 'Medium'),
                labels=t.get('labels', [])
            )
            for t in tasks_data if t.get('title')
        ]
        
        if not tasks:
            return jsonify({'error': 'No valid tasks provided'}), 400
        
        logger.info(f"Creating {len(tasks)} tasks...")
        
        # Run async task creation
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        results = loop.run_until_complete(
            integration.create_tasks_from_list(
                task_list=[t.to_dict() for t in tasks],
                sync_to_jira=data.get('sync_jira', True),
                sync_to_cb=data.get('sync_cb', True)
            )
        )
        
        loop.close()
        
        return jsonify(results)
    
    except Exception as e:
        logger.error(f"Error creating tasks: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/sample-tasks', methods=['GET'])
def get_sample_tasks():
    """Get sample tasks for reference"""
    sample_tasks = [
        {
            'title': 'Design new feature',
            'description': 'Create wireframes and mockups',
            'priority': 'High'
        },
        {
            'title': 'Write API documentation',
            'description': 'Document all REST endpoints',
            'priority': 'Medium'
        },
        {
            'title': 'Setup CI/CD pipeline',
            'description': 'Configure GitHub Actions for automated testing',
            'priority': 'High'
        }
    ]
    return jsonify(sample_tasks)

if __name__ == '__main__':
    # Initialize integration
    if not init_integration():
        logger.warning("Running in demo mode - integration may not work")
    
    # Run Flask server
    print("\n" + "="*60)
    print("🚀 Task Automation Suite - Web UI")
    print("="*60)
    print("\n📍 Open your browser:")
    print("   http://localhost:5000")
    print("\n✅ Ready to create tasks!")
    print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
