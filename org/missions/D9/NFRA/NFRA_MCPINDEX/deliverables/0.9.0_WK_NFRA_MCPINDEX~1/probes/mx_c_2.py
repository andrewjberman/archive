#!/usr/bin/env python3
"""MX-c-2 probe -- the catalog schema extended to silver datasets, one source file per
entry, through the one writer. Invoked as `py -3.12 probes/mx_c_2.py AC<n>` from <WS>
(cwd == the repository root, per the task order's invocation line -- REPO below relies on
that). Each AC function prints its measurement with instrument + denominator, then exactly
one line: `VERDICT: PASS-MXC2-AC<n>` or `VERDICT: FAIL-MXC2-AC<n> <reason>`.
"""
from __future__ import annotations

import fnmatch
import io
import os
import re
import subprocess
import sys
import tempfile

REPO = os.getcwd()
EMIT_PY = os.path.join(REPO, "workflows", "atom_decomposition", "emit_catalog_v02.py")
VALIDATE_PY = os.path.join(REPO, "workflows", "atom_decomposition", "validate_catalog_v02.py")
BATTERY_PY = os.path.join(REPO, "workflows", "atom_decomposition", "battery_catalog_v02.py")
CAT_PATH = os.path.join(REPO, "infra", "aws", "ec2", "opal-gateway", "app", "refs", "DATA_CATALOG.yaml")
REAL_ENTRIES_DIR = os.path.join(REPO, "workflows", "atom_decomposition", "catalog_entries")
VALIDATION_REPORT = os.path.join(REPO, "workflows", "atom_decomposition", "catalog_v02", "validation_report.json")
CUT_HEAD = "41da358d45"   # this worker's identity-line cut head (org/missions/.../TO-MX-c-2 <WS> cut)

sys.path.insert(0, os.path.join(REPO, "workflows", "atom_decomposition"))
import yaml  # noqa: E402
import emit_catalog_v02 as emit  # noqa: E402
import validate_catalog_v02 as validate  # noqa: E402

VALID_ENTRY = {
    "business_meaning": "per-account daily position snapshots for the Black Diamond silver tier",
    "example_questions": ["what positions does account X hold today?"],
    "grain": "date",
    "freshness_field": "FIELD:as_of_date",
    "firm_scope_rule": "firm-scoped",
    "never_sum_rules": ["never sum position market_value across accounts of different firms"],
    "producer": "data/black_diamond/scripts/silver/positions.py",
    "tools": ["bd_positions_query"],
}


def run(cmd, timeout=100):
    p = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True, timeout=timeout)
    return p.returncode, p.stdout, p.stderr


def verdict(cid, passed, reason=""):
    if passed:
        print("VERDICT: PASS-%s" % cid)
    else:
        print("VERDICT: FAIL-%s %s" % (cid, reason))


# ---------------------------------------------------------------------------------------

def ac1():
    print("=== MXC2-AC1: the entry schema carries exactly the C1 fields, each typed ===")
    fields = emit.ENTRY_REQUIRED_FIELDS
    expected = ("business_meaning", "example_questions", "grain", "freshness_field",
                "firm_scope_rule", "never_sum_rules", "producer", "tools")
    print("ENTRY_REQUIRED_FIELDS (%d): %s" % (len(fields), fields))
    ok_shape = fields == expected
    print("matches C1's 8 named fields exactly (business meaning, example questions, grain,"
          " freshness field, firm-scope rule, never-sum rules, producer, tools): %s" % ok_shape)

    valid_errs = emit.validate_entry("probe-valid", VALID_ENTRY)
    ok_valid = valid_errs == []
    print("fully valid synthetic entry -> errors=%r (expect [])" % valid_errs)

    denom = 0
    per_field = []
    for field in fields:
        denom += 1
        bad = dict(VALID_ENTRY)
        del bad[field]
        errs = emit.validate_entry("probe", bad)
        hit = bool(errs) and any(field in e for e in errs)
        per_field.append((field, hit))
    per_field_ok = all(h for _, h in per_field)
    print("per-field type enforcement, denominator %d of %d C1 fields, each individually dropped: %s"
          % (sum(1 for _, h in per_field if h), denom, per_field))

    extra_errs = emit.validate_entry("probe", dict(VALID_ENTRY, unexpected_field="x"))
    ok_extra = any("unexpected field" in e for e in extra_errs)
    print("an extra (9th) field is refused, keeping the schema at EXACTLY 8: %s (%r)" % (ok_extra, extra_errs))

    passed = ok_shape and ok_valid and per_field_ok and denom == 8 and ok_extra
    verdict("MXC2-AC1", passed, "" if passed else "schema/type enforcement incomplete")


def ac2():
    print("=== MXC2-AC2: a dataset entry is ONE source file under catalog_entries/, and the emitter reads that directory ===")
    resolved = os.path.normpath(emit.CATALOG_ENTRIES_DIR)
    expected = os.path.normpath(REAL_ENTRIES_DIR)
    print("emit_catalog_v02.CATALOG_ENTRIES_DIR resolves to: %s" % resolved)
    print("expected (workflows/atom_decomposition/catalog_entries): %s" % expected)
    ok_path = resolved == expected
    ok_dir_exists = os.path.isdir(expected)
    print("directory exists on disk: %s" % ok_dir_exists)

    # in-process exercise against a TEMP override -- never touches the real tracked directory.
    old = emit.CATALOG_ENTRIES_DIR
    try:
        with tempfile.TemporaryDirectory() as tmp:
            emit.CATALOG_ENTRIES_DIR = tmp
            before_entries, before_errors = emit.load_catalog_entries()
            print("temp dir, zero files -> entries=%r errors=%r" % (before_entries, before_errors))
            with io.open(os.path.join(tmp, "probe_dataset.yaml"), "w", encoding="utf-8") as f:
                yaml.safe_dump(VALID_ENTRY, f)
            after_entries, after_errors = emit.load_catalog_entries()
            print("ONE file planted -> entries=%s errors=%r" % (sorted(after_entries), after_errors))
    finally:
        emit.CATALOG_ENTRIES_DIR = old

    ok_read = (before_entries == {} and before_errors == {} and
               set(after_entries) == {"probe_dataset"} and after_errors == {})
    passed = ok_path and ok_dir_exists and ok_read
    verdict("MXC2-AC2", passed, "" if passed else "directory resolution or read mechanism wrong")


def ac3():
    print("=== MXC2-AC3 (difference): planted entry -> emitter gains it, validator passes;"
          " same file missing one field -> validator REFUSES, names the field ===")
    plant_path = os.path.join(REAL_ENTRIES_DIR, "_probe_ac3_plant.yaml")
    if os.path.exists(plant_path):
        print("NOTE: stale plant file from a prior interrupted run -- removing before starting")
        os.remove(plant_path)
    cat_before = io.open(CAT_PATH, encoding="ascii").read()
    ok = True
    reasons = []
    try:
        # ---- engaged arm: fully valid plant ----
        with io.open(plant_path, "w", encoding="utf-8") as f:
            yaml.safe_dump(VALID_ENTRY, f)
        rc, out, err = run([sys.executable, EMIT_PY])
        print("EMITTER RUN (valid plant) rc=%d" % rc)
        print(out[-1500:])
        cat_after = io.open(CAT_PATH, encoding="ascii").read()
        doc_before = yaml.safe_load(cat_before)
        doc_after = yaml.safe_load(cat_after)
        channels_unchanged = doc_before.get("channels") == doc_after.get("channels")
        silver_before = doc_before.get("silver_datasets")
        silver_after = doc_after.get("silver_datasets")
        gained_exactly_one = (
            isinstance(silver_after, list) and len(silver_after) == 1
            and silver_after[0].get("entity") == "_probe_ac3_plant"
            and all(silver_after[0].get(f) == VALID_ENTRY[f] for f in emit.ENTRY_REQUIRED_FIELDS)
        )
        print("channels: unchanged=%s | silver_datasets before=%r after=%r"
              % (channels_unchanged, silver_before, silver_after))
        if not (rc == 0 and channels_unchanged and gained_exactly_one):
            ok = False
            reasons.append("engaged-arm emit did not gain exactly the planted entry (rc=%d channels_unchanged=%s gained_exactly_one=%s)"
                            % (rc, channels_unchanged, gained_exactly_one))

        silver_errors = validate.validate_silver_entries()
        print("validator (schema pass) on the valid plant -> errors=%r" % silver_errors)
        if silver_errors:
            ok = False
            reasons.append("validator refused a fully valid planted entry: %r" % silver_errors)

        # ---- disengaged arm: same file, missing one field (producer) ----
        broken = dict(VALID_ENTRY)
        del broken["producer"]
        with io.open(plant_path, "w", encoding="utf-8") as f:
            yaml.safe_dump(broken, f)
        silver_errors2 = validate.validate_silver_entries()
        print("validator (schema pass) on the SAME file missing 'producer' -> errors=%r" % silver_errors2)
        names_field = ("_probe_ac3_plant" in silver_errors2
                        and any("producer" in e for e in silver_errors2["_probe_ac3_plant"]))
        if not names_field:
            ok = False
            reasons.append("validator did not REFUSE-and-name 'producer' for the broken plant: %r" % silver_errors2)
    finally:
        if os.path.exists(plant_path):
            os.remove(plant_path)
        rc_restore, out_restore, _err_restore = run([sys.executable, EMIT_PY])
        cat_restored = io.open(CAT_PATH, encoding="ascii").read()
        restored_ok = cat_restored == cat_before
        print("RESTORE: plant removed, emitter re-run rc=%d, CAT restored to its pre-probe bytes: %s"
              % (rc_restore, restored_ok))
        if not restored_ok:
            ok = False
            reasons.append("CAT was not restored to its pre-probe state after cleanup")

    verdict("MXC2-AC3", ok, "; ".join(reasons))


def ac4():
    print("=== MXC2-AC4: the 36 existing rows across 15 channels re-emit with every field unchanged ===")
    rc, out, err = run(["git", "show", "%s:infra/aws/ec2/opal-gateway/app/refs/DATA_CATALOG.yaml" % CUT_HEAD])
    if rc != 0:
        verdict("MXC2-AC4", False, "could not read the cut-head baseline via git show (rc=%d): %s" % (rc, err[:200]))
        return
    orig = yaml.safe_load(out)
    cur = yaml.safe_load(io.open(CAT_PATH, encoding="ascii").read())
    orig_ch = orig.get("channels", {})
    cur_ch = cur.get("channels", {})
    total_rows = sum(len(c.get("artifacts") or []) for c in orig_ch.values())
    print("BASELINE (git show @%s) denominator: %d channels, %d artifact rows" % (CUT_HEAD, len(orig_ch), total_rows))

    diffs = []
    checked_rows = 0
    for ch_name, ch_body in orig_ch.items():
        cur_body = cur_ch.get(ch_name)
        if cur_body is None:
            diffs.append("channel %s MISSING after re-emit" % ch_name)
            continue
        for k in ch_body:
            if k == "artifacts":
                continue
            if cur_body.get(k) != ch_body.get(k):
                diffs.append("%s.%s changed" % (ch_name, k))
        orig_rows = {r["entity"]: r for r in (ch_body.get("artifacts") or [])}
        cur_rows = {r["entity"]: r for r in (cur_body.get("artifacts") or [])}
        for eid, orow in orig_rows.items():
            checked_rows += 1
            crow = cur_rows.get(eid)
            if crow is None:
                diffs.append("%s/%s row MISSING after re-emit" % (ch_name, eid))
                continue
            if orow != crow:
                for f in sorted(set(orow) | set(crow)):
                    if orow.get(f) != crow.get(f):
                        diffs.append("%s/%s.%s: %r -> %r" % (ch_name, eid, f, orow.get(f), crow.get(f)))

    EXCEPT_TOP = ("version", "built_at_git_head")
    top_diffs = [k for k in set(orig) | set(cur)
                 if k not in EXCEPT_TOP and k != "silver_datasets" and orig.get(k) != cur.get(k)]
    print("CHECKED: %d of %d rows across %d of %d channels; field-level diffs: %d"
          % (checked_rows, total_rows, len(orig_ch), len(orig_ch), len(diffs)))
    for d in diffs[:60]:
        print("  DIFF: " + d)
    print("TOP-LEVEL fields EXCEPTED (version and build-head): orig=%s cur=%s"
          % ({k: orig.get(k) for k in EXCEPT_TOP}, {k: cur.get(k) for k in EXCEPT_TOP}))
    print("TOP-LEVEL fields that differ OUTSIDE the exception + the new silver_datasets addition: %s" % top_diffs)

    passed = checked_rows == 36 and len(orig_ch) == 15 and not diffs and not top_diffs
    verdict("MXC2-AC4", passed, "" if passed else "field drift detected (see DIFF lines above)")


def ac5():
    print("=== MXC2-AC5: validate_catalog_v02.py and battery_catalog_v02.py pass at the cell's HEAD ===")
    rc_v, out_v, err_v = run([sys.executable, VALIDATE_PY], timeout=100)
    print("VALIDATE rc=%d" % rc_v)
    print(out_v[-3500:])
    if err_v.strip():
        print("VALIDATE STDERR (tail): " + err_v[-1000:])
    # validate_catalog_v02.py writes catalog_v02/validation_report.json as a side effect --
    # that path is NOT in this cell's <paths> grant, so restore it rather than leave it
    # modified in the worktree (surprise row NFRA_MCPINDEX-W1-S3 names the gap).
    rc_git, _out_git, err_git = run(["git", "checkout", "--", "workflows/atom_decomposition/catalog_v02/validation_report.json"])
    print("restored out-of-grant side effect (git checkout rc=%d%s)" % (rc_git, ("" if rc_git == 0 else "; " + err_git[:200])))

    rc_b, out_b, err_b = run([sys.executable, BATTERY_PY], timeout=100)
    print("BATTERY rc=%d" % rc_b)
    print(out_b[-3500:])
    if err_b.strip():
        print("BATTERY STDERR (tail): " + err_b[-1000:])

    passed = rc_v == 0 and rc_b == 0
    verdict("MXC2-AC5", passed, "" if passed else "rc_v=%d rc_b=%d" % (rc_v, rc_b))


def ac6():
    print("=== MXC2-AC6: the emitted file stays ASCII-clean ===")
    b = io.open(CAT_PATH, "rb").read()
    decoded = b.decode("utf-8")
    delta = len(b) - len(decoded)
    print("len(bytes)=%d len(decoded utf-8 chars)=%d delta=%d (0 == ascii-clean)" % (len(b), len(decoded), delta))
    ascii_ok = True
    try:
        b.decode("ascii")
    except UnicodeDecodeError as e:
        ascii_ok = False
        print("ascii decode failed: %s" % e)
    print("strict ascii decode of the emitted file: %s" % ascii_ok)
    passed = delta == 0 and ascii_ok
    verdict("MXC2-AC6", passed, "" if passed else "non-ascii bytes present")


def _catalog_shaped_census(root):
    hits = set()
    for dirpath, _dirnames, filenames in os.walk(root):
        parts = dirpath.replace("\\", "/").split("/")
        if ".git" in parts or "__pycache__" in parts:
            continue
        for fn in filenames:
            if fnmatch.fnmatch(fn, "*DATA_CATALOG*") or fnmatch.fnmatch(fn, "*catalog*.yaml"):
                hits.add(os.path.relpath(os.path.join(dirpath, fn), REPO).replace("\\", "/"))
    return hits


def ac7():
    print("=== MXC2-AC7: no second catalog file is created ===")
    roots = [os.path.join(REPO, "infra", "aws", "ec2", "opal-gateway"),
             os.path.join(REPO, "workflows", "atom_decomposition")]
    after = set()
    for r in roots:
        after |= _catalog_shaped_census(r)
    print("AFTER (current worktree walk) denominator: %d hit(s): %s" % (len(after), sorted(after)))

    rc, out, _err = run(["git", "ls-tree", "-r", "--name-only", CUT_HEAD,
                          "--", "infra/aws/ec2/opal-gateway", "workflows/atom_decomposition"])
    before = set(p for p in out.splitlines()
                 if fnmatch.fnmatch(os.path.basename(p), "*DATA_CATALOG*")
                 or fnmatch.fnmatch(os.path.basename(p), "*catalog*.yaml"))
    print("BEFORE (git ls-tree @%s) denominator: %d hit(s): %s" % (CUT_HEAD, len(before), sorted(before)))

    added = sorted(after - before)
    removed = sorted(before - after)
    print("ADDED since the cut: %s" % added)
    print("REMOVED since the cut: %s" % removed)
    disallowed_added = [p for p in added if "catalog_entries/" not in p]
    passed = not removed and not disallowed_added
    verdict("MXC2-AC7", passed, "" if passed else "unexpected catalog-shaped file(s): added=%s removed=%s" % (disallowed_added, removed))


def ac8():
    print("=== MXC2-AC8: Rule 24 four-postulate record for the entry schema's value sets ===")
    result_path = os.path.join(REPO, "org", "missions", "D9", "NFRA", "NFRA_MCPINDEX", "deliverables",
                                "0.9.0_WK_NFRA_MCPINDEX~1", "catalog-silver-schema.result.md")
    exists = os.path.exists(result_path)
    print("deliverable exists: %s (%s)" % (exists, result_path))
    text = io.open(result_path, encoding="utf-8").read() if exists else ""

    checks = {
        "(i) MECE section present": re.search(r"\(i\)\s*MECE", text, re.I) is not None,
        "(ii) SAME GRAIN section present": re.search(r"\(ii\)\s*SAME GRAIN", text, re.I) is not None,
        "(iii) INTENT COHERENCE section present": re.search(r"\(iii\)\s*INTENT COHERENCE", text, re.I) is not None,
        "(iv) STATE COHERENCE section present": re.search(r"\(iv\)\s*STATE COHERENCE", text, re.I) is not None,
        "word-boundary census language present": "word-boundary" in text.lower() and "denominator" in text.lower(),
    }
    for k, v in checks.items():
        print("  %s: %s" % (k, v))

    # independent re-run of the word-boundary census (not trusted from the doc's own prose):
    # every declared firm_scope_rule value must appear at least once, word-boundary, in the
    # schema's own definition (the census's positive control) -- denominator = 3 declared.
    py_text = io.open(EMIT_PY, encoding="utf-8").read()
    firm_hits = {v: len(re.findall(r"\b%s\b" % re.escape(v), py_text)) for v in emit.ENTRY_FIRM_SCOPE_RULES}
    print("firm_scope_rule word-boundary census over emit_catalog_v02.py (denominator = %d declared values): %s"
          % (len(emit.ENTRY_FIRM_SCOPE_RULES), firm_hits))
    census_ok = all(n >= 1 for n in firm_hits.values())

    passed = all(checks.values()) and census_ok
    verdict("MXC2-AC8", passed, "" if passed else "record incomplete: %s" % {k: v for k, v in checks.items() if not v})


DISPATCH = {"AC1": ac1, "AC2": ac2, "AC3": ac3, "AC4": ac4, "AC5": ac5, "AC6": ac6, "AC7": ac7, "AC8": ac8}


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in DISPATCH:
        print("usage: mx_c_2.py AC1..AC8")
        return 3
    DISPATCH[sys.argv[1]]()
    return 0


if __name__ == "__main__":
    sys.exit(main())
