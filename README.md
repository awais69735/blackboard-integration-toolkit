# Blackboard Integration Toolkit

Enterprise-grade Python library for integrating Blackboard Learn with external systems (SIS, ERP, HRMS, etc.).

## Features

* Full coverage of Users, Courses, Enrollments, Assignments, and more.
* Automatic retries, pagination, rate limiting, and token refresh.
* Synchronisation engines for students, courses, enrollments, and grades.
* CLI tool and mock server for offline development.
* Clean, testable architecture.

## Quick Start

```bash
pip install blackboard-integration-toolkit
```

```python
from blackboard import BlackboardClient

client = BlackboardClient.from_env()
student = client.get_student("some_id")
```

## Documentation

Full documentation: https://awais69735.github.io/blackboard-integration-toolkit/

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT
