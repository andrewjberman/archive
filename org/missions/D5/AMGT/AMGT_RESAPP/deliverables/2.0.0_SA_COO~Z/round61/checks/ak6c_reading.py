"""AMGT_RESAPP round 61 -- ak-6 act (C), CTO half @b49f4d2db3 condition 4: for the 7 names of the B5 plan, the DEPLOYED
`/security/{key}/thesis` -> `management.ceo_profile_reading` keeps its `reading` (state) and `urls_returned`; only `reason` may change.

  --what pre --out <json>        record each name's reading, urls_returned, reason and ceo_public_profile.basis, off the deployed function
  --what post --pre <json> [--expect-urls KEY=N ...]
                                 re-read and compare: C1 reading equal 7/7; C2 urls_returned equal 7/7 except a named KEY=N; C3 reason and basis now
                                 carry neither "SERP" nor "contract's search" 7/7 (the words reached the reader)
Verdict: AK6C READINGS HOLD AND SPEAK WORDS: YES|NO. Read-only.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys

import boto3

ROOT = "org/missions/D5/AMGT/AMGT_RESAPP/deliverables"
CAPTURE_LIB = ROOT + "/0.9.0_WK_AMGT_RESAPP~158/capture_lib.py"
PLAN = ROOT + "/0.9.0_WK_AMGT_RESAPP~201/m1_ceo_basis_plan.json"
SERP = re.compile(r"SERP|contract's search")


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def _read():
    cl = _load("capture_lib", CAPTURE_LIB)
    lam = boto3.client("lambda", region_name=cl.REGION)
    keys = sorted({e["security_key"] for e in json.load(open(PLAN, encoding="utf-8"))["entries"]})
    out = {}
    for k in keys:
        body, meta = cl._invoke(lam, f"/api/scoped/amgt/security/{k}/thesis")
        mg = (body or {}).get("management") or {}
        rd = mg.get("ceo_profile_reading") or {}
        out[k] = {"status": meta.get("status") if body is None else 200, "reading": rd.get("reading"),
                  "urls_returned": rd.get("urls_returned"), "reason": rd.get("reason"),
                  "basis": (mg.get("ceo_public_profile") or {}).get("basis")}
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--what", choices=("pre", "post"), required=True)
    ap.add_argument("--out")
    ap.add_argument("--pre")
    ap.add_argument("--expect-urls", action="append", default=[], help="KEY=N: a named urls_returned change (the half's correction)")
    a = ap.parse_args()
    expect = {kv.split("=", 1)[0]: (None if kv.split("=", 1)[1] in ("None", "null") else int(kv.split("=", 1)[1])) for kv in a.expect_urls}
    now = _read()
    if a.what == "pre":
        json.dump(now, open(a.out, "w", encoding="utf-8"), indent=1)
        for k, v in now.items():
            print(f"pre {k}: reading={v['reading']} urls_returned={v['urls_returned']} basis={str(v['basis'])[:70]!r}")
        return 0
    pre = json.load(open(a.pre, encoding="utf-8"))
    ok = []

    def clause(name, cond, detail=""):
        ok.append(bool(cond))
        print(f"{'PASS' if cond else 'FAIL'} {name} {detail}")

    keys = sorted(pre)
    same_state = [k for k in keys if now.get(k, {}).get("reading") == pre[k]["reading"]]
    same_urls = [k for k in keys if now.get(k, {}).get("urls_returned") == (expect[k] if k in expect else pre[k]["urls_returned"])]
    worded = [k for k in keys if not SERP.search(str(now.get(k, {}).get("reason") or "")) and not SERP.search(str(now.get(k, {}).get("basis") or ""))]
    clause("C1 every reading state unchanged", len(same_state) == len(keys), f"{len(same_state)} of {len(keys)}")
    clause("C2 every urls_returned unchanged, or equal to its named --expect-urls value", len(same_urls) == len(keys),
           f"{len(same_urls)} of {len(keys)}; named changes {expect}")
    clause("C3 reason and basis speak words", len(worded) == len(keys), f"{len(worded)} of {len(keys)}")
    for k in keys:
        print(f"   {k}: {pre[k]['reading']} -> {now.get(k, {}).get('reading')} | urls {pre[k]['urls_returned']} -> {now.get(k, {}).get('urls_returned')} | reason {str(now.get(k, {}).get('reason'))[:60]!r}")
    print(f"AK6C READINGS HOLD AND SPEAK WORDS: {'YES' if all(ok) else 'NO'}")
    return 0 if all(ok) else 1


if __name__ == "__main__":
    sys.exit(main())
