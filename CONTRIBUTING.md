# Contributing to Blackboard Integration Toolkit

We love your input! We want to make contributing to this project as easy and transparent as possible.

## How to Contribute

1. Fork the repo and create your branch from `main`.
2. If you've added code, add tests.
3. Ensure the test suite passes.
4. Make sure your code lints.
5. Issue that pull request.

## Any Contributions You Make Will Be Under the MIT Software License

In short, when you submit code changes, your submissions are understood to be under the same [MIT License](LICENSE) that covers the project.

## Report Bugs Using GitHub Issues

We use GitHub issues to track public bugs. Report a bug by opening a new issue.

## Write Bug Reports With Detail, Background, and Sample Code

**Great Bug Reports** tend to have:

* A quick summary and/or background
* Steps to reproduce
* What you expected would happen
* What actually happens
* Notes (possibly including why you think this might be happening, or stuff you tried that didn't work)

## Development Setup

```bash
git clone https://github.com/awais69735/blackboard-integration-toolkit.git
cd blackboard-integration-toolkit
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -e ".[dev]"
pre-commit install
```

## Testing

```bash
pytest
```

## Style Guide

We use Ruff for linting and formatting. Run:

```bash
ruff check .
ruff format .
```

## Code of Conduct

This project adheres to the Contributor Covenant code of conduct. By participating, you are expected to uphold this code.
