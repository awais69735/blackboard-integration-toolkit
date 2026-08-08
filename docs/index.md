# Blackboard Integration Toolkit

Enterprise-grade Python library for integrating Blackboard Learn with external systems.

## Features

* **Blackboard REST API** – full coverage of Users, Courses, Enrollments, Assignments, and more.
* **Provider-agnostic** – designed to support other LMS later.
* **Automatic retries, pagination, rate limiting, token refresh** – built-in.
* **Synchronisation engines** – for students, courses, enrollments, and grades.
* **CLI tool** – for configuration, validation, and sync operations.
* **Mock server** – for offline development and testing.
* **Fully tested** – with a mock Blackboard server and comprehensive unit/integration tests.

## Installation

```bash
pip install blackboard-integration-toolkit
```

## Quick Example

```python
from blackboard import BlackboardClient

client = BlackboardClient.from_env()
student = client.get_student("some_id")
print(student.full_name)
```

## Documentation

* [Quick Start](quickstart.md)
* [Configuration](configuration.md)
* [CLI Reference](cli.md)
* [Architecture](architecture.md)
* [Contributing](contributing.md)

## License

MIT
