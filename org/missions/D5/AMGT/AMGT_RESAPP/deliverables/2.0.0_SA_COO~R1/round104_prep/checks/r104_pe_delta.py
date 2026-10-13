"""AMGT_RESAPP round-104 PREP -- `AMGT-bk-2`: the live /thesis payloads captured BEFORE and AFTER the apply differ in the PE_RATIO rows and nowhere else.

  PYTHONPATH=. python r104_pe_delta.py <pre.json> <post.json>          (the files `aw4_capture.py` writes: {"function": ..., "keys": {<security_key>: <payload>}})

Per name, over the figures lists (`fiscal_year_figures` and `model.fiscal_year_figures`), `model.fiscal_unresolved` and every other captured field:
    D1 every non-PE_RATIO figure row, every other top field and every other `model` key (team_sheet included) is equal pre to post (a vintage stamp that moved with a daily pull is printed, never hidden);
    D2 every post PE_RATIO row is round(PX_LAST / IS_EPS, 4) of its own list's same-year rows, a minor unit of the same currency scaled by `case_rule.MINOR_UNIT_FACTOR`, never a different currency;
    D3 every pre PE_RATIO year is, post, served OR withheld with a `fiscal_unresolved` entry naming the reason (served + withheld = pre);
    D4 `fiscal_unresolved` post = pre plus PE_RATIO entries only.
Prints per-name `pe <key> served <s> withheld <w> DIFF[...]` only for a name with a difference outside the PE rows, then
`pe totals names <n> served <s> withheld <w>` and `R104 PE DELTA: YES|NO`; exit 0|1.
"""
import json
import sys

sys.path.insert(0, ".")
from lib.research.api import case_rule  # noqa: E402

OTHER_TOP = ("fiscal_years", "header_figures", "check_face", "model_status", "posture", "dossier_fields")


def canon(v):
    return json.dumps(v, sort_keys=True, ensure_ascii=True)


def expected(figs, year):
    inputs = {f["mnemonic"]: (f.get("value"), f.get("currency")) for f in figs if f.get("fiscal_year") == year and f.get("mnemonic") in ("PX_LAST", "IS_EPS")}
    try:
        (px, pc), (eps, ec) = inputs["PX_LAST"], inputs["IS_EPS"]
    except KeyError:
        return None
    if not (isinstance(px, (int, float)) and isinstance(eps, (int, float)) and px > 0 and eps > 0 and pc and ec):
        return None
    if pc != ec:
        if not case_rule.is_minor_unit_quote(pc, ec):
            return None
        px, eps = (px / case_rule.MINOR_UNIT_FACTOR, eps) if pc[2:].islower() else (px, eps / case_rule.MINOR_UNIT_FACTOR)
    return round(px / eps, 4)


def non_pe(figs):
    return [f for f in figs if f.get("mnemonic") != "PE_RATIO"]


def pe_years(figs):
    return {f.get("fiscal_year"): f for f in figs if f.get("mnemonic") == "PE_RATIO"}


def main(argv):
    pre = json.load(open(argv[0], encoding="utf-8"))
    post = json.load(open(argv[1], encoding="utf-8"))
    names = sorted(post["keys"])
    ok_all, served, withheld = True, 0, 0
    for key in names:
        a, b = pre["keys"].get(key), post["keys"][key]
        if a is None:
            print("NO-PRE %s" % key)
            ok_all = False
            continue
        diffs = []
        for k in OTHER_TOP:
            if canon(a.get(k)) != canon(b.get(k)):
                diffs.append(k)
        ma, mb = a.get("model") or {}, b.get("model") or {}
        for k in sorted(set(ma) | set(mb)):
            if k in ("fiscal_year_figures", "fiscal_unresolved"):
                continue
            if canon(ma.get(k)) != canon(mb.get(k)):
                diffs.append("model." + k)
        for name, fa, fb in (("fiscal_year_figures", a.get("fiscal_year_figures") or [], b.get("fiscal_year_figures") or []),
                             ("model.fiscal_year_figures", ma.get("fiscal_year_figures") or [], mb.get("fiscal_year_figures") or [])):
            if canon(non_pe(fa)) != canon(non_pe(fb)):
                diffs.append(name + " (non-PE rows)")
            pa, pb = pe_years(fa), pe_years(fb)
            for y, row in pb.items():
                if y not in pa or row.get("value") != expected(fb, y):
                    diffs.append("%s PE %s not the derivation" % (name, y))
        ua = [u for u in ma.get("fiscal_unresolved") or []]
        ub = [u for u in mb.get("fiscal_unresolved") or []]
        extra = [u for u in ub if u not in ua]
        if any(u.get("mnemonic") != "PE_RATIO" for u in extra) or any(u not in ub for u in ua):
            diffs.append("model.fiscal_unresolved (non-PE change)")
        pa, pb = pe_years(ma.get("fiscal_year_figures") or []), pe_years(mb.get("fiscal_year_figures") or [])
        reasoned = {u.get("fiscal_year") for u in extra if u.get("reason")}
        for y in pa:
            if y not in pb and y not in reasoned:
                diffs.append("PE %s neither served nor withheld with a reason" % y)
        served += len(pb)
        withheld += len([y for y in pa if y not in pb])
        if diffs:
            ok_all = False
            print("pe %s DIFF[%s]" % (key, "; ".join(diffs[:6])))
    print("pe totals names %d served %d withheld %d" % (len(names), served, withheld))
    print("R104 PE DELTA: %s" % ("YES" if ok_all and names else "NO"))
    return 0 if ok_all and names else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
