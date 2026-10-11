"""IRPT_BCKEND round 135 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of one order:
  IB135-1  IB-pr-437  the sections response schema's `data.properties` members are typed, so the portal's wire generator renders
                      the file (2.0.0_SA_COO~D2 msg 5188: IB-pr-432 left them as description-only schemas and the generator
                      refuses an untyped member on purpose).

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  IB135-1-AC1  every member under the response schema's `data.properties`, and under each closed form's `properties`, carries a
               $ref, a const, an enum or a type; and IB-pr-432's four arms still hold (the two forms still validate and refuse as
               before). Base: FAIL (the members under data.properties are description-only).
  IB135-1-AC2  the record shows the portal's own generator run on the changed schema in the worktree's portal at the named ref:
               its exit code 0, the three named portal tests' result lines, and the wire files the generator rewrote (listed, not
               committed by this cell). Base: FAIL (no record).
  IB135-1-AC3  the `_contracts` suite fails on nothing new and the owned-report test passes. Base: PASS (a bound).
"""
import json
import re
import subprocess
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~295/"
REC = D + "IB135-1_generator_record.json"
RESP = "docs/contracts/investor-reporting/v1/responses/analysis-report.response.schema.json"
PKG = "infra/aws/lambda/investor-reporting"
P130 = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P2/checks/r130/p130_cells.py"
BASE_FAILING = ("test_every_declared_route_has_a_response_contract_whose_refs_resolve",
                "test_control_a_known_good_document_conforms_and_a_known_bad_one_does_not[analysis-request-original]")
TESTS = ("IVE98", "F14-AC13", "F57-AC2")


def typed(member):
    return isinstance(member, dict) and any(k in member for k in ("$ref", "const", "enum", "type"))


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB135"))
        sys.exit(1)

    if cid == "IB135-1-AC1":
        data = json.loads((root / RESP).read_text(encoding="utf-8"))["properties"]["data"]
        untyped = ["data/" + k for k, v in (data.get("properties") or {}).items() if not typed(v)]
        for i, form in enumerate(data.get("anyOf") or data.get("oneOf") or []):
            untyped += ["form%d/%s" % (i, k) for k, v in (form.get("properties") or {}).items() if not typed(v)]
        if untyped:
            fail("%d member(s) carry no $ref, const, enum or type: %s" % (len(untyped), untyped))
        p = subprocess.run([sys.executable, str(root / P130), str(root), "IB130-1-AC1"], capture_output=True, timeout=100)
        if p.returncode != 0 or b"IB130-1-AC1 PASS" not in p.stdout:
            fail("IB-pr-432's four arms no longer hold: %s" % p.stdout.decode("utf-8", "replace")[-240:].replace("\n", " "))
        print("OK: every member is typed; the two closed forms still validate and refuse as IB-pr-432's arms require")
    elif cid == "IB135-1-AC2":
        f = root / REC
        if not f.is_file():
            fail("no %s" % REC)
        a = json.loads(f.read_text(encoding="utf-8"))
        g = a.get("generator") or {}
        if not g.get("command") or g.get("exit_code") != 0 or not re.fullmatch(r"[0-9a-f]{10,40}", str(g.get("portal_ref") or "")):
            fail("generator needs its command, exit_code 0 and the portal ref it ran at; got exit_code %r" % g.get("exit_code"))
        if g.get("ran_on_the_changed_schema") is not True:
            fail("the record does not say the generator read the worktree's changed schema")
        t = a.get("portal_tests") or {}
        for name in TESTS:
            r = t.get(name) or {}
            if r.get("passed") is not True or not r.get("result_line"):
                fail("portal test %s: passed=%r" % (name, r.get("passed")))
        if not isinstance(a.get("wire_files_rewritten_by_generator"), list) or a.get("portal_files_committed_by_this_cell") != 0:
            fail("wire_files_rewritten_by_generator must be listed and portal_files_committed_by_this_cell must be 0")
        if not isinstance(a.get("control_base_schema_exit_code"), int) or a["control_base_schema_exit_code"] == 0:
            fail("the control (the generator on the schema as it was before this cell) must be run and must exit non-zero")
        print("OK: generator exit 0 at portal %s; %d of %d named portal tests pass; %d wire file(s) rewritten, 0 committed here" % (
            str(g["portal_ref"])[:10], len(TESTS), len(TESTS), len(a["wire_files_rewritten_by_generator"])))
    elif cid == "IB135-1-AC3":
        p = subprocess.run([sys.executable, "-m", "pytest", "_contracts", "ops/tests/test_owned_report.py", "-q", "-p", "no:cacheprovider",
                            "-rf", "--color=no"], cwd=str(root / PKG), capture_output=True, timeout=110)
        out = p.stdout.decode("utf-8", "replace")
        failed = re.findall(r"^FAILED \S+::(\S+)", out, re.MULTILINE)
        m = re.search(r"(\d+) passed", out)
        new = [x for x in failed if x not in BASE_FAILING]
        if new or not m or int(m.group(1)) < 235:
            fail("new failures %s; %s" % (new[:4], out.strip().splitlines()[-1][:120] if out.strip() else "no output"))
        print("OK: %d failed (all among the 2 base failures), %s passed (base 235)" % (len(failed), m.group(1)))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
