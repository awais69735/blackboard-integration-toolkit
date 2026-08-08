# Quick Start

## Prerequisites

* Python 3.10+
* A Blackboard Learn instance (or use the provided mock server)

## Installation

```bash
pip install blackboard-integration-toolkit
```

## Configuration

Set environment variables (or create a `.env` file):

```env
BB_BASE_URL=https://your-blackboard-instance.com
BB_CLIENT_ID=your_client_id
BB_CLIENT_SECRET=your_client_secret
BB_TOKEN_URL=https://your-blackboard-instance.com/learn/api/public/v1/oauth2/token
```

## Using the Mock Server (for development)

Start the mock server:

```bash
bb-toolkit mock-server --port 5001
```

Set environment variables to point to it:

```bash
export BB_BASE_URL=http://localhost:5001
export BB_TOKEN_URL=http://localhost:5001/learn/api/public/v1/oauth2/token
export BB_CLIENT_ID=dummy
export BB_CLIENT_SECRET=dummy
```

Validate the connection:

```bash
bb-toolkit config validate
```

## Synchronisation

Create a JSON file with your external data (e.g., `students.json`) and run:

```bash
bb-toolkit sync-students --file students.json
```

## Python API

```python
from blackboard import BlackboardClient

client = BlackboardClient.from_env()
student = client.get_student("s1")
```

See the [API Reference](api.md) for more.
