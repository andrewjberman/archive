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
        # CloudTrail lookup-events never returns PutEvents (FB-i-2 sweep, FB1's positive control), so the put is
        # evidenced by cloudtrail_putevents >= 1 OR by the rule firing: chain.triggered_rules_sum >= 1 (AWS/Events).
        put_seen = d["chain"]["cloudtrail_putevents"] >= 1 or d["chain"].get("triggered_rules_sum", 0) >= 1
        if d["chain"]["emitted_line"] is not True or not put_seen or d["chain"]["generator_invocations"] < 1:
            p.append("the first chain must show the emitted line, a PutEvents (CloudTrail, or the rule's TriggeredRules >= 1) and a generator invocation")
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


def trailsel(a):
    """FB-j-15: the organization trail holds the two ruled selectors unchanged plus a third, WriteOnly, on exactly bd, inf and cot.

    Reads the JSON of `aws cloudtrail get-event-selectors` on stdin.
    """
    try:
        d = json.load(sys.stdin)
        sel = d["EventSelectors"]
    except (ValueError, KeyError, TypeError):
        print("TRAILSEL: FAIL input is not get-event-selectors JSON")
        return 1
    want_read = sorted("arn:aws:s3:::%s/" % b for b in ("opal-data-49financial", "opal-data-bd", "opal-data-cot", "opal-data-inf"))
    want_write = sorted("arn:aws:s3:::%s/" % b for b in ("opal-data-bd", "opal-data-cot", "opal-data-inf"))

    def shape(s):
        vals = sorted(v for r in s.get("DataResources", []) if r.get("Type") == "AWS::S3::Object" for v in r.get("Values", []))
        return (s.get("ReadWriteType"), bool(s.get("IncludeManagementEvents")), vals)

    got = [shape(s) for s in sel]
    problems = []
    if len(got) != 3:
        problems.append("selectors=%d, want 3" % len(got))
    if ("All", True, []) not in got:
        problems.append("management selector missing or changed")
    if ("ReadOnly", False, want_read) not in got:
        problems.append("read selector missing or changed")
    if ("WriteOnly", False, want_write) not in got:
        problems.append("write selector missing or not exactly bd, inf and cot")
    if problems:
        print("TRAILSEL: FAIL " + "; ".join(problems))
        return 1
    print("TRAILSEL: OK selectors=3 write_buckets=3")
    return 0


PLANINV_CLAIMS = ("measured", "inferred", "held", "absent")
PLANINV_KINDS = ("rule", "schedule", "task", "service", "lambda", "edge", "topic", "email", "script", "role", "reader", "other")
PLANINV_WRITE_VERBS = re.compile(
    r"(\s(put|delete|create|update|modify|attach|detach|start|stop|run|terminate|enable|disable|register|deregister|tag|untag|send|publish|invoke)-[a-z-]+)"
    r"|(\ss3(api)?\s+(cp|mv|rm|sync|put-object|delete-object)\b)|(\sterraform\s+(apply|destroy|import)\b)")
PLANINV_ID_TOKEN = re.compile(r"(?<![0-9A-Za-z])[A-Za-z]?[0-9]{9,}(?![0-9A-Za-z])")
PLANINV_OK_TOKENS = ("313476888478",)


def _planinv_text_problems(raw):
    out = []
    bad = [m for m in PLANINV_ID_TOKEN.findall(raw) if m not in PLANINV_OK_TOKENS]
    if bad:
        out.append("%d id-shaped token(s) of nine or more digits (replace with <id>)" % len(bad))
    return out


def planinv(a):
    """FB-k-1..5: the read-only plan inventories (shape and read-only discipline; completeness is read by the issuer)."""
    try:
        raw = open(a.file, encoding="utf-8").read()
        d = json.loads(raw)
    except (OSError, ValueError) as e:
        print("PLANINV: FAIL cannot read %s: %s" % (a.file, type(e).__name__))
        return 1
    p = _planinv_text_problems(raw)
    for k in ("order", "read_at", "calls", "denominators", "not_read", "claim"):
        if k not in d:
            p.append("missing %s" % k)
    if p and any(x.startswith("missing") for x in p):
        print("PLANINV: FAIL " + "; ".join(p))
        return 1
    if d["claim"] not in PLANINV_CLAIMS:
        p.append("claim outside the four")
    if not isinstance(d["calls"], list) or not d["calls"] or not all(isinstance(c, str) for c in d["calls"]):
        p.append("calls must be a non-empty list of strings")
    else:
        for c in d["calls"]:
            if PLANINV_WRITE_VERBS.search(" " + c):
                p.append("a call carries a write verb")
                break
    den = d["denominators"]
    if not isinstance(den, dict) or not den or not all(isinstance(v, int) and v >= 0 for v in den.values()) or not any(v > 0 for v in den.values()):
        p.append("denominators must be integers with at least one above zero")
    if not isinstance(d["not_read"], list):
        p.append("not_read must be a list")
    rows = d.get("candidates" if a.shape == "retire" else "functions")
    if not isinstance(rows, list) or len(rows) < a.min:
        p.append("%s must be a list of at least %d" % ("candidates" if a.shape == "retire" else "functions", a.min))
        rows = []
    legacy = 0
    for i, r in enumerate(rows):
        if not isinstance(r, dict):
            p.append("row %d is not an object" % i)
            continue
        need = ["id", "kind", "name", "evidence", "claim"]
        need += ["legacy_reason", "replaced_by", "replaced_by_claim", "decision_owner"] if a.shape == "retire" else ["trigger", "reads", "writes", "legacy_touch"]
        miss = [k for k in need if k not in r]
        if miss:
            p.append("row %d missing %s" % (i, ",".join(miss)))
            continue
        if r["kind"] not in PLANINV_KINDS or r["claim"] not in PLANINV_CLAIMS or not str(r["evidence"]).strip():
            p.append("row %d has a kind or claim outside the closed sets, or no evidence" % i)
        if a.shape == "retire":
            if r["replaced_by_claim"] not in PLANINV_CLAIMS or r["decision_owner"] not in ("Andrew", "CTO", "COO", "none") or not str(r["replaced_by"]).strip():
                p.append("row %d replaced_by / decision_owner outside the closed sets" % i)
        else:
            if not isinstance(r["reads"], list) or not isinstance(r["writes"], list) or not isinstance(r["legacy_touch"], bool):
                p.append("row %d reads, writes or legacy_touch has the wrong type" % i)
                continue
            for acc in r["reads"] + r["writes"]:
                if not isinstance(acc, dict) or "bucket" not in acc or acc.get("claim") not in PLANINV_CLAIMS:
                    p.append("row %d has an access without bucket or claim" % i)
                    break
            if r["legacy_touch"]:
                legacy += 1
                if not (r["reads"] or r["writes"]):
                    p.append("row %d is legacy_touch with no read or write" % i)
    if a.shape == "inventory" and a.firm and d.get("firm") != a.firm:
        p.append("firm is %s, want %s" % (d.get("firm"), a.firm))
    blob = json.dumps(rows).lower()
    for need in a.require_text or []:
        if need.lower() not in blob:
            p.append("no row names %s" % need)
    if p:
        print("PLANINV: FAIL " + "; ".join(p[:6]))
        return 1
    if a.shape == "retire":
        print("PLANINV: OK shape=retire rows=%d" % len(rows))
    else:
        print("PLANINV: OK firm=%s rows=%d legacy=%d" % (d.get("firm"), len(rows), legacy))
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
    sub.add_parser("trailsel")
    pi = sub.add_parser("planinv")
    pi.add_argument("--file", required=True)
    pi.add_argument("--shape", choices=("inventory", "retire"), default="inventory")
    pi.add_argument("--firm", default="")
    pi.add_argument("--min", type=int, default=5)
    pi.add_argument("--require-text", nargs="*", default=[])
    sc = sub.add_parser("scrub")
    sc.add_argument("--files", nargs="+", required=True)
    a = ap.parse_args()
    return {"awsdiff": awsdiff, "agree2": agree2, "emiterr": emiterr, "firstchain": firstchain, "dryrun": dryrun, "prescreen": prescreen, "slotcause": slotcause,
            "tfslots": tfslots, "iqlt": iqlt, "switchsample": switchsample, "scrub": scrub, "trailsel": trailsel, "planinv": planinv}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
