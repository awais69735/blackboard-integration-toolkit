# Configuration

The toolkit reads configuration from environment variables or a `.env` file.

## Required Variables

| Variable           | Description                                                                   |
| ------------------ | ----------------------------------------------------------------------------- |
| `BB_BASE_URL`      | Blackboard instance base URL                                                  |
| `BB_CLIENT_ID`     | OAuth2 client ID                                                              |
| `BB_CLIENT_SECRET` | OAuth2 client secret                                                          |
| `BB_TOKEN_URL`     | OAuth2 token endpoint (usually `{BASE_URL}/learn/api/public/v1/oauth2/token`) |

## Optional Variables

| Variable                         | Default | Description                                    |
| -------------------------------- | ------- | ---------------------------------------------- |
| `BB_TIMEOUT`                     | `60`    | HTTP request timeout (seconds)                 |
| `BB_MAX_RETRIES`                 | `3`     | Number of retries for failed requests          |
| `BB_RATE_LIMIT_ENABLED`          | `true`  | Whether to apply rate limiting                 |
| `BB_RATE_LIMIT_CALLS_PER_SECOND` | `5.0`   | Maximum calls per second                       |
| `BB_RATE_LIMIT_BURST`            | `10`    | Burst capacity                                 |
| `BB_LOG_LEVEL`                   | `INFO`  | Log level (DEBUG, INFO, WARNING, ERROR)        |
| `BB_LOG_JSON`                    | `false` | Output logs as JSON (otherwise human-readable) |

## .env File

Create a `.env` file in the project root to automatically load variables.

Example:

```env
BB_BASE_URL=https://your-blackboard-instance.com
BB_CLIENT_ID=your_client_id
BB_CLIENT_SECRET=your_client_secret
BB_TOKEN_URL=https://your-blackboard-instance.com/learn/api/public/v1/oauth2/token
```

## Using the Mock Server

For development, see the [Mock Server](mock-server.md) guide.
