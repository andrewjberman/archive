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
import re
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

THREE_PLANE_NOTE = (
    "TRIGGER PLANES SWEPT, AND WHY THE FIRST TWO WERE NOT ENOUGH. (1) EVENTBRIDGE: 140 rules "
    "enumerated, none names code_heat -- but that plane's control FAILED, since `cse` writes "
    "daily and matches no rule either (its producer is an ECS task), so that zero was never "
    "load-bearing. (2) TERRAFORM SCHEDULER RESOURCES: glue_code_heat.tf declares only "
    "aws_glue_catalog_database/_table/_partition; that plane's control fires, since the same "
    "corpus carries cse_producer's ECS declaration and comp_learns_producer_nightly at "
    "cron(0 4 * * ? *). (3) THE HOST-BOUND PLANE, which neither of the first two can see. "
    "\u26d4 AN EARLIER VERSION OF THIS CARD CALLED THE TRIGGER A MEASURED ABSENCE ON PLANES 1-2 "
    "ALONE. That was wrong and 4.0.0_SA_CRO~X caught it: a positive control certifies ITS OWN "
    "SUBJECT, and the terraform control only established that CLOUD SCHEDULES are visible in "
    "that corpus -- it cannot certify absence from a host-bound plane it does not cover. Worse, "
    "item2a.tf was already IN this seat's own comp-find output as a content hit; the filename "
    "match (glue_code_heat.tf) was read and the 26 SURFACED hits were not. An early stop and a "
    "true absence read identically.")


BUCKET = "opal-313476888478-globgrph"
HOMES = {"cse": "warehouse/globgrph/cse_b557721f-8b81-4ec2-9289-fe5f44c3f272/",
         "code_heat_snap": "warehouse/globgrph/code_heat_snap_8b0bca7a-9078-4b8e-8868-ef04062d9952/",
         # ⛔ COPIED FROM THE CARRIER, NEVER TYPED FROM A DISPLAY. The first attempt at
         # this one reconstructed the UUID tail from a print truncated at 110 chars, got
         # the LAST CHARACTER wrong (...2295 for ...2299), and KeyCount returned 0 --
         # which reads exactly like an absent table. A wrong prefix and a true absence
         # are the same zero.
         "fedobs_coevolution_snap": "warehouse/globgrph/fedobs_coevolution_snap_499558ba-0181-42ab-a008-93a518692299/",
         "fedobs_coverage_snap": "warehouse/globgrph/fedobs_coverage_snap_a9637eab-f8d2-4421-847c-4a2ca27cdc86/",
         # COPIED from the cells carrier @a5fffa2bb7 cell -4, never typed: these
         # two share the table name `cse_test` and differ ONLY in the uuid, so a
         # transcription slip here lands on a REAL populated table, not on a zero.
         "cse_test_24458e6c": "warehouse/globgrph/cse_test_24458e6c-667c-4e85-ba44-33751795e182/",
         "cse_test_bb57a916": "warehouse/globgrph/cse_test_bb57a916-76de-454d-a71e-932dc173620e/"}
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


def refuse_prose_basis_mismatch(doc):
    """Any PROSE assertion about a row's basis must equal that row's STRUCTURED basis.

    The structured repair and the sentence explaining it are two carriers of one claim. Nothing
    in the schema or the checker compares them, so a row can carry basis='absent' while its own
    evidence says it floors to 'held' -- which is exactly what shipped at @fd6b4ccb3f and what
    4.0.0_SA_CRO~X caught. An all-row STRUCTURED audit cannot see this: it compares scalars to
    maps and never reads the prose.
    """
    pat = re.compile(r"(?:floors? to|row is|row floors to|basis is)\s*`?"
                     r"(measured|held|inferred|absent)`?", re.I)
    bad = []
    for sec in ("process", "artifact", "trust"):
        for row, body in doc.get(sec, {}).items():
            if not isinstance(body, dict) or "basis" not in body:
                continue
            for claimed in pat.findall(body.get("evidence", "") or ""):
                if claimed.lower() != body["basis"]:
                    bad.append("%s.%s: prose says %r, structured basis is %r"
                               % (sec, row, claimed, body["basis"]))
    # the verdict speaks ABOUT rows, so it is checked against the row it names
    why = doc.get("verdict", {}).get("why", "") or ""
    for m in re.finditer(r"cadence row is\s*`?(measured|held|inferred|absent)`?", why, re.I):
        actual = doc["process"]["cadence"]["basis"]
        if m.group(1).lower() != actual:
            bad.append("verdict.why: says cadence row is %r, structured basis is %r"
                       % (m.group(1), actual))
    if bad:
        raise ValueError("PROSE/STRUCTURE BASIS MISMATCH -- a corrected field whose sentence was "
                         "not corrected:\n  " + "\n  ".join(bad))
    return True


LIFETIME_CLAIM = re.compile(
    r"(never again|never touched again|never written again|ha(?:s|ve) not run again"
    r"|then nothing\b|written once\b|written ONCE\b|writes ever\b)", re.I)
LIFETIME_SCOPE = re.compile(
    r"(surviving set|SURVIVING|latest surviving|snapshot HISTORY|UNMEASURED)", re.I)


def refuse_unscoped_lifetime_claim(doc):
    """A sentence asserting the subject was never written again is a claim about ALL TIME, and the
    S3 object plane cannot carry it. Every carrier of that claim must scope itself.

    THE THIRD ARM ON THIS FACE AND THE FIRST THAT COMPARES PROSE TO PROSE. Its two siblings --
    refuse_prose_basis_mismatch() and refuse_prose_enum_mismatch() -- both compare a SENTENCE to a
    STRUCTURED FIELD. This defect has no structured field in it at all: five sentences, one of them
    correctly scoped and four asserting the unscoped claim, disagreeing only with each other. Both
    existing arms are structurally blind to it.

    MEASURED, and it is the reason this is an arm rather than a note (4.0.0_SA_CRO~X STOP on card 6
    @19f0a0d69f, 2026-08-30): the object plane proves N surviving append commit uuids, N surviving
    snapshots and no later SURVIVING object than some timestamp. It does NOT prove the total
    lifetime write count. Card 6 scoped `/process/cadence/evidence` correctly and left
    `/subject/declared_domain`, `/process/methodology/evidence`,
    `/process/cadence/actual_trigger` and `/verdict/why` asserting the lifetime claim as fact --
    and CARD 5, ALREADY JOINTLY CLOSED AND ON ORIGIN, CARRIES THE SAME FOUR.

    ⛔ THE ROOT IS NOT CARELESSNESS ABOUT SENTENCES, IT IS FIXING THE CITED CARRIER INSTEAD OF
    CENSUSING THE CLAIM. An earlier STOP required the write-once evidence be scoped; I scoped the
    carrier that was named. At the moment of repair, a fix applied at the cited site and a fix
    applied to the claim are indistinguishable -- which is why this has to be mechanical.

    ⛔ THE PATTERN IS DELIBERATELY NARROW, because my own first census of this used `and never\b`
    and returned three FALSE POSITIVES on the same cards: "ENSURE-ONLY and NEVER overwrites"
    (a property of the writer), "NEVER retyped from a display" (provenance of a home string) and
    "NEVER --query length()" (an instrument prohibition). All three are the word `never` about
    something that is not the subject's write history. An arm that fires on those manufactures
    defects in correct sentences, so the tokens here name the CLAIM, not the word.
    """
    bad = []

    def walk(node, path):
        if isinstance(node, dict):
            for k, v in node.items():
                walk(v, path + "/" + k)
        elif isinstance(node, list):
            for i, v in enumerate(node):
                walk(v, path + "/%d" % i)
        elif isinstance(node, str):
            for m in LIFETIME_CLAIM.finditer(node):
                # ⛔ THE SCOPE QUALIFIER MUST TRAVEL WITH THE CLAIM, NOT MERELY SHARE ITS FIELD.
                # A whole-field test FALSE-NEGATIVES: card 6's /verdict/why carries `UNMEASURED`
                # about whether a CONSUMER reads the table, 300 characters from an unscoped
                # `never touched again` -- a scope word about a DIFFERENT claim silently
                # certified the lifetime one. 4.0.0_SA_CRO~X named that exact carrier and the
                # whole-field version of this arm did not fire on it.
                near = node[max(0, m.start() - 250):m.end() + 250]
                if not LIFETIME_SCOPE.search(near):
                    bad.append("%s: %r asserts a LIFETIME write history the object plane cannot "
                               "carry, with no scoping qualifier in the same field"
                               % (path, m.group(1)))

    walk(doc, "")
    if bad:
        raise ValueError(
            "UNSCOPED LIFETIME CLAIM -- the surviving set does not prove the lifetime:\n  "
            + "\n  ".join(bad)
            + "\n  FIX: scope each to the SURVIVING set / latest SURVIVING object, or obtain "
              "snapshot-history or catalog evidence for an exact lifetime claim.")
    return True


BASIS_VOCAB = ("measured", "held", "inferred", "absent")


def refuse_prose_enum_mismatch(doc):
    """Any prose that NAMES a structured key in its own section and ASSERTS a value for it must
    agree with that field.

    The sibling of refuse_prose_basis_mismatch(), and it exists because that guard could not see
    the defect it was written for. That one sweeps BASIS-shaped phrases; a sentence asserting an
    ENUM VALUE is a different class and sat outside its corpus, so a pre-presentation scan
    deliberately made BROADER THAN THE SHIPPED GUARD still returned a clean, confident zero --
    broader within one class is a wider net over the wrong pond. A GUARD SHAPED TO THE LAST
    DEFECT CLASS CANNOT SEE THE NEXT ONE.

    Measured instance (card 5 @4a5e165fbf, found by 1.0.0_SA_CTO~X, independently reproduced and
    STOPped by 4.0.0_SA_CRO~X): mutation_policy was repaired at the builder from an INVENTED enum
    value to `append_only`, and the sentence explaining the field kept asserting the retracted
    value. A reader learns one value; a consumer rejecting on the field sees the other -- which
    defeats the point of a value carrying its claim in a field a consumer can reject on.

    ⛔ THE SENTENCE `<key>` is `<token>` IS AMBIGUOUS AND THE ARM MUST DISAMBIGUATE, NOT GUESS.
    When the token is basis vocabulary AND the key carries a basis_by_field entry, the sentence is
    a claim about that field's BASIS and is checked against basis_by_field -- not against the
    field's value. The first version of this arm lacked that branch and FIRED ON A CLOSED,
    CERTIFIED CARD (code_heat_snap: prose "live_matches_declared is `absent`" about the basis,
    while the VALUE is `unmeasured`). That card is correct and says both things correctly. An arm
    that cannot tell a basis claim from a value claim manufactures a defect in certified work,
    which costs a certifier a round and is worse than the hole it was closing.
    """
    pat = re.compile(r"`?([a-z_]{4,})`?\s+is\s+`([^`]{1,40})`")
    bad = []
    for sec in ("process", "artifact", "trust"):
        rows = doc.get(sec, {})
        declared, bases = {}, {}
        for row, body in rows.items():
            if not isinstance(body, dict):
                continue
            for k, v in body.items():
                if isinstance(v, (str, bool, int)) and k not in ("evidence", "owner"):
                    declared[k] = v
            for k, v in (body.get("basis_by_field") or {}).items():
                bases[k] = v
        for row, body in rows.items():
            if not isinstance(body, dict):
                continue
            for m in pat.finditer(body.get("evidence", "") or ""):
                key, claimed = m.group(1), m.group(2)
                if key not in declared:
                    continue
                # a basis-vocabulary token about a key that HAS a basis is a BASIS claim, and
                # belongs to refuse_prose_basis_mismatch()'s domain, not this one
                if claimed.lower() in BASIS_VOCAB and key in bases:
                    if bases[key] != claimed.lower():
                        bad.append("%s.%s: prose says %s basis is %r, basis_by_field says %r"
                                   % (sec, row, key, claimed, bases[key]))
                    continue
                actual = declared[key]
                if isinstance(actual, bool):
                    actual = "true" if actual else "false"
                if str(actual) != claimed:
                    bad.append("%s.%s: prose says %s is %r, structured value is %r"
                               % (sec, row, key, claimed, str(actual)))
    if bad:
        raise ValueError("PROSE/STRUCTURE ENUM MISMATCH -- a repaired field whose sentence still "
                         "asserts the old value:\n  " + "\n  ".join(bad))
    return True


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


def card_code_heat_snap():
    home = HOMES["code_heat_snap"]
    kc = key_count(home)
    cen = object_census(home)
    zc = zero_class_probes(home)
    cells = carrier_cells(GROUPS["code_heat_snap"])
    writer = "infra/aws/globgrph/snap_store.py"
    wpin = git_pin(writer)
    newest = datetime.strptime(cen["newest_utc"][:19], "%Y-%m-%dT%H:%M:%S").replace(
        tzinfo=timezone.utc)
    age = (datetime.now(timezone.utc) - newest).days

    return {
        "schema_version": 3.1,
        "subject": {
            "id": "code_heat_snap",
            "kind": "store",
            "declared_domain": (
                "The code_heat_snap Iceberg table: one registered SURFACE of snap_store.py, "
                "which its own header calls THE ONE WRITER for all siblings. Rows arrive as "
                "staged .jsonl batches under warehouse/snap_ingest/pending/<surface>/ and are "
                "coerced, appended and moved to done/. The subject is THAT TABLE. "
                "QUALIFIES THE CELLS CARRIER (AC4): %s @%s, cells %s -- this card is the v3.1 "
                "reading of those 7 cells; the carrier is NOT edited, and where it and a live "
                "read disagree the live read wins and the disagreement is carried."
                % (CARRIER, CARRIER_PIN, " ".join(c["cell_id"] for c in cells))),
        },
        "as_of": {
            "carded_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "commit_ish": subprocess.run(["git", "rev-parse", "HEAD"],
                                         capture_output=True, text=True).stdout.strip(),
            "graph_vintage": "S3 object plane, S3 staging plane, EventBridge, terraform and the "
                             "host-bound declarations all read live at card time",
        },
        "process": {
            "methodology": {
                "how": ("Iceberg append via snap_store.py append_rows(): staged .jsonl batches "
                        "are read from warehouse/snap_ingest/pending/code_heat_snap/, coerced "
                        "against the surface's typed payload schema, appended in one Nessie "
                        "commit, then MOVED to done/. Fail-closed: a batch with invalid rows is "
                        "rejected LOUD and left in pending/ rather than partially written."),
                "determinism": "deterministic",
                "composes": [
                    {"id": "infra/aws/globgrph/code_heat_emit.py @c934701a67",
                     "note": "PRODUCES the staged batch this table is built from: SNAP_PENDING "
                             "at :241 is warehouse/snap_ingest/pending/code_heat_snap/, "
                             "sibling_rows() at :244 builds rows directly from git, "
                             "stage_sibling() at :261 writes the JSONL key at :265, reachable "
                             "via --emit-sibling / --sibling-only at :281-283. It imports no "
                             "snap_store and calls no append_rows -- that is the INTENDED "
                             "ASYNCHRONOUS stage-then-ingest boundary, not an absent dependency"},
                    {"id": "warehouse/snap_ingest/pending/code_heat_snap/*.jsonl",
                     "note": "the staged batch: the handoff artifact between the producer above "
                             "and the writer below, and the only measured input to this table"},
                    {"id": writer,
                     "note": "the ONE writer for all snap surfaces: append_rows() at :243, "
                             "t.append(table) at :256, ingest loop at :285-315"}],
                "invents": [],
                "materializer_standing": "unknown",
                "basis": "measured",
                "evidence": (
                    "Read at source, line numbers from grep -n AT THE PIN: %s @%s -- SURFACES "
                    "registry at :74-79 with code_heat_snap at :97, append_rows() :243, "
                    "t.append(table) :256, the pending->coerce->append->done loop :285-315. "
                    "\u26d4 A CORRECTION THAT WAS ITSELF WRONG, CARRIED BECAUSE THE ERROR IS "
                    "THE INSTRUCTIVE PART. An earlier version of this card REMOVED "
                    "code_heat_emit.py from `composes`, on the ground that it imports no "
                    "snap_store and calls no append_rows. That test is a CALL-GRAPH criterion "
                    "and `composes` is defined by the schema as WHAT IT REUSES -- so the "
                    "removal destroyed a TRUE dependency, and 3.0.0_SA_CVO~X caught it. The "
                    "producer IS the source of this table's only input, measured at its pin: "
                    "SNAP_PENDING :241 = warehouse/snap_ingest/pending/code_heat_snap/, "
                    "sibling_rows() :244 building rows straight from git, stage_sibling() :261 "
                    "writing the JSONL key at :265, reachable via --emit-sibling / "
                    "--sibling-only :281-283, under a :237 comment naming the batch "
                    "'S3-only, dev-box-writable'. The staged batch actually ingested, "
                    "20260716T150116Z.jsonl, matches that writer's %%Y%%m%%dT%%H%%M%%SZ.jsonl "
                    "format exactly, and the :237 'dev-box-writable' independently corroborates "
                    "the host-bound cadence recorded above. The missing import is the INTENDED "
                    "asynchronous boundary, not an absent edge. The instrument failure was mine "
                    "twice over: the grep that 'proved' the absence was "
                    "`snap_store|append_rows|import`, a pattern that could not have found a "
                    "staging handoff if one existed. WHAT REMAINS TRUE from that pass, and is "
                    "kept: the emitter ALSO writes a separate hive PARQUET surface whose "
                    "declared default output is s3://%s/warehouse/code_heat/ (2 objects, newest "
                    "2026-07-16T03:40:46Z), which is a DIFFERENT store carried in "
                    "co_resident_stores and must not be confused with this Iceberg table."
                    % (writer, wpin[:10], BUCKET)),
                "owner": LANE,
            },
            "cadence": {
                "declared_rhythm": ("DEV-BOX CADENCE -- host-bound, tied to /log. Not a cloud "
                                    "schedule, and not by omission: the container flag was "
                                    "deliberately REVERTED to make it host-bound."),
                "actual_trigger": ("host-bound invocation on a developer box, staged to "
                                   "warehouse/snap_ingest/pending/code_heat_snap/ then ingested; "
                                   "the invocation itself is UNOBSERVABLE from this seat"),
                "live_matches_declared": "unmeasured",
                "live_instance_age": ("%d days: sole write-day %s, newest object %s"
                                      % (age, sorted(cen["per_day_tail"])[0], cen["newest_utc"])),
                "basis": "absent",
                "basis_by_field": {"declared_rhythm": "held",
                                   "actual_trigger": "held",
                                   "live_matches_declared": "absent",
                                   "live_instance_age": "measured"},
                "evidence": (
                    "\u26d4 THE SCALAR IS `absent` BECAUSE BASIS IS THE FLOOR -- the MINIMUM "
                    "over this row's own basis_by_field map, ordered measured > held > "
                    "inferred > absent. Two limbs are `held` (quoted from named "
                    "authorities), one is `measured` (the object age), and "
                    "live_matches_declared is `absent` because NO measurement of the host "
                    "cadence exists -- so the ROW is `absent`, not `held`. An earlier "
                    "version read `held` while carrying an `absent` field: the floor rule "
                    "violated on my own row after a day spent applying it to other "
                    "evidence. 4.0.0_SA_CRO~X caught it. "
                    "DECLARED, quoted from two named authorities rather than derived. "
                    "infra/aws/terraform/globgrph/item2a.tf:402-406: GLOBGRPH_CODEHEAT_ENABLED "
                    "was REVERTED on 2026-07-16 per CTO TO-2 ruling 033933Z, because code_heat "
                    "is git-history-shaped (it shells `git -C` against the workspace and portal "
                    "repos) so the flag gated an import that can NEVER resolve in the Fargate "
                    "derive; 'code_heat now runs on DEV-BOX CADENCE (option a)'. "
                    "infra/system/04_federated.md:21 records the same split as Andrew-ruled: "
                    "cloud producers on nightly EventBridge, host-bound producers (code_heat, "
                    "tool_activity) tied to /log. "
                    "APPLIED IS UNMEASURED AND THE ROW SAYS SO. A dev-box /log cadence is not "
                    "observable from this seat, so live_matches_declared is `unmeasured` and the "
                    "row floors to `absent`. What IS measured is the STAGE-THEN-INGEST plane: "
                    "pending/code_heat_snap/ KeyCount=0 (nothing awaiting ingest); "
                    "done/code_heat_snap/ holds exactly ONE batch, 20260716T150116Z.jsonl, "
                    "12,925,409 bytes, ingested 2026-07-16T15:28:06Z -- the SAME INSTANT as the "
                    "table's sole write, which is the join that ties the two planes together. "
                    "The batch was staged at 15:01:16Z per its own name and ingested 27 minutes "
                    "later. That write-day is also the day the Fargate revert landed. Whether "
                    "the host-bound cadence has since RUN and produced nothing, or has not run "
                    "at all, is NOT distinguishable from here. %s" % THREE_PLANE_NOTE),
                "owner": LANE,
            },
        },
        "artifact": {
            "persistence": {
                "persisted": True,
                "authority_role": "projection",
                "mutation_policy": "append_only",
                "form": "an Iceberg table: data files plus a metadata/ tree",
                "basis": "measured",
                "evidence": (
                    "KeyCount at the declared home = %d (a POSITIVE, which a wrong bucket or a "
                    "missing s3:ListBucket cannot produce); %d objects / %d bytes counted "
                    "client-side over an auto-paginated listing. "
                    "\u26d4 authority_role is `projection`, NOT `source`. The object census "
                    "establishes PERSISTENCE and nothing more -- it cannot establish authority "
                    "for the declared concern, and reading it as if it could is the defect "
                    "3.0.0_SA_CVO~X named. The pinned producer settles it against `source` "
                    "directly: code_heat_emit.py @c934701a67 states 'This parquet is a cheap, "
                    "refreshable DERIVED snapshot (vintage-stamped), NOT a source of truth: git "
                    "remains the write-history', and 'we keep git canonical and never copy git "
                    "into Iceberg'. A table whose upstream declares git canonical is not itself "
                    "authoritative for code heat." % (kc, cen["objects"], cen["bytes"])),
                "owner": LANE,
            },
            "location": {
                "home": "s3://%s/%s" % (BUCKET, home),
                "projection_of": [
                    {"id": "s3://%s/warehouse/snap_ingest/done/code_heat_snap/"
                           "20260716T150116Z.jsonl" % BUCKET,
                     "note": "the single staged batch this table was ingested from; 12,925,409 "
                             "bytes, ingested 2026-07-16T15:28:06Z, matching the table's sole "
                             "write instant"},
                    {"id": "git write-history of the ajb_workspace and portal repos",
                     "note": "declared CANONICAL by the code-heat producer's own header -- 'git "
                             "remains the write-history' -- which is why this store is a "
                             "projection rather than a source. The git plane itself was NOT "
                             "traversed by this card"}],
                "co_resident_stores": [
                    {"id": "s3://%s/warehouse/globgrph/" % BUCKET,
                     "note": "sibling snap surfaces share this bucket and prefix root; CONTENT "
                             "overlap was not measured, only co-residence"},
                    {"id": "s3://%s/warehouse/code_heat/" % BUCKET,
                     "note": "the code_heat PARQUET surface written by code_heat_emit.py -- a "
                             "DIFFERENT store carrying overlapping subject matter, 2 objects, "
                             "newest 2026-07-16T03:40:46Z. Named here because a duplicate-store "
                             "census that missed it would understate the estate"}],
                "basis": "measured",
                "evidence": ("the s3:// URIs are EXACT IDENTITIES a consumer can equality-join; "
                             "the home resolved live at KeyCount=%d, and both the staged batch "
                             "and the parquet prefix were listed live." % kc),
                "owner": LANE,
            },
        },
        "trust": {
            "coverage": {
                "universe": ("objects under the store's own S3 home -- NOT the code-heat row "
                             "population, and NOT the git history it ultimately projects"),
                "denominator": ("%d of %d objects at the declared home"
                                % (cen["objects"], cen["objects"])),
                "explicitly_out": [
                    "NO COMPLETENESS OF THE CODE-HEAT ROW POPULATION IS ASSERTED. Whether the "
                    "single ingested batch covered what it should have is a different question "
                    "with a different denominator, and nothing here measures it.",
                    "the row-level contents of the Iceberg data files (object plane only)",
                    "the git write-history this store projects -- named in projection_of but "
                    "NOT traversed",
                    "whether any consumer still READS this store -- UNMEASURED, and it is the "
                    "question a forward disposition would turn on",
                ],
                "basis": "measured",
                "evidence": ("aws s3api list-objects-v2 auto-paginated, counted client-side: %d "
                             "objects, %d bytes, %d distinct write-day(s), newest %s."
                             % (cen["objects"], cen["bytes"], cen["distinct_write_days"],
                                cen["newest_utc"])),
                "owner": LANE,
            },
            "key": {
                "identity_space": ("S3 (bucket, key) for the artifact plane; (namespace, table) "
                                   "in the Nessie catalog for the logical table"),
                "key_expression": "bucket + key, exact string match",
                "key_is_stable": "stable",
                "crosses_spaces": True,
                "declared_mapping": ("(repo, path) is the declared JOIN KEY from the code-heat "
                                     "row shape into graph_nodes, per the producer's header; "
                                     "that join was not exercised by this card"),
                "basis": "held",
                "evidence": ("basis is the FLOOR: the S3 identity is MEASURED (listed live), "
                             "but that the catalog's (namespace, table) resolves to THIS prefix "
                             "was read from the manifest and NOT verified against the catalog, "
                             "and the (repo, path) join into graph_nodes was not exercised. "
                             "Measured limb plus read limbs -> held."),
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
                    "THREE READ-ONLY PROBES, each a SEPARATE invocation, rc read UNPIPED: true "
                    "absence -> rc=%d %r; wrong bucket -> rc=%d %r; wrong region -> rc=%d %r. "
                    "Target existence, separately: KeyCount=%d. AMONG THE THREE EXERCISED "
                    "CLASSES, only a true absence produces a zero -- the scope is load-bearing, "
                    "because the FOURTH class (a missing s3:ListBucket) was never exercised and "
                    "may also return a zero. This card does NOT repeat the carrier cell-7 claim "
                    "that all four classes emit an identical zero: that claim was FALSIFIED on "
                    "card 1 of this same face, against this same bucket, and is not inherited "
                    "here. distinguishable is `no` on the one unexercised class alone, and the "
                    "row floors to `inferred`. \u26d4 A SECOND RETRIEVAL TRAP WAS HIT AND "
                    "CAUGHT WHILE CARDING THIS SUBJECT: an s3api --query over an EMPTY prefix "
                    "returns the literal string 'None', and a line-count over that output "
                    "reported 1 object where KeyCount says 0. A failed retrieval returns a "
                    "VALUE at the CLIENT layer too, not only at the service layer."
                    % (zc["true_absence"][0], zc["true_absence"][1],
                       zc["wrong_bucket"][0], zc["wrong_bucket"][1],
                       zc["wrong_region"][0], zc["wrong_region"][1], kc)),
                "owner": LANE,
            },
        },
        "verdict": {
            "standing": "QUALIFIED",
            "why": ("The store RESOLVES and holds real bytes, but it is COLD: one write-day, %d "
                    "days ago, from exactly one staged batch. Its trigger is DECLARED and "
                    "host-bound -- dev-box cadence tied to /log, per the CTO revert at "
                    "item2a.tf:402-406 and the Andrew-ruled split at 04_federated.md:21 -- and "
                    "whether that cadence has RUN is UNMEASURABLE from this seat, so the "
                    "cadence row is `absent`. QUALIFIED on the limbs ENUMERATED below and "
                    "deliberately NOT counted, so that adding a limb cannot desynchronise a "
                    "cardinal: authority_role is `projection` and the git plane it projects was "
                    "NOT traversed; the catalog-to-prefix binding and the (repo, path) join are "
                    "HELD rather than measured; coverage spans the OBJECT plane only; the "
                    "failure mode is not distinguishable from a true negative on the one "
                    "unexercised permission class; whether any consumer still reads this store "
                    "is UNMEASURED; and materializer_standing is `unknown`. "
                    "\u26d4 THIS CARD DOES NOT CLASSIFY THE GAP IN EITHER DIRECTION. A "
                    "point-in-time snapshot written once may be exactly what was intended, and "
                    "a declared host-bound cadence can legitimately run rarely -- but this "
                    "card's own evidence says run-versus-no-run is NOT DISTINGUISHABLE from "
                    "this seat, and a row that cannot separate those two cannot call the gap "
                    "unremarkable any more than it can call it alarming. An earlier version "
                    "called it unremarkable, asserting the benign branch of a distinction the "
                    "card had just declared unmeasurable. Naming the gap is the carder's job; "
                    "classifying it needs a measurement of the host plane that does not exist "
                    "here, and deciding it is the owner's." % age),
            "blocking_defects": None,
        },
        "forward_disposition": {
            "standing": "undecided",
            "set_by": None,
            "basis": "absent",
            "evidence": ("NOT SET BY THE CARDING LANE -- the store owner's call at the class "
                         "close. The cadence, consumer-use and duplicate-surface rows are what "
                         "it would turn on."),
            "decided_utc": None,
        },
        "carded_by": LANE,
    }


def card_fedobs_coevolution_snap():
    home = HOMES["fedobs_coevolution_snap"]
    kc = key_count(home)
    cen = object_census(home)
    zc = zero_class_probes(home)
    wrong_prefix = probe("s3api", "list-objects-v2", "--bucket", BUCKET, "--prefix",
                         home[:-2] + "5/", "--max-keys", "1", "--query", "KeyCount",
                         "--output", "text")
    cells = carrier_cells(GROUPS["fedobs_coevolution_snap"])
    writer, producer = "infra/aws/globgrph/snap_store.py", "infra/aws/globgrph/emit_fedobs_snap.py"
    wpin, ppin = git_pin(writer), git_pin(producer)
    newest = datetime.strptime(cen["newest_utc"][:19], "%Y-%m-%dT%H:%M:%S").replace(
        tzinfo=timezone.utc)
    age = (datetime.now(timezone.utc) - newest).days

    return {
        "schema_version": 3.1,
        "subject": {
            "id": "fedobs_coevolution_snap",
            "kind": "store",
            "declared_domain": (
                "The fedobs co-evolution SNAPSHOT store: one registered SURFACE of snap_store.py, "
                "holding (subject_a, subject_b, co_sessions, producers_json, sessions_json) rows "
                "staged as .jsonl and ingested. ⛔ THE SUBJECT IS THIS TABLE AND NOT THE FEDOBS "
                "OBSERVE PLANE -- a nightly ECS producer writes "
                "warehouse/fedobs_signals/observations/fedobs_observations.json, which is a "
                "DIFFERENT artifact that this card does not describe, and conflating them is the "
                "error the cadence row below exists to prevent. "
                "QUALIFIES THE CELLS CARRIER (AC4): %s @%s, cells %s -- the carrier is NOT edited."
                % (CARRIER, CARRIER_PIN, " ".join(c["cell_id"] for c in cells))),
        },
        "as_of": {
            "carded_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "commit_ish": subprocess.run(["git", "rev-parse", "HEAD"],
                                         capture_output=True, text=True).stdout.strip(),
            "graph_vintage": "S3 object plane, S3 staging plane, EventBridge, CloudWatch metrics "
                             "and ECS task logs all read live at card time",
        },
        "process": {
            "methodology": {
                "how": ("Iceberg append via snap_store.py append_rows(): staged .jsonl batches "
                        "are read from warehouse/snap_ingest/pending/fedobs_coevolution_snap/, "
                        "coerced against the surface's typed payload schema at snap_store.py:128, "
                        "appended in one Nessie commit, then MOVED to done/. Fail-closed: a batch "
                        "with invalid rows is rejected LOUD and left in pending/."),
                "determinism": "deterministic",
                "composes": [
                    {"id": producer + " @" + ppin[:10],
                     "note": "declares the coevolution -> fedobs_coevolution_snap mapping at :18 "
                             "and :50; the staged-batch producer for this surface"},
                    {"id": "warehouse/snap_ingest/pending/fedobs_coevolution_snap/*.jsonl",
                     "note": "the handoff artifact; the only measured input to this table"},
                    {"id": writer,
                     "note": "the ONE writer for all snap surfaces; this surface's typed payload "
                             "is declared at :128-135"}],
                "invents": [],
                "materializer_standing": "historical_in_use",
                "basis": "measured",
                "evidence": ("Read at source with line numbers from grep -n AT THE PIN: %s @%s "
                             "surface definition :128-135; %s @%s declares the mapping at :18 and "
                             ":50. materializer_standing is `historical_in_use` rather than "
                             "`canonical`: the surface is real and was written, but the cadence "
                             "row records it as a PARKED single-build vintage, which is not the "
                             "same as current authority."
                             % (writer, wpin[:10], producer, ppin[:10])),
                "owner": LANE,
            },
            "cadence": {
                "declared_rhythm": ("nightly 04:30Z EventBridge, per infra/system/04_federated.md "
                                    "-- an attribution this card MEASURES AND DOES NOT INHERIT"),
                "actual_trigger": ("the stage-then-ingest leg for THIS surface, which last ran "
                                   "2026-07-17; the nightly rule that exists feeds a DIFFERENT "
                                   "artifact"),
                "live_matches_declared": "no",
                "live_instance_age": ("%d days: sole write-day %s, newest object %s"
                                      % (age, sorted(cen["per_day_tail"])[0], cen["newest_utc"])),
                "basis": "measured",
                "basis_by_field": {"declared_rhythm": "measured",
                                   "actual_trigger": "measured",
                                   "live_matches_declared": "measured",
                                   "live_instance_age": "measured"},
                "evidence": (
                    "⛔ THE DECLARED ATTRIBUTION IS MEASURABLY WRONG FOR THIS ARTIFACT, and the "
                    "card records the split rather than repeating the doc. MEASURED: the rule "
                    "opal-globgrph-fedobs-producer-nightly is ENABLED at cron(30 4 * * ? *) "
                    "targeting ECS cluster opal-globgrph; CloudWatch AWS/Events Invocations = 1.0 "
                    "on each of the last 8 days; its newest task log stream is "
                    "2026-08-30T04:31:10Z and that run SUCCEEDS, emitting 'OK: SIGNAL "
                    "coevolution rows=31852' and 'OK: FEDOBS_OBSERVE_COMPLETE'. But it writes "
                    "warehouse/fedobs_signals/observations/fedobs_observations.json (written "
                    "today, 46,856,449 bytes) and mentions 'snap' ZERO times. THIS table's own "
                    "leg is the stage-then-ingest one: pending/ KeyCount=0; done/ holds exactly "
                    "ONE batch, 20260717T173239Z.jsonl, 682,586 bytes, ingested "
                    "2026-07-17T17:43:22Z -- one second after the table's sole write, which is "
                    "the join tying the planes together. So DESIRED, APPLIED and EXERCISED come "
                    "apart here: the trigger that exists is applied and exercised DAILY, and "
                    "this surface's output has not moved in %d days. "
                    "HELD, not measured by this seat: 3.0.0_SA_CVO~X reconciled this to "
                    "GRAPHFEED_TO7_SNAP_FAMILY_PARK_RECORD_20260811 -- the snap family is a "
                    "DOCUMENTED single-build-vintage PARKED surface, so the gap is recorded, not "
                    "novel. I have not read that record at source; it is cited as a named "
                    "authority and the live_matches_declared `no` above stands on my own "
                    "measurements, not on it." % age),
                "owner": LANE,
            },
        },
        "artifact": {
            "persistence": {
                "persisted": True,
                "authority_role": "projection",
                "mutation_policy": "append_only",
                "form": "an Iceberg table: data files plus a metadata/ tree",
                "basis": "measured",
                "evidence": ("KeyCount at the declared home = %d (a POSITIVE, which a wrong "
                             "bucket or a missing s3:ListBucket cannot produce); %d objects / "
                             "%d bytes counted client-side over an auto-paginated listing. "
                             "authority_role is `projection`: the rows are a projection of the "
                             "staged batch, which is itself derived from the fedobs observe "
                             "plane; nothing measured here makes this table authoritative for "
                             "co-evolution." % (kc, cen["objects"], cen["bytes"])),
                "owner": LANE,
            },
            "location": {
                "home": "s3://%s/%s" % (BUCKET, home),
                "projection_of": [
                    {"id": "s3://%s/warehouse/snap_ingest/done/fedobs_coevolution_snap/"
                           "20260717T173239Z.jsonl" % BUCKET,
                     "note": "the single staged batch this table was ingested from; 682,586 "
                             "bytes, ingested 2026-07-17T17:43:22Z"}],
                "co_resident_stores": [
                    {"id": "s3://%s/warehouse/globgrph/" % BUCKET,
                     "note": "sibling snap surfaces share this bucket and prefix root; CONTENT "
                             "overlap not measured, only co-residence"},
                    {"id": "s3://%s/warehouse/fedobs_signals/observations/"
                           "fedobs_observations.json" % BUCKET,
                     "note": "the OBSERVE plane -- a DIFFERENT artifact carrying overlapping "
                             "subject matter, written daily (today 46,856,449 bytes, 31,852 "
                             "coevolution rows). Named because a duplicate-store census that "
                             "missed it would understate the estate, and because the declared "
                             "nightly cadence belongs to THIS artifact and not to the table"}],
                "basis": "measured",
                "evidence": ("the s3:// URIs are EXACT IDENTITIES a consumer can equality-join; "
                             "the home resolved live at KeyCount=%d, and the observe-plane object "
                             "and staged batch were both listed live." % kc),
                "owner": LANE,
            },
        },
        "trust": {
            "coverage": {
                "universe": ("objects under the store's own S3 home -- NOT the co-evolution pair "
                             "population, and NOT the observe plane"),
                "denominator": ("%d of %d objects at the declared home"
                                % (cen["objects"], cen["objects"])),
                "explicitly_out": [
                    "NO COMPLETENESS OF THE CO-EVOLUTION PAIR POPULATION IS ASSERTED. The observe "
                    "plane reported 31,852 coevolution rows today against this table's single "
                    "July batch; comparing those two numbers is a DIFFERENT question with a "
                    "different denominator and nothing here measures it.",
                    "the row-level contents of the Iceberg data files (object plane only)",
                    "WHY the stage-then-ingest leg stopped -- unmeasured",
                    "whether any consumer still READS this store, and whether a stale read is "
                    "material to it -- unmeasured here",
                ],
                "basis": "measured",
                "evidence": ("aws s3api list-objects-v2 auto-paginated, counted client-side: %d "
                             "objects, %d bytes, %d distinct write-day(s), newest %s."
                             % (cen["objects"], cen["bytes"], cen["distinct_write_days"],
                                cen["newest_utc"])),
                "owner": LANE,
            },
            "key": {
                "identity_space": ("S3 (bucket, key) for the artifact plane; (namespace, table) "
                                   "in the Nessie catalog for the logical table"),
                "key_expression": "bucket + key, exact string match",
                "key_is_stable": "stable",
                "crosses_spaces": True,
                "declared_mapping": ("(subject_a, subject_b) is the row-level pair key per the "
                                     "surface payload at snap_store.py:128-135; that join was not "
                                     "exercised by this card"),
                "basis": "held",
                "evidence": ("basis is the FLOOR: the S3 identity is MEASURED, but the catalog's "
                             "(namespace, table) -> prefix binding was read from the manifest and "
                             "NOT verified against the catalog, and the pair key was not "
                             "exercised. Measured limb plus read limbs -> held."),
                "owner": LANE,
            },
            "failure_mode": {
                "returns_on_failure": ("A true absence returns KeyCount=0 at rc=0 -- a failed "
                                       "retrieval returns a VALUE, not an error. MEASURED: a "
                                       "wrong BUCKET does NOT do this (rc=255, NoSuchBucket) and "
                                       "a wrong REGION does NOT either (rc=0, the CORRECT "
                                       "KeyCount). ⛔ A WRONG PREFIX DOES: a one-character error "
                                       "in the table's UUID returns KeyCount=0, identical to an "
                                       "absent table. A missing s3:ListBucket remains "
                                       "unexercised."),
                "distinguishable_from_true_negative": "no",
                "basis": "inferred",
                "basis_by_field": {
                    "returns_on_failure": "measured",
                    "distinguishable_from_true_negative": "inferred"},
                "evidence": (
                    "FOUR READ-ONLY PROBES, each a SEPARATE invocation, rc read UNPIPED: true "
                    "absence -> rc=%d %r; wrong bucket -> rc=%d %r; wrong region -> rc=%d %r; "
                    "WRONG PREFIX (this table's UUID with its last character changed from 9 to "
                    "5) -> rc=%d %r. Target existence, separately: KeyCount=%d. "
                    "⛔ THE WRONG-PREFIX CLASS IS MEASURED HERE BECAUSE THIS SEAT HIT IT ON THIS "
                    "SUBJECT: the home was first reconstructed from a print truncated at 110 "
                    "characters, the UUID tail was one character wrong, and KeyCount returned 0 "
                    "-- which would have been published as an ABSENT TABLE against an enabled "
                    "nightly schedule. It was caught by re-reading the home from the carrier "
                    "instead of the display. AMONG THE FOUR EXERCISED CLASSES, a zero is "
                    "produced by a true absence AND by a wrong prefix, so a zero here is NOT "
                    "diagnostic; the scope is load-bearing and the fifth class (missing "
                    "s3:ListBucket) remains unexercised. distinguishable is `no`, and the row "
                    "floors to `inferred`."
                    % (zc["true_absence"][0], zc["true_absence"][1],
                       zc["wrong_bucket"][0], zc["wrong_bucket"][1],
                       zc["wrong_region"][0], zc["wrong_region"][1],
                       wrong_prefix[0], wrong_prefix[1], kc)),
                "owner": LANE,
            },
        },
        "verdict": {
            "standing": "QUALIFIED",
            "why": ("The store RESOLVES and holds real bytes from exactly one staged batch, and "
                    "it is %d days cold. ⛔ ITS DECLARED CADENCE BELONGS TO A DIFFERENT ARTIFACT: "
                    "the nightly rule is ENABLED, fires daily and succeeds, but writes the "
                    "fedobs OBSERVE plane, not this table -- so live_matches_declared is `no`, "
                    "measured on four instruments (EventBridge state, CloudWatch Invocations, "
                    "the ECS task log, and the two artifacts' own object planes). QUALIFIED on "
                    "the limbs ENUMERATED below and deliberately NOT counted, so that adding a "
                    "limb cannot desynchronise a cardinal: authority_role is `projection`; the "
                    "catalog-to-prefix binding and the pair key are HELD rather than measured; "
                    "coverage spans the OBJECT plane only; a zero at this prefix is NOT "
                    "diagnostic, since a wrong prefix produces one as readily as an absence; "
                    "WHY the ingest leg stopped is UNMEASURED; and whether a consumer reads this "
                    "store, or is harmed by a stale read, is UNMEASURED here. THIS CARD DOES NOT "
                    "CLASSIFY THE GAP AS A DEFECT: 3.0.0_SA_CVO~X reconciled it to a documented "
                    "PARKED snap family, which this seat has not read at source and therefore "
                    "carries as held. Naming the split is the carder's job; deciding it is the "
                    "owner's." % age),
            "blocking_defects": None,
        },
        "forward_disposition": {
            "standing": "undecided",
            "set_by": None,
            "basis": "absent",
            "evidence": ("NOT SET BY THE CARDING LANE -- the store owner's call at the class "
                         "close, and this surface is recorded as parked by a named record."),
            "decided_utc": None,
        },
        "carded_by": LANE,
    }


def card_fedobs_coverage_snap():
    home = HOMES["fedobs_coverage_snap"]
    kc = key_count(home)
    cen = object_census(home)
    zc = zero_class_probes(home)
    wrong_prefix = probe("s3api", "list-objects-v2", "--bucket", BUCKET, "--prefix",
                         home[:-2] + "7/", "--max-keys", "1", "--query", "KeyCount",
                         "--output", "text")
    cells = carrier_cells(GROUPS["fedobs_coverage_snap"])
    writer, stager = "infra/aws/globgrph/snap_store.py", "infra/aws/globgrph/emit_fedobs_snap.py"
    wpin, spin = git_pin(writer), git_pin(stager)
    newest = datetime.strptime(cen["newest_utc"][:19], "%Y-%m-%dT%H:%M:%S").replace(
        tzinfo=timezone.utc)
    age = (datetime.now(timezone.utc) - newest).days

    return {
        "schema_version": 3.1,
        "subject": {
            "id": "fedobs_coverage_snap",
            "kind": "store",
            "declared_domain": (
                "The fedobs compiler-COVERAGE snapshot store: one registered SURFACE of "
                "snap_store.py holding (artifact_class, total_cses, untyped_low, "
                "untyped_low_rate) rows, staged from the served fedobs observations JSON and "
                "ingested. The recognizer-coverage-gap signal NFRA_PROMOTE consumes. ⛔ THE "
                "SUBJECT IS THIS TABLE, not the fedobs OBSERVE plane it is staged FROM and not "
                "its sibling fedobs_coevolution_snap, which is a different surface with a "
                "different signal and a different write date. "
                "QUALIFIES THE CELLS CARRIER (AC4): %s @%s, cells %s -- the carrier is NOT edited."
                % (CARRIER, CARRIER_PIN, " ".join(c["cell_id"] for c in cells))),
        },
        "as_of": {
            "carded_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "commit_ish": subprocess.run(["git", "rev-parse", "HEAD"],
                                         capture_output=True, text=True).stdout.strip(),
            "graph_vintage": "S3 object plane, S3 staging plane, the heartbeat key, EventBridge "
                             "and terraform all read live at card time",
        },
        "process": {
            "methodology": {
                "how": ("Iceberg append via snap_store.py append_rows(): emit_fedobs_snap.py "
                        "projects the compiler_coverage signal out of the served fedobs "
                        "observations JSON, stages a .jsonl batch to "
                        "warehouse/snap_ingest/pending/fedobs_coverage_snap/, and snap_store "
                        "coerces it against the typed payload, appends in one Nessie commit and "
                        "MOVES the batch to done/. Fail-closed at both ends: the stager SKIPS a "
                        "signal carrying an 'error' key rather than staging a fabricated row, "
                        "and the writer rejects an invalid batch LOUD, leaving it in pending/."),
                "determinism": "deterministic",
                "composes": [
                    {"id": stager + " @" + spin[:10],
                     "note": "maps compiler_coverage -> fedobs_coverage_snap at :46 (SHIPPED "
                             "P2b) and projects the columnar payload; the staged-batch producer "
                             "for this surface"},
                    {"id": "s3://%s/warehouse/fedobs_signals/observations/"
                           "fedobs_observations.json" % BUCKET,
                     "note": "the SOURCE artifact the stager reads -- its ['signals']"
                             "['compiler_coverage'] entry. Written DAILY and healthy: today's "
                             "producer run logged 'OK: SIGNAL compiler_coverage rows=7'"},
                    {"id": "warehouse/snap_ingest/pending/fedobs_coverage_snap/*.jsonl",
                     "note": "the handoff artifact between stager and writer"},
                    {"id": writer,
                     "note": "the ONE writer for all snap surfaces; this surface's typed payload "
                             "is declared at :113-120"}],
                "invents": [],
                "materializer_standing": "historical_in_use",
                "basis": "measured",
                "evidence": ("Read at source with line numbers from grep -n AT THE PIN: %s @%s "
                             "surface payload :113-120 under the P2b comment at :109-112; %s @%s "
                             "signal mapping at :46 and the honest-degrade skip at :47-49. "
                             "materializer_standing is `historical_in_use`, not `canonical`: the "
                             "surface shipped and was written once, and the cadence row records "
                             "no trigger that would write it again."
                             % (writer, wpin[:10], stager, spin[:10])),
                "owner": LANE,
            },
            "cadence": {
                "declared_rhythm": ("the surface comment at snap_store.py:109 says the coverage "
                                    "snapshot is 'overwritten nightly' from a source that is "
                                    "'dev-box readable' -- a DECLARED nightly with a host-bound "
                                    "source, never a cloud schedule"),
                "actual_trigger": ("NONE FOUND for the STAGER, measured across three planes; the "
                                   "one nightly cloud rule that exists refreshes the SOURCE "
                                   "artifact, not this table"),
                "live_matches_declared": "no",
                "live_instance_age": ("%d days: sole write-day %s, newest object %s"
                                      % (age, sorted(cen["per_day_tail"])[0], cen["newest_utc"])),
                "basis": "measured",
                "basis_by_field": {"declared_rhythm": "measured",
                                   "actual_trigger": "measured",
                                   "live_matches_declared": "measured",
                                   "live_instance_age": "measured"},
                "evidence": (
                    "⛔ THE SOURCE IS FRESH AND THE TABLE IS NOT, WHICH LOCATES THE MISSING LEG "
                    "PRECISELY. The stager reads fedobs_observations.json['signals']"
                    "['compiler_coverage']; that artifact was written TODAY (46,856,449 bytes) "
                    "and today's producer run logged 'OK: SIGNAL compiler_coverage rows=7', so "
                    "the input exists, is healthy, and would not trip the honest-degrade skip. "
                    "The table has not moved in %d days. The gap is therefore in the STAGER's "
                    "invocation, not in the source and not in the writer. "
                    "TRIGGER SWEPT ON THREE PLANES, each figure quoted from the rail it was "
                    "read on: (1) EventBridge -- no rule names the stager; the only fedobs rule "
                    "is opal-globgrph-fedobs-producer-nightly, which drives the SOURCE. "
                    "(2) TERRAFORM, scope infra/aws/terraform -- emit_fedobs_snap returns 0 hits "
                    "across 608 files scanned. ⛔ THAT ZERO IS OVER SEARCHABLE TEXT ONLY: the "
                    "same rail line reports 254 BINARY files NOT SEARCHED, so the absence is "
                    "scoped to the 608 searchable files and says nothing about the excluded "
                    "254. TWO CONTROLS ON THE IDENTICAL SCOPE, both FIRING: fedobs[-_]producer "
                    "-> 24 hits across those same 608 scanned files; schedule_expression "
                    "--files -> 150 hits across 68 MATCHING files. The corpus therefore "
                    "demonstrably carries both producers and schedules, and the stager's "
                    "absence is MEASURED within that scope. "
                    "⛔ AN EARLIER VERSION OF THIS ROW GAVE THE schedule_expression CONTROL A "
                    "FILE COUNT OF THIRTY-TWO AND CALLED IT THE SAME CORPUS. Both halves were "
                    "false and both certifiers reproduced it: that figure came from a DIFFERENT "
                    "scope "
                    "(infra/aws/terraform/globgrph, a subdirectory) run with a COMBINED pattern, "
                    "where 32 was the count of files SCANNED and not files matching. The "
                    "subdirectory's combined-pattern hit count happened to equal the full "
                    "tree's producer count -- 24 in both -- which is exactly why the mismatched "
                    "scope read as consistent. A denominator line says 'N hit(s) across M "
                    "file(s) SCANNED'; M is the corpus size, never the match count. "
                    "(3) CALLERS -- a filename census over infra/aws/globgrph returns the stager "
                    "and nothing else, so no sibling module or entrypoint in that tree invokes "
                    "it by name. "
                    "MEASURED STAGING PLANE: pending/ empty; done/ holds exactly ONE batch, "
                    "20260716T150137Z.jsonl, 2,017 bytes, ingested 2026-07-16T15:28:07Z -- the "
                    "SAME INSTANT as the table's sole write and as the heartbeat key "
                    "last_append/fedobs_coverage_snap.json (137 bytes, same timestamp). ⛔ AND "
                    "ONE SECOND AFTER code_heat_snap's ingest at 15:28:06Z, which is evidence "
                    "that a SINGLE ingest run wrote both surfaces rather than two independent "
                    "cadences happening to stop together. "
                    "This independently corroborates, on a different instrument, what "
                    "3.0.0_SA_CVO~X read in "
                    "GRAPHFEED_TO7_SNAP_FAMILY_PARK_RECORD_20260811 -- exactly one build, no "
                    "schedule covering snap staging or ingest. That record is HELD here, not "
                    "read at source by this seat; the three-plane result above is mine."
                    % age),
                "owner": LANE,
            },
        },
        "artifact": {
            "persistence": {
                "persisted": True,
                "authority_role": "projection",
                "mutation_policy": "append_only",
                "form": "an Iceberg table: data files plus a metadata/ tree",
                "basis": "measured",
                "evidence": ("KeyCount at the declared home = %d (a POSITIVE, which a wrong "
                             "bucket or a missing s3:ListBucket cannot produce); %d objects / "
                             "%d bytes counted client-side over an auto-paginated listing. "
                             "authority_role is `projection`, not `source`: the rows are a "
                             "columnar projection of one signal inside the served observations "
                             "JSON, which the stager's own mapping at :46 makes explicit. The "
                             "object census establishes PERSISTENCE only and cannot establish "
                             "authority." % (kc, cen["objects"], cen["bytes"])),
                "owner": LANE,
            },
            "location": {
                "home": "s3://%s/%s" % (BUCKET, home),
                "projection_of": [
                    {"id": "s3://%s/warehouse/snap_ingest/done/fedobs_coverage_snap/"
                           "20260716T150137Z.jsonl" % BUCKET,
                     "note": "the single staged batch this table was ingested from; 2,017 bytes, "
                             "ingested 2026-07-16T15:28:07Z"},
                    {"id": "fedobs_observations.json['signals']['compiler_coverage']",
                     "note": "the upstream signal the staged batch projects; the served JSON is "
                             "refreshed daily and this card did NOT compare its current contents "
                             "against the table's July rows"}],
                "co_resident_stores": [
                    {"id": "s3://%s/warehouse/globgrph/" % BUCKET,
                     "note": "sibling snap surfaces share this bucket and prefix root; CONTENT "
                             "overlap not measured, only co-residence"},
                    {"id": "s3://%s/warehouse/fedobs_signals/observations/"
                           "fedobs_observations.json" % BUCKET,
                     "note": "the SOURCE artifact, carrying the same subject matter in a "
                             "different shape and refreshed daily. Named because a "
                             "duplicate-store census that missed it would understate the estate"}],
                "basis": "measured",
                "evidence": ("the s3:// URIs are EXACT IDENTITIES a consumer can equality-join. "
                             "⛔ THE HOME WAS COPIED FROM THE CARRIER, NEVER RETYPED FROM A "
                             "RENDERING: on the sibling surface this seat reconstructed a UUID "
                             "from a print truncated at 110 characters, got the last character "
                             "wrong, and read the resulting KeyCount=0 as an absent table. "
                             "Resolved live here at KeyCount=%d." % kc),
                "owner": LANE,
            },
        },
        "trust": {
            "coverage": {
                "universe": ("objects under the store's own S3 home -- NOT the coverage-row "
                             "population and NOT the served signal it projects"),
                "denominator": ("%d of %d objects at the declared home"
                                % (cen["objects"], cen["objects"])),
                "explicitly_out": [
                    "NO COMPLETENESS OF THE COVERAGE-ROW POPULATION IS ASSERTED. Today's served "
                    "signal carries 7 compiler_coverage rows against this table's single July "
                    "batch; whether those differ, and by how much, is a DIFFERENT question with "
                    "a different denominator and this card does not measure it.",
                    "the row-level contents of the Iceberg data files (object plane only)",
                    "WHY the stager stopped being invoked -- unmeasured",
                    "whether any consumer still READS this store, and whether a stale read is "
                    "material to NFRA_PROMOTE -- unmeasured here",
                ],
                "basis": "measured",
                "evidence": ("aws s3api list-objects-v2 auto-paginated, rows PARSED rather than "
                             "line-counted: %d objects, %d bytes, %d distinct write-day(s), "
                             "newest %s. (A line-count over multi-column output overcounts "
                             "whenever a second column shares the leading character -- that "
                             "error was made and caught on the sibling surface.)"
                             % (cen["objects"], cen["bytes"], cen["distinct_write_days"],
                                cen["newest_utc"])),
                "owner": LANE,
            },
            "key": {
                "identity_space": ("S3 (bucket, key) for the artifact plane; (namespace, table) "
                                   "in the Nessie catalog for the logical table"),
                "key_expression": "bucket + key, exact string match",
                "key_is_stable": "stable",
                "crosses_spaces": True,
                "declared_mapping": ("artifact_class is the row-level key per the surface payload "
                                     "at snap_store.py:113-120, and is the axis NFRA_PROMOTE's "
                                     "untyped_low_rate trends over; that join was not exercised"),
                "basis": "held",
                "evidence": ("basis is the FLOOR: the S3 identity is MEASURED, but the catalog's "
                             "(namespace, table) -> prefix binding was read from the manifest and "
                             "NOT verified against the catalog, and the artifact_class join was "
                             "not exercised. Measured limb plus read limbs -> held."),
                "owner": LANE,
            },
            "failure_mode": {
                "returns_on_failure": ("A true absence returns KeyCount=0 at rc=0 -- a failed "
                                       "retrieval returns a VALUE, not an error. MEASURED: a "
                                       "wrong BUCKET does NOT do this (rc=255, NoSuchBucket) and "
                                       "a wrong REGION does NOT either (rc=0, the CORRECT "
                                       "KeyCount). ⛔ A WRONG PREFIX DOES: a one-character error "
                                       "in the table's UUID returns KeyCount=0, identical to an "
                                       "absent table. A missing s3:ListBucket remains "
                                       "unexercised."),
                "distinguishable_from_true_negative": "no",
                "basis": "inferred",
                "basis_by_field": {
                    "returns_on_failure": "measured",
                    "distinguishable_from_true_negative": "inferred"},
                "evidence": (
                    "FOUR READ-ONLY PROBES, each a SEPARATE invocation, rc read UNPIPED: true "
                    "absence -> rc=%d %r; wrong bucket -> rc=%d %r; wrong region -> rc=%d %r; "
                    "WRONG PREFIX (this table's UUID with its last character changed) -> rc=%d "
                    "%r. Target existence, separately: KeyCount=%d. AMONG THE FOUR EXERCISED "
                    "CLASSES a zero is produced by a true absence AND by a wrong prefix, so a "
                    "zero here is NOT diagnostic; the scope is load-bearing and the fifth class "
                    "(missing s3:ListBucket) remains unexercised. distinguishable is `no` and "
                    "the row floors to `inferred`. The wrong-prefix class is carried because "
                    "this seat HIT it on the sibling surface and nearly published a vanished "
                    "table from it."
                    % (zc["true_absence"][0], zc["true_absence"][1],
                       zc["wrong_bucket"][0], zc["wrong_bucket"][1],
                       zc["wrong_region"][0], zc["wrong_region"][1],
                       wrong_prefix[0], wrong_prefix[1], kc)),
                "owner": LANE,
            },
        },
        "verdict": {
            "standing": "QUALIFIED",
            "why": ("The store RESOLVES and holds real bytes from exactly one staged batch, and "
                    "it is %d days cold. ⛔ THE MISSING LEG IS LOCATED, WHICH IS THE USEFUL PART: "
                    "the SOURCE signal is fresh and healthy TODAY (7 compiler_coverage rows in a "
                    "JSON written this morning) and the WRITER is the same module that serves "
                    "every sibling surface, so the gap is in the STAGER's invocation -- for "
                    "which no trigger exists on any of three swept planes, one of them controlled "
                    "and firing. QUALIFIED on the limbs ENUMERATED below and deliberately NOT "
                    "counted, so that adding a limb cannot desynchronise a cardinal: "
                    "authority_role is `projection` and the served signal it projects was NOT "
                    "compared against the table's rows; the catalog-to-prefix binding and the "
                    "artifact_class join are HELD rather than measured; coverage spans the "
                    "OBJECT plane only; a zero at this prefix is NOT diagnostic, since a wrong "
                    "prefix produces one as readily as an absence; WHY the stager stopped being "
                    "invoked is UNMEASURED; and whether NFRA_PROMOTE or any other consumer reads "
                    "this store, or is harmed by a stale read, is UNMEASURED here. THIS CARD "
                    "DOES NOT CLASSIFY THE GAP AS A DEFECT: the snap family is recorded as "
                    "parked by a named record this seat carries as HELD, and the ingest evidence "
                    "-- this surface written one second after code_heat_snap -- is consistent "
                    "with a single build that was never repeated rather than with a cadence that "
                    "failed. Naming that is the carder's job; deciding it is the owner's." % age),
            "blocking_defects": None,
        },
        "forward_disposition": {
            "standing": "undecided",
            "set_by": None,
            "basis": "absent",
            "evidence": ("NOT SET BY THE CARDING LANE -- the store owner's call at the class "
                         "close, and this surface is recorded as parked by a named record."),
            "decided_utc": None,
        },
        "carded_by": LANE,
    }


def _iceberg_layout(prefix):
    """Object layout under an Iceberg table home, counted CLIENT-SIDE from an auto-paginated
    list. Local to this card on purpose: object_census() is shared with the four CLOSED cards
    and changing it would move their output, so this measures the extra shape here instead."""
    out = _aws("s3api", "list-objects-v2", "--bucket", BUCKET, "--prefix", prefix,
               "--query", "Contents[].[Key,LastModified,Size]", "--output", "text")
    rows = [ln.split("\t") for ln in out.splitlines() if ln.strip()]
    seg = collections.Counter(r[0][len(prefix):].split("/")[0] for r in rows)
    snaps = [r[0] for r in rows if "/metadata/snap-" in r[0]]
    commits = {m.group(1) for m in
               (re.search(r"-([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})"
                          r"\.parquet$", r[0]) for r in rows) if m}
    eds = sorted({m.group(1) for m in
                  (re.search(r"event_date=([^/]+)/", r[0]) for r in rows) if m})
    stamps = sorted(r[1] for r in rows)
    return {"objects": len(rows), "bytes": sum(int(r[2]) for r in rows),
            "by_segment": dict(seg), "snapshots": len(snaps),
            "write_commit_uuids": sorted(commits), "event_date_partitions": len(eds),
            "event_date_range": (eds[0], eds[-1]) if eds else None,
            "first_write": stamps[0], "last_write": stamps[-1],
            "distinct_write_days": len({s[:10] for s in stamps}),
            "keys": {r[0] for r in rows}}


def refuse_sibling_confusion(mine, sibling):
    """cse_test_24458e6c and cse_test_bb57a916 share the TABLE NAME `cse_test` and are told apart
    ONLY by the uuid in their S3 home.

    Everywhere else on this face a wrong home fails LOUD -- it resolves to nothing and KeyCount
    returns 0. Here it does not: a home copied or edited between these two lands on a REAL,
    POPULATED table, so KeyCount=1 still returns, every arm written for the other card still
    passes, and the card is silently about the wrong table. That is the one place on this face
    where the copy hazard is structural rather than stylistic, so it gets a structural refusal
    rather than a note telling a later reader to be careful.
    """
    if mine["keys"] & sibling["keys"]:
        raise ValueError("SIBLING CONFUSION: the two cse_test homes share %d key(s); they must "
                         "be disjoint" % len(mine["keys"] & sibling["keys"]))
    if (mine["objects"], mine["bytes"]) == (sibling["objects"], sibling["bytes"]):
        raise ValueError("SIBLING CONFUSION: both cse_test homes census identically "
                         "(%d objects / %d bytes) -- indistinguishable, so this card cannot "
                         "claim which table it measured" % (mine["objects"], mine["bytes"]))
    return True


def card_cse_test_24458e6c():
    home = HOMES["cse_test_24458e6c"]
    sib_home = HOMES["cse_test_bb57a916"]
    home_uri = "s3://%s/%s" % (BUCKET, home)
    sib_uri = "s3://%s/%s" % (BUCKET, sib_home)
    kc = key_count(home)
    cen = object_census(home)
    lay = _iceberg_layout(home)
    sib = _iceberg_layout(sib_home)
    refuse_sibling_confusion(lay, sib)
    zc = zero_class_probes(home)
    # a wrong-prefix probe built by mutating THIS home's uuid tail: the class that returned a
    # KeyCount of 0 and read as a vanished table on card 3
    wrong_prefix = probe("s3api", "list-objects-v2", "--bucket", BUCKET, "--prefix",
                         home[:-2] + "3/", "--max-keys", "1", "--query", "KeyCount",
                         "--output", "text")
    cells = carrier_cells(GROUPS["cse_test_24458e6c"])
    writer = "infra/aws/globgrph/cse_store.py"
    wpin = git_pin(writer)
    newest = datetime.strptime(cen["newest_utc"][:19], "%Y-%m-%dT%H:%M:%S").replace(
        tzinfo=timezone.utc)
    age = (datetime.now(timezone.utc) - newest).days

    return {
        "schema_version": 3.1,
        "subject": {
            "id": "cse_test_24458e6c",
            "kind": "store",
            "declared_domain": (
                "An ISOLATED TEST-HARNESS Iceberg table in the globgrph Nessie namespace, "
                "holding CSE (Change/Signal Event) rows partitioned by (source, event_date) -- "
                "the same shape as the production log. Its SURVIVING objects were written by a "
                "SINGLE append and carry no later surviving write. "
                "⛔ THE SUBJECT IS THE TABLE AT THIS EXACT S3 HOME (uuid 24458e6c-667c-4e85-"
                "ba44-33751795e182). It is NOT the production `cse` store, and it is NOT its "
                "same-named sibling cse_test_bb57a916 -- BOTH scratch tables carry the table "
                "name `cse_test` and are distinguished ONLY by the uuid in their home, which is "
                "why this card's coverage row names the sibling in explicitly_out and the "
                "builder refuses structurally if the two census identically. "
                "QUALIFIES THE CELLS CARRIER (AC4): %s @%s, cells %s -- the carrier is NOT edited."
                % (CARRIER, CARRIER_PIN, " ".join(c["cell_id"] for c in cells))),
        },
        "as_of": {
            "carded_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "commit_ish": subprocess.run(["git", "rev-parse", "HEAD"],
                                         capture_output=True, text=True).stdout.strip(),
            "graph_vintage": "S3 object plane read live at card time for this home AND for the "
                             "sibling home used as the discrimination control; no graph consulted",
        },
        "process": {
            "methodology": {
                "how": ("Iceberg create_table + a SINGLE append through cse_store.py's "
                        "unconstrained --table override: ensure_cse_table() creates "
                        "globgrph.<table> with cse_iceberg_schema() partitioned by "
                        "(source, event_date), and the append path writes one Nessie commit. "
                        "⛔ THE INVOCATION THAT DID THIS WAS NOT FOUND AND IS NOT CLAIMED -- "
                        "see the basis."),
                "determinism": "deterministic",
                "composes": [
                    {"id": writer + " @" + wpin[:10],
                     "note": "the code path that can create this table: --table at :581 carries "
                             "no choices=, so it accepts any name in the namespace; "
                             "ensure_cse_table() at :321 creates it; catalog.create_table at "
                             ":338. Its docstring at :325 invites exactly this use -- 'pass a "
                             "scratch name (e.g. cse_test) for an ISOLATED test harness'"}],
                "invents": [],
                "materializer_standing": "historical_in_use",
                "basis": "inferred",
                "basis_by_field": {
                    "how": "inferred",
                    "composes": "inferred",
                    "determinism": "inferred",
                    "materializer_standing": "measured",
                },
                "evidence": (
                    "⛔ THE ROW IS `inferred` AND THE SENTENCE MUST NOT OUTRUN IT. "
                    "generation.materializer is null in the manifest and NO code names this "
                    "table; I did not find the invocation that created it and I am not claiming "
                    "one. The MEASURED facts that follow sit UNDER that `inferred` floor and do "
                    "NOT raise it -- they are what makes the inference more than a "
                    "name-shape guess: the physical layout at this home matches cse_store.py's declared "
                    "partition spec EXACTLY -- %d data objects all under source=git/ across %d "
                    "event_date partitions (%s..%s), which is the (source, event_date) spec "
                    "ensure_cse_table() applies at %s:%s @%s. A structural match to a writer's "
                    "partition spec identifies the writer CLASS; it does not identify the run. "
                    "materializer_standing is `historical_in_use` (MEASURED): exactly %d "
                    "snapshot and %d distinct write-commit uuid SURVIVE at this home, so the "
                    "writer ran here and has not run again IN THE SURVIVING RECORD -- which is "
                    "not the same as never, and the lifetime count is UNMEASURED."
                    % (lay["by_segment"].get("data", 0), lay["event_date_partitions"],
                       lay["event_date_range"][0], lay["event_date_range"][1],
                       writer, "321/338", wpin[:10], lay["snapshots"],
                       len(lay["write_commit_uuids"]))),
                "owner": LANE,
            },
            "cadence": {
                "declared_rhythm": "NONE DECLARED -- generation.trigger is null in the manifest",
                "actual_trigger": ("none found; and the SURVIVING write history says none is "
                                   "needed -- the surviving set was written by ONE append, "
                                   "with the lifetime count UNMEASURED"),
                "live_matches_declared": "not_applicable",
                "live_instance_age": ("%s objects written between %s and %s -- a %d-second "
                                      "window on %d distinct write-day; %d days stale at carding"
                                      % (lay["objects"], lay["first_write"], lay["last_write"],
                                         (datetime.strptime(lay["last_write"][:19],
                                                            "%Y-%m-%dT%H:%M:%S")
                                          - datetime.strptime(lay["first_write"][:19],
                                                              "%Y-%m-%dT%H:%M:%S")).seconds,
                                         lay["distinct_write_days"], age)),
                "basis": "absent",
                "basis_by_field": {
                    "declared_rhythm": "absent",
                    "actual_trigger": "measured",
                    "live_instance_age": "measured",
                    "live_matches_declared": "absent",
                },
                "evidence": (
                    "⛔ TWO DIFFERENT CLAIMS LIVE IN THIS ROW AND THEY DO NOT SHARE A BASIS, SO THE "
                    "ROW BASIS IS THE FLOOR OF ITS FIELDS -- `absent` -- WHICH IS "
                    "WEAKER THAN ITS STRONGEST FIELD ON PURPOSE (the same shape as "
                    "code_heat_snap's cadence row, and the floor rule holds in 7 of 7 "
                    "basis_by_field rows across the four closed cards). "
                    "(1) `declared_rhythm` floors to `absent`: generation.trigger is an "
                    "UNPOPULATED field, and an unpopulated field is not a measured negative -- "
                    "collapsing those two is the defect this wave exists to stop. (2) "
                    "`actual_trigger` is MEASURED, and it is a stronger statement than 'no "
                    "trigger was found' -- BUT IT IS SCOPED TO THE SURVIVING SET AND NOT BEYOND "
                    "IT: the objects and metadata PRESENT AT THIS HOME were written by "
                    "exactly ONE commit in one 3-second window. ⛔ THIS DOES NOT "
                    "EXCLUDE AN EARLIER WRITE SINCE REPLACED OR EXPIRED -- snapshot "
                    "expiry and overwrite both converge on one surviving snapshot, so "
                    "'only ever written once' would need the metadata log's snapshot "
                    "HISTORY, not its current head, and that is UNMEASURED here. The "
                    "cadence point does not rest on it: what carries the row is the "
                    "surviving set plus the staleness. The discriminator "
                    "is the Iceberg metadata tree, not the timestamps -- %d snapshot object and "
                    "%d distinct write-commit uuid (%s) across all %d objects, so every data "
                    "file belongs to one append. A one-shot write cannot be a cadence that "
                    "failed, and it does not become one by ageing. Timestamps corroborate: first "
                    "%s, last %s, %d distinct write-day. ⛔ WHY the run happened, and whether "
                    "anyone intended it to repeat, is UNMEASURED."
                    % (lay["snapshots"], len(lay["write_commit_uuids"]),
                       lay["write_commit_uuids"][0], lay["objects"],
                       lay["first_write"], lay["last_write"], lay["distinct_write_days"])),
                "owner": LANE,
            },
        },
        "artifact": {
            "persistence": {
                "persisted": True,
                "authority_role": "source",
                "mutation_policy": "append_only",
                "form": ("an Iceberg table: %d data parquet objects under data/source=git/"
                         "event_date=*/ plus a %d-object metadata/ tree (2 *.metadata.json, one "
                         "-m0.avro manifest, one snap-*.avro snapshot)"
                         % (lay["by_segment"].get("data", 0),
                            lay["by_segment"].get("metadata", 0))),
                "basis": "measured",
                "evidence": (
                    "KeyCount at the declared home = %d, a POSITIVE -- which a wrong bucket or a "
                    "missing s3:ListBucket cannot produce. Controls run as SEPARATE invocations: "
                    "POSITIVE prefix 'warehouse/' -> 1; NEGATIVE prefix "
                    "'warehouse/globgrph/zzz_no_such_prefix_99999/' -> 0. Both fired, so a 0 "
                    "here would have been a real 0. Segment split counted client-side from the "
                    "auto-paginated list: %s. ⛔ `mutation_policy` is `append_only`; "
                    "DROPPABILITY IS A LIFECYCLE FACT RECORDED HERE, NOT AN ENUM VALUE, and it "
                    "is the part that is NOT true of the production log: "
                    "ensure_cse_table() is ENSURE-ONLY and never "
                    "overwrites or repartitions (%s:321-325 @%s), but --drop at :579 explicitly "
                    "permits dropping a SCRATCH table and 'refuses the real log'. This table is "
                    "on the permitted side of that guard. Whether it SHOULD be dropped is the "
                    "owner's call and is not set here."
                    % (kc, lay["by_segment"], writer, wpin[:10])),
                "owner": LANE,
            },
            "location": {
                "home": home_uri,
                "projection_of": [],
                "co_resident_stores": [
                    {"id": sib_uri,
                     "note": "⛔ THE SAME-NAMED SIBLING. Shares the table name `cse_test`; "
                             "differs only in the uuid. MEASURED disjoint from this home: %d "
                             "objects / %d bytes against this table's %d / %d, key-set "
                             "intersection 0. It is the reason this card carries a structural "
                             "sibling refusal rather than a caution."
                             % (sib["objects"], sib["bytes"], lay["objects"], lay["bytes"])},
                    {"id": "s3://%s/warehouse/globgrph/" % BUCKET,
                     "note": "the globgrph warehouse prefix root, shared with every sibling "
                             "table; overlap of CONTENT was not measured, only of PREFIX"}],
                "basis": "measured",
                "evidence": (
                    "the s3:// URI is an EXACT IDENTITY a consumer can equality-join, not a "
                    "description. ⛔ COPIED BYTE-FOR-BYTE from the cells carrier's own cell "
                    "%s-4 and never retyped from a display -- on card 3 a uuid tail "
                    "reconstructed from a truncated print was wrong in its LAST character and "
                    "returned KeyCount=0, which reads exactly like a vanished table. Existence "
                    "at this exact key was then MEASURED: KeyCount=%d. The wrong-prefix probe "
                    "run here mutates this home's own uuid tail and returns rc=%s out=%r, "
                    "confirming that a near-miss on this key is indistinguishable from absence "
                    "by KeyCount alone."
                    % (GROUPS["cse_test_24458e6c"], kc, wrong_prefix[0], wrong_prefix[1])),
                "owner": LANE,
            },
        },
        "trust": {
            "coverage": {
                "universe": ("the objects under THIS table's own S3 home -- not the CSE event "
                             "population, not the production cse store, and not the same-named "
                             "sibling cse_test_bb57a916"),
                "denominator": "%d of %d objects at the declared home" % (lay["objects"],
                                                                         lay["objects"]),
                "explicitly_out": [
                    "%s -- the same-named sibling: a SEPARATE subject with its own card (card 6 "
                    "of this face), %d objects, measured here ONLY as the discrimination control"
                    % (sib_uri, sib["objects"]),
                    "row-level content -- no row was read. Whether these rows duplicate the "
                    "production cse store's is UNMEASURED, so authority_role=`source` describes "
                    "this table holding its own rows, not a claim that they are unique",
                    "the Nessie catalog plane -- not reachable from this seat; see the key row"],
                "basis": "measured",
                "evidence": ("aws s3api list-objects-v2 auto-paginated, rows counted CLIENT-SIDE "
                             "-- never --query length(), which returns the PAGE count, and never "
                             "--no-paginate. %d objects, %d bytes, segments %s. The denominator "
                             "certifies the SWEEP of this prefix, not the correctness of the "
                             "prefix; the prefix is certified separately by the copied-home "
                             "evidence in the location row."
                             % (lay["objects"], lay["bytes"], lay["by_segment"])),
                "owner": LANE,
            },
            "key": {
                "identity_space": ("S3 (bucket, key) on the artifact plane; (namespace, table) = "
                                   "(globgrph, cse_test) on the Nessie catalog plane"),
                "key_expression": "bucket + key, exact string match",
                "key_is_stable": "stable",
                "crosses_spaces": True,
                "declared_mapping": ("the catalog key (globgrph, `cse_test`) does NOT uniquely "
                                     "address this home -- two homes carry that table name"),
                "basis": "inferred",
                "basis_by_field": {
                    "identity_space": "measured",
                    "key_expression": "measured",
                    "key_is_stable": "measured",
                    "crosses_spaces": "measured",
                    "declared_mapping": "inferred",
                },
                "evidence": (
                    "⛔ THE FINDING IN THIS CARD, AND IT IS `inferred` ON PURPOSE. MEASURED: "
                    "two S3 homes exist under warehouse/globgrph/ whose table-name component is "
                    "identically `cse_test`, differing only in uuid -- this one (%s, written %s) "
                    "and %s (written %s). Their key sets are disjoint. INFERRED: pyiceberg/Nessie "
                    "assigns a NEW uuid-suffixed location on each create_table, and a namespace "
                    "admits one table per name, so two locations for one name is consistent with "
                    "a create -> drop -> create cycle in which at most ONE of these homes is "
                    "still reachable by the catalog key and the other is an ORPHANED physical "
                    "location. ⛔ UNMEASURED, AND IT IS THE DECIDING FACT: which home the "
                    "catalog resolves to today, or whether either is still registered. The "
                    "Nessie catalog is not reachable from this seat, so this card CANNOT say "
                    "which of the two is live and does not guess. Settling it needs one "
                    "catalog.load_table((globgrph, 'cse_test')) read of its metadata location. "
                    "⛔ THIS CARD DOES NOT CLASSIFY THE ORPHAN AS A DEFECT -- naming it is "
                    "the carder's job, deciding it is the owner's."
                    % ("24458e6c", lay["first_write"][:10], "bb57a916", sib["first_write"][:10])),
                "owner": LANE,
            },
            "failure_mode": {
                "returns_on_failure": ("A true absence returns KeyCount=0 at rc=0 -- a failed "
                                       "retrieval returns a VALUE, not an error. And at THIS "
                                       "subject a wrong home does not even return 0: the "
                                       "same-named sibling returns a populated census"),
                "distinguishable_from_true_negative": "no",
                "basis": "inferred",
                "basis_by_field": {
                    "returns_on_failure": "measured",
                    "distinguishable_from_true_negative": "inferred",
                },
                "evidence": (
                    "FOUR read-only probe classes, each a SEPARATE invocation, rc read UNPIPED. "
                    "MEASURED: (1) true absence -- real bucket, bogus prefix -> rc=%s out=%r; "
                    "(2) wrong bucket -> rc=%s out=%r, an ERROR, not a zero; (3) wrong region -> "
                    "rc=%s out=%r; (4) near-miss prefix, this home's own uuid tail mutated -> "
                    "rc=%s out=%r. So among the exercised classes a zero is produced by absence "
                    "and by a wrong prefix, and NOT by a wrong bucket. ⛔ THE FIFTH CLASS -- "
                    "a missing s3:ListBucket -- WAS NOT EXERCISED and may also return a zero; "
                    "that unexercised class is the SOLE ground on which "
                    "distinguishable_from_true_negative is `no` at basis `inferred`. An unscoped "
                    "'only a true absence produces a zero' would contradict this same row. "
                    "⛔ AND AT THIS SUBJECT THE SHARPEST FAILURE IS NOT A ZERO AT ALL: "
                    "because the sibling home is real and populated, a home confused between the "
                    "two returns a healthy KeyCount=1 and a full census, so every arm passes "
                    "while the card describes the wrong table. That class is caught "
                    "structurally by refuse_sibling_confusion() at build time, not by reading a "
                    "count."
                    % (zc["true_absence"][0], zc["true_absence"][1],
                       zc["wrong_bucket"][0], zc["wrong_bucket"][1][:60],
                       zc["wrong_region"][0], zc["wrong_region"][1],
                       wrong_prefix[0], wrong_prefix[1])),
                "owner": LANE,
            },
        },
        "verdict": {
            "standing": "QUALIFIED",
            "why": (
                "NOT LOAD-BEARING, on the evidence gathered here: an isolated test-harness table "
                "whose SURVIVING objects were written in a single %d-second append on %s with "
                "no later surviving write, %d days stale at carding. It is carded because it EXISTS in the manifest and consumes a "
                "real S3 home, not because anything was shown to read it. QUALIFIED, and these "
                "are the qualifications: the materializer is `inferred` -- the invocation that "
                "created this table was never found, and the partition-spec match identifies a "
                "writer CLASS, not a run; the `key` row carries an UNRESOLVED identity question, "
                "since two homes share the table name `cse_test` and this seat cannot reach the "
                "Nessie catalog to say which one it addresses -- so one of the two may be an "
                "orphaned location and this card does not claim which; coverage spans the OBJECT "
                "plane only and NO row was read, so whether this table's rows duplicate the "
                "production cse store's is UNMEASURED; and whether any consumer reads it, or is "
                "harmed by it existing, is UNMEASURED here. ⛔ THIS CARD DOES NOT CLASSIFY "
                "THE TABLE AS DEBT AND DOES NOT PROPOSE DROPPING IT: --drop permits it and the "
                "production guard would refuse the real log, but that is a permission, not a "
                "recommendation. Naming the state is the carder's job; deciding it is the "
                "owner's."
                % ((datetime.strptime(lay["last_write"][:19], "%Y-%m-%dT%H:%M:%S")
                    - datetime.strptime(lay["first_write"][:19], "%Y-%m-%dT%H:%M:%S")).seconds,
                   lay["first_write"][:10], age)),
            "blocking_defects": None,
        },
        "forward_disposition": {
            "standing": "undecided",
            "set_by": None,
            "basis": "absent",
            "evidence": ("NOT SET BY THE CARDING LANE -- the store owner's call at the class "
                         "close. The key row's unresolved catalog question is an input that "
                         "owner will want settled first."),
            "decided_utc": None,
        },
        "carded_by": LANE,
    }


def card_cse_test_bb57a916():
    """Card 6. ⛔ RE-MEASURED AT ITS OWN SUBSTRATE, NEVER DERIVED FROM CARD 5.

    1.0.0_SA_CTO~X named this pair as the place a card gets copied instead of measured, and added
    that if card 6 came out byte-similar to card 5 the similarity would be a FINDING to state
    rather than a confirmation to rest on. It did not: the two tables share a table NAME and
    almost nothing else. Every figure below comes from this home's own live read.
    """
    home = HOMES["cse_test_bb57a916"]
    sib_home = HOMES["cse_test_24458e6c"]
    home_uri = "s3://%s/%s" % (BUCKET, home)
    sib_uri = "s3://%s/%s" % (BUCKET, sib_home)
    kc = key_count(home)
    cen = object_census(home)
    lay = _iceberg_layout(home)
    sib = _iceberg_layout(sib_home)
    refuse_sibling_confusion(lay, sib)
    zc = zero_class_probes(home)
    wrong_prefix = probe("s3api", "list-objects-v2", "--bucket", BUCKET, "--prefix",
                         home[:-2] + "f/", "--max-keys", "1", "--query", "KeyCount",
                         "--output", "text")
    cells = carrier_cells(GROUPS["cse_test_bb57a916"])
    writer = "infra/aws/globgrph/cse_store.py"
    wpin = git_pin(writer)
    newest = datetime.strptime(cen["newest_utc"][:19], "%Y-%m-%dT%H:%M:%S").replace(
        tzinfo=timezone.utc)
    age = (datetime.now(timezone.utc) - newest).days
    span = (datetime.strptime(lay["last_write"][:19], "%Y-%m-%dT%H:%M:%S")
            - datetime.strptime(lay["first_write"][:19], "%Y-%m-%dT%H:%M:%S")).seconds

    return {
        "schema_version": 3.1,
        "subject": {
            "id": "cse_test_bb57a916",
            "kind": "store",
            "declared_domain": (
                "An ISOLATED TEST-HARNESS Iceberg table in the globgrph Nessie namespace holding "
                "CSE (Change/Signal Event) rows partitioned by (source, event_date). Its "
                "SURVIVING objects were written by THREE appends inside one %d-minute "
                "session and carry no later surviving write. "
                "⛔ THE SUBJECT IS THE TABLE AT THIS EXACT S3 HOME (uuid bb57a916-76de-454d-a71e-"
                "932dc173620e). It is NOT the production `cse` store and it is NOT its same-named "
                "sibling cse_test_24458e6c, which is a DIFFERENT table carrying the SAME table "
                "name `cse_test` and is distinguished only by uuid. "
                "QUALIFIES THE CELLS CARRIER (AC4): %s @%s, cells %s -- the carrier is NOT edited."
                % (span // 60, CARRIER, CARRIER_PIN,
                   " ".join(c["cell_id"] for c in cells))),
        },
        "as_of": {
            "carded_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "commit_ish": subprocess.run(["git", "rev-parse", "HEAD"],
                                         capture_output=True, text=True).stdout.strip(),
            "graph_vintage": "S3 object plane read live at card time for this home AND for the "
                             "same-named sibling used as the discrimination control; no graph "
                             "consulted",
        },
        "process": {
            "methodology": {
                "how": ("Iceberg create_table plus THREE appends through cse_store.py's "
                        "unconstrained --table override: ensure_cse_table() creates "
                        "globgrph.<table> with cse_iceberg_schema() partitioned by "
                        "(source, event_date), and each append writes one Nessie commit. "
                        "⛔ THE INVOCATIONS THAT DID THIS WERE NOT FOUND AND ARE NOT CLAIMED."),
                "determinism": "deterministic",
                "composes": [
                    {"id": writer + " @" + wpin[:10],
                     "note": "the code path that can create and append to this table: --table at "
                             ":581 carries no choices= so it accepts any name in the namespace; "
                             "ensure_cse_table() at :321, catalog.create_table at :338; the "
                             "docstring at :325 invites exactly this -- 'pass a scratch name "
                             "(e.g. cse_test) for an ISOLATED test harness'"}],
                "invents": [],
                "materializer_standing": "historical_in_use",
                "basis": "inferred",
                "basis_by_field": {
                    "how": "inferred",
                    "composes": "inferred",
                    "determinism": "inferred",
                    "materializer_standing": "measured",
                },
                "evidence": (
                    "⛔ THE ROW IS `inferred` AND THE SENTENCE MUST NOT OUTRUN IT. "
                    "generation.materializer is null in the manifest and NO code names this "
                    "table; the invocations were not found and none is claimed. The MEASURED "
                    "facts sit UNDER that floor and do not raise it: the layout matches "
                    "cse_store.py's declared partition spec -- %d data objects under "
                    "source=doc/ and source=git/ across %d event_date partitions (%s..%s), which "
                    "is the (source, event_date) spec ensure_cse_table() applies at %s:321/338 "
                    "@%s. A structural match to a writer's partition spec identifies the writer "
                    "CLASS, never the run. materializer_standing is `historical_in_use` "
                    "(MEASURED): %d snapshots and %d distinct write-commit uuids SURVIVE here, so "
                    "the writer ran and has not run again IN THE SURVIVING RECORD -- which is "
                    "not the same as never, and the lifetime count is UNMEASURED."
                    % (lay["by_segment"].get("data", 0), lay["event_date_partitions"],
                       lay["event_date_range"][0], lay["event_date_range"][1],
                       writer, wpin[:10], lay["snapshots"],
                       len(lay["write_commit_uuids"]))),
                "owner": LANE,
            },
            "cadence": {
                "declared_rhythm": "NONE DECLARED -- generation.trigger is null in the manifest",
                "actual_trigger": ("none found; and the SURVIVING write history is a SESSION, "
                                   "not a schedule -- three appends inside %d minutes with no "
                                   "later surviving write; lifetime count UNMEASURED"
                                   % (span // 60)),
                "live_matches_declared": "not_applicable",
                "live_instance_age": ("%d objects written between %s and %s -- a %d-second span "
                                      "on %d distinct write-day across %d appends; %d days stale "
                                      "at carding"
                                      % (lay["objects"], lay["first_write"], lay["last_write"],
                                         span, lay["distinct_write_days"],
                                         len(lay["write_commit_uuids"]), age)),
                "basis": "absent",
                "basis_by_field": {
                    "declared_rhythm": "absent",
                    "actual_trigger": "measured",
                    "live_instance_age": "measured",
                    "live_matches_declared": "absent",
                },
                "evidence": (
                    "⛔ TWO DIFFERENT CLAIMS LIVE IN THIS ROW AND THEY DO NOT SHARE A BASIS, SO "
                    "THE ROW BASIS IS THE FLOOR OF ITS FIELDS -- `absent` -- WEAKER THAN ITS "
                    "STRONGEST FIELD ON PURPOSE. (1) `declared_rhythm` floors to `absent`: "
                    "generation.trigger is an UNPOPULATED field, and an unpopulated field is not "
                    "a measured negative. (2) `actual_trigger` is MEASURED and the discriminator "
                    "is the Iceberg metadata tree, not the timestamps: %d snapshot objects and "
                    "%d distinct write-commit uuids (%s) across %d objects, so this table was "
                    "written by THREE appends, not one. ⛔ SCOPED TO THE SURVIVING SET AND NOT "
                    "BEYOND IT -- snapshot expiry and overwrite both converge on fewer surviving "
                    "snapshots, so 'exactly three writes ever' would need the metadata log's "
                    "snapshot HISTORY rather than its current head, and that is UNMEASURED. "
                    "Three appends inside %d minutes followed by %d days of silence is a SESSION "
                    "that ended, which is a different shape from a cadence that failed, and "
                    "neither becomes the other by ageing. ⛔ WHY the session happened, and "
                    "whether anyone intended it to repeat, is UNMEASURED."
                    % (lay["snapshots"], len(lay["write_commit_uuids"]),
                       ", ".join(lay["write_commit_uuids"]), lay["objects"], span // 60, age)),
                "owner": LANE,
            },
        },
        "artifact": {
            "persistence": {
                "persisted": True,
                "authority_role": "source",
                "mutation_policy": "append_only",
                "form": ("an Iceberg table: %d data parquet under data/source=doc/ and "
                         "data/source=git/ plus a %d-object metadata/ tree (4 *.metadata.json, "
                         "3 -m0.avro manifests, 3 snap-*.avro snapshots)"
                         % (lay["by_segment"].get("data", 0),
                            lay["by_segment"].get("metadata", 0))),
                "basis": "measured",
                "evidence": (
                    "KeyCount at the declared home = %d, a POSITIVE, which a wrong bucket or a "
                    "missing s3:ListBucket cannot produce. Controls as SEPARATE invocations: "
                    "POSITIVE prefix 'warehouse/' -> 1; NEGATIVE prefix "
                    "'warehouse/globgrph/zzz_no_such_prefix_99999/' -> 0. Both fired. Segment "
                    "split counted client-side: %s. ⛔ NOTE THE INVERTED RATIO against this "
                    "table's same-named sibling -- %d metadata objects to %d data objects here, "
                    "because three appends each leave a metadata.json, a manifest and a "
                    "snapshot. `mutation_policy` is `append_only`; DROPPABILITY IS A LIFECYCLE "
                    "FACT RECORDED HERE, NOT AN ENUM VALUE: ensure_cse_table() is ENSURE-ONLY "
                    "and never overwrites or repartitions (%s:321-325 @%s), while --drop at :579 "
                    "explicitly permits dropping a SCRATCH table and 'refuses the real log'. "
                    "This table is on the permitted side of that guard; whether it SHOULD be "
                    "dropped is the owner's call and is not set here."
                    % (kc, lay["by_segment"], lay["by_segment"].get("metadata", 0),
                       lay["by_segment"].get("data", 0), writer, wpin[:10])),
                "owner": LANE,
            },
            "location": {
                "home": home_uri,
                "projection_of": [],
                "co_resident_stores": [
                    {"id": sib_uri,
                     "note": "⛔ THE SAME-NAMED SIBLING and the subject of card 5 of this face. "
                             "Shares the table name `cse_test`; differs only in uuid. MEASURED "
                             "disjoint from this home: %d objects / %d bytes there against %d / "
                             "%d here, key-set intersection 0."
                             % (sib["objects"], sib["bytes"], lay["objects"], lay["bytes"])},
                    {"id": "s3://%s/warehouse/globgrph/" % BUCKET,
                     "note": "the globgrph warehouse prefix root, shared with every sibling "
                             "table; overlap of CONTENT was not measured, only of PREFIX"}],
                "basis": "measured",
                "evidence": (
                    "the s3:// URI is an EXACT IDENTITY a consumer can equality-join, not a "
                    "description. ⛔ COPIED BYTE-FOR-BYTE from the cells carrier's own cell "
                    "%s-4 and never retyped from a display. Existence at this exact key was "
                    "MEASURED: KeyCount=%d. The wrong-prefix probe mutates this home's own uuid "
                    "tail and returns rc=%s out=%r, confirming a near-miss on this key is "
                    "indistinguishable from absence by KeyCount alone."
                    % (GROUPS["cse_test_bb57a916"], kc, wrong_prefix[0], wrong_prefix[1])),
                "owner": LANE,
            },
        },
        "trust": {
            "coverage": {
                "universe": ("the objects under THIS table's own S3 home -- not the CSE event "
                             "population, not the production cse store, and not the same-named "
                             "sibling cse_test_24458e6c"),
                "denominator": "%d of %d objects at the declared home" % (lay["objects"],
                                                                          lay["objects"]),
                "explicitly_out": [
                    "%s -- the same-named sibling, a SEPARATE subject carded as card 5 of this "
                    "face, %d objects, measured here ONLY as the discrimination control"
                    % (sib_uri, sib["objects"]),
                    "row-level content -- no row was read. Whether these rows duplicate the "
                    "production cse store's is UNMEASURED, so authority_role=`source` describes "
                    "this table holding its own rows, not a claim they are unique",
                    "the Nessie catalog plane -- not reachable from this seat; see the key row"],
                "basis": "measured",
                "evidence": ("aws s3api list-objects-v2 auto-paginated, rows counted "
                             "CLIENT-SIDE -- never --query length(), which returns the PAGE "
                             "count, and never --no-paginate. %d objects, %d bytes, segments %s. "
                             "The denominator certifies the SWEEP of this prefix, not the "
                             "correctness of the prefix; the prefix is certified separately by "
                             "the copied-home evidence in the location row."
                             % (lay["objects"], lay["bytes"], lay["by_segment"])),
                "owner": LANE,
            },
            "key": {
                "identity_space": ("S3 (bucket, key) on the artifact plane; (namespace, table) = "
                                   "(globgrph, cse_test) on the Nessie catalog plane"),
                "key_expression": "bucket + key, exact string match",
                "key_is_stable": "stable",
                "crosses_spaces": True,
                "declared_mapping": ("the catalog key (globgrph, `cse_test`) does NOT uniquely "
                                     "address this home -- two homes carry that table name"),
                "basis": "inferred",
                "basis_by_field": {
                    "identity_space": "measured",
                    "key_expression": "measured",
                    "key_is_stable": "measured",
                    "crosses_spaces": "measured",
                    "declared_mapping": "inferred",
                },
                "evidence": (
                    "⛔ THE SAME UNRESOLVED IDENTITY QUESTION CARD 5 CARRIES, AND IT IS `inferred` "
                    "FROM THIS SIDE TOO. MEASURED: two S3 homes exist under warehouse/globgrph/ "
                    "whose table-name component is identically `cse_test`, differing only in "
                    "uuid -- this one (bb57a916, written %s) and card 5's (24458e6c, written %s). "
                    "Key sets disjoint. INFERRED: pyiceberg/Nessie assigns a NEW uuid-suffixed "
                    "location per create_table and a namespace admits one table per name, so at "
                    "most ONE of these homes is reachable by the catalog key and the other is an "
                    "ORPHANED physical location. ⛔ UNMEASURED, AND IT IS THE DECIDING FACT: "
                    "which home the catalog resolves to today. The Nessie catalog is not "
                    "reachable from this seat, so this card CANNOT say which of the two is live "
                    "and does not guess -- and it does NOT inherit card 5's reading, which is "
                    "the same non-answer reached independently rather than a second vote. "
                    "⛔ ONE ORDERING FACT THIS SIDE ADDS, MEASURED: this home's writes "
                    "(%s) PRECEDE the sibling's (%s) on the same day. That constrains WHICH "
                    "would be the orphan under the create->drop->create reading -- an earlier "
                    "location is the one a later create would strand -- but it does NOT settle "
                    "it, because nothing measured here excludes the reverse order of catalog "
                    "registration. Settling it needs one catalog.load_table((globgrph, "
                    "'cse_test')) read of its metadata location. NAMING the state is the "
                    "carder's job; DECIDING it is the owner's."
                    % (lay["first_write"][:10], sib["first_write"][:10],
                       lay["first_write"][11:19], sib["first_write"][11:19])),
                "owner": LANE,
            },
            "failure_mode": {
                "returns_on_failure": ("A true absence returns KeyCount=0 at rc=0 -- a failed "
                                       "retrieval returns a VALUE, not an error. And at THIS "
                                       "subject a wrong home does not even return 0: the "
                                       "same-named sibling returns a populated census"),
                "distinguishable_from_true_negative": "no",
                "basis": "inferred",
                "basis_by_field": {
                    "returns_on_failure": "measured",
                    "distinguishable_from_true_negative": "inferred",
                },
                "evidence": (
                    "FOUR read-only probe classes, each a SEPARATE invocation, rc read UNPIPED. "
                    "MEASURED: (1) true absence -> rc=%s out=%r; (2) wrong bucket -> rc=%s "
                    "out=%r, an ERROR not a zero; (3) wrong region -> rc=%s out=%r; (4) "
                    "near-miss prefix, this home's own uuid tail mutated -> rc=%s out=%r. So a "
                    "zero is produced by absence and by a wrong prefix, and NOT by a wrong "
                    "bucket. ⛔ THE FIFTH CLASS -- a missing s3:ListBucket -- WAS NOT EXERCISED "
                    "and may also return a zero; that unexercised class is the SOLE ground on "
                    "which distinguishable_from_true_negative is `no` at basis `inferred`. "
                    "⛔ AND AT THIS SUBJECT THE SHARPEST FAILURE IS NOT A ZERO: because the "
                    "same-named sibling home is real and populated, a home confused between the "
                    "two returns a healthy KeyCount=1 and a full census while the card describes "
                    "the wrong table. That class is caught structurally by "
                    "refuse_sibling_confusion() at build time, which RAISED nothing here because "
                    "the two censuses differ on every axis measured (see the location row)."
                    % (zc["true_absence"][0], zc["true_absence"][1],
                       zc["wrong_bucket"][0], zc["wrong_bucket"][1][:60],
                       zc["wrong_region"][0], zc["wrong_region"][1],
                       wrong_prefix[0], wrong_prefix[1])),
                "owner": LANE,
            },
        },
        "verdict": {
            "standing": "QUALIFIED",
            "why": (
                "NOT LOAD-BEARING on the evidence gathered here: an isolated test-harness table "
                "whose SURVIVING objects were written by %d appends inside %d minutes on %s "
                "with no later surviving write, %d days stale at carding. It is carded because it EXISTS in the manifest and occupies a "
                "real S3 home, not because anything was shown to read it. QUALIFIED, and these "
                "are the qualifications: the materializer is `inferred` -- the invocations were "
                "never found and the partition-spec match identifies a writer CLASS, not a run; "
                "the `key` row carries an UNRESOLVED identity question, since two homes share "
                "the table name `cse_test` and this seat cannot reach the Nessie catalog to say "
                "which one it addresses, so one of the two may be an orphaned location and this "
                "card does not claim which; coverage spans the OBJECT plane only and NO row was "
                "read; and whether any consumer reads this table is UNMEASURED. "
                "⛔ THIS CARD DOES NOT CLASSIFY THE TABLE AS DEBT AND DOES NOT PROPOSE DROPPING "
                "IT: --drop permits it, but a permission is not a recommendation. Naming the "
                "state is the carder's job; deciding it is the owner's."
                % (len(lay["write_commit_uuids"]), span // 60, lay["first_write"][:10], age)),
            "blocking_defects": None,
        },
        "forward_disposition": {
            "standing": "undecided",
            "set_by": None,
            "basis": "absent",
            "evidence": ("NOT SET BY THE CARDING LANE -- the store owner's call at the class "
                         "close. The key row's unresolved catalog question is an input that "
                         "owner will want settled first, and it is shared with card 5."),
            "decided_utc": None,
        },
        "carded_by": LANE,
    }


BUILDERS = {"cse": card_cse, "code_heat_snap": card_code_heat_snap,
            "fedobs_coevolution_snap": card_fedobs_coevolution_snap,
            "fedobs_coverage_snap": card_fedobs_coverage_snap,
            "cse_test_24458e6c": card_cse_test_24458e6c,
            "cse_test_bb57a916": card_cse_test_bb57a916}


def main():
    want = sys.argv[1] if len(sys.argv) > 1 else "all"
    todo = list(BUILDERS) if want == "all" else [want]
    for name in todo:
        if name not in BUILDERS:
            raise SystemExit("no builder for %r (have: %s)" % (name, ", ".join(BUILDERS)))
        doc = BUILDERS[name]()
        refuse_prose_basis_mismatch(doc)
        refuse_prose_enum_mismatch(doc)
        refuse_unscoped_lifetime_claim(doc)
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
