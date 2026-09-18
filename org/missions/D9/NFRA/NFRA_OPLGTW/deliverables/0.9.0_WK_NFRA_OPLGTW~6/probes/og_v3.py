"""OG-v-3 probe: python og_v3.py AC<n> [--cell-dir <dir>]

Prints its measurement with its denominator, then exactly one line
`VERDICT: PASS-OGV3-AC<n>` or `VERDICT: FAIL-OGV3-AC<n> <reason>`. rc 0 on PASS, 1 on FAIL,
2 on usage error. --cell-dir points the probe at a copy of the cell's deliverables directory
(used by the mutant controls) instead of the real one.
"""
from __future__ import annotations

import ast
import json
import re
import subprocess
import sys
from pathlib import Path

PROBE = Path(__file__).resolve()
CELL_DIR_DEFAULT = PROBE.parents[0].parent  # .../deliverables/0.9.0_WK_NFRA_OPLGTW~6/
ROOT = PROBE.parents[8]

VENV_PY = ROOT / ".venv-og" / "Scripts" / "python.exe"
# The order names this whole directory ("under .../deliverables/0.9.0_WK_NFRA_OPLGTW~4/") as
# where OG-c-2's qualified object keys and VersionIds live; the silver-object VersionIds
# specifically are in replay/silver_versions_after.json, not the prose result.md.
OGC2_DIR = ROOT / "org" / "missions" / "D9" / "NFRA" / "NFRA_OPLGTW" / "deliverables" \
    / "0.9.0_WK_NFRA_OPLGTW~4"
OGC2_RESULT = OGC2_DIR / "producer-deploy-replay.result.md"
SEALED_DIR = Path("C:/tmp/nfra-oplgtw-sealed")
EXPECTED_DIR = SEALED_DIR / "expected"

FORBIDDEN_IMPORT_SUBSTRINGS = ("duckdb", "integrations" + "." + "schwab", "integrations/" + "schwab")

RQ_IDS = ["RQ1", "RQ2", "RQ3", "RQ4", "RQ5", "RQ6"]

# Fields whose value is metadata (a business date, a master id, a status label, prose) rather
# than a computed real-data answer value. Everything else under an answer dict is a
# customer-derived value AC3 must never find inside a committed file.
SAFE_KEYS = {
    "master", "business_date", "latest_business_date", "previous_qualified_business_date",
    "previous_qualified_business_date_status", "note", "delta", "combined_total",
}

AC = [None]


def fail_msg(reason: str) -> str:
    return "VERDICT: FAIL-OGV3-" + AC[0] + " " + reason


def verdict(ok: bool, reason: str = "") -> int:
    if ok:
        print("VERDICT: PASS-OGV3-" + AC[0])
        return 0
    print(fail_msg(reason))
    return 1


def _cell_dir(argv) -> tuple[list, Path]:
    args = list(argv)
    cell = CELL_DIR_DEFAULT
    if "--cell-dir" in args:
        i = args.index("--cell-dir")
        cell = Path(args[i + 1]).resolve()
        del args[i:i + 2]
    return args, cell


def _sealed_expected(cell: Path) -> dict:
    return json.loads((cell / "SEALED_EXPECTED.json").read_text(encoding="ascii"))


def _committed_cell_files(cell: Path) -> list[Path]:
    """The files THIS cell (OG-v-3) produced inside the repository -- never the whole
    deliverables directory, which also carries a prior order's (OG-v-1) files."""
    names = [
        "compute_expected.py",
        "SEALED_EXPECTED.json",
        "sealed-real-expectations.result.md",
        "NFRA_OPLGTW.TO-OG-v-3.sealed-real-expectations.proof_of_spec.json",
        "probes/og_v3.py",
    ]
    return [cell / n for n in names if (cell / n).is_file()]


def _leaf_values(obj, key=None, out=None):
    if out is None:
        out = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            _leaf_values(v, k, out)
    elif isinstance(obj, list):
        for v in obj:
            _leaf_values(v, key, out)
    else:
        if key not in SAFE_KEYS and obj is not None:
            out.append(str(obj))
    return out


def _all_answer_values() -> list[str]:
    vals = []
    for rq in RQ_IDS:
        p = EXPECTED_DIR / f"{rq}.txt"
        ans = json.loads(p.read_text(encoding="ascii"))
        vals.extend(_leaf_values(ans))
    # de-dupe, drop trivially short/ambiguous tokens (e.g. single-word narration)
    seen = []
    for v in vals:
        if v not in seen and re.fullmatch(r"-?[0-9]+(\.[0-9]+)?", v):
            seen.append(v)
    return seen


# ---------------------------------------------------------------------------------------------
def ac1(cell: Path) -> int:
    src_path = cell / "compute_expected.py"
    src = src_path.read_text(encoding="ascii")
    tree = ast.parse(src, filename=str(src_path))
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(a.name for a in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.append(node.module)
    forbidden = [i for i in imports if any(f in i for f in FORBIDDEN_IMPORT_SUBSTRINGS)]
    print("IMPORTS: " + str(len(imports)) + " statement(s) parsed from " + src_path.name
          + "; forbidden " + str(forbidden))

    sealed = _sealed_expected(cell)
    instrument = sealed.get("instrument", "")
    named_ok = ("pyarrow" in instrument and "Decimal" in instrument and "DuckDB" in instrument)
    print("INSTRUMENT NAMED: " + repr(instrument[:60]) + "... named_and_independent=" + str(named_ok))

    ogc2_files = [p for p in OGC2_DIR.rglob("*") if p.is_file() and p.suffix in (".md", ".json")]
    ogc2_text = "\n".join(p.read_text(encoding="utf-8", errors="ignore") for p in ogc2_files)
    used = sealed.get("qualified_objects_used", [])
    version_ids = [o.get("version_id") for o in used]
    after_ogc2 = [v for v in version_ids if v and v in ogc2_text]
    print("VERSIONIDS: " + str(len(used)) + " object(s) used; " + str(len(after_ogc2))
          + " of " + str(len(version_ids)) + " found verbatim across " + str(len(ogc2_files))
          + " file(s) under " + str(OGC2_DIR.relative_to(ROOT)))

    ids_present = sorted(q.get("id") for q in sealed.get("questions", []))
    ids_ok = ids_present == RQ_IDS

    # determinism: rerun the named instrument and confirm the plaintext answers reproduce
    # byte-identically (only the salt/hash may change between runs).
    before = {rq: (EXPECTED_DIR / f"{rq}.txt").read_bytes() for rq in RQ_IDS}
    rerun = subprocess.run([str(VENV_PY), str(src_path)], capture_output=True, text=True, timeout=120)
    after = {rq: (EXPECTED_DIR / f"{rq}.txt").read_bytes() for rq in RQ_IDS}
    reproduced = [rq for rq in RQ_IDS if before[rq] == after[rq]]
    print("RERUN: rc=" + str(rerun.returncode) + "; " + str(len(reproduced)) + " of "
          + str(len(RQ_IDS)) + " answer file(s) byte-identical across two runs")

    problems = []
    if forbidden:
        problems.append("forbidden import(s) " + str(forbidden))
    if not named_ok:
        problems.append("instrument not named/independent in SEALED_EXPECTED.json")
    if len(after_ogc2) != len(version_ids) or not version_ids:
        problems.append(str(len(version_ids) - len(after_ogc2)) + " VersionId(s) not found in OG-c-2's result file")
    if not ids_ok:
        problems.append("question ids " + str(ids_present) + " != " + str(RQ_IDS))
    if rerun.returncode != 0:
        problems.append("rerun rc=" + str(rerun.returncode))
    if len(reproduced) != len(RQ_IDS):
        problems.append(str(len(RQ_IDS) - len(reproduced)) + " answer file(s) not reproduced byte-identically")
    return verdict(not problems, "; ".join(problems))


def ac2(cell: Path) -> int:
    sealed = _sealed_expected(cell)
    top_allowed = {"schema_version", "cell", "instrument", "hash_algorithm",
                   "previous_qualified_business_date", "qualified_objects_used", "questions"}
    extra_top = set(sealed.keys()) - top_allowed
    q_allowed = {"id", "expected_answer_hash", "expected_answer_file"}
    q_problems = []
    for q in sealed.get("questions", []):
        extra = set(q.keys()) - q_allowed
        if extra:
            q_problems.append(q.get("id") + " extra keys " + str(extra))
        h = q.get("expected_answer_hash", "")
        if not re.fullmatch(r"sha256:[0-9a-f]{64}", h):
            q_problems.append(q.get("id") + " malformed hash " + repr(h))
    obj_allowed = {"master", "table", "date", "key", "version_id"}
    for o in sealed.get("qualified_objects_used", []):
        extra = set(o.keys()) - obj_allowed
        if extra:
            q_problems.append("qualified_objects_used entry extra keys " + str(extra))
    print("SEALED_EXPECTED.json: " + str(len(sealed.get("questions", []))) + " question(s), "
          + str(len(sealed.get("qualified_objects_used", []))) + " qualified object(s); "
          + "top-level extra keys " + str(extra_top) + "; per-row problems " + str(len(q_problems)))
    problems = list(extra_top) + q_problems
    return verdict(not problems, "; ".join(str(p) for p in problems))


def ac3(cell: Path) -> int:
    values = _all_answer_values()
    files = _committed_cell_files(cell)
    hits = []
    for f in files:
        text = f.read_text(encoding="utf-8", errors="strict")
        for v in values:
            # word-boundary style: not adjacent to another digit or a decimal point on either side
            pat = r"(?<![0-9.])" + re.escape(v) + r"(?![0-9])"
            if re.search(pat, text):
                hits.append(f.name + " contains " + v)
    print("DENOMINATOR: " + str(len(values)) + " sealed-answer value(s) scanned across "
          + str(len(files)) + " committed cell file(s): " + str([f.name for f in files]))
    print("HITS: " + str(len(hits)) + " " + str(hits[:5]))
    return verdict(not hits, str(len(hits)) + " customer value occurrence(s): " + str(hits[:3]))


def ac4(cell: Path) -> int:
    result_md = cell / "sealed-real-expectations.result.md"
    text = result_md.read_text(encoding="utf-8") if result_md.is_file() else ""
    has_location = "C:/tmp/nfra-oplgtw-sealed" in text
    # A specific retention POLICY statement in prose, not a bare mention of the word
    # "retention" somewhere unrelated -- a table cell echoing this probe's OWN print output
    # (which itself must describe what it checks) is not enough to pass, so the pattern is
    # pinned to the bold markdown label a real prose statement uses ("**Retention:**"),
    # never matched by this probe's own lowercase, non-bold "retention policy (...)" text.
    retention_pat = re.compile(
        r"\*\*Retention:\*\*\s*kept until.{0,80}OG-v-4.{0,120}removed", re.S
    )
    has_retention = bool(retention_pat.search(text))
    print("RESULT FILE: " + str(result_md.name) + " exists=" + str(result_md.is_file())
          + "; states outside-repo location=" + str(has_location)
          + "; states a bound retention policy (kept until OG-v-4 grades, then removed)=" + str(has_retention))
    ok = result_md.is_file() and has_location and has_retention
    problems = []
    if not result_md.is_file():
        problems.append("result file missing")
    if not has_location:
        problems.append("outside-repo location not stated")
    if not has_retention:
        problems.append("retention policy (kept until OG-v-4 grades, then removed) not stated")
    return verdict(ok, "; ".join(problems))


def main(argv) -> int:
    args, cell = _cell_dir(argv)
    if len(args) != 1 or not re.fullmatch(r"AC[1-4]", args[0]):
        print("usage: og_v3.py AC<1-4> [--cell-dir <dir>]")
        return 2
    AC[0] = args[0]
    print("PROBE: og_v3 " + AC[0] + " over " + str(cell))
    return {"AC1": ac1, "AC2": ac2, "AC3": ac3, "AC4": ac4}[AC[0]](cell)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
