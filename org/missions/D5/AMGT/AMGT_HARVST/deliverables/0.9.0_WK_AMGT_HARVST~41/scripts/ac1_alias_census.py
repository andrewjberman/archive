"""HVST-d-1 AC1: the universe census of tails a headline drops, then the rule's effect per security.
Reads the POOL universe (S3 GET) exactly as the served build did; no sa join; writes nothing."""
import json
import re
import sys

sys.path.insert(0, __file__.rsplit("scripts", 1)[0] + "scripts")
import _common  # noqa: E402,F401  (puts REPO on sys.path)

from lib.research.harvest import universe_securities as new  # noqa: E402

old = _common.load_old_module()

TOK = re.compile(r"\s+")
SUFFIX_WORDS = {s.lower() for s in new.CORPORATE_SUFFIXES}
# A WATCH LIST, not a census: legal-form words absent from CORPORATE_SUFFIXES. Counted, NOT added
# by this cell (the ruling is about non-suffix tails, and a suffix-list edit is a separate act).
WATCH_LEGAL_FORMS = ("spa", "se", "sca", "oyj", "lp", "cos", "persero", "de cv")

# Independent DETECTORS -- they do not call the rules under test.
DETECTORS = [
    ("dot_com", lambda name, ticker_loose: bool(re.search(r"\.com$", name, re.I))),
    ("state_of_incorporation", lambda name, tl: bool(re.search(r"/[A-Z]{2,3}$", name))),
    ("trailing_period", lambda name, tl: name.rstrip().endswith(".")),
    ("depositary_receipt", lambda name, tl: TOK.split(name)[-1] in ("ADR", "ADS", "GDR")),
    ("exchange_code", lambda name, tl: len(TOK.split(name)) > 1 and TOK.split(name)[-1] in new._EXCHANGE_CODES),
    ("ticker_token_tail", lambda name, tl: len(TOK.split(name)) > 1 and TOK.split(name)[-1].strip("*/.-").upper() in tl),
    ("ticker_code", lambda name, tl: len(TOK.split(name)) > 1 and bool(re.fullmatch(r"(?=[A-Z0-9]*\d)[A-Z0-9]{3,}", TOK.split(name)[-1]))),
]


def loose(ticker):
    return {t.strip("*/.-").upper() for t in TOK.split(str(ticker or "").strip()) if t}


def main():
    document, provenance = new._read_universe()
    names = document.get("names", []) or []
    print("== UNIVERSE READ ==")
    print("source=%s as_of=%s snapshot_date=%s fallback_reason=%s" % (
        provenance.get("source"), provenance.get("as_of"), provenance.get("snapshot_date"),
        provenance.get("fallback_reason")))
    print("denominators=%s" % json.dumps(provenance.get("denominators"), sort_keys=True))
    print("BASE module = git:%s:%s" % (_common.BASE, _common.MODULE_PATH))

    old_secs, old_sum = old.securities_from_universe(document)
    new_secs, new_sum = new.securities_from_universe(document)
    print("names scanned (denominator)=%d  securities old=%d new=%d  without_identity=%d" % (
        len(names), len(old_secs), len(new_secs), new_sum["without_identity"]))

    # ---- THE CENSUS ------------------------------------------------------------------------
    print("\n== CENSUS: non-suffix tails a headline would drop (detector over %d securities' company strings) ==" % len(new_secs))
    per_tail = {}
    for s in new_secs:
        tl = loose(s["ticker"])
        forms = [s["company"]] + new.suffix_forms(s["company"])
        for label, det in DETECTORS:
            if any(det(form, tl) for form in forms):
                per_tail.setdefault(label, []).append(s)
    for label, _det in DETECTORS:
        hit = per_tail.get(label, [])
        print("tail %-24s %3d of %d  %s" % (label, len(hit), len(new_secs),
                                             ["%s <- %r" % (s["ticker"], s["company"]) for s in hit]))
    trunc = [s for s in new_secs if len(s["company"]) == 30]
    print("tail %-24s %3d of %d  %s  [NO RULE: the cut word is unknowable without a guess; not added]" % (
        "possible_30char_truncation", len(trunc), len(new_secs), ["%s <- %r" % (s["ticker"], s["company"]) for s in trunc]))
    watch = []
    for s in new_secs:
        words = TOK.split(s["company"])
        if words[-1].lower() in WATCH_LEGAL_FORMS or (len(words) > 1 and words[-2].lower() in WATCH_LEGAL_FORMS):
            watch.append(s)
    print("tail %-24s %3d of %d  %s  [WATCH LIST, NOT A CENSUS; suffix-list gap, not added: e.g. bare 'Travelers' "
          "would false-hit ordinary prose]" % ("legal_form_not_in_suffix_list", len(watch), len(new_secs),
                                                ["%s <- %r" % (s["ticker"], s["company"]) for s in watch]))

    # ---- THE RULE: aliases each rule ADDS, per security; the ones _usable_alias REFUSES ------
    print("\n== THE RULE: aliases ADDED per security (old aliases are kept, in place, first) ==")
    by_rule_added = {r: 0 for r, _f in new.NAME_TAIL_RULES}
    by_rule_refused = {r: 0 for r, _f in new.NAME_TAIL_RULES}
    refused_rows = []
    securities_gaining = {r: set() for r, _f in new.NAME_TAIL_RULES}
    prefix_ok = True
    for o, n in zip(old_secs, new_secs):
        assert o["security_key"] == n["security_key"]
        if n["aliases"][:len(o["aliases"])] != o["aliases"]:
            prefix_ok = False
        added = [a for a in n["aliases"] if a not in o["aliases"]]
        if added:
            print("ADD  %-16s old=%s  +%s" % (n["key"], o["aliases"], added))
    for n in new_secs:
        tokens = new._ticker_tokens(n["ticker"])
        for rule, form in new.common_name_forms(n["company"], n["ticker"]):
            if new._usable_alias(form, tokens):
                if form in n["aliases"]:
                    by_rule_added[rule] += 1
                    securities_gaining[rule].add(n["key"])
            else:
                by_rule_refused[rule] += 1
                refused_rows.append((n["key"], rule, form))
    print("\n== ADDED-ALIAS COUNT PER RULE (denominator: %d names scanned, %d securities) ==" % (len(names), len(new_secs)))
    for rule, _fn in new.NAME_TAIL_RULES:
        print("rule %-24s aliases added=%2d  securities gaining=%2d of %d  refused by _usable_alias=%d" % (
            rule, by_rule_added[rule], len(securities_gaining[rule]), len(new_secs), by_rule_refused[rule]))
    print("summary tail_aliases_added_by_rule=%s" % json.dumps(new_sum["tail_aliases_added_by_rule"], sort_keys=True))
    print("summary tail_aliases_refused_by_rule=%s" % json.dumps(new_sum["tail_aliases_refused_by_rule"], sort_keys=True))
    print("summary tail_rules_denominator=%s" % json.dumps(new_sum["tail_rules_denominator"], sort_keys=True))

    print("\n== ALIASES _usable_alias REFUSES ==")
    print("tail-rule forms refused (%d):" % len(refused_rows))
    for key, rule, form in refused_rows:
        print("  REFUSED %-16s rule=%-22s form=%r" % (key, rule, form))
    base_refused = 0
    for n in new_secs:
        tokens = new._ticker_tokens(n["ticker"])
        for cand in [n["company"]] + new.suffix_forms(n["company"]):
            if not new._usable_alias(cand, tokens):
                base_refused += 1
                print("  REFUSED %-16s rule=%-22s form=%r  (pre-existing suffix/company form)" % (n["key"], "base", cand))
    print("pre-existing refusals=%d (old summary aliases_dropped_unusable=%d, new=%d)" % (
        base_refused, old_sum["aliases_dropped_unusable"], new_sum["aliases_dropped_unusable"]))

    # ---- CHECKS ----------------------------------------------------------------------------
    amzn_old = next(s for s in old_secs if s["key"] == "AMZN_US_Equity")
    amzn_new = next(s for s in new_secs if s["key"] == "AMZN_US_Equity")
    print("\n== AMZN ==")
    print("AMZN aliases OLD=%s" % amzn_old["aliases"])
    print("AMZN aliases NEW=%s" % amzn_new["aliases"])
    consistent = (sum(by_rule_added.values()) == sum(new_sum["tail_aliases_added_by_rule"].values())
                  and by_rule_added == new_sum["tail_aliases_added_by_rule"])
    checks = [
        ("AMZN gains 'Amazon'", "Amazon" in amzn_new["aliases"] and "Amazon" not in amzn_old["aliases"]),
        ("every old alias list is a PREFIX of the new one", prefix_ok),
        ("per-rule counts recomputed here == summary counts", consistent),
        ("same securities, same order, old vs new", [s["key"] for s in old_secs] == [s["key"] for s in new_secs]),
        ("no security ends with no alias", new_sum["securities_with_no_alias"] == 0),
    ]
    ok = True
    for label, res in checks:
        print("CHECK %-52s %s" % (label, "PASS" if res else "FAIL"))
        ok = ok and res
    print("AC1 %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
