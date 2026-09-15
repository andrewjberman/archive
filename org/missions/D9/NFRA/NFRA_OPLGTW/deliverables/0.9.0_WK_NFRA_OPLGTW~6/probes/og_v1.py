"""OG-v-1 probe: python og_v1.py AC<n> [--acceptance-dir <dir>]

Prints its measurement with its denominator, then exactly one line
`VERDICT: PASS-OGV1-AC<n>` or `VERDICT: FAIL-OGV1-AC<n> <reason>`. rc 0 on PASS, 1 on FAIL,
2 on usage error. --acceptance-dir points the probe at a copy (used by the mutant controls).
"""
from __future__ import annotations

import ast
import hashlib
import importlib.util
import json
import re
import sys
import tempfile
from decimal import Decimal
from pathlib import Path

import pyarrow.parquet as pq

PROBE = Path(__file__).resolve()
ROOT = PROBE.parents[8]
DEFAULT_ACC = ROOT / "infra" / "aws" / "ec2" / "opal-gateway" / "tests" / "acceptance"
CONTRACT = ROOT / "org" / "standards" / "NFRA_OPLGTW_CONTRACT.json"
SILVER = ROOT / "data" / "assets" / "scripts" / "silver"
FORBIDDEN_PATH = "integrations" + "/" + "schwab"
FORBIDDEN_MOD = "integrations" + "." + "schwab"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


class Ctx:
    def __init__(self, acc: Path):
        self.acc = acc
        self.mf = load_module("make_fixtures", acc / "make_fixtures.py")
        self.contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
        self._fx = None

    def fixtures(self) -> Path:
        """The fixture tree whose Parquet bytes equal MANIFEST's sha256 -- the worktree's, or a
        regeneration by the generator when the worktree lacks a file."""
        if self._fx:
            return self._fx
        fx = self.acc / "fixtures"
        man = json.loads((fx / "MANIFEST.json").read_text(encoding="utf-8"))
        missing = [o for o in man["objects"] if not (fx / o["path"]).is_file()]
        source = "worktree"
        if missing:
            tmp = Path(tempfile.mkdtemp(prefix="ogv1-regen-"))
            self.mf.build(tmp)
            fx, source = tmp, "regenerated (" + str(len(missing)) + " absent in worktree)"
        bad = [o["path"] for o in man["objects"]
               if hashlib.sha256((fx / o["path"]).read_bytes()).hexdigest() != o["sha256"]]
        print("FIXTURES: " + source + "; " + str(len(man["objects"]) - len(bad)) + " of "
              + str(len(man["objects"])) + " parquet sha256 match MANIFEST.json")
        if bad:
            raise SystemExit(fail_msg("fixture bytes differ from MANIFEST: " + ", ".join(bad[:3])))
        self._fx, self.man = fx, man
        return fx

    def rows(self, rel: str) -> list:
        return pq.read_table(self.fixtures() / rel).to_pylist()

    def objects(self, table=None, order=1):
        self.fixtures()
        return [o for o in self.man["objects"] if o["upload_order"] == order
                and (table is None or "/silver/" + table + "/" in o["key"])]


AC = [None]


def fail_msg(reason: str) -> str:
    return "VERDICT: FAIL-OGV1-" + AC[0] + " " + reason


def verdict(ok: bool, reason: str = "") -> int:
    if ok:
        print("VERDICT: PASS-OGV1-" + AC[0])
        return 0
    print(fail_msg(reason))
    return 1


def complete_slots(c: Ctx) -> list:
    return [(m["master"], m["date"]) for m in c.man["markers"] if m["variant"] == "complete"]


# ---------------------------------------------------------------------------------------------
def ac1(c: Ctx) -> int:
    doc = json.loads((c.acc / "A_ROWS.json").read_text(encoding="utf-8"))
    want = c.contract["acceptance_ids"]
    ids = [r.get("id") for r in doc.get("rows", [])]
    exp_path = c.acc / "expected" / "EXPECTED.json"
    cases = json.loads(exp_path.read_text(encoding="utf-8"))["cases"] if exp_path.is_file() else {}
    problems, halves = [], {"machine": 0, "person": 0}
    both = 0
    for r in doc.get("rows", []):
        hs = r.get("halves") or []
        if not hs:
            problems.append(r.get("id") + ": no half")
        ops = []
        for h in hs:
            op = h.get("operated_by")
            if op not in halves:
                problems.append(r["id"] + ": operated_by " + repr(op))
                continue
            halves[op] += 1
            ops.append(op)
            if len(str(h.get("expected_result", "")).strip()) < 20:
                problems.append(r["id"] + "/" + op + ": expected_result empty")
            if len(str(h.get("instrument", "")).strip()) < 10:
                problems.append(r["id"] + "/" + op + ": instrument empty")
            if not h.get("graded_by"):
                problems.append(r["id"] + "/" + op + ": graded_by empty")
            for ref in h.get("expected_refs") or []:
                if ref not in cases:
                    problems.append(r["id"] + ": expected_ref " + ref + " not in EXPECTED.json")
        if sorted(set(ops)) != sorted(r.get("operated_by") or []):
            problems.append(r["id"] + ": operated_by list disagrees with its halves")
        both += len(set(ops)) == 2
        if r.get("status") != "NOT_EXERCISED":
            problems.append(r["id"] + ": status " + repr(r.get("status")))
    dup = sorted({i for i in ids if ids.count(i) > 1})
    print("CENSUS: " + str(len(set(ids) & set(want))) + " of " + str(len(want))
          + " contract acceptance_ids present; rows " + str(len(ids)) + "; extra "
          + str(sorted(set(ids) - set(want))) + "; missing " + str(sorted(set(want) - set(ids)))
          + "; duplicates " + str(dup))
    print("HALVES: machine " + str(halves["machine"]) + ", person " + str(halves["person"])
          + "; rows with both " + str(both) + "; problems " + str(len(problems)))
    for p in problems[:10]:
        print("  PROBLEM: " + p)
    ok = sorted(ids, key=lambda x: int(x[1:])) == want and not dup and not problems
    return verdict(ok, "census or row content defective: " + str(problems[:3] or dup
                                                                 or sorted(set(want) ^ set(ids))))


def ac2(c: Ctx) -> int:
    per_master = {}
    for o in c.objects("dim_position") + c.objects("dim_balance"):
        master = o["key"].split("/")[1]
        date = o["key"].split("date=")[1][:10]
        for r in c.rows(o["path"]):
            per_master.setdefault(master, {}).setdefault(r["account_id"], set()).add(date)
    masters = sorted(per_master)
    shared = set.intersection(*(set(v) for v in per_master.values())) if len(masters) == 2 else set()
    numeric = sorted(a for a in shared if a.isdigit())
    same_day = sorted(a for a in numeric
                      if set.intersection(*(per_master[m][a] for m in masters)))
    for m in masters:
        print("MASTER " + m + ": " + str(len(per_master[m])) + " distinct account IDs")
    print("SHARED: " + str(len(numeric)) + " numeric account ID(s) in both of " + str(len(masters))
          + " masters " + str(numeric) + "; present in both on a common date: " + str(same_day))
    return verdict(len(masters) == 2 and bool(same_day), "no numeric account ID shared by the two masters")


def _dec_cols(table_cols):
    return [(n, s) for n, s in table_cols if isinstance(s, tuple)]


def ac3(c: Ctx) -> int:
    mf = c.mf
    overlap_cash = overlap_mv = 0
    nulls, neg, pos, zero, max_edge, step_edge = {}, 0, 0, 0, set(), set()
    cells = 0
    for table in ("dim_position", "dim_balance"):
        cols = _dec_cols(mf.DIM_COLS[table])
        served = set(c.contract["fields"][table])
        for o in c.objects(table):
            for r in c.rows(o["path"]):
                for n, (_, p, s) in cols:
                    v = r[n]
                    if n in served:
                        cells += 1
                        if v is None:
                            nulls[table] = nulls.get(table, 0) + 1
                    if v is None:
                        continue
                    neg += v < 0
                    pos += v > 0
                    zero += v == 0
                    if abs(v) == Decimal(10) ** (p - s) - Decimal(1).scaleb(-s):
                        max_edge.add(table + "." + n)
                    if abs(v) == Decimal(1).scaleb(-s):
                        step_edge.add(table + "." + n)
                if table == "dim_balance":
                    a, b, t = r["net_mv_positions"], r["cash_balance_settled_only"], r["net_mv_plus_cash"]
                    if None not in (a, b, t) and a + b == t:
                        overlap_cash += 1
                    lo, sh = r["mkt_value_long"], r["mkt_value_short"]
                    if None not in (lo, sh, a) and lo + sh == a:
                        overlap_mv += 1
    dups = []
    for table, grain in (("dim_position", ("account_id", "cusip", "l_s")),
                         ("dim_balance", ("account_id",)), ("dim_asset", ("cusip",))):
        for o in c.objects(table):
            keys = [tuple(r[g] for g in grain) for r in c.rows(o["path"])]
            if len(keys) != len(set(keys)):
                dups.append(o["key"])
    print("DENOMINATOR: " + str(cells) + " served decimal cells across "
          + str(len(c.objects("dim_position")) + len(c.objects("dim_balance")))
          + " position/balance objects")
    print("OVERLAP: net_mv_plus_cash == net_mv_positions + cash_balance_settled_only in "
          + str(overlap_cash) + " rows; net_mv_positions == long + short in " + str(overlap_mv))
    print("NULLS: " + json.dumps(nulls, sort_keys=True) + "; SIGNS: negative " + str(neg)
          + ", positive " + str(pos) + ", zero " + str(zero))
    print("DECIMAL EDGES: at type maximum " + str(sorted(max_edge)) + "; at one scale step "
          + str(sorted(step_edge)))
    print("DUPLICATE GRAIN: " + str(len(dups)) + " object(s) " + str(dups))
    ok = (overlap_cash and overlap_mv and nulls.get("dim_position") and nulls.get("dim_balance")
          and neg and pos and zero and max_edge and step_edge and dups)
    return verdict(bool(ok), "a required property is absent (see counts above)")


PROMPT_RE = re.compile(r"(?i)(ignore (all )?previous instructions|^system:|call schwab_\w+|grant master)")
FORMULA_RE = re.compile(r"^[\s\x00-\x1f]*[=+\-@]")


def ac4(c: Ctx) -> int:
    text_cells, prompt, formula, lead = 0, [], [], []
    for table in ("dim_asset", "dim_position", "dim_balance"):
        strcols = [n for n, s in c.mf.DIM_COLS[table] if s == "s"]
        for o in c.objects(table):
            for r in c.rows(o["path"]):
                for n in strcols:
                    v = r[n]
                    if v is None:
                        continue
                    text_cells += 1
                    if table == "dim_asset" and n.startswith("security_description") and PROMPT_RE.search(v):
                        prompt.append(n)
                    if FORMULA_RE.match(v):
                        formula.append(v)
                        if v[:1] in (" ", "\t", "\r", "\n"):
                            lead.append(v)
    print("DENOMINATOR: " + str(text_cells) + " non-null text cells scanned")
    print("PROMPT-LIKE: " + str(len(prompt)) + " security-description cells ("
          + str(sorted(set(prompt))) + ")")
    print("FORMULA-LIKE: " + str(len(formula)) + " text cells, " + str(len(set(formula)))
          + " distinct; with leading whitespace/control " + str(len(set(lead))))
    return verdict(bool(prompt and formula and lead), "prompt-like or formula-like text absent")


def ac5(c: Ctx) -> int:
    fx = c.fixtures()
    later_keys = {o["key"] for o in c.man["objects"] if o["upload_order"] == 2}
    closures = []
    for m in c.man["markers"]:
        if m["path"]:
            mk = json.loads((fx / m["path"]).read_text(encoding="utf-8"))
            closures.append((m, mk.get("closure")))
    kinds = {k: [] for k in ("missing", "partial", "failed", "stale", "unversioned")}
    qualified = {}
    for m, cl in closures:
        if not cl:
            continue
        tabs = cl["tables"]
        exp_types = {p["type"] for p in cl["source_partitions"] if p["disposition"] == "EXPECTED"}
        if any(t["disposition"] == "MISSING" for t in tabs.values()):
            kinds["missing"].append(m["date"])
        if exp_types and any(req not in exp_types for req in cl["required_types"]):
            kinds["partial"].append(m["date"])
        if cl["outputs"]["failed"] or any(t["disposition"] == "FAILED" for t in tabs.values()):
            kinds["failed"].append(m["date"])
        if any((t.get("object") or {}).get("version_id") in ("null", "") or t["disposition"] == "UNVERSIONED"
               for t in tabs.values()):
            kinds["unversioned"].append(m["date"])
        if cl["status"] == "qualified" and not any(t["disposition"] != "PRESENT" for t in tabs.values()):
            qualified.setdefault(m["master"], []).append(m["date"])
            if any(o["key"] in later_keys for o in cl["objects"]):
                kinds["stale"].append(m["date"] + " (later version at a pinned key)")
    import datetime as dt
    for master, dates in qualified.items():
        floor = dt.date.fromisoformat(max(dates)) - dt.timedelta(days=29)
        kinds["stale"] += [d + " (outside the 30-day window)" for d in dates
                           if dt.date.fromisoformat(d) < floor]
    print("DENOMINATOR: " + str(len(closures)) + " marker files, "
          + str(sum(1 for _, cl in closures if cl)) + " carrying a closure")
    for k, v in kinds.items():
        print("VARIANT " + k + ": " + str(len(v)) + " " + str(v))
    print("COMPLETE: qualified clean closures per master " + json.dumps(
        {k: len(v) for k, v in sorted(qualified.items())}))
    # CONTROL: the published validator (OG-c-1) agrees with every closure's built intent.
    sys.path.insert(0, str(SILVER))
    try:
        import conversion_manifest as cm
    except Exception as exc:  # noqa: BLE001
        print("VALIDATOR: import failed " + type(exc).__name__)
        return verdict(False, "published validator could not be imported")
    agree = 0
    disagree = []
    for m, cl in closures:
        if not cl:
            continue
        v = cm.validate_closure(cl)
        intent = c.man["variants"][m["variant"]]
        found = {f["class"] for f in v["findings"]}
        if v["status"] == intent["built_status"] and set(intent["built_finding_classes"]) <= found:
            agree += 1
        else:
            disagree.append(m["variant"] + " " + v["status"] + " " + str(sorted(found)))
    n = sum(1 for _, cl in closures if cl)
    print("VALIDATOR (conversion_manifest.validate_closure): agrees with built intent on "
          + str(agree) + " of " + str(n) + " closures; disagreements " + str(disagree))
    ok = all(kinds.values()) and len(qualified) == 2 and agree == n
    return verdict(ok, "a variant is absent or the published validator disagrees")


def ac6(c: Ctx) -> int:
    files = [c.acc / "make_fixtures.py", c.acc / "expect_independent.py", PROBE]
    bad, imports = [], 0
    for f in files:
        tree = ast.parse(f.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            mods = []
            if isinstance(node, ast.Import):
                mods = [a.name for a in node.names]
            elif isinstance(node, ast.ImportFrom):
                mods = [node.module or ""] + [(node.module or "") + "." + a.name for a in node.names]
            elif isinstance(node, ast.Call):
                fn = getattr(node.func, "attr", getattr(node.func, "id", ""))
                if fn in ("__import__", "import_module") and node.args and isinstance(node.args[0], ast.Constant):
                    mods = [str(node.args[0].value)]
                # a path handed to any call (sys.path.insert, Path, spec_from_file_location, open)
                for arg in list(node.args) + [k.value for k in node.keywords]:
                    if (isinstance(arg, ast.Constant) and isinstance(arg.value, str)
                            and FORBIDDEN_PATH in arg.value.replace("\\", "/")):
                        bad.append(f.name + ": path argument " + arg.value[:60])
            elif isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div):
                parts = [n.value for n in ast.walk(node)
                         if isinstance(n, ast.Constant) and isinstance(n.value, str)]
                if "integrations" in parts and "schwab" in parts:
                    bad.append(f.name + ": path join to " + FORBIDDEN_PATH)
            imports += isinstance(node, (ast.Import, ast.ImportFrom))
            for mname in mods:
                if FORBIDDEN_MOD in mname or mname == "app" or mname.startswith("app.") or mname.split(".")[0] == "duckdb":
                    bad.append(f.name + ": import " + mname)
    ei = load_module("expect_independent", c.acc / "expect_independent.py")
    committed = json.loads((c.acc / "expected" / "EXPECTED.json").read_text(encoding="utf-8"))
    rebuilt = json.loads(json.dumps(ei.build(c.fixtures())))
    named = committed.get("instrument") == ei.INSTRUMENT and "decimal" in ei.INSTRUMENT and "pyarrow" in ei.INSTRUMENT
    print("DENOMINATOR: " + str(len(files)) + " python files written by this cell parsed; "
          + str(imports) + " import statements; forbidden " + str(len(bad)) + " " + str(bad))
    print("INSTRUMENT: " + str(committed.get("instrument")))
    print("REPRODUCED: expect_independent.build() over the fixtures equals expected/EXPECTED.json: "
          + str(rebuilt == committed) + " (" + str(len(committed.get("cases", {}))) + " cases)")
    return verdict(not bad and named and rebuilt == committed,
                   "forbidden import, unnamed instrument, or EXPECTED.json not reproduced")


def _sections(text: str) -> dict:
    out, cur = {}, None
    for line in text.splitlines():
        m = re.match(r"^### (A\d+) -- ", line)
        if m:
            cur = m.group(1)
            out[cur] = []
        elif line.startswith("## ") or line.startswith("### "):
            cur = None
        elif cur:
            out[cur].append(line)
    return out


def ac7(c: Ctx) -> int:
    doc = json.loads((c.acc / "A_ROWS.json").read_text(encoding="utf-8"))
    person = [r["id"] for r in doc["rows"] if any(h["operated_by"] == "person" for h in r["halves"])]
    secs = _sections((c.acc / "WALKTHROUGH_PROTOCOL.md").read_text(encoding="utf-8"))
    need = ("tool", "utc time", "public connector url", "server correlation", "ofid_")
    ok_rows, problems = [], []
    for rid in person:
        lines = secs.get(rid)
        if lines is None:
            problems.append(rid + ": no section")
            continue
        body = "\n".join(lines)
        steps = re.search(r"\*\*Steps:\*\*\s*\n((?:\d+\. .+\n?)+)", body)
        obs = re.search(r"\*\*Expected observation:\*\*\s*(\S.+)", body)
        ev = re.search(r"\*\*Evidence to record:\*\*\s*(\S.+)", body)
        miss = [t for t in need if not ev or t not in ev.group(1).lower()]
        if not steps or not obs or miss:
            problems.append(rid + ": steps " + str(bool(steps)) + ", observation " + str(bool(obs))
                            + ", evidence missing " + str(miss))
        else:
            ok_rows.append(rid)
    print("PERSON-OPERATED ROWS (A_ROWS.json): " + str(len(person)) + " " + str(person))
    print("PROTOCOL: " + str(len(ok_rows)) + " of " + str(len(person))
          + " carry steps, expected observation and the five evidence items; problems " + str(problems))
    return verdict(bool(person) and len(ok_rows) == len(person), "; ".join(problems[:3]))


def ac8(c: Ctx) -> int:
    text = (c.acc / "WALKTHROUGH_PROTOCOL.md").read_text(encoding="utf-8")
    rows = []
    for line in text.splitlines():
        if re.match(r"^\| RQ\d+ \|", line):
            cells = [x.strip() for x in line.strip().strip("|").split("|")]
            rows.append({"id": cells[0], "kind": cells[1], "masters": re.findall(r"\d{8}", cells[2]),
                         "dates": cells[3], "dataset": cells[4], "question": cells[5]})
    masters = list(c.contract["masters"])
    per_master = {m: [r["id"] for r in rows if r["kind"] == "per_master" and r["masters"] == [m]] for m in masters}
    between_m = [r["id"] for r in rows if r["kind"] == "between_masters" and sorted(r["masters"]) == sorted(masters)]
    between_d = [r["id"] for r in rows if r["kind"] == "between_dates" and len(r["masters"]) == 1]
    odd = [r["id"] for r in rows if r["kind"] not in ("per_master", "between_masters", "between_dates")
           or r["dataset"] not in c.contract["datasets"] or len(r["question"]) < 20]
    print("DENOMINATOR: " + str(len(rows)) + " real-data questions listed")
    print("PER MASTER: " + json.dumps(per_master) + "; BETWEEN MASTERS: " + str(between_m)
          + "; BETWEEN DATES: " + str(between_d) + "; malformed " + str(odd))
    ok = all(per_master.values()) and between_m and between_d and not odd
    return verdict(bool(ok), "a required question kind is absent or a row is malformed")


def ac9(c: Ctx) -> int:
    import datetime as dt
    u = c.mf.seed_universe()
    fx = c.fixtures()
    foreign, cells, files = [], 0, 0
    for o in c.man["objects"]:
        files += 1
        for r in c.rows(o["path"]):
            for k, v in r.items():
                if v is None:
                    continue
                cells += 1
                if k == "account_id" and v not in u["accounts"]:
                    foreign.append(o["key"] + " account_id " + str(v))
                elif isinstance(v, str) and v not in u["strings"]:
                    foreign.append(o["key"] + " " + k + " " + v[:30])
                elif isinstance(v, Decimal) and v not in u["decimals"]:
                    foreign.append(o["key"] + " " + k + " " + str(v))
                elif isinstance(v, dt.date) and v.isoformat() not in u["dates"]:
                    foreign.append(o["key"] + " " + k + " " + v.isoformat())
                elif isinstance(v, int) and not (0 <= v < u["max_fixture_row"]):
                    foreign.append(o["key"] + " " + k + " " + str(v))
    allowed_runs = u["accounts"] | u["masters"] | {d.replace("-", "") for d in u["dates"]}
    json_strings = 0

    def walk(x, key=None):
        nonlocal json_strings
        if isinstance(x, dict):
            for k2, v2 in x.items():
                walk(k2)
                walk(v2, k2)
        elif isinstance(x, list):
            for v2 in x:
                walk(v2, key)
        elif isinstance(x, str) and key not in ("sha256", "etag", "closure_id"):
            json_strings += 1
            for run in re.findall(r"(?<![0-9])[0-9]{8,}(?![0-9])", x):
                if run not in allowed_runs:
                    foreign.append("json " + str(key) + " " + run)
    jfiles = [fx / "MANIFEST.json"] + [fx / m["path"] for m in c.man["markers"] if m["path"]]
    for jf in jfiles:
        files += 1
        walk(json.loads(jf.read_text(encoding="utf-8")))
    print("DENOMINATOR: " + str(files) + " fixture files (" + str(len(c.man["objects"]))
          + " parquet, " + str(len(jfiles)) + " json); " + str(cells) + " non-null parquet cells; "
          + str(json_strings) + " json strings")
    print("SEEDS: " + str(len(u["accounts"])) + " account IDs, " + str(len(u["strings"]))
          + " strings, " + str(len(u["decimals"])) + " decimals, " + str(len(u["dates"])) + " dates")
    print("FOREIGN (not from the generator's seeds): " + str(len(foreign)) + " " + str(foreign[:5]))
    return verdict(not foreign, str(len(foreign)) + " value(s) not from the seeds")


def main(argv) -> int:
    args = list(argv)
    acc = DEFAULT_ACC
    if "--acceptance-dir" in args:
        i = args.index("--acceptance-dir")
        acc = Path(args[i + 1]).resolve()
        del args[i:i + 2]
    if len(args) != 1 or not re.fullmatch(r"AC[1-9]", args[0]):
        print("usage: og_v1.py AC<1-9> [--acceptance-dir <dir>]")
        return 2
    AC[0] = args[0]
    print("PROBE: og_v1 " + AC[0] + " over " + str(acc))
    c = Ctx(acc)
    return {"AC1": ac1, "AC2": ac2, "AC3": ac3, "AC4": ac4, "AC5": ac5, "AC6": ac6,
            "AC7": ac7, "AC8": ac8, "AC9": ac9}[AC[0]](c)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
