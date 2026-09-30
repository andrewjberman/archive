"""AMGT_CORPUS round 26, CRPS-ab-3 (analysis ruling 3) -- case_rule refuses a constructed INPUT, not only the value, when quote and
reporting currencies differ beyond the GBp/GBP unit factor. The producer's own `stage_derive` runs for BP/ LN and NG/ LN with a
client that passes reads through and CAPTURES writes (nothing is written); the captured block's `cases.base` is read. Also the
scoped API's own path: `case_rule.compute_cases` is what `/thesis` calls per request. The issuer's file.

  -> 'ab3 bp_status S bp_trailing_input V bp_input_reason_set True|False ng_status S ng_value V'
"""
import importlib.util
import json
import os
import subprocess

import boto3

TOP = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
RES = os.path.join(TOP, "integrations", "bloomberg", "research")
WRITES = {"put_object", "copy_object", "delete_object", "delete_objects", "upload_file", "upload_fileobj"}


class Capture:
    def __init__(self, real):
        self._real = real
        self.captured = []

    def __getattr__(self, name):
        if name in WRITES:
            def cap(*a, **kw):
                body = kw.get("Body")
                self.captured.append((name, kw.get("Key"), body.read() if hasattr(body, "read") else body))
                return {"ETag": '"dry-run"'}
            return cap
        return getattr(self._real, name)


spec = importlib.util.spec_from_file_location("mbp_ab3", os.path.join(RES, "model_block_pull.py"))
mbp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mbp)
real = boto3.client("s3")
bases = {}
for sec in ("BP/ LN Equity", "NG/ LN Equity"):
    cap = Capture(real)
    mbp.stage_derive(cap, sec, raw_stamp=None, sa_fallback=False)
    blk = json.loads([b for op, k, b in cap.captured if op == "put_object" and str(k).endswith("/model_block.json")][0])
    bases[sec] = (blk.get("cases") or {}).get("base") or {}
bp, ng = bases["BP/ LN Equity"], bases["NG/ LN Equity"]
tm = (bp.get("inputs") or {}).get("trailing_median_pe")
tm_value = tm.get("value") if isinstance(tm, dict) else tm
tm_reason = bool(isinstance(tm, dict) and str(tm.get("reason") or "").strip())
ngv = ng.get("value")
print("ab3 bp_status %s bp_trailing_input %s bp_input_reason_set %s ng_status %s ng_value %s" % (
    bp.get("status"), "null" if tm_value is None else round(float(tm_value), 2), tm_reason, ng.get("status"),
    None if ngv is None else round(float(ngv), 2)))
