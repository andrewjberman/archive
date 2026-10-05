"""AMGT_RESAPP AMGT-au-5 -- FWD-8's identity read (PRD v0.38 :540-543), on the DEPLOYED function.

DONE WHEN: on every covered name the comparison block's subject identity equals the page's subject, and a name with no
sensible set says so in words.

Population: covered_security_keys() (the dossier table's partitions, read fresh from S3) -- every covered name.
For each name, two reads of the DEPLOYED `opal-amgt-scoped-api` (lambda:Invoke, GET only, no write):
  PAGE        overlay  -> security_key, identity.security_key, display_name, name        (what the page header shows)
  COMPARISON  peers    -> security_key, identity.security_key, subject.security_key,
                          subject.display_name, subject.name                              (the Peers tab's block)
              overlay.peers (the copy the overlay carries) is read the same way.
A name is RIGHT when every key the comparison block carries equals the page's key AND, where the block carries a subject
name, it equals the page's display_name (or name). A name whose peer block is the absent arm (basis "absent") is RIGHT
only when it carries a non-empty `reason` (the words); an absent arm with no reason is WRONG. A read that did not
complete is WRONG (never skipped), counted and listed.
Prints one line per WRONG name, then `FWD8 WRONG n of N`. Exit 0 when the reads completed (the count is the result).
usage: PYTHONPATH=<repo root> python <this>
"""
from __future__ import annotations

import importlib.util
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import boto3

ROOT = Path.cwd()
CAPTURE_LIB = ROOT / "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~158/capture_lib.py"


def _lib():
    spec = importlib.util.spec_from_file_location("capture_lib", str(CAPTURE_LIB))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


CL = _lib()
CLIENT = boto3.client("lambda", region_name=CL.REGION, config=boto3.session.Config(read_timeout=300, retries={"max_attempts": 3}))


def check(key):
    """Return (verdict, reasons, detail) for one covered name."""
    pre = CL.ROUTE_PREFIX + "/security/" + key
    ov, ovm = CL._invoke(CLIENT, pre + "/overlay")
    pr, prm = CL._invoke(CLIENT, pre + "/peers")
    if ov is None or pr is None:
        return "WRONG", ["read did not complete: overlay=%s peers=%s" % (ovm.get("status") or ovm.get("error"), prm.get("status") or prm.get("error"))], {}
    page_key = ov.get("security_key")
    page_ident = (ov.get("identity") or {}).get("security_key")
    page_names = {n for n in (ov.get("display_name"), ov.get("name")) if n}
    why = []
    if page_key != key or (page_ident not in (None, key)):
        why.append("page itself does not carry the requested key (overlay %r / identity %r vs %r)" % (page_key, page_ident, key))
    blocks = {"peers-route": pr, "overlay.peers": ov.get("peers")}
    absent_words = []
    for label, b in blocks.items():
        if not isinstance(b, dict):
            why.append("%s: no block (%r)" % (label, type(b).__name__))
            continue
        if b.get("basis") == "absent":
            if (b.get("reason") or "").strip():
                absent_words.append(label)
            else:
                why.append("%s: absent arm with NO reason" % label)
            continue
        sub = b.get("subject") or {}
        carried = {"security_key": b.get("security_key"), "identity.security_key": (b.get("identity") or {}).get("security_key"),
                   "subject.security_key": sub.get("security_key")}
        for field, v in carried.items():
            if v is None:
                why.append("%s: %s not carried" % (label, field))
            elif v != key:
                why.append("%s: %s=%r != page %r" % (label, field, v, key))
        names = {n for n in (sub.get("display_name"), sub.get("name")) if n}
        if not names:
            why.append("%s: no subject name carried" % label)
        elif page_names and not (names & page_names):
            # the block's names are compared to the page's: the display names must agree
            if sub.get("display_name") and ov.get("display_name") and sub.get("display_name") != ov.get("display_name"):
                why.append("%s: subject.display_name %r != page display_name %r" % (label, sub.get("display_name"), ov.get("display_name")))
            elif not (sub.get("display_name") and ov.get("display_name")):
                why.append("%s: subject names %r share none with page names %r" % (label, sorted(names), sorted(page_names)))
    return ("WRONG" if why else "RIGHT"), why, {"basis": (pr or {}).get("basis"), "absent_with_words": absent_words}


def main():
    from lib.research.coverage.covered_universe import covered_security_keys

    keys = covered_security_keys()
    N = len(keys)
    print("FWD8 population: %d covered names (covered_security_keys(), read fresh from S3)" % N, flush=True)
    with ThreadPoolExecutor(max_workers=6) as pool:
        results = list(pool.map(check, keys))
    wrong = 0
    absent = 0
    for key, (verdict, why, detail) in zip(keys, results):
        if detail.get("basis") == "absent":
            absent += 1
        if verdict == "WRONG":
            wrong += 1
            print("WRONG %s: %s" % (key, "; ".join(why)))
    print("FWD8 peer-block basis absent-with-words: %d of %d (the rest derived/analyst)" % (absent, N))
    print("FWD8 WRONG %d of %d" % (wrong, N))
    return 0


if __name__ == "__main__":
    sys.exit(main())
