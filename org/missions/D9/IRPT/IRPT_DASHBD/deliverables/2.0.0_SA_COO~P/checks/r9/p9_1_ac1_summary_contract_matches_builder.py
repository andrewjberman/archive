"""DB9-1-AC1 -- CTO batch 197 (a): the per-client summary has its OWN versioned contract, and the contract describes what the
publisher's builder emits.

Grades org/standards/IRPT_DASHBD_CLIENT_SUMMARY_CONTRACT.json:
  - contract_version "0.1.0";
  - a `summary` section with `required` (a list) and `fields` (an object naming every required key);
  - `required` includes client_id, firm, as_of, windows, accounts and unpublished_account_ids;
  - the address it states contains "platinum/reporting/client=" and "summary.json";
  - a `window_status` enum section carrying `values` (a non-empty list), a `four_postulate_record` with the four keys i, ii, iii
    and iv each non-empty, and a non-empty `token_census`.
Then runs the publisher's own build_client_summary on a two-account fixture (one published, one not) and grades: every
contract-required key is present in the built document, and every top-level key the builder emits is declared in the contract's
`fields`. Usage: python <this file> <repo_root>
"""
import json
import sys
from pathlib import Path

CONTRACT = "org/standards/IRPT_DASHBD_CLIENT_SUMMARY_CONTRACT.json"
PUB = "infra/aws/lambda/investor-reporting/reporting-publish"
MUST = {"client_id", "firm", "as_of", "windows", "accounts", "unpublished_account_ids"}


def fail(msg):
    print("FAIL: " + msg)
    print("DB9-1-AC1 FAIL")
    sys.exit(1)


def find(obj, key):
    """The first value under `key` anywhere in the document (the contract's layout is the author's)."""
    if isinstance(obj, dict):
        if key in obj:
            return obj[key]
        for v in obj.values():
            got = find(v, key)
            if got is not None:
                return got
    elif isinstance(obj, list):
        for v in obj:
            got = find(v, key)
            if got is not None:
                return got
    return None


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    p = root / CONTRACT
    if not p.is_file():
        fail("no contract at %s" % CONTRACT)
    c = json.loads(p.read_text(encoding="utf-8"))
    if c.get("contract_version") != "0.1.0":
        fail("contract_version is %r, not 0.1.0" % c.get("contract_version"))
    s = c.get("summary")
    if not isinstance(s, dict) or not isinstance(s.get("required"), list) or not isinstance(s.get("fields"), dict):
        fail("no summary section with a required list and a fields object")
    missing = MUST - set(s["required"])
    if missing:
        fail("summary.required lacks %s" % sorted(missing))
    undeclared = set(s["required"]) - set(s["fields"])
    if undeclared:
        fail("required keys with no fields entry: %s" % sorted(undeclared))
    text = json.dumps(c)
    if "platinum/reporting/client=" not in text or "summary.json" not in text:
        fail("the contract does not state the builder's address (platinum/reporting/client=<id>/summary.json)")
    ws = find(c, "window_status")
    if not isinstance(ws, dict) or not ws.get("values"):
        fail("no window_status enum section with values")
    fp = ws.get("four_postulate_record") or {}
    if not all(str(fp.get(k) or "").strip() for k in ("i", "ii", "iii", "iv")):
        fail("window_status.four_postulate_record lacks a non-empty i, ii, iii or iv")
    if not ws.get("token_census"):
        fail("window_status has no token_census")
    sys.path.insert(0, str(root / PUB))
    sys.path.insert(0, str(root))
    try:
        import publisher as P  # noqa: E402
    except Exception as exc:  # noqa: BLE001
        fail("cannot import the publisher: %s" % exc)
    # The published-shape fixture of reporting-publish/tests/test_client_summary.py (make_series, manifest_for).
    dates = ["2026-09-28", "2026-09-29", "2026-09-30", "2026-10-01"]
    series = {"date": dates, "total_return_daily": [None, 0.001, -0.002, 0.0005], "first_data_date": dates[0],
              "as_of": dates[-1], "method_version": 2, "history_scope": "PARTIAL_HISTORY"}
    manifest = {"account_id": "RAW", "firm": "49financial", "as_of": dates[-1], "first_data_date": dates[0],
                "byte_sizes": {P.SERIES_OBJECT: 100}}
    try:
        doc = P.build_client_summary({"client_id": "cli_fixture", "account_ids": ["acc_one", "acc_two"]},
                                     {"acc_one": {"series": series, "manifest": manifest}},
                                     built_at="2026-10-03T00:00:00Z")
    except Exception as exc:  # noqa: BLE001 -- the fixture is the grader's; a builder that cannot take it is reported
        fail("build_client_summary on the fixture raised %s: %s" % (type(exc).__name__, exc))
    absent = set(s["required"]) - set(doc)
    if absent:
        fail("the builder's document lacks contract-required keys %s" % sorted(absent))
    extra = set(doc) - set(s["fields"])
    if extra:
        fail("the builder emits keys the contract does not declare: %s" % sorted(extra))
    print("OK: contract 0.1.0, %d required keys, window_status %d values with its record and census; the builder's "
          "document carries every required key and no undeclared one" % (len(s["required"]), len(ws["values"])))
    print("DB9-1-AC1 PASS")


if __name__ == "__main__":
    main()
