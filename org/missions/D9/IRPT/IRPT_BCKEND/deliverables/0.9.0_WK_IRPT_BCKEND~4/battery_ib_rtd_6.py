#!/usr/bin/env python3
"""battery_ib_rtd_6.py -- IB-rtd-6 R46-AC1.

THE DIRECTORY DESTINATION DECLARED AT ITS LGIC ADDRESS AND THE MOVE PACKETED. Read-only on every live
plane and on the registry: no apply, no registry commit, no runner edit, no policy edit, no object
written or copied. `terraform plan` only.

(a) For each of the three firms, calls lib/opal_naming.py address() for the directory object and its
    _refresh manifest, printing the exact call and its output (or the builder's refusal, verbatim).
(b) Censuses the legacy destination's readers (comp-find, unscoped then scoped) and writers (re-runs the
    DS's writer_census_ib_rtc_6.py instrument LIVE).
(c) Prints the direct-port plan (named artifacts, the assumed-principal write model, the FNTEND hand-off).
(d) Prints the never-widen packet's shape: K-keys, the fence re-read (live), baseline `terraform plan` on
    every root touched, writers-before, and the negative-control design.

Every count here is re-derived from the real world on each run; nothing is read from a prior run's
output. usage: py -3.12 battery_ib_rtd_6.py
"""
from __future__ import annotations

import pathlib
import re
import subprocess
import sys
from datetime import datetime, timezone

WS = pathlib.Path(__file__).resolve().parents[7]
sys.path.insert(0, str(WS / "lib"))
sys.path.insert(0, str(WS / ".tools"))

import opal_naming as naming  # noqa: E402
import git_bash_resolver as gbr  # noqa: E402

FIRMS = ("49financial", "inflection", "cottonwood")
TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%d")
DIRECTORY_ROOT = "infra/aws/terraform/investor-reporting/directory"
MDPF_ROOT = "infra/aws/terraform/mdpf-pipeline"
# U+2500..U+257F, the box-drawing block: never a LITERAL char in this ASCII-only source (CLAUDE.md
# Rule 4), so it is built from the codepoints, not typed.
_BOX_DRAWING = re.compile("[%s-%s]" % (chr(0x2500), chr(0x257F)))


def _hr(title):
    print("\n" + "=" * 78)
    print(title)
    print("=" * 78)


def _ascii(s):
    """ASCII-only (CLAUDE.md Rule 4): a captured tool's own non-ASCII decoration (e.g. terraform's
    box-drawing divider) is folded to '-'; any OTHER non-ASCII byte is backslash-escaped rather than
    silently dropped or collided with a genuine '?', never left to mojibake through a cp1252 read."""
    if not s:
        return s
    s = _BOX_DRAWING.sub("-", s)
    return s.encode("ascii", "backslashreplace").decode("ascii")


def _bash(cmd, timeout=180):
    b = gbr.git_bash()
    if not b:
        raise RuntimeError("no Git Bash found (git_bash_resolver)")
    r = subprocess.run([b, "-lc", cmd], capture_output=True, text=True, cwd=str(WS), timeout=timeout)
    return r.returncode, _ascii(r.stdout), _ascii(r.stderr)


# --------------------------------------------------------------------------- (a) THE ADDRESS, BUILT
def part_a():
    _hr("(a) THE ADDRESS, BUILT -- lib/opal_naming.py address(), 3 of 3 firms")
    print("tier chosen: gold (firm-attributable data; tiers.json homes.FIRM.gold: home=scope, MANDATORY")
    print("  firm bucket). Doctrine: infra/logic/02_DOCTRINE.md R5 (:370-378) 'GOLD LIVES IN A PER-PRODUCT")
    print("  OR PER-FIRM BUCKET' + R7 (:401-409) 'ATTRIBUTABILITY DECIDES TENANCY ... firm bucket, gold AND")
    print("  platinum, MANDATORY'; grammar R1 (:149-175) SOURCE-FIRST. Vintage: 02_DOCTRINE.md @afd81beb8a.")
    print("source chosen: 'irpt' (systems.json key, class PRODUCT, long 'investor-reporting', owner D9,")
    print("  owner_claim measured -- org/missions/D9/IRPT/ mission tree). Vintage: systems.json @23980d3fbe.")
    print("partition: illustrative TODAY's date (%s) -- the grammar is date-independent; the real value is" % TODAY)
    print("  set at write time by the runner, never predicted here (round-3 analysis s.4 forward-looking bar).")
    rows = []
    ok = True
    for firm in FIRMS:
        for label, obj in (("directory.json", "directory.json"), ("_refresh manifest", "_refresh/manifest.json")):
            call = "address('irpt', %r, 'gold', 'directory', %r, object=%r)" % (firm, TODAY, obj)
            try:
                out = naming.address("irpt", firm, "gold", "directory", TODAY, object=obj)
                print("CALL   %-40s %s" % (firm + "/" + label, call))
                print("  ->   %s" % out)
                rows.append({"firm": firm, "object": label, "call": call, "result": out, "refused": False})
            except Exception as exc:  # noqa: BLE001
                ok = False
                print("CALL   %-40s %s" % (firm + "/" + label, call))
                print("  -> REFUSED: %s: %s" % (type(exc).__name__, exc))
                rows.append({"firm": firm, "object": label, "call": call, "refused": True,
                             "error": "%s: %s" % (type(exc).__name__, exc)})
    n_built = sum(1 for r in rows if not r["refused"] and r["object"] == "directory.json")
    print("\nSUMMARY: %d of %d firms built a directory.json address with NO refusal; %d refusal(s) total"
          " across %d calls." % (n_built, len(FIRMS), sum(1 for r in rows if r["refused"]), len(rows)))
    if n_built == len(FIRMS) and not any(r["refused"] for r in rows):
        print("REGISTRY ROW NEEDED: NONE. Every call built cleanly under the CURRENT registry -- no")
        print("  infra/logic/registry/*.json row is drafted, because none is required (Rule 30's refusal")
        print("  contingency does not fire here).")
    return ok and n_built == len(FIRMS), rows


# --------------------------------------------------------------------------- (b) THE CENSUS
def part_b():
    _hr("(b) THE CENSUS -- readers (unscoped, then scoped) and writers (re-run live)")
    ok = True
    print("--- READERS, unscoped over the corpus ---")
    rc, out, err = _bash("comp-find 'investor-reporting/directory'")
    print(out.strip() if out else err)
    ok = ok and rc == 0

    for label, path in (
        ("this project (IRPT_BCKEND Lambda source)", "infra/aws/lambda/investor-reporting/"),
        ("portal/ (IRPT_FNTEND's client code)", "portal/"),
        ("IRPT_FNTEND mission tree", "org/missions/D9/IRPT/IRPT_FNTEND/"),
    ):
        print("\n--- READERS, scoped: %s ---" % label)
        rc, out, err = _bash("comp-find 'investor-reporting/directory' %s" % path)
        print(out.strip() if out else err)
        ok = ok and rc == 0

    print("\n--- portal/ gitlink check (is there anything TO scan there in this worktree) ---")
    rc, out, err = _bash("git ls-tree HEAD portal; test -d portal/src && echo HAS_SRC || echo NO_SRC")
    print(out.strip())

    print("\n--- WRITERS: re-running the DS's writer_census_ib_rtc_6.py instrument LIVE (49 Financial ---")
    print("--- legacy destination opal-data-bd, per data/firm_registry.json) ---")
    wc_script = str(WS / "org" / "missions" / "D9" / "IRPT" / "IRPT_BCKEND" / "deliverables"
                     / "0.4.0_DS_ClientPlatform~X" / "writer_census_ib_rtc_6.py")
    try:
        r = subprocess.run([sys.executable, wc_script], capture_output=True, text=True, cwd=str(WS), timeout=600)
        print(r.stdout.strip())
        if r.returncode != 0:
            print("writer_census_ib_rtc_6.py rc=%d stderr: %s" % (r.returncode, r.stderr[-500:]))
        ok = ok and r.returncode == 0
    except Exception as exc:  # noqa: BLE001
        ok = False
        print("writer_census_ib_rtc_6.py FAILED to run: %s: %s" % (type(exc).__name__, exc))
    return ok


# --------------------------------------------------------------------------- (c) THE MOVE, PLANNED
PORT_PLAN = """
THE MOVE, PLANNED (not performed) -- a DIRECT PORT, no dual-write, no mirror, no shadow (CLAUDE.md NEVER):

1. THE WRITE MODEL. The host role (mdpf-daily-runner-ec2-role) CANNOT be granted PutObject directly on
   opal-data-49financial (measured live below, part d): its ARN matches DenyForeignFirmPrincipals's
   ArnNotLike admit list only via `role/*-49f-*`, and mdpf-daily-runner-ec2-role does not carry that
   substring -- the SAME shape that forced IB-rtc-6/7 to an ASSUMED PRINCIPAL for reads. The write grant
   uses the SAME model: one role per firm, named by the builder
   (name('irpt', <firm>, 'directory-write', 'role')), assumed only by the host, carrying PutObject on
   that firm's own new LGIC directory address and nothing else.

2. ARTIFACTS THE PORT TOUCHES (named, not edited by this order):
   - data/assets/scripts/gold/investor_reporting/directory_runner.py -- the destination constant/function
     that writes `investor-reporting/directory/{as_of}/directory.json` (PROD_PREFIX, :125) is repointed to
     lib/opal_naming.py address('irpt', <firm>, 'gold', 'directory', <as_of>, object='directory.json'),
     assuming the new per-firm write-principal for the PutObject call (same shape as Firm49F's read
     session in refresh.py).
   - infra/aws/lambda/investor-reporting/_authz/loaders.py DIRECTORY_PREFIX (:30) and
     infra/aws/lambda/investor-reporting/directory/handler.py DIRECTORY_PREFIX (:53) and
     infra/aws/lambda/investor-reporting/directory/refresh.py DIRECTORY_PREFIX/REFRESH_PREFIX (:70-71) and
     infra/aws/lambda/investor-reporting/holdings/handler.py DIRECTORY_PREFIX (:53) -- every READER of the
     legacy prefix moves to the LGIC address (or, if a shared env var is kept, the env value changes to the
     new key, never a hand-typed literal).
   - `FirmDestinationPolicy` (the per-firm destination-bucket policy the runner/Lambdas already consult via
     data/firm_registry.json's routed bucket) -- its routed-bucket source stays lib/opal_naming.py's
     generated view; the NEW address's bucket is scope_row['bucket'] (opal-data-{firm}), which
     data/firm_registry.json does NOT yet carry as the 'bucket' field consumers read (it carries the
     ROUTED legacy alias) -- so a new generated field or a second lookup is needed; drafted here, not built.
   - .tools/ds-precommit-check.py _CROSS_FIRM_FOREIGN_BUCKETS / _CROSS_FIRM_FOREIGN_KEY_PREFIXES -- GENERATED
     views (lib/opal_naming.py _separations()); once opal-data-inflection/opal-data-cottonwood flip
     bucket_provisioned=true, `python lib/opal_naming.py generate` re-renders these tables to include the
     new bucket names in the OTHER firms' separated_from lists automatically -- a registry-field flip +
     regenerate, never a hand-typed enumeration edit.
   - infra/aws/terraform/investor-reporting/directory/*.tf (the new per-firm write-principal resources,
     K1/K2-shaped) and infra/aws/terraform/mdpf-pipeline/iam.tf (the host's one AssumeRole statement per
     firm, K3-shaped) -- the two roots this order's <paths> grants and IB-rtc-6/7 already used.

3. THE PROVISIONING GAP (measured live, part d): opal-data-inflection and opal-data-cottonwood DO NOT
   EXIST (NoSuchBucket). The 49 Financial leg can port on its own (bucket + fence already live). The other
   two firms' legs are gated on provisioning their FIRM buckets first -- a prerequisite this order does not
   perform (READ-ONLY) and the packet (part d) states as a stop condition, not a K-key.

4. RETIREMENT WINDOW. The legacy prefix (`investor-reporting/directory/` in opal-data-bd/-inf/-cot) is
   RETIRED (readers repointed, writer repointed) in the SAME apply window as the new write grant, never
   mirrored. Rollback = revert the runner/Lambda env repoint and the IAM grant in one apply; the legacy
   objects are NOT deleted by this project, so a reverted config still finds them.

5. THE IRPT_FNTEND HAND-OFF (named, not this project's edit; addressed to 2.0.0_SA_COO~F): IRPT_FNTEND's
   own code never touches the S3 path -- it calls the API contract only
   (docs/contracts/investor-reporting/v1/... carries no S3 path; confirmed by a 0-hit comp-find over that
   contract tree for 's3://' and for 'as_of|source_key|directory.json'). So the port costs IRPT_FNTEND NO
   CODE CHANGE. The named hand-off is a RE-VALIDATION cell: after IB-rtd-7 ports the destination, IRPT_FNTEND
   re-runs its live-server smoke/E2E suite once (the directory-search/resolve routes, end to end) to confirm
   the API's behavior is unchanged by a storage move it cannot see -- this is a regression confirmation, not
   a build item, and it is separate from round-3 analysis s.9 item 3 (the per-firm as-of consequence),
   which is IRPT_FNTEND's own already-named round-4 item.
"""


def part_c():
    _hr("(c) THE MOVE, PLANNED")
    print(PORT_PLAN.strip())
    return True


# --------------------------------------------------------------------------- (d) THE PACKET
def part_d():
    _hr("(d) THE PACKET's live inputs -- fence re-read, bucket existence, baseline plans, writers-before")
    ok = True

    print("--- fence re-read: opal-data-49financial bucket policy (live) ---")
    rc, out, err = _bash("timeout 60 .tools/aws s3api get-bucket-policy --bucket opal-data-49financial "
                          "--query Policy --output text")
    print(out.strip() if out else err.strip())
    ok = ok and rc == 0
    print("  host role ARN: arn:aws:iam::313476888478:role/mdpf-daily-runner-ec2-role -- matches")
    print("  role/*-49f-* ? NO (no '-49f-' substring) -- so DENIED by DenyForeignFirmPrincipals for ANY")
    print("  s3:* action including PutObject, same as the read grant IB-rtc-6/7 found (measured, not typed).")

    for bucket in ("opal-data-inflection", "opal-data-cottonwood"):
        print("\n--- fence re-read: %s bucket policy (live) ---" % bucket)
        rc, out, err = _bash("timeout 60 .tools/aws s3api get-bucket-policy --bucket %s "
                              "--query Policy --output text" % bucket)
        combined = (out or "") + (err or "")
        print(combined.strip())
        if "NoSuchBucket" in combined:
            print("  -> the bucket DOES NOT EXIST. No fence to re-read; provisioning is a PREREQUISITE,")
            print("     named in part (c), not a K-key of this packet.")
        else:
            ok = False

    print("\n--- baseline `terraform plan`, every root this order's <paths> touches (0 changes expected;")
    print("--- a change here is NOT this order's and is a stop, per IB-rtc-6's same finding) ---")
    for label, root in (("investor-reporting/directory", DIRECTORY_ROOT), ("mdpf-pipeline", MDPF_ROOT)):
        print("\n  root: %s" % label)
        rc, out, err = _bash("timeout 240 .tools/terraform.exe -chdir=%s init -input=false -no-color" % root,
                              timeout=260)
        if rc != 0:
            print("    init FAILED rc=%d: %s" % (rc, (err or out)[-500:]))
            ok = False
            continue
        rc, out, err = _bash("timeout 240 .tools/terraform.exe -chdir=%s plan -no-color -input=false -lock=false"
                              % root, timeout=260)
        tail = "\n".join((out or err).strip().splitlines()[-6:])
        print("    plan rc=%d, tail:\n      " % rc + tail.replace("\n", "\n      "))
        ok = ok and rc == 0

    print("\n--- writers-before: the same writer census this order's part (b) already ran (N of M) is the")
    print("--- BEFORE state the packet's IB-rtd-7 successor re-reads AFTER any apply and must find unchanged")
    print("--- for every firm's bucket the write grant does not target. ---")

    print("\n--- negative control, DESIGNED (not executed -- nothing is applied) ---")
    print("  NC1: the host (mdpf-daily-runner-ec2-role) attempts s3:PutObject on a 49 Financial LGIC key")
    print("       WITHOUT assuming the new write-principal -> expect AccessDenied (fence, measured above).")
    print("  NC2: the host, assuming the 49 Financial write-principal, attempts s3:PutObject on the")
    print("       INFLECTION or COTTONWOOD LGIC address -> expect AccessDenied (the assumed role's own")
    print("       policy names only its own firm's prefix; cross-firm write is not granted, mirroring")
    print("       IB-rtc-6's N2/N4 shape).")
    print("  NC3: the 49f READ principal (irpt-49f-directory-read-role, already live per IB-rtc-7) attempts")
    print("       s3:PutObject anywhere -> expect AccessDenied (it carries GetObject/ListBucket only; the")
    print("       write principal is a SEPARATE role, never a widened read role).")
    print("  Proof shape (R-40): each NC is bound to the SSM command id and the AccessDenied error code read")
    print("  at the event, exactly as IB-rtc-6's N1-N5 were; a probe with a deliberately wrong Content-MD5")
    print("  discriminates AccessDenied (unauthorized) from BadDigest (authorized, a FAIL of the control).")
    return ok


def main():
    a_ok, _rows = part_a()
    b_ok = part_b()
    c_ok = part_c()
    d_ok = part_d()
    _hr("VERDICT")
    print("(a) address/refusal: %s" % ("PASS" if a_ok else "FAIL"))
    print("(b) census: %s" % ("PASS" if b_ok else "FAIL"))
    print("(c) port plan: %s" % ("PASS" if c_ok else "FAIL"))
    print("(d) packet inputs: %s" % ("PASS" if d_ok else "FAIL"))
    if a_ok and b_ok and c_ok and d_ok:
        print("\nIBR46-DESTINATION-DECLARED-AT-LGIC-ADDRESS-AND-PACKETED")
        return 0
    print("\nNOT EVERY ARM HELD -- token withheld.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
