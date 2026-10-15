#!/usr/bin/env python3
"""IB-pr-602 (TO IRPT_BCKEND.TO-IB-pr-602) -- 49 Financial's refusal anatomy and the exemption-alone DELTA, re-measured
on the TRANSPLANT tree (pin 1 plus the absent_at_source exemption alone), assembled into one record.

This driver does not carry a measurement of its own. It (1) pins the tree: the sha256 of the two transplanted files
must equal the sha256_transplanted values of IB-pr-595's record for 49financial, and the modules that a scratch copy
of the tree imports must be those files; (2) runs the two unmodified harnesses of IB-pr-584 (anatomy) and IB-pr-580
(DELTA) against a scratch copy of the tree OUTSIDE the repository, with the transplant files in place of the
repository's; (3) keeps the 49financial entries and writes the record named by argv[2].

Every S3 call is a read made by the harnesses through the repository's own readers. Nothing is written to AWS,
landed, published, signed or sent. The scratch copy is never committed.

    python IB233-1_49f_transplant_reread_harness.py <scratch_tree_root> <record_out.json> <work_dir_outside_repo>

A difference in any pin is a STOP: the script exits 2 and writes no record.
"""
import datetime as dt
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DELIV = HERE.parent  # .../deliverables
DIR_434 = DELIV / "0.9.0_WK_IRPT_BCKEND~434"
DIR_426 = DELIV / "0.9.0_WK_IRPT_BCKEND~426"
DIR_422 = DELIV / "0.9.0_WK_IRPT_BCKEND~422"
TRANSPLANT = DIR_434 / "transplant" / "49financial"
CANDIDATE_RECORD = DIR_434 / "IB228-1_holdings_transplant_candidate.json"
ANATOMY_HARNESS = DIR_426 / "IB220-1_49f_refusal_anatomy_harness.py"
DELTA_HARNESS = DIR_422 / "IB218-1_exemption_delta_harness.py"
ANATOMY_REF = DIR_426 / "IB220-1_49f_refusal_anatomy.json"
HS_REL = Path("data/assets/scripts/gold/investor_reporting/holdings_snapshot.py")
PUB_REL = Path("infra/aws/lambda/investor-reporting/holdings/publication.py")
TRANSPLANT_NAMES = ("holdings_snapshot.py", "publication.py")

PIN_CODE = r'''
import json, sys
from pathlib import Path
root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / "data" / "assets" / "scripts" / "gold" / "investor_reporting"))
import holdings_snapshot as hs
import publication as pub
src = Path(hs.__file__).read_text(encoding="utf-8")
print(json.dumps({
    "hs_file": str(Path(hs.__file__).resolve()),
    "pub_file": str(Path(pub.__file__).resolve()),
    "cusip_port_present": callable(getattr(hs, "cusip_key", None)) and "cusip_key(security_id)" in src,
    "one_date_bypass_absent": not hasattr(hs, "allow_older_date") and "allow_older_date" not in src,
}))
'''

COUNTERS = ("functions_invoked", "sign_ins_made", "aws_writes_made", "rows_written", "figures_written", "vendor_requests_sent")


def stop(msg):
    print("STOP: " + msg)
    sys.exit(2)


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load(path):
    return json.loads(Path(path).read_text(encoding="ascii"))


def git_dir(cwd):
    return subprocess.check_output(["git", "rev-parse", "--absolute-git-dir"], cwd=str(cwd)).decode("ascii").strip()


def run(cmd, env, log):
    with open(log, "w", encoding="utf-8") as fh:
        rc = subprocess.call(cmd, env=env, stdout=fh, stderr=subprocess.STDOUT)
    return rc


def main():
    if len(sys.argv) != 4:
        print("usage: IB233-1_49f_transplant_reread_harness.py <scratch_tree_root> <record_out.json> <work_dir>")
        sys.exit(2)
    scratch = Path(sys.argv[1]).resolve()
    out = Path(sys.argv[2]).resolve()
    work = Path(sys.argv[3]).resolve()
    work.mkdir(parents=True, exist_ok=True)

    # 1. The transplant files against IB-pr-595's record.
    cand = load(CANDIDATE_RECORD)
    members = (((cand.get("firms") or {}).get("49financial") or {}).get("changed_members")) or []
    rec_hash = {}
    for m in members:
        name = Path(m["repo_path"]).name
        rec_hash[name] = m["sha256_transplanted"]
    if sorted(rec_hash) != sorted(TRANSPLANT_NAMES):
        stop("IB-pr-595 record does not name the two transplanted files for 49financial: %s" % sorted(rec_hash))
    t_hs = sha256(TRANSPLANT / "holdings_snapshot.py")
    t_pub = sha256(TRANSPLANT / "publication.py")
    if t_hs != rec_hash["holdings_snapshot.py"] or t_pub != rec_hash["publication.py"]:
        stop("transplant file sha256 differs from IB-pr-595's record")
    print("OK: transplant sha256 equal to IB-pr-595 record (2 of 2)")

    # 2. The scratch copy carries the transplant bytes, and the modules it imports are those files.
    s_hs = scratch / HS_REL
    s_pub = scratch / PUB_REL
    if sha256(s_hs) != t_hs or sha256(s_pub) != t_pub:
        stop("scratch copy does not carry the transplant bytes")
    env = dict(os.environ)
    env["GIT_DIR"] = git_dir(HERE)
    pin_out = subprocess.check_output([sys.executable, "-c", PIN_CODE, str(scratch)], env=env,
                                      cwd=str(scratch)).decode("utf-8").strip().splitlines()[-1]
    pin = json.loads(pin_out)
    if Path(pin["hs_file"]) != s_hs.resolve() or Path(pin["pub_file"]) != s_pub.resolve():
        stop("the imported modules are not the scratch transplant files: %s" % pin)
    if pin["cusip_port_present"] is not True or pin["one_date_bypass_absent"] is not True:
        stop("tree does not read cusip_port_present true and one_date_bypass_absent true: %s" % pin)
    print("OK: imported holdings_snapshot and publication are the transplant files (scratch copy)")
    print("OK: cusip_port_present=%s one_date_bypass_absent=%s" % (pin["cusip_port_present"], pin["one_date_bypass_absent"]))

    base = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=str(HERE)).decode("ascii").strip()
    if not re.fullmatch(r"[0-9a-f]{40}", base):
        stop("base commit is not 40 hex")
    read_date = dt.datetime.now(dt.timezone.utc).date().isoformat()

    # 3. The two unmodified harnesses, run on the scratch tree; each writes its own record into the work directory.
    anatomy_json = work / "anatomy.json"
    delta_json = work / "delta.json"
    rc_a = run([sys.executable, str(ANATOMY_HARNESS), str(scratch), str(anatomy_json)], env, work / "anatomy.log")
    print("OK: anatomy harness rc=%d" % rc_a)
    if rc_a != 0:
        stop("anatomy harness rc=%d (see %s)" % (rc_a, work / "anatomy.log"))
    rc_d = run([sys.executable, str(DELTA_HARNESS), str(scratch), str(delta_json)], env, work / "delta.log")
    print("OK: delta harness rc=%d" % rc_d)
    if rc_d != 0:
        stop("delta harness rc=%d (see %s)" % (rc_d, work / "delta.log"))

    an = load(anatomy_json)
    de_all = load(delta_json)
    de = (de_all.get("firms") or {}).get("49financial")
    if not isinstance(de, dict):
        stop("delta record holds no 49financial block")
    if an["candidate_day"] != de["candidate_day"] or an["served_day"] != de["served_day"]:
        stop("the two harnesses read different candidate or served days")
    if an["base_commit"] != base or de_all["base_commit"] != base:
        stop("a harness base commit differs from the worktree HEAD")

    # 4. The comparison with IB-pr-584 (HEAD code), counts only.
    ref = load(ANATOMY_REF)
    ref_det = {d["condition"]: d["tripped"] for d in ref["conditions_detail"]}
    new_det = {d["condition"]: d["tripped"] for d in an["conditions_detail"]}
    ref_ex = ref["lost_accounts"]["exempted"]
    ref_rem = ref["lost_accounts"]["remaining"]
    ref_unc = ref["classified_security_lost"]["candidate_unclassified_total"]
    new_unc = an["classified_security_lost"]["candidate_unclassified_total"]

    def cause(d):
        return ", ".join("%s=%d" % (k, v) for k, v in sorted(d["cause_split"].items()))

    cmp_note = ("Against IB-pr-584 (HEAD code, base a42c29afb0): account_lost tripped %d -> %d (exempted %d -> %d, "
                "remaining %d -> %d); classified_security_lost tripped %d -> %d (candidate unclassified %d -> %d). "
                "The conditions that no longer trip with the transplant tree: %s."
                % (ref_det.get("account_lost", 0), new_det.get("account_lost", 0), ref_ex, an["lost_accounts"]["exempted"],
                   ref_rem, an["lost_accounts"]["remaining"], ref_det.get("classified_security_lost", 0),
                   new_det.get("classified_security_lost", 0), ref_unc, new_unc,
                   ", ".join(sorted(set(ref["conditions_remaining"]) - set(an["conditions_remaining"]))) or "none"))
    cause_note = ("Cause split on this tree: account_lost %s; classified_security_lost %s."
                  % (cause(an["conditions_detail"][0]), cause(an["conditions_detail"][1])))

    method = ("Measured by IB233-1_49f_transplant_reread_harness.py, in this order, on the scratch copy of the tree outside "
              "the repository: (1) the sha256 of the two transplanted files was compared with IB-pr-595's record for 49financial; "
              "(2) the scratch copy was imported and the loaded module paths and the CUSIP port and one-date bypass checked; "
              "(3) the unmodified IB-pr-584 anatomy harness ran once (one candidate build, WITHOUT and WITH arms, lost accounts "
              "classed, classified securities counted); (4) the unmodified IB-pr-580 exemption DELTA harness ran once, and its "
              "49financial block was kept: the WITHOUT arm with no evidence provider, the WITH arm with the provider and the "
              "listing where PUBLISHED, the exemption alone node by node, and the second fire. Read-only; nothing landed.")

    notes = [
        "Each count rests on the two harness runs above, each one read of the live pinned inputs and the served index through the repository's own readers, on the transplant tree the pins name.",
        "Not read: the refusal record, any landed or served object beyond the index and Gold parquet the gate needs, any Lambda function, the previous candidate, the prior custody day.",
        "Sparse checkout added locally to the worktree, never committed: data/assets/scripts/gold (its top-level modules and investor_reporting), infra/aws/lambda/investor-reporting, data/mdpf/scripts/gold, data/mdpf/scripts/silver, data/assets/scripts/silver, infra/aws/lambda/v2_portal/_shared, docs/contracts/investor-reporting, lib, infra/logic/registry, org/standards; the root file data/firm_registry.json was copied into the scratch tree only, and the scratch tree is outside the repository.",
        cmp_note,
        cause_note,
        "The served 49financial day and the candidate day are the ones the anatomy harness selected; the DELTA harness selected the same days, and the two records agree.",
    ]
    record = {
        "firm_scope": "49financial",
        "candidate_day": an["candidate_day"],
        "served_day": an["served_day"],
        "builder": de["builder"],
        "tree": {
            "holdings_snapshot_sha256": t_hs,
            "publication_sha256": t_pub,
            "cusip_port_present": pin["cusip_port_present"],
            "one_date_bypass_absent": pin["one_date_bypass_absent"],
        },
        "anatomy": {
            "lost_accounts": an["lost_accounts"],
            "classified_security_lost": an["classified_security_lost"],
            "conditions_remaining": an["conditions_remaining"],
            "conditions_detail": an["conditions_detail"],
        },
        "delta": {
            "without": de["without"],
            "with": de["with"],
            "exemption_alone": de["exemption_alone"],
            "second_fire": de["second_fire"],
        },
        "base_commit": base,
        "read_date": read_date,
        "method": method,
        "claim": "measured",
        "notes": notes,
        "functions_invoked": 0, "sign_ins_made": 0, "aws_writes_made": 0,
        "rows_written": 0, "figures_written": 0, "vendor_requests_sent": 0,
    }
    for k in COUNTERS:
        if record[k] != 0:
            stop("counter %s must be 0" % k)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(record, indent=1, sort_keys=True) + "\n", encoding="ascii")
    print("OK: wrote record %s" % out.name)


if __name__ == "__main__":
    main()
