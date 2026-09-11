"""build_field_map.py -- AMGT-s-1 (d): re-measure the CRO's field map's unit and sign, per field,
on the control (SAP GY Equity) plus a US-domiciled name (BA US Equity) and an ADR (BABA US
Equity), reading the RAW bytes already landed in S3 (grounding the read in the served artifact,
never the pull's in-memory result or a self-report).

METHOD (F4's method, C-UNIT-MAP-MEASURED): for each numeric field, the observed value's
MAGNITUDE on that specific security is compared against the known real-world scale for that
field family (percent vs decimal; absolute vs millions; per-share; dimensionless ratio) -- the
same technique the CRO's own brief used on SAP alone (e.g. "26.13 vs workbook's 0.23" -> PERCENT,
not DECIMAL). A field's unit_status is "MEASURED" only when this comparison actually discriminated
on THAT security; otherwise it is recorded "UNRESOLVED-ON-<security>", never guessed.

For SIGN, the field's algebraic sign as returned is read directly (not inferred) and, where the
estate holds an established real-world convention for that field (Bloomberg's own cash-outflow
convention on CAPITAL_EXPEND), the observed sign is compared against it and labelled accordingly;
a sign that contradicts the established convention is recorded as a FINDING, not smoothed away.

Where a field's classified unit or sign DIFFERS across the three securities, `unit`/`sign` is
recorded PER-SECURITY (a dict) rather than one shared string, per the cell text: "a field that
differs is a FINDING, recorded, and its unit is per-security in the map."
"""
from __future__ import annotations

import json
from pathlib import Path

import boto3

BUCKET = "opal-data-research"
SECURITIES = ["SAP GY Equity", "BA US Equity", "BABA US Equity"]

TEXT_FIELDS = {"NAME", "CRNCY", "CNTRY_OF_DOMICILE", "GICS_SECTOR_NAME"}
PERCENT_FIELDS = {
    "OPER_MARGIN", "EBITDA_MARGIN", "RETURN_ON_ASSET", "RETURN_COM_EQY",
    "EQY_FREE_FLOAT_PCT", "EQY_DVD_YLD_IND", "SI_PERCENT_EQUITY_FLOAT",
}
ABSOLUTE_OR_MILLIONS_FIELDS = {
    "CUR_MKT_CAP", "NET_DEBT", "CURR_ENTP_VAL", "SALES_REV_TURN", "IS_OPER_INC",
    "EBITDA", "EBITDA_ADJUSTED", "CF_FREE_CASH_FLOW", "CAPITAL_EXPEND",
}
PER_SHARE_FIELDS = {"BOOK_VAL_PER_SH", "IS_DIV_PER_SHR", "IS_EPS"}
RATIO_FIELDS = {"EQY_BETA", "PE_RATIO", "CURRENT_EV_TO_T12M_EBITDA", "PX_TO_BOOK_RATIO", "SHORT_INT_RATIO"}
SHARE_COUNT_ABSOLUTE_FIELDS = {"EQY_SH_OUT_REAL", "VOLUME_AVG_30D"}
SHARE_COUNT_MILLIONS_FIELDS = {"IS_SH_FOR_DILUTED_EPS"}

# Established real-world sign conventions (a comparison target, per bound (f)/F4's method) --
# only stated where the estate already holds a specific finding (the CRO's CAPITAL_EXPEND
# reading; NET_DEBT's ordinary net-cash/net-debt duality).
SIGN_CONVENTIONS = {
    "CAPITAL_EXPEND": {
        "NEGATIVE": "NEGATIVE (Bloomberg cash-outflow convention, matches CRO's SAP finding)",
        "POSITIVE": "POSITIVE (DIFFERS FROM CRO'S CAPITAL_EXPEND SIGN FINDING ON SAP -- recorded, not smoothed)",
    },
    "NET_DEBT": {
        "NEGATIVE": "NEGATIVE (net-cash position)",
        "POSITIVE": "POSITIVE (net-debt position)",
    },
}

BASIS = {
    "NAME": "Bloomberg-maintained legal/short name of the issuer.",
    "CRNCY": "ISO currency code of the security's trading/reporting currency.",
    "CNTRY_OF_DOMICILE": "ISO country code of the issuer's domicile.",
    "GICS_SECTOR_NAME": "GICS sector classification name, Bloomberg's own taxonomy mapping.",
    "PX_LAST": "Last traded/closing price, in the security's trading currency.",
    "CUR_MKT_CAP": "Current market capitalization, full currency units (not millions).",
    "NET_DEBT": "Total debt minus cash and equivalents; can be negative (a net-cash position).",
    "CURR_ENTP_VAL": "Current enterprise value (market cap + net debt + minority interest - equity affiliates).",
    "VOLUME_AVG_30D": "30-trading-day average daily volume, absolute share count.",
    "EQY_SH_OUT_REAL": "Real-time shares outstanding, absolute share count.",
    "EQY_FREE_FLOAT_PCT": "Free-float shares as a percent of shares outstanding.",
    "EQY_BETA": "Bloomberg-computed equity beta, Bloomberg's default calculation window.",
    "EQY_DVD_YLD_IND": "Indicated dividend yield, percent.",
    "SHORT_INT_RATIO": "Short interest ratio (days-to-cover).",
    "SI_PERCENT_EQUITY_FLOAT": "Short interest as a percent of free float.",
    "SALES_REV_TURN": "Total revenue/turnover.",
    "IS_OPER_INC": "Operating income.",
    "OPER_MARGIN": "Operating margin, percent.",
    "EBITDA": "Bloomberg's reported (unadjusted) EBITDA.",
    "EBITDA_ADJUSTED": "Bloomberg's adjusted EBITDA (Bloomberg's own methodology).",
    "EBITDA_MARGIN": "EBITDA margin, percent (denominator is Bloomberg's EBITDA definition).",
    "IS_EPS": "Bloomberg's reported earnings-per-share figure, Bloomberg's own definition.",
    "BOOK_VAL_PER_SH": "Book value per share.",
    "IS_SH_FOR_DILUTED_EPS": "Weighted-average diluted shares used for EPS.",
    "CAPITAL_EXPEND": "Capital expenditure; Bloomberg reports this as a cash outflow (negative sign).",
    "CF_FREE_CASH_FLOW": "Free cash flow.",
    "IS_DIV_PER_SHR": "Dividend per share.",
    "RETURN_ON_ASSET": "Return on assets, percent.",
    "RETURN_COM_EQY": "Return on common equity, percent.",
    "PE_RATIO": "Price/earnings ratio.",
    "CURRENT_EV_TO_T12M_EBITDA": "Enterprise value / trailing-twelve-month EBITDA.",
    "PX_TO_BOOK_RATIO": "Price/book ratio.",
}

ALL_MNEMONICS = sorted(
    TEXT_FIELDS | PERCENT_FIELDS | ABSOLUTE_OR_MILLIONS_FIELDS | PER_SHARE_FIELDS
    | RATIO_FIELDS | SHARE_COUNT_ABSOLUTE_FIELDS | SHARE_COUNT_MILLIONS_FIELDS | {"PX_LAST"}
)


def security_key(security: str) -> str:
    return security.replace(" ", "_")


def _latest_stamp(s3, prefix: str) -> str:
    resp = s3.list_objects_v2(Bucket=BUCKET, Prefix=prefix, Delimiter="/")
    stamps = [cp["Prefix"][len(prefix):-1] for cp in resp.get("CommonPrefixes", [])]
    if not stamps:
        raise RuntimeError(f"no stamp under s3://{BUCKET}/{prefix}")
    return sorted(stamps)[-1]


def load_raw(s3, security: str) -> tuple[dict, list]:
    sec_key = security_key(security)
    prefix = f"raw/bloomberg/{sec_key}/"
    stamp = _latest_stamp(s3, prefix)
    ref_obj = s3.get_object(Bucket=BUCKET, Key=f"{prefix}{stamp}/refdata.json")
    hist_obj = s3.get_object(Bucket=BUCKET, Key=f"{prefix}{stamp}/histdata.json")
    ref = json.loads(ref_obj["Body"].read())
    hist = json.loads(hist_obj["Body"].read())
    return ref.get(security, {}), hist.get(security, [])


def sample_value(mnemonic: str, header: dict, hist_rows: list):
    """One representative value to classify: header's own value if header carries this
    mnemonic; else the most recent fiscal year (by date, descending) that carries it."""
    if mnemonic in header:
        return header.get(mnemonic)
    for row in sorted(hist_rows, key=lambda r: r.get("date", ""), reverse=True):
        if mnemonic in row and row[mnemonic] is not None:
            return row[mnemonic]
    return None


def classify_unit(mnemonic: str, value, security: str) -> tuple[str | None, str]:
    if value is None or value == "":
        return None, f"UNRESOLVED-ON-{security}"
    if mnemonic in TEXT_FIELDS:
        if isinstance(value, str) and value.strip():
            return "TEXT (string field)", "MEASURED"
        return None, f"UNRESOLVED-ON-{security}"
    try:
        v = float(value)
    except (TypeError, ValueError):
        return None, f"UNRESOLVED-ON-{security}"
    av = abs(v)

    if mnemonic == "PX_LAST":
        if 0 < av < 100000:
            return "PRICE (local trading currency, per share/unit)", "MEASURED"
        return None, f"UNRESOLVED-ON-{security}"
    if mnemonic in PERCENT_FIELDS:
        # Bloomberg's established convention for this field family (CRO's SAP finding, e.g.
        # OPER_MARGIN 26.13 vs the workbook's decimal 0.23) is PERCENT. A genuine DECIMAL
        # fraction for a margin/return/yield/float-pct field is realistically < 0.3 (below
        # that, a percent-scale reading would mean an implausibly tiny sub-0.3% margin/yield
        # for a large-cap issuer); at or above 0.3 the value is unambiguously percent-scale --
        # 0.3 itself reads as a plausible 0.3% yield, never a plausible 30% expressed oddly.
        if av >= 0.3:
            return "PERCENT", "MEASURED"
        if 0 < av < 0.3:
            return "DECIMAL (differs from CRO's PERCENT reading on SAP)", "MEASURED"
        return None, f"UNRESOLVED-ON-{security}"
    if mnemonic in ABSOLUTE_OR_MILLIONS_FIELDS:
        if av > 1e9:
            return "ABSOLUTE (full currency units)", "MEASURED"
        if 1.0 < av < 1e7:
            return "MILLIONS", "MEASURED"
        return None, f"UNRESOLVED-ON-{security}"
    if mnemonic in PER_SHARE_FIELDS:
        if 0 < av < 2000:
            return "PER SHARE (local trading/reporting currency)", "MEASURED"
        return None, f"UNRESOLVED-ON-{security}"
    if mnemonic in RATIO_FIELDS:
        if 0 < av < 1000:
            return "RATIO (dimensionless multiple)", "MEASURED"
        return None, f"UNRESOLVED-ON-{security}"
    if mnemonic in SHARE_COUNT_ABSOLUTE_FIELDS:
        if av > 1e2:
            return "ABSOLUTE (share count)", "MEASURED"
        return None, f"UNRESOLVED-ON-{security}"
    if mnemonic in SHARE_COUNT_MILLIONS_FIELDS:
        if 1 < av < 1e6:
            return "MILLIONS (share count)", "MEASURED"
        return None, f"UNRESOLVED-ON-{security}"
    return None, f"UNRESOLVED-ON-{security}"


def classify_sign(mnemonic: str, value, security: str) -> tuple[str | None, str]:
    if value is None or value == "":
        return None, f"UNRESOLVED-ON-{security}"
    if mnemonic in TEXT_FIELDS:
        return "N/A (non-numeric field)", "MEASURED"
    try:
        v = float(value)
    except (TypeError, ValueError):
        return "N/A (non-numeric field)", "MEASURED"
    if v > 0:
        base = "POSITIVE"
    elif v < 0:
        base = "NEGATIVE"
    else:
        return None, f"UNRESOLVED-ON-{security}"  # zero: ambiguous, not claimed
    conv = SIGN_CONVENTIONS.get(mnemonic)
    if conv and base in conv:
        return conv[base], "MEASURED"
    return base, "MEASURED"


def merge_by_fiscal_year(hist_rows: list) -> dict:
    """Same grouping rule as model_block_pull.py's merge_by_fiscal_year (duplicated rather than
    imported -- there is no package marker linking deliverables/ to integrations/bloomberg/research/,
    and this one function is simple enough that a documented duplicate is safer than a path hack).
    Needed here because a security whose fiscal-year end is NOT December (BABA US Equity, FYE
    March 31) can return a raw historical series where NO SINGLE raw row carries both a price
    field and a fundamentals field -- fiscal-period rows (March) and calendar-year price/ratio
    rows (December) are always disjoint for that security, so a same-currency PE cross-check must
    read the MERGED fiscal-year record, not a raw row."""
    groups: dict[str, dict] = {}
    for row in hist_rows:
        date = row.get("date")
        if not date:
            continue
        fy = date[:4]
        g = groups.setdefault(fy, {"fiscal_year": fy})
        for k, v in row.items():
            if k == "date":
                continue
            g[k] = v
    return groups


def detect_reporting_currency_mismatch(per_security: dict) -> list[dict]:
    """A SELF-CONSISTENT cross-check, not an external assumption: Bloomberg computes PE_RATIO
    itself (PX_LAST / EPS). Merging each security's raw historical rows onto the fiscal-year
    join key (merge_by_fiscal_year, above -- the SAME grouping model_block_pull.py's `derive`
    stage uses) and then dividing THAT fiscal year's merged PX_LAST by its merged IS_EPS, then
    comparing the result against Bloomberg's OWN PE_RATIO for the same fiscal-year label, tests
    whether the two figures merged under one fiscal-year label are actually mutually consistent.

    On the control (SAP GY Equity, a December-FYE issuer where the price and fundamentals
    sub-rows fall in the same or adjacent calendar days) this reconciles to 6 decimal places --
    a positive control confirming the method itself is sound. On the ADR (BABA US Equity, FYE
    31 March) it does NOT reconcile -- naive PE comes out roughly 5-6x smaller than Bloomberg's
    own PE_RATIO for the same fiscal-year label.

    WHAT THIS DOES NOT CLAIM: BABA's raw historical response never carries a single row with
    both a price field and an IS_EPS/fundamentals field (see README -- 100% of its rows split
    fundamentals, dated the fiscal period end 31 March, from price/ratios, dated the CALENDAR
    year end 31 December, roughly nine months later). So a mismatch here is CONSISTENT WITH
    EITHER a currency difference between the fundamentals-reporting basis and the ADR's USD
    trading quote, OR the ~9-month timing gap between the two sub-rows merged under one
    fiscal-year label (the stock price moved between the fiscal period end and the calendar
    year end), OR an ADR-to-ordinary-share ratio effect, OR some combination -- this check
    isolates THAT the fiscal-year-merged PX_LAST/IS_EPS pairing does not reproduce Bloomberg's
    own multiple for a non-December-FYE issuer; it does not isolate WHICH of those causes, and
    does not claim to (bound (f): state the basis and the finding, never guess past what was
    actually measured).
    """
    findings = []
    for sec in SECURITIES:
        header = per_security[sec]["header"]
        hist_rows = per_security[sec]["hist_rows"]
        crncy = header.get("CRNCY")
        fy_groups = merge_by_fiscal_year(hist_rows)
        for fy in sorted(fy_groups.keys(), reverse=True):
            row = fy_groups[fy]
            px, eps, bbg_pe = row.get("PX_LAST"), row.get("IS_EPS"), row.get("PE_RATIO")
            # A loss year (eps <= 0) makes P/E undefined on a GAAP basis; Bloomberg's own
            # PE_RATIO then commonly switches to a different EPS basis (e.g. forward/adjusted)
            # to still report a positive multiple -- comparing against raw IS_EPS in that case
            # tests basis-swap, not currency/timing, and is not evidence either way. Only a
            # genuine positive-earnings fiscal year is a clean comparison.
            if not px or not eps or eps <= 0 or not bbg_pe or bbg_pe <= 0:
                continue
            naive_pe = px / eps
            ratio = naive_pe / bbg_pe
            if not (0.8 <= ratio <= 1.25):
                findings.append(
                    {
                        "security": sec,
                        "crncy": crncy,
                        "checked_fiscal_year": fy,
                        "px_last": px,
                        "is_eps": eps,
                        "naive_pe_px_over_eps": naive_pe,
                        "bloomberg_pe_ratio": bbg_pe,
                        "naive_to_bloomberg_ratio": ratio,
                        "finding": (
                            f"fiscal-year-{fy}-merged naive PE (PX_LAST/IS_EPS = {naive_pe:.4f}) "
                            f"disagrees with Bloomberg's own PE_RATIO ({bbg_pe}) for the same "
                            f"fiscal-year label by a factor of {ratio:.4f} on {sec} -- consistent "
                            "with a currency difference between the fundamentals-reporting basis "
                            "and the header's CRNCY/PX_LAST trading-currency quote, AND/OR the "
                            "gap between the fiscal-period-end fundamentals sub-row and the "
                            "calendar-year-end price sub-row this security's raw response always "
                            "splits into (never a single merged row), AND/OR an ADR share-ratio "
                            "effect. NOT isolated to one cause; the other MILLIONS/PER-SHARE-scale "
                            "financial-statement fields on this security carry the same caveat. "
                            "Recorded as a FINDING, not resolved further (bound (f))."
                        ),
                    }
                )
                break  # one confirming fiscal year is sufficient evidence; do not repeat per year
            else:
                # First fiscal year that DID reconcile is the positive control for this
                # security -- stop looking (no finding to record).
                break
    return findings


def build() -> dict:
    s3 = boto3.client("s3")
    per_security = {}
    for sec in SECURITIES:
        header, hist_rows = load_raw(s3, sec)
        per_security[sec] = {"header": header, "hist_rows": hist_rows}

    currency_findings = detect_reporting_currency_mismatch(per_security)

    fields = []
    for mnemonic in ALL_MNEMONICS:
        unit_by_sec: dict[str, str | None] = {}
        unit_status_by_sec: dict[str, str] = {}
        sign_by_sec: dict[str, str | None] = {}
        sign_status_by_sec: dict[str, str] = {}
        measured_on = []
        for sec in SECURITIES:
            header = per_security[sec]["header"]
            hist_rows = per_security[sec]["hist_rows"]
            val = sample_value(mnemonic, header, hist_rows)
            u, u_status = classify_unit(mnemonic, val, sec)
            s, s_status = classify_sign(mnemonic, val, sec)
            unit_by_sec[sec] = u
            unit_status_by_sec[sec] = u_status
            sign_by_sec[sec] = s
            sign_status_by_sec[sec] = s_status
            if u_status == "MEASURED" and s_status == "MEASURED":
                measured_on.append(sec)

        all_measured = all(unit_status_by_sec[sec] == "MEASURED" for sec in SECURITIES) and all(
            sign_status_by_sec[sec] == "MEASURED" for sec in SECURITIES
        )
        distinct_units = {unit_by_sec[sec] for sec in SECURITIES if unit_status_by_sec[sec] == "MEASURED"}
        distinct_signs = {sign_by_sec[sec] for sec in SECURITIES if sign_status_by_sec[sec] == "MEASURED"}

        if all_measured:
            unit_status = "MEASURED"
            sign_status = "MEASURED"
            unit_out = next(iter(distinct_units)) if len(distinct_units) == 1 else dict(unit_by_sec)
            sign_out = next(iter(distinct_signs)) if len(distinct_signs) == 1 else dict(sign_by_sec)
        else:
            first_bad = next(
                sec for sec in SECURITIES
                if unit_status_by_sec[sec] != "MEASURED" or sign_status_by_sec[sec] != "MEASURED"
            )
            unit_status = unit_status_by_sec[first_bad] if unit_status_by_sec[first_bad] != "MEASURED" else "MEASURED"
            sign_status = sign_status_by_sec[first_bad] if sign_status_by_sec[first_bad] != "MEASURED" else "MEASURED"
            unit_out = dict(unit_by_sec)
            sign_out = dict(sign_by_sec)

        finding = None
        if len(distinct_units) > 1:
            finding = f"unit differs across securities: {unit_by_sec}"

        fields.append(
            {
                "mnemonic": mnemonic,
                "unit": unit_out,
                "unit_status": unit_status,
                "sign": sign_out,
                "sign_status": sign_status,
                "measured_on": measured_on,
                "basis": {"mnemonic": mnemonic, "definition": BASIS.get(mnemonic, "Bloomberg DAPI field.")},
                "per_security_detail": {
                    sec: {
                        "value_sampled": sample_value(mnemonic, per_security[sec]["header"], per_security[sec]["hist_rows"]),
                        "unit_status": unit_status_by_sec[sec],
                        "sign_status": sign_status_by_sec[sec],
                    }
                    for sec in SECURITIES
                },
                "finding": finding,
            }
        )

    return {
        "securities": SECURITIES,
        "fields": fields,
        "cross_security_findings": currency_findings,
    }


def main() -> int:
    out = build()
    n_fields = len(out["fields"])
    n_three = sum(
        1 for f in out["fields"]
        if f["unit_status"] == "MEASURED" and f["sign_status"] == "MEASURED" and len(f["measured_on"]) >= 3
    )
    n_findings = sum(1 for f in out["fields"] if f["finding"])
    n_currency = len(out["cross_security_findings"])
    out_path = Path("org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~1/field_map.json")
    out_path.write_text(json.dumps(out, indent=2, default=str), encoding="utf-8")
    print(
        f"FIELD MAP BUILT: {n_fields} fields, {n_three} measured-on-3 (unit+sign), "
        f"{n_findings} cross-security unit findings, {n_currency} reporting-currency findings"
    )
    for cf in out["cross_security_findings"]:
        print(f"  CURRENCY FINDING: {cf['security']} -- {cf['finding']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
