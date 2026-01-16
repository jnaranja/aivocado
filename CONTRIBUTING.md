# Contributing to AIVOCADO

Thank you for your interest in contributing to AIVOCADO! This document provides guidelines and instructions for contributing.

## Getting Started

### Prerequisites

- Python 3.9 or higher
- Git

### Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/jnaranja/aivocado.git
   cd aivocado
   ```

2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

4. Set up pre-commit hooks (optional but recommended):
   ```bash
   pre-commit install
   ```

## Development Workflow

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_sensors.py

# Run tests matching a pattern
pytest -k "test_mock"
```

### Code Formatting

We use `black` for code formatting and `ruff` for linting:

```bash
# Format code
black .

# Check formatting
black --check .

# Lint code
ruff check .

# Auto-fix lint issues
ruff check --fix .
```

### Type Checking

```bash
mypy . --ignore-missing-imports
```

## Making Changes

### Branch Naming

Use descriptive branch names:
- `feature/add-temperature-alerts`
- `fix/sensor-reading-timeout`
- `docs/update-hardware-guide`

### Commit Messages

Write clear, concise commit messages:
- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters
- Reference issues when applicable

Examples:
```
feat: add temperature alert notifications
fix: handle sensor timeout gracefully
docs: update installation instructions
test: add tests for API client
```

### Pull Request Process

1. Create a new branch from `main`
2. Make your changes
3. Ensure all tests pass
4. Update documentation if needed
5. Submit a pull request

### Pull Request Checklist

- [ ] Tests pass locally (`pytest`)
- [ ] Code is formatted (`black --check .`)
- [ ] Linting passes (`ruff check .`)
- [ ] Type checking passes (`mypy .`)
- [ ] Documentation updated (if applicable)
- [ ] Commit messages are clear and descriptive

## Project Structure

```
aivocado/
├── main.py           # Entry point and main loop
├── sensors.py        # Sensor interfaces (mock and real)
├── display.py        # Terminal UI dashboard
├── ai_advisor.py     # Claude AI integration
├── api_client.py     # External API client
├── tests/            # Test suite
│   ├── conftest.py   # Shared fixtures
│   ├── test_*.py     # Test modules
├── .github/
│   └── workflows/    # CI/CD configuration
└── docs/             # Documentation
```

## Code Style Guidelines

- Follow PEP 8 style guidelines
- Use type hints for function parameters and return values
- Write docstrings for public functions and classes
- Keep functions focused and small
- Use meaningful variable names

## Testing Guidelines

- Write tests for all new functionality
- Maintain or improve code coverage
- Use fixtures for common test data
- Mock external dependencies (APIs, hardware)
- Test edge cases and error conditions

## Reporting Issues

When reporting issues, please include:
- A clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Python version and OS
- Relevant log output or error messages

## Questions?

Feel free to open an issue for questions or discussions about the project.
