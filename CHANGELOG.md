# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial release with Blackboard REST API support (Users, Courses, Enrollments, Assignments).
- Synchronisation engines for students, courses, enrollments, and grades.
- CLI with config, sync, and mock-server commands.
- Mock Blackboard server for offline development.
- Comprehensive test suite with 90%+ coverage.
- Clean architecture following SOLID principles.
- OAuth2 authentication with automatic token refresh.
- Rate limiting, retries, and pagination.
- Structured logging with structlog.
- Full MkDocs documentation.