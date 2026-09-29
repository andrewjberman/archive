"""IB-pr-201 amendment 2 AC (P20-3-AC1) -- in the PACKAGED layout the served Lambda runs from, a ruled period (YTD) computes
its dates without ModuleNotFoundError. The 49F switch (hD7G6YT1) was rolled back because installed._holdings_source dropped
the runners_49f sys.path insert that _engine_source made, so holdings_gold._period_for -> f49_engine.ruled_period_for ->
import parity_period_returns failed for every YTD/QTD/1Y (CRO 102735, CTO 102736).

Usage: python p20_3_ac1_packaged_ruled_period.py <worktree root>
Builds the irpt-performance-adapter layout from infra/aws/lambda/ci/lambda-source-map.json: each 'files' member is copied
from the WORKTREE (a staged_from row's repo_path, else source_dir/<member>) to its packaged path in a temp dir. Then, in a
fresh interpreter whose import path is ONLY that layout (cwd = layout; no repo directory added):
  import installed; installed.build_runtime(table=<stub>, s3=<stub>, mapping_as_of='2026-09-25', transport_factory=<stub>)
  import holdings_gold; holdings_gold._period_for("2026-01-01", "2026-09-25")
Pass: that YTD ruled period resolves (no ModuleNotFoundError). Since inception never calls _period_for, which is why it hid the defect.
"""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
m = json.loads((root / "infra/aws/lambda/ci/lambda-source-map.json").read_text(encoding="utf-8"))
e = m.get("functions", m)["irpt-performance-adapter"]
staged = {s["packaged_as"]: s["repo_path"] for s in e.get("staged_from", [])}
src_dir = root / e["source_dir"]
layout = Path(tempfile.mkdtemp(prefix="adapter_layout_"))
missing = []
for member in e["files"]:
    src = root / staged[member] if member in staged else src_dir / member
    if not src.is_file():
        missing.append(member)
        continue
    dst = layout / member
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)
print("layout members %d (missing %d%s)" % (len(e["files"]) - len(missing), len(missing), (": %s" % missing[:3]) if missing else ""))
PROBE = r'''
import sys, datetime
REPO = %r
sys.path[:] = [p for p in sys.path if p and not p.replace(chr(92), "/").lower().startswith(REPO)]
sys.path.insert(0, ".")
class Stub:
    def __getattr__(self, name):
        raise AssertionError("no AWS call expected at composition: " + name)
import installed
installed.build_runtime(table=Stub(), s3=Stub(), mapping_as_of="2026-09-25", transport_factory=lambda *a, **k: None)
import holdings_gold
for label, start in (("YTD", "2026-01-01"),):
    try:
        holdings_gold._period_for(start, "2026-09-25")
        print("arm", label, "resolves: True")
    except ModuleNotFoundError as exc:
        print("arm", label, "resolves: False ModuleNotFoundError", exc)
'''
r = subprocess.run([sys.executable, "-c", PROBE % str(root).replace(chr(92), "/").lower()], capture_output=True, text=True, cwd=str(layout))
out = (r.stdout + r.stderr).strip()
print(out[-900:])
ok = "arm YTD resolves: True" in out and not missing
shutil.rmtree(layout, ignore_errors=True)
print("P20-3-AC1 PASS" if ok else "P20-3-AC1 FAIL")
sys.exit(0 if ok else 1)
