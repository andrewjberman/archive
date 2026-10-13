"""ADVI_FIRMBKTS round 7 graders, issuer 2.0.0_SA_COO~B1.

  awsdiff --root R --file F [--allow-pattern P]   FB-j-2, FB-j-4: every `aws ` line of F is byte-unchanged between the merge-base of R's
                    HEAD with the primary checkout and HEAD, EXCEPT lines containing the pattern (default `events put-events`), which may
                    change; and no changed hunk lies outside the file's `emit_chain_complete` function or the one EVENTS_REGION line.
  agree2 --a A --b B [--root R]                    FB-j-1: reader 2's answers against reader 1's and the key (per field and all four).
  emiterr --file F                                 FB-j-3: the measured CLI error record.
  firstchain --file F                              FB-j-7: the first chain after the fix deploy.
  dryrun --file F                                  FB-j-6: the deployed dry-run handler's sample record.
Plain ASCII; exit 0 on a pass. Proves SHAPE and discipline, never that a finding is true.
"""
import argparse
import json
import re
import subprocess
import sys

R6 = "org/missions/D8/ADVI/ADVI_FIRMBKTS/deliverables/2.0.0_SA_COO~B1/round6"
CLAIMS = ("measured", "inferred", "held", "absent")
FIELDS = ("system", "firm", "tier", "table")


def _git(root, *a):
    r = subprocess.run(["git", "-C", root] + list(a), capture_output=True, text=True, encoding="utf-8", errors="replace")
    return r.returncode, r.stdout


def awsdiff(a):
    rc, wl = _git(a.root, "worktree", "list", "--porcelain")
    primary = next((ln.split()[1] for ln in wl.split("\n") if ln.startswith("worktree ")), "")
    rc, base = _git(a.root, "merge-base", "HEAD", primary and "box/dell1")
    base = base.strip()
    if rc or not base:
        print("AWSDIFF: FAIL no merge-base")
        return 1
    rc, old = _git(a.root, "show", "%s:%s" % (base, a.file))
    rc2, new = _git(a.root, "show", "HEAD:%s" % a.file)
    if rc or rc2:
        print("AWSDIFF: FAIL cannot read the file at the base or at HEAD")
        return 1
    pat = a.allow_pattern

    def aws_lines(t):
        return [x.strip() for x in t.split("\n") if re.search(r"^[^#]*\baws ", x) and pat not in x]
    same = aws_lines(old) == aws_lines(new)
    # hunks
    rc, df = _git(a.root, "diff", "-U0", base, "HEAD", "--", a.file)
    hunks = [(int(m.group(1)), int(m.group(2) or 1)) for m in re.finditer(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@", df, re.M)]
    lines = new.split("\n")
    start = next((i + 1 for i, ln in enumerate(lines) if ln.startswith("emit_chain_complete() {")), None)
    end = next((i + 1 for i in range((start or 1), len(lines)) if lines[i] == "}"), None)
    ev = [i + 1 for i, ln in enumerate(lines) if re.match(r"^\s*EVENTS_REGION=", ln)]
    outside = []
    for s, n in hunks:
        for ln in range(s, s + max(n, 1)):
            if n == 0:
                continue
            if start and end and start <= ln <= end:
                continue
            if ln in ev:
                continue
            outside.append(ln)
    print("  aws lines other than the pattern unchanged: %s; changed hunks %d; changed lines outside the function and the variable: %s"
          % (same, len(hunks), outside[:8]))
    ok = same and not outside and bool(hunks)
    print("AWSDIFF: %s" % ("OK" if ok else "FAIL"))
    return 0 if ok else 1


def _norm(v):
    return re.sub(r"[^a-z0-9]", "", str(v).lower())


def agree2(a):
    root = a.root or subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
    key = json.load(open("%s/%s/READING_KEY.json" % (root, R6), encoding="utf-8"))
    ra = {x["id"]: x for x in json.load(open(a.a, encoding="utf-8"))["answers"]}
    rb = {x["id"]: x for x in json.load(open(a.b, encoding="utf-8"))["answers"]}
    ids = sorted(key)
    print("reader1=%d reader2=%d key=%d" % (len(ra), len(rb), len(key)))
    line = ["n=%d" % len(ids)]
    for f in FIELDS:
        ag = sum(1 for i in ids if _norm(ra[i][f]) == _norm(rb[i][f]) != "unknown")
        line.append("%s agree %d of %d" % (f, ag, len(ids)))
    allf = sum(1 for i in ids if all(_norm(ra[i][f]) == _norm(rb[i][f]) != "unknown" for f in FIELDS))
    eq2 = sum(1 for i in ids if all(_norm(rb[i][f]) == _norm(key[i]["truth"][f]) for f in FIELDS))
    line.append("all four agree %d of %d" % (allf, len(ids)))
    line.append("reader 2 equals the key on all four %d of %d" % (eq2, len(ids)))
    print(" | ".join(line))
    for i in ids:
        if not all(_norm(ra[i][f]) == _norm(rb[i][f]) != "unknown" for f in FIELDS):
            print("  DISAGREE %s class=%s r1=%s r2=%s key=%s" % (
                i, key[i]["class"], "/".join(ra[i][f] for f in FIELDS), "/".join(rb[i][f] for f in FIELDS),
                "/".join(key[i]["truth"][f] for f in FIELDS)))
    return 0


def _need(d, keys):
    out = []
    for k in keys:
        cur = d
        for p in k.split("."):
            if not isinstance(cur, dict) or p not in cur:
                out.append("missing %s" % k)
                break
            cur = cur[p]
    return out


def emiterr(a):
    try:
        d = json.load(open(a.file, encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        print("FAIL ABSENT or unreadable: %s" % type(e).__name__)
        return 1
    p = _need(d, ["deployed.key", "deployed.sha256", "deployed.equals_repo", "ledger.entry", "ledger.closed",
                  "next_chain.label", "next_chain.started_at", "warn_text", "cause_class", "claim", "calls"])
    if not p:
        if d["cause_class"] not in ("NO_REGION", "CREDENTIALS", "OTHER_NAMED", "NOT_OBSERVED"):
            p.append("cause_class not in the closed set")
        if d["claim"] not in CLAIMS:
            p.append("claim not one of %s" % "/".join(CLAIMS))
        if d["deployed"]["equals_repo"] is not True or not re.fullmatch(r"[0-9a-f]{64}", str(d["deployed"]["sha256"])):
            p.append("the deployed object must equal the repository file (sha256)")
        if d["ledger"]["closed"] is not True:
            p.append("the ledger entry is not closed")
        if d["cause_class"] != "NOT_OBSERVED" and not str(d["warn_text"] or "").strip():
            p.append("a named cause carries no verbatim warn_text")
        if len(str(d["warn_text"] or "")) > 300:
            p.append("warn_text longer than 300 characters")
        bad = [c for c in d["calls"] if not re.match(r"^(aws|\.tools/aws)\s+[a-z0-9-]+\s+(get|describe|list|lookup|head|filter|cp|s3api put-object)", str(c))]
        if bad and any(re.search(r"\b(delete|rm|terminate|stop|start|update|invoke|put-events)\b", str(c)) for c in bad):
            p.append("a call is a write other than the one object copy")
    if p:
        for x in p:
            print("FAIL %s" % x)
        print("EMITERR: %d problem(s)" % len(p))
        return 1
    print("EMITERR record ok cause_class=%s" % d["cause_class"])
    return 0


def firstchain(a):
    try:
        d = json.load(open(a.file, encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        print("FAIL ABSENT or unreadable: %s" % type(e).__name__)
        return 1
    p = _need(d, ["pair.coo_half", "pair.cto_half", "dry_run_sample.advisors", "dry_run_sample.objects_written",
                  "dry_run_sample.read_before_deploy", "deploy.ledger_closed", "chain.label", "chain.emitted_line",
                  "chain.cloudtrail_putevents", "chain.generator_invocations", "keys.regenerated", "keys.ceiling",
                  "keys.prior_version_ids_recorded", "keys.advisors_with_bullets_before", "keys.bullet_regressions", "keys.nonempty_bullets", "slots_disabled", "claim"])
    if not p:
        if d["claim"] not in CLAIMS:
            p.append("claim not one of %s" % "/".join(CLAIMS))
        if d["dry_run_sample"]["objects_written"] != 0 or d["dry_run_sample"]["read_before_deploy"] is not True:
            p.append("the dry-run sample must write 0 objects and be read before the deploy")
        if not (1 <= d["dry_run_sample"]["advisors"] <= 10):
            p.append("the dry-run sample is 1 to 10 advisors")
        if d["chain"]["emitted_line"] is not True or d["chain"]["cloudtrail_putevents"] < 1 or d["chain"]["generator_invocations"] < 1:
            p.append("the first chain must show the emitted line, a CloudTrail PutEvents and a generator invocation")
        if not (0 <= d["keys"]["regenerated"] <= d["keys"]["ceiling"] <= 194) or d["keys"]["prior_version_ids_recorded"] is not True:
            p.append("regenerated keys must be within the named ceiling (at most 194) with prior VersionIds recorded")
        if d["keys"]["nonempty_bullets"] != 0 or len(d["slots_disabled"]) != 6:
            p.append("the first regeneration is empty-for-empty: all six slots disabled and no regenerated artifact may carry a bullet")
        if not isinstance(d["keys"]["advisors_with_bullets_before"], int) or d["keys"]["bullet_regressions"] != 0:
            p.append("a summary that carried bullets before was replaced by one with none (bullet_regressions must be 0, read per advisor)")
        if d["deploy"]["ledger_closed"] is not True:
            p.append("the ledger entry is not closed")
    if p:
        for x in p:
            print("FAIL %s" % x)
        print("FIRSTCHAIN: %d problem(s)" % len(p))
        return 1
    print("FIRSTCHAIN record ok regenerated=%d invocations=%d" % (d["keys"]["regenerated"], d["chain"]["generator_invocations"]))
    return 0


def dryrun(a):
    try:
        d = json.load(open(a.file, encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        print("FAIL ABSENT or unreadable: %s" % type(e).__name__)
        return 1
    p = _need(d, ["advisors", "listing_before", "listing_after", "artifacts_returned", "deployed_version", "pair.coo_half",
                  "pair.cto_half", "ledger_closed", "claim"])
    if not p:
        if d["claim"] not in CLAIMS:
            p.append("claim not one of %s" % "/".join(CLAIMS))
        if not (1 <= d["advisors"] <= 10):
            p.append("the sample is 1 to 10 advisors")
        if d["listing_before"] != d["listing_after"]:
            p.append("the bucket listing changed across the dry run: it wrote an object")
        if d["artifacts_returned"] != d["advisors"]:
            p.append("artifacts returned must equal the advisors asked")
        if d["ledger_closed"] is not True:
            p.append("the ledger entry is not closed")
    if p:
        for x in p:
            print("FAIL %s" % x)
        print("DRYRUN: %d problem(s)" % len(p))
        return 1
    print("DRYRUN record ok advisors=%d listing=%s" % (d["advisors"], d["listing_after"]))
    return 0


def prescreen(a):
    try:
        d = json.load(open(a.file, encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        print("FAIL ABSENT or unreadable: %s" % type(e).__name__)
        return 1
    p = _need(d, ["advisors", "per_slot_fired", "advisors_firing_any", "targeted_ids", "second_dry_run.done",
                  "second_dry_run.bullets_returned", "no_model_call_in_prescreen", "zero_reason", "claim"])
    if not p:
        if d["claim"] not in CLAIMS:
            p.append("claim not one of %s" % "/".join(CLAIMS))
        if d["no_model_call_in_prescreen"] is not True:
            p.append("the pre-screen must make no model call")
        if not (0 <= d["advisors_firing_any"] <= d["advisors"]) or d["advisors"] < 1:
            p.append("advisors_firing_any must lie between 0 and a positive advisors count")
        if not isinstance(d["per_slot_fired"], dict) or len(d["per_slot_fired"]) != 6:
            p.append("per_slot_fired must name the six slots")
        if len(d["targeted_ids"]) > 10:
            p.append("targeted_ids is at most 10")
        if d["advisors_firing_any"] == 0 and not str(d["zero_reason"]).strip():
            p.append("zero advisors fire: zero_reason must say why, per slot")
        sd = d["second_dry_run"]
        if sd["done"] is True and sd["bullets_returned"] < 1 and d["advisors_firing_any"] > 0:
            # the control failing is a FINDING when the record names the drops and the cause (or says it is unknown)
            dropped = sd.get("slots_dropped")
            if not isinstance(dropped, int) or dropped < 1 or not str(sd.get("control_failed_cause", "")).strip():
                p.append("a targeted dry run on firing advisors returned no bullets: record slots_dropped (>= 1) and control_failed_cause (the exception class, or the words cause not known)")
    if p:
        for x in p:
            print("FAIL %s" % x)
        print("PRESCREEN: %d problem(s)" % len(p))
        return 1
    print("PRESCREEN record ok advisors=%d firing_any=%d second_dry_run=%s" % (
        d["advisors"], d["advisors_firing_any"], d["second_dry_run"]["done"]))
    return 0


def slotcause(a):
    try:
        d = json.load(open(a.file, encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        print("FAIL ABSENT or unreadable: %s" % type(e).__name__)
        return 1
    p = _need(d, ["advisors", "listing_before", "listing_after", "drops", "classes", "messages", "bullets_returned",
                  "advisors_with_bullets", "cause_class", "pair.coo_half_addendum", "pair.cto_half_addendum", "ledger_closed",
                  "deployed_version", "claim"])
    if not p:
        if d["claim"] not in CLAIMS:
            p.append("claim not one of %s" % "/".join(CLAIMS))
        if d["advisors"] != 10:
            p.append("the CTO's dry run is TEN pre-screened advisors")
        if d["listing_before"] != d["listing_after"]:
            p.append("the served listing changed across the dry run: an object was written")
        if d["cause_class"] not in ("NOT_APPLICABLE", "CONFIG", "PRODUCT", "NOT_KNOWN"):
            p.append("cause_class not in the closed set")
        if any(len(str(m)) > 200 for m in d["messages"]):
            p.append("a logged message is over 200 characters")
        if not isinstance(d["bullets_returned"], int) or d["bullets_returned"] < 1:
            p.append("the bullets must be NON-EMPTY (the CTO's criterion); a zero-bullet record carries drops and a cause for the next cut")
        if d["drops"] > 0 and d["cause_class"] == "NOT_APPLICABLE":
            p.append("drops were logged: name the cause class")
        if d["ledger_closed"] is not True:
            p.append("the ledger entry is not closed")
    if p:
        for x in p:
            print("FAIL %s" % x)
        print("SLOTCAUSE: %d problem(s)" % len(p))
        return 1
    print("SLOTCAUSE record ok drops=%d classes=%d bullets=%d" % (d["drops"], len(d["classes"]), d["bullets_returned"]))
    return 0


def tfslots(a):
    """FB-j-11 part C: the Terraform carrier of the slot switch, three text arms over the worker's tree (and the base for arm 3)."""
    root = a.root
    res = []
    try:
        with open(root + "/infra/aws/terraform/exec-summary/variables.tf", encoding="utf-8") as fh:
            var = fh.read()
        with open(root + "/infra/aws/terraform/exec-summary/main.tf", encoding="utf-8") as fh:
            main = fh.read()
    except OSError as e:
        print("FAIL cannot read the Terraform root: %s" % type(e).__name__)
        print("TFSLOTS: 0 of 3 arms")
        return 1
    m = re.search(r'variable\s+"disabled_slots"\s*\{(.*?)\n\}', var, re.S)
    ok1 = bool(m) and 'default' in m.group(1) and re.search(r'default\s*=\s*""', m.group(1)) is not None \
        and "validation" in m.group(1)
    res.append(("T1 variable disabled_slots exists with default empty and a validation", ok1))
    ok2 = re.search(r'var\.disabled_slots\s*==\s*""\s*\?\s*\{\}\s*:\s*\{\s*EXEC_SUMMARY_DISABLED_SLOTS\s*=\s*var\.disabled_slots\s*\}', main) is not None
    res.append(("T2 the environment adds EXEC_SUMMARY_DISABLED_SLOTS only when the variable is non-empty", ok2))
    rc, base = _git(root, "merge-base", "HEAD", "box/dell1")
    base = base.strip()
    rc1, old = _git(root, "show", "%s:infra/aws/terraform/exec-summary/main.tf" % base)
    keep = ["platinum_mode == \"\" ? {} : { BD_PLATINUM_MODE = var.platinum_mode }", "ANTHROPIC_SECRET_NAME", "MAX_ADVISORS_HARD_CAP", "DATA_BUCKET"]
    ok3 = rc == 0 and rc1 == 0 and all((k in old) == (k in main) and k in main for k in keep)
    res.append(("T3 the six existing environment keys and the platinum_mode term are untouched", ok3))
    for name, ok in res:
        print("%s %s" % ("PASS" if ok else "FAIL", name))
    n = sum(1 for _, ok in res if ok)
    print("TFSLOTS: %d of 3 arms" % n)
    return 0 if n == 3 else 1


def iqlt(a):
    try:
        d = json.load(open(a.file, encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        print("FAIL ABSENT or unreadable: %s" % type(e).__name__)
        return 1
    p = _need(d, ["ticker", "advisor_id", "accounts", "market_value", "cost_basis", "unrealized_loss", "loss_pct", "price_used",
                  "price_sources", "classification", "reason", "calls", "claim"])
    if not p:
        if d["claim"] not in CLAIMS:
            p.append("claim not one of %s" % "/".join(CLAIMS))
        if d["classification"] not in ("DATA_DEFECT", "REAL_LOSS", "NOT_DETERMINED"):
            p.append("classification not in the closed set")
        if not isinstance(d["price_sources"], list) or len(d["price_sources"]) < 2:
            p.append("price_sources must name at least two independent sources (or say which could not be read)")
        bad = [c for c in d["calls"] if not re.match(r"^(aws|\.tools/aws)\s+[a-z0-9-]+\s+(get|describe|list|lookup|head|filter)", str(c))]
        if bad:
            p.append("a call is not a read verb: %s" % str(bad[0])[:80])
    if p:
        for x in p:
            print("FAIL %s" % x)
        print("IQLT: %d problem(s)" % len(p))
        return 1
    print("IQLT record ok classification=%s loss_pct=%s" % (d["classification"], d["loss_pct"]))
    return 0


def switchsample(a):
    try:
        d = json.load(open(a.file, encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        print("FAIL ABSENT or unreadable: %s" % type(e).__name__)
        return 1
    p = _need(d, ["plan.add", "plan.change", "plan.destroy", "plan.env_keys_added", "advisors", "listing_before", "listing_after",
                  "nna_bullets", "bullets_returned", "drops", "ledger_closed", "pair.coo_half_addendum2", "pair.cto_half_addendum2",
                  "deployed_version", "claim"])
    if not p:
        if d["claim"] not in CLAIMS:
            p.append("claim not one of %s" % "/".join(CLAIMS))
        if (d["plan"]["add"], d["plan"]["change"], d["plan"]["destroy"]) != (0, 1, 0):
            p.append("the plan must read 0 to add, 1 to change, 0 to destroy")
        if d["plan"]["env_keys_added"] != ["EXEC_SUMMARY_DISABLED_SLOTS"]:
            p.append("the plan may add exactly ONE environment key, EXEC_SUMMARY_DISABLED_SLOTS")
        if d["advisors"] != 10 or d["listing_before"] != d["listing_after"]:
            p.append("ten advisors and an identical served listing are required")
        if d["nna_bullets"] != 0:
            p.append("the disabled slot returned bullets")
        if not isinstance(d["bullets_returned"], int) or d["bullets_returned"] < 1:
            p.append("the four other slots must still return bullets")
        if d["ledger_closed"] is not True:
            p.append("the ledger entry is not closed")
    if p:
        for x in p:
            print("FAIL %s" % x)
        print("SWITCHSAMPLE: %d problem(s)" % len(p))
        return 1
    print("SWITCHSAMPLE record ok bullets=%d nna=%d drops=%d" % (d["bullets_returned"], d["nna_bullets"], d["drops"]))
    return 0


def scrub(a):
    """FB-j-14: no raw relationship id (z followed by six or more digits) in the named files; hashed forms h_<12 hex> are fine."""
    pat = re.compile(r"(?<![0-9A-Za-z])z[0-9]{6,}(?![0-9A-Za-z])")
    n_files = n_ids = 0
    for f in a.files:
        try:
            txt = open(f, encoding="utf-8").read()
        except OSError:
            print("FAIL cannot read %s" % f)
            return 1
        n_files += 1
        n_ids += len(pat.findall(txt))
    if n_ids:
        print("SCRUB: FAIL files=%d ids=%d" % (n_files, n_ids))
        return 1
    print("SCRUB: OK files=%d ids=0" % n_files)
    return 0


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    x = sub.add_parser("awsdiff")
    x.add_argument("--root", required=True)
    x.add_argument("--file", required=True)
    x.add_argument("--allow-pattern", default="events put-events")
    g = sub.add_parser("agree2")
    g.add_argument("--a", required=True)
    g.add_argument("--b", required=True)
    g.add_argument("--root")
    e = sub.add_parser("emiterr")
    e.add_argument("--file", required=True)
    f = sub.add_parser("firstchain")
    f.add_argument("--file", required=True)
    h = sub.add_parser("dryrun")
    h.add_argument("--file", required=True)
    s = sub.add_parser("prescreen")
    s.add_argument("--file", required=True)
    c = sub.add_parser("slotcause")
    c.add_argument("--file", required=True)
    for nm in ("iqlt", "switchsample"):
        q = sub.add_parser(nm)
        q.add_argument("--file", required=True)
    tf = sub.add_parser("tfslots")
    tf.add_argument("--root", required=True)
    sc = sub.add_parser("scrub")
    sc.add_argument("--files", nargs="+", required=True)
    a = ap.parse_args()
    return {"awsdiff": awsdiff, "agree2": agree2, "emiterr": emiterr, "firstchain": firstchain, "dryrun": dryrun, "prescreen": prescreen, "slotcause": slotcause,
            "tfslots": tfslots, "iqlt": iqlt, "switchsample": switchsample, "scrub": scrub}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
