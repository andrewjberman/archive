"""AMGT_RESAPP round 42 -- THE LOCAL POPULATION SWEEP: FWD-30's field-by-field comparison for every coverage-list name, with
the rich export REBUILT from the working tree's code over the SAME served inputs the page renders from.

Per folder of 0.9.0_WK_AMGT_RESAPP~4/universe.json (the 89-name snapshot, read 2026-09-10T23:18Z):
  key      scoped_amgt.resolve_identity(crosswalk.harvester_key(folder, pilots)[0])
  page     the deployed function's served routes, captured once into --cache by 0.9.0_WK_AMGT_RESAPP~158's capture_lib
  export   scoped_amgt.handler(print?format=rich) run IN PROCESS on this tree's code, every reader stubbed from that capture
  compare  exportCompare.harness.cjs --fixture <capture> --rich <rebuilt export>
Writes a TSV with rp-1's header to --out and prints the verdict counts. Reads AWS (lambda invoke, crosswalk); writes nothing
to it. Exit 0 only when every swept name reads OK.
With --served the export side is the DEPLOYED body captured beside the page (print?format=rich), not a rebuild -- the
same comparison on the served plane.
usage: PYTHONPATH=<repo root> python <this> --cache <dir outside the repo> --out <tsv> [--only KEY,...] [--served]"""
import argparse
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path.cwd()
UNIVERSE = ROOT / "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~4/universe.json"
CAPTURE_LIB = ROOT / "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~158/capture_lib.py"
HARNESS = "src/pages/SecurityAnalysis/__harness__/exportCompare.harness.cjs"
COUNTS = [s + "_" + c for s in ("fig", "cit", "abs") for c in ("page", "rich", "same", "missing", "extra")] + ["abs_covered"]
HEADER = ["folder", "security_key"] + COUNTS + ["verdict", "reason"]


def load_capture_lib():
    spec = importlib.util.spec_from_file_location("capture_lib", str(CAPTURE_LIB))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def captured(cache, key, cl):
    d = Path(cache) / re.sub(r"[^A-Za-z0-9_.-]", "_", key)
    served = d / "served"
    fx = next(iter(sorted(served.glob("served_fixture.*.json"))), None) if served.exists() else None
    if fx is None:
        # The page routes and the model block are read at the SAME moment, so a cached pair never mixes vintages: the
        # store moves under a round (measured 2026-09-25 ~05:0xZ, when AMGT_CORPUS re-pulled the blocks after capture).
        from lib.research.api import scoped_amgt as sa
        cl.capture(key, str(d))
        (d / "model_block.json").write_text(json.dumps(sa.read_model_block(key)), encoding="utf-8")
        fx = next(iter(sorted(served.glob("served_fixture.*.json"))), None)
    return d, fx


def rebuild(key, fixture_path, out_path):
    # The MODEL BLOCK is the store's own block (scoped_amgt.read_model_block, what the deployed function reads), saved in the
    # cache at capture time beside the page routes: the thesis payload's fiscal_year_figures are a SUBSET of the block
    # (measured on 992_HK_Equity: 2016-2026 against the block's 2016-2029), so a block rebuilt from the thesis understates the
    # export. Every other reader is stubbed from the capture.
    from lib.research.api import scoped_amgt as sa
    from lib.research.print import render_pack as rp
    bundle = json.loads(Path(fixture_path).read_text(encoding="utf-8"))
    thesis = bundle["thesis"]
    overlay = bundle.get("overlay") or {}
    names = ("resolve_identity", "read_model_block", "read_thesis_bundle", "read_peer_set", "read_posture", "read_description")
    saved = {n: getattr(sa, n) for n in names}
    saved_key = rp.security_key
    try:
        # LOCAL ONLY: Windows refuses '*' in a file name (WALMEX*_MM_Equity); the Lambda's Linux temp dir takes it as is.
        rp.security_key = lambda security: saved_key(security).replace("*", "-")
        sa.resolve_identity = lambda requested: {"security_key": key, "requested": requested, "identity_status": "RESOLVED"}
        block = json.loads((Path(fixture_path).parent.parent / "model_block.json").read_text(encoding="utf-8"))
        sa.read_model_block = lambda security_key: block
        sa.read_thesis_bundle = lambda security_key, identity=None: thesis
        sa.read_peer_set = lambda security_key: bundle.get("peers")
        sa.read_posture = lambda security_key, identity=None: thesis.get("posture")
        sa.read_description = lambda security_key, identity=None, model_block=None, drafting=None: overlay.get("description")
        event = {"rawPath": "/api/scoped/amgt/security/%s/print" % key, "httpMethod": "GET",
                 "headers": {"X-Firm-Id": "opal-capital"}, "queryStringParameters": {"format": "rich"}}
        resp = sa.handler(event)
    finally:
        for n, f in saved.items():
            setattr(sa, n, f)
        rp.security_key = saved_key
    if resp.get("statusCode") != 200:
        return "rebuild statusCode=%s body=%s" % (resp.get("statusCode"), str(resp.get("body"))[:120])
    Path(out_path).write_text(resp["body"], encoding="utf-8")
    return None


def compare(fixture_path, rich_path):
    p = subprocess.run(["node", HARNESS, "--fixture", str(fixture_path), "--rich", str(rich_path)],
                       cwd=str(ROOT / "portal"), capture_output=True, text=True, encoding="utf-8")
    out = p.stdout
    row = {}
    for label, s in (("FIGURES", "fig"), ("CITES", "cit"), ("ABSENCES", "abs")):
        m = re.search(r"^%s page=(\d+) \S+=(\d+) same=(\d+) missing=(\d+) extra=(\d+)" % label, out, re.M)
        if not m:
            return None, "harness printed no %s line (rc=%s)" % (label, p.returncode)
        for c, v in zip(("page", "rich", "same", "missing", "extra"), m.groups()):
            row["%s_%s" % (s, c)] = v
    m = re.search(r"PAGE ABSENCE LINES COVERED IN RICH DOC \(verbatim reason found\): (\d+) of", out)
    row["abs_covered"] = m.group(1) if m else ""
    ok = "EXPORT-COMPARE OK" in out and p.returncode == 0
    reason = ""
    if not ok:
        bad = [lab for lab, s in (("FIGURES", "fig"), ("CITES", "cit"), ("ABSENCES", "abs"))
               if row[s + "_missing"] != "0" or row[s + "_extra"] != "0"]
        reason = ("%s differ" % "+".join(bad)) if bad else "harness NOT OK"
    row["verdict"], row["reason"] = ("OK" if ok else "NOT_OK"), reason
    return row, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--only", default="")
    ap.add_argument("--served", action="store_true")
    a = ap.parse_args()
    from lib.research.identity import crosswalk
    from lib.research.api import scoped_amgt as sa
    cl = load_capture_lib()
    pilots = crosswalk.load_pilots()
    folders = [n["folder"] for n in json.load(open(UNIVERSE, encoding="utf-8"))["names"]]
    only = set(x for x in a.only.split(",") if x)
    rows = []
    for i, folder in enumerate(folders, 1):
        key = sa.resolve_identity(crosswalk.harvester_key(folder, pilots)[0]).get("security_key")
        if only and key not in only:
            continue
        row = {"folder": folder, "security_key": key or ""}
        try:
            d, fx = captured(a.cache, key, cl)
            if a.served:
                rich = next(iter(sorted((d / "served").glob("*.rich.md"))), None)
                err = None if rich else "no served rich body captured"
            else:
                rich = d / "local.rich.md"
                err = rebuild(key, fx, rich)
            if not err:
                cmp_row, err = compare(fx, rich)
            if err:
                row.update({c: "" for c in COUNTS})
                row.update(verdict="CAPTURE_FAILED", reason=err)
            else:
                row.update(cmp_row)
        except Exception as exc:  # a failed read is a row, never a silent skip
            row.update({c: "" for c in COUNTS})
            row.update(verdict="CAPTURE_FAILED", reason="%s: %s" % (type(exc).__name__, str(exc)[:160]))
        rows.append(row)
        print("%d/%d %s %s %s" % (i, len(folders), key, row["verdict"], row["reason"]), flush=True)
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    with open(a.out, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\t".join(HEADER) + "\n")
        for r in rows:
            fh.write("\t".join(str(r.get(h, "")) for h in HEADER) + "\n")
    n = {v: sum(1 for r in rows if r["verdict"] == v) for v in ("OK", "NOT_OK", "CAPTURE_FAILED")}
    print(("served" if a.served else "local rebuild") + " over %d of %d folders: OK %d, NOT_OK %d, CAPTURE_FAILED %d" % (
        len(rows), len(folders), n["OK"], n["NOT_OK"], n["CAPTURE_FAILED"]))
    return 0 if rows and n["OK"] == len(rows) else 1


if __name__ == "__main__":
    sys.exit(main())
