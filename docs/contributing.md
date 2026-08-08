# Contributing

We welcome contributions! Please follow these guidelines.

## Development Setup

1. Fork the repository and clone it.

2. Create a virtual environment: `python -m venv venv`

3. Activate it and install the package in editable mode with development extras:

   ```bash
   pip install -e ".[dev]"
   ```

4. Install pre-commit hooks: `pre-commit install`

## Coding Standards

* Python 3.10+
* Type hints everywhere.
* Ruff for linting and formatting (`ruff check . && ruff format .`).
* `mypy` for static type checking.
* 90%+ test coverage.

## Testing

```bash
pytest
```

## Pull Request Process

1. Create a feature branch.
2. Write tests for your changes.
3. Ensure all tests pass and coverage does not decrease.
4. Open a pull request against `main`.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
