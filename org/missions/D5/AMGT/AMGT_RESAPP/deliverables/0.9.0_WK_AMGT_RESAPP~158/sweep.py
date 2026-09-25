"""AMGT_RESAPP round 41, AMGT-rp-1 -- FWD-30 measured across the WHOLE coverage list (89 folders).

For each of the 89 folders in `0.9.0_WK_AMGT_RESAPP~4/universe.json`:
  1. KEY -- resolve the folder's security_key via crosswalk.harvester_key + scoped_amgt.resolve_identity
     (the same two-step resolution `resolve_identity` itself performs, done here to get the key BEFORE
     the capture call).
  2. CAPTURE -- invoke the deployed opal-amgt-scoped-api's served routes for that key (capture_lib.py,
     generalised from rn-5's served_capture.py), into a FRESH temp directory outside the repository
     (BOUNDS 3: captures stay out of the repository).
  3. COMPARE -- run portal's exportCompare.harness.cjs --fixture <served_fixture> --rich <rich body>,
     parse its FIGURES/CITES/ABSENCES lines, its PAGE ABSENCE LINES COVERED line and its EXPORT-COMPARE
     verdict line.

Writes ONE row per folder to fwd30_population.tsv and one per-folder log to logs/<slug>.log. The temp
capture directory is removed after its log is written (BOUNDS 3).

Run (from the repo root):
  PYTHONPATH=<repo root> python org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~158/sweep.py
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[6]
sys.path.insert(0, str(REPO_ROOT))

from lib.research.identity import crosswalk  # noqa: E402
from lib.research.api import scoped_amgt  # noqa: E402

sys.path.insert(0, str(HERE))
import capture_lib  # noqa: E402

UNIVERSE = REPO_ROOT / "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~4/universe.json"
TSV = HERE / "fwd30_population.tsv"
LOG_DIR = HERE / "logs"
PORTAL_DIR = REPO_ROOT / "portal"
HARNESS = "src/pages/SecurityAnalysis/__harness__/exportCompare.harness.cjs"

SETS = ("fig", "cit", "abs")
COUNTS = [s + "_" + c for s in SETS for c in ("page", "rich", "same", "missing", "extra")] + ["abs_covered"]
HEADER = ["folder", "security_key"] + COUNTS + ["verdict", "reason"]

SET_RE = {
    "fig": re.compile(r"^FIGURES page=(\d+) rich=(\d+) same=(\d+) missing=(\d+) extra=(\d+)", re.M),
    "cit": re.compile(r"^CITES page=(\d+) rich=(\d+) same=(\d+) missing=(\d+) extra=(\d+)", re.M),
    "abs": re.compile(r"^ABSENCES page=(\d+) rich=(\d+) same=(\d+) missing=(\d+) extra=(\d+)", re.M),
}
COVERED_RE = re.compile(r"^PAGE ABSENCE LINES COVERED IN RICH DOC \(verbatim reason found\): (\d+) of \d+", re.M)


def slug(folder):
    return re.sub(r"[^A-Za-z0-9_-]+", "_", folder).strip("_") or "folder"


def resolve_key(folder, pilots):
    harvester_key, _basis = crosswalk.harvester_key(folder, pilots)
    block = scoped_amgt.resolve_identity(harvester_key)
    return block.get("security_key"), block


def run_harness(fixture_path, rich_path):
    proc = subprocess.run(
        ["node", HARNESS, "--fixture", str(fixture_path), "--rich", str(rich_path)],
        cwd=str(PORTAL_DIR),
        capture_output=True,
        text=True,
        timeout=120,
    )
    return proc.returncode, proc.stdout, proc.stderr


def blank_row(folder, security_key, verdict, reason):
    row = {c: "" for c in COUNTS}
    row["folder"] = folder
    row["security_key"] = security_key or ""
    row["verdict"] = verdict
    row["reason"] = reason
    return row


def main():
    universe = json.load(open(UNIVERSE, encoding="utf-8"))
    folders = [n["folder"] for n in universe["names"]]
    pilots = crosswalk.load_pilots()

    LOG_DIR.mkdir(parents=True, exist_ok=True)
    rows = []
    verdict_counts = {"OK": 0, "NOT_OK": 0, "CAPTURE_FAILED": 0}

    for idx, folder in enumerate(folders, start=1):
        log_lines = []
        log_lines.append("folder: %s (%d of %d)" % (folder, idx, len(folders)))
        security_key, identity_block = resolve_key(folder, pilots)
        log_lines.append("identity_block: %s" % json.dumps(identity_block, sort_keys=True))

        if not security_key:
            reason = "identity UNRESOLVED: %s" % identity_block.get("reason", "")
            row = blank_row(folder, None, "CAPTURE_FAILED", reason)
            rows.append(row)
            verdict_counts["CAPTURE_FAILED"] += 1
            log_lines.append("CAPTURE_FAILED: %s" % reason)
            (LOG_DIR / (slug(folder) + ".log")).write_text("\n".join(log_lines) + "\n", encoding="utf-8", newline="\n")
            print("%3d/%3d  %-30s  %-20s  CAPTURE_FAILED  %s" % (idx, len(folders), folder, "(none)", reason))
            continue

        tmpdir = tempfile.mkdtemp(prefix="amgt_rp1_")
        try:
            cap = capture_lib.capture(security_key, tmpdir)
            log_lines.append("code_sha256: %s" % cap["code_sha256"])
            failed_route = None
            for m in cap["routes_meta"]:
                status = m.get("status")
                log_lines.append("  route %s status=%s bytes=%s error=%s" % (
                    m.get("path"), status, m.get("bytes"), m.get("error")))
                if status != 200 and failed_route is None:
                    failed_route = "%s status=%s" % (m.get("path"), status if status is not None else m.get("error"))

            if failed_route or cap["rich_path"] is None:
                reason = failed_route or "print?format=rich route did not produce a body"
                row = blank_row(folder, security_key, "CAPTURE_FAILED", reason)
                rows.append(row)
                verdict_counts["CAPTURE_FAILED"] += 1
                log_lines.append("CAPTURE_FAILED: %s" % reason)
                print("%3d/%3d  %-30s  %-20s  CAPTURE_FAILED  %s" % (idx, len(folders), folder, security_key, reason))
            else:
                rc, out, err = run_harness(cap["served_fixture_path"], cap["rich_path"])
                log_lines.append("harness rc=%d" % rc)
                log_lines.append("--- stdout ---")
                log_lines.append(out)
                if err.strip():
                    log_lines.append("--- stderr ---")
                    log_lines.append(err)

                counts = {}
                ok_shape = True
                for s, rx in SET_RE.items():
                    m = rx.search(out)
                    if not m:
                        ok_shape = False
                        continue
                    for c, v in zip(("page", "rich", "same", "missing", "extra"), m.groups()):
                        counts[s + "_" + c] = v
                cm = COVERED_RE.search(out)
                if cm:
                    counts["abs_covered"] = cm.group(1)
                else:
                    ok_shape = False

                is_ok = "EXPORT-COMPARE OK" in out
                if ok_shape and is_ok:
                    verdict = "OK"
                    reason = ""
                elif ok_shape:
                    verdict = "NOT_OK"
                    first_bad = None
                    for s, label in (("fig", "FIGURES"), ("cit", "CITES"), ("abs", "ABSENCES")):
                        if counts.get(s + "_missing", "0") != "0" or counts.get(s + "_extra", "0") != "0":
                            first_bad = label
                            break
                    reason = "%s set(s) differ (harness printed EXPORT-COMPARE NOT OK / rc=%d)" % (
                        first_bad or "unnamed", rc)
                else:
                    verdict = "CAPTURE_FAILED"
                    reason = "harness output did not carry the expected FIGURES/CITES/ABSENCES/COVERED lines (rc=%d)" % rc
                    counts = {}

                row = blank_row(folder, security_key, verdict, reason)
                row.update(counts)
                rows.append(row)
                verdict_counts[verdict] += 1
                print("%3d/%3d  %-30s  %-20s  %-14s  %s" % (idx, len(folders), folder, security_key, verdict, reason))
        finally:
            shutil.rmtree(tmpdir, ignore_errors=True)
            (LOG_DIR / (slug(folder) + ".log")).write_text("\n".join(log_lines) + "\n", encoding="utf-8", newline="\n")

    with open(TSV, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\t".join(HEADER) + "\n")
        for row in rows:
            fh.write("\t".join(str(row.get(c, "")) for c in HEADER) + "\n")

    print("")
    print("rows written: %d of %d folders" % (len(rows), len(folders)))
    print("verdicts: OK %d, NOT_OK %d, CAPTURE_FAILED %d" % (
        verdict_counts["OK"], verdict_counts["NOT_OK"], verdict_counts["CAPTURE_FAILED"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
