# Future Basics — Isolated Rollback Test Plan

## Scope

Test Laravel and Caddy image switching in an isolated Docker
environment. Do not connect to production containers, networks,
volumes, secrets or domain ports.

## Preconditions

- Use a unique Docker Compose project name.
- Use disposable, project-specific volumes.
- Use test credentials only.
- Bind HTTP to the local loopback interface.
- Do not use production environment files.
- Do not run database migrations.
- Verify baseline Laravel and Caddy images.

## Test sequence

1. Start temporary MySQL, Laravel and Caddy containers.
2. Verify Laravel readiness and HTTP 200 responses.
3. Record both baseline image IDs.
4. Replace the application image with an intentionally unhealthy image.
5. Confirm that deployment health verification rejects the candidate.
6. Restore the previous Laravel image.
7. Restore the previous Caddy image if it was changed.
8. Confirm application health and HTTP 200 responses.
9. Confirm test data survives the image switch.
10. Remove only the explicitly named test resources.

## Acceptance criteria

- A failed image is never marked as a successful release.
- Both application and web image versions can be restored.
- Temporary database data remains intact during rollback.
- No production containers or persistent volumes are modified.
- Rollback failure is reported rather than concealed.

## Production safeguards

A future production controller must:

- Independently verify release approval.
- Validate both immutable image digests.
- Reject mutable image tags.
- Deploy only the application and web services.
- Preserve existing database, storage and certificate volumes.
- Save the previous approved release metadata.
- Verify readiness after activation.
- Provide an auditable rollback operation.
- Never grant Docker privileges to the fbdeploy account.
