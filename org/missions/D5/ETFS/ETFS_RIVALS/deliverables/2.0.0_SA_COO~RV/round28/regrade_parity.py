"""Run the page's recheck (guardrails.analysis_grounding's grounding_check call) over a served accounts object under the
_figures of two pins. Usage: python regrade_parity.py <parquet> <ai_accounts_pinA.py> <ai_accounts_pinB.py> <repo>
Each pin's ai_accounts.py is loaded as rivalfunds.ai_accounts from the repo's package dir (its other imports at HEAD;
grounding_check is byte-identical across the pins, only _figures differs)."""
import importlib.util
import json
import sys
import pyarrow.parquet as pq

parquet, pa_path, pb_path, repo = sys.argv[1:5]
sys.path.insert(0, repo)
sys.path.insert(0, repo + "/data/etfs/scripts")


def load(path, tag):
    spec = importlib.util.spec_from_file_location("rivalfunds.ai_accounts_" + tag, path,
                                                  submodule_search_locations=None)
    mod = importlib.util.module_from_spec(spec)
    mod.__package__ = "rivalfunds"
    spec.loader.exec_module(mod)
    return mod


A, B = load(pa_path, "A"), load(pb_path, "B")
rows = pq.read_table(parquet).to_pylist()


def _l(v):
    try:
        x = json.loads(v) if isinstance(v, str) else v
    except ValueError:
        return []
    return x if isinstance(x, list) else []


def _vint_names(v):
    try:
        d = json.loads(v) if isinstance(v, str) else v
    except ValueError:
        return set()
    return {str(k).split("/", 1)[1] for k in d if "/" in str(k)} if isinstance(d, dict) else set()


diff = phrase = figdiff = 0
stored = {}
for r in rows:
    text = " ".join([str(r.get("text") or "")] + [str(x) for x in _l(r.get("observed")) + _l(r.get("inferred"))])
    if A._PERIOD_NAME_RE.search(text) if hasattr(A, "_PERIOD_NAME_RE") else B._PERIOD_NAME_RE.search(text):
        phrase += 1
    if A._figures(text) != B._figures(text):
        figdiff += 1
    ga = A.grounding_check(text, _l(r.get("cited_rows")), known_keys=None, names=_vint_names(r.get("input_vintages")))
    gb = B.grounding_check(text, _l(r.get("cited_rows")), known_keys=None, names=_vint_names(r.get("input_vintages")))
    stored[str(r.get("grounding"))] = stored.get(str(r.get("grounding")), 0) + 1
    if ga[0] != gb[0]:
        diff += 1
        print("DIFF", r.get("fund_id"), r.get("kind"), ga, gb)
print("rows: %d (stored grounding %s; prompt_version %s)" % (len(rows), stored,
      sorted({str(r.get("prompt_version")) for r in rows})))
print("rows whose text holds a period phrase: %d" % phrase)
print("rows whose figure list differs between the pins: %d" % figdiff)
print("rows whose recheck verdict differs between the pins: %d of %d" % (diff, len(rows)))
