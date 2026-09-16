#!/usr/bin/env python3
"""TX-v-1 probe: grades the expected-case manifest for one criterion.

Usage: py -3.12 tx_v_1.py AC1|AC2|AC3|AC4 [--manifest PATH] [--script PATH]
Prints its measurement with vintage and denominator, then exactly one VERDICT line (AC1-AC3);
AC4 is a judgment criterion and prints its output with no verdict.
"""
from __future__ import annotations

import argparse
import ast
import datetime as dt
import hashlib
import json
import re
import subprocess
import sys
import tempfile
import unicodedata
from decimal import Decimal
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = Path(subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=str(HERE), capture_output=True,
                           check=True).stdout.decode().strip())
MANIFEST = ROOT / "data/mdpf/tests/taxsma/expected_cases.json"
SCRIPT = HERE.parent / "author_expected_cases.py"
TWO = Decimal("0.01")
ROW_RE = re.compile(r"^\| (A0[1-8]) [^|]*\| (FWD-\d) \| (.*) \|\s*$", re.M)


def git(*a) -> str:
    return subprocess.run(["git", "-C", str(ROOT), *a], capture_output=True, check=True).stdout.decode("utf-8")


def vintage(path: Path) -> None:
    raw = path.read_bytes().replace(b"\r\n", b"\n")
    print(f"VINTAGE: HEAD {git('rev-parse', '--short=10', 'HEAD').strip()}  manifest {path.name} sha256(LF) "
          f"{hashlib.sha256(raw).hexdigest()[:16]}  at {dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}")


def derive_clauses(prd: str) -> dict:
    out = {}
    for pid, fwd, cell in ROW_RE.findall(prd):
        cl = []
        for s in re.split(r"(?<=\.)\s+(?=[A-Z])", cell.strip()):
            for c in s.split("; "):
                c = c.strip().rstrip(".")
                if c:
                    cl.append(c)
        for i, c in enumerate(cl, 1):
            out[f"{pid}.c{i}"] = c
    return out


def getp(obj, path: str):
    cur = obj
    for part in path.split("."):
        if not isinstance(cur, dict) or part not in cur:
            raise KeyError(path)
        cur = cur[part]
    return cur


def resolve(v, led: dict):
    if isinstance(v, dict):
        if set(v) == {"num"}:
            return ("num", led.get(v["num"]))
        return {k: resolve(x, led) for k, x in v.items()}
    if isinstance(v, list):
        return [resolve(x, led) for x in v]
    return v


def observables(arm: dict):
    yield "expected_observable", arm.get("expected_observable")
    for side in ("engaged", "disengaged"):
        yield side, arm.get("control", {}).get(side, {}).get("expected_observable")
    for cname, c in (arm.get("cases") or {}).items():
        if isinstance(c, dict) and "expected_observable" in c:
            yield f"case:{cname}", c["expected_observable"]


def vocab_map(contract: dict) -> dict:
    ax = contract["status_axes"]
    m = {k: set(v) for k, v in ax.items()}
    m["reason_codes"] = set(contract["reason_codes"])
    m["kind"] = set(contract["membership"]["disposition_kinds"])
    m["row_kind"] = set(contract["workbook"]["row_kind"])
    m["error"] = set(contract["capability"]["errors"])
    m["membership_date_basis"] = {"FIRST_OBSERVED_UTC", "UNVERIFIED"}  # contract field_types.membership_date_basis text
    return m


def leaves(v):
    if isinstance(v, str):
        yield v
    elif isinstance(v, list):
        for x in v:
            yield from leaves(x)
    elif isinstance(v, dict):
        for x in v.values():
            yield from leaves(x)


def vocab_violations(obj, vm: dict, where: str) -> list:
    bad = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            hit = [name for name in vm if k == name or k.startswith(name + "_") or k.endswith("_" + name)]
            if hit:
                name = max(hit, key=len)
                for s in leaves(v):
                    if s not in vm[name]:
                        bad.append(f"{where}.{k}={s!r} not in contract {name}")
            bad += vocab_violations(v, vm, f"{where}.{k}")
    elif isinstance(obj, list):
        for i, x in enumerate(obj):
            bad += vocab_violations(x, vm, f"{where}[{i}]")
    return bad


def ac1(m: dict) -> str:
    prd_c = m["prd_ref"]["commit"]
    derived = derive_clauses(git("show", f"{prd_c}:{m['prd_ref']['path']}"))
    wt = derive_clauses((ROOT / m["prd_ref"]["path"]).read_text(encoding="utf-8"))
    contract = json.loads(git("show", f"{m['contract_ref']['commit']}:{m['contract_ref']['path']}"))
    vm = vocab_map(contract)
    arms = m["arms"]
    fails = []
    print(f"DENOMINATOR: PRD s.4 at {prd_c}: {len({k[:3] for k in derived})} properties, {len(derived)} clauses "
          f"(worktree PRD derives {len(wt)} clauses, identical={wt == derived})")
    ids = [a["id"] for a in arms]
    if len(ids) != len(set(ids)):
        fails.append("duplicate arm ids")
    for cid, text in m["prd_clause_text"].items():
        if derived.get(cid) != text:
            fails.append(f"clause text {cid} differs from the PRD")
    if set(m["prd_clause_text"]) != set(derived):
        fails.append("manifest clause set != PRD clause set")
    covered = {c: [] for c in derived}
    by_id = {a["id"]: a for a in arms}
    for a in arms:
        aid = a["id"]
        if not re.fullmatch(r"A0[1-8]-\d{2}", aid) or a["property"] != aid[:3]:
            fails.append(f"{aid}: bad id/property")
        for c in a["prd_clauses"]:
            if c not in derived:
                fails.append(f"{aid}: cites unknown clause {c}")
            else:
                covered[c].append(aid)
        fi = a.get("fixture_input")
        if not isinstance(fi, dict) or not fi:
            fails.append(f"{aid}: empty fixture_input")
        else:
            h = hashlib.sha256(json.dumps(fi, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()).hexdigest()
            if h != a.get("fixture_input_sha256"):
                fails.append(f"{aid}: fixture_input_sha256 mismatch")
        ctl = a.get("control", {})
        e, d = ctl.get("engaged", {}), ctl.get("disengaged", {})
        for side, s in (("engaged", e), ("disengaged", d)):
            if "input" not in s or not isinstance(s.get("expected_observable"), dict) or not s["expected_observable"]:
                fails.append(f"{aid}: {side} control lacks input or expected_observable")
        if not a.get("expected_observable") or a["expected_observable"] != e.get("expected_observable"):
            fails.append(f"{aid}: expected_observable missing or != engaged observable")
        led = {x["id"]: x["result"] for x in m["ledger"]}
        E, D = resolve(e.get("expected_observable"), led), resolve(d.get("expected_observable"), led)
        try:
            if ctl.get("kind") == "DIFFERENCE":
                if not ctl.get("differs_on"):
                    fails.append(f"{aid}: DIFFERENCE with no differs_on")
                for p in ctl.get("differs_on", []):
                    if getp(E, p) == getp(D, p):
                        fails.append(f"{aid}: differs_on {p} is equal engaged/disengaged")
                for p in ctl.get("invariant_within", []):
                    if getp(E, p) != getp(D, p):
                        fails.append(f"{aid}: invariant_within {p} differs")
            elif ctl.get("kind") == "INVARIANCE":
                for p in ctl.get("invariant_on", []):
                    if getp(E, p) != getp(D, p):
                        fails.append(f"{aid}: invariant_on {p} differs")
                ca = by_id.get(ctl.get("contrast_arm"))
                if not ca or ca["control"]["kind"] != "DIFFERENCE":
                    fails.append(f"{aid}: contrast_arm missing or not a DIFFERENCE arm")
            else:
                fails.append(f"{aid}: control kind {ctl.get('kind')!r}")
        except KeyError as exc:
            fails.append(f"{aid}: control path {exc} absent")
        for where, ob in observables(a):
            fails += vocab_violations(ob, vm, f"{aid}:{where}")
    uncovered = [c for c, v in covered.items() if not v]
    fails += [f"clause {c} has no arm" for c in uncovered]
    mem_total = mem_cov = 0
    for cid, members in m["clause_members"].items():
        for mem in members:
            mem_total += 1
            if cid not in derived or mem not in derived[cid]:
                fails.append(f"member {cid}:{mem!r} is not a substring of the clause")
                continue
            if any(cid in by_id[x]["prd_clauses"] and mem in by_id[x]["covers_members"] for x in covered.get(cid, [])):
                mem_cov += 1
            else:
                fails.append(f"member {cid}:{mem!r} has no arm")
    print("PER PROPERTY: property  clauses covered  arms  local  difference  invariance")
    for p in sorted({k[:3] for k in derived}):
        pc = [c for c in derived if c.startswith(p + ".")]
        pa = [a for a in arms if a["property"] == p]
        row = {"clauses": len(pc), "arms": len(pa), "local_arms": sum(a["environment"] == "LOCAL" for a in pa),
               "difference_controls": sum(a["control"]["kind"] == "DIFFERENCE" for a in pa),
               "invariance_controls": sum(a["control"]["kind"] == "INVARIANCE" for a in pa)}
        s = m["summary"].get(p, {})
        if any(s.get(k) != v for k, v in row.items()):
            fails.append(f"summary for {p} disagrees with the arms")
        print(f"  {p}  {sum(1 for c in pc if covered[c])}/{len(pc)}  {row['arms']}  {row['local_arms']}  "
              f"{row['difference_controls']}  {row['invariance_controls']}")
    print(f"TOTALS: arms {len(arms)}; clauses covered {len(derived) - len(uncovered)}/{len(derived)}; "
          f"list members covered {mem_cov}/{mem_total}; vocabulary fields checked against contract "
          f"{m['contract_ref']['version']} @{m['contract_ref']['commit']}")
    for f in fails[:40]:
        print("FAIL-DETAIL: " + f)
    return "VERDICT: PASS-TXV1-AC1" if not fails else f"VERDICT: FAIL-TXV1-AC1 {len(fails)} defect(s); first: {fails[0]}"


def rend(d: Decimal, unit: str) -> str:
    s = format(d.quantize(TWO), "f") if unit == "USD" else str(int(d))
    return f"({s})" if d < 0 else s


def ac2(m: dict, script: Path) -> str:
    fails = []
    amounts = m["fixture_world"]["amounts"]
    seen = {}
    for e in m["ledger"]:
        unit = e["unit"]
        if e["op"] == "count_distinct":
            r = Decimal(len(set(e["members"])))
            worked = "count_distinct(" + ", ".join(e["members"]) + ") = " + str(int(r))
        else:
            vals = []
            for t in e["terms"]:
                if t in amounts:
                    vals.append(Decimal(amounts[t]["value"]))
                elif t in seen:
                    vals.append(seen[t])
                else:
                    fails.append(f"ledger {e['id']}: term {t} unresolved or forward")
                    vals.append(Decimal(0))
            if e["op"] == "sum":
                r = sum(vals, Decimal(0))
                sep = " + "
            elif e["op"] == "sub":
                r = vals[0] - sum(vals[1:], Decimal(0))
                sep = " - "
            else:
                fails.append(f"ledger {e['id']}: unknown op")
                continue
            res = format(r.quantize(TWO), "f") if unit == "USD" else str(int(r))
            worked = sep.join(rend(v, unit) for v in vals) + " = " + res
        res = format(r.quantize(TWO), "f") if unit == "USD" else str(int(r))
        if res != e["result"]:
            fails.append(f"ledger {e['id']}: recomputed {res} != recorded {e['result']}")
        if worked != e["worked"]:
            fails.append(f"ledger {e['id']}: worked text does not match its arithmetic")
        seen[e["id"]] = r
    refs = raw = 0
    used = set()

    def walk(v, where):
        nonlocal refs, raw
        if isinstance(v, dict):
            if set(v) == {"num"}:
                refs += 1
                used.add(v["num"])
                if v["num"] not in seen:
                    fails.append(f"{where}: num ref {v['num']} is not a ledger entry")
                return
            for k, x in v.items():
                walk(x, f"{where}.{k}")
        elif isinstance(v, list):
            for i, x in enumerate(v):
                walk(x, f"{where}[{i}]")
        elif isinstance(v, bool) or v is None:
            return
        elif isinstance(v, (int, float)):
            raw += 1
            fails.append(f"{where}: raw number {v} in an expected observable")
        elif isinstance(v, str) and re.fullmatch(r"-?\d+(\.\d+)?", v):
            raw += 1
            fails.append(f"{where}: numeric string {v!r} in an expected observable")
    for a in m["arms"]:
        for where, ob in observables(a):
            walk(ob, f"{a['id']}:{where}")
    print(f"LEDGER: {len(m['ledger'])} entries recomputed by Decimal; {len(amounts)} synthetic amounts; "
          f"{refs} expected-number references ({len(used)} distinct), {raw} unworked numbers")
    tree = ast.parse(script.read_text(encoding="utf-8"))
    imports, dyn = [], []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports += [a.name for a in node.names]
        elif isinstance(node, ast.ImportFrom):
            if node.level:
                fails.append(f"relative import from {node.module}")
            imports.append(node.module or "")
        elif isinstance(node, ast.Call):
            f = node.func
            if isinstance(f, ast.Name) and f.id in ("__import__", "exec", "eval", "compile"):
                dyn.append(f.id)
            elif isinstance(f, ast.Attribute) and f.attr in ("import_module", "run_path", "run_module", "__import__"):
                dyn.append(f.attr)
    tops = sorted({i.split(".")[0] for i in imports})
    nonstd = [t for t in tops if t not in sys.stdlib_module_names]
    engine = [i for i in imports if re.search(r"taxsma|mdpf|gateway|opal|lambda_function", i, re.I)]
    fails += [f"non-stdlib import {t}" for t in nonstd] + [f"engine import {t}" for t in engine] + \
             [f"dynamic import/exec call {t}" for t in dyn]
    print(f"IMPORT CENSUS (AST of {script.name}): {len(tops)} top-level modules {tops}; non-stdlib {len(nonstd)}; "
          f"engine-named {len(engine)}; dynamic import/exec calls {len(dyn)}")
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "regen.json"
        code = "\n".join([
            "import sys, runpy, json",
            "b = set(sys.modules)",
            "p, o = sys.argv[1], sys.argv[2]",
            "sys.argv = [p, '--out', o]",
            "try:",
            "    runpy.run_path(p, run_name='__main__')",
            "except SystemExit as x:",
            "    assert not x.code, x.code",
            "n = sorted(set(sys.modules) - b)",
            "print('MODULES:' + json.dumps([[k, getattr(sys.modules[k], '__file__', None)] for k in n]))",
        ])
        pr = subprocess.run([sys.executable, "-c", code, str(script), str(out)], capture_output=True, timeout=100)
        line = [x for x in pr.stdout.decode("utf-8", "replace").splitlines() if x.startswith("MODULES:")]
        if pr.returncode != 0 or not line:
            fails.append(f"runtime census run failed rc={pr.returncode}: {pr.stderr.decode('utf-8', 'replace')[-300:]}")
            mods = []
        else:
            mods = json.loads(line[0][8:])
        root_s = str(ROOT).replace("\\", "/").lower()
        in_repo = [k for k, f in mods if f and str(f).replace("\\", "/").lower().startswith(root_s)]
        rt_nonstd = [k for k, _ in mods if k.split(".")[0].lstrip("_") not in sys.stdlib_module_names
                     and k.split(".")[0] not in sys.stdlib_module_names]
        fails += [f"runtime import from the repository: {k}" for k in in_repo] + \
                 [f"runtime non-stdlib module {k}" for k in rt_nonstd]
        print(f"IMPORT CENSUS (runtime, {sys.executable.split(chr(92))[-1]}): {len(mods)} modules newly loaded; "
              f"from the repository {len(in_repo)}; non-stdlib {len(rt_nonstd)}")
        if out.exists():
            a = out.read_bytes().replace(b"\r\n", b"\n")
            b = MANIFEST.read_bytes().replace(b"\r\n", b"\n") if MANIFEST.exists() else b""
            same = a == b
            print(f"REGENERATION: author script output sha256 {hashlib.sha256(a).hexdigest()[:16]} vs committed "
                  f"{hashlib.sha256(b).hexdigest()[:16]} identical={same}")
            if not same:
                fails.append("regenerated manifest differs from data/mdpf/tests/taxsma/expected_cases.json")
    for f in fails[:40]:
        print("FAIL-DETAIL: " + f)
    return "VERDICT: PASS-TXV1-AC2" if not fails else f"VERDICT: FAIL-TXV1-AC2 {len(fails)} defect(s); first: {fails[0]}"


def norm_digits(s: str) -> str:
    return "".join(str(unicodedata.digit(c)) if unicodedata.digit(c, None) is not None else c for c in s)


SYNTH = re.compile(r"SYNTH-[A-Z0-9-]+")
ISO = re.compile(r"\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}(:\d{2})?Z)?")
AMT = re.compile(r"-?\d+\.\d{2}")


def cell_ok(col: str, v, fw: dict) -> bool:
    if v is None or v == "":
        return True
    if col == "Index":
        return isinstance(v, int) or v == "Total"
    if col == "Account Number":
        return isinstance(v, str) and re.fullmatch(r"[0-9*.\-E]+", norm_digits(v)) is not None
    if col in ("Ready", "Traded"):
        return v in fw["traded_ready_values"]
    if col in ("Inception Date", "Last Trade Date"):
        return isinstance(v, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", v) is not None
    if col == "AUM (Mn)":
        return v in fw["sales_estimates_mn"]
    return isinstance(v, str) and SYNTH.fullmatch(v) is not None


def ac3(m: dict, raw_text: str) -> str:
    fails = []
    fw = m["fixture_world"]
    reg_vals = {a["value"] for a in fw["amounts"].values()}
    acct_tokens = amounts_seen = 0

    def scan(v, where):
        nonlocal acct_tokens
        if isinstance(v, dict):
            for k, x in v.items():
                scan(x, f"{where}.{k}")
        elif isinstance(v, list):
            for i, x in enumerate(v):
                scan(x, f"{where}[{i}]")
        elif isinstance(v, bool) or v is None:
            return
        elif isinstance(v, int):
            if abs(v) >= 10 ** 7:
                acct_tokens += 1
                if not str(abs(v)).startswith("99"):
                    fails.append(f"{where}: integer {v} outside the synthetic key block")
        elif isinstance(v, str):
            if re.fullmatch(r"[0-9a-f]{64}", v) or AMT.fullmatch(v) or ISO.fullmatch(v):
                return
            s = norm_digits(v)
            if where.endswith(".worked"):
                s = re.sub(r"-?\d+\.\d{2}(?!\d)", " ", s)
            for tok in re.findall(r"(?<!\d)\d{4}-\d{4}(?!\d)", s) + re.findall(r"\d{8,}", s):
                acct_tokens += 1
                if not (tok.startswith("99") or tok.startswith("0099")):
                    fails.append(f"{where}: account-shaped token {tok} outside the synthetic key block")
    scan(m, "manifest")

    def amounts_in(v, where):
        nonlocal amounts_seen
        if isinstance(v, dict):
            for k, x in v.items():
                amounts_in(x, f"{where}.{k}")
        elif isinstance(v, list):
            for i, x in enumerate(v):
                amounts_in(x, f"{where}[{i}]")
        elif isinstance(v, str) and AMT.fullmatch(v):
            amounts_seen += 1
            if v not in reg_vals:
                fails.append(f"{where}: fixture amount {v} is not a declared synthetic amount")
    amounts_in({k: v for k, v in fw.items() if k != "amounts"}, "fixture_world")
    for a in m["arms"]:
        amounts_in(a["fixture_input"], f"{a['id']}.fixture_input")
        for side in ("engaged", "disengaged"):
            amounts_in(a["control"][side]["input"], f"{a['id']}.{side}.input")
        amounts_in({k: v.get("input") if isinstance(v, dict) else v for k, v in (a.get("cases") or {}).items()},
                   f"{a['id']}.cases")
    cells = 0

    def cells_in(v, where):
        nonlocal cells
        if isinstance(v, dict):
            if "column" in v and "value" in v:
                cells += 1
                if not cell_ok(v["column"], v["value"], fw):
                    fails.append(f"{where}: cell {v['column']}={v['value']!r} outside the closed synthetic vocabulary")
            for key in ("cells", "append_before_r8"):
                if isinstance(v.get(key), dict):
                    for col, val in v[key].items():
                        cells += 1
                        if not cell_ok(col, val, fw):
                            fails.append(f"{where}: cell {col}={val!r} outside the closed synthetic vocabulary")
            if isinstance(v.get("set"), dict):
                for rc, val in v["set"].items():
                    cells += 1
                    if not cell_ok(rc.split(".", 1)[1], val, fw):
                        fails.append(f"{where}: cell {rc}={val!r} outside the closed synthetic vocabulary")
            if v.get("op") == "insert_rows":
                for r in v.get("rows", []):
                    for col, val in r.items():
                        cells += 1
                        if not cell_ok(col, val, fw):
                            fails.append(f"{where}: inserted cell {col}={val!r} outside the vocabulary")
            for k, x in v.items():
                if k not in ("cells", "append_before_r8", "set"):
                    cells_in(x, f"{where}.{k}")
        elif isinstance(v, list):
            for i, x in enumerate(v):
                cells_in(x, f"{where}[{i}]")
    cells_in({k: v for k, v in fw.items() if k.startswith("WB-")}, "fixture_world")
    for a in m["arms"]:
        cells_in(a["control"], a["id"])
    for case in (m["arms"][[x["id"] for x in m["arms"]].index("A02-05")].get("cases") or {}).get("rejected", []) \
            if any(x["id"] == "A02-05" for x in m["arms"]) else []:
        sv = case["scalar"].get("string_value")
        cells += 1
        if sv is not None and not cell_ok("Account Number", sv, fw):
            fails.append(f"A02-05 case {case['form']}: {sv!r} outside the vocabulary")
    contract = json.loads(git("show", f"{m['contract_ref']['commit']}:{m['contract_ref']['path']}"))
    prd = git("show", f"{m['prd_ref']['commit']}:{m['prd_ref']['path']}")
    real = {contract["identity"]["reporting_master"], contract["identity"]["base_master_control"],
            contract["workbook"]["site_id"], contract["workbook"]["item_id"]}
    real |= set(re.findall(r"\d{4}-\d{4}", contract["identity"]["trading_master_role"]))
    real |= set(re.findall(r"(?<![\d-])\d{4}-\d{4}(?![\d-])", prd)) | set(re.findall(r"(?<![0-9a-f])\d{8,}(?![0-9a-f])", prd))
    forms = set()
    for r in real:
        forms.add(r)
        d = r.replace("-", "")
        if d.isdigit():
            forms |= {d, d[-8:], "00" + d[-8:]}
    text = norm_digits(raw_text)
    hits = sorted(f for f in forms if f in text)
    fails += [f"real identifier form {h!r} from the PRD/contract appears in the manifest" for h in hits]
    print(f"ACCOUNT TOKENS: {acct_tokens} account-shaped tokens scanned across the whole manifest; rule: begins 99 / 0099")
    print(f"AMOUNTS: {amounts_seen} fixture amount literals, each checked against {len(reg_vals)} declared synthetic values")
    print(f"NAMES: {cells} workbook cells checked against the closed per-column vocabulary (SYNTH labels, enumerated values)")
    print(f"REAL IDENTIFIERS: {len(forms)} forms from the PRD @{m['prd_ref']['commit']} and contract "
          f"@{m['contract_ref']['commit']} (masters, site/item, account-shaped PRD tokens); hits {len(hits)}")
    print("LIMIT: no intersection with the protected live account population was run (outside the order's paths); "
          "the claim is by construction, closed vocabulary and non-intersection with the specification's identifiers")
    for f in fails[:40]:
        print("FAIL-DETAIL: " + f)
    return "VERDICT: PASS-TXV1-AC3" if not fails else f"VERDICT: FAIL-TXV1-AC3 {len(fails)} defect(s); first: {fails[0]}"


def ac4(m: dict) -> None:
    derived = derive_clauses(git("show", f"{m['prd_ref']['commit']}:{m['prd_ref']['path']}"))
    print(f"JUDGMENT INPUT: arm set against PRD s.4 @{m['prd_ref']['commit']} ({len(derived)} clauses, "
          f"{len(m['arms'])} arms)")
    for cid, text in derived.items():
        arms = [a["id"] for a in m["arms"] if cid in a["prd_clauses"]]
        print(f"  {cid} [{', '.join(arms)}] {text}")
        for mem in m["clause_members"].get(cid, []):
            ma = [a["id"] for a in m["arms"] if cid in a["prd_clauses"] and mem in a["covers_members"]]
            print(f"      member {mem!r}: {', '.join(ma)}")
    print("NON-LOCAL ARMS: " + ", ".join(f"{a['id']} ({a['environment']}, {a['executes_in']})"
                                         for a in m["arms"] if a["environment"] != "LOCAL"))
    print(f"READINGS ({len(m['readings'])}):")
    for rid, t in m["readings"].items():
        used = [a["id"] for a in m["arms"] if rid in a["readings"]]
        print(f"  {rid} [{', '.join(used) or 'manifest-wide'}] {t}")
    print("JUDGMENT: recorded for 3.0.0_SA_CVO at L9 -- no verdict given")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("criterion", choices=["AC1", "AC2", "AC3", "AC4"])
    ap.add_argument("--manifest", default=str(MANIFEST))
    ap.add_argument("--script", default=str(SCRIPT))
    a = ap.parse_args()
    mp = Path(a.manifest)
    print(f"PROBE: tx_v_1.py {a.criterion}  manifest {mp}")
    if not mp.exists():
        if a.criterion != "AC4":
            print(f"VERDICT: FAIL-TXV1-{a.criterion} manifest absent")
        return 0
    vintage(mp)
    raw = mp.read_text(encoding="utf-8")
    m = json.loads(raw)
    if a.criterion == "AC1":
        print(ac1(m))
    elif a.criterion == "AC2":
        print(ac2(m, Path(a.script)))
    elif a.criterion == "AC3":
        print(ac3(m, raw))
    else:
        ac4(m)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
