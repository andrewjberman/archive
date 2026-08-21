"""exercise_precond.py -- P3 (real-plane exercise) + P4 (mutant battery) for the precondition
-token leg. NOTHING here is wired into a deploy; it writes ONLY to a scratch prefix under the
bounded class's bucket and deletes every object it mints.

Run:  python exercise_precond.py --bucket opal-data-bd [--prefix _probe/c10-precond/]
Exit: 0 iff every P3 scenario PASSES, every mutant FIRES, every Observation_Record validates
      against the Component 1 envelope, and the verdict set is byte-stable across two runs.

The bounded class's real plane is the S3 code-artifact-put surface of safe-deploy
(safe_deploy_core.py deploy_file/mint_bundle). We exercise the SAME store, SAME runtime, SAME
account under a dedicated scratch prefix -- the probe_ifmatch_cas.py precedent exactly: same
plane, no litter in the live `code/` namespace.
"""
from __future__ import annotations

import argparse
import json
import sys
import uuid
from datetime import timedelta

from precondition_token import (
    DETAIL_ALREADY_EXISTS_412,
    DETAIL_ETAG_MISMATCH_412,
    DETAIL_READ_WINDOW_NULL,
    DETAIL_WINDOW_EXPIRED,
    GATE_COMPILATION,
    PRECOND_ABSENT,
    PreconditionToken,
    REASON_BUNDLE_MALFORMED,
    _iso,
    _now_utc,
    put_if_precondition,
    read_precondition_token,
)

# Safety: this leg's bounded class writes to the firm code trees. We refuse anything that is not
# our scratch prefix, and we refuse the globgrph warehouse outright (its mark+sweep reasons about
# reachability and would treat probe litter as a GC candidate).
SCRATCH_PREFIX = "_probe/c10-precond/"
FORBIDDEN_BUCKETS = {"opal-313476888478-globgrph"}


class CountingS3:
    """Wraps a boto3 s3 client to count put/head calls -- used to PROVE 'no call made' when an
    out-of-window token is rejected before any store call (P3 case c)."""

    def __init__(self, inner):
        self.inner = inner
        self.put_calls = 0
        self.head_calls = 0

    def put_object(self, **kw):
        self.put_calls += 1
        return self.inner.put_object(**kw)

    def head_object(self, **kw):
        self.head_calls += 1
        return self.inner.head_object(**kw)

    def delete_object(self, **kw):
        return self.inner.delete_object(**kw)


class Harness:
    def __init__(self, bucket: str, prefix: str):
        import boto3

        if bucket in FORBIDDEN_BUCKETS:
            raise SystemExit(f"REFUSING: {bucket} is a mark+sweep warehouse; use a firm code bucket.")
        if not prefix.rstrip("/").endswith("c10-precond"):
            raise SystemExit(f"REFUSING: prefix '{prefix}' is not the c10-precond scratch prefix.")
        self.bucket = bucket
        self.prefix = prefix.rstrip("/") + "/"
        self.s3 = boto3.client("s3", region_name="us-east-1")
        self.minted: list[str] = []
        self.observations: list[dict] = []

    def _key(self, tag: str) -> str:
        k = f"{self.prefix}{tag}-{uuid.uuid4().hex}.bin"
        self.minted.append(k)
        return k

    def _seed(self, key: str, body: bytes) -> str:
        """Unconditional setup put (a second/first writer). Returns the ETag."""
        r = self.s3.put_object(Bucket=self.bucket, Key=key, Body=body,
                               ContentType="application/octet-stream")
        return r["ETag"]

    def _body_of(self, key: str) -> bytes:
        return self.s3.get_object(Bucket=self.bucket, Key=key)["Body"].read()

    def _exists(self, key: str) -> bool:
        from botocore.exceptions import ClientError

        try:
            self.s3.head_object(Bucket=self.bucket, Key=key)
            return True
        except ClientError:
            return False

    def cleanup(self) -> dict:
        deleted, failed = [], []
        for k in self.minted:
            try:
                self.s3.delete_object(Bucket=self.bucket, Key=k)
                deleted.append(k)
            except Exception as exc:  # noqa: BLE001 -- report, never mask a verdict
                failed.append(f"{k}: {exc}")
        return {"deleted": deleted, "failed": failed}

    # ---- P3: the real-plane scenarios ------------------------------------------------------
    def p3a_fresh_token_commit(self) -> dict:
        key = self._key("p3a")
        etag_a = self._seed(key, b"A-original")
        token, obs = read_precondition_token(self.bucket, key, 300, client=self.s3)
        self.observations.append(obs)
        res = put_if_precondition(self.bucket, key, b"B-updated", token, client=self.s3)
        self.observations.extend(res.observations)
        stored = self._body_of(key)
        ok = res.outcome == "COMMITTED" and stored == b"B-updated" and token.target_state_digest == etag_a
        return {"scenario": "P3a fresh-token commit", "outcome": res.outcome,
                "expected": "COMMITTED", "stored_matches_new": stored == b"B-updated",
                "denominator": "1 target object, 1 bound put", "pass": ok}

    def p3b_stale_token_rejected(self) -> dict:
        key = self._key("p3b")
        self._seed(key, b"A-original")
        token, obs = read_precondition_token(self.bucket, key, 300, client=self.s3)
        self.observations.append(obs)
        # A SECOND WRITER lands between the read and the bound put.
        self._seed(key, b"C-second-writer")
        res = put_if_precondition(self.bucket, key, b"B-updated", token, client=self.s3)
        self.observations.extend(res.observations)
        stored = self._body_of(key)
        ok = (res.outcome == "REJECTED"
              and res.rejection is not None
              and res.rejection.reason == "PRECONDITION_CHANGED"
              and res.rejection.detail == DETAIL_ETAG_MISMATCH_412
              and stored == b"C-second-writer")  # bytes UNCHANGED by our refused put
        return {"scenario": "P3b stale-token rejected (412), bytes unchanged", "outcome": res.outcome,
                "expected": "REJECTED/PRECONDITION_CHANGED", "bytes_unchanged": stored == b"C-second-writer",
                "detail": res.rejection.detail if res.rejection else None,
                "denominator": "1 target object, 1 interleaved writer, 1 bound put", "pass": ok}

    def p3c_expired_window_no_call(self) -> dict:
        key = self._key("p3c")
        etag_a = self._seed(key, b"A-original")
        # A token read 10s ago with a 1s window -> out of window NOW.
        token = PreconditionToken(etag_a, _iso(_now_utc() - timedelta(seconds=10)), 1)
        counting = CountingS3(self.s3)
        res = put_if_precondition(self.bucket, key, b"B-updated", token, client=counting)
        self.observations.extend(res.observations)
        ok = (res.outcome == "REJECTED"
              and res.rejection is not None
              and res.rejection.detail == DETAIL_WINDOW_EXPIRED
              and counting.put_calls == 0        # NO store call made
              and counting.head_calls == 0)      # not even a re-read
        return {"scenario": "P3c expired-window rejected with NO call made", "outcome": res.outcome,
                "expected": "REJECTED/WINDOW_EXPIRED", "store_put_calls": counting.put_calls,
                "store_head_calls": counting.head_calls,
                "denominator": "1 target object, 0 store calls (short-circuit before the put)", "pass": ok}

    def p3d_first_mint_once(self) -> dict:
        key = self._key("p3d")  # never seeded -> absent
        token1, obs1 = read_precondition_token(self.bucket, key, 300, client=self.s3)
        self.observations.append(obs1)
        res1 = put_if_precondition(self.bucket, key, b"first-mint", token1, client=self.s3)
        self.observations.extend(res1.observations)
        # A second first-mint attempt on the now-existing object must be rejected.
        token2 = PreconditionToken(PRECOND_ABSENT, _iso(_now_utc()), 300)
        res2 = put_if_precondition(self.bucket, key, b"second-mint", token2, client=self.s3)
        self.observations.extend(res2.observations)
        stored = self._body_of(key)
        ok = (token1.target_state_digest == PRECOND_ABSENT
              and res1.outcome == "COMMITTED"
              and res2.outcome == "REJECTED"
              and res2.rejection is not None
              and res2.rejection.detail == DETAIL_ALREADY_EXISTS_412
              and stored == b"first-mint")
        return {"scenario": "P3d first-mint succeeds once, repeat rejected",
                "outcome": f"{res1.outcome}->{res2.outcome}", "mint1": res1.outcome,
                "mint2": res2.outcome, "expected": "COMMITTED then REJECTED/ALREADY_EXISTS_412",
                "denominator": "1 target key, 2 first-mint attempts", "pass": ok}

    # ---- P4: the mutant battery. Each mutant MUST be caught ('FIRED'). --------------------
    def m1_conditional_header_load_bearing(self) -> dict:
        """Remove the If-Match binding; the stale-writer case (b) that must REJECT instead
        COMMITS. The header is load-bearing."""
        key = self._key("m1")
        self._seed(key, b"A-original")
        token, obs = read_precondition_token(self.bucket, key, 300, client=self.s3)
        self.observations.append(obs)
        self._seed(key, b"C-second-writer")  # world moves under the token
        mutant = put_if_precondition(self.bucket, key, b"B-updated", token, client=self.s3,
                                     _omit_conditional_header=True)
        self.observations.extend(mutant.observations)
        stored = self._body_of(key)
        # FIRED = removing the header turned a should-REJECT into a COMMIT that clobbered the writer.
        fired = mutant.outcome == "COMMITTED" and stored == b"B-updated"
        return {"mutant": "m1 conditional-header removed", "mutant_outcome": mutant.outcome,
                "real_code_would": "REJECTED (see P3b)", "clobbered_second_writer": stored == b"B-updated",
                "FIRED": fired}

    def m2_null_window_refused(self) -> dict:
        """A token with a null read_window must be REFUSED (S6), never treated as 'no window'."""
        key = self._key("m2")
        etag_a = self._seed(key, b"A-original")
        bad = PreconditionToken(etag_a, _iso(_now_utc()), None)  # null window
        res = put_if_precondition(self.bucket, key, b"B-updated", bad, client=self.s3)
        self.observations.extend(res.observations)
        stored = self._body_of(key)
        # A null field is a BUNDLE-SHAPE defect -> (COMPILATION, BUNDLE_MALFORMED), base ruling 63913.
        fired = (res.outcome == "REJECTED"
                 and res.rejection is not None
                 and res.rejection.gate == GATE_COMPILATION
                 and res.rejection.reason == REASON_BUNDLE_MALFORMED
                 and res.rejection.detail == DETAIL_READ_WINDOW_NULL
                 and stored == b"A-original")
        return {"mutant": "m2 null read_window", "outcome": res.outcome,
                "gate_reason": f"{res.rejection.gate}/{res.rejection.reason}" if res.rejection else None,
                "detail": res.rejection.detail if res.rejection else None,
                "refused_and_unchanged": stored == b"A-original", "FIRED": fired}

    def m3_wrong_object_digest_refused(self) -> dict:
        """A digest read from a DIFFERENT object must be refused by the CAS on the target."""
        other = self._key("m3-other")
        wrong_etag = self._seed(other, b"OTHER-object")
        target = self._key("m3-target")
        self._seed(target, b"TARGET-original")
        bad = PreconditionToken(wrong_etag, _iso(_now_utc()), 300)  # digest of the WRONG object
        res = put_if_precondition(self.bucket, target, b"B-updated", bad, client=self.s3)
        self.observations.extend(res.observations)
        stored = self._body_of(target)
        fired = (res.outcome == "REJECTED"
                 and res.rejection is not None
                 and res.rejection.detail == DETAIL_ETAG_MISMATCH_412
                 and stored == b"TARGET-original")
        return {"mutant": "m3 wrong-object digest", "outcome": res.outcome,
                "detail": res.rejection.detail if res.rejection else None,
                "target_unchanged": stored == b"TARGET-original", "FIRED": fired}

    def m4_skip_verify_reread(self) -> dict:
        """THE mutant that matters (CTO cond. 2). A put that CLAIMS success without writing (a
        hung-cp lie). With the verifying re-read ON, the lie is caught (VERIFY_FAILED). With the
        re-read SKIPPED, the same lie reads as COMMITTED. FIRED = the re-read is demonstrably
        load-bearing: removing it flips a caught lie into a false commit."""
        key = self._key("m4")
        etag_a = self._seed(key, b"A-original")
        token = PreconditionToken(etag_a, _iso(_now_utc()), 300)
        fake_etag = '"deadbeefdeadbeefdeadbeefdeadbeef"'

        def lying_put():
            # Claims a 200 with a fabricated ETag and DOES NOT WRITE. The object stays b"A-original".
            return {"ETag": fake_etag}

        with_verify = put_if_precondition(self.bucket, key, b"B-updated", token, client=self.s3,
                                          _lying_put=lying_put)
        self.observations.extend(with_verify.observations)
        without_verify = put_if_precondition(self.bucket, key, b"B-updated", token, client=self.s3,
                                             _lying_put=lying_put, _skip_verify_reread=True)
        self.observations.extend(without_verify.observations)
        stored = self._body_of(key)
        fired = (with_verify.outcome == "VERIFY_FAILED"
                 and without_verify.outcome == "COMMITTED"
                 and stored == b"A-original")  # the lie never actually wrote anything
        return {"mutant": "m4 skip verifying re-read (hung-cp-reports-success)",
                "with_reread": with_verify.outcome, "expected_with_reread": "VERIFY_FAILED (lie caught)",
                "without_reread": without_verify.outcome, "expected_without_reread": "COMMITTED (lie slips)",
                "object_never_changed": stored == b"A-original", "FIRED": fired}

    def run(self) -> dict:
        p3 = [self.p3a_fresh_token_commit(), self.p3b_stale_token_rejected(),
              self.p3c_expired_window_no_call(), self.p3d_first_mint_once()]
        p4 = [self.m1_conditional_header_load_bearing(), self.m2_null_window_refused(),
              self.m3_wrong_object_digest_refused(), self.m4_skip_verify_reread()]
        return {"p3": p3, "p4": p4}


def _validate_observations(observations: list[dict]) -> dict:
    import pathlib

    import jsonschema

    schema_path = (pathlib.Path(__file__).resolve().parent.parent.parent.parent.parent
                   / "tier1_exec" / "4.0.0_SA_CRO~A" / "deliverables"
                   / "NFRA_EPISTEMY.C1-ENVELOPE" / "schemas" / "observation_record.schema.json")
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    errors = []
    for i, obs in enumerate(observations):
        try:
            jsonschema.validate(obs, schema)
        except jsonschema.ValidationError as exc:
            errors.append(f"obs[{i}]: {exc.message}")
    return {"c1_schema": str(schema_path), "count": len(observations),
            "conformant": len(observations) - len(errors), "errors": errors}


def _verdict_shape(result: dict) -> dict:
    """The stable verdict skeleton -- booleans only, no keys/etags/timestamps -- so two runs are
    comparable for determinism (P4) even though every uuid key and ETag differs per run."""
    return {
        "p3": [{"scenario": s["scenario"], "pass": s["pass"]} for s in result["p3"]],
        "p4": [{"mutant": m["mutant"], "FIRED": m["FIRED"]} for m in result["p4"]],
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--bucket", required=True, help="the bounded class's bucket (a firm code bucket, e.g. opal-data-bd)")
    ap.add_argument("--prefix", default=SCRATCH_PREFIX)
    args = ap.parse_args()

    # Two independent runs for determinism (P4). Each mints + cleans its own scratch objects.
    runs = []
    verdict_shapes = []
    all_obs_report = None
    for n in (1, 2):
        h = Harness(args.bucket, args.prefix)
        try:
            result = h.run()
        finally:
            cleanup = h.cleanup()
        obs_report = _validate_observations(h.observations)
        result["cleanup"] = cleanup
        result["observations_report"] = obs_report
        runs.append(result)
        verdict_shapes.append(_verdict_shape(result))
        if n == 1:
            all_obs_report = obs_report

    determinism_stable = verdict_shapes[0] == verdict_shapes[1]
    r0 = runs[0]

    print("=== P3 REAL-PLANE EXERCISE (run 1) ===")
    for s in r0["p3"]:
        print(f"  {'OK' if s['pass'] else 'FAIL'}: {s['scenario']} -> {s.get('outcome', '?')} "
              f"[{s['denominator']}]")
    print("=== P4 MUTANT BATTERY (run 1) -- each mutant must FIRE ===")
    for m in r0["p4"]:
        print(f"  {'FIRED' if m['FIRED'] else 'MISSED'}: {m['mutant']}")
    # m4 firing shown explicitly on its own line (CTO arch condition 2: do not let m4 be quiet).
    m4 = next(m for m in r0["p4"] if m["mutant"].startswith("m4"))
    print(f"  m4 detail: with_reread={m4['with_reread']} (expect VERIFY_FAILED) | "
          f"without_reread={m4['without_reread']} (expect COMMITTED) | "
          f"object_never_changed={m4['object_never_changed']} -> FIRED={m4['FIRED']}")
    print(f"=== CLEANUP: deleted={len(r0['cleanup']['deleted'])} failed={r0['cleanup']['failed']} ===")
    print(f"=== C1 OBSERVATION ENVELOPE: {all_obs_report['conformant']}/{all_obs_report['count']} "
          f"conformant; errors={all_obs_report['errors']} ===")
    print(f"=== DETERMINISM (2 runs, verdict shape): {'STABLE' if determinism_stable else 'UNSTABLE'} ===")

    p3_pass = all(s["pass"] for s in r0["p3"])
    p4_fired = all(m["FIRED"] for m in r0["p4"])
    obs_ok = all_obs_report["conformant"] == all_obs_report["count"] and all_obs_report["count"] > 0
    cleanup_ok = not r0["cleanup"]["failed"]
    overall = p3_pass and p4_fired and obs_ok and cleanup_ok and determinism_stable

    print("\n" + json.dumps({
        "P3_all_pass": p3_pass, "P4_all_fired": p4_fired, "observations_conformant": obs_ok,
        "cleanup_clean": cleanup_ok, "determinism_stable": determinism_stable, "OVERALL": overall,
    }, indent=2))
    return 0 if overall else 1


if __name__ == "__main__":
    sys.exit(main())
