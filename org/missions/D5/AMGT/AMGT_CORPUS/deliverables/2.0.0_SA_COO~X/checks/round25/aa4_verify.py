"""AMGT_CORPUS round 25 CRPS-aa-4 -- the leg-c verify of the BP/NG re-derive. The issuer's file; run as a named script with python -u.

  python -u aa4_verify.py capture <dir>   -> BEFORE the act: the serializing dry run (stage_derive with a write-capturing client)
                                             saves each expected block to <dir>/<encoded>.expected.json, and the served
                                             predecessor's stamp to <dir>/<encoded>.pred.txt
  python -u aa4_verify.py compare <dir>   -> AFTER the act: the newest served block of each name must EQUAL its captured expected
                                             block, with every `vintage` stripped (the derive stamp moves by construction). Against
                                             the predecessor, it must show exactly the pair's counts, and every sign transition's
                                             new label must match its value's sign (CTO condition 2)
  -> 'aa4v <security> new_stamp S equals_dry_run True|False unit U sign G currency C value V m2o X sign_all_match_value B
      case_status P case_value Q'
"""
import json
import os
import subprocess
import sys

import boto3

TOP = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
HERE = os.path.dirname(os.path.abspath(__file__))
B = "opal-data-harvest"
NAMES = {"BP/ LN Equity": "BP-SLASH-_LN_Equity", "NG/ LN Equity": "NG-SLASH-_LN_Equity"}
EXPECT = {"BP-SLASH-_LN_Equity": dict(U=211, G=14, C=0, V=0, X=10), "NG-SLASH-_LN_Equity": dict(U=174, G=4, C=0, V=0, X=0)}


def load_dryrun():
    src = open(os.path.join(HERE, "aa4_dryrun.py"), encoding="utf-8").read().split("real = boto3.client")[0]
    ns = {"__file__": os.path.join(HERE, "aa4_dryrun.py")}
    exec(compile(src, ns["__file__"], "exec"), ns)
    return ns


def newest(s3, enc):
    st = sorted(o["Key"] for o in s3.list_objects_v2(Bucket=B, Prefix="derived/model_block/%s/" % enc).get("Contents", [])
                if o["Key"].endswith("/model_block.json"))
    return st[-1]


def capture(d):
    ns = load_dryrun()
    real = boto3.client("s3")
    os.makedirs(d, exist_ok=True)
    for sec, enc in NAMES.items():
        cap = ns["Capture"](real)
        ns["mbp"].stage_derive(cap, sec, raw_stamp=None, sa_fallback=False)
        blocks = [b for op, k, b in cap.captured if op == "put_object" and str(k).endswith("/model_block.json")]
        assert len(cap.captured) == 1 and len(blocks) == 1, cap.captured
        open(os.path.join(d, enc + ".expected.json"), "wb").write(blocks[0] if isinstance(blocks[0], bytes) else blocks[0].encode())
        open(os.path.join(d, enc + ".pred.txt"), "w").write(newest(real, enc))
        print("CAPTURED %s expected block, predecessor %s" % (enc, newest(real, enc).split("/")[-2]), flush=True)


def compare(d):
    ns = load_dryrun()
    s3 = boto3.client("s3")
    for sec, enc in NAMES.items():
        exp = json.load(open(os.path.join(d, enc + ".expected.json"), encoding="utf-8"))
        pred_key = open(os.path.join(d, enc + ".pred.txt")).read().strip()
        new_key = newest(s3, enc)
        if new_key == pred_key:
            print("aa4v %s NO NEW STAMP -- STOP" % sec)
            continue
        cur = json.loads(s3.get_object(Bucket=B, Key=new_key)["Body"].read())
        old = json.loads(s3.get_object(Bucket=B, Key=pred_key)["Body"].read())
        sv = ns["strip_vintage"]
        eq = json.dumps(sv(cur), sort_keys=True, default=str) == json.dumps(sv(exp), sort_keys=True, default=str)
        of = {ns["fkey"](f): f for f in old["figures"]}
        c = dict(U=0, G=0, C=0, V=0, X=0)
        sign_ok = True
        for f in cur["figures"]:
            a = of.get(ns["fkey"](f))
            if a is None:
                continue
            if a.get("unit") != f.get("unit"):
                c["U"] += 1
                c["X"] += int(ns["measured"](a.get("unit")))
            if a.get("sign") != f.get("sign"):
                c["G"] += 1
                try:
                    v = float(f.get("value"))
                    own = "POSITIVE" if v > 0 else ("NEGATIVE" if v < 0 else "ZERO")
                    sign_ok = sign_ok and str(f.get("sign")).split(" ", 1)[0] == own
                except (TypeError, ValueError):
                    sign_ok = False
            c["C"] += int(a.get("currency") != f.get("currency"))
            c["V"] += int(json.dumps(a.get("value")) != json.dumps(f.get("value")))
        base = (cur.get("cases") or {}).get("base") or {}
        ok = eq and c == EXPECT[enc] and sign_ok
        print("aa4v %s new_stamp %s equals_dry_run %s unit %d sign %d currency %d value %d m2o %d sign_all_match_value %s "
              "case_status %s case_value %s counts_as_pair %s" % (sec, new_key.split("/")[-2], eq, c["U"], c["G"], c["C"], c["V"],
                                                                  c["X"], sign_ok, base.get("status"), base.get("value"),
                                                                  c == EXPECT[enc]), flush=True)
        if not ok:
            print("aa4v %s MISMATCH -- STOP" % sec)


if __name__ == "__main__":
    {"capture": capture, "compare": compare}[sys.argv[1]](sys.argv[2])
