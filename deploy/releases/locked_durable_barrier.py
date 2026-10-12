#!/usr/bin/env python3
"""Gate 4D.22B.4: lease-enforced inert barrier operations.

This is a laboratory-only facade. It does not execute Docker,
authorize production, settle an attempt or permit automatic retry.

Only this interface is eligible for subsequent laboratory integration.
The legacy unguarded store remains unsuitable for deployment execution.
"""

from pathlib import Path

from deployment_lock import DeploymentLease
from docker_execution_evidence import DockerExecutionEvidenceStore
from durable_barrier_controller import prepare_bound_barrier


class LockedEvidenceStore(DockerExecutionEvidenceStore):
    """Evidence store requiring an active matching deployment lease."""

    def __init__(self, root, lock_dir, lease):
        if not isinstance(lease, DeploymentLease):
            raise RuntimeError("DeploymentLease required")

        self.lock_dir = Path(lock_dir)
        self.lease = lease
        self.require_lease()

        super().__init__(root)

    def require_lease(self):
        self.lease.require(self.lock_dir)
        return True

    def prepare(self, attempt, command):
        self.require_lease()
        return super().prepare(attempt, command)

    def observe(self, release_id, identity):
        self.require_lease()
        return super().observe(release_id, identity)

    def record_exit(self, release_id, exit_code):
        self.require_lease()
        return super().record_exit(release_id, exit_code)


class LockedBoundBarrier:
    """Wrap an inert bound child with lease validation."""

    def __init__(self, binding, store):
        if not isinstance(store, LockedEvidenceStore):
            raise ValueError("LockedEvidenceStore required")

        store.require_lease()

        self.binding = binding
        self.store = store

    @property
    def child(self):
        return self.binding.child

    def verify(self):
        self.store.require_lease()
        return self.binding.verify()

    def release(self):
        """Fail closed if the lease is unavailable or invalid."""
        try:
            self.store.require_lease()
            self.binding.verify()
            self.store.require_lease()
            self.binding.release()
        except BaseException:
            self.binding.close_without_release()
            raise

    def close_without_release(self):
        self.binding.close_without_release()

    def wait(self, timeout=10):
        return self.binding.wait(timeout=timeout)


def prepare_locked_barrier(store, attempt, marker):
    """Create a blocked inert child under an active matching lease."""
    if not isinstance(store, LockedEvidenceStore):
        raise RuntimeError("LockedEvidenceStore required")

    store.require_lease()

    binding = prepare_bound_barrier(store, attempt, marker)

    try:
        store.require_lease()
        return LockedBoundBarrier(binding, store)
    except BaseException:
        binding.close_without_release()
        binding.wait(timeout=10)
        raise
