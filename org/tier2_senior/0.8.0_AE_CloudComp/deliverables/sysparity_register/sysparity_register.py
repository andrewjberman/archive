"""
NFRA_SYSPARITY re-ground REGISTER -- denominator + artifact pointer, never a bare verdict.

BUILT BY 0.8.0_AE_CloudComp (base) per 1.0.0_SA_CTO~Z dispatch 170502Z + CORRECTION 170539Z,
to 3.0.0_SA_CVO~Z's spec 170631Z. Design credit: 0.8.0_AE_CloudComp~C.
CVO~Z SPECS AND POPULATES; base BUILDS. That seam is deliberate -- the verifier does not build
the instrument that certifies its own sweep.

--------------------------------------------------------------------------------------------
WHY THIS EXISTS
    The parity harness has a machine denominator (infra/system/scope_contract.json, 22 units).
    The RE-GROUND pass -- the half that decides anything -- had none: verdicts lived only in
    session-log prose. A session was killed mid-sweep; cycles 20-21 are unrecoverable, and a
    Tier-1 decision was blocked on a finding that no longer exists anywhere.

    THE FAILURE MODE: a successor cannot distinguish "swept and clean" from "never swept."

TWO PROPERTIES, ORTHOGONAL, BOTH REQUIRED (the two dispatches each named one):
    RE-DERIVABILITY (content, LOAD-BEARING per CTO~Z 170539Z)
        Persist the DENOMINATOR and the ARTIFACT POINTER, not the verdict. A survivor can
        re-derive a verdict from those; it can never re-derive them from a verdict. A stored
        "verdict: clean" is a TERMINAL CLAIM -- it cannot disagree with anything, so it
        reproduces the very unfalsifiability it was meant to fix, one layer down.
    DURABILITY (timing, per CVO~Z S2)
        The row is written AT VERDICT TIME and fsync'd before record() returns. A register
        written at session close has the identical failure mode and would look like a fix.
    If the two ever trade off, CONTENT WINS -- that is CTO~Z's ruling.

THE THREE STATES ARE STRUCTURAL, NOT PROSE -- this is the whole point:
    NO ROW                      -> NEVER_SWEPT       absence means exactly one thing
    row, verdict=UNRECORDED     -> SWEPT_UNRECORDED  first-class, distinct from absent
    row + a RESOLVING pointer   -> SWEPT             re-derivable
    row, pointer does NOT resolve -> SWEPT_DANGLING  LOUD, never silently trusted
    A gap can never be read as clean: clean requires a row, and a row requires a pointer.

TWO NUMBERS, and the second is MEASURED not trusted:
    units_touched        = units holding any row
    verdicts_recoverable = units whose artifact_pointer ACTUALLY RESOLVES
    The gap between them is the signal. Averaging them together would destroy it.

APPEND-ONLY. A correction appends a superseding row; reads are latest-wins per (unit, cycle)
with full history retained. Rewriting would destroy the older disagreeable evidence, which is
the one thing this artifact exists to keep.
--------------------------------------------------------------------------------------------
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from typing import Any

HERE = os.path.dirname(os.path.abspath(__file__))


def _repo_root() -> str:
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
        if out:
            return out
    except Exception:
        pass
    return os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))


REPO = _repo_root()
CONTRACT = os.path.join(REPO, "infra", "system", "scope_contract.json")
DEFAULT_REGISTER = os.path.join(HERE, "sysparity_register.jsonl")

# A verdict is recorded ALONGSIDE, never as the load-bearing artifact.
VERDICTS = {"CLEAN", "DRIFTED", "BLOCKED", "PARTIAL", "UNRECORDED"}


# ---------------------------------------------------------------------------------------
# DENOMINATOR -- derived at run time, NEVER hand-copied.
# A hand-copied denominator is the frozen-count class this program keeps finding, and it is
# the exact defect the register is meant to detect. So the register must not contain one.
# ---------------------------------------------------------------------------------------
def load_units(contract_path: str = CONTRACT) -> dict[str, str]:
    """Return {unit_id: domain} derived live from scope_contract.json."""
    if not os.path.isfile(contract_path):
        raise SystemExit(f"ERROR: scope contract not found: {contract_path}")
    with open(contract_path, encoding="utf-8") as fh:
        data = json.load(fh)
    units: dict[str, str] = {}
    for domain, body in (data.get("domains") or {}).items():
        for unit in body.get("units") or []:
            uid = unit.get("id")
            if not uid:
                raise SystemExit(f"ERROR: unit without id in domain {domain}")
            if uid in units:
                raise SystemExit(f"ERROR: duplicate unit id {uid}")
            units[uid] = domain
    if not units:
        raise SystemExit("ERROR: scope contract declares zero units -- refusing to proceed")
    return units


def _now_z() -> str:
    # Explicit Z. This host is UTC-4; a bare local timestamp is ambiguous, and an ambiguous
    # timestamp in a provenance record is worse than none.
    import datetime
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _head_commit() -> str:
    try:
        return subprocess.run(
            ["git", "-C", REPO, "rev-parse", "HEAD"],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
    except Exception:
        return "UNKNOWN"


# ---------------------------------------------------------------------------------------
# RECORD -- called AT VERDICT TIME. fsync before returning, so a kill -9 immediately after
# cannot lose the row. If it dies between verdict-formation and this call there is nothing
# any register could do; the window this closes is verdict -> session-close, which is the
# window that actually lost cycles 20-21.
# ---------------------------------------------------------------------------------------
def record(
    unit_id: str,
    verdict: str,
    denominator: str,
    pointers: list[str],
    cycle: str,
    agent: str,
    residuals: list[str] | None = None,
    denominator_count: int | None = None,
    register_path: str = DEFAULT_REGISTER,
    contract_path: str = CONTRACT,
) -> dict[str, Any]:
    units = load_units(contract_path)
    if unit_id not in units:
        raise SystemExit(
            f"ERROR: unit_id '{unit_id}' is not in the scope contract "
            f"({len(units)} declared). An unknown id is an ERROR, not a new row."
        )
    verdict = verdict.upper()
    if verdict not in VERDICTS:
        raise SystemExit(f"ERROR: verdict '{verdict}' not one of {sorted(VERDICTS)}")

    # A non-UNRECORDED verdict with no pointer is exactly the terminal claim we refuse to
    # store. UNRECORDED is the honest value for "the record does not support better".
    if verdict != "UNRECORDED" and not pointers:
        raise SystemExit(
            f"ERROR: verdict '{verdict}' requires at least one --pointer. "
            "A verdict with no artifact pointer is a terminal claim: the successor inherits "
            "it with no means to check it. Use --verdict UNRECORDED if there is no evidence."
        )

    row = {
        "unit_id": unit_id,
        "domain": units[unit_id],
        "verdict": verdict,
        "vintage": {"commit": _head_commit(), "ts": _now_z()},
        "denominator": {"stated": denominator, "count": denominator_count},
        "artifact_pointer": [_parse_pointer(p) for p in pointers],
        "agent": agent,
        "cycle": cycle,
        "residuals": residuals or [],
        "contract_units_at_write": len(units),
    }

    os.makedirs(os.path.dirname(os.path.abspath(register_path)) or ".", exist_ok=True)
    line = json.dumps(row, sort_keys=True) + "\n"
    # O_APPEND + fsync: the row is on disk before this function returns.
    fd = os.open(register_path, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o644)
    try:
        os.write(fd, line.encode("utf-8"))
        os.fsync(fd)
    finally:
        os.close(fd)
    return row


def _parse_pointer(spec: str) -> dict[str, str]:
    """
    Accepted forms:
      git:<commit-ish>:<path>   -- resolvable, the strong form
      file:<path>               -- resolvable
      tool:<invocation>         -- NOT mechanically resolvable; counted honestly, never silently
    """
    if spec.startswith("git:"):
        rest = spec[4:]
        commit, _, path = rest.partition(":")
        return {"kind": "git", "commit": commit, "path": path}
    if spec.startswith("file:"):
        return {"kind": "file", "path": spec[5:]}
    if spec.startswith("tool:"):
        return {"kind": "tool", "invocation": spec[5:]}
    return {"kind": "opaque", "raw": spec}


# ---------------------------------------------------------------------------------------
# RESOLUTION -- the falsifiability channel. The pointer is the field capable of DISAGREEING,
# so it is EXERCISED, never read. A dangling pointer is LOUD.
# ---------------------------------------------------------------------------------------
def resolve_pointer(ptr: dict[str, str]) -> tuple[bool, str]:
    kind = ptr.get("kind")
    if kind == "git":
        commit, path = ptr.get("commit", ""), ptr.get("path", "")
        if not commit or not path:
            return False, "malformed git pointer"
        rc = subprocess.run(
            ["git", "-C", REPO, "cat-file", "-e", f"{commit}:{path}"],
            capture_output=True, text=True,
        ).returncode
        return (rc == 0), ("resolves" if rc == 0 else f"DANGLING: {commit}:{path} not found")
    if kind == "file":
        p = ptr.get("path", "")
        full = p if os.path.isabs(p) else os.path.join(REPO, p)
        ok = os.path.exists(full)
        return ok, ("resolves" if ok else f"DANGLING: {p} does not exist")
    if kind == "tool":
        # Honest: we cannot mechanically confirm a tool invocation. It is NOT counted as
        # recoverable -- silently counting it would be the instrument lying in our favour.
        return False, "UNRESOLVABLE-KIND: tool invocation, not mechanically checkable"
    return False, f"UNRESOLVABLE-KIND: {kind}"


def load_rows(register_path: str) -> list[dict[str, Any]]:
    if not os.path.isfile(register_path):
        return []
    rows = []
    with open(register_path, encoding="utf-8") as fh:
        for n, line in enumerate(fh, 1):
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                # A corrupt line is surfaced, never skipped silently.
                rows.append({"_corrupt": True, "_line_no": n, "_raw": line[:200]})
    return rows


def report(register_path: str = DEFAULT_REGISTER, contract_path: str = CONTRACT) -> dict[str, Any]:
    units = load_units(contract_path)
    rows = load_rows(register_path)
    corrupt = [r for r in rows if r.get("_corrupt")]
    good = [r for r in rows if not r.get("_corrupt")]

    # latest-wins per (unit, cycle); full history retained on disk regardless.
    latest: dict[tuple[str, str], dict[str, Any]] = {}
    for r in good:
        latest[(r.get("unit_id", ""), r.get("cycle", ""))] = r

    per_unit: dict[str, dict[str, Any]] = {}
    for (uid, _cycle), r in latest.items():
        if uid not in units:
            continue  # an unknown id cannot silently become coverage
        cur = per_unit.get(uid)
        if cur is None or r.get("vintage", {}).get("ts", "") >= cur.get("vintage", {}).get("ts", ""):
            per_unit[uid] = r

    states: dict[str, str] = {}
    detail: dict[str, str] = {}
    for uid in units:
        r = per_unit.get(uid)
        if r is None:
            states[uid] = "NEVER_SWEPT"
            detail[uid] = "no row -- absence means exactly one thing"
            continue
        if r.get("verdict") == "UNRECORDED":
            states[uid] = "SWEPT_UNRECORDED"
            detail[uid] = "swept, record did not survive -- NOT clean"
            continue
        ptrs = r.get("artifact_pointer") or []
        results = [resolve_pointer(p) for p in ptrs]
        if any(ok for ok, _ in results):
            states[uid] = "SWEPT"
            detail[uid] = "; ".join(m for _, m in results)
        else:
            states[uid] = "SWEPT_DANGLING"
            detail[uid] = "; ".join(m for _, m in results) or "no pointers"

    touched = sum(1 for u in units if states[u] != "NEVER_SWEPT")
    recoverable = sum(1 for u in units if states[u] == "SWEPT")
    return {
        "contract_units": len(units),
        "units_touched": touched,
        "verdicts_recoverable": recoverable,
        "states": states,
        "detail": detail,
        "corrupt_lines": corrupt,
        "register_path": register_path,
    }


def render(rep: dict[str, Any]) -> str:
    n = rep["contract_units"]
    L = []
    L.append("NFRA_SYSPARITY RE-GROUND REGISTER")
    L.append(f"  register:   {rep['register_path']}")
    L.append(f"  DENOMINATOR: {n} units, derived at run time from scope_contract.json (never hand-copied)")
    L.append("")
    L.append(f"  units touched:        {rep['units_touched']}/{n}")
    L.append(f"  verdicts RECOVERABLE: {rep['verdicts_recoverable']}/{n}   <- pointers actually resolved, not trusted")
    if rep["units_touched"] != rep["verdicts_recoverable"]:
        L.append(f"  >> GAP: {rep['units_touched'] - rep['verdicts_recoverable']} unit(s) touched but NOT re-derivable. That gap IS the signal.")
    L.append("")
    order = {"NEVER_SWEPT": 0, "SWEPT_DANGLING": 1, "SWEPT_UNRECORDED": 2, "SWEPT": 3}
    for uid in sorted(rep["states"], key=lambda u: (order.get(rep["states"][u], 9), u)):
        st = rep["states"][uid]
        mark = {"NEVER_SWEPT": "!!", "SWEPT_DANGLING": "!!", "SWEPT_UNRECORDED": " ~", "SWEPT": " ok"}.get(st, "  ")
        L.append(f"  {mark} {uid:34s} {st:18s} {rep['detail'][uid][:88]}")
    if rep["corrupt_lines"]:
        L.append("")
        L.append(f"  !! {len(rep['corrupt_lines'])} CORRUPT LINE(S) -- surfaced, not skipped:")
        for c in rep["corrupt_lines"]:
            L.append(f"     line {c['_line_no']}: {c['_raw'][:80]}")
    return "\n".join(L)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="NFRA_SYSPARITY re-ground register")
    sub = ap.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("record", help="append one row AT VERDICT TIME (fsync'd before return)")
    r.add_argument("--unit", required=True)
    r.add_argument("--verdict", required=True, help=f"one of {sorted(VERDICTS)}")
    r.add_argument("--denominator", default="", help="what the pass was OF: population, predicate, exclusions")
    r.add_argument("--denominator-count", type=int, default=None)
    r.add_argument("--pointer", action="append", default=[],
                   help="git:<commit-ish>:<path> | file:<path> | tool:<invocation> (repeatable)")
    r.add_argument("--cycle", default="")
    r.add_argument("--agent", default=os.environ.get("OPAL_AGENT_SERIAL", "UNKNOWN"))
    r.add_argument("--residual", action="append", default=[])
    r.add_argument("--register", default=DEFAULT_REGISTER)

    p = sub.add_parser("report", help="coverage as a SET DIFFERENCE against the derived denominator")
    p.add_argument("--register", default=DEFAULT_REGISTER)
    p.add_argument("--json", action="store_true")

    sub.add_parser("units", help="print the derived denominator and exit")

    a = ap.parse_args(argv)

    if a.cmd == "units":
        units = load_units()
        for uid, dom in sorted(units.items(), key=lambda kv: (kv[1], kv[0])):
            print(f"{dom:16s} {uid}")
        print(f"TOTAL {len(units)}")
        return 0

    if a.cmd == "record":
        row = record(
            unit_id=a.unit, verdict=a.verdict, denominator=a.denominator,
            pointers=a.pointer, cycle=a.cycle, agent=a.agent,
            residuals=a.residual, denominator_count=a.denominator_count,
            register_path=a.register,
        )
        print(f"RECORDED {row['unit_id']} verdict={row['verdict']} cycle={row['cycle']} -> {a.register}")
        return 0

    if a.cmd == "report":
        rep = report(a.register)
        if a.json:
            print(json.dumps(rep, indent=2, sort_keys=True))
        else:
            print(render(rep))
        # A dangling pointer or a corrupt line is LOUD -- nonzero exit.
        bad = sum(1 for s in rep["states"].values() if s == "SWEPT_DANGLING") + len(rep["corrupt_lines"])
        return 2 if bad else 0

    return 1


if __name__ == "__main__":
    sys.exit(main())
