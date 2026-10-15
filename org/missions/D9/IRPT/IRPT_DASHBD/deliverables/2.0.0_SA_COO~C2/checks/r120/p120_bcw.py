"""IRPT_DASHBD round 120, workstream B-CW (issuer 2.0.0_SA_COO~C2) -- the resume of the Cottonwood apply under the signed addendum (blob 1a7a8c68bb) by 0.7.0_AE_CloudOps~DB2.

  DBC120-1-AC1 the gates, the second shared-zip build (the member diff against the live zip is scopes.json only, equal to the blob at the new pin), the registry test on the BUILT zip, the source-map diff,
               the printed 49 Financial and Inflection schedule states, the ledger continued, the 0/3/0 plan and the post-apply No changes
  DBC120-2-AC1 the 12-date catch-up resumed from date 1 (the round-117 arm, on this order's record)
  DBC120-3-AC1 the live state (the round-117 arm, on this order's record): one CodeSha256 on the three functions, ENABLED at cron(15 8 ? * MON-FRI *) New York, the planted listing test

Reuses the round-117 arms of p117_bcw.py with this order's record. Usage: python -I <this file> <repo_root> <criterion_id>
"""
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("p117", str(HERE.parent / "r117" / "p117_bcw.py"))
p117 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p117)
p114, Fail, need = p117.p114, p117.Fail, p117.need

REC = p114.D + "0.7.0_AE_CloudOps~DB2/COTTONWOOD_APPLY_RECORD_R2.json"
PACKET = p114.D + "0.9.0_WK_IRPT_DASHBD~406/NEVER_WIDEN_ADDENDUM_DB-c-11_R118.md"
BLOB = "1a7a8c68bb153a1b92fab3c5247301ba1d9aae4e"
COO_HALF = p114.D + "2.0.0_SA_COO~C2/NEVER_WIDEN_ADDENDUM_DB-c-11_R118_COO_HALF.md"
CTO_HALF = p114.D + "1.0.0_SA_CTO~DELL2/NEVER_WIDEN_ADDENDUM_DB-c-11_R118_CTO_HALF.md"
SRC_MAP = "infra/aws/lambda/ci/lambda-source-map.json"
NEW_PIN = "69679b90e3dc52b670d33fddd96d06be1deaac90"
NEW_SHA = "6ce64167c26588521fded21330dc59e0109450e9a01c92e0f6ca9aa90b53cfae"
FIRST_NEW_ZIP_VERSION = "vrBQAr57i.p3TMhjdSld3c_E5HMqX8iy"
BASE = "eae8170b22"  # the tree the re-pin and the test were merged at
COT_FN = "irpt-cot-holdings-performance-lambda"


def git(root, *args):
    r = subprocess.run(["git", "-C", str(root)] + list(args), capture_output=True)
    need(r.returncode == 0, "git " + " ".join(args[:2]) + " failed: " + r.stderr.decode("utf-8", "replace")[:100])
    return r.stdout.decode("utf-8")


def ac_1(root):
    r = p114.load(root, REC)
    for k, v in p114.walk(r):
        if isinstance(v, str) and k in ("words", "basis_words", "note"):
            need(not p114.LONG_DIGITS.search(v), "a run of 8 or more digits in field " + k)
    g = r["gates"]
    need(git(root, "hash-object", PACKET).strip() == BLOB == g["packet_blob"], "the addendum packet blob is not the signed one")
    for half in (COO_HALF, CTO_HALF):
        t = (Path(root) / half).read_text(encoding="utf-8")
        need("1a7a8c68bb" in t and "SIGNED" in t, "a half does not read SIGNED at the addendum blob: " + half)
    need(g["coo_half_signed"] is True and g["cto_half_signed"] is True, "halves not recorded signed")
    need(g["first_pair_blob"] == "ad049d506cdb22d4fd729b85ef206a548aa4a6d2", "the first pair's blob is not recorded")
    sm = r["schedules_before_upload"]
    for fn in ("irpt-holdings-performance-lambda", "irpt-inf-holdings-performance-lambda"):
        need(sm[fn]["state"] in ("ENABLED", "DISABLED") and sm[fn]["expression"] and sm[fn]["next_fire_utc"], "the schedule state and next fire of " + fn + " are not printed")
    b = r["build"]
    need(b["registry_test_on_built_zip"]["rc"] == 0, "the registry test on the BUILT zip did not pass before upload")
    need(b["upload_member_diff"] == ["infra/logic/registry/scopes.json"], "the built zip differs from the live zip by more than scopes.json: " + str(b["upload_member_diff"]))
    need(b["scopes_member_sha256"] == NEW_SHA, "the built scopes.json is not the blob at the new pin")
    need(b["live_version_before"] == FIRST_NEW_ZIP_VERSION and b["landed_version_id"] != FIRST_NEW_ZIP_VERSION and b["built_equals_landed"] is True, "version ids or landed-equals-built wrong")
    # the source map: the new Cottonwood row (mirroring the Inflection entry) and every holdings-performance entry's scopes.json at the new pin
    now = json.loads((Path(root) / SRC_MAP).read_text(encoding="utf-8"))
    base = json.loads(git(root, "show", BASE + ":" + SRC_MAP))
    need(COT_FN in now["functions"] and COT_FN not in base["functions"], "the Cottonwood source-map row is absent or was already there")
    cot = now["functions"][COT_FN]
    need(cot.get("tf_resource") == "module.irpt_holdings_performance_cot.aws_lambda_function.this" and cot.get("iam_role") == "irpt-cot-holdings-performance-role", "the Cottonwood row names the wrong resource or role")
    for fn in ("irpt-holdings-performance-lambda", "irpt-inf-holdings-performance-lambda", COT_FN):
        sc = [s for s in now["functions"][fn]["staged_from"] if s["repo_path"] == "infra/logic/registry/scopes.json"]
        need(len(sc) == 1 and sc[0]["pin"] == NEW_PIN and sc[0]["sha256"] == NEW_SHA, "the scopes.json entry of %s is not at the new pin" % fn)
    need(cot["staged_from"] == now["functions"]["irpt-holdings-performance-lambda"]["staged_from"], "the Cottonwood row's staged_from differs from the 49 Financial entry's")
    need(r["ledger_entry"] == "irpt-dashbd-cottonwood-holdings-performance-20261015", "the ledger was not continued")
    led = list((Path(root) / "org/critical_paths/change_management").glob("*" + r["ledger_entry"] + "*"))
    need(led, "the ledger entry is absent")
    pl = r["plan"]
    need(pl["add"] == 0 and pl["destroy"] == 0 and pl["change"] == 3 and pl["change_addresses"] == [
        "module.irpt_holdings_performance.aws_lambda_function.this",
        "module.irpt_holdings_performance_inf.aws_lambda_function.this",
        "module.irpt_holdings_performance_cot.aws_lambda_function.this"], "the plan is not 0 to add, 3 to change (the three named functions), 0 to destroy")
    need(pl["replan_no_changes"] is True, "the post-apply plan did not read No changes")
    d = r["derivations_after"]
    need(d["identical_to_before"] is True, "the 49 Financial and Inflection derivations were not read unchanged after the apply")


def ac_2(root):
    p117.REC = REC
    facts = json.loads((Path(root) / (p114.D + "0.9.0_WK_IRPT_DASHBD~403/PACKET_FACTS_R115.json")).read_text(encoding="utf-8"))
    rec = p114.load(root, REC)
    need(rec["catch_up"]["dates"] == facts["catch_up"]["dates"], "the catch-up dates are not the first pair's twelve (as-of 2026-10-13); a different set is a STOP")
    p117.ac_2(root)


def ac_3(root):
    p117.REC = REC
    p117.ac_3(root)


ARMS = {"DBC120-1-AC1": ac_1, "DBC120-2-AC1": ac_2, "DBC120-3-AC1": ac_3}


def main(argv):
    root, cid = argv[0], argv[1]
    try:
        need(cid in ARMS, "unknown criterion " + cid)
        ARMS[cid](root)
    except Fail as e:
        print(str(e))
        print(cid + " FAIL")
        return 1
    except Exception as e:
        print("checker error: " + type(e).__name__ + ": " + str(e)[:200])
        print(cid + " FAIL")
        return 1
    print(cid + " PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
