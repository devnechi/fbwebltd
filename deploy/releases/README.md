# Future Basics Immutable Release Contract

A production release consists of two container images built from the
same approved Git commit:

1. Laravel PHP-FPM application image.
2. Caddy web image containing the matching public assets.

Each release manifest must record:

- release_id
- repository
- commit_sha
- application_image (immutable registry digest)
- web_image (immutable registry digest)
- approval reference
- creation timestamp

Security rules:

- A manifest is descriptive metadata, not deployment authorization.
- The production controller must independently verify approval.
- Images must be referenced by immutable digests, not mutable tags.
- The deployment account must not control Docker or trusted configuration.
- Existing database, storage and TLS volumes must be preserved.
- Database migrations require separate approval.
- Previous approved image digests must be retained for rollback.
- Health checks must pass before a release is accepted.
- Production secrets must never enter image layers or Git commits.
- Automated production deployment remains disabled until all gates pass.

Rollback must restore the previously approved application/web image pair.
It must not delete or recreate persistent production volumes.
