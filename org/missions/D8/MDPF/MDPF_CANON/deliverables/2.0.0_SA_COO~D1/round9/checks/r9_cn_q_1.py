#!/usr/bin/env python3
"""r9_cn_q_1.py -- the issuer's checks for MDPF_CANON round 9, cell CN-q-1 (the edge firm gate on /api/general/mdpf/).

  python r9_cn_q_1.py handler   [--root R]   CN-Q-1 HANDLER: n of 14 arms   (the REAL edge handler, synthetic claims)
  python r9_cn_q_1.py seam      [--root R]   CN-Q-1 SEAM:    n of 5 arms    (admitted requests through the REAL router)
  python r9_cn_q_1.py control   [--root R]   CN-Q-1 CONTROL: n of 5 arms    (unmoved behaviour, bounds, the worker's spec)
  python r9_cn_q_1.py selftest               OK line when the pure helpers behave

Each mode prints one line per arm, then 'CN-Q-1 <MODE>: <passed> of <arms> arms'. Exit 0 only when every arm passes.
<root> is the tree whose infra/aws/lambda-edge/ is graded (default: the git toplevel of the cwd). ASCII only.
"""
from __future__ import annotations

import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
EDGE_REL = Path("infra/aws/lambda-edge/auth-validator-edge")
NODE_TIMEOUT = 100

# LF-normalised sha256 of the files this cell must not touch (measured at the cut, box/dell1 @3a6a8d98e0).
PINS = {
    "infra/aws/lambda-edge/auth-validator-edge/aggregate_gate.mjs": "75fcb8a19867328e00eb4499706c647905c4872811b79bc44f032c9f6bb69073",
    "infra/aws/lambda-edge/auth-validator-edge/tier_policy.mjs": "a8ea08cdd7c10bd88b225d10fd7ccc06bcc933ce793f1ab13a5eab83fca09e7c",
    "infra/aws/lambda-edge/auth-validator-edge/render_auth.mjs": "90597af77ac9cd558d788283f7e61327f919c76befe9cdb39b6c09fcc8bb8f23",
    "infra/aws/lambda-edge/auth-validator-edge/ownership_key.mjs": "2f4bdaece6a2d44202d9682e8720f39fabba9fea055dd767e514da601c29a428",
    "infra/aws/lambda-edge/auth-validator-edge/tests/ownership_key.spec.mjs": "7743225d9c5d3acd99c153143b528055dead66bd0aba1b5b430bf5e6a352c94f",
    "infra/aws/lambda-edge/_shared/firm-config.mjs": "7a1b34ac6376c0c71bae371e6d6a57959a2defbada1a9d326a117604c5f0c8c3",
    "infra/aws/lambda-edge/public-data-router/index.mjs": "aff51ca11181d9067ab5ff987402d29555d29745e073b1f24e52176955cb6e1c",
}
BASE_INDEX_SHA = "36dd40b7325de4824557b74fc018938d914517ccec751707b9391afe8a494b68"
BASE_EDGE_FILES = {"aggregate_gate.mjs", "bun.lock", "index.mjs", "ownership_key.mjs", "package-lock.json", "package.json",
                   "render_auth.mjs", "tier_policy.mjs", "tests/ownership_key.spec.mjs"}
IMPORT_LINE = 'import { mdpfGate, MDPF_DENY } from "./mdpf_gate.mjs";'
MARK_START = "// --- MDPF_CANON CN-q-1:"
MARK_END = "// --- end MDPF_CANON CN-q-1 ---"
MIN_SPEC_TESTS = 12


def toplevel() -> Path:
    out = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True)
    if out.returncode != 0:
        sys.exit("ERROR: not in a git work tree and no --root given")
    return Path(out.stdout.strip())


def lf(b: bytes) -> bytes:
    return b.replace(b"\r\n", b"\n")


def sha_lf(path: Path) -> str:
    return hashlib.sha256(lf(path.read_bytes())).hexdigest()


def find_bun() -> str | None:
    w = shutil.which("bun")
    if w:
        return w
    home = Path(os.environ.get("USERPROFILE") or os.environ.get("HOME") or "~").expanduser()
    for name in ("bun.exe", "bun"):
        p = home / ".bun" / "bin" / name
        if p.exists():
            return str(p)
    return None


def run_harness(mode: str, root: Path) -> tuple[list[str], int]:
    node = shutil.which("node")
    if not node:
        sys.exit("ERROR: node not found on PATH")
    p = subprocess.run([node, str(HERE / "q1_harness.mjs"), mode, "--root", str(root)], capture_output=True, text=True,
                       timeout=NODE_TIMEOUT)
    lines = p.stdout.splitlines()
    if p.returncode != 0:
        lines.append("ERROR: harness rc=%d %s" % (p.returncode, p.stderr.strip()[:400]))
    return lines, p.returncode


def arms_of(lines: list[str]) -> dict[str, bool]:
    got: dict[str, bool] = {}
    for ln in lines:
        m = re.match(r"ARM (\S+) (PASS|FAIL) ", ln)
        if m:
            got[m.group(1)] = m.group(2) == "PASS"
    return got


def report(label: str, lines: list[str], arms: dict[str, bool], expected: int) -> int:
    for ln in lines:
        if not ln.startswith("TOTAL "):
            print(ln)
    passed = sum(1 for v in arms.values() if v)
    n = max(expected, len(arms))
    print("CN-Q-1 %s: %d of %d arms" % (label, passed, n))
    return 0 if passed == n and len(arms) == expected else 1


# ---- K3 bounds -------------------------------------------------------------------------------------------------------
def strip_added(index_text: str) -> str | None:
    """index.mjs minus the two insertions the order fixes; None when a marker pair is not exactly once."""
    lines = lf(index_text.encode()).decode().split("\n")
    starts = [i for i, ln in enumerate(lines) if ln.strip().startswith(MARK_START)]
    ends = [i for i, ln in enumerate(lines) if ln.strip() == MARK_END]
    if lines.count(IMPORT_LINE) == 0 and not starts and not ends:
        return "\n".join(lines)  # nothing inserted yet (the base): the whole file is the base text
    if lines.count(IMPORT_LINE) != 1:
        return None
    lines.remove(IMPORT_LINE)
    starts = [i for i, ln in enumerate(lines) if ln.strip().startswith(MARK_START)]
    ends = [i for i, ln in enumerate(lines) if ln.strip() == MARK_END]
    if len(starts) != 1 or len(ends) != 1 or ends[0] <= starts[0] or starts[0] < 1 or lines[starts[0] - 1].strip() != "":
        return None
    del lines[starts[0] - 1: ends[0] + 1]
    return "\n".join(lines)


def bounds(root: Path) -> tuple[bool, str]:
    edge = root / EDGE_REL
    problems: list[str] = []
    seen = set()
    for p in edge.rglob("*"):
        if p.is_file() and "node_modules" not in p.parts and "dist" not in p.parts and "__pycache__" not in p.parts:
            seen.add(p.relative_to(edge).as_posix())
    extra = sorted(s for s in seen - BASE_EDGE_FILES if s != "mdpf_gate.mjs" and not re.fullmatch(r"tests/mdpf_[A-Za-z0-9_.-]+\.mjs", s))
    if extra:
        problems.append("files outside the grant: " + ", ".join(extra))
    for rel, want in PINS.items():
        p = root / rel
        if not p.exists():
            problems.append("missing " + rel)
        elif sha_lf(p) != want:
            problems.append("changed " + rel)
    idx = edge / "index.mjs"
    if not idx.exists():
        problems.append("index.mjs missing")
    else:
        raw = idx.read_bytes()
        if b"\r" in raw:
            problems.append("index.mjs line endings changed (the file is LF; a CR was introduced)")
        base = strip_added(raw.decode("utf-8"))
        if base is None:
            problems.append("index.mjs insertions are not exactly the import line and one marked block")
        elif hashlib.sha256(base.encode()).hexdigest() != BASE_INDEX_SHA:
            problems.append("index.mjs differs from the base outside the two insertions")
    gate = edge / "mdpf_gate.mjs"
    if gate.exists():
        raw = gate.read_bytes()
        if b"\r" in raw:
            problems.append("mdpf_gate.mjs has a CR (the new file is LF, as index.mjs)")
        if any(b > 127 for b in raw):
            problems.append("mdpf_gate.mjs is not ASCII")
    return (not problems, "; ".join(problems) if problems else "protected files byte-equal, index.mjs = base + the two insertions, no file outside the grant")


# ---- K4 / K5 the worker's spec -----------------------------------------------------------------------------------------
def bun_test(bun: str, cwd: Path, spec_rel: str) -> tuple[int, int, int, str]:
    env = dict(os.environ, NO_COLOR="1", FORCE_COLOR="0")
    p = subprocess.run([bun, "test", spec_rel], cwd=str(cwd), capture_output=True, text=True, timeout=60, env=env)
    text = re.sub(r"\x1b\[[0-9;]*m", "", p.stdout + "\n" + p.stderr)
    mp = re.search(r"^\s*(\d+) pass", text, re.M)
    mf = re.search(r"^\s*(\d+) fail", text, re.M)
    return p.returncode, int(mp.group(1)) if mp else 0, int(mf.group(1)) if mf else 0, text


def mutants(ref_gate: str) -> list[tuple[str, str]]:
    """(id, mutated module text): one behaviour broken each. Each replacement must hit the reference exactly once."""
    table = [
        ("M1-always-pass", "export function mdpfGate(uri, payload) {\n", "export function mdpfGate(uri, payload) {\n  return MDPF_PASS;\n"),
        ("M2-internal-not-admitted", 'return payload.firmId === "opal-capital" || payload.userType === "Dev";', "return false;"),
        ("M3-folder-prefix-match", ".includes(route.folder)", ".some((f) => route.folder.startsWith(f))"),
        ("M4-folder-case-insensitive", ".includes(route.folder)", ".map((x) => x.toLowerCase()).includes(String(route.folder).toLowerCase())"),
        ("M5-no-traversal-check", ' && s !== "." && s !== ".."', ""),
        ("M6-no-firm-reads-all", "return MDPF_NO_FIRM_FOLDERS;", 'return ["global", "49financial", "inflection", "cottonwood"];'),
        ("M7-demo-reads-49financial", 'demo: Object.freeze(["global"])', 'demo: Object.freeze(["global", "49financial"])'),
        ("M8-prototype-key", "Object.prototype.hasOwnProperty.call(MDPF_FIRM_FOLDERS, firm) ? MDPF_FIRM_FOLDERS[firm] : []", "MDPF_FIRM_FOLDERS[firm] || []"),
        ("M9-dev-not-admitted", ' || payload.userType === "Dev"', ""),
        ("M10-bare-prefix-passes", "if (segs.length === 0) return { folder: null, clean: false };", "if (segs.length === 0) return null;"),
        ("M11-legacy-prefix-ungated", ', "/api/general/json/mdpf"', ""),
        ("M12-prefix-case-variant-passes", "const exact = p.startsWith(prefix) && uri.startsWith(prefix);", "const exact = true;"),
        ("M13-trailing-empty-segment-anywhere", '(s === "" && i === last && i > 0)', '(s === "")'),
    ]
    out = []
    for mid, a, b in table:
        if ref_gate.count(a) != 1:
            raise SystemExit("selftest: mutant %s anchor count %d" % (mid, ref_gate.count(a)))
        out.append((mid, ref_gate.replace(a, b)))
    return out


def copy_edge_tree(root: Path, dest: Path) -> None:
    for sub in ("auth-validator-edge", "_shared", "public-data-router"):
        src = root / "infra/aws/lambda-edge" / sub
        shutil.copytree(src, dest / "infra/aws/lambda-edge" / sub, ignore=shutil.ignore_patterns("node_modules", "dist", "__pycache__"))


def spec_arms(root: Path) -> tuple[bool, str, bool, str]:
    bun = find_bun()
    spec_rel = "tests/mdpf_gate.spec.mjs"
    spec = root / EDGE_REL / spec_rel
    if not bun:
        return False, "bun not found", False, "bun not found"
    if not spec.exists():
        return False, "tests/mdpf_gate.spec.mjs does not exist", False, "no spec to run against the mutants"
    rc, npass, nfail, text = bun_test(bun, root / EDGE_REL, spec_rel)
    k4 = rc == 0 and nfail == 0 and npass >= MIN_SPEC_TESTS
    k4msg = "spec runs %d pass, %d fail (needs rc 0, 0 fail, at least %d pass)" % (npass, nfail, MIN_SPEC_TESTS)
    if not k4:
        return False, k4msg + " :: " + text.strip().splitlines()[-1][:160] if text.strip() else k4msg, False, "the spec does not pass the real gate, so the mutant run is void"
    ref = (HERE / "ref" / "mdpf_gate.mjs").read_text(encoding="utf-8")
    survivors: list[str] = []
    tmp = Path(tempfile.mkdtemp(prefix="q1_mut_"))
    try:
        copy_edge_tree(root, tmp)
        edge = tmp / EDGE_REL
        for mid, text_m in mutants(ref):
            # the mutants are mutations of the REFERENCE module with the same interface; the worker's spec imports only that interface
            (edge / "mdpf_gate.mjs").write_text(text_m, encoding="utf-8", newline="\n")
            rc2, _, nf2, _ = bun_test(bun, edge, spec_rel)
            if rc2 == 0 and nf2 == 0:
                survivors.append(mid)
        # positive control: the reference module itself passes the worker's spec (so a kill is the spec, not a broken harness)
        (edge / "mdpf_gate.mjs").write_text(ref, encoding="utf-8", newline="\n")
        rc3, _, nf3, _ = bun_test(bun, edge, spec_rel)
        if rc3 != 0 or nf3 != 0:
            survivors.append("CONTROL: the reference module does not pass the spec")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    k5 = not survivors
    return k4, k4msg, k5, ("every one of %d mutants fails the spec" % len(mutants(ref)) if k5 else "survivors: " + ", ".join(survivors))


def main(argv: list[str]) -> int:
    if not argv or argv[0] not in ("handler", "seam", "control", "selftest"):
        print(__doc__)
        return 2
    mode = argv[0]
    if mode == "selftest":
        ref = (HERE / "ref" / "mdpf_gate.mjs").read_text(encoding="utf-8")
        muts = mutants(ref)
        assert len({m for m, _ in muts}) == len(muts)
        sample = "a\nb\n\n" + MARK_START + " x ---\nblock\n" + MARK_END + "\nc"
        t = strip_added(IMPORT_LINE + "\n" + sample)
        assert t == "a\nb\nc", t
        assert strip_added(sample) is None  # a block with no import line
        assert strip_added("a\nb") == "a\nb"  # nothing inserted: the base text itself
        assert strip_added(IMPORT_LINE + "\nb") is None  # an import with no block
        assert strip_added(IMPORT_LINE + "\nx\n" + MARK_START + "\n" + MARK_END) is None  # marker not preceded by a blank line
        print("CN-Q-1 SELFTEST: OK (%d mutants anchor once; strip_added pairs the markers)" % len(muts))
        return 0
    root = Path(os.environ.get("Q1_ROOT") or "") if os.environ.get("Q1_ROOT") else toplevel()
    if "--root" in argv:
        root = Path(argv[argv.index("--root") + 1]).resolve()
    if mode in ("handler", "seam"):
        lines, _ = run_harness(mode, root)
        arms = arms_of(lines)
        return report(mode.upper(), lines, arms, 14 if mode == "handler" else 5)
    # control
    lines, _ = run_harness("control", root)
    arms = arms_of(lines)
    ok3, msg3 = bounds(root)
    arms["K3"] = ok3
    lines.append("ARM K3 %s :: bounds: %s" % ("PASS" if ok3 else "FAIL", msg3))
    k4, m4, k5, m5 = spec_arms(root)
    arms["K4"] = k4
    arms["K5"] = k5
    lines.append("ARM K4 %s :: the worker's own tests: %s" % ("PASS" if k4 else "FAIL", m4))
    lines.append("ARM K5 %s :: the worker's tests catch %s" % ("PASS" if k5 else "FAIL", m5))
    return report("CONTROL", lines, arms, 5)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
