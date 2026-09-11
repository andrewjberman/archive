#!/usr/bin/env python3
"""IB-s-17 acceptance battery -- S17-AC1, five arms, every count beside its denominator.

Prints IBS17-STORAGE-APPLIED on the last line ONLY when all five arms hold.

  (a) THE BUCKET IS THERE, ENCRYPTED, CLOSED.
  (b) THE LAYOUT IS DECLARED FROM THE REGISTRY.
  (c) TABLES AND QUEUES, N OF N.
  (d) THE KEY GRAMMAR REFUSES A CLIENT NAME -- THE DIFFERENCE CONTROL.
  (e) THE LEDGER IS CLOSED AND ITS SENTINEL COMMITTED.

EVERY ARM READS THE APPLIED PLANE, NOT THE RECORD OF IT. No arm reads terraform state,
the plan, or the apply log: state is a DESCRIPTION and this criterion is about what is
actually there. Arm (b) is the exception and says so -- layout.json is a declaration by
construction, so it is compared against the registry it claims to be derived from.

READ-ONLY. No write of any kind: no PutObject, no SendMessage, no PutItem, no apply.
No vendor call, no mailbox read. Every AWS call is a describe/get/head.
"""
from __future__ import annotations

import importlib.util
import io
import json
import os
import subprocess
import sys

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    "..", "..", "..", "..", "..", "..", ".."))
CORE = os.path.join(REPO, "infra", "aws", "terraform", "investor-reporting", "core")
KEYS_DIR = os.path.join(REPO, "infra", "aws", "lambda", "investor-reporting", "_keys")
LAYOUT = os.path.join(CORE, "layout.json")
REGISTRY = os.path.join(REPO, "data", "firm_registry.json")
SENTINEL = "org/critical_paths/.open_deploys/irpt-bckend-s17.json"
SLUG = "irpt-bckend-s17"
BUCKET = "opal-data-ycharts"
ALIAS = "alias/investor-reporting"
TABLES = ["irpt-requests", "irpt-jobs", "irpt-outbox", "irpt-checkpoints"]
QUEUE_BASES = ["irpt-intake", "irpt-generation", "irpt-export"]

FAILS = []
ARMS = {}
AWS_CALLS = []


def fail(arm, msg):
    FAILS.append("%s: %s" % (arm, msg))
    print("ERROR: [%s] %s" % (arm, msg))


def check(arm, cond, msg):
    if not cond:
        fail(arm, msg)
    return bool(cond)


def _bash_argv(script, *args):
    """Resolve Git Bash EXPLICITLY. A bare `bash` on this box is the WSL stub, which
    fails with a UTF-16 'no installed distribution' message that looks nothing like an
    AWS error -- so the resolver is not a nicety, it is what makes the arm's failures
    mean what they say."""
    spec = importlib.util.spec_from_file_location(
        "gbr", os.path.join(REPO, ".tools", "git_bash_resolver.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.bash_argv(script, *args)


def aws(*args):
    """One AWS read through the estate's own shim. Returns (rc, parsed_json_or_text)."""
    argv = _bash_argv(os.path.join(REPO, ".tools", "aws"), *args)
    r = subprocess.run(argv, capture_output=True, cwd=REPO)
    AWS_CALLS.append(" ".join(args))
    out = r.stdout.decode("utf-8", "replace").replace("\r\n", "\n").strip()
    err = r.stderr.decode("utf-8", "replace").replace("\r\n", "\n").strip()
    if r.returncode != 0:
        return r.returncode, err
    if not out:
        return 0, {}
    try:
        return 0, json.loads(out)
    except ValueError:
        return 0, out


def git(*args):
    r = subprocess.run(["git"] + list(args), capture_output=True, cwd=REPO)
    return r.returncode, r.stdout.decode("utf-8", "replace").replace("\r\n", "\n").strip()


def registry_client_firms():
    with io.open(REGISTRY, encoding="utf-8") as fh:
        reg = json.load(fh)
    return tuple(sorted(f["firm_id"] for f in reg["firms"]
                        if f.get("enabled") is True and f.get("kind") == "client"))


# ------------------------------------------------------------------ arm (a)
def arm_a(key_arn):
    print("")
    print("(a) THE BUCKET IS THERE, ENCRYPTED, CLOSED.")
    ok = True

    rc, out = aws("s3api", "head-bucket", "--bucket", BUCKET)
    print("    head-bucket %s -> rc=%d %s" % (BUCKET, rc, "200 OK (no body)" if rc == 0 else out[:120]))
    ok = check("a", rc == 0, "head-bucket did not return 200: %s" % str(out)[:160]) and ok

    rc, enc = aws("s3api", "get-bucket-encryption", "--bucket", BUCKET, "--output", "json")
    rule = {}
    if rc == 0 and isinstance(enc, dict):
        rules = enc.get("ServerSideEncryptionConfiguration", {}).get("Rules", [])
        rule = (rules[0] if rules else {}).get("ApplyServerSideEncryptionByDefault", {})
    algo = rule.get("SSEAlgorithm")
    kms_id = rule.get("KMSMasterKeyID")
    print("    get-bucket-encryption -> SSEAlgorithm=%s KMSMasterKeyID=%s" % (algo, kms_id))
    ok = check("a", algo == "aws:kms", "SSEAlgorithm is %r, not aws:kms" % algo) and ok
    # The criterion says the encryption must name the alias/investor-reporting KEY. A string
    # compare against the alias would pass on a bucket encrypted with a DIFFERENT key that
    # happened to carry a similar arn, so the alias is RESOLVED and the key ids compared.
    print("    alias %s resolves to key arn %s" % (ALIAS, key_arn))
    ok = check("a", kms_id == key_arn,
               "bucket key %r is not the alias/investor-reporting key %r" % (kms_id, key_arn)) and ok

    rc, pab = aws("s3api", "get-public-access-block", "--bucket", BUCKET, "--output", "json")
    cfg = pab.get("PublicAccessBlockConfiguration", {}) if isinstance(pab, dict) else {}
    axes = ["BlockPublicAcls", "IgnorePublicAcls", "BlockPublicPolicy", "RestrictPublicBuckets"]
    on = [a for a in axes if cfg.get(a) is True]
    print("    get-public-access-block -> %s" % json.dumps(cfg, sort_keys=True))
    print("      %d of %d axis(es) true" % (len(on), len(axes)))
    ok = check("a", len(on) == 4, "public access block is not all four: %r" % cfg) and ok

    rc, ver = aws("s3api", "get-bucket-versioning", "--bucket", BUCKET, "--output", "json")
    status = ver.get("Status") if isinstance(ver, dict) else None
    print("    get-bucket-versioning -> Status=%s" % status)
    ok = check("a", status == "Enabled", "versioning is %r, not Enabled" % status) and ok

    ARMS["a"] = ok
    return ok


# ------------------------------------------------------------------ arm (b)
def arm_b():
    print("")
    print("(b) THE LAYOUT IS DECLARED FROM THE REGISTRY.")
    print("    NOTE: this is the one arm that reads a FILE rather than the applied plane,")
    print("    because layout.json IS a declaration -- the claim under test is that it was")
    print("    derived from the registry, and the registry is the only thing that can show it.")
    ok = True
    if not os.path.exists(LAYOUT):
        fail("b", "layout.json was not written by the apply: %s" % LAYOUT)
        ARMS["b"] = False
        return False
    with io.open(LAYOUT, encoding="utf-8") as fh:
        layout = json.load(fh)

    expected = registry_client_firms()
    declared = tuple(layout.get("firms") or ())
    print("    registry enabled client firms: %s" % list(expected))
    print("    layout.json firms            : %s" % list(declared))
    print("    %d of %d firm id(s) match the registry" % (
        len([f for f in declared if f in expected]), len(expected)))
    ok = check("b", declared == expected,
               "layout firms %r != registry %r" % (declared, expected)) and ok

    q = layout.get("quarantine")
    print("    quarantine prefix -> %r" % q)
    ok = check("b", q == "quarantine/", "quarantine prefix is %r" % q) and ok
    for firm in declared:
        ok = check("b", firm not in str(q), "the quarantine prefix must carry no firm") and ok

    families = layout.get("prefix_families") or {}
    per_firm = layout.get("firm_prefixes") or {}
    print("    prefix families declared: %s" % sorted(families))
    ok = check("b", sorted(families) == ["generations", "intake", "requests"],
               "prefix families are %r" % sorted(families)) and ok
    present = 0
    for firm in expected:
        fam = per_firm.get(firm) or {}
        got = sorted(fam)
        rendered_ok = all(fam.get(k, "").startswith("firms/%s/" % firm) for k in got)
        print("      %-12s %d of 3 family prefix(es): %s" % (firm, len(got), sorted(fam.values())))
        if got == ["generations", "intake", "requests"] and rendered_ok:
            present += 1
        else:
            fail("b", "%s does not carry the three rendered family prefixes" % firm)
            ok = False
    print("    %d of %d firm(s) carry all three prefix families" % (present, len(expected)))

    # The runtime library and the declaration are two carriers of one fact; this is the
    # comparison that keeps them from drifting.
    sys.path.insert(0, KEYS_DIR)
    import keys  # noqa: E402
    agreed, diffs = keys.verify_against_layout(LAYOUT)
    print("    _keys/keys.py vs layout.json: %s%s" % ("AGREE" if agreed else "DIFFER", "" if agreed else " %r" % diffs))
    ok = check("b", agreed, "the key library and the declared layout disagree: %r" % diffs) and ok

    # No empty prefix object was created: the layout is a declaration, not a directory tree.
    rc, listing = aws("s3api", "list-objects-v2", "--bucket", BUCKET, "--max-items", "10", "--output", "json")
    n = len(listing.get("Contents", [])) if isinstance(listing, dict) else -1
    print("    list-objects-v2 -> %d object(s) in the bucket (expected 0: prefixes are DECLARED, never created as empty objects)" % n)
    ok = check("b", n == 0, "the bucket is not empty: %d object(s)" % n) and ok

    ARMS["b"] = ok
    return ok


# ------------------------------------------------------------------ arm (c)
def arm_c(key_arn):
    print("")
    print("(c) TABLES AND QUEUES, N OF N.")
    ok = True
    good = 0
    for name in TABLES:
        rc, out = aws("dynamodb", "describe-table", "--table-name", name, "--output", "json")
        if rc != 0:
            fail("c", "describe-table %s failed: %s" % (name, str(out)[:120]))
            ok = False
            continue
        t = out.get("Table", {})
        sse = t.get("SSEDescription", {})
        billing = t.get("BillingModeSummary", {}).get("BillingMode")
        rc2, cb = aws("dynamodb", "describe-continuous-backups", "--table-name", name, "--output", "json")
        pitr = (cb.get("ContinuousBackupsDescription", {})
                  .get("PointInTimeRecoveryDescription", {}).get("PointInTimeRecoveryStatus")
                if isinstance(cb, dict) else None)
        keys_desc = ",".join("%s:%s" % (k["AttributeName"], k["KeyType"]) for k in t.get("KeySchema", []))
        row_ok = (sse.get("Status") == "ENABLED" and sse.get("SSEType") == "KMS"
                  and sse.get("KMSMasterKeyArn") == key_arn
                  and billing == "PAY_PER_REQUEST" and pitr == "ENABLED")
        print("    %-18s keys=%-28s SSE=%s/%s PITR=%s billing=%s key-is-ours=%s"
              % (name, keys_desc, sse.get("Status"), sse.get("SSEType"), pitr, billing,
                 sse.get("KMSMasterKeyArn") == key_arn))
        if row_ok:
            good += 1
        else:
            fail("c", "%s: SSE/PITR/billing not as required" % name)
            ok = False
    print("    %d of %d table(s) SSE-KMS with OUR key, PITR enabled, PAY_PER_REQUEST" % (good, len(TABLES)))
    ok = check("c", good == len(TABLES), "tables %d of %d" % (good, len(TABLES))) and ok

    qgood = 0
    dgood = 0
    for base in QUEUE_BASES:
        for suffix in ("", "-dlq"):
            name = base + suffix
            rc, url = aws("sqs", "get-queue-url", "--queue-name", name, "--output", "json")
            if rc != 0:
                fail("c", "get-queue-url %s failed: %s" % (name, str(url)[:120]))
                ok = False
                continue
            qurl = url.get("QueueUrl")
            rc, attrs = aws("sqs", "get-queue-attributes", "--queue-url", qurl,
                            "--attribute-names", "All", "--output", "json")
            a = attrs.get("Attributes", {}) if isinstance(attrs, dict) else {}
            kms = a.get("KmsMasterKeyId")
            maxsize = a.get("MaximumMessageSize")
            redrive = a.get("RedrivePolicy")
            if suffix == "":
                names_dlq = bool(redrive) and (base + "-dlq") in redrive
                row_ok = bool(kms) and names_dlq and maxsize == "4096"
                print("    %-22s KmsMasterKeyId=%-38s MaxMessageSize=%s RedrivePolicy names %s-dlq=%s"
                      % (name, kms, maxsize, base, names_dlq))
                if row_ok:
                    qgood += 1
                else:
                    fail("c", "%s: kms=%r redrive_names_dlq=%s maxsize=%r" % (name, kms, names_dlq, maxsize))
                    ok = False
            else:
                row_ok = bool(kms) and maxsize == "4096"
                print("    %-22s KmsMasterKeyId=%-38s MaxMessageSize=%s (dead-letter target)"
                      % (name, kms, maxsize))
                if row_ok:
                    dgood += 1
                else:
                    fail("c", "%s: kms=%r maxsize=%r" % (name, kms, maxsize))
                    ok = False
    print("    %d of %d work queue(s) KMS-encrypted with a RedrivePolicy naming their DLQ" % (qgood, len(QUEUE_BASES)))
    print("    %d of %d dead-letter queue(s) KMS-encrypted" % (dgood, len(QUEUE_BASES)))
    print("    MaximumMessageSize 4096 on 6 of 6: an attachment cannot fit, so 'ids not")
    print("      attachments' is refused by the TRANSPORT and not only by the producer.")
    ok = check("c", qgood == 3 and dgood == 3, "queues %d/%d dlqs %d/%d" % (qgood, 3, dgood, 3)) and ok

    ARMS["c"] = ok
    return ok


# ------------------------------------------------------------------ arm (d)
def arm_d():
    print("")
    print("(d) THE KEY GRAMMAR REFUSES A CLIENT NAME -- THE DIFFERENCE CONTROL.")
    test = os.path.join(KEYS_DIR, "tests", "test_keys.py")
    r = subprocess.run([sys.executable, "-m", "pytest", test, "-q", "--color=no"],
                       capture_output=True, cwd=REPO)
    out = r.stdout.decode("utf-8", "replace").replace("\r\n", "\n")
    tail = [ln for ln in out.strip().split("\n") if ln.strip()][-1:]
    passed = failed = 0
    for ln in out.split("\n"):
        if " passed" in ln or " failed" in ln:
            for tok in ln.replace(",", " ").split():
                if tok.isdigit():
                    nxt = ln.split(tok, 1)[1].strip().split(" ")[0]
                    if nxt.startswith("passed"):
                        passed = int(tok)
                    elif nxt.startswith("failed"):
                        failed = int(tok)
    total = passed + failed
    print("    python -m pytest %s -q" % os.path.relpath(test, REPO).replace("\\", "/"))
    print("    %s" % (tail[0] if tail else "(no summary line)"))
    print("    %d of %d test(s) passed, %d failed" % (passed, total, failed))
    ok = check("d", r.returncode == 0 and failed == 0 and passed > 0,
               "pytest rc=%d passed=%d failed=%d" % (r.returncode, passed, failed))

    # The four arms the criterion names, exercised HERE too rather than only inside pytest,
    # so this battery's own output carries them and a reader need not open the test file.
    sys.path.insert(0, KEYS_DIR)
    import keys  # noqa: E402
    base = dict(tenant="49financial", account_set_fingerprint="a" * 64, source_revision="src-1",
                schema_revision="sch-1", config_revision="cfg-1", operation="holdings_snapshot",
                params={"as_of": "2026-09-09"})
    k1 = keys.cache_key(**base)
    components = {"tenant": "49financial", "account-set fingerprint": "a" * 64,
                  "source revision": "src-1", "schema revision": "sch-1",
                  "config revision": "cfg-1", "operation": "holdings_snapshot",
                  "operation parameter": "as_of=2026-09-09"}
    carried = [n for n, v in components.items() if v in k1]
    print("    a well-formed key: %s" % k1)
    print("    %d of %d II.3 component(s) present in the key: %s"
          % (len(carried), len(components), ", ".join(carried)))
    ok = check("d", len(carried) == len(components), "components carried %d of %d"
               % (len(carried), len(components))) and ok

    refused = 0
    names = ["Smith Family", "Smith-Family", "smith family trust", "cottonwood", "blackdiamond"]
    for name in names:
        try:
            keys.cache_key(**dict(base, params={"client": name}))
            fail("d", "a key built with client-name component %r did NOT raise" % name)
            ok = False
        except keys.KeyComponentRefused:
            refused += 1
    print("    %d of %d client/firm-name component(s) REFUSED at construction" % (refused, len(names)))

    k2 = keys.cache_key(**base)
    k3 = keys.cache_key(**dict(base, account_set_fingerprint="b" * 64))
    print("    idempotent: same inputs give the same key -> %s" % (k1 == k2))
    print("    discriminating: a different account-set fingerprint gives a different key -> %s" % (k1 != k3))
    ok = check("d", k1 == k2, "the key builder is not idempotent") and ok
    ok = check("d", k1 != k3, "two fingerprints produced the same key") and ok

    ARMS["d"] = ok
    return ok


# ------------------------------------------------------------------ arm (e)
def arm_e():
    print("")
    print("(e) THE LEDGER IS CLOSED AND ITS SENTINEL COMMITTED.")
    r = subprocess.run([sys.executable, os.path.join(REPO, ".tools", "deploy_ledger.py"), "check"],
                       capture_output=True, cwd=REPO)
    out = (r.stdout.decode("utf-8", "replace") + r.stderr.decode("utf-8", "replace")).replace("\r\n", "\n")
    mine = [ln for ln in out.split("\n") if SLUG in ln]
    print("    deploy_ledger.py check -> rc=%d" % r.returncode)
    for ln in out.strip().split("\n")[:6]:
        print("      %s" % ln)
    print("    line(s) naming this slug: %d" % len(mine))
    for ln in mine:
        print("      %s" % ln)
    ok = check("e", not any("OPEN" in ln for ln in mine),
               "deploy_ledger check still reports this slug OPEN: %r" % mine)

    rc, h = git("log", "-1", "--format=%H", "--", SENTINEL)
    print("    git log -1 --format=%%H -- %s" % SENTINEL)
    print("      %s" % (h if h else "(no commit -- the sentinel was never committed)"))
    ok = check("e", bool(h), "the sentinel has no commit") and ok

    rc, status = git("status", "--porcelain", "--", SENTINEL)
    print("    working-tree status of the sentinel: %s" % (status if status else "clean (committed, no pending change)"))
    ok = check("e", not status, "the sentinel has an uncommitted change: %r" % status) and ok

    ARMS["e"] = ok
    return ok


def main():
    print("IB-s-17 BATTERY -- S17-AC1, five arms. READ-ONLY: no write, no vendor call, no apply.")
    print("repo %s" % REPO)

    rc, k = aws("kms", "describe-key", "--key-id", ALIAS, "--output", "json")
    key_arn = k.get("KeyMetadata", {}).get("Arn") if isinstance(k, dict) else None
    rotation = None
    if key_arn:
        rc2, rot = aws("kms", "get-key-rotation-status", "--key-id", ALIAS, "--output", "json")
        rotation = rot.get("KeyRotationEnabled") if isinstance(rot, dict) else None
    print("the system key: %s -> %s (rotation=%s)" % (ALIAS, key_arn, rotation))
    if not key_arn:
        fail("pre", "the alias %s does not resolve to a key: %s" % (ALIAS, str(k)[:160]))

    arm_a(key_arn)
    arm_b()
    arm_c(key_arn)
    arm_d()
    arm_e()

    print("")
    print("AWS calls made by this battery: %d, all read-only (%s)"
          % (len(AWS_CALLS), ", ".join(sorted({c.split()[1] for c in AWS_CALLS}))))
    held = sum(1 for v in ARMS.values() if v)
    print("arms: %d of 5 evaluated; arms holding: %d of 5; assertions failed: %d"
          % (len(ARMS), held, len(FAILS)))
    for f in FAILS:
        print("  FAILED -- %s" % f)
    if len(ARMS) == 5 and held == 5 and not FAILS:
        print("IBS17-STORAGE-APPLIED")
        return 0
    print("BLOCKED: the token is withheld -- %d of 5 arm(s) held" % held)
    return 1


if __name__ == "__main__":
    sys.exit(main())
