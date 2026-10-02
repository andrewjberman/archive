"""Build task 1: the transaction-code classification table + materiality measurement.
Classification per the GIPS standard's sec4 taxonomy: EXTERNAL / INTERNAL / FEE /
CONDITIONAL-BY-COUNTERPARTY (boundary-relative, resolution rule attached) / UNRESOLVED.
Money column = gross_amount (measured: universal); in-kind rows valued qty*price separately.

Two modes:
  python build_schwab_txn_classification.py
      the original build over the raw TRN census (the 2026-08-11 scratchpad; that data is no longer on disk)
  python build_schwab_txn_classification.py --reapply <table.json>
      re-run THIS rule set over a recorded table's code rows, rewriting only `rule` and `partition` and printing
      every row that moved. The census columns (rows, sums, dates) are untouched: classification reads only the
      code identity (tran_srcde, tr_cd, sb_cd) and the recorded description, exactly as the build's classify() did.

2026-10-02 (IRPT_DASHBD round 3; CTO round analysis ADDENDUM 1 A4 @7a888d7675; ask 2.0.0_SA_COO~P msg 104137):
"foreign-tax" moved ahead of "wd-generic". First match wins, and wd-generic (sb_cd WD/WI) caught FTP/FC/WD and
FTR/FC/WD before foreign-tax could, so foreign tax paid and reclaimed read EXTERNAL. They are INTERNAL (tax), the
same as the FC/FC legs of the same codes always were.
"""
import argparse
import glob
import json
import os
import sys

import pandas as pd

SCR = r"C:\Users\ANDREW~1\AppData\Local\Temp\claude\C--Users-AndrewBerman-Desktop-ajb-workspace\3d236cad-007b-44c9-82e5-5614e20a648a\scratchpad"


# ---- THE RULE SET. Order matters: first match wins. Each rule = (name, predicate, partition, rationale)
def R(code=None, sb=None, tr=None, desc_kw=None):
    def pred(r):
        if code and r["tran_srcde"] not in code:
            return False
        if sb and r["sb_cd"] not in sb:
            return False
        if tr and r["tr_cd"] not in tr:
            return False
        if desc_kw and not any(k in r["transaction_source_code_description"].upper() for k in desc_kw):
            return False
        return True
    return pred


RULES = [
 # --- INTERNAL: trading + income + reinvestment + corp actions + sweeps (standard sec4 internal list) ---
 ("trades", R(code={"TRADE"}), "INTERNAL", "purchases and sales -- the standard's internal list, item 1"),
 ("reinvest", R(code={"RID","RIDA"}), "INTERNAL", "reinvestment activity -- explicitly internal in the standard (vendor leaves category EMPTY on these; classified by code)"),
 ("sweeps", R(code={"BKSWP","BRSWP","BKTRF"}), "INTERNAL", "auto bank sweep between brokerage and the sweep bank feature -- sec2 includes cash/sweep/money-market accounts INSIDE the portfolio boundary, so sweep legs are internal DESPITE the vendor category 'Deposits and Withdrawals'"),
 ("dividends", R(sb={"DV"}), "INTERNAL", "dividends / cap-gain distributions / their adjustments and reinvest legs -- internal income (sb_cd=DV family)"),
 ("interest", R(sb={"IN"}), "INTERNAL", "bank/CD interest and adjustments -- internal income (sb_cd=IN family)"),
 ("int-adj-fc", R(code={"BRINA","BWBKI"}), "INTERNAL", "interest manual adjustments carried under FC -- income adjustments, internal"),
 ("corp-actions", R(sb={"RO"}), "INTERNAL", "reorg family (mergers, conversions, liquidations, exchanges, maturities) -- corporate actions are internal; FC-side legs of the same events (vendor category often EMPTY) classify with their IC twins"),
 ("corp-actions-ic", R(tr={"IC"}, code={"ADJ","CVN","EXP","EXRT","ASG","CAPU","DIV","DEL_IN"}), "INTERNAL", "position adjustments / conversions / expirations / assignments on the IC side -- corporate-action mechanics, internal"),
 ("cash-in-lieu", R(code={"CIL","CILA"}), "INTERNAL", "cash in lieu of fractional shares -- corporate-action residue, internal"),
 ("withholding", R(code={"BWDIV","BWDIA","BWCAP","BWCRI","BWDYE","BWSTG","NRAW","NRAWA"}), "INTERNAL", "backup/NRA withholding on income -- a tax component of internal income (sec8: prefer net of non-reclaimable withholding); NOT an external flow"),
 # moved here 2026-10-02 from the second-pass block: it must precede wd-generic, whose sb_cd WD/WI match took the
 # FTP/FC/WD and FTR/FC/WD legs first and read them EXTERNAL (IRPT_DASHBD round 3, CTO ADDENDUM 1 A4).
 ("foreign-tax", R(code={"FTP","FTR"}), "INTERNAL", "foreign tax paid / reclaimed -- income tax components, internal (sec8 withholding policy), on every leg including the WD sub-code"),
 # --- FEE: management/advisory fee debits (the gross-vs-net lever) + custody/admin fees ---
 ("advisory-fee", R(code={"BILL","ABFEE","ABFEA","MFEE","ADVFE"}), "FEE-MANAGEMENT", "billing invoice / advisory-program fee debits -- THE gross-vs-net-of-fees lever (sec8); identified by code, not category"),
 ("service-fees", R(code={"FEE","FEEA","AS1FE"}), "FEE-ADMIN", "service fees -- custody/admin class; sec8 requires documenting whether included; retained in both gross and net unless ruled otherwise"),
 ("adr-fee", R(code={"ADRF","ADRFA"}), "FEE-ADMIN", "ADR pass-through management fee -- custody/admin class embedded at the security level"),
 # --- CONDITIONAL: boundary-relative journals/transfers (the standard: never classify from the label alone) ---
 ("journals", R(code={"$JNL","$TYPE","JNL","JRNL"}), "CONDITIONAL-BY-COUNTERPARTY", "TRF BTWN SCH ACCTS / JOURNAL -- internal iff BOTH accounts are inside the performance boundary, external otherwise. RESOLUTION RULE: swb_from/to where populated, else cross-account pair-match on (date, amount, +/-); fact_fam parse extends this to household boundaries"),
 ("shares-delivered", R(code={"DEL","REC"}), "CONDITIONAL-BY-COUNTERPARTY", "in-kind securities delivered out / received in -- external in-kind flow iff the counterparty is outside the boundary; valued at qty x same-date close (sec4 in-kind rule)"),
 ("acat", R(desc_kw=["ACAT","TRANSFER OF ACCT","ACCT TRANSFER"]), "CONDITIONAL-BY-COUNTERPARTY", "account-migration transfers -- external at the boundary unless both sides included; pair-match resolution"),
 # --- EXTERNAL: client money in/out (deposits, withdrawals, wires, checks, MoneyLink) ---
 ("deposits", R(sb={"FI"}), "EXTERNAL-IN", "funds-in family (deposits, wired funds in, MoneyLink) -- client capital entering; sign positive per sec4"),
 ("withdrawals", R(sb={"FO"}), "EXTERNAL-OUT", "funds-out family (wires out, checks paid) -- client capital leaving; sign negative"),
 ("wd-generic", R(sb={"WD","WI"}), "EXTERNAL", "withdrawal/deposit legs carried under WD/WI sub-codes -- external by family; per-code review at build refines direction"),
 ("checks-classified", R(code={"AS1DR","DPRET"}), "EXTERNAL", "Schwab One check disbursements / returned deposits -- client cash movements (returned deposit = external reversal pair)"),
  # --- second-pass families (from the first pass's unresolved residue, classified by inspection) ---
 ("acct-transfer", R(code={"TOA","T/A","TYP"}), "CONDITIONAL-BY-COUNTERPARTY", "TRANSFER ACCOUNT / journal family (FC cash side + IC in-kind side) -- the standard's account-migration class: EXTERNAL at the boundary unless both sides included; in-kind legs valued qty x close; pair-match + swb resolution"),
 ("advisor-fee-explicit", R(code={"MGFEE","MGFEA"}), "FEE-MANAGEMENT", "ADVISOR FEE / ADVISOR FEE ADJ -- explicit management-fee debits, the sec8 gross-vs-net lever"),
 ("advisor-fee-inferred", R(code={"TPFEE","SMFEE"}), "FEE-MANAGEMENT-INFERRED", "empty vendor description; classified management-fee by (a) code-name family (third-party fee / SMA-manager fee), (b) adjacency to explicit MGFEE, (c) magnitude plausibility (~$22M/yr on a $1.8B book ~ advisory-fee scale). INFERRED-STRONG -- specimen-verify one account's rows against its billing schedule at build; if refuted these re-partition and materiality re-runs"),
 ("ira-withholding", R(code={"IRAWH","MCE"}), "EXTERNAL-OUT", "IRS withholding on retirement distributions -- the withheld component leaves the portfolio with the distribution; external outflow component"),
 ("schwab-checks-out", R(code={"S1C"}), "EXTERNAL-OUT", "Schwab check disbursements -- client cash out"),
 ("alt-income", R(code={"NDST","NDSTA","NDIV","NDIVA"}), "INTERNAL", "alternative-investment distributions/dividends carried under FC/FC -- internal income"),
 ("corp-misc", R(code={"RDM","LIT","RCR","GUP","PRO"}), "INTERNAL", "redemption/conversion, litigation proceeds, small-balance adj, service credits -- internal economic events, de minimis"),
 ("returned-deposits", R(code={"PDRTN"}), "EXTERNAL", "returned deposit family -- external reversal pair"),
 ("lending-misc-ic", R(code={"WLES"}), "UNRESOLVED-PENDING-SPECIMEN", "IC no-description zero-cash micro-code (7 rows) -- specimen at build"),
 # --- residual small-print codes with explicit dispositions ---
 ("misc-adj", R(code={"AS1CR","ADJ","DPAJ","DPCSH","CHEA"}), "UNRESOLVED-PENDING-SPECIMEN", "misc/funds adjustments -- low-frequency adjustment codes; classify per specimen at build (the standard's unresolved bucket, materiality measured below)"),
]


def classify(row):
    for name, pred, part, why in RULES:
        try:
            if pred(row):
                return pd.Series({"rule": name, "partition": part})
        except Exception:
            continue
    return pd.Series({"rule": "no-rule", "partition": "UNRESOLVED"})


def reapply(path):
    """Re-run RULES over a recorded table, in place; return (rows, moved, kept).

    A row whose recorded rule is NOT a rule of this file is KEPT as recorded: a later act owns it (for example
    pair_match_engine.py's 5bb3b2626d, which upgraded TPFEE/SMFEE to advisor-fee-verified by measurement), and this
    builder must never walk it back. The file is rewritten in its own format (json indent 1, LF, no final newline),
    so the git diff carries only the rows that moved."""
    with open(path, encoding="utf-8") as fh:
        rows = json.load(fh)
    census = [k for k in ("tran_srcde", "tr_cd", "sb_cd", "rows", "sum_abs_gross", "max_abs_gross", "sum_inkind",
                          "first_date", "last_date", "category", "desc") if k in rows[0]]
    owned = {name for name, _, _, _ in RULES} | {"no-rule"}
    moved, kept = [], []
    for r in rows:
        if r["rule"] not in owned:
            kept.append("%s/%s/%s:%s" % (r["tran_srcde"], r["tr_cd"], r["sb_cd"], r["rule"]))
            continue
        # the build's classify() saw the census row's own columns (no transaction_source_code_description), so it
        # is handed exactly those again; the recorded rule and partition are not part of what it reads
        got = classify(pd.Series({k: r[k] for k in census}))
        if (got["rule"], got["partition"]) != (r["rule"], r["partition"]):
            moved.append({"code": "%s/%s/%s" % (r["tran_srcde"], r["tr_cd"], r["sb_cd"]), "rows": r.get("rows"),
                          "sum_abs_gross": r.get("sum_abs_gross"), "from": [r["rule"], r["partition"]],
                          "to": [got["rule"], got["partition"]]})
            r["rule"], r["partition"] = got["rule"], got["partition"]
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(rows, indent=1))
    return rows, moved, kept


def build(scr):
    d = os.path.join(scr, "trn_full")
    files = sorted(glob.glob(os.path.join(d, "date=*", "data.parquet")))
    frames = []
    for f in files:
        frames.append(pd.read_parquet(f, columns=[
            "business_date","tran_srcde","tr_cd","sb_cd","transaction_category",
            "transaction_source_code_description","gross_amount","net_amount","quantity","price","closing_price"]))
    t = pd.concat(frames, ignore_index=True)
    for c in ["tran_srcde","tr_cd","sb_cd","transaction_category","transaction_source_code_description"]:
        t[c] = t[c].astype(str).str.strip()
    for c in ["gross_amount","net_amount","quantity","price","closing_price"]:
        t[c] = pd.to_numeric(t[c], errors="coerce").fillna(0.0)
    t["abs_gross"] = t["gross_amount"].abs()
    t["inkind_value"] = (t["quantity"].abs() * t["closing_price"].abs())
    print("rows:", len(t), "days:", t["business_date"].nunique())

    key = ["tran_srcde","tr_cd","sb_cd"]
    cen = t.groupby(key).agg(
        rows=("abs_gross","size"), sum_abs_gross=("abs_gross","sum"), max_abs_gross=("abs_gross","max"),
        sum_inkind=("inkind_value","sum"),
        first_date=("business_date","min"), last_date=("business_date","max"),
        category=("transaction_category", lambda s: s.mode().iloc[0] if len(s.mode()) else ""),
        desc=("transaction_source_code_description", lambda s: next((x for x in s if x), "")),
    ).reset_index()
    cls = cen.apply(classify, axis=1)
    cen = pd.concat([cen, cls], axis=1)

    print("\n=== PARTITION TOTALS (full 25-month series, money = |gross|; security-transfer value = qty*close) ===")
    g = cen.groupby("partition").agg(codes=("rows","size"), rows=("rows","sum"), dollars=("sum_abs_gross","sum"), inkind=("sum_inkind","sum"))
    for p, r in g.sort_values("dollars", ascending=False).iterrows():
        print(f"  {p:34} codes={int(r['codes']):3} rows={int(r['rows']):8} |gross|=${r['dollars']:18,.2f} inkind=${r['inkind']:16,.2f}")

    unres = cen[cen["partition"].str.startswith("UNRESOLVED")]
    print(f"\n=== UNRESOLVED RESIDUE: {len(unres)} codes, {int(unres['rows'].sum())} rows, ${unres['sum_abs_gross'].sum():,.2f} |gross| ===")
    for _, r in unres.sort_values("sum_abs_gross", ascending=False).head(40).iterrows():
        print(f"  srcde={r['tran_srcde']:>6} tr={r['tr_cd']:>3} sb={r['sb_cd']:>3} rows={int(r['rows']):7} ${r['sum_abs_gross']:14,.2f} cat='{r['category']}' desc='{r['desc'][:48]}'")

    # materiality frames
    bal = pd.read_parquet(os.path.join(scr, "sdd", "dim_balance.parquet"))
    book = pd.to_numeric(bal["net_mv_plus_cash"], errors="coerce").fillna(0).sum()
    ext = cen[cen["partition"].str.startswith("EXTERNAL")]["sum_abs_gross"].sum()
    cond = cen[cen["partition"]=="CONDITIONAL-BY-COUNTERPARTY"]["sum_abs_gross"].sum()
    u_d = unres["sum_abs_gross"].sum()
    print("\n=== MATERIALITY FRAMES ===")
    print(f"  book value (dim_balance 2026-08-07 sum net_mv_plus_cash): ${book:,.2f}")
    print(f"  EXTERNAL |gross| (25 months): ${ext:,.2f}")
    print(f"  CONDITIONAL |gross| (journals etc, resolution-ruled): ${cond:,.2f}")
    print(f"  UNRESOLVED |gross|: ${u_d:,.2f}  = {u_d/book*100:.4f}% of book, {u_d/max(ext,1)*100:.4f}% of external-flow magnitude")

    cen_out = cen.sort_values("sum_abs_gross", ascending=False)
    cen_out.to_json(os.path.join(scr, "classification_table_full.json"), orient="records", indent=1)
    print("\nsaved classification_table_full.json  rows:", len(cen_out))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--reapply", help="re-run the rule set over a recorded table JSON, in place")
    a = ap.parse_args()
    if a.reapply:
        table, moved, kept = reapply(a.reapply)
        print("REAPPLY: %d code rows, %d moved, %d kept as recorded (rules this file does not own: %s)"
              % (len(table), len(moved), len(kept), ", ".join(kept) or "none"))
        for m in moved:
            print("  %(code)s rows=%(rows)s |gross|=%(sum_abs_gross)s  %(from)s -> %(to)s" % m)
        sys.exit(0)
    build(SCR)
