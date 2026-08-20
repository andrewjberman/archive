"""precondition_token.py -- NFRA_EPISTEMY Component 10, the PRECONDITION-TOKEN leg.

BUILD-STAGING ONLY. Nothing in this module is wired into any live write path. Its
activation as a real gate on any mutation class is a separate, WORDED act (Andrew's,
per the no-gates-without-his-word law). This module is a capability a wiring proposal
may LATER connect to safe-deploy's code-artifact put -- it connects nothing today.

WHAT IT IS
----------
A `Precondition_Token` (S5 sec.1 `precondition_token` row; PRD sec.2.6 element D) is a
LIVE read of a target's state, taken inside a declared window, ATOMICALLY BOUND to the
write it authorizes. `put_if_precondition(bucket, key, body, token)` performs the write
bound to that token using S3's OWN conditional write (If-Match for an update, If-None-Match
for a first mint) -- rung 4 of the Build Ladder, a NATIVE platform feature: no lock table,
no second store, no DynamoDB. A world that moved under the token expires it: the store
returns 412 PreconditionFailed and the write is refused with the TYPED two-field rejection
(gate=TRANSACTION, reason=PRECONDITION_CHANGED -- S5 sec.2, REUSED not re-coined).

WHY IT IS A REAL PRECONDITION AND NOT A CHECK-THEN-ACT
-----------------------------------------------------
The bounded class this leg is cut for -- safe-deploy's `aws s3 cp` of gold/silver code
artifacts (`safe_deploy_core.py:549 deploy_file`, `:665 mint_bundle`) -- already reads the
object back after the put to verify its ETag. But that is a check AFTER an UNCONDITIONAL
last-writer-wins put: it confirms "my bytes landed", never "I did not clobber a writer who
landed between my read and my put". Binding the write to the ETag S3 itself evaluates closes
that window atomically, on the store, with no gap for a second writer to slip through. If an
implementation of this ever needs a lock table or a second store to work, that is the
mechanism FAILING ITS OWN PREMISE -- STOP AND SURFACE (CTO arch condition 1, TO 63836).

THE VERIFYING RE-READ IS LOAD-BEARING (the 2026-07-13 class)
-----------------------------------------------------------
A "successful" put whose bytes never landed -- a hung `aws s3 cp --quiet` that reports rc=0
while S3 keeps the old object -- is the exact failure this leg exists to close. So a 200 from
the store is NOT the success signal; the success signal is a re-read that confirms the stored
object is the object we wrote. Omit that re-read and a lie reads as a commit (mutant m4, the
one that matters most -- CTO arch condition 2). The re-read is a distinct, separately
mutable step here precisely so the mutant battery can show it firing.

ESTATE PRECEDENT (Build Ladder rung 2): `infra/aws/globgrph/probe_ifmatch_cas.py` already
exercises PutObject(IfMatch=) end-to-end on this account's runtimes and names the three
outcomes -- SUPPORTED (412 on a wrong ETag + 200 on the right one), ABSENT (ParamValidationError),
and IGNORED (a wrong-ETag put that SUCCEEDS -- a CAS that guards nothing). This module reuses
that 412-discrimination idiom rather than re-deriving it.

Source of record (CITED, never re-declared): S5
`org/tier1_exec/4.0.0_SA_CRO/deliverables/NFRA_EPISTEMY/S5_PROFILE_ALGEBRA_AND_MUTATION_GATEWAY_SPEC_20260820.md`
sec.1 (the `precondition_token` row), sec.2 (the two-field rejection), sec.4 (estate
correspondence: the naked layer = plain S3 put). The Precondition_Token SCHEMA ACT routes
through 4.0.0_SA_CRO base (registry executor); this module does not become a competing
source of record. The Observation_Record envelope is CONSUMED from Component 1
(`observation_record.schema.json`), not redefined here.
"""
from __future__ import annotations

import dataclasses
import hashlib
import json
from datetime import datetime, timezone
from typing import Any, Callable, Optional

# --- The typed rejection vocabulary (S5 sec.2 -- REUSED, not re-coined). -------------------
# gate x reason, two fields, because one flat enum mixes WHERE it failed with WHY.
GATE_TRANSACTION = "TRANSACTION"
REASON_PRECONDITION_CHANGED = "PRECONDITION_CHANGED"

# The first-mint sentinel: the token asserts the target is ABSENT and the write must be the
# first one. Distinct from a null digest (which is a REFUSED token -- see S6 semantics below).
PRECOND_ABSENT = "ABSENT"

# S6 absence semantics, made explicit as detail codes on a REFUSED token. A null field is NOT
# "no constraint" -- it is a token we REFUSE to act on. These ride in Rejection.detail; the
# canonical (gate, reason) stays the reused S5 pair. S5 sec.2 has no distinct TRANSACTION
# reason for an inadmissible/malformed token; coining one here would violate the CITE-NOT-COPY
# / reuse-not-re-coin rider, so the discriminator lives in detail and a distinct typed reason
# (e.g. TOKEN_INADMISSIBLE) is recorded as a PROPOSAL to base in the Rule-24 record, not minted.
DETAIL_WINDOW_EXPIRED = "WINDOW_EXPIRED"                 # token older than its window at act time
DETAIL_READ_WINDOW_NULL = "READ_WINDOW_NULL_REFUSED"    # null window -> REFUSED (S6), not "no window"
DETAIL_DIGEST_NULL = "DIGEST_NULL_REFUSED"              # null digest (and not the ABSENT sentinel) -> REFUSED (S6)
DETAIL_READ_AT_NULL = "READ_AT_NULL_REFUSED"           # null read_at -> cannot place the read in time -> REFUSED
DETAIL_ETAG_MISMATCH_412 = "ETAG_MISMATCH_412"          # If-Match rejected: current ETag != token digest
DETAIL_ALREADY_EXISTS_412 = "ALREADY_EXISTS_412"        # If-None-Match rejected: object exists, not a first mint

# Plane is carried OPAQUE (CTO bind-time condition 63744): no consumer may parse, branch on,
# or key off `plane` until the ratified plane enum lands. This module sets it and never reads it.
PLANE_OPAQUE = "s3-object"

INSTRUMENT_ID = "precondition_token.put_if_precondition"
INSTRUMENT_VERSION = "0.1.0-staged"


class StopAndSurface(RuntimeError):
    """Raised when the mechanism would have to abandon rung 4 (a lock table / second store)
    to work. Per CTO arch condition 1 this is not an implementation detail to route around --
    it is the precondition mechanism failing its own premise, and it must halt loud."""


@dataclasses.dataclass(frozen=True)
class Rejection:
    """The typed two-field rejection (S5 sec.2). `detail` carries the S6/412 discriminator
    without inventing a new reason value."""
    gate: str
    reason: str
    detail: str

    def as_dict(self) -> dict:
        return {"gate": self.gate, "reason": self.reason, "detail": self.detail}


@dataclasses.dataclass(frozen=True)
class PreconditionToken:
    """S5 sec.1 `precondition_token`: {target_state_digest, read_at, read_window}, a LIVE read
    inside a declared window, atomically bound at act time.

    target_state_digest: the object's ETag as the store returned it (the value If-Match
        evaluates -- the ONLY value S3 will condition on, so it is the binding anchor even
        when a multipart ETag is not the object's MD5); or PRECOND_ABSENT for a first-mint
        intent; or None (a REFUSED token -- S6: a null digest is not "no precondition").
    read_at: ISO-8601 UTC instant the state was read. None -> REFUSED (cannot place the read).
    read_window_seconds: how long after read_at the token stays admissible. None -> REFUSED
        (S6: a null window is not "no window").
    content_sha256: OPTIONAL secondary content cross-check (sha256 of the read bytes). NEVER the
        binding anchor -- recorded only where a multipart ETag makes byte-identity ambiguous."""
    target_state_digest: Optional[str]
    read_at: Optional[str]
    read_window_seconds: Optional[int]
    content_sha256: Optional[str] = None

    def as_dict(self) -> dict:
        return dataclasses.asdict(self)


@dataclasses.dataclass(frozen=True)
class PutOutcome:
    """Result of an attempted bound write.

    outcome:
      COMMITTED     -- the conditional put landed AND a verifying re-read confirmed it.
      REJECTED      -- a typed rejection (token out of window / REFUSED / 412 from the store).
      VERIFY_FAILED -- the put reported success but the verifying re-read did NOT confirm the
                       written bytes (the 2026-07-13 hung-cp-reports-success class, caught).
    """
    outcome: str
    rejection: Optional[Rejection]
    committed_etag: Optional[str]
    observations: list[dict]

    def as_dict(self) -> dict:
        return {
            "outcome": self.outcome,
            "rejection": self.rejection.as_dict() if self.rejection else None,
            "committed_etag": self.committed_etag,
            "observations": self.observations,
        }


def _now_utc() -> datetime:
    return datetime.now(timezone.utc)


def _iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).isoformat()


def _request_hash(payload: dict) -> str:
    canon = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "sha256:" + hashlib.sha256(canon).hexdigest()


def observe(
    *,
    request: dict,
    acquisition: str,
    value: Any,
    unknown_reason: Optional[str],
    population_predicate: str,
    denominator_count: Optional[int],
    denominator_grain: str,
    generated_by: str,
    support_pointers: list[str],
    invalidation_predicates: list[str],
    transport: str = "SUCCEEDED",
    enumeration: str = "SUCCEEDED",
    parse: str = "SUCCEEDED",
) -> dict:
    """Build one Observation_Record conformant to Component 1's envelope (P6).

    Honesty rule enforced here, matching the C1 schema's own allOf: a substantive value is
    KNOWN only when the whole status tuple is (PRESENT, SUCCEEDED, SUCCEEDED, SUCCEEDED). Any
    other status -> substantive_result UNKNOWN with a reason. A head-object that fails is not
    'no object'; a clean 404 is acquisition=ABSENT with the absence carried in status, value
    UNKNOWN because an absent object has no value to report."""
    all_succeeded = (
        acquisition == "PRESENT"
        and transport == "SUCCEEDED"
        and enumeration == "SUCCEEDED"
        and parse == "SUCCEEDED"
    )
    if all_succeeded:
        substantive = {"state": "KNOWN", "value": value, "reason": None}
    else:
        substantive = {
            "state": "UNKNOWN",
            "value": None,
            "reason": unknown_reason or f"status not all-succeeded: acquisition={acquisition}",
        }
    return {
        "instrument": {"id": INSTRUMENT_ID, "version": INSTRUMENT_VERSION},
        "request_hash": _request_hash(request),
        "status": {
            "acquisition": acquisition,
            "transport": transport,
            "enumeration": enumeration,
            "parse": parse,
        },
        "plane": PLANE_OPAQUE,  # opaque; never branched on (CTO 63744 bind-time condition)
        "population_predicate": population_predicate,
        "denominator": {
            "count": denominator_count,
            "grain": denominator_grain,
            "generated_by": generated_by,
        },
        "traversal_residue": [],
        "substantive_result": substantive,
        "control_references": [],
        "discrimination_certificate_ref": None,
        "observed_at": _iso(_now_utc()),
        "support_pointers": support_pointers,
        "invalidation_predicates": invalidation_predicates,
    }


def _s3_uri(bucket: str, key: str) -> str:
    return f"s3://{bucket}/{key}"


def _head_etag(client, bucket: str, key: str) -> tuple[str, Optional[str], dict]:
    """Read the current state of a target object. Returns (acquisition, etag, observation).

    acquisition in {PRESENT, ABSENT, UNKNOWN}. A 404 is a CLEAN ABSENT (etag None); any other
    error is UNKNOWN (etag None) -- an unreadable object is not an absent one."""
    from botocore.exceptions import ClientError

    request = {"op": "head_object", "bucket": bucket, "key": key}
    try:
        head = client.head_object(Bucket=bucket, Key=key)
        etag = head.get("ETag")
        obs = observe(
            request=request,
            acquisition="PRESENT",
            value={"etag": etag},
            unknown_reason=None,
            population_predicate=f"single S3 object head: {_s3_uri(bucket, key)}",
            denominator_count=1,
            denominator_grain="s3-object",
            generated_by="s3:HeadObject",
            support_pointers=[_s3_uri(bucket, key)],
            invalidation_predicates=["object ETag changes", "object is deleted"],
        )
        return "PRESENT", etag, obs
    except ClientError as exc:
        status = exc.response.get("ResponseMetadata", {}).get("HTTPStatusCode")
        code = exc.response.get("Error", {}).get("Code")
        if status == 404 or code in ("404", "NoSuchKey", "NotFound"):
            obs = observe(
                request=request,
                acquisition="ABSENT",
                value=None,
                unknown_reason=f"object absent (404 {code}) -> first-mint intent",
                population_predicate=f"single S3 object head: {_s3_uri(bucket, key)}",
                denominator_count=0,
                denominator_grain="s3-object",
                generated_by="s3:HeadObject",
                support_pointers=[_s3_uri(bucket, key)],
                invalidation_predicates=["an object is created at this key"],
            )
            return "ABSENT", None, obs
        obs = observe(
            request=request,
            acquisition="UNKNOWN",
            value=None,
            unknown_reason=f"head-object failed, not a clean 404: {status} {code}",
            population_predicate=f"single S3 object head: {_s3_uri(bucket, key)}",
            denominator_count=None,
            denominator_grain="s3-object",
            generated_by="s3:HeadObject",
            support_pointers=[_s3_uri(bucket, key)],
            invalidation_predicates=["the transient condition clears and the object is readable"],
            transport="FAILED",
        )
        return "UNKNOWN", None, obs


def read_precondition_token(
    bucket: str,
    key: str,
    read_window_seconds: int,
    *,
    client=None,
    content_sha256: Optional[str] = None,
) -> tuple[Optional[PreconditionToken], dict]:
    """Take a LIVE read of the target and mint a token bound to it (S5 sec.1). Returns
    (token, observation). A PRESENT object -> digest = its ETag; a clean ABSENT -> digest =
    PRECOND_ABSENT (first-mint intent); an UNKNOWN read -> no token (None): we will not bind a
    write to a state we could not read."""
    client = client or _default_s3()
    acquisition, etag, obs = _head_etag(client, bucket, key)
    read_at = _iso(_now_utc())
    if acquisition == "PRESENT":
        return PreconditionToken(etag, read_at, read_window_seconds, content_sha256), obs
    if acquisition == "ABSENT":
        return PreconditionToken(PRECOND_ABSENT, read_at, read_window_seconds, content_sha256), obs
    return None, obs  # UNKNOWN: an unreadable target yields no token, never a silent guess


def _default_s3():
    import boto3

    return boto3.client("s3", region_name="us-east-1")


def _validate_token(token: PreconditionToken) -> Optional[Rejection]:
    """Token admissibility, evaluated BEFORE any store call (S5 sec.1; P2 'rejected before any
    call'). Null fields are REFUSED per S6 absence semantics -- a null is never read as 'no
    constraint'. An out-of-window token is PRECONDITION_CHANGED."""
    if token.read_window_seconds is None:
        return Rejection(GATE_TRANSACTION, REASON_PRECONDITION_CHANGED, DETAIL_READ_WINDOW_NULL)
    if token.target_state_digest is None:
        return Rejection(GATE_TRANSACTION, REASON_PRECONDITION_CHANGED, DETAIL_DIGEST_NULL)
    if token.read_at is None:
        return Rejection(GATE_TRANSACTION, REASON_PRECONDITION_CHANGED, DETAIL_READ_AT_NULL)
    try:
        read_at = datetime.fromisoformat(token.read_at)
    except (ValueError, TypeError):
        return Rejection(GATE_TRANSACTION, REASON_PRECONDITION_CHANGED, DETAIL_READ_AT_NULL)
    if read_at.tzinfo is None:
        read_at = read_at.replace(tzinfo=timezone.utc)
    age = (_now_utc() - read_at).total_seconds()
    if age > token.read_window_seconds or age < 0:
        return Rejection(GATE_TRANSACTION, REASON_PRECONDITION_CHANGED, DETAIL_WINDOW_EXPIRED)
    return None


def put_if_precondition(
    bucket: str,
    key: str,
    body: bytes,
    token: PreconditionToken,
    *,
    client=None,
    content_type: str = "application/octet-stream",
    # --- MUTATION HOOKS (test-only; the mutant battery sets these to exercise the controls;
    #     every non-test caller leaves them at their safe defaults). ---
    _omit_conditional_header: bool = False,   # m1: drop the If-Match/If-None-Match binding
    _skip_verify_reread: bool = False,        # m4: return success without the verifying re-read
    _lying_put: Optional[Callable[[], dict]] = None,  # m4 driver: a put that claims 200 without writing
) -> PutOutcome:
    """Write `body` to `bucket/key`, ATOMICALLY BOUND to `token` via S3's own conditional
    write (P2). Rung 4: no lock table, no second store.

      - token.target_state_digest == PRECOND_ABSENT -> IfNoneMatch='*' (write iff object absent).
      - otherwise                                    -> IfMatch=<digest>  (write iff ETag unchanged).

    A precondition failure returns REJECTED (gate=TRANSACTION, reason=PRECONDITION_CHANGED) and
    the object is confirmed byte-unchanged by a re-read, not assumed. A store 200 is verified by
    a re-read before it is called COMMITTED; a put that reports success but does not verify is
    VERIFY_FAILED (the 2026-07-13 class)."""
    from botocore.exceptions import ClientError, ParamValidationError

    client = client or _default_s3()
    observations: list[dict] = []

    # 1. Admissibility BEFORE any call.
    rej = _validate_token(token)
    if rej is not None:
        return PutOutcome("REJECTED", rej, None, observations)

    first_mint = token.target_state_digest == PRECOND_ABSENT

    # 2. The atomically-bound put. The conditional header IS the mechanism; omitting it (m1)
    #    reduces this to a last-writer-wins put with no guard.
    put_kwargs: dict = {"Bucket": bucket, "Key": key, "Body": body, "ContentType": content_type}
    if not _omit_conditional_header:
        if first_mint:
            put_kwargs["IfNoneMatch"] = "*"
        else:
            put_kwargs["IfMatch"] = token.target_state_digest

    try:
        if _lying_put is not None:
            put_resp = _lying_put()  # a transport that claims success without writing (m4 driver)
        else:
            put_resp = client.put_object(**put_kwargs)
    except ParamValidationError as exc:
        # The runtime does not know the conditional parameter. Per the probe's ABSENT verdict this
        # is a runtime gap, not a rejection of the write -- surfaced, never swallowed into a WARN.
        raise StopAndSurface(
            "S3 conditional-write parameter not honoured by this runtime "
            f"(ParamValidationError: {exc}). The precondition cannot be atomically bound here; "
            "moving the boto3 pin is its own change. See probe_ifmatch_cas.py VERDICT=ABSENT."
        ) from exc
    except ClientError as exc:
        status = exc.response.get("ResponseMetadata", {}).get("HTTPStatusCode")
        code = exc.response.get("Error", {}).get("Code")
        if status == 412 or code in ("PreconditionFailed", "412"):
            # The world moved under the token. Confirm the object is byte-unchanged (P2: verified,
            # not assumed) and return the typed rejection.
            detail = DETAIL_ALREADY_EXISTS_412 if first_mint else DETAIL_ETAG_MISMATCH_412
            acq, _etag, obs = _head_etag(client, bucket, key)
            observations.append(obs)
            return PutOutcome(
                "REJECTED",
                Rejection(GATE_TRANSACTION, REASON_PRECONDITION_CHANGED, detail),
                None,
                observations,
            )
        raise  # any other ClientError is a real fault, not a precondition outcome -- surface it

    # 3. The verifying re-read. A 200 is a CLAIM; the commit signal is a re-read that confirms the
    #    stored object is the one we wrote. This step is what catches the hung-cp lie (m4).
    put_etag = put_resp.get("ETag")
    if _skip_verify_reread:
        # m4 mutant: trust the put's own report. A lie here becomes a false COMMITTED.
        return PutOutcome("COMMITTED", None, put_etag, observations)

    acq, stored_etag, obs = _head_etag(client, bucket, key)
    observations.append(obs)
    if acq != "PRESENT" or stored_etag != put_etag:
        # The put claimed success; the store does not corroborate it. Do NOT report COMMITTED.
        return PutOutcome(
            "VERIFY_FAILED",
            Rejection(
                GATE_TRANSACTION,
                REASON_PRECONDITION_CHANGED,
                f"put reported etag={put_etag} but re-read acquisition={acq} etag={stored_etag} "
                "-- unverified write (2026-07-13 hung-cp-reports-success class)",
            ),
            None,
            observations,
        )
    return PutOutcome("COMMITTED", None, stored_etag, observations)
