"""battery_ib_rth_6.py -- TO IRPT_BCKEND.TO-IB-rth-6, criterion R81-AC1.

STOP DISPOSITION (see the surprise row cited below): arm (c).1's literal instruction (update
scopes.json's inflection/cottonwood `bucket` field to opal-data-inflectionwealth /
opal-data-cottonwoodcapital while leaving key/short/aliases untouched) is REFUSED by the
registry's own validator (python lib/opal_naming.py validate): a FIRM row's bucket MUST equal
"opal-data-{long}" (lib/opal_naming.py:365-366) and key MUST equal long (:357-358), so the
requested bucket rename is impossible without renaming the firm itself -- contradicting the
task's own framing ("this is a bucket swap, not a firm rename") and its bound against touching
key/short/aliases. Row: IRPT_BCKEND-W6-S1 (surprise-channel/investigations/INVESTIGATION_v1.md).

Consequently: no registry edit was committed, no exemptions.json edit was made, and no Terraform
apply was attempted -- the premise the apply depends on (a VALID registry naming the new bucket
names) never existed. This battery measures and reports the ACTUAL, unchanged state: the two new
buckets do NOT exist (never created); the two old buckets are unchanged from their known-locked
state. It cannot print the criterion's <expect> token
(IBR81-NEW-BUCKETS-EXEMPT-IDENTITIES-SUCCEED-OLD-BUCKETS-STILL-DENY) truthfully, because the "new
buckets" half of that claim never came into existence. It prints the actual state instead, and
exits non-zero.

Run: py -3.12 battery_ib_rth_6.py
"""
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[7] / ".tools"))
from msys_argv_guard import msys_safe_run  # noqa: E402  (aws is an MSYS-linked shim; CLAUDE.md Rule 22a)

AWS = "aws"  # resolved via the .tools/aws shim already on PATH per CLAUDE.md Git section

OLD_BUCKETS = ["opal-data-inflection", "opal-data-cottonwood"]
NEW_BUCKETS = ["opal-data-inflectionwealth", "opal-data-cottonwoodcapital"]


def run(*args):
    r = msys_safe_run([AWS] + list(args), capture_output=True, text=True, timeout=60)
    return r.returncode, r.stdout.strip(), r.stderr.strip()


def head_bucket(bucket):
    rc, out, err = run("s3api", "head-bucket", "--bucket", bucket)
    return rc, out, err


def arm_a_registry_state():
    print("== arm (a): measured registry state (should be UNCHANGED from CLOUD HEAD) ==")
    with open("infra/logic/registry/scopes.json", encoding="utf-8") as f:
        scopes = json.load(f)["scopes"]
    seen = {}
    for s in scopes:
        if s.get("key") in ("inflection", "cottonwood"):
            seen[s["key"]] = (s.get("bucket"), s.get("bucket_provisioned"))
            print("  %s: bucket=%s bucket_provisioned=%s" % (s["key"], s.get("bucket"), s.get("bucket_provisioned")))
    ok = seen.get("inflection") == ("opal-data-inflection", True) and \
        seen.get("cottonwood") == ("opal-data-cottonwood", True)
    print("  registry unchanged from pre-cell baseline: %s" % ok)
    return ok


def arm_b_validate_refusal():
    print("== arm (b): python lib/opal_naming.py validate on the UNCHANGED registry (must be OK) ==")
    r = subprocess.run([sys.executable, "lib/opal_naming.py", "validate"], capture_output=True, text=True, timeout=60)
    last_line = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else "(no output)"
    print("  " + last_line)
    return "VALIDATE: OK" in last_line


def arm_c_new_buckets_absent():
    print("== arm (c): head-bucket on the two WOULD-BE new buckets (expect NOT FOUND -- never created) ==")
    all_absent = True
    for b in NEW_BUCKETS:
        rc, out, err = head_bucket(b)
        print("  %s -> rc=%s err=%s" % (b, rc, err[:200]))
        if rc == 0:
            all_absent = False
            print("  UNEXPECTED: %s exists (this battery expected it to be absent under the STOP disposition)" % b)
    return all_absent


def arm_d_old_buckets_unchanged():
    print("== arm (d): head-bucket on the two OLD buckets as Andrew_Berman (expect AccessDenied -- unchanged lockout) ==")
    rc, out, err = run("sts", "get-caller-identity")
    print("  identity: %s" % out.replace("\n", " "))
    all_denied = True
    for b in OLD_BUCKETS:
        rc, out, err = head_bucket(b)
        denied = ("AccessDenied" in err) or ("403" in err) or (rc != 0 and "Forbidden" in err)
        print("  %s -> rc=%s err=%s denied=%s" % (b, rc, err[:200], denied))
        if not denied:
            all_denied = False
    return all_denied


def main():
    reg_ok = arm_a_registry_state()
    val_ok = arm_b_validate_refusal()
    new_absent = arm_c_new_buckets_absent()
    old_unchanged = arm_d_old_buckets_unchanged()

    print()
    print("== VERDICT ==")
    print("registry unchanged: %s | validate OK on unchanged registry: %s | new buckets absent: %s | "
          "old buckets still denied (no regression): %s" % (reg_ok, val_ok, new_absent, old_unchanged))
    if reg_ok and val_ok and new_absent and old_unchanged:
        print("IBR81-STOP-NEW-BUCKETS-NOT-CREATED-REGISTRY-REFUSED-OLD-BUCKETS-UNCHANGED")
        print("This is NOT the criterion's expected token. The criterion's <expect> "
              "(IBR81-NEW-BUCKETS-EXEMPT-IDENTITIES-SUCCEED-OLD-BUCKETS-STILL-DENY) requires the "
              "two new buckets to exist and be exempt-identity-accessible; per row "
              "IRPT_BCKEND-W6-S1, the registry edit that would let them be created is REFUSED by "
              "lib/opal_naming.py validate as written, so this cell is STOPPED short of that state.")
        sys.exit(1)
    else:
        print("IBR81-STOP-STATE-NOT-AS-EXPECTED -- one of the four measured facts above diverged from "
              "the documented STOP baseline; see output above.")
        sys.exit(2)


if __name__ == "__main__":
    main()
