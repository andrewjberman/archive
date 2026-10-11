"""AMGT_RESAPP round-94 PREP -- D1-S23: a classification name never overrides a registered company name that disagrees with it.

  PYTHONPATH=<repo root> python r94_display_name.py            (no network, no AWS: the chain's two readers are replaced by fixtures)

`names_read.display_names(keys, classifications)` serves, per key, the classifications table's name looked up by the key's BARE Bloomberg ticker
(`SAN FP` -> `SAN`), else the crosswalk's registered name. A bare ticker is not a company: `SAN` is Banco Santander on Madrid and Sanofi on Paris, so the
table's row for `SAN` named Sanofi's key "Banco Santander S.A." (row D1-S23, served on the overlay and the peers subject). The rule: the classification name
is served only when it AGREES with the registered name (the cleaned name tokens, the generic words com, stk, cl, class, cos, holdings, holding, group, del, new, and, corp, co, inc, ltd removed, share at least one token of two or more characters); when they disagree the
registered name is served, source `crosswalk`. A registered name that is only the bare ticker, or no registered name, leaves the chain as it was.

    D1 SAN FP: classification 'Banco Santander S.A.' against registered 'SANOFI' -> the registered name, source `crosswalk`.
    D2 control: a spelling variant of the same company (CELH 'Celsius Hldgs Inc Com New' against 'CELSIUS HOLDINGS INC') keeps the classification name.
    D3 control: no registered name -> the classification name.
    D4 control: ICT 'International Container Terminal Services Inc' against 'INTL CONTAINER TERM SVCS INC' (one shared word) keeps the classification name.
    D5 control: the registered name is only the bare ticker -> the classification name (the rule cannot judge it).
    D6 control: classification and registered names equal -> unchanged, source `classification`.

AMENDMENT 1 (the same cell): the chain above is ONE of three places the table's name is served. The overlay's header name (`scoped_amgt._overlay_name`, which the
page header prints) and a ranked row's name (`scoped_amgt._join_ranked_rows`) read the same table by the same bare ticker, each on its own path; the table measured in
round 94 (live against the merged chain) moved only `peers.subject.display_name` and left the overlay header at 'Banco Santander S.A.'.
    D7 the overlay: a classification name that disagrees with the registered name is not served as the header name: `_overlay_name` serves the registered name,
       `display_name_source` `crosswalk`.
    D8 control: the overlay keeps a spelling variant's classification name (`display_name_source` `etf-classifications`).
    D9 a ranked row: a classification name that disagrees with the registered name is replaced by the registered name (`name_source` `crosswalk`) in
       `_join_ranked_rows`; a spelling variant's row keeps the classification name.
Verdict: R94 DISPLAY NAME: YES|NO (exit 0|1). At the base (2026-10-11) D1, D7 and D9 FAIL and D2-D6, D8 PASS.
"""
import sys

from lib.research.api import names_read, scoped_amgt

CASES = {
    "SAN_FP_Equity": ("SAN FP", "Banco Santander S.A.", "SANOFI"),
    "CELH_US_Equity": ("CELH US", "Celsius Hldgs Inc Com New", "CELSIUS HOLDINGS INC"),
    "NOREG_US_Equity": ("NOREG US", "Norege Corp", None),
    "ICT_PM_Equity": ("ICT PM", "International Container Terminal Services Inc", "INTL CONTAINER TERM SVCS INC"),
    "JUNK_US_Equity": ("JUNK US", "Junkco Holdings Inc", "JUNK"),
    "SAME_US_Equity": ("SAME US", "Same Company Inc", "SAME COMPANY INC"),
}


def say(ok, label, detail=""):
    print("%s %s%s" % ("PASS" if ok else "FAIL", label, ("  [" + detail + "]") if detail else ""))
    return ok


def overlay_and_rows(clean):
    out = []
    saved = (scoped_amgt._crosswalk_names, scoped_amgt._classification_for_ticker, scoped_amgt._join_classification,
             scoped_amgt._join_covered_identity, scoped_amgt._fill_names_from_model_block, scoped_amgt._phase_log)
    registered = {"SAN_FP_Equity": "SANOFI", "CELH_US_Equity": "CELSIUS HOLDINGS INC"}
    table = {"SAN": {"name": "Banco Santander S.A. ADR", "status": "SERVED"}, "CELH": {"name": "Celsius Hldgs Inc Com New", "status": "SERVED"}}
    try:
        scoped_amgt._crosswalk_names = lambda: registered
        scoped_amgt._classification_for_ticker = lambda ticker, security_key=None: dict(table.get(str(ticker).split(" ")[0]) or {})
        san = scoped_amgt._overlay_name({"display_ticker": "SAN FP"}, "SAN_FP_Equity", "SAN FP")
        out.append(say(san.get("display_name") == clean("SANOFI") and san.get("display_name_source") == "crosswalk",
                       "D7 the overlay serves the registered name when the classification name disagrees",
                       "served %r from %s" % (san.get("display_name"), san.get("display_name_source"))))
        celh = scoped_amgt._overlay_name({"display_ticker": "CELH US"}, "CELH_US_Equity", "CELH US")
        out.append(say(celh.get("display_name") == clean("Celsius Hldgs Inc Com New") and celh.get("display_name_source") == "etf-classifications",
                       "D8 control: the overlay keeps a spelling variant's classification name",
                       "served %r from %s" % (celh.get("display_name"), celh.get("display_name_source"))))
        rows = [{"ticker": "SAN FP", "security_key": "SAN_FP_Equity"}, {"ticker": "CELH US", "security_key": "CELH_US_Equity"}]

        def join(served):
            return [dict(r, name=table[r["ticker"].split(" ")[0]]["name"], name_source="etf-classifications", name_state="SERVED",
                         classification={"sector": None}) for r in served]
        scoped_amgt._join_classification = join
        scoped_amgt._join_covered_identity = lambda r: r
        scoped_amgt._fill_names_from_model_block = lambda r: r
        scoped_amgt._phase_log = lambda route, phase, started: started
        got = {r["security_key"]: r for r in scoped_amgt._join_ranked_rows(rows, "test")}
        a, b = got["SAN_FP_Equity"], got["CELH_US_Equity"]
        out.append(say(a.get("name_source") == "crosswalk" and clean("SANOFI").lower() in str(a.get("name")).lower()
                       and b.get("name_source") == "etf-classifications",
                       "D9 a ranked row takes the registered name on disagreement; a variant keeps the classification name",
                       "SAN row %r from %s, CELH row %r from %s" % (a.get("name"), a.get("name_source"), b.get("name"), b.get("name_source"))))
    except Exception as exc:  # noqa: BLE001 -- a fixture that cannot run is a FAIL with its reason, not a crash
        out.append(say(False, "D7-D9 the overlay and ranked-row arms ran", "%s: %s" % (type(exc).__name__, exc)))
    finally:
        (scoped_amgt._crosswalk_names, scoped_amgt._classification_for_ticker, scoped_amgt._join_classification,
         scoped_amgt._join_covered_identity, scoped_amgt._fill_names_from_model_block, scoped_amgt._phase_log) = saved
    return out


def main():
    keys = sorted(CASES)
    registered = {k: v[2] for k, v in CASES.items() if v[2]}
    identities = {k: {"bloomberg": v[0], "display_ticker": v[0]} for k, v in CASES.items()}
    classified = {v[0].split(" ")[0]: {"name": v[1]} for v in CASES.values()}
    saved = (scoped_amgt._crosswalk_names, scoped_amgt.resolve_identity)
    try:
        scoped_amgt._crosswalk_names = lambda: registered
        scoped_amgt.resolve_identity = lambda key: identities.get(key) or {}
        got = names_read.display_names(keys, lambda tickers: classified)
    finally:
        scoped_amgt._crosswalk_names, scoped_amgt.resolve_identity = saved
    clean = scoped_amgt._clean_display_name
    results = []
    name, source = got["SAN_FP_Equity"]
    results.append(say(name == clean("SANOFI") and source == "crosswalk",
                       "D1 a classification name that disagrees with the registered name is not served",
                       "served %r from %s" % (name, source)))
    for key, label in (("CELH_US_Equity", "D2 control: a spelling variant keeps the classification name"),
                       ("NOREG_US_Equity", "D3 control: no registered name keeps the classification name"),
                       ("ICT_PM_Equity", "D4 control: one shared word keeps the classification name"),
                       ("JUNK_US_Equity", "D5 control: a bare-ticker registered name cannot be judged"),
                       ("SAME_US_Equity", "D6 control: equal names are unchanged")):
        name, source = got[key]
        want = clean(CASES[key][1])
        results.append(say(name == want and source == "classification", label, "served %r from %s" % (name, source)))
    results.extend(overlay_and_rows(clean))
    print("   arms passed %d of %d" % (sum(1 for r in results if r), len(results)))
    ok = all(results)
    print("R94 DISPLAY NAME: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
