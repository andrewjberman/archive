"""AMGT_RESAPP round 54, AMGT-ad-1 AC2 -- `drafting_build.hold_unspanned(document)` moves EXACTLY the non-verbatim served sentences
(no non-blank quoted span: the deployed adapter's read gate) to `held_no_span` and moves nothing else. Run IN MEMORY over every stored D-1 document (drafting/v1/*.json, read-only; the population
check in ad_1_census.py shows the listing equals the MEASURED population's stored documents). Per document, on the result:
  - no sentence left in sections[].sentences lacks a non-blank quoted span;
  - every span-carrying served sentence is present, byte-equal (json, sorted keys), in the same section and the same order;
  - `held_no_span` is the pipeline's own held shape (lib/research/drafting/pipeline.py:166; schema.json `held_sentence`): one
    {"section", "text", "evidence", "reason": pipeline.HOLD_NO_SPAN_REASON} per removed sentence, and nothing else;
  - every top-level key other than sections / held_no_span / denominators is byte-equal to the stored one;
  - the DEPLOYED adapter's validator (scoped_amgt._validate_drafting_document) accepts it;
  - the input document is not mutated.
Plant: a copy of ASML with one non-verbatim sentence given a quoted span must KEEP that sentence served (the transform reads the span,
not the text). Prints per-document counts. Writes nothing.
usage: python <this>   (from the repo root)"""
import copy
import json
import os
import sys

sys.path.insert(0, os.getcwd())
import boto3  # noqa: E402
from lib.research.api import scoped_amgt  # noqa: E402
from lib.research.drafting.pipeline import HOLD_NO_SPAN_REASON as HOLD_REASON  # noqa: E402
from lib.research.filings import drafting_build as db  # noqa: E402
from lib.research.identity import crosswalk  # noqa: E402

KEEP = ("sections", "held_no_span", "denominators")


def j(o):
    return json.dumps(o, sort_keys=True)


def nonverbatim(s):
    return not any(str(x).strip() for x in s.get("quoted_spans") or [])  # the deployed adapter's read gate


def grade(doc, out):
    bad = []
    before = {sec.get("section"): sec.get("sentences") or [] for sec in doc.get("sections") or []}
    after = {sec.get("section"): sec.get("sentences") or [] for sec in out.get("sections") or []}
    removed = [(k, s) for k, ss in before.items() for s in ss if nonverbatim(s)]
    for k, ss in before.items():
        want = [j(s) for s in ss if not nonverbatim(s)]
        got = [j(s) for s in after.get(k, [])]
        if got != want:
            bad.append("section %s: served %d, want %d span-carrying in order" % (k, len(got), len(want)))
    held = out.get("held_no_span")
    held = held if isinstance(held, list) else []
    got_held = sorted(j([h.get("section"), h.get("text"), h.get("evidence"), h.get("reason")]) for h in held if isinstance(h, dict))
    want_held = sorted(j([k, s.get("text"), list(s.get("evidence") or []), HOLD_REASON]) for k, s in removed)
    if got_held != want_held or len(held) != len(removed):
        bad.append("held_no_span carries %d entries, want %d (section, text, evidence, reason) for the removed sentences"
                   % (len(held), len(removed)))
    for k in set(doc) | set(out):
        if k not in KEEP and j(doc.get(k)) != j(out.get(k)):
            bad.append("top-level %s moved" % k)
    valid, reason = scoped_amgt._validate_drafting_document(out)
    if not valid:
        bad.append("served validator: %s" % reason)
    return len(removed), bad


def main():
    fn = getattr(db, "hold_unspanned", None)
    if fn is None:
        print("drafting_build.hold_unspanned: ABSENT")
        print("HOLD_UNSPANNED MOVES EXACTLY THE NON-VERBATIM SENTENCES: NO")
        return 1
    cl = boto3.client("s3", region_name="us-east-1")
    pages = cl.get_paginator("list_objects_v2").paginate(Bucket=crosswalk.POOL_BUCKET, Prefix="drafting/v1/")
    keys = [o["Key"] for p in pages for o in p.get("Contents", []) if o["Key"].endswith(".json")]
    bad_all, moved_total = [], 0
    asml = None
    for key in keys:
        doc = db._get_json_object(cl, key)
        snap = j(doc)
        out = fn(doc)
        if j(doc) != snap:
            bad_all.append("%s: input mutated" % key)
        n, bad = grade(doc, out)
        moved_total += n
        print("%s: moved %d%s" % (key, n, "" if not bad else " BAD %s" % bad[:3]))
        bad_all += ["%s: %s" % (key, b) for b in bad]
        if key.endswith("ASML_NA_Equity.json"):
            asml = doc
    if asml is not None:
        plant = copy.deepcopy(asml)
        for sec in plant["sections"]:
            hit = next((s for s in sec.get("sentences") or [] if nonverbatim(s)), None)
            if hit is not None:
                hit["quoted_spans"] = ["planted span"]
                hit["quote_method"] = "model-marked"
                text = hit["text"]
                break
        out = fn(plant)
        kept = any(s.get("text") == text for sec in out.get("sections") or [] for s in sec.get("sentences") or [])
        print("plant (one ASML sentence given a span) kept served: %s" % kept)
        if not kept:
            bad_all.append("plant: a span-carrying sentence was removed")
    else:
        bad_all.append("ASML document not read")
    print("documents %d; sentences moved %d" % (len(keys), moved_total))
    ok = bool(keys) and moved_total > 0 and not bad_all
    print("HOLD_UNSPANNED MOVES EXACTLY THE NON-VERBATIM SENTENCES: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
