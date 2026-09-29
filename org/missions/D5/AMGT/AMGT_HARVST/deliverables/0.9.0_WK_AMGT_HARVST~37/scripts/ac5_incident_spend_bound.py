#!/usr/bin/env python3
"""HVST-w-2 AC5 (guard c) -- the 00:21Z incident's Kimi spend, as a LEDGERED UPPER BOUND from LOCAL evidence.

Inputs (local only): the incident's run.log and screenshots under .scratch/auth/<stamp>-sa-*/ and the harvester
source org/tier1_exec/4.0.0_SA_CRO/scripts/sa_harvest_session.py. The ONLY network read is ONE unauthenticated GET of
Moonshot's PUBLIC pricing page (no key, no account, no API). NO call to api.moonshot.ai and no console / usage
endpoint. If the page cannot be read or carries no kimi-k3 row, the rate is recorded UNMEASURED and the call/token
bound stands; AC5 still passes. The provider-read figure is recorded NOT MEASURED (an account-holder item).

HVST_W2_STUB=1: canned pricing page, no network, scratch ledger (development arm).
"""
import datetime
import glob
import hashlib
import math
import os
import re
import struct
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
DELIV = HERE.parent
REPO = HERE.parents[7]
STUB = os.environ.get("HVST_W2_STUB") == "1"
SEAT = "0.9.0_WK_AMGT_HARVST~37"
PRICING_URL = "https://platform.moonshot.ai/docs/pricing/chat"
if STUB:
    SCR = REPO / ".scratch" / "w2_stub"
    SCR.mkdir(parents=True, exist_ok=True)
    LEDGER = SCR / "VENDOR_CALLS_STUB.md"
    OUTDIR = SCR
else:
    LEDGER = REPO / "org/missions/D5/AMGT/AMGT_HARVST/ledger/VENDOR_CALLS_0.9.0_WK_AMGT_HARVST_37.md"
    OUTDIR = DELIV
HEADER = "## INCIDENT 1 SPEND -- ESTIMATE-UPPER-BOUND"
# ASSUMPTIONS (labelled, conservative, not measured): the tokens one screenshot may cost and the prompt text.
IMAGE_TOKEN_CAP = 4096
PROMPT_TOKENS = 500


def png_dims(path):
    with open(path, "rb") as fh:
        head = fh.read(24)
    return struct.unpack(">II", head[16:24]) if head[:8] == b"\x89PNG\r\n\x1a\n" else (None, None)


def read_pricing():
    """ONE unauthenticated GET; returns a dict describing exactly what happened."""
    at = datetime.datetime.now(datetime.timezone.utc).isoformat()
    if STUB:
        body = b"<html><body><table><tr><td>kimi-k3</td><td>$0.60 / 1M</td><td>$2.50 / 1M</td><td>$3.00 / 1M</td></tr></table></body></html>"
        return {"url": PRICING_URL, "read_at": at, "http_status": 200, "bytes": len(body), "body": body, "stub": True}
    req = urllib.request.Request(PRICING_URL, headers={"User-Agent": "Mozilla/5.0 (HVST-w-2 AC5 public pricing read)"})
    try:
        with urllib.request.urlopen(req, timeout=25) as resp:  # noqa: S310 -- fixed https URL, no credential, ONE read
            body = resp.read()
            return {"url": PRICING_URL, "read_at": at, "http_status": resp.status, "bytes": len(body), "body": body}
    except Exception as exc:
        return {"url": PRICING_URL, "read_at": at, "http_status": None, "bytes": 0, "body": b"",
                "error": "%s: %s" % (type(exc).__name__, str(exc)[:160])}


def rate_from(page):
    """Upper-bound $/1M-token figure from the kimi-k3 row, or None (UNMEASURED). Takes the MAX dollar figure found
    within a window around the first 'kimi-k3' occurrence and applies it to input AND output tokens, so a mixed window
    over-states the bound rather than under-states it."""
    text = page["body"].decode("utf-8", "replace")
    text = re.sub(r"<script.*?</script>|<style.*?</style>", " ", text, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    m = re.search(r"kimi-k3", text, re.I)
    if not m:
        return None, "no 'kimi-k3' text in the page (status %s, %d bytes)" % (page["http_status"], page["bytes"])
    window = text[max(0, m.start() - 100): m.end() + 500]
    nums = [float(x) for x in re.findall(r"\$\s*([0-9]+(?:\.[0-9]+)?)", window)]
    if not nums:
        return None, "'kimi-k3' found but no dollar figure in the following 500 characters: %r" % window[:200]
    return max(nums), "kimi-k3 row window (max of %r): %r" % (nums, window[:300])


def main():
    if not STUB and LEDGER.exists() and HEADER in LEDGER.read_text(encoding="utf-8"):
        print("REFUSED: the ledger already holds '%s' -- the one pricing read was spent" % HEADER)
        return 2
    logs = sorted(glob.glob(str(REPO / ".scratch" / "auth" / "*-sa-*" / "run.log")))
    print("AC5 -- HVST-w-2 guard (c): incident 1 Kimi spend, upper bound from LOCAL evidence")
    print("incident run.log candidates: %d %s" % (len(logs), [Path(x).parent.name for x in logs]))
    if len(logs) != 1:
        print("REFUSED: expected exactly one incident run.log")
        return 1
    log_path = Path(logs[0])
    text = log_path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    steps = re.findall(r"step (\d+): state=(\w+) \((kimi\+cache|kimi)\)", text)
    vision = [s for s in steps if s[2] == "kimi"]
    cached = [s for s in steps if s[2] == "kimi+cache"]
    cache_hit_lines = [ln for ln in lines if "cache hit" in ln]
    err_lines = [ln for ln in lines if re.search(r"KIMI_(ERROR|EMPTY|UNPARSED)", ln)]
    locate_lines = [ln for ln in lines if "locate(" in ln or "via vision" in ln or "locate:" in ln]
    model = (re.search(r"kimi=(\S+)", text) or [None, None])[1]
    started = (re.search(r"\[sa-harvest (\d\d:\d\d:\d\d)\]", text) or [None, None])[1]
    print("run.log: %s (%d lines), first line time %s local, model=%s" % (log_path.parent.name, len(lines), started, model))
    print("steps found: %d; classified by a Kimi call (state token '(kimi)'): %d %s; classified from the perceptual cache "
          "('(kimi+cache)'): %d %s" % (len(steps), len(vision), [(s[0], s[1]) for s in vision], len(cached),
                                        [(s[0], s[1]) for s in cached]))
    print("'cache hit ... no Kimi call' log lines: %d; KIMI_ERROR/EMPTY/UNPARSED retry lines: %d; vision-locate lines: %d"
          % (len(cache_hit_lines), len(err_lines), len(locate_lines)))
    src = (REPO / "org/tier1_exec/4.0.0_SA_CRO/scripts/sa_harvest_session.py").read_text(encoding="utf-8")
    default_mt = (re.search(r"def kimi_vision\(png_bytes, prompt, max_tokens=(\d+)", src) or [None, None])[1]
    locate_mt = (re.search(r"max_tokens=(\d+)\s*\n?\s*\)\s*#\s*reasoning model", src) or [None, None])[1]
    print("harvester source: kimi_vision default max_tokens=%s (classify); locate() max_tokens=%s; sha256 of source %s" % (
        default_mt, locate_mt, hashlib.sha256(src.encode()).hexdigest()[:16]))
    dims = []
    for step, _state, _ in vision:
        pngs = glob.glob(str(log_path.parent / ("harvest_*_step%s_*.png" % step)))
        dims.append((step, png_dims(pngs[0]) if pngs else (None, None)))
    print("screenshot dimensions of the vision-classified steps (from the saved PNG IHDR): %r" % dims)
    px_tokens = [math.ceil(w * h / 750.0) if w else None for _s, (w, h) in dims]
    print("cross-check of the image-token assumption: w*h/750 per shot = %r (assumed cap %d)" % (px_tokens, IMAGE_TOKEN_CAP))

    n_calls = len(vision)
    out_tokens = n_calls * 4000                       # the order's bound: max_tokens 4000 each
    in_tokens = n_calls * (IMAGE_TOKEN_CAP + PROMPT_TOKENS)
    print("BOUND: %d calls x max_tokens 4000 = %d output tokens; input <= %d x (%d image + %d prompt) = %d tokens" % (
        n_calls, out_tokens, n_calls, IMAGE_TOKEN_CAP, PROMPT_TOKENS, in_tokens))

    page = read_pricing()
    print("PRICING READ (the ONE permitted public read): url=%s read_at=%s status=%s bytes=%d%s" % (
        page["url"], page["read_at"], page["http_status"], page["bytes"], " error=" + page["error"] if page.get("error") else ""))
    rate, rate_note = rate_from(page)
    if rate is None:
        usd = "UNMEASURED (no kimi-k3 rate could be read; the call/token bound above stands)"
        rate_txt = "UNMEASURED -- %s" % rate_note
    else:
        usd_val = (in_tokens + out_tokens) * rate / 1e6
        usd = "<= US$%.4f (all %d tokens priced at the row's MAX figure US$%.2f per 1M tokens)" % (usd_val, in_tokens + out_tokens, rate)
        rate_txt = "read: %s" % rate_note
    print("rate: %s" % rate_txt)
    print("upper bound: %s" % usd)

    redacted = re.sub(r"[\w.+-]+@[\w-]+\.[\w.-]+", "<email-redacted>", text)
    (OUTDIR / "ac5_incident_runlog_redacted.txt").write_text(redacted, encoding="utf-8", newline="\n")
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    entry = """
%s

| field | value |
|---|---|
| seat | `%s` (worker of `2.0.0_SA_COO~H`, task order `HVST-w-2` AC5 = guard (c)), written %s BEFORE any capture |
| what is bounded | the Kimi vision-model calls made by the 00:21Z incident (`INCIDENT 1` above; row `AMGT_HARVST-Z-W37-S3`) |
| method | LOCAL evidence only: the incident's `run.log` (%d lines; copy with the account e-mail redacted: `deliverables/0.9.0_WK_AMGT_HARVST~37/ac5_incident_runlog_redacted.txt`), the saved screenshots' PNG headers, and the harvester source `org/tier1_exec/4.0.0_SA_CRO/scripts/sa_harvest_session.py`. CTO ruling msg 26396 method |
| calls counted | **%d** vision-classified steps %s (state token `(kimi)`); **%d** cache hits, `no Kimi call` %s; retry lines (`KIMI_ERROR/EMPTY/UNPARSED`) in the log: %d; vision-locate lines in the log: %d (the press-and-hold and sign-in clicks were DOM-driven) |
| model | `%s` (from the run's own header line) |
| output tokens, upper bound | %d calls x `max_tokens` 4000 = **%d** (the classify calls' actual default is %s; 4000 is the order's bound) |
| input tokens, upper bound | %d x (%d image + %d prompt) = **%d**. ASSUMPTION, labelled: %d image tokens per screenshot is a cap not read from the provider; the screenshot sizes (%r) give w*h/750 = %r |
| rate card | %s -- URL `%s`, read %s, HTTP %s, %d bytes (ONE unauthenticated GET; no key, no account, no API, no console) |
| **estimate (UPPER BOUND)** | **%s** |
| provider-read figure | **NOT MEASURED** -- an account-holder item (the Moonshot console/usage view); no console, usage or `api.moonshot.ai` endpoint was called by this cell |
| what this is not | not a measurement and not a refund claim; it bounds the incident only |
""" % (HEADER, SEAT, now, len(lines), n_calls, [(s[0], s[1]) for s in vision], len(cached), [(s[0], s[1]) for s in cached],
       len(err_lines), len(locate_lines), model, n_calls, out_tokens, default_mt,
       n_calls, IMAGE_TOKEN_CAP, PROMPT_TOKENS, in_tokens, IMAGE_TOKEN_CAP, dims, px_tokens,
       rate_txt[:400], PRICING_URL, page["read_at"], page["http_status"], page["bytes"], usd)
    with LEDGER.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(entry)
    print("=== LEDGER ENTRY AS WRITTEN (%s) ===" % LEDGER.name)
    print(entry)
    print("AC5: no call to api.moonshot.ai or any Moonshot console/usage endpoint was made; the only read was %s" % PRICING_URL)
    return 0


if __name__ == "__main__":
    sys.exit(main())
