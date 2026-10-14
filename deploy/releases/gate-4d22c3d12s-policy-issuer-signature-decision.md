# Gate 4D.22C.3D.12S - Pure Replay Policy Issuer Signature and Approval Evidence

Status: OFFLINE LABORATORY ONLY - NON-AUTHORIZING
Date: 2026-10-14

Docker execution: DENIED
Automatic retries: DENIED
Production deployment: DISABLED
Independent issuer trust roots: NOT PROVISIONED
Issuer identity independently authenticated: NOT IMPLEMENTED
Administrative approval independently authenticated: NOT IMPLEMENTED
Protected policy currentness: NOT IMPLEMENTED
Protected policy storage and durable commits: NOT IMPLEMENTED
Independent policy rollback witness: NOT IMPLEMENTED
Trusted time: NOT IMPLEMENTED
Automatic recovery: NOT IMPLEMENTED
Runtime isolation: NOT VERIFIED

## 1. Decision

Implement strict offline Ed25519 verification for caller-supplied replay
trust-policy issuer keys and an immutable, non-authorizing approval declaration.
This translates the Gate 3D.12R architecture into pure contracts and tests.

## 2. Dependencies

Reuse Gate 3D.12Q ReplayPolicySnapshot, its canonical domain-separated
commitment and structural validation. Do not alter the replay-response verifier
from Gate 3D.12O, the ordinary policy continuity module or any existing code.

## 3. Issuer Trust Domain

The issuer purpose and signing domain are different from registry ADMIN,
REPLAY_STATE and REPLAY_WITNESS signing purposes. Reusing an existing
response signature cannot approve a replay policy.

## 4. Caller-Supplied Issuer Keys

ReplayPolicyIssuerKeyPolicy contains a versioned issuer-key policy identifier
and a bounded, canonically ordered tuple of ReplayPolicyIssuerKey records.
Each key binds issuer, key ID, Ed25519 public key, separate signing purpose,
status and declared validity interval. Retired keys cannot sign successfully
under a supplied active-policy check. No independent root is provisioned.

## 5. Approval Declaration

ReplayPolicyApprovalDeclaration binds registry, ledger, policy, issuer,
approval reference, transition ID, predecessor and proposed policy commitments,
policy epoch, generation, recovery epoch, declared decision and at least two
separately named, caller-supplied approver labels.

These labels are NOT authenticated human identities or actual approvals.
A signer may manufacture matching labels and a valid approval checksum.

## 6. Bootstrap Versus Rotation

The exact decision label is BOOTSTRAP_DECLARATION for genesis and
ROTATION_DECLARATION for later epochs. Both are structural declarations only.
No bootstrap or rotation is independently approved by this contract.

## 7. Signed Envelope

SignedReplayPolicyEnvelope binds format version, issuer identity, key ID,
registry, ledger, policy identity, epoch, generation, recovery epoch,
previous policy commitment, transition ID, approval reference, complete
policy commitment, declared approval commitment, algorithm and issuer purpose.
Only the signature field is omitted from the signing bytes.

## 8. Canonical Wire Format

A separate issuer-specific signature domain prefixes sorted, whitespace-free,
ASCII-escaped canonical JSON. The parser rejects duplicate or unknown fields,
missing fields, wrong primitive types, noncanonical bytes, bad signatures,
invalid algorithms and oversized messages.

## 9. Signature Verification

Verification checks the exact policy and declared approval commitments,
expected caller-supplied issuer label, supplied issuer key policy, declared
key status, validity under caller-supplied time, distinct issuer/replay key
material, and Ed25519 signature integrity.

A positive result only means a particular signature verifies under a
caller-supplied key and that the supplied declarations are logically bound.

## 10. Currentness and Continuity Boundary

A valid signature on an older policy can still verify. This module does not
establish the latest independently accepted policy epoch, read a protected
policy-state authority or authenticate an independent policy witness.
Ordinary rotation continuity remains a separate Gate 3D.12Q pure assessment.

## 11. Cryptographic Approval Boundary

Binding two named approvers within an issuer-signed declaration does NOT
establish their actual consent, independent identities, permission or
separation of duties. A future policy requires authenticated approvals
from a protected authority outside the issuer's own signing claim.

## 12. Reconciliation and Unknown Commits

No real conditional policy commit, witness advancement, automatic catch-up,
rollback recovery or retry is performed. Signed policy evidence is not
proof of a durable database write or successful atomic transaction.

## 13. Security Assessment

The immutable assessment reports signature integrity under supplied key,
policy-byte and approval-declaration binding. Independent issuer identity,
root provenance, approver authentication, protected currentness, durable
commits, trusted time, rollback prevention, recovery and execution permissions
remain false. Manual verification is always required.

## 14. Adversarial Validation

Tests cover valid Ed25519 signatures, independent signing domain, signature
and policy tampering, approval mismatches, bogus decision or approver labels,
revoked or disabled keys, incorrect declared time, replay key-material overlap,
canonical wire violations, old signed policies and non-authorizing flags.
No operational signing keys are created or installed; tests use ephemeral
in-memory issuer keys.

## 15. Deferred Operational Dependencies

Independently provisioned trusted issuer roots, real approval authority,
protected key revocation, protected policy generation, independent witness,
trusted freshness, durable transactions and reviewed recovery remain absent.

## 16. Final Decision

Gate 3D.12S implements pure offline issuer-signature and declared approval
evidence contracts only. Matching signatures and approval labels are NOT
independent authority evidence. Docker execution, automatic retries and
production deployment remain blocked.
