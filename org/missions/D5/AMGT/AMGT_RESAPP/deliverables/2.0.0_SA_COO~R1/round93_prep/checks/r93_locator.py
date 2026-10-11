"""AMGT_RESAPP round-93 PREP -- the round-91 locator check, re-based on the mixed-scale rule (D1-S22): a locator arm asks about ONE point.

Round 91's L3, L4 and K1 read SAP's three points out of the production re-verification of the whole set. Round 93's `AMGT-ss-2` holds that set
WHOLE (2023 and 2024 are stated "million", 2025 "billion"), so those three arms, as written, assert the very defect ss-2 removes. They now ask the
locator about ONE point at a time (a single point has a single scale, so the set rule never applies), and a new arm L5 asserts the production
re-verification of SAP holds all three with a reason naming both scales. Every other arm is round 91's, unchanged.

  PYTHONPATH=<repo root> python r93_locator.py

The production path is `lib/research/filings/analyze.py::_apply_point_verification(points, excerpt_text, passage_map, anchor)` -- the
SAME function a fresh run and `reverify_stored_thesis_driver` take. This check runs `reverify_stored_thesis_driver(.., dry_run=True)`
(it writes nothing) for the three names, and for the refusal arms calls `_apply_point_verification` on the SAME silver source
excerpt, passage map and anchor the dry-run uses. Read-only: S3 GETs and silver reads only.

  L1..L4  the four LOCATOR points verify, each with a span INSIDE the excerpt whose text carries the value:
            L1 BABA `FY2025` 118,028 and L2 BABA `FY2026` 158,132 (the filing prints the period as `2025` / `2026`);
            L3 SAP `2023` 13,745 (`(2023: <euro sign>13,745 million)`, an inline prior-period parenthetical);
            L4 SAP `2025` 21.05 (`<euro sign>21.05 billion in 2025`, a decimal).
  E1      PBR `2025` 2.99 mboed stays HELD (its value is in no part of its excerpt), with a reason.
  K1      control: SAP `2024` 18,078, asked ALONE, verifies with span [129709, 129715] and the stored passage id.
  L5      the production re-verification of SAP holds all three points (none kept) under a reason naming both scales.
  X1..X7  the refusals that make the fix a locator and not a text search -- each is a point the filing does NOT state for that period:
            X1 BABA FY2025 = 158,132 (FY2026's figure)        X2 BABA FY2026 = 118,028 (FY2025's figure)
            X3 SAP 2025 = 18.08 (2024's figure, in the same sentence)   X4 SAP 2025 = 21.5 (not 21.05)   X5 SAP 2025 = 1.05 (a suffix of 21.05)
            X6 BABA FY2019 = 118,028 (a period the excerpt never labels)  X7 SAP 2023 = 18,078 (2024's figure, same sentence)
Verdict: R93 LOCATOR: YES|NO (exit 0|1). At the base (2026-10-11) L5 FAILs (the set is kept) and every other arm PASSes.
"""
import copy
import json
import sys

import boto3

from lib.research.filings import analyze

BUCKET = "opal-data-harvest"
CASES = {
    "BABA_US_Equity": "000119312526231755",
    "PBR_US_Equity": "000129281426002168",
    "SAP_GY_Equity": "000110465926020058",
}
_S3 = boto3.client("s3", region_name="us-east-1")


def get(key):
    return json.loads(_S3.get_object(Bucket=BUCKET, Key=key)["Body"].read())


def silver_source(name, acc):
    """The filing source the production re-verification reads (silver `filing_source`), as reverify_stored_thesis_driver does."""
    from lib.research.harvest import filings as hf
    from lib.research.harvest import store as hstore

    for vendor in ("sec", "issuer-site"):
        latest = hstore.silver_latest(vendor, "filing_source", ("security_key", "accession"), client=_S3)
        row = latest.get((name, acc))
        if row is not None:
            return hf.source_object_from_row(row)
    raise RuntimeError("no silver filing_source row for %s %s" % (name, acc))


def load(name):
    acc = CASES[name]
    src = silver_source(name, acc)
    ana = get("filings/v1/%s/%s.analysis.json" % (name, acc))
    driver = ana["thesis_driver"]
    claimed = driver.get("source_passage_id")
    passage_map = ana["passage_map"]
    anchor = next((p["start"] for p in passage_map if p["id"] == claimed), 0)
    emitted = []
    for p in list(driver.get("points") or []) + list(driver.get("held_uncited") or []):
        emitted.append({"period": p["period"], "value": p["value"]})
    return {"text": src["excerpt"]["text"], "passage_map": passage_map, "anchor": anchor, "emitted": emitted,
            "stored_points": driver.get("points") or [], "name": name, "acc": acc}


def production_dry_run(name):
    """(kept map, held map) from the production re-verification, dry-run (nothing written)."""
    doc, _key, _receipt = analyze.reverify_stored_thesis_driver(name, CASES[name], client=_S3, dry_run=True)
    d = doc["thesis_driver"]
    return {p["period"]: p for p in d["points"]}, {p["period"]: p for p in d["held_uncited"]}


def verify(case, points):
    kept, held = analyze._apply_point_verification(
        copy.deepcopy(points), case["text"], copy.deepcopy(case["passage_map"]), anchor=case["anchor"])
    return kept, held


def say(ok, label, detail=""):
    print("%s %s%s" % ("PASS" if ok else "FAIL", label, ("  [" + detail + "]") if detail else ""))
    return ok


def main():
    data = {n: load(n) for n in CASES}
    res = []

    def holds_value(name, entry):
        s, e = entry["span"]
        return 0 <= s < e <= len(data[name]["text"])

    runs = {n: production_dry_run(n) for n in CASES}
    # L1, L2
    kept, held = runs["BABA_US_Equity"]
    for per, val, tag in (("FY2025", 118028, "L1"), ("FY2026", 158132, "L2")):
        e = kept.get(per)
        ok = bool(e) and e["value"] == val and holds_value("BABA_US_Equity", e)
        res.append(say(ok, "%s BABA %s %s verifies with a span inside the excerpt" % (tag, per, format(val, ",")),
                       ("span %s" % e.get("span")) if e else "held: %s" % (held.get(per) or {}).get("reason")))
    # L3, L4, K1
    kept, held = runs["SAP_GY_Equity"]
    sap = data["SAP_GY_Equity"]
    k3, h3 = verify(sap, [{"period": "2023", "value": 13745}])
    e = k3[0] if k3 else None
    res.append(say(bool(e) and e["value"] == 13745 and holds_value("SAP_GY_Equity", e),
                   "L3 SAP 2023 13,745 (inline prior-period parenthetical), asked alone, verifies",
                   ("span %s" % e.get("span")) if e else "held: %s" % (h3[0].get("reason") if h3 else None)))
    k4, h4 = verify(sap, [{"period": "2025", "value": 21.05}])
    e = k4[0] if k4 else None
    res.append(say(bool(e) and e["value"] == 21.05 and holds_value("SAP_GY_Equity", e),
                   "L4 SAP 2025 21.05 (a decimal), asked alone, verifies",
                   ("span %s" % e.get("span")) if e else "held: %s" % (h4[0].get("reason") if h4 else None)))
    stored = {p["period"]: p for p in sap["stored_points"]}
    k1, _h1 = verify(sap, [{"period": "2024", "value": 18078}])
    e = k1[0] if k1 else None
    res.append(say(bool(e) and e.get("span") == stored["2024"]["span"] == [129709, 129715]
                   and e.get("passage_id") == stored["2024"]["passage_id"],
                   "K1 control: SAP 2024 18,078, asked alone, keeps its stored span and passage", "span %s" % (e or {}).get("span")))
    reasons = " | ".join(str((h or {}).get("reason")) for h in held.values()).lower()
    res.append(say(not kept and sorted(held) == ["2023", "2024", "2025"] and "million" in reasons and "billion" in reasons,
                   "L5 the production re-verification of SAP holds all three points under a reason naming both scales",
                   "kept %s, held %s" % (sorted(kept), sorted(held))))
    # E1
    kept, held = runs["PBR_US_Equity"]
    h = held.get("2025")
    res.append(say("2025" not in kept and bool(h) and bool(h.get("reason")),
                   "E1 PBR 2025 2.99 mboed stays held with a reason", "reason: %s" % (h or {}).get("reason")))
    # X1..X7
    def refused(name, period, value):
        c = data[name]
        k, hld = verify(c, [{"period": period, "value": value}])
        return not k and len(hld) == 1

    arms = [
        ("X1 BABA FY2025 = 158,132 (FY2026's figure) is refused", "BABA_US_Equity", "FY2025", 158132),
        ("X2 BABA FY2026 = 118,028 (FY2025's figure) is refused", "BABA_US_Equity", "FY2026", 118028),
        ("X3 SAP 2025 = 18.08 (2024's figure, same sentence) is refused", "SAP_GY_Equity", "2025", 18.08),
        ("X4 SAP 2025 = 21.5 (not 21.05) is refused", "SAP_GY_Equity", "2025", 21.5),
        ("X5 SAP 2025 = 1.05 (a suffix of 21.05) is refused", "SAP_GY_Equity", "2025", 1.05),
        ("X6 BABA FY2019 = 118,028 (a period the excerpt never labels) is refused", "BABA_US_Equity", "FY2019", 118028),
        ("X7 SAP 2023 = 18,078 (2024's figure, same sentence) is refused", "SAP_GY_Equity", "2023", 18078),
    ]
    for label, name, period, value in arms:
        res.append(say(refused(name, period, value), label))

    print("   arms passed %d of %d" % (sum(1 for r in res if r), len(res)))
    ok = all(res)
    print("R93 LOCATOR: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
