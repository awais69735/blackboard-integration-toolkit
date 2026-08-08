# Mock Server

The mock server simulates Blackboard's REST API and OAuth2 token endpoint, allowing you to develop and test without a real Blackboard instance.

## Starting the Server

```bash
bb-toolkit mock-server --port 5001
```

## Configuration

Set environment variables to point to the mock server:

```bash
export BB_BASE_URL=http://localhost:5001
export BB_TOKEN_URL=http://localhost:5001/learn/api/public/v1/oauth2/token
export BB_CLIENT_ID=dummy
export BB_CLIENT_SECRET=dummy
```

## Fixtures

The server loads fixture data from `src/blackboard/testing/fixtures/`. You can edit these JSON files to customize the mock data.

## Endpoints Supported

* `POST /learn/api/public/v1/oauth2/token`
* `GET /learn/api/public/v1/users`
* `GET /learn/api/public/v1/users/{id}`, `PATCH`, `DELETE`, `POST`
* `GET /learn/api/public/v3/courses`, `GET /v3/courses/{id}`, `PATCH`, `DELETE`, `POST`
* `GET /learn/api/public/v1/courses/{id}/enrollments`, `POST`, `DELETE`
* `GET /learn/api/public/v1/courses/{id}/assignments`
* `POST /learn/api/public/v1/courses/{id}/contents/createAssignment`
* `PATCH /learn/api/public/v1/courses/{id}/assignments/{id}`
* `GET /learn/api/public/v2/courses/{id}/gradebook/columns` (stub)

## Limitations

* No authentication validation (any credentials accepted).
* Data is reset on each server restart.
* Some advanced Blackboard features are not implemented.
