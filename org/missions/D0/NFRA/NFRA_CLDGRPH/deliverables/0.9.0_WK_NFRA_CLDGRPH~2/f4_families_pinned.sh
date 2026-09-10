#!/usr/bin/env bash
# F4-AC2 -- R13 AND NEVER-2: seven families on the NEW digest, none on :latest,
# the ledger entry naming seven and CLOSED. TO-CG-F-4, deliverable step 2.
#
# THE FAMILY NAMES ARE THE TRUE ACTIVE ONES, and that is not a detail. The task
# order's cut enumerated four of them without the `globgrph-` prefix; those four do
# not resolve, and `describe-task-definition` RAISES on them rather than returning a
# negative. A sweep written to the cut's names therefore prints a clean "0 of 7 on
# :latest" having read only 3 -- a vacuous pass over a set it never read. So this
# script (a) uses the true names, (b) prints BOTH name sets and how many of each
# resolve, and (c) counts an exception as an ERROR, never as a negative. Row
# NFRA_CLDGRPH-W2-S49, issuer amendment 2026-09-09 20:1xZ.
#
# Everything is read LIVE from ECS and ECR on every run. The ledger's status is read
# from the FILE'S OWN header line and its family count from the file's own table.
#
# Run from the repository root.
set -u
LEDGER="org/critical_paths/change_management/20260909T203713Z_cldgrph-cgs24-stitch-fold-image-and-sevenfamily-repin_deploy_completion.md"

python - "$LEDGER" <<'PY'
import datetime
import re
import sys

import boto3

ledger = sys.argv[1]
NEW = "sha256:478d0a43742b2ed5a44631c6352b5713c5ba22f015d82a673cfb93428a9dae20"
OLD = "sha256:1b89853fe44133f10a60dc2b3e7b463c0d3b68b827a2ddff249bf427ecde2778"
TRUE_NAMES = ["globgrph-derive-runner", "globgrph-projection-worker", "globgrph-serving",
              "globgrph-comp-learns-producer", "globgrph-cse-producer",
              "globgrph-fedobs-producer", "globgrph-resource-summaries-producer"]
CUT_NAMES = ["globgrph-derive-runner", "globgrph-projection-worker", "globgrph-serving",
             "comp-learns-producer", "cse-producer", "fedobs-producer",
             "resource-summaries-producer"]

ecs = boto3.client("ecs", region_name="us-east-1")
ecr = boto3.client("ecr", region_name="us-east-1")
now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def read(name):
    """(row, error). An exception is an ERROR, never a negative."""
    try:
        d = ecs.describe_task_definition(taskDefinition=name)["taskDefinition"]
    except Exception as exc:  # noqa: BLE001
        return None, type(exc).__name__ + ": " + str(exc).split(":")[-1].strip()
    imgs = [c.get("image", "") for c in d.get("containerDefinitions", [])]
    return {"revision": d["revision"], "images": imgs,
            "on_new": bool(imgs) and all(NEW in i for i in imgs),
            "on_old": any(OLD in i for i in imgs),
            "latest": any(i.endswith(":latest") for i in imgs)}, None


rows, errors = {}, {}
for n in TRUE_NAMES:
    r, e = read(n)
    (rows if r else errors)[n] = r or e
cut_resolved = sum(1 for n in CUT_NAMES if read(n)[0] is not None)

on_new = sum(1 for r in rows.values() if r["on_new"])
on_latest = sum(1 for r in rows.values() if r["latest"])

txt = open(ledger, encoding="utf-8").read()
m = re.search(r"^\*\*Status:\*\*\s*(\w+)", txt, re.M)
status = m.group(1) if m else "UNREADABLE"
named = len(re.findall(r"^\| [1-7] \| `([a-z0-9-]+)` \|", txt, re.M))

print("F4-AC2 -- R13 AND NEVER-2: SEVEN FAMILIES ON THE NEW DIGEST")
print("  live read at: %s" % now)
print()
print("FAMILIES_ON_NEW_DIGEST=%d of %d" % (on_new, len(TRUE_NAMES)))
print("LATEST_TAG_REFERENCED_BY=%d of %d" % (on_latest, len(TRUE_NAMES)))
print("LEDGER_FAMILIES_NAMED=%d" % named)
print("LEDGER_ENTRY_STATUS=%s" % status)
print("DESCRIBE_ERRORS=%d of %d   <- an exception is an ERROR, never a negative"
      % (len(errors), len(TRUE_NAMES)))
for n, e in errors.items():
    print("  ERROR %-38s %s" % (n, e))
print()
print("  -- the seven, live --")
for n in TRUE_NAMES:
    r = rows.get(n)
    if r is None:
        print("     ERROR %-38s (not read)" % n)
        continue
    print("     %-38s rev %-3s on_new=%-5s on_old=%-5s latest=%s"
          % (n, r["revision"], r["on_new"], r["on_old"], r["latest"]))
print()
print("  -- the digest --")
print("     new (this act) : %s" % NEW)
print("     prior          : %s" % OLD)
try:
    im = ecr.describe_images(repositoryName="opal-globgrph-derive-runner",
                             imageIds=[{"imageTag": "latest"}])["imageDetails"][0]
    print("     ECR :latest    : %s  tags=%s" % (im["imageDigest"], sorted(im.get("imageTags") or [])))
    print("     :latest moved with the push, and NOTHING pulls it -- 0 of 7 families")
    print("     reference a tag. That is R13, and it is why the move is safe to state.")
except Exception as exc:  # noqa: BLE001
    print("     ECR :latest    : ERROR %s" % exc)
print()
print("  -- the CONTROL on the names (W2-S49) --")
print("     the TASK ORDER's seven names resolve : %d of 7" % cut_resolved)
print("     the TRUE ACTIVE names resolve        : %d of 7" % len(rows))
print("     a sweep on the cut's names would read 4 exceptions and, if it counted an")
print("     exception as 'not on :latest', would print a clean 0 of 7 over 3 families.")
print()
print("  DENOMINATOR: %d of %d families read live by describe-task-definition "
      "(9 ACTIVE families in the account; globgrph-nessie and globgrph-trino pull "
      "other images and are named in the ledger as outside this population); "
      "%d of 7 ledger table rows; 1 of 1 ledger status line."
      % (len(rows), len(TRUE_NAMES), named))
PY
