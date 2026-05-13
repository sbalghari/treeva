# Contributing to Treeva

Thank you for your interest in contributing to Treeva! This document provides guidelines and instructions for contributing to the project.


## Getting Started

### Fork and Clone
1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/your-username/treeva.git
   cd treeva
   ```

### Set Up Development Environment
```bash
# Install dependencies with uv
uv sync

# Verify installation
uv run treeva --version
```

## Making Changes

### Create a Feature Branch
```bash
git checkout -b feature/your-feature-name
```

### Code Style Guidelines

- Follow PEP 8 conventions
- Use type hints throughout
- Keep line length to 79 characters (enforced by ruff)
- Use meaningful variable and function names

### Running Tests and Checks

Before submitting a PR, ensure all checks pass:

```bash
# Run linting and formatting checks
uv run ruff check src/
uv run ruff format src/

# Run type checking
uv run mypy src/
```

## Submitting Changes

### Commit Messages

Write clear, concise commit messages.

### Push and Create a Pull Request

1. Push your branch:
   ```bash
   git push origin feature/your-feature-name
   ```

2. Create a Pull Request on GitHub with:
   - Clear title describing the change
   - Description of what changed and why
   - Reference to any related issues (#issue-number)
   - Any breaking changes or migration notes
