# Development Tools

Welcome! This document describes how to run tests, measure coverage, and enforce code quality with pre-commit.

## 🧪 Running Tests & Coverage

### Pytest Configuration

Add this to `pytest.ini` in the project root:

```ini
[pytest]
DJANGO_SETTINGS_MODULE = pristine.settings
python_files = tests.py test_*.py *_tests.py

```

### Common Pytest Commands

- **Install pytest-cov**  
  ```bash
  poetry add --dev pytest-cov
  ```
- **Run all tests**  
  ```bash
  poetry run pytest
  ```
- **Show coverage report**  
  ```bash
  poetry run pytest --cov=hr --cov-report=term-missing --cov-fail-under=95
  ```
- **Generate HTML coverage report**  
  ```bash
  poetry run pytest --cov=hr --cov-report=html
  open htmlcov/index.html
  ```
- **List all collected tests**  
  ```bash
  poetry run pytest --collect-only
  ```

## 🔧 Pre-commit Setup & Usage

### Installing pre-commit

```bash
poetry add --dev pre-commit
poetry run pre-commit install
```

Once you’ve installed pre-commit and created .pre-commit-config.yaml, you can verify everything locally before you commit:

### Running Pre-commit Hooks

- **Run all hooks against all files**  
  ```bash
  poetry run pre-commit run --all-files
  ```
- **Run a single hook**  
  ```bash
  poetry run pre-commit run black
  poetry run pre-commit run flake8
  ```
- **Skip hooks on a commit**  
  ```bash
  git commit --no-verify
  ```
- **Dry-run a commit** (simulate what would happen on `git commit`)
  ```bash
  poetry run pre-commit run --hook-stage commit
  ```
- **Fix any issues** the hooks report, then recommit. Once everything passes, `git commit` will succeed.

On each commit, pre-commit will run pytest and enforce 95% coverage threshold.
---
