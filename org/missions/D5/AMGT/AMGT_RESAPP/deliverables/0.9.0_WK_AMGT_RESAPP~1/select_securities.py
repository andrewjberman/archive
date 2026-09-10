"""select_securities.py -- reproduces, from AMGT-s-12's universe.json, the rule that picks the
two non-control securities for AMGT-s-1 (a US-listed name and an ADR), so the choice is a
re-runnable procedure and not an unrecorded eyeball pick.

RULE, stated once and applied mechanically:
  1. Read org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~3/universe.json.
  2. Keep only entries with bloomberg_ticker.status == "MEASURED".
  3. DROP every entry whose bloomberg_ticker.value is a value shared by more than one folder.
     universe.json carries a measurement defect (recorded separately as a surprise row): 16 of
     the 48 MEASURED entries -- unrelated folders from AstraZeneca to Total Energies, including
     the folder for the CRO's own control name "SAP GY" -- all read the identical string
     "AAPL US". A value that recurs across unrelated folders is not a per-security read; it is
     excluded from consideration here rather than trusted.
  4. Among the remaining uniquely-valued entries, classify each surviving folder by hand-checked
     public-record fact (never inferred from the ticker string alone): US_DOMICILED if the
     issuer is a US-domiciled operating company trading on its home exchange, ADR if the issuer
     is foreign-domiciled and the Bloomberg ticker is a US-listed depositary-receipt line.
  5. Pick the alphabetically-first (by folder name) qualifying entry in each category.

This never reads or trusts the "SAP GY" row in universe.json (defective per step 3); the control
security SAP GY Equity is taken directly from the task order's own text and the CRO's field map,
not from this file.
"""
from __future__ import annotations

import json
from pathlib import Path

UNIVERSE_PATH = Path(
    "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~3/universe.json"
)

# Hand-checked, independent of the ticker string itself (step 4). This is a classification of
# company DOMICILE + LISTING TYPE for the folders that survive the uniqueness filter (step 3) --
# not a guess from the ticker suffix.
US_DOMICILED_FOLDERS = {
    "Boeing BA": "US-domiciled aerospace manufacturer, primary listing NYSE.",
    "Costco COST": "US-domiciled retailer, primary listing NASDAQ.",
    "Haliburton HAL": "US-domiciled (originally; now UK-domiciled post-2010 redomicile, "
                      "still trades as a US primary listing) oilfield-services company, NYSE.",
    "Home Depot HD": "US-domiciled retailer, primary listing NYSE.",
    "Intuit INTU": "US-domiciled software company, primary listing NASDAQ.",
    "Kimberly Clark KMB": "US-domiciled consumer-products company, primary listing NYSE.",
    "Valero Energy VLO": "US-domiciled refiner, primary listing NYSE.",
}
ADR_FOLDERS = {
    "Alibaba BABA": "Cayman-Islands-domiciled / China-operating company; BABA US Equity is the "
                    "NYSE-listed American Depositary Share line, not the primary listing.",
    "Petrobras PETR3 BZ": "Brazil-domiciled company; PBR US Equity is the NYSE-listed American "
                          "Depositary Receipt line, distinct from the BZ-listed PETR3 primary line.",
}


def load_measured_entries() -> list[dict]:
    u = json.loads(UNIVERSE_PATH.read_text(encoding="utf-8"))
    return [n for n in u["names"] if n["bloomberg_ticker"]["status"] == "MEASURED"]


def drop_duplicate_values(entries: list[dict]) -> tuple[list[dict], dict[str, int]]:
    counts: dict[str, int] = {}
    for n in entries:
        v = n["bloomberg_ticker"]["value"]
        counts[v] = counts.get(v, 0) + 1
    clean = [n for n in entries if counts[n["bloomberg_ticker"]["value"]] == 1]
    dup_report = {v: c for v, c in counts.items() if c > 1}
    return clean, dup_report


def pick(clean_entries: list[dict], eligible_folders: dict[str, str]) -> dict:
    candidates = [n for n in clean_entries if n["folder"] in eligible_folders]
    candidates.sort(key=lambda n: n["folder"])
    if not candidates:
        raise RuntimeError("no eligible candidate survived the uniqueness filter")
    chosen = candidates[0]
    return {
        "folder": chosen["folder"],
        "bloomberg_ticker": chosen["bloomberg_ticker"]["value"],
        "security": chosen["bloomberg_ticker"]["value"] + " Equity",
        "rationale": eligible_folders[chosen["folder"]],
        "all_eligible_folders_considered": [c["folder"] for c in candidates],
    }


def main() -> int:
    measured = load_measured_entries()
    clean, dup_report = drop_duplicate_values(measured)
    us_pick = pick(clean, US_DOMICILED_FOLDERS)
    adr_pick = pick(clean, ADR_FOLDERS)

    result = {
        "measured_entries": len(measured),
        "clean_unique_entries": len(clean),
        "dropped_as_duplicate_defect": dup_report,
        "control_security": {
            "security": "SAP GY Equity",
            "rationale": "Named directly by the task order text and the CRO's field map; "
                         "NOT read from universe.json (whose own SAP GY row is one of the "
                         "16 defective duplicates, value 'AAPL US').",
        },
        "us_domiciled_pick": us_pick,
        "adr_pick": adr_pick,
    }
    print(json.dumps(result, indent=2))
    print(
        "SELECTED: control=SAP GY Equity | us_name={} | adr={}".format(
            us_pick["security"], adr_pick["security"]
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
