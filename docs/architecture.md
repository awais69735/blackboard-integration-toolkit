# Architecture Overview

The toolkit follows Clean Architecture / Hexagonal architecture, ensuring separation of concerns and maintainability.

## Layers

1. **Domain** – Business entities (Student, Course, etc.) and repository interfaces.
2. **Application** – Use cases (sync engines) and DTOs.
3. **Infrastructure** – Concrete implementations: HTTP client, OAuth2, providers (Blackboard), repositories, logging.
4. **Interfaces** – CLI and configuration.

All dependencies point inward: Infrastructure depends on Domain/Application, never the reverse.

## Provider Adapter

The `BlackboardProvider` implements all repository interfaces and abstracts the Blackboard REST API. Future providers (Moodle, Canvas) can be added by implementing the same interfaces.

## Synchronisation Engines

Each entity type has a sync engine that compares external data with Blackboard data and calculates differences (create/update/delete). The engines support dry‑run mode and batch processing.

## Testing

The toolkit includes a complete mock Blackboard server (with OAuth2) for offline development, plus unit and integration tests.

For more details, see the source code and API reference.