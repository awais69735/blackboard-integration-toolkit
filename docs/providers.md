# Provider Guide

The toolkit currently supports **Blackboard Learn** as the primary provider.

## Supported Providers

| Provider | Status | API Version |
|----------|--------|-------------|
| Blackboard Learn | ✅ Supported | v1 (users, enrollments), v3 (courses) |

## Adding a New Provider

To add support for another LMS (e.g., Moodle, Canvas), implement the `LMSProvider` interface defined in `domain/interfaces.py`.

1. Create a new package under `infrastructure/providers/`.
2. Implement all abstract methods.
3. Register the provider in the `ProviderFactory` (or use dependency injection).
4. Add tests and documentation.

## Blackboard‑Specific Notes

- Uses OAuth2 client credentials flow.
- Pagination uses offset/limit.
- Assignment creation uses the `/contents/createAssignment` endpoint (v3900.98+).

For more details, see the architecture overview and source code.