"""AMGT_CORPUS round 25 CRPS-aa-4 -- the SERIALIZING DRY RUN of the BP/NG re-derive (standing ruling 3): the producer's own
`model_block_pull.stage_derive` runs with a client that passes every READ through to S3 and CAPTURES every write instead of making
it. The captured block is diffed against the served predecessor on EVERYTHING -- top-level keys, `cases`, and each figure's
unit / sign / currency / value / other fields. The derive `vintage` stamp is counted separately. Writes NOTHING. The issuer's file;
run as a named script with python -u.

  python -u aa4_dryrun.py "BP/ LN Equity" "NG/ LN Equity"
  -> 'WRITE-ATTEMPT <op> <key>' per captured write
  -> 'TOP <key> changed' / 'CASES changed <paths>' / 'FIG ...' transitions
  -> 'aa4 <security> writes W figures F unit U sign S currency C value V other O measured_to_other X top T cases K vintage_only VT'
"""
import collections
import importlib.util
import json
import os
import subprocess
import sys

import boto3

TOP = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
RES = os.path.join(TOP, "integrations", "bloomberg", "research")
B = "opal-data-harvest"
WRITES = {"put_object", "copy_object", "delete_object", "delete_objects", "upload_file", "upload_fileobj"}


class Capture:
    """Reads go to the real client; any write is captured and never sent."""

    def __init__(self, real):
        self._real = real
        self.captured = []

    def __getattr__(self, name):
        if name in WRITES:
            def cap(*a, **kw):
                body = kw.get("Body")
                if hasattr(body, "read"):
                    body = body.read()
                self.captured.append((name, kw.get("Key"), body))
                return {"ETag": '"dry-run"'}
            return cap
        return getattr(self._real, name)


spec = importlib.util.spec_from_file_location("mbp_aa4", os.path.join(RES, "model_block_pull.py"))
mbp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mbp)
from lib.research.identity import crosswalk  # noqa: E402


def fkey(f):
    return (f.get("mnemonic"), f.get("scope"), f.get("fiscal_period"), f.get("fiscal_year"), f.get("period_end_date"),
            f.get("override"))


def strip_vintage(x):
    if isinstance(x, dict):
        return {q: strip_vintage(w) for q, w in x.items() if q != "vintage"}
    if isinstance(x, list):
        return [strip_vintage(w) for w in x]
    return x


def measured(u):
    u = str(u or "")
    return bool(u) and not u.startswith("UNRESOLVED") and not u.startswith("SEE field_map")


def paths(x, y, p, out):
    if isinstance(x, dict) and isinstance(y, dict):
        for q in set(x) | set(y):
            paths(x.get(q), y.get(q), p + "." + q, out)
    elif json.dumps(x, sort_keys=True, default=str) != json.dumps(y, sort_keys=True, default=str):
        out.append(p)


real = boto3.client("s3")
for security in sys.argv[1:]:
    cap = Capture(real)
    mbp.stage_derive(cap, security, raw_stamp=None, sa_fallback=False)
    blocks = [(k, b) for op, k, b in cap.captured if op == "put_object" and str(k).endswith("/model_block.json")]
    for op, k, _ in cap.captured:
        print("WRITE-ATTEMPT %s %s" % (op, k), flush=True)
    if len(blocks) != 1:
        print("aa4 %s writes %d model_block_captured %d -- STOP" % (security, len(cap.captured), len(blocks)))
        continue
    new = json.loads(blocks[0][1])
    enc = crosswalk.slash_safe_key(security.replace(" ", "_"))
    st = sorted(o["Key"] for o in real.list_objects_v2(Bucket=B, Prefix="derived/model_block/%s/" % enc).get("Contents", [])
                if o["Key"].endswith("model_block.json"))
    old = json.loads(real.get_object(Bucket=B, Key=st[-1])["Body"].read())
    tops = sorted(q for q in (set(old) | set(new)) - {"figures", "cases"}
                  if json.dumps(old.get(q), sort_keys=True, default=str) != json.dumps(new.get(q), sort_keys=True, default=str))
    for q in tops:
        print("TOP %s changed: %s -> %s" % (q, json.dumps(old.get(q), default=str)[:120], json.dumps(new.get(q), default=str)[:120]))
    cp = []
    paths(strip_vintage(old.get("cases")), strip_vintage(new.get("cases")), "cases", cp)
    if cp:
        print("CASES changed %s" % " ".join(sorted(cp)[:20]))
    of = {fkey(f): f for f in old.get("figures", [])}
    nf = {fkey(f): f for f in new.get("figures", [])}
    c = collections.Counter()
    trans = collections.Counter()
    for kk in set(of) | set(nf):
        a, b = of.get(kk), nf.get(kk)
        if a is None or b is None:
            c["O"] += 1
            trans["figure %s %s" % ("added" if a is None else "removed", kk[0])] += 1
            continue
        if a.get("unit") != b.get("unit"):
            c["U"] += 1
            c["X"] += int(measured(a.get("unit")))
        c["S"] += int(a.get("sign") != b.get("sign"))
        if a.get("currency") != b.get("currency"):
            c["C"] += 1
            trans["currency %s %s->%s" % (kk[0], a.get("currency"), b.get("currency"))] += 1
        c["V"] += int(json.dumps(a.get("value")) != json.dumps(b.get("value")))
        c["VT"] += int(a.get("vintage") != b.get("vintage"))
        skip = ("unit", "sign", "value", "vintage", "currency", "currency_basis")
        ra = {q: w for q, w in a.items() if q not in skip}
        rb = {q: w for q, w in b.items() if q not in skip}
        if json.dumps(ra, sort_keys=True, default=str) != json.dumps(rb, sort_keys=True, default=str):
            c["O"] += 1
            trans["other-fields %s %s" % (kk[0], sorted(q for q in set(ra) | set(rb) if ra.get(q) != rb.get(q)))] += 1
    for t, n in sorted(trans.items()):
        print("FIG %s %d" % (t, n))
    print("aa4 %s predecessor %s writes %d figures %d unit %d sign %d currency %d value %d other %d measured_to_other %d top %d "
          "cases %d vintage_only %d" % (security, st[-1].split("/")[-2], len(cap.captured), len(nf), c["U"], c["S"], c["C"],
                                        c["V"], c["O"], c["X"], len(tops), len(cp), c["VT"]), flush=True)
