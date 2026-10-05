"""RIV-iam-1 AC1 (row Z-S31; CTO~Z msg 29806: "a simulate arm (deny then allow, plus a sibling-prefix negative control)"): the two
round-9 tables are granted to the roles that run them. Measured 2026-10-05: the D12 Step B refresh republish failed
holding_contribution with "etfs-rivalfunds-daily-role ... not authorized to perform: s3:ListBucket on opal-data-etfs" (the
gold/security_names read, RIV-nm-3), and the sweep's security_universe write (RIV-su-2) has no grant either; `gen_policies.py`
names neither prefix (patch: deliverables/2.0.0_SA_COO~RV/round9/Z-S31_IAM_GRANT_FOR_AE.patch).

Interface (prescribed): `infra/aws/terraform/etfs-rivalfunds/gen_policies.py` grants the publish-page stage (and so the daily
union role) Get + List on `rivalfunds/etfs/gold/security_names/` and Put + Get + List on `rivalfunds/etfs/gold/security_universe/`,
regenerated and applied; nothing else widens.
Instrument: `aws iam simulate-principal-policy` against the LIVE roles (read-only), for both `etfs-rivalfunds-daily-role` and
`rivalfunds-publish-page-role`:
  - (a) s3:ListBucket on the bucket with s3:prefix rivalfunds/etfs/gold/security_names/ and s3:GetObject on a key under it: allowed;
  - (b) s3:PutObject and s3:GetObject on a key under rivalfunds/etfs/gold/security_universe/: allowed;
  - (c) control: s3:PutObject on rivalfunds/etfs/gold/security_names/ (read-only grant) and s3:GetObject under the sibling prefix
    rivalfunds/etfs/gold/security_namesX/: denied;
  - (d) positive control: s3:GetObject on rivalfunds/etfs/gold/holding_contribution/ (granted since round 5): allowed -- the
    simulator can say allowed.
FAIL at base (before the apply): (a) and (b) FAIL (implicitDeny); (c) and (d) PASS."""
import json
import pathlib
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

ACCOUNT = "313476888478"
BUCKET = "opal-data-etfs"
ROLES = ("etfs-rivalfunds-daily-role", "rivalfunds-publish-page-role")
P = "rivalfunds/etfs/gold"


def simulate(role, action, resource, prefix=None):
    cmd = ["bash", str(c.ROOT / ".tools" / "aws"), "iam", "simulate-principal-policy",
           "--policy-source-arn", f"arn:aws:iam::{ACCOUNT}:role/{role}", "--action-names", action,
           "--resource-arns", resource, "--output", "json"]
    if prefix is not None:
        cmd += ["--context-entries", f"ContextKeyName=s3:prefix,ContextKeyValues={prefix},ContextKeyType=string"]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=110)
    if r.returncode != 0:
        raise RuntimeError(f"simulate failed rc={r.returncode}: {r.stderr.strip()[:300]}")
    return json.loads(r.stdout)["EvaluationResults"][0]["EvalDecision"]


def run(v):
    for role in ROLES:
        a = (simulate(role, "s3:ListBucket", f"arn:aws:s3:::{BUCKET}", f"{P}/security_names/"),
             simulate(role, "s3:GetObject", f"arn:aws:s3:::{BUCKET}/{P}/security_names/names-x.parquet"))
        b = (simulate(role, "s3:PutObject", f"arn:aws:s3:::{BUCKET}/{P}/security_universe/date=2026-10-02/universe-x.parquet"),
             simulate(role, "s3:GetObject", f"arn:aws:s3:::{BUCKET}/{P}/security_universe/date=2026-10-02/universe-x.parquet"))
        cc = (simulate(role, "s3:PutObject", f"arn:aws:s3:::{BUCKET}/{P}/security_names/names-x.parquet"),
              simulate(role, "s3:GetObject", f"arn:aws:s3:::{BUCKET}/{P}/security_namesX/names-x.parquet"))
        print(role, "| names list/get", a, "| universe put/get", b, "| control names put / sibling get", cc)
        v.check(all(x == "allowed" for x in a), f"(a) {role}: list + get on gold/security_names/ allowed")
        v.check(all(x == "allowed" for x in b), f"(b) {role}: put + get on gold/security_universe/ allowed")
        v.check(all(x != "allowed" for x in cc), f"(c) control {role}: put on security_names and get on a sibling prefix denied")
        d = simulate(role, "s3:GetObject", f"arn:aws:s3:::{BUCKET}/{P}/holding_contribution/date=2026-10-05/x.parquet")
        print(role, "| positive control holding_contribution get", d)
        v.check(d == "allowed", f"(d) positive control {role}: get on the already-granted gold/holding_contribution/ is allowed")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
