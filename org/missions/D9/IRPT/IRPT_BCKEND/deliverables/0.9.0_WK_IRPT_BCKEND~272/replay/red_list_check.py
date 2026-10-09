"""IB-pr-409 red-list check (CTO ADDENDUM 18, row IRPT_BCKEND-D2-S46). From the worktree root:
    python <this file> <base_commit> <census_json> <out_json>
Runs `pytest _contracts -rf` from infra/aws/lambda/investor-reporting/, lists the FAILED node ids, names each red test's TARGET (the
route, the response contract or the fixture it reads, taken from the node id), and intersects (a) every path this cell changed against
<base_commit> and (b) every source path of a packaged changed member (the census) with the red tests' target surface:
the `_contracts/` tree, `docs/contracts/investor-reporting/`, and the five operations / contract names the red ids carry.
A non-empty intersection is a STOP (exit 1). ASCII only.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, check=True).stdout.decode().strip())
base, census_path, out_path = sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3])
IR = ROOT / "infra/aws/lambda/investor-reporting"
p = subprocess.run([sys.executable, "-m", "pytest", "_contracts", "-rf", "-q", "-p", "no:cacheprovider"], cwd=str(IR), capture_output=True, timeout=280)
text = re.sub(r"\x1b\[[0-9;]*m", "", (p.stdout + p.stderr).decode("utf-8", "replace"))
failed = [ln[len("FAILED "):].split(" - ")[0].strip() for ln in text.splitlines() if ln.startswith("FAILED ")]
summary = [ln for ln in text.splitlines() if re.search(r"\d+ (passed|failed)", ln)][-1]
ops = sorted({m for n in failed for m in re.findall(r"\[([a-z-]+)\]", n)})
target_prefixes = ["infra/aws/lambda/investor-reporting/_contracts/", "docs/contracts/investor-reporting/"]
changed = subprocess.run(["git", "diff", "--name-only", base, "HEAD"], cwd=str(ROOT), capture_output=True, check=True).stdout.decode().split()
census = json.loads(census_path.read_text(encoding="utf-8"))
member_paths = sorted({m["source_path"] for a in census["artifacts"] for m in a["changed_members"]})
touch_changed = [c for c in changed if any(c.startswith(t) for t in target_prefixes)]
touch_members = [c for c in member_paths if any(c.startswith(t) for t in target_prefixes)]
named = [c for c in changed + member_paths if any(o in c for o in ops)]
doc = {"pytest_summary": summary, "failed_node_ids": failed, "failed_count": len(failed), "red_test_operations": ops,
       "target_prefixes": target_prefixes, "paths_this_cell_changed_vs_base": changed, "packaged_member_source_paths": member_paths,
       "changed_paths_touching_a_target": touch_changed, "member_paths_touching_a_target": touch_members,
       "paths_naming_a_red_operation": named, "stop": bool(touch_changed or touch_members or named)}
out_path.write_text(json.dumps(doc, indent=1) + "\n", encoding="utf-8")
print(summary)
print("failed:", len(failed), "| changed vs base:", len(changed), "| member source paths:", len(member_paths),
      "| touching a target:", len(touch_changed) + len(touch_members), "| naming a red operation:", len(named), "| STOP:", doc["stop"])
sys.exit(1 if doc["stop"] else 0)
