# CLI Reference

The toolkit provides a command-line interface via the `bb-toolkit` command.

## Global Options

* `--log-level` – set the log level (DEBUG, INFO, WARNING, ERROR).

## Commands

### `config`

Manage configuration.

* `config show` – display current configuration.
* `config validate` – test connection to Blackboard.

### `mock-server`

Start the mock Blackboard server.

```bash
bb-toolkit mock-server --port 5001
```

### `sync-students`

Sync students from a JSON file.

```bash
bb-toolkit sync-students --file students.json [--dry-run]
```

### `sync-courses`

Sync courses from a JSON file.

```bash
bb-toolkit sync-courses --file courses.json [--dry-run]
```

### `sync-enrollments`

Sync enrollments from a JSON file.

```bash
bb-toolkit sync-enrollments --file enrollments.json [--dry-run]
```

## Example JSON File Format

### Students

```json
[
  {
    "id": "ext1",
    "username": "john",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "active": true
  }
]
```

### Courses

```json
[
  {
    "id": "ext1",
    "name": "Math 101",
    "code": "MATH101",
    "active": true
  }
]
```

### Enrollments

```json
[
  {
    "student_id": "ext1",
    "course_id": "ext_course1",
    "role": "student",
    "active": true
  }
]
```

The `id` fields refer to your external identifiers; the toolkit uses them to match records.
