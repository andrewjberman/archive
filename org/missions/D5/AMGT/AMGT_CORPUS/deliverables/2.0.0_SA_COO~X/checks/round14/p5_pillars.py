"""AMGT_CORPUS round 14, CRPS-p-5 -- the thesis pillars continuation.build() produces (NO write) for ML_FP_Equity (row
Z-W1-S16) and two controls: IMB_LN_Equity (docx) and ADBE_US_Equity (PDF-only). Read-only; the issuer's file.

  -> 'p5 <key> pillars N empty_text E | ...'  or  '<key> ABSENT reason <reason>' for a field served ABSENT
"""
from lib.research.corpus import continuation

KEYS = ("ML_FP_Equity", "IMB_LN_Equity", "ADBE_US_Equity")


def describe(key):
    field = continuation.build(key)["fields"]["thesis_pillars"]
    if isinstance(field, dict) and field.get("value") is None:
        return "%s ABSENT reason %s" % (key, field.get("absent"))
    items = field if isinstance(field, list) else field.get("value") or []
    empty = sum(1 for p in items if not (p.get("text") or "").strip())
    return "%s pillars %d empty_text %d" % (key, len(items), empty)


print("p5 " + " | ".join(describe(k) for k in KEYS))
