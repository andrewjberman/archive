"""RIV-al-1 AC1 (ROUND_ANALYSIS.round10.md ADDENDUM 5 @a8fb9c1df1): every call site in `data/etfs/scripts/rivalfunds/` (tests
excluded) that calls an identity-key function able to take pk-1's parsekey passes it -- census with a printed denominator.

The functions are found, not listed: every module-level function in the package whose parameters include `pk` or `parsekeys`
(measured at the cut: `_books`, `_cross_sectors`, `identity_maps`, `row_keys` in gold_holding_contribution; `bbg_by_xid`,
`held_funds`, `infer_windows`, `infer_pairs`, `infer_trades`, `infer_recon` in gold_trade_schedule). A call passes the
parsekey when it supplies that parameter positionally or by keyword. A call inside the body of another pk-taking function
that forwards its own parameter counts as passing.
Measured at base (CLOUD 325e20b091): 23 call sites of 13 identity functions; 6 omit it -- gold_buying_trend.py:79, :192
(identity_maps), gold_input_census.py:139 (identity_maps), :140 (_cross_sectors), :146 (_books), sweep.py:306 (held_funds).
  - (a) 0 call sites omit the parsekey;
  - (b) control: the census finds at least 20 call sites and at least 8 pk-taking functions (the instrument still sees them).
FAIL at base: (a) FAILS (6); (b) PASSES."""
import ast
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

PKG = c.ROOT / "data" / "etfs" / "scripts" / "rivalfunds"
PK_NAMES = ("pk", "parsekeys")


def run(v):
    files = [p for p in sorted(PKG.rglob("*.py")) if "tests" not in p.parts]
    trees = {p: ast.parse(p.read_text(encoding="utf-8")) for p in files}
    funcs = {}
    for p, t in trees.items():
        for n in t.body:
            if isinstance(n, ast.FunctionDef):
                params = [a.arg for a in n.args.posonlyargs + n.args.args]
                kw = [a.arg for a in n.args.kwonlyargs]
                for name in PK_NAMES:
                    if name in params or name in kw:
                        funcs[n.name] = (params.index(name) if name in params else None, name)
    sites, missing = [], []
    for p, t in trees.items():
        for n in ast.walk(t):
            if not isinstance(n, ast.Call):
                continue
            f = n.func
            nm = f.attr if isinstance(f, ast.Attribute) else getattr(f, "id", None)
            if nm not in funcs:
                continue
            pos, pname = funcs[nm]
            ok = any(k.arg == pname for k in n.keywords) or (pos is not None and len(n.args) > pos) \
                or any(k.arg is None for k in n.keywords)
            site = f"{p.name}:{n.lineno} {nm}"
            sites.append(site)
            if not ok:
                missing.append(site)
    print(f"pk-taking functions: {len(funcs)} {sorted(funcs)}")
    print(f"call sites: {len(sites)} | omit the parsekey: {len(missing)}")
    for m in missing:
        print("  OMITS:", m)
    v.check(not missing, f"(a) every identity call site passes the parsekey ({len(sites) - len(missing)} of {len(sites)})")
    v.check(len(sites) >= 20 and len(funcs) >= 8, f"(b) control: the census sees {len(sites)} sites of {len(funcs)} functions")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
