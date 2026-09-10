"""AMGT_RESAPP.TO-AMGT-s-11 -- produces figure_units.json.

Not a corpus scan: this is a hand-transcription of the CRO's own MEASURED field map
(org/tier1_exec/4.0.0_SA_CRO/deliverables/AMGT_RESAPP_BLOOMBERG_FIELD_MAP_20260910.md
@e06bc53d8067d9a5fdd936a8b1151eca0693f550), measured on one security, SAP GY Equity,
sections 2 and 3 ("Header block" and "Financial summary"). Every row in those two tables
is transcribed below with the unit-convention category the field map's own text assigns it;
the histogram is computed from that list (never hand-summed) so the count cannot drift from
the transcription.

The figure rule (lib/research/rules/figure.py) has NO numeric threshold -- its refusal is
categorical: a figure whose unit_status is not MEASURED is REFUSED. This distribution is
what shows why a categorical rule is still warranted: Bloomberg's own field families disagree
on ABSOLUTE vs MILLIONS vs PERCENT vs DECIMAL, one field has its sign inverted, one field has
no reproducing mnemonic at all, and one label is used for two different quantities.
"""
from __future__ import annotations

import json
import os
from collections import Counter

OUT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figure_units.json")

SOURCE = (
    "org/tier1_exec/4.0.0_SA_CRO/deliverables/"
    "AMGT_RESAPP_BLOOMBERG_FIELD_MAP_20260910.md@e06bc53d8067d9a5fdd936a8b1151eca0693f550"
)

# Every mapped row in field-map s.2 (Header block) and s.3 (Financial summary), transcribed
# with the unit-convention category the field map's own prose assigns. "Mapped" here = the
# row has a Bloomberg mnemonic attempted (served YES/NULL/NO all counted -- a figure whose
# unit/sign status was never established is exactly the REFUSE case this rule names).
FIELDS = [
    # -- s.2 Header block (16 rows) --
    {"field": "Name", "mnemonic": "NAME", "category": "STRING_FORMAT_ONLY"},
    {"field": "Currency", "mnemonic": "CRNCY", "category": "STRING_FORMAT_ONLY"},
    {"field": "Location", "mnemonic": "CNTRY_OF_DOMICILE", "category": "STRING_FORMAT_ONLY"},
    {"field": "Sector", "mnemonic": "GICS_SECTOR_NAME", "category": "TAXONOMY_MISMATCH"},
    {"field": "Share Price", "mnemonic": "PX_LAST", "category": "PER_SHARE"},
    {"field": "Market Cap", "mnemonic": "CUR_MKT_CAP", "category": "ABSOLUTE"},
    {"field": "Net Debt", "mnemonic": "NET_DEBT", "category": "MILLIONS"},
    {"field": "Enterprise Value", "mnemonic": "CURR_ENTP_VAL", "category": "MILLIONS"},
    {"field": "ADTV", "mnemonic": "VOLUME_AVG_30D", "category": "ABSOLUTE"},
    {"field": "Outstanding Shares", "mnemonic": "EQY_SH_OUT_REAL", "category": "ABSOLUTE"},
    {"field": "Float", "mnemonic": "EQY_FREE_FLOAT_PCT", "category": "CONFLICTING_DEFINITION"},
    {"field": "Beta", "mnemonic": "EQY_BETA", "category": "RATIO"},
    {"field": "Div Yield", "mnemonic": "EQY_DVD_YLD_IND", "category": "PERCENT_VS_DECIMAL"},
    {"field": "Fiscal Yr", "mnemonic": "FISCAL_YEAR_END", "category": "INVALID_FIELD"},
    {"field": "Short Interest", "mnemonic": "SHORT_INT_RATIO / SI_PERCENT_EQUITY_FLOAT", "category": "NULL_VALID_NO_DATA"},
    # "Date of Pricing" excluded: field map states "n/a -- pull timestamp, not a field".
    # -- s.3 Financial summary (17 rows with a mnemonic; 2 without one are their own categories) --
    {"field": "Revenue", "mnemonic": "SALES_REV_TURN", "category": "MILLIONS"},
    {"field": "Operating Income", "mnemonic": "IS_OPER_INC", "category": "MILLIONS"},
    {"field": "Operating Margin", "mnemonic": "OPER_MARGIN", "category": "PERCENT_VS_DECIMAL"},
    {"field": "EBITDA", "mnemonic": "EBITDA_ADJUSTED", "category": "MILLIONS"},
    {"field": "EBITDA Margin", "mnemonic": "EBITDA_MARGIN", "category": "PERCENT_VS_DECIMAL"},
    {"field": "EPS recurring", "mnemonic": None, "category": "UNRESOLVED"},
    {"field": "BVPS", "mnemonic": "BOOK_VAL_PER_SH", "category": "PER_SHARE"},
    {"field": "Avg Diluted Shares", "mnemonic": "IS_SH_FOR_DILUTED_EPS", "category": "MILLIONS"},
    {"field": "Cap Ex", "mnemonic": "CAPITAL_EXPEND", "category": "SIGN_INVERTED"},
    {"field": "FCF", "mnemonic": "CF_FREE_CASH_FLOW", "category": "MILLIONS"},
    {"field": "DPS", "mnemonic": "IS_DIV_PER_SHR", "category": "PER_SHARE"},
    {"field": "ROA", "mnemonic": "RETURN_ON_ASSET", "category": "PERCENT_VS_DECIMAL"},
    {"field": "ROE", "mnemonic": "RETURN_COM_EQY", "category": "PERCENT_VS_DECIMAL"},
    {"field": "P/E", "mnemonic": "PE_RATIO", "category": "RATIO"},
    {"field": "EV/EBITDA", "mnemonic": "CURRENT_EV_TO_T12M_EBITDA", "category": "RATIO"},
    {"field": "P/B", "mnemonic": "PX_TO_BOOK_RATIO", "category": "RATIO"},
    {"field": "Dividend Yield", "mnemonic": "EQY_DVD_YLD_IND", "category": "PERCENT_VS_DECIMAL"},
    {"field": "FCF Yield / FCF Margin", "mnemonic": None, "category": "DERIVED_NOT_A_FIELD"},
]


def main() -> None:
    histogram = dict(Counter(f["category"] for f in FIELDS))
    sign_inversions = [f["field"] for f in FIELDS if f["category"] == "SIGN_INVERTED"]

    out = {
        "cell": "AMGT-s-11",
        "produced_by": "0.9.0_WK_AMGT_RESAPP~8",
        "source": SOURCE,
        "measured_on": "one security: SAP GY Equity (the field map's own stated scope)",
        "method": "hand-transcription of field-map s.2+s.3 table rows; histogram computed from the transcription list, not hand-summed",
        "denominator": len(FIELDS),
        "fields": FIELDS,
        "histogram": histogram,
        "sign_inversions": len(sign_inversions),
        "sign_inversion_fields": sign_inversions,
        "note": (
            "the figure rule has NO numeric threshold -- refusal is categorical: unit_status "
            "not MEASURED -> REFUSE. This histogram is what shows why: ABSOLUTE vs MILLIONS vs "
            "PERCENT-vs-DECIMAL vs PER_SHARE vs RATIO are all live conventions across the SAME "
            "vendor's own field families on ONE security, one field has no reproducing mnemonic "
            "at all (UNRESOLVED), one label serves two different quantities "
            "(CONFLICTING_DEFINITION), and one field's sign is inverted relative to the workbook."
        ),
    }

    with open(OUT_PATH, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2)

    print(f"wrote {OUT_PATH}")
    print(f"denominator {len(FIELDS)} histogram {histogram} sign_inversions {len(sign_inversions)}")


if __name__ == "__main__":
    main()
