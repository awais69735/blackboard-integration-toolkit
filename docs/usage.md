# Usage Guide

This guide covers every feature of the Blackboard Integration Toolkit, from basic CRUD operations to advanced synchronisation.

## Prerequisites

* Python 3.10+
* Blackboard Learn instance (or mock server)
* Configured environment variables (see [Configuration](configuration.md))

---

## 1. Python API

The toolkit provides a clean Python interface via the `BlackboardClient` facade.

### Initialise the Client

```python
from blackboard import BlackboardClient

client = BlackboardClient.from_env()  # reads from .env
```

Or manually:

```python
from blackboard import BlackboardClient
from blackboard.interfaces.config.settings import Settings

settings = Settings.from_env()
client = BlackboardClient(settings)
```

---

### Students

#### Get a Student

```python
student = client.get_student("student_id")
if student:
    print(student.full_name)
```

#### List Students

```python
# All students (paginated internally)
for student in client.list_students(limit=50):
    print(student.username)

# With filters (e.g., active only)
active_students = client.list_students(active=True)
```

#### Create or Update a Student

```python
from blackboard.domain.entities import Student
from blackboard.domain.value_objects import StudentId

new_student = Student(
    id=StudentId("ext123"),
    username="jdoe",
    email="jdoe@example.com",
    first_name="John",
    last_name="Doe",
    active=True
)

created = client.save(new_student)  # Creates if not exists, updates otherwise
```

#### Delete a Student

```python
client.delete(StudentId("ext123"))
```

---

### Courses

#### Get a Course

```python
course = client.get_course("course_id")
```

#### List Courses

```python
courses = client.list_courses(limit=100)
```

#### Create or Update a Course

```python
from blackboard.domain.entities import Course
from blackboard.domain.value_objects import CourseId

new_course = Course(
    id=CourseId("ext_course_1"),
    name="Python Programming",
    code="PY101",
    description="Intro to Python",
    active=True
)

created = client.save(new_course)
```

#### Delete a Course

```python
client.delete(CourseId("ext_course_1"))
```

---

### Enrollments

#### Get Enrollments by Course

```python
enrollments = client.list_enrollments(course_id, active_only=True)
```

#### Get Enrollments by Student

```python
enrollments = client.enrollments.list_by_student(student_id)
```

#### Create an Enrollment

```python
from blackboard.domain.entities import Enrollment
from blackboard.domain.value_objects import EnrollmentId, StudentId, CourseId

enrollment = Enrollment(
    id=EnrollmentId("s1_c1"),
    student_id=StudentId("s1"),
    course_id=CourseId("c1"),
    role="student",
    active=True
)

created = client.save(enrollment)
```

#### Delete an Enrollment

```python
client.delete(EnrollmentId("s1_c1"))
```

---

### Assignments

#### List Assignments in a Course

```python
assignments = client.list_assignments(course_id)
```

#### Create an Assignment

```python
from blackboard.domain.entities import Assignment
from blackboard.domain.value_objects import AssignmentId, CourseId

assignment = Assignment(
    id=None,  # None will trigger a POST (create)
    course_id=CourseId("c1"),
    name="Homework 1",
    points_possible=100,
    description="Solve problems 1-5"
)

created = client.save(assignment)
```

#### Update an Assignment

```python
# Get existing, modify, save
assignment = client.get_assignment("a1")  # if you have a get method
assignment.name = "Updated Homework 1"
updated = client.save(assignment)
```

---

## 2. Synchronisation Engines

Sync engines compare external data (from SIS, ERP, etc.) with Blackboard and perform create/update/delete operations in bulk.

### Sync Students

```python
from blackboard.application.services.sync_service import SyncService
from blackboard.application.dto import SyncOptions

service = SyncService(client.provider)

external_students = [
    {"id": "ext1", "username": "john", "email": "john@example.com", ...}
]

result = service.sync_students(
    external_students,
    SyncOptions(dry_run=False)
)

print(f"Created: {result.created}, Updated: {result.updated}")
```

### Sync Courses

```python
external_courses = [
    {"id": "ext_c1", "name": "Math 101", "code": "MATH101", ...}
]

result = service.sync_courses(
    external_courses,
    SyncOptions(dry_run=True)
)
```

### Sync Enrollments

```python
external_enrollments = [
    {
        "student_id": "ext_s1",
        "course_id": "ext_c1",
        "role": "student",
        "active": True
    }
]

result = service.sync_enrollments(external_enrollments)
```

### Sync Grades (stub – extend as needed)

```python
external_grades = [
    {
        "student_id": "ext_s1",
        "assignment_id": "ext_a1",
        "score": 85.0
    }
]

result = service.sync_grades(
    external_grades,
    assignment_id="ext_a1"
)
```

---

## 3. CLI Commands

All operations are also available via the command line.

### Show Configuration

```bash
bb-toolkit config show
```

### Validate Connection

```bash
bb-toolkit config validate
```

### Sync Students

```bash
bb-toolkit sync-students --file students.json
```

With dry-run:

```bash
bb-toolkit sync-students --file students.json --dry-run
```

### Sync Courses

```bash
bb-toolkit sync-courses --file courses.json
```

### Sync Enrollments

```bash
bb-toolkit sync-enrollments --file enrollments.json
```

### Start Mock Server

```bash
bb-toolkit mock-server --port 5001
```

---

## 4. Mock Server

For development without a real Blackboard instance, use the mock server. It fully supports all endpoints and OAuth2.

```bash
bb-toolkit mock-server --port 5001
```

Then set environment variables to point to `http://localhost:5001` and run any command.

---

## 5. Error Handling

All methods raise custom exceptions:

* `AuthenticationError` – invalid credentials or token expired.
* `ResourceNotFoundError` – requested resource does not exist.
* `RateLimitExceededError` – too many requests.
* `ValidationError` – invalid input data.
* `BlackboardError` – generic error.

Example:

```python
from blackboard.exceptions import ResourceNotFoundError

try:
    student = client.get_student("non_existent")
except ResourceNotFoundError:
    print("Student not found")
```

---

## 6. Advanced: Direct Repository Access

If you need more low-level control, you can access repositories directly via `client.provider`:

```python
# List all students using the repository
students = list(client.provider.students.list_all())

# Get a specific student
student = client.provider.students.get(StudentId("s1"))
```

---

## 7. Extending with Events

The toolkit includes an event bus for custom hooks.

```python
from blackboard.events.event_bus import EventBus, Event

def on_sync_completed(event):
    print(f"Sync finished: {event.payload.status}")

EventBus.register("sync.students.completed", on_sync_completed)
```

Now your handler will be called after every student sync.

---

## Summary

| Feature                  | Python API                           | CLI                           |
| ------------------------ | ------------------------------------ | ----------------------------- |
| Get student              | `client.get_student(id)`             | –                             |
| List students            | `client.list_students()`             | –                             |
| Create/update student    | `client.save(Student)`               | `bb-toolkit sync-students`    |
| Delete student           | `client.delete(StudentId)`           | –                             |
| Get course               | `client.get_course(id)`              | –                             |
| List courses             | `client.list_courses()`              | –                             |
| Create/update course     | `client.save(Course)`                | `bb-toolkit sync-courses`     |
| Delete course            | `client.delete(CourseId)`            | –                             |
| List enrollments         | `client.list_enrollments(course_id)` | –                             |
| Create/update enrollment | `client.save(Enrollment)`            | `bb-toolkit sync-enrollments` |
| Delete enrollment        | `client.delete(EnrollmentId)`        | –                             |
| List assignments         | `client.list_assignments(course_id)` | –                             |
| Create/update assignment | `client.save(Assignment)`            | –                             |
| Sync students            | `service.sync_students()`            | `bb-toolkit sync-students`    |
| Sync courses             | `service.sync_courses()`             | `bb-toolkit sync-courses`     |
| Sync enrollments         | `service.sync_enrollments()`         | `bb-toolkit sync-enrollments` |
| Validate config          | –                                    | `bb-toolkit config validate`  |
| Start mock server        | –                                    | `bb-toolkit mock-server`      |

---

Now you have everything you need to fully integrate Blackboard with your systems!
