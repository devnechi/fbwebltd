#!/usr/bin/env python3
"""Lease-enforced inert barrier facade for the laboratory.

Base evidence mutations are now protected directly by
DockerExecutionEvidenceStore. This facade also protects release.
No Docker execution or production authorization.
"""

from deployment_lock import DeploymentLease
from docker_execution_evidence import DockerExecutionEvidenceStore
from durable_barrier_controller import prepare_bound_barrier


class LockedEvidenceStore(DockerExecutionEvidenceStore):
    """Compatibility interface backed by the secured base store."""

    def __init__(self, root, lock_dir, lease):
        if not isinstance(lease, DeploymentLease):
            raise RuntimeError("DeploymentLease required")

        super().__init__(
            root,
            lock_dir=lock_dir,
            lease=lease,
        )


class LockedBoundBarrier:
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
