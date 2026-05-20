# Contributing to Gitish

Thank you for your interest in contributing to Gitish! This document provides guidelines and instructions for contributing.

## 🚀 Quick Start

1. Fork the repository
2. Clone your fork: `git clone https://github.com/rifat-simoom/gitish.git`
3. Create a branch: `git checkout -b feature/your-feature`
4. Make your changes
5. Run tests: `make test`
6. Format code: `make format`
7. Commit: `git commit -m "Add your feature"`
8. Push: `git push origin feature/your-feature`
9. Create a Pull Request

## 📋 Development Setup

### Prerequisites

- Python 3.6 or higher
- pip
- git

### Installation

```bash
# Clone your fork
git clone https://github.com/rifat-simoom/gitish.git
cd gitish

# Install in development mode
pip install -e ".[dev]"
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
make test

# Run specific test file
pytest tests/test_github_api.py

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=gitish --cov-report=html
```

### Writing Tests

- Place tests in the `tests/` directory
- Name test files `test_*.py`
- Name test functions `test_*`
- Use pytest fixtures from `conftest.py`
- Aim for high code coverage

Example test:

```python
def test_resolve_repository_alias():
    """Test resolving repository alias"""
    result = resolve_repository('symfony')
    assert result == 'symfony/symfony'
```

## 📝 Code Style

### Formatting

We use Black for code formatting and isort for import sorting:

```bash
# Format all code
make format

# Or manually
black gitish tests
isort gitish tests
```

### Linting

```bash
# Run all linters
make lint

# Or individually
flake8 gitish tests
mypy gitish
```

### Style Guidelines

- **Line length**: 100 characters (Black default)
- **Imports**: Sorted with isort
- **Type hints**: Use where appropriate
- **Docstrings**: Required for all public functions/classes
- **Comments**: Explain why, not what

Example:

```python
def resolve_repository(repo_input: Optional[str] = None) -> str:
    """
    Resolve repository alias or owner/repo format
    
    Args:
        repo_input: Repository alias or owner/repo format (optional)
        
    Returns:
        Repository in owner/repo format
        
    Raises:
        RepositoryError: If repository is invalid
    """
    # Implementation
```

## 🏗️ Project Structure

```
gitish/
├── gitish/              # Main package
│   ├── commands/        # CLI commands
│   ├── services/        # Business logic
│   └── utils/           # Utilities
├── tests/               # Test suite
└── .github/workflows/   # CI/CD
```

### Adding New Features

1. **Commands**: Add to `gitish/commands/`
2. **Services**: Add to `gitish/services/`
3. **Utilities**: Add to `gitish/utils/`
4. **Tests**: Add corresponding tests in `tests/`

## 🔄 Pull Request Process

### Before Submitting

- [ ] Tests pass: `make test`
- [ ] Code is formatted: `make format`
- [ ] Linters pass: `make lint`
- [ ] Documentation is updated
- [ ] CHANGELOG is updated (if applicable)

### PR Guidelines

- **Title**: Clear and descriptive
- **Description**: Explain what and why
- **Tests**: Include tests for new features
- **Documentation**: Update README if needed
- **Commits**: Clear, atomic commits

### Review Process

1. Automated CI checks must pass
2. At least one maintainer review required
3. Address review feedback
4. Squash commits if requested
5. Merge when approved

## 🐛 Bug Reports

### Before Reporting

- Check existing issues
- Try latest version
- Gather reproduction steps

### Report Template

```markdown
**Description**
Clear description of the bug

**To Reproduce**
Steps to reproduce:
1. Run command '...'
2. See error

**Expected Behavior**
What should happen

**Environment**
- OS: [e.g., Ubuntu 22.04]
- Python version: [e.g., 3.10]
- Gitish version: [e.g., 1.0.0]

**Additional Context**
Any other relevant information
```

## 💡 Feature Requests

### Before Requesting

- Check existing issues
- Consider if it fits project scope
- Think about implementation

### Request Template

```markdown
**Problem**
What problem does this solve?

**Proposed Solution**
How should it work?

**Alternatives**
Other solutions considered

**Additional Context**
Any other relevant information
```

## 📚 Documentation

### Types of Documentation

- **Code comments**: Explain complex logic
- **Docstrings**: Document all public APIs
- **README**: User-facing documentation
- **CONTRIBUTING**: This file

### Documentation Style

- Clear and concise
- Include examples
- Keep up to date
- Use proper formatting

## 🎯 Coding Standards

### Python Version

- Support Python 3.6+
- Use features compatible with 3.6
- Test on multiple versions (CI does this)

### Dependencies

- **Zero runtime dependencies** - This is a core principle
- Dev dependencies are fine
- Justify any new dependencies

### Error Handling

- Use custom exceptions
- Provide helpful error messages
- Handle edge cases

Example:

```python
class RepositoryError(Exception):
    """Raised when repository is invalid"""
    pass

def resolve_repository(repo_input):
    if not is_valid(repo_input):
        raise RepositoryError(
            f"Invalid repository: {repo_input}\n"
            f"Use format: owner/repo"
        )
```

## 🔐 Security

### Reporting Security Issues

**DO NOT** open public issues for security vulnerabilities.

Instead:
- Email: security@gitish.dev (if available)
- Or create a private security advisory on GitHub

### Security Best Practices

- Never commit secrets
- Validate all inputs
- Use HTTPS for API calls
- Follow principle of least privilege

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🙏 Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Credited in documentation

## ❓ Questions?

- Open a discussion on GitHub
- Check existing issues
- Read the documentation

## 🎉 Thank You!

Your contributions make Gitish better for everyone. We appreciate your time and effort!

---

**Happy Contributing!** 🚀
