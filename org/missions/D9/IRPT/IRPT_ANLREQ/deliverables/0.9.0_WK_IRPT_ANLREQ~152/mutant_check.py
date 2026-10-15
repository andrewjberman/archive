#!/usr/bin/env python3
"""AR351-y-AC2 -- the one mutant that must fail.

Builds a scratch copy OUTSIDE the product tree (.scratch/mutant351/) of the candidate's src/pages/TicketCenter folder, read
from the candidate commit with git show, plus a tsconfig whose '@/' alias points at the real portal src. Then:
  1. CONTROL: the unmutated copy, with the new test file, must pass every case (rc 0, 0 failing).
  2. MUTANT: analysisRequest.ts with filingHints made to ALSO return a hint for every swap in `suggestions` (the forbidden
     shape). The new test file runs against it. MUTANT-FIRES only when that run FAILS and the failing set includes case (b)
     (the swap-only and suggestion-plus-swap cases). Otherwise MUTANT-SURVIVES, exit 1; a control that does not pass prints
     MUTANT-CONTROL-BAD, exit 1, because a failure the control also shows is not evidence of the mutant.
"""
import os
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[7]
PORTAL = ROOT / "portal"
CAND = "cand/dell2/anlreq-filing-hint-did-you-mean"
TC = "src/pages/TicketCenter"
NEW_NAME = "filing-hint.test.tsx"
SCRATCH = ROOT / ".scratch" / "mutant351"

MUTANT_TAIL = """

/* MUTANT (AR351-y-AC2): the forbidden shape -- a hint for every swap in suggestions, as well as the suggestion. */
export function filingHints(findings: AnalysisUploadResultWire['findings'] | undefined): FilingHint[] {
  const base = filingHintsBase(findings)
  const extra: FilingHint[] = []
  for (const f of proxyableFindings(findings)) {
    for (const s of f.suggestions ?? []) extra.push({ row: f.row, value: f.value, suggestion: s.symbol, description: f.description })
  }
  return [...base, ...extra]
}
"""


def git_bytes(args):
    res = subprocess.run(["git", "-C", str(PORTAL)] + args, capture_output=True)
    if res.returncode != 0:
        raise SystemExit("MUTANT-CONTROL-BAD git failed: " + " ".join(args) + " " + res.stderr.decode(errors="replace"))
    return res.stdout


def build(mutant):
    # Clear only the copied src tree: the node_modules link is never walked (it points into the portal worktree).
    if (SCRATCH / "src").exists():
        shutil.rmtree(SCRATCH / "src")
    SCRATCH.mkdir(parents=True, exist_ok=True)
    (SCRATCH / TC / "__tests__").mkdir(parents=True)
    names = git_bytes(["ls-tree", "-r", "--name-only", CAND, TC]).decode().split()
    for rel in names:
        data = git_bytes(["show", f"{CAND}:{rel}"])
        if mutant and rel == f"{TC}/analysisRequest.ts":
            text = data.decode("utf-8")
            head = "export function filingHints(findings: AnalysisUploadResultWire['findings'] | undefined): FilingHint[] {"
            if text.count(head) != 1:
                raise SystemExit("MUTANT-CONTROL-BAD filingHints head not found exactly once")
            text = text.replace(head, head.replace("filingHints(", "filingHintsBase(", 1)) + MUTANT_TAIL
            data = text.encode("utf-8")
        (SCRATCH / rel).write_bytes(data)
    # the '@/' alias resolves into the real portal src; node_modules is linked from the portal worktree
    (SCRATCH / "tsconfig.json").write_text(
        '{"compilerOptions": {"jsx": "react-jsx", "baseUrl": "%s", "paths": {"@/*": ["src/*"]}}}'
        % str(PORTAL).replace("\\", "/"), encoding="utf-8")
    link = SCRATCH / "node_modules"
    if not link.exists():
        try:
            os.symlink(str(PORTAL / "node_modules"), str(link), target_is_directory=True)
        except OSError:
            subprocess.run(["cmd", "/c", "mklink", "/J", str(link), str(PORTAL / "node_modules")], capture_output=True, check=False)
    if not link.exists():
        raise SystemExit("MUTANT-CONTROL-BAD could not link node_modules into the scratch copy")
    return SCRATCH / TC / "__tests__" / NEW_NAME


def run(test_file, name):
    out = SCRATCH / name
    if out.exists():
        out.unlink()
    subprocess.run(["bun", "test", str(test_file), "--reporter=junit", f"--reporter-outfile={out}"],
                   cwd=str(SCRATCH), capture_output=True, text=True, timeout=300)
    rows = []
    for tc in ET.parse(out).getroot().iter("testcase"):
        failed = any(child.tag in ("failure", "error") for child in tc)
        rows.append((tc.get("name") or "", failed))
    return rows


def main():
    control_file = build(mutant=False)
    control = run(control_file, "control.xml")
    if not control or any(f for _, f in control):
        print("MUTANT-CONTROL-BAD the unmutated copy does not pass: %d cases, %d failing"
              % (len(control), sum(1 for _, f in control if f)))
        return 1
    mutant_file = build(mutant=True)
    mutant = run(mutant_file, "mutant.xml")
    failing = [n for n, f in mutant if f]
    b_fails = any(n.startswith("(b)") for n in failing)
    if failing and b_fails:
        print("MUTANT-FIRES control %d of %d pass; mutant %d of %d fail, including (b); control rc 0"
              % (len(control) - sum(1 for _, f in control if f), len(control), len(failing), len(mutant)))
        return 0
    if failing:
        print("MUTANT-SURVIVES the mutant fails %d case(s) but not (b): %s" % (len(failing), " | ".join(n[:30] for n in failing)))
        return 1
    print("MUTANT-SURVIVES the mutant run passes all %d cases" % len(mutant))
    return 1


if __name__ == "__main__":
    sys.exit(main())
