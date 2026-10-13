#!/usr/bin/env python3
"""Gate 4D.22B.3: durable binding for an inert child-start barrier.

Laboratory-only coordination. Never runs Docker or authorizes deployment.

The caller must hold the existing deployment lease across the entire
prepare, spawn, observe and release sequence. This module does not
acquire or substitute for that lock.
"""

from dataclasses import dataclass
from pathlib import Path

from docker_execution_evidence import (
    DockerExecutionEvidenceStore,
    PREPARED,
    OBSERVED,
    command_fingerprint,
)
from docker_process_supervision import (
    ProcessStatus,
    observe_linux_process,
)
from docker_start_barrier import spawn_blocked_child
from lab_rollback_command import PREVIOUS, plan_lab_rollback
from rollback_attempt_store import validate_attempt_record


@dataclass
class BoundBarrier:
    store: DockerExecutionEvidenceStore
    release_id: str
    execution_id: str
    operation_fingerprint: str
    command_fingerprint: str
    child: object

    def verify(self):
        """Verify durable binding and current Linux process identity."""
        record = self.store.read(self.release_id)

        if record["phase"] != OBSERVED:
            raise ValueError("Durable process observation required")

        if record["execution_id"] != self.execution_id:
            raise ValueError("Execution identity changed")

        if record["operation_fingerprint"] != self.operation_fingerprint:
            raise ValueError("Operation fingerprint changed")

        if record["command_fingerprint"] != self.command_fingerprint:
            raise ValueError("Command fingerprint changed")

        if record["pid"] != self.child.identity.pid:
            raise ValueError("Durable PID mismatch")

        if record["start_ticks"] != self.child.identity.start_ticks:
            raise ValueError("Durable kernel start-time mismatch")

        observation = observe_linux_process(self.child.identity)

        if observation.status != ProcessStatus.ACTIVE:
            raise ValueError("Original blocked child is not active")

        if self.child.released or self.child.release_fd < 0:
            raise ValueError("Barrier already released or closed")

        return True

    def release(self):
        """Release the inert child only after durable revalidation."""
        try:
            self.verify()
            self.child.release()
        except BaseException:
            self.child.close_without_release()
            raise

    def close_without_release(self):
        self.child.close_without_release()

    def wait(self, timeout=10):
        return self.child.wait(timeout=timeout)


def prepare_bound_barrier(store, attempt, marker):
    """Prepare, spawn and bind an inert child; do not release it.

    The caller must hold a valid deployment lease throughout.
    A PREPARED record remains unresolved after any launch failure.
    """
    if not isinstance(store, DockerExecutionEvidenceStore):
        raise ValueError("DockerExecutionEvidenceStore required")

    validate_attempt_record(attempt)

    if attempt.get("schema_version") != 2:
        raise ValueError("Bound rollback attempt required")

    if attempt["status"] != "STARTED":
        raise ValueError("Active STARTED attempt required")

    if not isinstance(marker, str) or not marker:
        raise ValueError("Inert marker path required")

    command = plan_lab_rollback(PREVIOUS)
    prepared = store.prepare(attempt, command)

    if prepared["phase"] != PREPARED:
        raise ValueError("Durable PREPARED record required")

    child = None

    try:
        # The spawned child is blocked on an inherited pipe.
        # It has no Docker-changing capability.
        child = spawn_blocked_child(marker)

        observed = store.observe(
            attempt["release_id"],
            child.identity,
        )

        if observed["phase"] != OBSERVED:
            raise ValueError("Durable OBSERVED record required")

        binding = BoundBarrier(
            store=store,
            release_id=attempt["release_id"],
            execution_id=attempt["execution_id"],
            operation_fingerprint=attempt["operation_fingerprint"],
            command_fingerprint=command_fingerprint(command),
            child=child,
        )

        binding.verify()
        return binding

    except BaseException:
        if child is not None:
            child.close_without_release()
            child.wait(timeout=10)
        raise
