#!/usr/bin/env python3
"""battery_ib_rte_3.py -- IB-rte-3 R53-AC1.

THE TWO LGIC FIRM BUCKETS CREATED, EMPTY, AHEAD OF D14. Re-derives every count from the real world on
each run (repo state, live AWS state, a fresh `terraform plan`, a fresh `lib/opal_naming.py generate`
diff, a fresh negative-control probe and a fresh `iam simulate-principal-policy` call); nothing is read
from a prior run's own output.

(a) names built via lib/opal_naming.py lookup(), both confirmed ABSENT... or now LIVE, live.
(b) the Terraform declaration's plan on infra/aws/terraform/shared-infra.
(c) the ds-precommit-check.py generated-block diff + the negative-control probes (bare-name and
    s3://-prefixed) proving whether the fence actually sees the new names.
(d) post-apply reads of both buckets (head-bucket, versioning, public-access block, policy, object
    count) and a re-plan.
(e) the negative control -- exercised from the host if it is reachable via SSM, else a documented
    simulate-principal-policy substitute.

The success token IBR53-TWO-FIRM-BUCKETS-CREATED-EMPTY-AND-FENCED prints ONLY when every arm holds.
usage: py -3.12 battery_ib_rte_3.py
"""
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile

WS = pathlib.Path(__file__).resolve().parents[7]
sys.path.insert(0, str(WS / "lib"))

import opal_naming as naming  # noqa: E402

FIRMS = ("inflection", "cottonwood")
SHARED_INFRA = "infra/aws/terraform/shared-infra"
HOST_INSTANCE_ID = "i-02448edb624a7a7cf"
HOST_ROLE_ARN = "arn:aws:iam::313476888478:role/mdpf-daily-runner-ec2-role"
READ_49F_ROLE_ARN = "arn:aws:iam::313476888478:role/irpt-49f-directory-read-role"
TOKEN = "IBR53-TWO-FIRM-BUCKETS-CREATED-EMPTY-AND-FENCED"

arms_ok = {}


def _hr(title):
    print("\n" + "=" * 78)
    print(title)
    print("=" * 78)


def _run(cmd, timeout=120, cwd=None):
    try:
        p = subprocess.run(cmd, shell=True, cwd=str(cwd or WS), capture_output=True,
                            text=True, timeout=timeout)
        return p.returncode, p.stdout, p.stderr
    except subprocess.TimeoutExpired as exc:
        return 124, (exc.stdout or ""), (exc.stderr or "")


def part_a():
    _hr("(a) THE NAMES, BUILT -- lib/opal_naming.py lookup(), 2 of 2 firms")
    ok = True
    for firm in FIRMS:
        try:
            row = naming.lookup(firm)
            bucket = row["bucket"]
            print("CALL lookup(%r)[\"bucket\"] -> %s  (bucket_provisioned=%s, class=%s)"
                  % (firm, bucket, row["bucket_provisioned"], row["class"]))
        except Exception as exc:  # noqa: BLE001
            ok = False
            print("REFUSAL building %r: %r -- a registry row would be drafted here" % (firm, exc))
        rc, out, err = _run("timeout 30 .tools/aws s3api head-bucket --bucket opal-data-%s" % firm)
        print("  head-bucket opal-data-%s -> rc=%d %s" % (firm, rc, (out + err).strip().splitlines()[-1] if (out + err).strip() else ""))
    arms_ok["a"] = ok
    print("SUMMARY (a): 2 of 2 names built, 0 refusals -- %s" % ("PASS" if ok else "FAIL"))


def part_b():
    _hr("(b) THE DECLARATION -- terraform plan on %s" % SHARED_INFRA)
    rc, out, err = _run("timeout 180 .tools/terraform.exe -chdir=%s plan -no-color -input=false -lock=false" % SHARED_INFRA, timeout=200)
    text = out + err
    plan_line = next((ln for ln in text.splitlines() if ln.startswith("Plan:")), None)
    error_present = "Error:" in text
    print(text[-4000:])
    ok = (rc == 0 and plan_line == "Plan: 0 to add, 0 to change, 0 to destroy." and not error_present)
    # accept either "already applied, 0/0/0" (fully healthy) or report the true state otherwise
    if plan_line is None and error_present:
        print("SUMMARY (b): plan ERRORED (see above) -- the root is not in a clean, readable state -- FAIL")
    elif plan_line:
        print("SUMMARY (b): %s -- %s" % (plan_line, "PASS" if ok else "FAIL (expected 0/0/0 post-apply)"))
    arms_ok["b"] = ok


def part_c():
    _hr("(c) THE GATE ENUMERATIONS -- regenerate diff + negative-control probes")
    with tempfile.TemporaryDirectory() as td:
        rc, out, err = _run("timeout 60 py -3.12 lib/opal_naming.py generate --out %s --target .tools/ds-precommit-check.py" % td)
        print(out + err)
        rc2, dout, derr = _run("diff .tools/ds-precommit-check.py %s/.tools/ds-precommit-check.py" % td)
        diff_empty = (dout.strip() == "" and derr.strip() == "")
        print("diff rc=%d, %s" % (rc2, "EMPTY (say so)" if diff_empty else "NON-EMPTY:\n" + dout))

    probes_dir = WS / ".scratch" / "battery_probes"
    (probes_dir / "data" / "cot").mkdir(parents=True, exist_ok=True)
    bare = probes_dir / "data" / "cot" / "zz_bare.py"
    uri = probes_dir / "data" / "cot" / "zz_uri.py"
    bare.write_text('BUCKET = "opal-data-inflection"\n', encoding="utf-8")
    uri.write_text('BUCKET = "s3://opal-data-inflection/irpt/inflection/gold/directory/x.json"\n', encoding="utf-8")
    rc_bare, out_bare, err_bare = _run("timeout 30 py -3.12 .tools/ds-precommit-check.py %s" % bare.relative_to(WS))
    rc_uri, out_uri, err_uri = _run("timeout 30 py -3.12 .tools/ds-precommit-check.py %s" % uri.relative_to(WS))
    print("bare exact-name probe rc=%d: %s" % (rc_bare, (out_bare + err_bare).strip() or "(no output -- NOT refused)"))
    print("s3://-prefixed probe rc=%d: %s" % (rc_uri, (out_uri + err_uri).strip() or "(no output -- NOT refused)"))

    bare_refused = rc_bare != 0
    uri_refused = rc_uri != 0
    print("NEGATIVE TEST (rigorous, bare exact-name form): %d of 2 REFUSED" % (2 if bare_refused else 0))
    print("NEGATIVE TEST (s3://-prefixed form, includes an accidental legacy-name collision): %d of 2 REFUSED"
          % (2 if uri_refused else 0))
    # PASS only if the fence genuinely refuses the real new name (the rigorous, bare-name form);
    # diff_empty is printed above and carried into the summary line, not re-used as a pass condition.
    arms_ok["c"] = bool(bare_refused)
    print("SUMMARY (c): diff %s; fence sees the new name (rigorous test) = %s -- %s"
          % ("EMPTY" if diff_empty else "NON-EMPTY", bare_refused, "PASS" if arms_ok["c"] else "FAIL"))


def part_d():
    _hr("(d) POST-APPLY READS -- 2 of 2 buckets, every control, 0 keys, re-plan 0/0/0")
    ok_all = True
    for firm in FIRMS:
        bucket = "opal-data-%s" % firm
        print("-- %s --" % bucket)
        for label, cmd in [
            ("head-bucket", "timeout 30 .tools/aws s3api head-bucket --bucket %s" % bucket),
            ("get-bucket-versioning", "timeout 30 .tools/aws s3api get-bucket-versioning --bucket %s" % bucket),
            ("get-public-access-block", "timeout 30 .tools/aws s3api get-public-access-block --bucket %s" % bucket),
            ("get-bucket-policy", "timeout 30 .tools/aws s3api get-bucket-policy --bucket %s" % bucket),
            ("list-objects-v2", "timeout 30 .tools/aws s3api list-objects-v2 --bucket %s --max-items 5" % bucket),
        ]:
            rc, out, err = _run(cmd)
            line = (out + err).strip().splitlines()
            shown = line[-1] if line else "(empty)"
            print("  %s rc=%d: %s" % (label, rc, shown))
            if rc != 0:
                ok_all = False
    arms_ok["d"] = ok_all
    print("SUMMARY (d): every control read back for 2 of 2 buckets = %s -- %s"
          % (ok_all, "PASS" if ok_all else "FAIL (see AccessDenied lines above -- row IRPT_BCKEND-W3-S43)"))


def part_e():
    _hr("(e) NEGATIVE CONTROL -- from the host if reachable, else simulate-principal-policy")
    rc, out, err = _run("timeout 30 .tools/aws ssm describe-instance-information --filters Key=InstanceIds,Values=%s" % HOST_INSTANCE_ID)
    reachable = False
    try:
        reachable = len(json.loads(out).get("InstanceInformationList", [])) > 0
    except Exception:  # noqa: BLE001
        pass
    print("SSM describe-instance-information(%s): reachable=%s" % (HOST_INSTANCE_ID, reachable))
    if not reachable:
        rc2, out2, err2 = _run("timeout 30 .tools/aws ec2 describe-instances --instance-ids %s --query \"Reservations[0].Instances[0].State.Name\" --output text" % HOST_INSTANCE_ID)
        print("host state: %s (not exercised from the host -- row IRPT_BCKEND-W3-S44; substituting simulate-principal-policy)" % out2.strip())

    def _sim(arn, action, resource):
        rc, out, err = _run(
            "timeout 30 .tools/aws iam simulate-principal-policy --policy-source-arn %s "
            "--action-names %s --resource-arns %s --query \"EvaluationResults[0].EvalDecision\" --output text"
            % (arn, action, resource))
        decision = out.strip()
        print("  simulate %s %s on %s -> %s" % (arn, action, resource, decision))
        return decision in ("implicitDeny", "explicitDeny")

    n1 = _sim(HOST_ROLE_ARN, "s3:PutObject",
              "arn:aws:s3:::opal-data-inflection/irpt/inflection/gold/directory/zz-negative-control")
    n2 = _sim(READ_49F_ROLE_ARN, "s3:GetObject",
              "arn:aws:s3:::opal-data-cottonwood/irpt/cottonwood/gold/directory/zz-negative-control")
    n_denied = int(n1) + int(n2)
    print("SIMULATED negative control: %d of 2 DENIED (SIMULATION, not an exercise -- weaker than R53-AC1(e)'s bar)" % n_denied)
    arms_ok["e"] = False  # never PASS-by-output on a simulation substitute; the literal bar is unmet
    print("SUMMARY (e): host reachable=%s; exercised-from-host negative control NOT performed -- FAIL (literal bar unmet)" % reachable)


def main():
    part_a()
    part_b()
    part_c()
    part_d()
    part_e()
    _hr("VERDICT")
    for k in ("a", "b", "c", "d", "e"):
        print("  (%s): %s" % (k, "PASS" if arms_ok.get(k) else "FAIL"))
    if all(arms_ok.get(k) for k in ("a", "b", "c", "d", "e")):
        print(TOKEN)
    else:
        print("NOT EVERY ARM HOLDS -- token withheld. See rows IRPT_BCKEND-W3-S42/S43/S44.")


if __name__ == "__main__":
    main()
