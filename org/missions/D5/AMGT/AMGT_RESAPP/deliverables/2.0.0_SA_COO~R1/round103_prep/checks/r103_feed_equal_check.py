"""AMGT_RESAPP round-103 PREP -- the overlay's feed and news card read ONLY the subject's rows, and every served byte stays equal (`AMGT-bj-1`).

  PYTHONPATH=<repo root> python r103_feed_equal_check.py [--candidate-file <path to a scoped_amgt.py>]

BASE is the merged blob `02627c18a0ea` of `lib/research/api/scoped_amgt.py` (the live package's, after round 102), read with `git cat-file blob` and loaded as its own module. CANDIDATE is the
checkout's `lib.research.api.scoped_amgt` (or `--candidate-file`, used for the dry-run at the base). READ-ONLY on the live pool (S3 reads; no function invoke, no write).
THE SAMPLE (deterministic, printed): `ASML_NA_Equity`; four keys drawn from the covered universe that HAVE mention rows, ordered by sha256(key + ':r103'); and ONE NEGATIVE CONTROL, a covered key
with NO mention row (the same ordering), or, when every covered key has mentions, the unresolved key `ZZZZ_XX_Equity`. Arms, in ONE process for the byte arms, then ONE fresh process each for R4:
  R1  per subject, the overlay's status and body are byte-equal between base and candidate
  R2  per subject, the body's `feed` and `top_band` sections are byte-equal (the two sections the change touches)
  R3  the negative control's overlay (its empty feed answer) is byte-equal, and its feed `item_count` is 0
  R4  in a FRESH process, after one overlay request, the candidate holds NO whole-snapshot cache entry for `article_security_mention` and DOES hold the column-scoped one; the base holds the
      whole-snapshot entry (the control: the instrument can tell the two reads apart)
  R5  the candidate's `AMGT_PHASE route=overlay phase=feed` and `top_band` lines are present (bj-1 keeps the round-102 lines)
Local timings are printed for information (base and candidate feed phase, fresh process each) and NOT graded: local timings did not transfer to Lambda in rounds 99 and 100.
Verdict `R103 FEED EQUAL: YES|NO`, exit 0 on YES. Writes nothing.
"""
import contextlib
import hashlib
import importlib.util
import io
import json
import os
import subprocess
import sys
import tempfile

BASE_BLOB = "02627c18a0ea"
TABLE = "article_security_mention"


def event(key, leaf="overlay"):
    return {"rawPath": "/api/scoped/amgt/security/%s/%s" % (key, leaf), "queryStringParameters": None, "requestContext": {"http": {"method": "GET"}}, "headers": {"x-firm-id": "opal"}}


def load_file(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def call(mod, key):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        resp = mod.handler(event(key))
    return resp, buf.getvalue()


def sections(resp):
    try:
        body = json.loads(resp.get("body") or "{}")
    except Exception:  # noqa: BLE001
        return None, None, {}
    feed = json.dumps(body.get("feed"), sort_keys=True)
    band = json.dumps(body.get("top_band"), sort_keys=True)
    return feed, band, body


def draw(keys, salt):
    return sorted(keys, key=lambda k: hashlib.sha256((k + salt).encode()).hexdigest())


CHILD = r"""
import contextlib, io, json, re, sys
sys.path.insert(0, ".")
which = sys.argv[1]
key = sys.argv[2]
if which == "base":
    import importlib.util
    spec = importlib.util.spec_from_file_location("scoped_amgt_base", sys.argv[3])
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
elif which == "candidate_file":
    import importlib.util
    spec = importlib.util.spec_from_file_location("scoped_amgt_candidate", sys.argv[3])
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
else:
    from lib.research.api import scoped_amgt as mod
from lib.research.harvest import publication_gold as pg
ev = {"rawPath": "/api/scoped/amgt/security/%s/overlay" % key, "queryStringParameters": None,
      "requestContext": {"http": {"method": "GET"}}, "headers": {"x-firm-id": "opal"}}
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    resp = mod.handler(ev)
ph = dict(re.findall(r"phase=(\S+) ms=(\d+)", buf.getvalue()))
cache = list(pg._GOLD_SNAPSHOT_CACHE.keys())
whole = "article_security_mention" in cache
scoped = any(isinstance(k, tuple) and k and k[0] == "article_security_mention" for k in cache)
print(json.dumps({"status": resp.get("statusCode"), "whole_cache": whole, "scoped_cache": scoped, "feed_ms": ph.get("feed"), "top_band_ms": ph.get("top_band"),
                  "has_feed_line": "feed" in ph, "has_top_band_line": "top_band" in ph}))
"""


def child(which, key, path=None):
    args = [sys.executable, "-c", CHILD, which, key] + ([path] if path else [])
    out = subprocess.run(args, capture_output=True, text=True, cwd=os.getcwd(), env=dict(os.environ, PYTHONPATH=os.getcwd()))
    for line in reversed(out.stdout.strip().splitlines()):
        if line.startswith("{"):
            return json.loads(line)
    return {"error": (out.stderr or out.stdout)[-300:]}


def main(argv):
    base_src = subprocess.run(["git", "cat-file", "blob", BASE_BLOB], capture_output=True, check=True).stdout
    tmp = tempfile.mkdtemp(prefix="r103base_")
    base_path = os.path.join(tmp, "scoped_amgt_base.py")
    with open(base_path, "wb") as fh:
        fh.write(base_src)
    cand_file = argv[argv.index("--candidate-file") + 1] if "--candidate-file" in argv else None
    base = load_file("scoped_amgt_base", base_path)
    cand = load_file("scoped_amgt_candidate", cand_file) if cand_file else __import__("lib.research.api.scoped_amgt", fromlist=["x"])

    from lib.research.coverage.covered_universe import covered_security_keys
    from lib.research.harvest import publication_gold as pg

    covered = sorted(covered_security_keys())
    rows = pg._latest_gold_snapshot_rows_cached(TABLE, columns=("security_key",))
    mentioned = {r.get("security_key") for r in rows}
    with_mentions = [k for k in covered if k in mentioned and k != "ASML_NA_Equity"]
    without = [k for k in covered if k not in mentioned]
    sample = ["ASML_NA_Equity"] + draw(with_mentions, ":r103")[:4]
    negative = draw(without, ":r103")[0] if without else "ZZZZ_XX_Equity"
    print("covered %d | with mention rows %d | without %d | sample %s | negative control %s%s" % (
        len(covered), len(with_mentions) + 1, len(without), sample, negative, "" if without else " (synthetic: every covered key has mentions)"))

    arms = []

    def arm(name, ok, detail=""):
        arms.append((name, ok))
        print("   %s %s %s" % ("PASS" if ok else "FAIL", name, detail))

    for key in sample + [negative]:
        b_resp, _ = call(base, key)
        c_resp, c_out = call(cand, key)
        same = b_resp.get("statusCode") == c_resp.get("statusCode") and b_resp.get("body") == c_resp.get("body")
        arm("R1 %s overlay status and body byte-equal" % key, same, "status %s/%s bytes %d/%d" % (b_resp.get("statusCode"), c_resp.get("statusCode"),
            len(b_resp.get("body") or ""), len(c_resp.get("body") or "")))
        bf, bb, _ = sections(b_resp)
        cf, cb, cbody = sections(c_resp)
        arm("R2 %s feed and top_band sections byte-equal" % key, bf is not None and bf == cf and bb == cb, "feed items %s" % ((cbody.get("feed") or {}).get("item_count")))
        if key == negative:
            arm("R3 negative control: empty feed answer equal, item_count 0", same and (cbody.get("feed") or {}).get("item_count") == 0,
                "coverage_status %s" % ((cbody.get("feed") or {}).get("coverage_status")))
        if key == "ASML_NA_Equity":
            arm("R5 the candidate prints the feed and top_band phase lines", "phase=feed" in c_out and "phase=top_band" in c_out)

    b = child("base", "ASML_NA_Equity", base_path)
    c = child("candidate_file" if cand_file else "candidate", "ASML_NA_Equity", cand_file)
    arm("R4a the base holds the WHOLE-snapshot cache entry (control)", b.get("whole_cache") is True, str(b))
    arm("R4b the candidate holds NO whole-snapshot entry and holds the column-scoped one", c.get("whole_cache") is False and c.get("scoped_cache") is True, str(c))
    print("local timings, not graded: feed phase base %s ms, candidate %s ms (fresh process each)" % (b.get("feed_ms"), c.get("feed_ms")))
    passed = sum(1 for _, ok in arms if ok)
    print("   arms passed %d of %d" % (passed, len(arms)))
    verdict = "YES" if passed == len(arms) else "NO"
    print("R103 FEED EQUAL: %s" % verdict)
    return 0 if verdict == "YES" else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
