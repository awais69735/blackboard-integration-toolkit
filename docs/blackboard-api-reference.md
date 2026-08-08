# Blackboard API Reference

This page documents the Blackboard REST API endpoints that the toolkit uses, including version information, required parameters, and response structures.

---

## Authentication

### OAuth2 Token

| Method | Endpoint                            | Description                                     |
| ------ | ----------------------------------- | ----------------------------------------------- |
| `POST` | `/learn/api/public/v1/oauth2/token` | Obtain an access token using client credentials |

#### Request Body

```text
grant_type=client_credentials
client_id={client_id}
client_secret={client_secret}
```

#### Response

```json
{
  "access_token": "string",
  "token_type": "Bearer",
  "expires_in": 3600
}
```

---

## Users (v1)

### List Users

| Method | Endpoint                     | Description                   |
| ------ | ---------------------------- | ----------------------------- |
| `GET`  | `/learn/api/public/v1/users` | Get a paginated list of users |

#### Query Parameters

| Parameter  | Type    | Description                                          |
| ---------- | ------- | ---------------------------------------------------- |
| `limit`    | integer | Number of results per page (default: 100, max: 1000) |
| `offset`   | integer | Pagination offset                                    |
| `userName` | string  | Filter by username (exact match)                     |
| `active`   | boolean | Filter by active status                              |

#### Response

```json
{
  "results": [
    {
      "id": "string",
      "userName": "string",
      "email": "string",
      "firstName": "string",
      "lastName": "string",
      "active": true,
      "created": "2023-01-01T00:00:00Z",
      "modified": "2023-01-01T00:00:00Z"
    }
  ],
  "totalCount": 100
}
```

### Get User

| Method | Endpoint                              | Description               |
| ------ | ------------------------------------- | ------------------------- |
| `GET`  | `/learn/api/public/v1/users/{userId}` | Get a specific user by ID |

### Update User

| Method  | Endpoint                              | Description        |
| ------- | ------------------------------------- | ------------------ |
| `PATCH` | `/learn/api/public/v1/users/{userId}` | Update user fields |

#### Request Body

```json
{
  "userName": "string",
  "email": "string",
  "firstName": "string",
  "lastName": "string",
  "active": true
}
```

### Create User

| Method | Endpoint                     | Description       |
| ------ | ---------------------------- | ----------------- |
| `POST` | `/learn/api/public/v1/users` | Create a new user |

#### Request Body

```json
{
  "userName": "string",
  "email": "string",
  "firstName": "string",
  "lastName": "string",
  "active": true
}
```

### Delete User

| Method   | Endpoint                              | Description   |
| -------- | ------------------------------------- | ------------- |
| `DELETE` | `/learn/api/public/v1/users/{userId}` | Delete a user |

---

## Courses (v3)

**Important:** The toolkit uses **v3** of the Courses API for the latest features.

### List Courses

| Method | Endpoint                       | Description                     |
| ------ | ------------------------------ | ------------------------------- |
| `GET`  | `/learn/api/public/v3/courses` | Get a paginated list of courses |

#### Query Parameters

| Parameter  | Type    | Description                                          |
| ---------- | ------- | ---------------------------------------------------- |
| `limit`    | integer | Number of results per page (default: 100, max: 1000) |
| `offset`   | integer | Pagination offset                                    |
| `courseId` | string  | Filter by course ID (exact match)                    |
| `userId`   | string  | Filter courses a user is enrolled in                 |

#### Response

```json
{
  "results": [
    {
      "id": "string",
      "name": "string",
      "courseId": "string",
      "description": "string",
      "available": true,
      "startDate": "2023-09-01T00:00:00Z",
      "endDate": "2023-12-15T00:00:00Z",
      "term": {
        "name": "string"
      },
      "created": "2023-08-01T00:00:00Z",
      "modified": "2023-08-15T00:00:00Z"
    }
  ],
  "totalCount": 100
}
```

### Get Course

| Method | Endpoint                                  | Description                 |
| ------ | ----------------------------------------- | --------------------------- |
| `GET`  | `/learn/api/public/v3/courses/{courseId}` | Get a specific course by ID |

### Update Course

| Method  | Endpoint                                  | Description          |
| ------- | ----------------------------------------- | -------------------- |
| `PATCH` | `/learn/api/public/v3/courses/{courseId}` | Update course fields |

#### Request Body

```json
{
  "name": "string",
  "courseId": "string",
  "description": "string",
  "available": true
}
```

### Create Course

| Method | Endpoint                       | Description         |
| ------ | ------------------------------ | ------------------- |
| `POST` | `/learn/api/public/v3/courses` | Create a new course |

#### Request Body

```json
{
  "name": "string",
  "courseId": "string",
  "description": "string",
  "available": true
}
```

### Delete Course

| Method   | Endpoint                                  | Description     |
| -------- | ----------------------------------------- | --------------- |
| `DELETE` | `/learn/api/public/v3/courses/{courseId}` | Delete a course |

---

## Enrollments (v1)

### List Enrollments by Course

| Method | Endpoint                                              | Description                      |
| ------ | ----------------------------------------------------- | -------------------------------- |
| `GET`  | `/learn/api/public/v1/courses/{courseId}/enrollments` | Get all enrollments for a course |

#### Query Parameters

| Parameter | Type    | Description                |
| --------- | ------- | -------------------------- |
| `limit`   | integer | Number of results per page |
| `offset`  | integer | Pagination offset          |
| `active`  | boolean | Filter by active status    |

#### Response

```json
{
  "results": [
    {
      "userId": "string",
      "role": "student|instructor|ta|auditor",
      "active": true,
      "created": "2023-01-01T00:00:00Z"
    }
  ],
  "totalCount": 100
}
```

### Create Enrollment

| Method | Endpoint                                              | Description               |
| ------ | ----------------------------------------------------- | ------------------------- |
| `POST` | `/learn/api/public/v1/courses/{courseId}/enrollments` | Enroll a user in a course |

#### Request Body

```json
{
  "userId": "string",
  "role": "student"
}
```

### Delete Enrollment

| Method   | Endpoint                                                       | Description                 |
| -------- | -------------------------------------------------------------- | --------------------------- |
| `DELETE` | `/learn/api/public/v1/courses/{courseId}/enrollments/{userId}` | Remove a user from a course |

---

## Assignments (v1)

**Note:** Assignment creation uses a different endpoint in newer Blackboard versions (3900.98+).

### List Assignments

| Method | Endpoint                                              | Description                      |
| ------ | ----------------------------------------------------- | -------------------------------- |
| `GET`  | `/learn/api/public/v1/courses/{courseId}/assignments` | Get all assignments for a course |

#### Response

```json
{
  "results": [
    {
      "id": "string",
      "name": "string",
      "description": "string",
      "dueDate": "2023-09-15T23:59:59Z",
      "points": {
        "possible": 100
      },
      "created": "2023-09-01T00:00:00Z",
      "modified": "2023-09-01T00:00:00Z"
    }
  ],
  "totalCount": 100
}
```

### Create Assignment (Modern)

| Method | Endpoint                                                            | Description                             |
| ------ | ------------------------------------------------------------------- | --------------------------------------- |
| `POST` | `/learn/api/public/v1/courses/{courseId}/contents/createAssignment` | Create a new assignment via content API |

#### Request Body

```json
{
  "name": "string",
  "description": "string",
  "dueDate": "2023-09-15T23:59:59Z",
  "points": {
    "possible": 100
  }
}
```

### Update Assignment

| Method  | Endpoint                                                             | Description              |
| ------- | -------------------------------------------------------------------- | ------------------------ |
| `PATCH` | `/learn/api/public/v1/courses/{courseId}/assignments/{assignmentId}` | Update assignment fields |

#### Request Body

```json
{
  "name": "string",
  "description": "string",
  "dueDate": "2023-09-15T23:59:59Z",
  "points": {
    "possible": 100
  }
}
```

---

## Gradebook (v2)

### Get Gradebook Columns

| Method | Endpoint                                                    | Description                        |
| ------ | ----------------------------------------------------------- | ---------------------------------- |
| `GET`  | `/learn/api/public/v2/courses/{courseId}/gradebook/columns` | Get all grade columns for a course |

**Note:** This endpoint is currently a stub in the toolkit. Full gradebook support will be added in a future release.

---

## API Version Summary

| Resource             | API Version | Endpoint Base                                                 |
| -------------------- | ----------- | ------------------------------------------------------------- |
| Users                | v1          | `/learn/api/public/v1/users`                                  |
| Courses              | v3          | `/learn/api/public/v3/courses`                                |
| Enrollments          | v1          | `/learn/api/public/v1/courses/{id}/enrollments`               |
| Assignments (List)   | v1          | `/learn/api/public/v1/courses/{id}/assignments`               |
| Assignments (Create) | v1          | `/learn/api/public/v1/courses/{id}/contents/createAssignment` |
| Gradebook            | v2          | `/learn/api/public/v2/courses/{id}/gradebook/columns`         |
| Token                | v1          | `/learn/api/public/v1/oauth2/token`                           |

---

## Toolkit Methods vs API Endpoints

| Toolkit Method                        | Blackboard API Endpoint                      | Method |
| ------------------------------------- | -------------------------------------------- | ------ |
| `client.students.get()`               | `/users/{id}`                                | GET    |
| `client.students.list()`              | `/users`                                     | GET    |
| `client.students.save()` (create)     | `/users`                                     | POST   |
| `client.students.save()` (update)     | `/users/{id}`                                | PATCH  |
| `client.students.delete()`            | `/users/{id}`                                | DELETE |
| `client.courses.get()`                | `/v3/courses/{id}`                           | GET    |
| `client.courses.list()`               | `/v3/courses`                                | GET    |
| `client.courses.save()` (create)      | `/v3/courses`                                | POST   |
| `client.courses.save()` (update)      | `/v3/courses/{id}`                           | PATCH  |
| `client.courses.delete()`             | `/v3/courses/{id}`                           | DELETE |
| `client.enrollments.list_by_course()` | `/v1/courses/{id}/enrollments`               | GET    |
| `client.enrollments.save()`           | `/v1/courses/{id}/enrollments`               | POST   |
| `client.enrollments.delete()`         | `/v1/courses/{id}/enrollments/{userId}`      | DELETE |
| `client.assignments.list_by_course()` | `/v1/courses/{id}/assignments`               | GET    |
| `client.assignments.save()` (create)  | `/v1/courses/{id}/contents/createAssignment` | POST   |
| `client.assignments.save()` (update)  | `/v1/courses/{id}/assignments/{id}`          | PATCH  |

---

This reference is generated from the latest Blackboard API documentation (version 4001.1.0) and the toolkit's implementation.
