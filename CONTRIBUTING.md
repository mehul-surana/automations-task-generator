# Contributing to Task Automation Suite

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

Be respectful, inclusive, and professional in all interactions.

## How to Contribute

### Reporting Bugs

Before creating bug reports, please check the issue list as you might find out that you don't need to create one. When you are creating a bug report, include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps which reproduce the problem**
- **Provide specific examples to demonstrate the steps**
- **Describe the behavior you observed after following the steps**
- **Explain which behavior you expected to see instead and why**
- **Include screenshots** (especially CB Workspace error screenshots)
- **Include your environment details** (Python version, OS, etc.)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

- **Use a clear and descriptive title**
- **Provide a step-by-step description of the suggested enhancement**
- **Provide specific examples to demonstrate the steps**
- **Describe the current behavior and explain the expected behavior**
- **Explain why this enhancement would be useful**

### Pull Requests

- Follow the Python style guide (PEP 8)
- Document any new code with docstrings
- Include appropriate comments for complex logic
- Update documentation if you change functionality
- Add tests for new features if applicable
- Keep commits atomic and write clear commit messages

## Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/task-automation-suite.git
   cd task-automation-suite
   ```

3. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. Install development dependencies:
   ```bash
   pip install -r requirements.txt
   python3 -m playwright install chromium
   ```

5. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Making Changes

### Code Style

- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Keep functions focused and concise
- Add docstrings to all functions and classes
- Comment complex logic

### Example Docstring

```python
def create_task(
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
```

## Submitting Changes

1. Commit your changes with clear messages:
   ```bash
   git commit -m "Add feature: brief description"
   ```

2. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

3. Submit a Pull Request with:
   - Clear description of changes
   - Reference to related issues
   - Screenshots if UI-related
   - Any new dependencies or breaking changes

## Pull Request Review Process

- A maintainer will review your PR
- Changes may be requested - please address them promptly
- Once approved, your PR will be merged

## Testing

While we don't have formal tests yet, please:

- Test your changes with sample tasks
- Verify both Jira and CB Workspace creation
- Check error handling works correctly
- Test with different environment configurations

## Documentation

If you add a new feature:

- Update `README.md` if it affects usage
- Update docstrings in code
- Add examples if appropriate
- Update `.env.example` if adding new configuration options

## Areas for Contribution

We're especially interested in contributions for:

- CB Workspace selector improvements (UI changes)
- Additional platform integrations (Asana, Monday.com, etc.)
- Performance optimizations
- Additional logging and debugging
- Documentation improvements
- Test coverage

## Questions?

- Check existing issues and discussions
- Create a new discussion for questions
- Email: mehul@example.com (if needed)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

Thank you for contributing! 🎉
