"""Emit the TO-CARD-R-W4-COX v3.1 substrate cards, authored from LIVE reads of each subject.

AC2 forbids a migrator. The 7 subjects already carry 7 MEASURED cells each in
cells.0.7.0_AE_CloudOps~X.json @a5fffa2bb7, authored by this same seat -- and that carrier is a
POINTER TO WHERE TO LOOK, never a source of answers. Every value below is re-measured here; where
a carrier cell and a live read disagree, the live read wins and the disagreement is carried.

⛔ THE CARRIER IS NOT A CONTROL ON ITSELF. It was written by this lane, so agreeing with it is
agreeing with myself -- REPETITION, not corroboration. The independent instruments here are the
live S3 plane and the writer's source at its pin.

⛔ THE RETRIEVAL TRAP, AS MEASURED -- NOT AS INHERITED. A failed retrieval RETURNS A VALUE: a true
absence yields KeyCount=0 at rc=0. But the carrier's cell 7 claimed a wrong bucket, a wrong region
and a missing s3:ListBucket ALL yield that same zero, and zero_class_probes() below FALSIFIED two
of those three: a wrong bucket ERRORS (rc=255, NoSuchBucket) and a wrong region returns the CORRECT
count (rc=0). AMONG THE THREE EXERCISED CLASSES, only a true absence produces a zero -- the
scope qualifier is load-bearing, because the FOURTH class (a missing s3:ListBucket) was never
exercised and may also return a zero. That unexercised class is the sole ground on which the card
reads distinguishable_from_true_negative = no, at basis `inferred`. An unscoped "only a true
absence produces a zero" would contradict that same row.

⛔ THIS PARAGRAPH ONCE ASSERTED THE FALSIFIED VERSION AND CALLED IT "RE-CONFIRMED LIVE", and it
survived three STOPs on this card because every repair went to the emitted JSON while the source
preamble kept the disproved claim as present truth. It was caught by 3.0.0_SA_CVO~X, not by my own
builder census, because that census grepped a LITERAL PHRASE lifted from the verdict text
("emitted identically by absence") which does not match this file's wording ("emitted identically
for a true absence"). A literal-phrase census FALSE-ZEROS on a semantic variant. The residue check
is now semantic and runs over BOTH carriers.
"""

from __future__ import annotations

import collections
import json
import os
import subprocess
import sys
from datetime import datetime, timezone

D = os.path.dirname(os.path.abspath(__file__))
LANE = "0.7.0_AE_CloudOps~X"
CARRIER = "org/tier2_senior/0.7.0_AE_CloudOps/deliverables/cells.0.7.0_AE_CloudOps~X.json"
CARRIER_PIN = "a5fffa2bb7"
# CreateProcess will not spawn the MSYS script, and a relative forward-slash path fails
# too -- resolve the Windows entry point ABSOLUTELY. Repo root is this file + 5 parents.
_ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     *([os.pardir] * 5)))
AWS = os.path.normpath(os.path.join(_ROOT, ".tools",
                                    "aws.cmd" if os.name == "nt" else "aws"))

# group -> subject, read EXACTLY from the backticked cell of TO-W4-REMOTE's subject table, never
# by substring: evidence prose cross-references other subjects (cse_store.py cites
# _branch_head.main.json as its marker oracle), and a first-substring-wins matcher mapped 5 groups
# onto _branch_head and 4 onto code_heat_snap before this was caught.
GROUPS = {"code_heat_snap": "W4-wvft", "cse": "W4-bqrk", "cse_test_24458e6c": "W4-kzhx",
          "cse_test_bb57a916": "W4-dlqq", "fedobs_coevolution_snap": "W4-kyjs",
          "fedobs_coverage_snap": "W4-siwi", "ms_heat_snap": "W4-cjtn"}

BUCKET = "opal-313476888478-globgrph"
HOMES = {"cse": "warehouse/globgrph/cse_b557721f-8b81-4ec2-9289-fe5f44c3f272/"}
BOGUS = "warehouse/globgrph/cse_00000000-0000-0000-0000-000000000000/"


def _aws(*args):
    r = subprocess.run([AWS] + list(args), capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError("aws failed rc=%d: %s" % (r.returncode, r.stderr.strip()[:300]))
    return r.stdout.strip()


def probe(*args):
    """Run a read-only call and RETURN (rc, first line), never raise. _aws() raises on rc!=0,
    which would make the error-producing classes unmeasurable by the very helper used to measure
    them -- the instrument would refuse exactly the cases under test."""
    r = subprocess.run([AWS] + list(args), capture_output=True, text=True)
    out = (r.stdout.strip() or r.stderr.strip()).splitlines()
    return r.returncode, (out[0][:150] if out else "")


def zero_class_probes(home):
    """Which failure classes actually PRODUCE a KeyCount of 0? Each a SEPARATE invocation."""
    base = ["s3api", "list-objects-v2", "--max-keys", "1", "--query", "KeyCount",
            "--output", "text"]
    return {
        "true_absence": probe(*(base + ["--bucket", BUCKET, "--prefix", BOGUS])),
        "wrong_bucket": probe(*(base + ["--bucket", "opal-no-such-bucket-probe-20260830",
                                        "--prefix", "x/"])),
        "wrong_region": probe(*(base + ["--bucket", BUCKET, "--prefix", home,
                                        "--region", "us-west-1"])),
    }


def key_count(prefix):
    """A POSITIVE is load-bearing; a 0 is not (see the module docstring)."""
    return int(_aws("s3api", "list-objects-v2", "--bucket", BUCKET, "--prefix", prefix,
                    "--max-keys", "1", "--query", "KeyCount", "--output", "text") or 0)


def object_census(prefix):
    """Auto-paginated and counted CLIENT-SIDE. --query length() over a paginated list-* returns
    the PAGE count, not the population, and --no-paginate is the hazard, not the fix."""
    out = _aws("s3api", "list-objects-v2", "--bucket", BUCKET, "--prefix", prefix,
               "--query", "Contents[].[LastModified,Size]", "--output", "text")
    rows = [ln.split("\t") for ln in out.splitlines() if ln.strip()]
    days = collections.Counter(r[0][:10] for r in rows)
    return {"objects": len(rows), "bytes": sum(int(r[1]) for r in rows),
            "distinct_write_days": len(days), "newest_utc": max(r[0] for r in rows),
            "per_day_tail": dict(sorted(days.items())[-12:])}


def git_pin(path):
    return subprocess.run(["git", "log", "-1", "--format=%H", "--", path],
                          capture_output=True, text=True).stdout.strip()


def carrier_cells(group):
    raw = subprocess.run(["git", "show", "%s:%s" % (CARRIER_PIN, CARRIER)],
                         capture_output=True).stdout
    return [c for c in json.loads(raw)["cells"] if c["cell_id"].startswith(group + "-")]


def card_cse():
    home = HOMES["cse"]
    kc = key_count(home)          # the bogus-prefix call now lives in zero_class_probes(),
                                  # which runs each class as its own invocation
    cen = object_census(home)
    zc = zero_class_probes(home)
    writer = "infra/aws/globgrph/cse_store.py"
    wpin = git_pin(writer)
    cells = carrier_cells(GROUPS["cse"])
    per_day = cen["per_day_tail"]
    norm = collections.Counter(per_day.values()).most_common(1)[0][0]
    short = sorted(d for d, n in per_day.items() if n < norm)

    return {
        "schema_version": 3.1,
        "subject": {
            "id": "cse",
            "kind": "store",
            "declared_domain": (
                "The production CSE (Change/Signal Event) store: an Apache Iceberg table under "
                "the globgrph Nessie catalog, holding validated CSE rows appended by the nightly "
                "producers. The subject is THE STORE, not its writer -- cse_store.py is carded "
                "separately at D11_CARDS_W3 (PATH_A_append / PATH_B_drop), and conflating the "
                "two is the grain error this domain line exists to prevent. "
                "QUALIFIES THE CELLS CARRIER (AC4): %s @%s, cells %s -- this card is the v3.1 "
                "reading of those 7 cells and the carrier itself is NOT edited."
                % (CARRIER, CARRIER_PIN, " ".join(c["cell_id"] for c in cells))),
        },
        "as_of": {
            "carded_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "commit_ish": subprocess.run(["git", "rev-parse", "HEAD"],
                                         capture_output=True, text=True).stdout.strip(),
            "graph_vintage": "S3 plane read live at card time; no graph consulted",
        },
        "process": {
            "methodology": {
                "how": ("pyiceberg table.append(pa_table) -- ONE Nessie commit per batch, "
                        "append-only. Validation is FAIL-CLOSED and precedes the write: "
                        "validate_batch() raises CSEValidationError if ANY row in the batch is "
                        "rejected, so a batch with one invalid CSE is never partially written. A "
                        "genuine ref-CAS 409 (concurrent writer) is retried with backoff and "
                        "raises LOUD on exhaustion rather than freezing silently."),
                "determinism": "deterministic",
                "composes": [
                    {"id": "cse_producers_nightly.py",
                     "note": "supplies CSE rows via append_cses() at :164, :209 and :269"},
                    {"id": "cse_emit_graphhead.py",
                     "note": "supplies CSE rows via append_cses() at :218"}],
                "invents": [
                    {"id": "ingested_at_ms",
                     "note": "stamped from _now_ms() at write time, so the same logical batch "
                             "appended twice yields rows that differ in this column. That is "
                             "OUTPUT VARIATION, not model inference, and it does NOT move the "
                             "determinism axis -- recorded here because invents is the field "
                             "that asks it"}],
                "materializer_standing": "canonical",
                "basis": "measured",
                "evidence": ("Read at source @%s: append_cses() at %s:357, table.append(pa_table) "
                             "at :386 inside the retry loop, table re-loaded each attempt for "
                             "post-conflict metadata; validation call, rejection and fail-closed "
                             "raise at :370-376; the empty-batch early return printing "
                             "CSE_APPEND_NOOP at :366-368. "
                             "⛔ determinism=deterministic, not hybrid: the enum's own conditional "
                             "requires inference_detail{model, invocations_per_run, "
                             "failure_is_loud} for hybrid/inferential, so the axis is MODEL "
                             "INFERENCE, not output reproducibility. No model is invoked here. "
                             "The wall-clock ingested_at_ms is carried in invents, which is the "
                             "field that actually asks the question."
                             % (wpin[:10], writer)),
                "owner": LANE,
            },
            "cadence": {
                "declared_rhythm": "nightly, via its callers -- the store has NO trigger of its own",
                "actual_trigger": ("invoked as a LIBRARY: cse_producers_nightly.py:164/:209/:269 "
                                   "and cse_emit_graphhead.py:218 call append_cses()"),
                "live_matches_declared": "yes",
                "live_instance_age": ("newest object %s; %d distinct write-days across the "
                                      "store's life" % (cen["newest_utc"], cen["distinct_write_days"])),
                "basis": "measured",
                "evidence": (
                    "⛔ CADENCE IS A CLAIM ABOUT AN EVENT CLASS AND ONE TIMESTAMP CANNOT CARRY IT, "
                    "so the write-day distribution was measured rather than the latest write: %d "
                    "distinct write-days, %d objects total. Over the last 12 write-days the "
                    "modal count is %d objects/day, and %s sit at less than that (%s). "
                    "append_cses() returns EARLY on an empty batch (CSE_APPEND_NOOP at :366) "
                    "writing nothing at all, so a short day is consistent with a producer batch "
                    "being empty -- NOT with a failed write, which raises. Which of the callers "
                    "was short on those days is NOT measured here."
                    % (cen["distinct_write_days"], cen["objects"], norm,
                       "2 days" if len(short) == 2 else "%d day(s)" % len(short),
                       ", ".join(short) or "none")),
                "owner": LANE,
            },
        },
        "artifact": {
            "persistence": {
                "persisted": True,
                "authority_role": "source",
                "mutation_policy": "append_only",
                "form": ("an Iceberg table: data files plus a metadata/ tree of "
                         "*.metadata.json, manifest (-m0.avro) and snapshot (snap-*.avro) objects"),
                "basis": "measured",
                "evidence": ("KeyCount at the declared home = %d (a POSITIVE, which a wrong "
                             "bucket or a missing s3:ListBucket cannot produce). %d objects / "
                             "%d bytes counted client-side over an auto-paginated listing."
                             % (kc, cen["objects"], cen["bytes"])),
                "owner": LANE,
            },
            "location": {
                "home": "s3://%s/%s" % (BUCKET, home),
                "projection_of": [],
                "co_resident_stores": [
                    {"id": "s3://%s/warehouse/globgrph/" % BUCKET,
                     "note": "the sibling globgrph warehouse tables share this bucket and "
                             "prefix root; overlap of CONTENT was not measured, only co-residence"}],
                "basis": "measured",
                "evidence": ("the s3:// URI is an EXACT IDENTITY a consumer can equality-join, "
                             "not a description; resolved live this session at KeyCount=%d." % kc),
                "owner": LANE,
            },
        },
        "trust": {
            "coverage": {
                "universe": ("the objects under the store's own S3 home -- NOT the CSE event "
                             "population, which this card does not measure"),
                "denominator": "%d of %d objects at the declared home" % (cen["objects"], cen["objects"]),
                "explicitly_out": [
                    "⛔ NO COMPLETENESS OF THE CSE EVENT POPULATION IS ASSERTED. That every "
                    "producer that should have appended did append is a DIFFERENT question with "
                    "a different denominator, and nothing here measures it.",
                    "the row-level contents of the Iceberg data files (not read; only the object "
                    "plane was measured)",
                    "which caller was short on the %s short day(s)" % (len(short) or 0),
                ],
                "basis": "measured",
                "evidence": ("aws s3api list-objects-v2 auto-paginated, rows counted client-side: "
                             "%d objects, %d bytes, newest %s."
                             % (cen["objects"], cen["bytes"], cen["newest_utc"])),
                "owner": LANE,
            },
            "key": {
                "identity_space": "S3 (bucket, key) for the artifact plane; (namespace, table) "
                                  "in the Nessie catalog for the logical table",
                "key_expression": "bucket + key, exact string match",
                "key_is_stable": "stable",
                "crosses_spaces": True,
                "declared_mapping": ("the table is addressed logically as (NAMESPACE, CSE_TABLE) "
                                     "through the catalog and physically by the s3:// home; the "
                                     "two spaces are joined by the catalog's own metadata "
                                     "pointer, which this card did not traverse"),
                "basis": "held",
                "evidence": ("⛔ basis is the FLOOR: the S3 identity is MEASURED (listed live), "
                             "but that the catalog's (namespace, table) resolves to THIS prefix "
                             "was read from the manifest's home field and NOT verified against "
                             "the catalog. One limb measured, one limb read -> held."),
                "owner": LANE,
            },
            "failure_mode": {
                "returns_on_failure": ("A true absence returns KeyCount=0 at rc=0 -- a failed "
                                       "retrieval returns a VALUE, not an error. MEASURED: a "
                                       "wrong BUCKET does NOT do this (rc=255, NoSuchBucket) "
                                       "and a wrong REGION does NOT either (rc=0, the CORRECT "
                                       "KeyCount). A missing s3:ListBucket was NOT exercised "
                                       "and is the one class that may still return an "
                                       "ambiguous result."),
                "distinguishable_from_true_negative": "no",
                "basis": "inferred",
                "basis_by_field": {
                    "returns_on_failure": "measured",
                    "distinguishable_from_true_negative": "inferred"},
                "evidence": (
                    "THREE READ-ONLY PROBES, each a SEPARATE invocation, rc read UNPIPED: "
                    "true absence (real bucket, bogus prefix %s) -> rc=%d %r; wrong bucket "
                    "(nonexistent) -> rc=%d %r; wrong region (real bucket, --region us-west-1) "
                    "-> rc=%d %r. Target existence, separately: KeyCount=%d. "
                    "⛔ AMONG THE THREE EXERCISED CLASSES, ONLY A TRUE ABSENCE PRODUCES A "
                    "ZERO -- a wrong bucket ERRORS and a wrong region returns the CORRECT "
                    "count. The scope is load-bearing: the FOURTH class was never exercised "
                    "and may also return a zero, so an unscoped 'only' would contradict this "
                    "row's own returns_on_failure. The earlier claim on this row -- that "
                    "all four classes emit an identical zero -- came from the CARRIER'S CELL 7, "
                    "written by this same seat in wave 3, and was repeated here as "
                    "'re-confirmed' when what had actually been exercised was the target's "
                    "EXISTENCE. Different claims about different objects. distinguishable "
                    "stays `no`, but ONLY on the one class never exercised: a missing "
                    "s3:ListBucket, unprobeable from this principal without altering a "
                    "permission. ⛔ BASIS IS THE FLOOR, SO THIS ROW IS `inferred`: "
                    "returns_on_failure is measured, but the `no` is a conservative judgement "
                    "resting on an UNEXERCISED class, and a row may not read measured while a "
                    "sub-claim is weaker."
                    % (BOGUS.rsplit("/", 2)[-2],
                       zc["true_absence"][0], zc["true_absence"][1],
                       zc["wrong_bucket"][0], zc["wrong_bucket"][1],
                       zc["wrong_region"][0], zc["wrong_region"][1], kc)),
                "owner": LANE,
            },
        },
        "verdict": {
            "standing": "QUALIFIED",
            "why": ("LOAD-BEARING: the production CSE store, authority_role=source, appended by "
                    "the nightly producers and read downstream. QUALIFIED on the limbs "
                    "ENUMERATED below and deliberately NOT counted, so that adding a limb "
                    "cannot desynchronise a cardinal: "
                    "the catalog-to-prefix binding is HELD rather than measured (trust.key); "
                    "coverage is over the OBJECT plane only, asserting nothing about whether the "
                    "CSE event population is complete; and the failure mode is NOT "
                    "distinguishable from a true negative -- MEASURED OVER THE THREE "
                    "EXERCISED CLASSES: of those, only a true absence returns a zero (a wrong "
                    "bucket ERRORS at rc=255, a wrong region returns the CORRECT count). The "
                    "fourth class was not exercised and may also return a zero, so the `no` "
                    "rests on that one class never "
                    "exercised, a revoked s3:ListBucket, and that row carries basis "
                    "`inferred` rather than measured. The %s short write-day(s) (%s) are "
                    "recorded as an observation about the as-built rhythm, not a defect: an "
                    "empty batch writes nothing by design and a failed write raises."
                    % (len(short) or "no", ", ".join(short) or "n/a")),
            "blocking_defects": None,
        },
        "forward_disposition": {
            "standing": "undecided",
            "set_by": None,
            "basis": "absent",
            "evidence": "NOT SET BY THE CARDING LANE -- the store owner's call at the class close.",
            "decided_utc": None,
        },
        "carded_by": LANE,
    }


BUILDERS = {"cse": card_cse}


def main():
    want = sys.argv[1] if len(sys.argv) > 1 else "all"
    todo = list(BUILDERS) if want == "all" else [want]
    for name in todo:
        if name not in BUILDERS:
            raise SystemExit("no builder for %r (have: %s)" % (name, ", ".join(BUILDERS)))
        doc = BUILDERS[name]()
        p = os.path.join(D, "%s.v3.1.json" % name)
        with open(p, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(doc, fh, indent=1)
        print("WROTE %s" % p)
        print("  home        %s" % doc["artifact"]["location"]["home"])
        print("  coverage    %s" % doc["trust"]["coverage"]["denominator"])
        print("  cadence     %s" % doc["process"]["cadence"]["live_instance_age"])
        print("  carded_by   %s" % doc["carded_by"])


if __name__ == "__main__":
    main()
