#!/usr/bin/env python3
"""Gate 4D.22C.1: non-executing architecture bypass audit.

This test suite confirms that known execution-boundary gaps are
identified. It does not claim the gaps have been remediated.
"""

import ast
from pathlib import Path
import unittest


RELEASES = Path(__file__).resolve().parents[1] / "releases"


def syntax_tree(filename):
    source = (RELEASES / filename).read_text(encoding="utf-8")
    return ast.parse(source)


def class_method(tree, class_name, method_name):
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            for member in node.body:
                if (
                    isinstance(member, (ast.FunctionDef, ast.AsyncFunctionDef))
                    and member.name == method_name
                ):
                    return member
    raise ValueError(f"Missing {class_name}.{method_name}")


def function_node(tree, name):
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == name:
            return node
    raise ValueError(f"Missing function: {name}")


def direct_calls(node):
    """Return direct syntactic calls, not inferred runtime behavior."""
    result = set()

    for child in ast.walk(node):
        if not isinstance(child, ast.Call):
            continue

        fn = child.func

        if isinstance(fn, ast.Name):
            result.add(fn.id)
        elif isinstance(fn, ast.Attribute):
            result.add(fn.attr)

    return result


def audit_boundary():
    evidence = syntax_tree("docker_execution_evidence.py")
    locked = syntax_tree("locked_durable_barrier.py")
    executor = syntax_tree("lab_rollback_executor.py")

    findings = []

    for name in ("prepare", "observe", "record_exit"):
        base_method = class_method(
            evidence, "DockerExecutionEvidenceStore", name
        )

        locked_method = class_method(
            locked, "LockedEvidenceStore", name
        )

        if "require_lease" not in direct_calls(base_method):
            findings.append(
                f"BASE_STORE_UNGUARDED_{name.upper()}"
            )

        if "require_lease" not in direct_calls(locked_method):
            findings.append(
                f"LOCKED_FACADE_UNGUARDED_{name.upper()}"
            )

    launcher = function_node(executor, "_run_restoration")
    launcher_calls = direct_calls(launcher)

    if "run" in launcher_calls:
        findings.append("LEGACY_DIRECT_SUBPROCESS_RUN")

    execution = function_node(executor, "execute_lab_rollback")
    execution_calls = direct_calls(execution)

    if "prepare_locked_barrier" not in execution_calls:
        findings.append("EXECUTOR_NOT_BARRIER_INTEGRATED")

    return tuple(sorted(set(findings)))


class ExecutionBoundaryAuditTests(unittest.TestCase):

    def test_known_base_store_bypasses_detected(self):
        findings = audit_boundary()

        self.assertIn(
            "BASE_STORE_UNGUARDED_PREPARE", findings
        )
        self.assertIn(
            "BASE_STORE_UNGUARDED_OBSERVE", findings
        )
        self.assertIn(
            "BASE_STORE_UNGUARDED_RECORD_EXIT", findings
        )

    def test_locked_facade_has_lease_checks(self):
        findings = audit_boundary()

        for name in ("PREPARE", "OBSERVE", "RECORD_EXIT"):
            self.assertNotIn(
                f"LOCKED_FACADE_UNGUARDED_{name}",
                findings,
            )

    def test_legacy_launcher_detected(self):
        self.assertIn(
            "LEGACY_DIRECT_SUBPROCESS_RUN",
            audit_boundary(),
        )

    def test_missing_barrier_integration_detected(self):
        self.assertIn(
            "EXECUTOR_NOT_BARRIER_INTEGRATED",
            audit_boundary(),
        )

    def test_current_execution_boundary_is_blocked(self):
        findings = audit_boundary()
        self.assertGreater(len(findings), 0)


if __name__ == "__main__":
    unittest.main()
