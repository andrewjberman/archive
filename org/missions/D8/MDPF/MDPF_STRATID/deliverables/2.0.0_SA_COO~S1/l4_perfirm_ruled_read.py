"""MDPF_STRATID L4 -- the CTO-ruled per-firm prior-frontier read (@5a151aacea).

Read-only S3. For each per-firm served aggregate-aua-timeseries it diffs POST (prev -> new key) against the CONTROL (the prior pair
written by the old code):
  1  every moved key family also moved in the control;
  2  no move on a date before the prior frontier date;
  3  49financial by_model deltas sum to the model_aua delta (a cent).
Edit PAIRS below to read another fire. Prints data only; the grade is written in the read page.

usage: python -I l4_perfirm_ruled_read.py
"""
from __future__ import annotations

import json

import boto3

B = "opal-data-assets"
FIRMS = ("49financial", "inflection", "cottonwood")
PAIRS = {"CONTROL": ("2026-10-07", "2026-10-08"), "POST": ("2026-10-08", "2026-10-09")}
S3 = boto3.client("s3")


def _key(firm, day):
    return "portal/gold/mdpf/%s/aggregate-aua-timeseries/%s.json" % (firm, day)


def get(firm, day):
    return json.loads(S3.get_object(Bucket=B, Key=_key(firm, day))["Body"].read())


def written(firm, day):
    return S3.head_object(Bucket=B, Key=_key(firm, day))["LastModified"].strftime("%m-%d %H:%MZ")


def differs(a, b):
    if (a is None) != (b is None):
        return True
    return isinstance(a, (int, float)) and isinstance(b, (int, float)) and abs(a - b) > 0.01


def moves(old, new):
    """Return (family, key, date, old value, new value) rows for every common-date cell that moved."""
    od = {d: i for i, d in enumerate(old["dates"])}
    nd = {d: i for i, d in enumerate(new["dates"])}
    common = [d for d in old["dates"] if d in nd]
    out = []
    for k, v in new.items():
        ov = old.get(k)
        if isinstance(v, list) and len(v) == len(new["dates"]) and isinstance(ov, list) and len(ov) == len(old["dates"]):
            for d in common:
                if differs(ov[od[d]], v[nd[d]]):
                    out.append(("top:" + k, k, d, ov[od[d]], v[nd[d]]))
    for m, e in (new.get("by_model") or {}).items():
        oe = (old.get("by_model") or {}).get(m)
        if not oe:
            out.append(("by_model", m, "(new member)", None, None))
            continue
        for f in ("model_value", "account_count"):
            if f in e and f in oe:
                for d in common:
                    if differs(oe[f][od[d]], e[f][nd[d]]):
                        out.append(("by_model." + f, m, d, oe[f][od[d]], e[f][nd[d]]))
    return out


def report(tag, firm, d_old, d_new):
    old, new = get(firm, d_old), get(firm, d_new)
    mv = moves(old, new)
    frontier = old["dates"][-1]
    fam = sorted({m[0] for m in mv})
    early = [m for m in mv if m[2] != frontier]
    print("%-8s %-12s %s(%s) -> %s(%s) | prior frontier %s | moves %d | families %s | dates %s | moves BEFORE frontier: %d"
          % (tag, firm, d_old, written(firm, d_old), d_new, written(firm, d_new), frontier, len(mv), fam,
             sorted({m[2] for m in mv}), len(early)))
    return mv, set(fam)


def main():
    for firm in FIRMS:
        print("---", firm)
        _, cfam = report("CONTROL", firm, *PAIRS["CONTROL"])
        pmv, pfam = report("POST", firm, *PAIRS["POST"])
        print("   post families not in control:", sorted(pfam - cfam))
        if firm == "49financial":
            aua = [(m[3], m[4]) for m in pmv if m[0] == "top:model_aua"]
            d_aua = sum(b - a for a, b in aua) if aua else None
            d_bm = sum(m[4] - m[3] for m in pmv if m[0] == "by_model.model_value" and m[3] is not None and m[4] is not None)
            print("   model_aua delta %s | by_model model_value delta sum %s | diff %s"
                  % (d_aua, round(d_bm, 2), None if d_aua is None else round(d_aua - d_bm, 4)))


if __name__ == "__main__":
    main()
