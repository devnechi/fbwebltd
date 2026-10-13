#!/usr/bin/env python3
"""Gate 4D.22C: syntax-level execution-boundary audit.

This is a targeted structural check, not a complete security proof.
The Docker executor is expected to remain unintegrated and blocked.
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
                    isinstance(
                        member,
                        (ast.FunctionDef, ast.AsyncFunctionDef)
                    )
                    and member.name == method_name
                ):
                    return member

    raise ValueError(
        f"Missing {class_name}.{method_name}"
    )


def function_node(tree, name):
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == name:
            return node

    raise ValueError(f"Missing function: {name}")


def direct_calls(node):
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
    executor = syntax_tree("lab_rollback_executor.py")

    findings = []

    for name in ("prepare", "observe", "record_exit", "_write"):
        method = class_method(
            evidence, "DockerExecutionEvidenceStore", name
        )

        if "require_lease" not in direct_calls(method):
            findings.append(
                f"BASE_STORE_UNGUARDED_{name.upper()}"
            )

    launcher = function_node(executor, "_run_restoration")

    if "run" in direct_calls(launcher):
        findings.append("LEGACY_DIRECT_SUBPROCESS_RUN")

    execution = function_node(executor, "execute_lab_rollback")

    if "prepare_locked_barrier" not in direct_calls(execution):
        findings.append("EXECUTOR_NOT_BARRIER_INTEGRATED")

    return tuple(sorted(set(findings)))


class ExecutionBoundaryAuditTests(unittest.TestCase):

    def test_base_prepare_has_lease_guard(self):
        self.assertNotIn(
            "BASE_STORE_UNGUARDED_PREPARE",
            audit_boundary(),
        )

    def test_base_observe_has_lease_guard(self):
        self.assertNotIn(
            "BASE_STORE_UNGUARDED_OBSERVE",
            audit_boundary(),
        )

    def test_base_exit_has_lease_guard(self):
        self.assertNotIn(
            "BASE_STORE_UNGUARDED_RECORD_EXIT",
            audit_boundary(),
        )

    def test_internal_writer_has_lease_guard(self):
        self.assertNotIn(
            "BASE_STORE_UNGUARDED__WRITE",
            audit_boundary(),
        )

    def test_legacy_launcher_remains_blocked(self):
        findings = audit_boundary()

        self.assertIn(
            "LEGACY_DIRECT_SUBPROCESS_RUN",
            findings,
        )
        self.assertIn(
            "EXECUTOR_NOT_BARRIER_INTEGRATED",
            findings,
        )

    def test_only_expected_integration_blockers_remain(self):
        self.assertEqual(
            set(audit_boundary()),
            {
                "LEGACY_DIRECT_SUBPROCESS_RUN",
                "EXECUTOR_NOT_BARRIER_INTEGRATED",
            },
        )


if __name__ == "__main__":
    unittest.main()
