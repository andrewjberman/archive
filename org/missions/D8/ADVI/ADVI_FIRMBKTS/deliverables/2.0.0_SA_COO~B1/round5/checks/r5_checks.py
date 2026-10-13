"""ADVI_FIRMBKTS round 5 shape graders for the read-only cells, issuer 2.0.0_SA_COO~B1.

  diag  --file F    FB-h-6   the exec-summary put-events diagnosis (EXEC_SUMMARY_DIAGNOSIS.json)
  quant --file F    FB-h-7   the Black Diamond pricing quantification (PRICING_QUANT.json)
  live  --file F    FB-h-5   the validator's live ownership-path read (VALIDATOR_LIVE_READ.json)
  replay --file F   FB-h-3   the offline replay's result record (REPLAY_RESULT.json)
  mutant --root R   FB-h-4   the validator spec against a COPY whose generated bucket list is emptied: it must FAIL

Each prints one result line and exits 0 on a pass, 1 otherwise. A grader proves the record's SHAPE and its discipline (every
value carries its claim, every AWS call is a read verb, counts carry denominators, the recommendation follows the CTO's rule);
whether the findings are TRUE is the issuer's and the CVO's read of the cited calls, never this file's. Plain ASCII.
"""
import argparse
import json
import re
import sys

CLAIMS = ("measured", "inferred", "held", "absent")
READ_VERB = re.compile(r"^(aws|\.tools/aws|bash \.tools/aws)\s+[a-z0-9-]+\s+(get|describe|list|lookup|head|filter)[a-z0-9-]*\b")


def _load(p):
    try:
        with open(p, encoding="utf-8") as fh:
            return json.load(fh), None
    except Exception as e:  # noqa: BLE001
        return None, "%s: %s" % (type(e).__name__, str(e)[:120])


def _need(d, path, kinds):
    cur = d
    for k in path.split("."):
        if not isinstance(cur, dict) or k not in cur:
            return "missing %s" % path
        cur = cur[k]
    ks = kinds if isinstance(kinds, tuple) else (kinds,)
    if not isinstance(cur, ks) or (isinstance(cur, bool) and bool not in ks):
        return "wrong type at %s" % path
    return None


def _claim(d, path):
    cur = d
    for k in path.split("."):
        cur = cur.get(k) if isinstance(cur, dict) else None
    return "claim at %s not one of %s" % (path, "/".join(CLAIMS)) if cur not in CLAIMS else None


def _calls(d):
    calls = d.get("calls")
    if not isinstance(calls, list) or not calls:
        return ["calls: a non-empty list of the AWS calls made"]
    bad = [c for c in calls if not isinstance(c, str) or not READ_VERB.match(c.strip())]
    return ["call is not a read verb: %s" % str(c)[:90] for c in bad[:3]]


def diag(f):
    d, err = _load(f)
    if err:
        return ["ABSENT or unreadable: %s" % err], ""
    p = []
    p += _calls(d)
    for path, kinds in (("put_events_error_text.value", (str, type(None))), ("bus.name", str), ("bus.exists", (bool, type(None))),
                        ("rule.name", str), ("rule.state", (str, type(None))), ("rule.event_pattern", (dict, type(None))),
                        ("rule.targets", list), ("dispatcher_role.role", str),
                        ("dispatcher_role.events_putevents_allowed", (bool, type(None))), ("dispatcher_role.evidence", str),
                        ("cloudtrail.put_events_total", int), ("cloudtrail.put_events_errors", int),
                        ("cloudtrail.error_codes", dict), ("cloudtrail.window_start", str), ("cloudtrail.window_end", str),
                        ("dispatcher_test.line", str), ("dispatcher_test.note", str), ("verdict", str),
                        ("verdict_reason", str), ("fix_owner_proposal", str)):
        e = _need(d, path, kinds)
        if e:
            p.append(e)
    for path in ("put_events_error_text", "bus", "rule", "dispatcher_role", "cloudtrail", "dispatcher_test"):
        e = _claim(d, path + ".claim")
        if e:
            p.append(e)
    if d.get("verdict") not in ("EMITTED_NOT_MATCHED", "NOT_EMITTED_SCRIPT_TEST", "DENIED", "BUS_OR_RULE_ABSENT", "INDETERMINATE"):
        p.append("verdict not in the closed set")
    pe = d.get("put_events_error_text", {})
    if isinstance(pe, dict) and pe.get("claim") == "measured" and not (pe.get("source") or "").strip():
        p.append("a measured error text names no source")
    return p, "DIAG keys ok calls=%d verdict=%s" % (len(d.get("calls") or []), d.get("verdict"))


def quant(f):
    d, err = _load(f)
    if err:
        return ["ABSENT or unreadable: %s" % err], ""
    p = []
    p += _calls(d)
    for path, kinds in (("s32.window.days", int), ("s32.asset_days_considered", int), ("s32.asset_days_median_changes", int),
                        ("s32.assets_affected", int), ("s32.max_abs_price_delta", (int, float)), ("s32.writers", list),
                        ("s33.date", str), ("s33.tied_assets", int), ("s33.alternative_differs", int),
                        ("s33.max_abs_price_delta", (int, float)), ("s33.canonical_prices_writers", (list, str)),
                        ("s34.readers", list), ("s34.served_0820_0823.objects_compared", int),
                        ("s34.served_0820_0823.changed", int), ("recommendation", str), ("recommendation_reason", str)):
        e = _need(d, path, kinds)
        if e:
            p.append(e)
    for path in ("s32", "s33", "s34.served_0820_0823"):
        e = _claim(d, path + ".claim")
        if e:
            p.append(e)
    if not p:
        s32, s33, s34 = d["s32"], d["s33"], d["s34"]
        if not (0 <= s32["asset_days_median_changes"] <= s32["asset_days_considered"] and s32["asset_days_considered"] > 0):
            p.append("s32: changes must be between 0 and a positive denominator")
        if not s32["writers"]:
            p.append("s32: the writer of the served price is not named")
        if not (0 <= s33["alternative_differs"] <= s33["tied_assets"]):
            p.append("s33: alternative_differs must be between 0 and tied_assets")
        w = s33["canonical_prices_writers"]
        if not (w == "unidentified" or (isinstance(w, list) and w)):
            p.append("s33: the canonical_prices writer is neither named nor 'unidentified'")
        names = " ".join(str(r.get("reader", "")) for r in s34["readers"] if isinstance(r, dict))
        if not all(t in names for t in ("B_03", "bd_price_update")) or len(s34["readers"]) != 3:
            p.append("s34: exactly three readers naming B_03.account_gains, bd_price_update and its Lambda twin")
        for r in s34["readers"]:
            if not isinstance(r, dict) or r.get("claim") not in CLAIMS or "reran_since_20260902" not in r:
                p.append("s34: a reader row lacks claim or reran_since_20260902")
                break
        moved = (s32["asset_days_median_changes"] > 0 or s33["alternative_differs"] > 0
                 or s34["served_0820_0823"]["changed"] > 0)
        want = "BRIEF_TO_CRO" if moved else "NOT_MATERIAL"
        if d["recommendation"] != want:
            p.append("recommendation must be %s (any non-zero count goes to the CRO; all zero is not material)" % want)
    return p, "QUANT keys ok calls=%d recommendation=%s" % (len(d.get("calls") or []), d.get("recommendation"))


def live(f):
    d, err = _load(f)
    if err:
        return ["ABSENT or unreadable: %s" % err], ""
    p = []
    p += _calls(d)
    for path, kinds in (("window_start", str), ("log_groups_read", int), ("lines_total", int),
                        ("lines_on_ownership_paths", int), ("non_admin_on_ownership_paths", int),
                        ("statuses", dict), ("events.ownership_map_fetch_failed", int),
                        ("events.ownership_map_schema_mismatch", int), ("origin", str),
                        ("session.in_hand", bool), ("session.minted_by_this_order", bool)):
        e = _need(d, path, kinds)
        if e:
            p.append(e)
    e = _claim(d, "claim") if "claim" in d else "missing claim"
    if e:
        p.append(e)
    if not p:
        if d["session"]["minted_by_this_order"]:
            p.append("a session was minted by this order: refused")
        if d["origin"] not in ("organic", "driven"):
            p.append("origin must be organic or driven")
        if d["claim"] != "measured":
            p.append("claim must be measured")
        if d["non_admin_on_ownership_paths"] < 1:
            p.append("no non-admin request on an accounts or relationship path was read")
        if d["events"]["ownership_map_fetch_failed"] != 0 or d["events"]["ownership_map_schema_mismatch"] != 0:
            p.append("an ownership_map fetch_failed or schema_mismatch event was read")
    return p, "LIVE-READ non_admin_ownership_lines=%s fetch_failed=%s origin=%s" % (
        d.get("non_admin_on_ownership_paths"), (d.get("events") or {}).get("ownership_map_fetch_failed"), d.get("origin"))


def replay(f):
    d, err = _load(f)
    if err:
        return ["ABSENT or unreadable: %s" % err], ""
    p = []
    for path, kinds in (("handler", str), ("canonical_request_bucket", str), ("canonical_request_key", str),
                        ("legacy_sha256", str), ("canonical_sha256", str), ("bytes_equal", bool), ("pairs", int),
                        ("mismatches", int), ("control_mismatches", int), ("accounts", int), ("relationships", int),
                        ("advisors", int), ("decisions", dict)):
        e = _need(d, path, kinds)
        if e:
            p.append(e)
    if not p:
        if d["handler"] != "infra/aws/lambda-edge/auth-validator-edge/index.mjs":
            p.append("handler must be the validator's index.mjs, driven as the handler (not its key helper)")
        if d["canonical_request_bucket"] != "opal-data-49financial" or                 d["canonical_request_key"] != "advi/49financial/platinum/49financial/ownership_map.json":
            p.append("the handler's own S3 request did not name the canonical bucket and key")
        for h in ("legacy_sha256", "canonical_sha256"):
            if not re.fullmatch(r"[0-9a-f]{64}", d[h]):
                p.append("%s is not a sha256" % h)
        if d["pairs"] < 100 or d["accounts"] < 1 or d["relationships"] < 1:
            p.append("fewer than 100 pairs, or no account or no relationship path replayed")
        if d["control_mismatches"] < 1:
            p.append("the perturbed-map control produced no differing decision: the comparison does not discriminate")
    return p, "REPLAY record ok pairs=%s mismatches=%s control_mismatches=%s bytes_equal=%s" % (
        d.get("pairs"), d.get("mismatches"), d.get("control_mismatches"), d.get("bytes_equal"))


def mutant(root):
    import os
    import shutil
    import subprocess
    import tempfile
    val = os.path.join(root, "infra/aws/lambda-edge/auth-validator-edge")
    fc = os.path.join(root, "infra/aws/lambda-edge/_shared/firm-config.mjs")
    tmp = tempfile.mkdtemp(prefix="r5mut_")
    try:
        dv = os.path.join(tmp, "auth-validator-edge")
        os.makedirs(os.path.join(tmp, "_shared"))
        os.makedirs(dv)
        shutil.copy(os.path.join(val, "ownership_key.mjs"), dv)
        shutil.copytree(os.path.join(val, "tests"), os.path.join(dv, "tests"))
        with open(fc, encoding="utf-8") as fh:
            src = fh.read()
        pat = r"(export const CANONICAL_PLATINUM_BUCKETS = Object\.freeze\(\[)[^\]]*(\]\);)"
        new, n = re.subn(pat, lambda m: m.group(1) + m.group(2), src)
        if n != 1:
            return ["could not locate the generated list to empty (matches=%d)" % n], ""
        dest = os.path.join(tmp, "_shared", "firm-config.mjs")
        with open(dest, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(new)
        env = dict(os.environ)
        env["PATH"] = env.get("PATH", "") + os.pathsep + os.path.join(os.path.expanduser("~"), ".bun", "bin")
        r = subprocess.run(["bun", "test", "tests/"], cwd=dv, capture_output=True, text=True, env=env, timeout=100)
        out = re.sub(chr(27) + r"\[[0-9;]*m", "", r.stdout + r.stderr)
        m = re.search(r"^\s*(\d+) fail", out, re.M)
        fails = int(m.group(1)) if m else -1
        if fails < 1:
            return ["the spec still passes with the generated list emptied (fail=%s): it does not read the flip" % fails], ""
        return [], "MUTANT: the spec FAILS as expected with the list emptied (%d fail)" % fails
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=("diag", "quant", "live", "replay", "mutant"))
    ap.add_argument("--file")
    ap.add_argument("--root")
    a = ap.parse_args()
    if a.cmd == "mutant":
        probs, line = mutant(a.root)
    else:
        probs, line = {"diag": diag, "quant": quant, "live": live, "replay": replay}[a.cmd](a.file)
    for x in probs:
        print("FAIL %s" % x)
    if probs:
        print("%s: %d problem(s)" % (a.cmd.upper(), len(probs)))
        return 1
    print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
