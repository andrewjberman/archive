"""NFRA_OPLGTW OG-c-2 probe -- one criterion per call: `og_c2.py AC<n>`.

Prints the measurement with its vintage and denominator, then exactly one line
`VERDICT: PASS-OGC2-AC<n>` or `VERDICT: FAIL-OGC2-AC<n> <reason>`. Exit 0 on PASS, 1 on FAIL.

READ-ONLY: git reads, and AWS Get/List/Head calls through boto3. Nothing is written.

Evidence the order's acts leave in this slot's deliverables, read here when present:
  plans/plan_apply.json            the plan that was applied (else plans/plan_pre_upload.json)
  deploy/build.log, deploy/apply.log   build-and-upload and safe-apply output
  replay/replay.json               {"date": D, "records": [{"master","key","version_id","run_id"}]}
  replay/silver_versions_before.json   {master: {silver key: VersionId}} read before the replay
An absent file is reported as absent -- never as a pass.
"""
from __future__ import annotations

import datetime
import json
import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve()
SLOT = HERE.parent.parent
MERGED = "1f03a3f209"                       # OG-c-1's merge into CLOUD
PKG = "infra/aws/lambda/opal-assets/opal-assets-silver-schwab"
SILVER_TF = "infra/aws/terraform/opal-assets/silver.tf"
FN = "opal-assets-silver-schwab"
BUCKET = "opal-data-assets"
MASTERS = ("08242234", "08335338")
SLUG = "nfra-oplgtw-og-c-2-producer"
SENTINEL = "org/critical_paths/.open_deploys/" + SLUG + ".json"
SIGNOFF = "org/tier1_exec/2.0.0_SA_COO~O/deliverables/NEVER_WIDEN_SIGNOFF_NFRA_OPLGTW_OG_C2.md"
BASELINE = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~2/BASELINE.json"
PRE_DEPLOY_LAST_MODIFIED = "2026-08-30T03:37:41"   # get-function-configuration, read 2026-09-15 ~12:50Z
CLOSURE_SCHEMA = "opal.silver.closure/v1"
CLOSURE_FIELDS = ("schema_version", "master", "date", "run", "expected_source_basis",
                  "required_types", "source_partitions", "non_applicable", "expected_tables",
                  "tables", "objects", "empty", "day_disposition", "outputs", "counts",
                  "inventory_errors", "write_guard", "closure_id", "status", "findings")


def _run(args, cwd=None, binary=False):
    out = subprocess.run(args, cwd=str(cwd or HERE.parent), capture_output=True)
    if out.returncode != 0:
        raise RuntimeError(" ".join(args[:3]) + " rc=" + str(out.returncode) + ": "
                           + out.stderr.decode("utf-8", "replace")[:200])
    return out.stdout if binary else out.stdout.decode("utf-8", "replace")


ROOT = pathlib.Path(_run(["git", "rev-parse", "--show-toplevel"]).strip())


def git(*args, binary=False):
    return _run(["git", *args], cwd=ROOT, binary=binary)


def show(ref_path, binary=False):
    return git("show", ref_path, binary=binary)


def head_short():
    return git("rev-parse", "--short=10", "HEAD").strip()


def now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def client(name):
    import boto3
    return boto3.client(name, region_name="us-east-1")


def vintage():
    print("vintage: " + now() + "  HEAD=" + head_short() + "  worktree=" + str(ROOT))


def slot_json(rel):
    p = SLOT / rel
    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else None


def silver_families():
    tf = show("HEAD:" + SILVER_TF)
    block = re.search(r"silver_families\s*=\s*\{(.*?)\n  \}", tf, re.S)
    return re.findall(r"^\s*([a-z0-9_]+)\s*=\s*\{", block.group(1), re.M) if block else []


def sentinel_add():
    """(commit, ISO time) of the commit that ADDED the ledger sentinel, or (None, None)."""
    log = git("log", "--diff-filter=A", "--format=%H %cI", "--", SENTINEL).split()
    return (log[-2], log[-1]) if len(log) >= 2 else (None, None)


def replay():
    r = slot_json("replay/replay.json")
    if not r or not r.get("records"):
        return None
    return r


# ------------------------------------------------------------------------ criteria
def ac1():
    manifest = json.loads(show("HEAD:" + PKG + "/BUILD_MANIFEST.json"))
    mods = manifest.get("vendored_modules", [])
    print("instrument: git show " + MERGED + ":<module> vs git show HEAD:" + PKG + "/<basename> vs the "
          "worktree bytes; CR byte count of the vendored copy")
    print("denominator: " + str(len(mods)) + " vendored module(s) named by BUILD_MANIFEST.json at HEAD")
    bad = []
    for m in mods:
        base = m.rsplit("/", 1)[1]
        src = show(MERGED + ":" + m, binary=True)
        head = show("HEAD:" + PKG + "/" + base, binary=True)
        wt = (ROOT / PKG / base).read_bytes()
        same = src == head == wt
        cr = wt.count(b"\r")
        print("  " + ("EQUAL " if same and cr == 0 else "DIFFER") + " " + base + " src=" + str(len(src))
              + "B head=" + str(len(head)) + "B worktree=" + str(len(wt)) + "B CR=" + str(cr) + "  <- " + m)
        if not same or cr:
            bad.append(base)
    if not mods:
        return "FAIL", "BUILD_MANIFEST.json names no vendored module"
    if bad:
        return "FAIL", str(len(bad)) + " of " + str(len(mods)) + " vendored module(s) differ from " + MERGED + ": " + ",".join(bad)
    return "PASS", ""


def ac2():
    tf = show("HEAD:" + SILVER_TF)
    m = re.search(r'silver_build_commit\s*=\s*\{[^}]*?schwab\s*=\s*"([0-9a-f]+)"', tf, re.S)
    full = git("rev-parse", MERGED + "^{commit}").strip()
    print("instrument: regex over git show HEAD:" + SILVER_TF + "; git rev-parse " + MERGED)
    print("denominator: 1 pin (silver_build_commit.schwab)")
    if not m:
        return "FAIL", "silver_build_commit.schwab not found in silver.tf at HEAD"
    pin = m.group(1)
    print("silver_build_commit.schwab at HEAD = " + pin + " ; OG-c-1 merged commit = " + full)
    try:
        env = client("lambda").get_function_configuration(FunctionName=FN)["Environment"]["Variables"]
        print("live env OPAL_BUILD_COMMIT (context, not graded) = " + str(env.get("OPAL_BUILD_COMMIT")))
    except Exception as exc:                                        # noqa: BLE001
        print("live env read failed (context only): " + type(exc).__name__)
    if len(pin) >= 7 and full.startswith(pin):
        return "PASS", ""
    return "FAIL", "pin " + pin + " does not name " + full


def ac3():
    fams = silver_families()
    rel = "plans/plan_apply.json" if (SLOT / "plans/plan_apply.json").is_file() else "plans/plan_pre_upload.json"
    plan = slot_json(rel)
    print("instrument: terraform show -json of the saved plan " + rel + " (resource_changes, actions other than no-op/read)")
    if plan is None:
        print("denominator: 0 plans saved")
        return "FAIL", "no saved plan in " + str(SLOT / "plans")
    rcs = plan.get("resource_changes", [])
    changed = [r for r in rcs if set(r["change"]["actions"]) - {"no-op", "read"}]
    print("plan file: " + rel + "  terraform_version=" + str(plan.get("terraform_version"))
          + "  timestamp=" + str(plan.get("timestamp")))
    print("denominator: " + str(len(rcs)) + " resource_changes in the plan; " + str(len(changed))
          + " with an action; " + str(len(fams)) + " silver families " + str(fams))
    prefix = 'module.silver_converter["schwab"].'
    for r in changed:
        print("  " + ("IN-SCOPE " if r["address"].startswith(prefix) else "FOREIGN  ") + r["address"]
              + " " + str(r["change"]["actions"]))
    per_family = {f: sum(1 for r in changed if '["' + f + '"]' in r["address"]) for f in fams}
    print("rows per family: " + json.dumps(per_family, sort_keys=True))
    foreign = [r["address"] for r in changed if not r["address"].startswith(prefix)]
    others = {f: n for f, n in per_family.items() if f != "schwab" and n}
    if not any(r["address"] == prefix + "aws_lambda_function.this" for r in changed):
        return "FAIL", "the plan does not change opal-assets-silver-schwab"
    if foreign or others:
        return "FAIL", str(len(foreign)) + " of " + str(len(changed)) + " changed row(s) are outside opal-assets-silver-schwab: " + ", ".join(foreign)
    return "PASS", ""


def ac4():
    entries = [p for p in git("ls-tree", "-r", "--name-only", "HEAD", "--",
                              "org/critical_paths/change_management/").split() if SLUG in p]
    commit, when = sentinel_add()
    cfg = client("lambda").get_function_configuration(FunctionName=FN)
    lm = cfg["LastModified"]
    apply_log = SLOT / "deploy/apply.log"
    print("instrument: git ls-tree HEAD org/critical_paths/change_management/; git log --diff-filter=A -- "
          + SENTINEL + "; lambda get-function-configuration; " + str(apply_log.relative_to(ROOT)))
    print("denominator: 1 ledger entry sought (slug " + SLUG + "), 1 sentinel, 1 function")
    print("ledger entries at HEAD naming the slug: " + str(entries))
    print("sentinel added by: " + str(commit) + " at " + str(when))
    print("live LastModified=" + lm + "  (pre-deploy value " + PRE_DEPLOY_LAST_MODIFIED + ")")
    print("apply log present: " + str(apply_log.is_file()))
    if not entries or commit is None:
        return "FAIL", "no ledger entry " + SLUG + " at HEAD and no sentinel commit -- no deploy was opened"
    if lm.startswith(PRE_DEPLOY_LAST_MODIFIED):
        return "FAIL", "the function is unchanged since " + PRE_DEPLOY_LAST_MODIFIED + " -- no deploy ran"
    if not apply_log.is_file() or "safe-apply" not in apply_log.read_text(encoding="utf-8", errors="replace"):
        return "FAIL", "no safe-apply output recorded for the deploy"
    t_open = datetime.datetime.fromisoformat(when)
    t_lm = datetime.datetime.fromisoformat(lm.replace("+0000", "+00:00"))
    if t_open >= t_lm:
        return "FAIL", "the ledger commit (" + when + ") does not precede the deploy (" + lm + ")"
    return "PASS", ""


def ac5():
    cfg = client("lambda").get_function_configuration(FunctionName=FN)
    live = cfg["CodeSha256"]
    log = SLOT / "deploy/build.log"
    print("instrument: lambda get-function-configuration CodeSha256 vs the SHA256 build-and-upload.sh printed")
    print("denominator: 1 function, 1 build")
    print("live CodeSha256=" + live + "  LastModified=" + cfg["LastModified"])
    if not log.is_file():
        return "FAIL", "no build ran -- deploy/build.log absent; the live code is the pre-deploy artifact"
    m = re.search(r"SHA256:\s+([A-Za-z0-9+/]{43}=)", log.read_text(encoding="utf-8", errors="replace"))
    built = m.group(1) if m else None
    print("built zip SHA256=" + str(built))
    if built and built == live:
        return "PASS", ""
    return "FAIL", "deployed CodeSha256 " + live + " != built " + str(built)


def ac6():
    text = show("HEAD:" + SIGNOFF)
    log = git("log", "--format=%H %cI %an", "--", SIGNOFF).splitlines()
    print("instrument: git show HEAD:" + SIGNOFF + "; git log -- that path; the ledger sentinel's add commit")
    print("denominator: 2 halves required (1.0.0_SA_CTO, 2.0.0_SA_COO~O); " + str(len(log)) + " commit(s) on the path")
    for line in log:
        print("  commit " + line)
    halves = {}
    parts = re.split(r"(?m)^## ", text)
    for seat in ("2.0.0_SA_COO~O", "1.0.0_SA_CTO"):
        sec = next((p for p in parts if re.match(r"Half \d+ -- `" + re.escape(seat) + r"` -- SIGNED", p)), None)
        halves[seat] = bool(sec)
        # context only, not graded: the adequacy of a half's content is its signer's, not this probe's
        ctx = ("" if not sec else " (context: 'N = 1' " + ("present" if "N = 1" in sec else "absent")
               + ", 'advi-49f-gold-dispatch' " + ("named" if "advi-49f-gold-dispatch" in sec else "not named") + ")")
        print("  half " + seat + ": " + ("SIGNED" if sec else "ABSENT") + ctx)
    cite = SIGNOFF + "@" + (log[0].split()[0][:10] if log else "NONE")
    print("cited: " + cite)
    commit, when = sentinel_add()
    print("deploy's commit (ledger sentinel add): " + str(commit) + " at " + str(when))
    if not all(halves.values()):
        return "FAIL", "the sign-off at HEAD does not carry both halves"
    if commit is None:
        return "FAIL", "no deploy or replay occurred, so no deploy commit exists for the sign-off to precede"
    if datetime.datetime.fromisoformat(log[0].split()[1]) > datetime.datetime.fromisoformat(when):
        return "FAIL", "the sign-off's last commit is later than the deploy's"
    return "PASS", ""


def _records():
    r = replay()
    if r is None:
        return None, []
    s3 = client("s3")
    out = []
    for rec in r["records"]:
        body = s3.get_object(Bucket=BUCKET, Key=rec["key"], VersionId=rec["version_id"])["Body"].read()
        out.append((rec, json.loads(body.decode("utf-8"))))
    return r, out


def ac7():
    r, recs = _records()
    print("instrument: s3 get-object of each replayed record at its VersionId (replay/replay.json)")
    if r is None:
        print("denominator: 0 replayed records (replay/replay.json absent)")
        return "FAIL", "no controlled replay ran (blocked before the deploy) -- 0 of 2 masters carry a replayed record"
    print("denominator: " + str(len(recs)) + " record(s), " + str(len(MASTERS)) + " masters, date " + r["date"])
    per = {m: 0 for m in MASTERS}
    for rec, body in recs:
        c = body.get("closure") or {}
        ok = (c.get("master") == rec["master"] and c.get("date") == r["date"]
              and c.get("status") == "qualified" and (c.get("run") or {}).get("run_id") == rec["run_id"])
        print("  " + rec["master"] + " " + rec["key"] + " v=" + rec["version_id"] + " status="
              + str(c.get("status")) + " run_id=" + str((c.get("run") or {}).get("run_id")) + (" OK" if ok else " NOT-QUALIFIED"))
        if ok:
            per[rec["master"]] = per.get(rec["master"], 0) + 1
    if all(per.get(m) == 1 for m in MASTERS):
        return "PASS", ""
    return "FAIL", "qualified replayed records per master " + json.dumps(per)


def ac8():
    r, recs = _records()
    print("instrument: validate_closure from the vendored " + PKG + "/conversion_manifest.py at this worktree")
    if r is None:
        print("denominator: 0 replayed records")
        return "FAIL", "no controlled replay ran -- nothing to validate"
    sys.path.insert(0, str(ROOT / PKG))
    import conversion_manifest as cm                                 # noqa: E402
    print("denominator: " + str(len(recs)) + " record(s); " + str(len(CLOSURE_FIELDS)) + " fields each")
    bad = 0
    for rec, body in recs:
        c = body.get("closure") or {}
        missing = [f for f in CLOSURE_FIELDS if f not in c]
        v = cm.validate_closure(c)
        ok = not missing and c.get("schema_version") == CLOSURE_SCHEMA and v["status"] == "qualified"
        print("  " + rec["master"] + " validate=" + v["status"] + " findings=" + str(len(v.get("findings", [])))
              + " missing_fields=" + str(missing))
        bad += 0 if ok else 1
    return ("PASS", "") if bad == 0 else ("FAIL", str(bad) + " record(s) do not validate")


def ac9():
    r, recs = _records()
    print("instrument: s3 head-object of every key a replayed record lists, VersionId compared")
    if r is None:
        print("denominator: 0 VersionIds (no replay)")
        return "FAIL", "no controlled replay ran -- no VersionId to match"
    s3 = client("s3")
    n = mism = 0
    for rec, body in recs:
        for o in (body.get("closure") or {}).get("objects", []):
            n += 1
            live = s3.head_object(Bucket=BUCKET, Key=o["key"]).get("VersionId")
            if live != o["version_id"]:
                mism += 1
                print("  MISMATCH " + o["key"] + " record=" + str(o["version_id"]) + " live=" + str(live))
    print("denominator: " + str(n) + " VersionId(s) listed across " + str(len(recs)) + " record(s)")
    return ("PASS", "") if n and not mism else ("FAIL", str(mism) + " of " + str(n) + " VersionIds do not match")


def ac10():
    r = replay()
    before = slot_json("replay/silver_versions_before.json")
    print("instrument: s3 list-objects-v2 + head-object of every silver object for the replayed date, vs the "
          "snapshot read before the replay")
    if r is None or before is None:
        print("denominator: 0 silver objects compared (no replay)")
        return "FAIL", "no controlled replay ran -- there is no before/after to compare"
    s3 = client("s3")
    n = diff = 0
    for m in MASTERS:
        after = {}
        root = "schwab/" + m + "/silver/"
        tables = [p["Prefix"] for p in s3.list_objects_v2(Bucket=BUCKET, Prefix=root, Delimiter="/").get("CommonPrefixes", [])]
        for t in tables:
            for o in s3.list_objects_v2(Bucket=BUCKET, Prefix=t + "date=" + r["date"] + "/").get("Contents", []):
                after[o["Key"]] = s3.head_object(Bucket=BUCKET, Key=o["Key"]).get("VersionId")
        b = before.get(m, {})
        n += len(set(b) | set(after))
        for k in sorted(set(b) | set(after)):
            if b.get(k) != after.get(k):
                diff += 1
                print("  CHANGED " + k + " before=" + str(b.get(k)) + " after=" + str(after.get(k)))
    print("denominator: " + str(n) + " silver object(s) across " + str(len(MASTERS)) + " masters for " + r["date"])
    return ("PASS", "") if n and not diff else ("FAIL", str(diff) + " of " + str(n) + " silver VersionIds changed")


def _notifications(s3):
    resp = s3.get_bucket_notification_configuration(Bucket=BUCKET)
    rows = []
    for c in resp.get("LambdaFunctionConfigurations", []):
        rules = {r["Name"].lower(): r["Value"] for r in c.get("Filter", {}).get("Key", {}).get("FilterRules", [])}
        rows.append((c.get("Id"), c["LambdaFunctionArn"], tuple(sorted(c["Events"])),
                     rules.get("prefix", ""), rules.get("suffix", "")))
    extra = len(resp.get("QueueConfigurations", [])) + len(resp.get("TopicConfigurations", []))
    return sorted(rows), extra, "EventBridgeConfiguration" in resp


def ac11():
    base = json.loads((ROOT / BASELINE).read_text(encoding="utf-8"))
    b4 = base["OGP1-AC4"]["measurement"]
    b9 = base["OGP1-AC9"]["measurement"]
    s3 = client("s3")
    ver = s3.get_bucket_versioning(Bucket=BUCKET).get("Status")
    rules = s3.get_bucket_encryption(Bucket=BUCKET)["ServerSideEncryptionConfiguration"]["Rules"]
    sse = [r["ApplyServerSideEncryptionByDefault"]["SSEAlgorithm"] for r in rules]
    kms = [r["ApplyServerSideEncryptionByDefault"].get("KMSMasterKeyID") for r in rules]
    bke = [r.get("BucketKeyEnabled", False) for r in rules]
    pab = s3.get_public_access_block(Bucket=BUCKET)["PublicAccessBlockConfiguration"]
    pol = s3.get_bucket_policy_status(Bucket=BUCKET)["PolicyStatus"]
    notes, extra, eb = _notifications(s3)
    base_notes = sorted((c["id"], c["target"], tuple(sorted(c["events"])), c["prefix"], c["suffix"])
                        for c in b9["configurations"])
    print("instrument: s3 GetBucketVersioning/GetBucketEncryption/GetPublicAccessBlock/GetBucketPolicyStatus/"
          "GetBucketNotificationConfiguration via boto3, vs " + BASELINE + " OGP1-AC4 (read "
          + base["OGP1-AC4"]["measured_utc"] + ") and OGP1-AC9 (read " + base["OGP1-AC9"]["measured_utc"] + ")")
    print("denominator: 7 bucket values (versioning, encryption, 4 public-access-block flags, policy status) + "
          + str(len(base_notes)) + " baseline notification configuration(s) + the EventBridge flag")
    checks = [
        ("versioning", ver, b4["versioning"]),
        ("sse_algorithm", sse, b4["sse_algorithm"]),
        ("kms_key", kms, b4["kms_key"]),
        ("bucket_key_enabled", bke, b4["bucket_key_enabled"]),
        ("public_access_block", pab, b4["public_access_block"]),
        ("policy_status.IsPublic", pol.get("IsPublic"), b4["policy_status"]["IsPublic"]),
        ("notification_configurations", notes, base_notes),
        ("queue_or_topic_configurations", extra, 0),
        ("eventbridge_enabled", eb, b9["eventbridge_enabled"]),
    ]
    bad = []
    for name, live, want in checks:
        same = live == want
        shown = (str(len(live)) + " configs") if name == "notification_configurations" else str(live)
        print("  " + ("MATCH  " if same else "DIFFERS") + " " + name + " live=" + shown)
        if not same:
            bad.append(name)
    print("read_utc: " + now())
    return ("PASS", "") if not bad else ("FAIL", "differs from the OG-p-1 baseline: " + ",".join(bad))


CRITERIA = {"AC1": ac1, "AC2": ac2, "AC3": ac3, "AC4": ac4, "AC5": ac5, "AC6": ac6,
            "AC7": ac7, "AC8": ac8, "AC9": ac9, "AC10": ac10, "AC11": ac11}


def main(argv):
    if len(argv) != 2 or argv[1] not in CRITERIA:
        print("usage: og_c2.py AC1..AC11")
        return 2
    cid = argv[1]
    vintage()
    try:
        verdict, reason = CRITERIA[cid]()
    except Exception as exc:                                        # noqa: BLE001
        verdict, reason = "FAIL", "probe error " + type(exc).__name__ + ": " + str(exc)[:200]
    n = cid[2:]
    print("VERDICT: " + verdict + "-OGC2-AC" + n + ((" " + reason) if reason else ""))
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
