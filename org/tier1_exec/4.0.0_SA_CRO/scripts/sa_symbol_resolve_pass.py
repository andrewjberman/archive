#!/usr/bin/env python
"""
sa_symbol_resolve_pass.py -- resolve sa_symbol for the AMGT_RESAPP 89-name
universe, and MEASURE each resolved name's article density in the same sweep.

WHY BOTH IN ONE PASS. HARVEST_BACKFILL_PLAN_20260911_Z.md s.18 measured that the
two things gating the SA backfill are (1) sa_symbol identity -- the Bloomberg root
404s for every non-US name, only the US ADR resolves -- and (2) article DENSITY,
because a thinly-covered ADR cannot clear s.11's >=3-mentions bar no matter how
the harvest is run. The news call that corroborates a symbol is the same call that
measures its density, so doing them together costs nothing extra.

NO VENDOR. Direct HTTPS to seekingalpha.com, unauthenticated, no proxy, no quota.
s.18: the vendor path for this endpoint returned a SMALLER, structurally corrupted
payload than the direct GET.

THE ACCEPTANCE RULE, and it is s.14's discipline carried onto the symbol axis.
    s.18 measured the failure it exists to stop: 'ROG' returns HTTP 200 with 50
    well-formed records spanning three years, and it is ROGERS CORPORATION, not
    Roche. A 200 with fifty clean records is NOT evidence of the right company.
    So a symbol is accepted only when BOTH hold:
      (a) SA'S OWN COMPANY NAME for that symbol shares a distinctive token with
          the subject company -- never by rank, never by relevance score; and
      (b) THE RETURNED ARTICLE TITLES tie to the subject company.
    (b) is free: the titles arrive in the payload the density read already pays
    for. Where either fails, the value is UNRESOLVED, not a best guess.

USAGE
    python sa_symbol_resolve_pass.py --dry-run            # 0 calls, prints queries
    python sa_symbol_resolve_pass.py --out <path>         # the full pass
    python sa_symbol_resolve_pass.py --limit 6 --out ...  # a bounded batch
"""

from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import sys
import time
import urllib.error
import unicodedata
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ir_domain_bulk_pass import (  # noqa: E402  -- one rule, one definition
    STOP_TOKENS, UNIVERSE, company_name, name_tokens,
)

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")
SEARCH = ("https://seekingalpha.com/api/v3/searches"
          "?filter%5Bquery%5D={q}&filter%5Btype%5D=symbols&page%5Bsize%5D=10")
NEWS = "https://seekingalpha.com/api/v3/symbols/{s}/news"

WINDOW_DAYS = 30          # lib/research/metrics/chatter_axis.py
DENSITY_MIN = 3           # BREAKOUT's minimum raw mentions

# SOURCE-NAME DEFECTS (2.0.0_SA_COO~Y, 2026-09-26, on Andrew's word; 4.0.0_SA_CRO
# has no live lane). `company_name(folder)` is the ONLY input to the search query
# AND to tests (a) and (b), so a folder whose name is misspelled or truncated can
# never resolve no matter how much rate-limit headroom is spent on it. Measured on
# batch 14: 'Haliburton' returned 0 candidates, and 'International Container
# Terminals' returned 10 of which 1 passed the name test and none tied a title.
#
# EACH ENTRY IS A FACTUAL REPAIR OF THE SOURCE STRING AND NEVER A GUESS AT A
# SYMBOL. The acceptance rule is untouched: the corrected name still has to win
# test (a) against SA's own company name and test (b) against returned titles.
# That is the point -- an alias that made a test PASS would defeat the rule that
# caught the 'ROG' -> Rogers Corporation trap s.18 exists for.
#
# WHY THE SAME DEFECT IS ALREADY PATCHED ELSEWHERE AND WAS NOT HERE: the harvest
# CLI carries its own Haliburton special case ("Preserve the known source-folder
# spelling defect, with its measured HAL symbol", lib/opal_data_harvest/__main__.py).
# Two consumers read one universe; one was guarded and this one was not. A control
# does not travel between scripts on its own -- the same sentence this file already
# says about the 403 stop guard, one axis over.
#
# NOT INCLUDED, DELIBERATELY: 'Nubank'. SA names it 'Nu Holdings Ltd.', so no
# distinctive token is shared and the name test CORRECTLY refuses it. That is a
# REBRAND the rule cannot corroborate by name, not a source-string defect, and
# aliasing it would be inventing the corroboration. It stays UNRESOLVED with its
# evidence, for the later-guidance list.
SEARCH_NAME_FIX = {
    # folder spelling -> the company's actual name. Keys are company_name() output,
    # measured, not the raw folder.
    "Haliburton": "Halliburton",
    "International Container Terminals": "International Container Terminal Services",
}


def get_json(url):
    """(status, parsed_or_None). A non-200 is a VALUE, never an exception."""
    req = urllib.request.Request(url, headers={"User-Agent": UA,
                                               "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            raw = r.read().decode("utf-8", "replace")
            code = r.status
    except urllib.error.HTTPError as e:
        return e.code, None
    except Exception as e:
        return type(e).__name__, None
    try:
        return code, json.loads(raw)
    except Exception:
        return code, None


def strip_tags(s: str) -> str:
    """
    SA MARKS THE MATCHED SUBSTRING WITH <b> IN *EVERY* FIELD, INCLUDING `name`.
    Measured: a search for "ASML" returned the symbol as '<b>ASML</b>', so the
    news URL became /symbols/%3Cb%3EASML%3C/b%3E/news and 404'd. That produced
    FALSE REFUSALS on exactly the EASIEST names -- the ones where the query
    matched the ticker itself. Strip tags from the symbol, not just the label.
    """
    return re.sub(r"<[^>]+>", "", s or "")


def fold(s: str) -> str:
    """
    Accent-fold before comparing. 'America Movil' vs SA's 'America Movil,
    S.A.B. de C.V.' -- written with the accents it actually carries -- failed
    every token test, because stripping non-ASCII turned the accented name into
    'amricamvil'. THE CORRECT ANSWER WAS REJECTED FOR HAVING ACCENTS.
    """
    return unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode()


def _words(s: str) -> set:
    """Distinctive word tokens, accent-folded, corporate furniture removed."""
    return {w for w in re.split(r"[^a-z0-9]+", fold(s).lower())
            if len(w) >= 4 and w not in STOP_TOKENS}


def name_matches(subject: str, sa_name: str):
    """
    TEST (a). Returns (passed, overlap) comparing SA's own company name to ours.

    THIS USED TO BE 'does SA's name CONTAIN any one of our tokens', AND THAT
    RULE SHIPPED A WRONG COMPANY ON ITS FIRST BATCH: 'America Movil' matched
    'Liberty Latin **America** Ltd.' on the token 'america' and was accepted
    with 48 of 50 titles "confirming" it -- because test (b) uses THE SAME
    TOKENS, so both tests failed together on one weak geographic word. Two
    tests that share a dependency are one test (Rule 22).

    The fix is not a longer stopword list written from recall -- it is a
    SYMMETRIC measure, derived from the two names themselves:
        jaccard(our distinctive words, SA's distinctive words) >= 0.5
    'America Movil' vs 'Liberty Latin America' = 1/4 -> REFUSED.
    'America Movil' vs 'America Movil, S.A.B. de C.V.' = 2/2 -> ACCEPTED.
    A containment match on the concatenated forms also passes, so
    "L'Air Liquide S.A." still matches 'Air Liquide'.
    """
    a, b = _words(subject), _words(strip_tags(sa_name))
    ca = re.sub(r"[^a-z0-9]+", "", fold(subject).lower())
    cb = re.sub(r"[^a-z0-9]+", "", fold(strip_tags(sa_name)).lower())
    if ca and cb and (ca in cb or cb in ca):
        return True, 1.0
    if not a or not b:
        return False, 0.0
    j = len(a & b) / float(len(a | b))
    return j >= 0.5, round(j, 3)


def titles_match(subject: str, records: list) -> tuple:
    """TEST (b). Do the articles' own titles name this company? Returns (hits, n)."""
    toks = [fold(t) for t in name_tokens(subject)]
    hits = 0
    for rec in records:
        t = re.sub(r"[^a-z0-9]+", "",
                   fold(str((rec.get("attributes") or {}).get("title", ""))).lower())
        if any(tok in t for tok in toks):
            hits += 1
    return hits, len(records)


def density(records: list, today: datetime.date) -> dict:
    pubs = sorted(str((r.get("attributes") or {}).get("publishOn", ""))
                  for r in records)
    pubs = [p for p in pubs if p]
    if not pubs:
        return {"records": 0, "in_window": 0, "oldest": None, "newest": None,
                "distinct_days": 0, "covers_window": False}
    cut = (today - datetime.timedelta(days=WINDOW_DAYS)).isoformat()
    return {
        "records": len(pubs),
        "in_window": sum(1 for p in pubs if p[:10] >= cut),
        "oldest": pubs[0][:10],
        "newest": pubs[-1][:10],
        "distinct_days": len({p[:10] for p in pubs}),
        # The window is COVERED when the payload reaches back past the cut --
        # otherwise the 30 days are not all represented in what we hold.
        "covers_window": pubs[0][:10] <= cut,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--max-candidates", type=int, default=2,
                    help="news probes per name; each is free but not instant")
    ap.add_argument("--exclude-done", default="",
                    help="path to a prior output JSON; any folder it ANSWERED "
                         "is skipped. FOURTH instance of the same lesson: "
                         "ir_domain_bulk_pass.py has had this limb all along "
                         "and this pass shipped without it. The scarce resource "
                         "here is not calls -- they are free -- it is RATE-LIMIT "
                         "HEADROOM, and re-asking 17 already-answered names "
                         "spends ~50 calls of it before reaching an unasked one.")
    ap.add_argument("--out", default="")
    ap.add_argument("--sleep", type=float, default=0.25)
    args = ap.parse_args()

    universe = json.load(open(UNIVERSE, encoding="utf-8"))
    names = universe["names"]
    targets = names
    carried = []
    if args.exclude_done:
        prior = json.load(open(args.exclude_done, encoding="utf-8"))
        # ONLY a folder that was genuinely ANSWERED is skipped. One the vendor
        # refused was NEVER ASKED, so it must be retried -- skipping it would
        # bake a rate limit into the result as though it were a finding.
        # 2.0.0_SA_COO~Y 2026-09-26: `search_http == 200` ALONE WAS NOT "ANSWERED",
        # and the gap is why a chained run gained ~1 name per batch. A name whose
        # SEARCH returned 200 but whose NEWS call was refused 403 also carries
        # search_http 200, so it was skipped every batch and its rate limit was
        # baked in as though it were a finding -- exactly what the comment above
        # forbids, one call further down the path. MEASURED on batch 14: 7 of the
        # 34 unanswered names sat in that state, and their symbols were ALREADY
        # identified at name_overlap 1.0 (Nike -> NKE 'NIKE, Inc.', Roche ->
        # RHHBY 'Roche Holding AG'); only the density call was missing.
        def _answered(r):
            if r.get("search_http") != 200:
                return False              # the vendor refused the SEARCH: never asked
            # A SOURCE-NAME REPAIR INVALIDATES A PRIOR ANSWER: the query string
            # changed, so an old refusal was about a DIFFERENT company name.
            prior_nm = r.get("company_name")
            if SEARCH_NAME_FIX.get(prior_nm, prior_nm) != prior_nm:
                return False
            if ((r.get("sa_symbol") or {}).get("value")):
                return True               # resolved
            # No value. Was that an EVIDENCE refusal, or a vendor refusal on the
            # news leg? Any probed candidate with a non-200 means NEVER ANSWERED.
            for probe in (r.get("candidates_probed") or []):
                if (probe.get("http") or 200) != 200:
                    return False
            return True                   # a genuine refusal on evidence

        done = {r["folder"] for r in prior["records"] if _answered(r)}
        carried = [r for r in prior["records"] if r["folder"] in done]
        refused_before = len(prior["records"]) - len(done)
        targets = [t for t in targets if t["folder"] not in done]
        print("CARRIED        %d already-ANSWERED folder(s) skipped and carried "
              "into the output" % len(done))
        print("RETRIED        %d folder(s) the vendor had refused -- a refusal "
              "is not an answer" % refused_before)
    targets = targets[:args.limit] if args.limit else targets
    today = datetime.date.today()

    print("UNIVERSE       %s" % UNIVERSE)
    print("DENOMINATOR    %d folders   THIS BATCH %d" % (len(names), len(targets)))
    print("PROVIDER       seekingalpha.com, DIRECT, unauthenticated, no vendor")
    print("BARS           window %d days, density >= %d in window"
          % (WINDOW_DAYS, DENSITY_MIN))

    if args.dry_run:
        print("MODE           DRY RUN -- zero calls\n")
        for rec in targets:
            # SAME repair as the live loop. A preview that does not apply it
            # would show a query the run will not make -- the control lying.
            nm = SEARCH_NAME_FIX.get(company_name(rec["folder"]), company_name(rec["folder"]))
            print("  %-42s -> search %-34s tokens=%s"
                  % (rec["folder"], repr(nm), name_tokens(nm)))
        return 0

    print("MODE           LIVE\n")
    out, calls = list(carried), 0
    # SEED THE COUNTERS FROM THE CARRIED RECORDS. `out` starts non-empty, so
    # counters starting at 0 would report a resume as though the carried names
    # had all failed -- an undercount that reads exactly like a regression.
    resolved = sum(1 for r in carried
                   if r.get("sa_symbol", {}).get("status") == "INFERRED")
    served = sum(1 for r in carried
                 for p in [max(r.get("candidates_probed") or [{}],
                               key=lambda x: x.get("records", 0))]
                 if p.get("in_window", 0) >= DENSITY_MIN and p.get("covers_window"))
    consecutive_refusals = 0
    not_asked_news = 0

    for i, rec in enumerate(targets, 1):
        folder = rec["folder"]
        nm = company_name(folder)
        nm = SEARCH_NAME_FIX.get(nm, nm)   # source-name repair, before BOTH the query and the tests
        code, payload = get_json(SEARCH.format(q=urllib.parse.quote(nm)))
        calls += 1
        cands = (payload or {}).get("symbols", []) if code == 200 else []

        # A VENDOR REFUSAL IS NOT A FINDING ABOUT THE COMPANY. Measured
        # 2026-09-14: this endpoint served 17 queries then returned HTTP 403
        # for the remaining 72, and without this stop the pass spent 72 calls
        # recording "no SA symbol" for Costco, Netflix, Visa and Mastercard.
        # The IR pass had this guard; this one did not, because it was written
        # after it -- a control does not travel between scripts on its own.
        if code != 200:
            consecutive_refusals += 1
            out.append({
                "folder": folder, "company_name": nm, "search_http": code,
                "sa_symbol": {
                    "value": None, "status": "UNRESOLVED",
                    "evidence": ("NOT ASKED -- the search endpoint returned "
                                 "HTTP %s. THIS IS NOT A FINDING ABOUT THIS "
                                 "COMPANY and carries no evidence either way "
                                 "about whether it has an SA symbol." % code),
                    "resolved_at": datetime.datetime.utcnow()
                                   .strftime("%Y-%m-%dT%H:%MZ"),
                },
                "candidates_probed": [], "candidates_rejected_on_name": [],
            })
            print("  [%2d] %-40s --       NOT ASKED, HTTP %s" % (i, folder[:40], code))
            if consecutive_refusals >= 3:
                print("\n  STOPPING: 3 consecutive vendor refusals. The rest "
                      "of the batch would record absences never asked about.")
                break
            continue
        consecutive_refusals = 0

        # TEST (a) -- SA's own company name must carry a distinctive token.
        # Rank and score are RECORDED but never decide.
        scored = [(c, ) + name_matches(nm, c.get("content", "")) for c in cands]
        passed = [c for c, ok, _ in scored if ok]
        overlap = {strip_tags(c.get("name")): j for c, ok, j in scored if ok}
        rejected = [{"symbol": c.get("name"),
                     "sa_company": strip_tags(c.get("content", "")),
                     "score": c.get("score"),
                     "name_overlap": j}
                    for c, ok, j in scored if not ok][:3]

        best, probes = None, []
        news_refused = 0
        for c in passed[:args.max_candidates]:
            sym = strip_tags(c.get("name"))
            ncode, npayload = get_json(NEWS.format(s=urllib.parse.quote(sym)))
            calls += 1
            if ncode != 200:
                news_refused += 1
            recs = (npayload or {}).get("data", []) if ncode == 200 else []
            hits, n = titles_match(nm, recs)          # TEST (b) -- free
            d = density(recs, today)
            probe = {"symbol": sym, "sa_company": strip_tags(c.get("content", "")),
                     "name_overlap": overlap.get(sym),
                     "http": ncode, "title_hits": hits, "title_of": n, **d}
            probes.append(probe)
            # (b) must fire on at least one title, else this symbol is not
            # demonstrably about this company whatever its name said.
            if hits > 0 and (best is None or probe["records"] > best["records"]):
                best = probe
            if args.sleep:
                time.sleep(args.sleep)

        if best:
            resolved += 1
            ok = best["in_window"] >= DENSITY_MIN and best["covers_window"]
            served += 1 if ok else 0
            status, value = "INFERRED", best["symbol"]
            verdict = ("ACCEPTED %s -- SA names it %r (test a) and %d of %d "
                       "returned titles name the company (test b). Window: %s .. "
                       "%s, %d in the last %d days -- density bar (>=%d) %s."
                       % (best["symbol"], best["sa_company"], best["title_hits"],
                          best["title_of"], best["oldest"], best["newest"],
                          best["in_window"], WINDOW_DAYS, DENSITY_MIN,
                          "MET" if ok else "NOT MET"))
        elif news_refused and news_refused >= len(probes):
            # NOT ASKED, NOT REFUSED. Measured 2026-09-14: this vendor's block
            # MOVES BETWEEN ENDPOINTS -- the SEARCH limit lifted at the same
            # moment the NEWS limit engaged. Without this branch, test (b) reads
            # zero titles for a reason that has nothing to do with the company,
            # and the record says "REFUSED ON EVIDENCE".
            # >> THE SEARCH SIDE ALREADY HAD THIS GUARD AND THE NEWS SIDE DID
            #    NOT. That is the third time tonight a control failed to travel
            #    to the sibling surface it obviously applies to.
            status, value = "UNRESOLVED", None
            not_asked_news += 1
            verdict = ("NOT ASKED -- the name test passed for %d candidate(s), "
                       "but every news call was refused by the vendor (HTTP %s). "
                       "THIS IS NOT A FINDING ABOUT THIS COMPANY: test (b) never "
                       "ran." % (len(passed),
                                 ", ".join(str(p["http"]) for p in probes)))
        else:
            status, value = "UNRESOLVED", None
            verdict = ("REFUSED -- %d candidate(s) returned, %d passed the "
                       "name test, and none had a single returned title naming "
                       "the company. A symbol that resolves is not a symbol "
                       "that is right (s.18: ROG is Rogers Corp, not Roche)."
                       % (len(cands), len(passed)))

        out.append({
            "folder": folder, "company_name": nm, "search_http": code,
            "sa_symbol": {
                "value": value, "status": status,
                "evidence": ("seekingalpha.com/api/v3, DIRECT and "
                             "unauthenticated. " + verdict),
                "resolved_at": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%MZ"),
            },
            "candidates_probed": probes,
            "candidates_rejected_on_name": rejected,
        })
        print("  [%2d] %-40s %-8s %s"
              % (i, folder[:40], value or "--", verdict[:66]))
        if args.sleep:
            time.sleep(args.sleep)

    # A VENDOR REFUSAL AND A REFUSAL ON EVIDENCE ARE DIFFERENT FACTS. The first
    # run of this pass printed "RESOLVED 17 of 89 / REFUSED 72 of 89" when 72 of
    # those had returned HTTP 403 and were never asked -- which reads as
    # "Costco, Netflix, Visa and Mastercard have no SA symbol".
    # `carried` entries are already-answered records folded back in, so the
    # partition below is over the WHOLE universe, not just this run.
    # THIS ARITHMETIC WAS WRONG AND IT PRINTED A NUMBER THAT CANNOT BE TRUE:
    # "ASKED 19 of 6" and "NOT ASKED -13". Cause: `out` is seeded with the
    # CARRIED records while `targets` is the LIMITED batch, so
    # `len(targets) - len(out)` goes negative the moment --limit is combined
    # with --exclude-done. Each field was right on its own and the SUBTRACTION
    # mixed two different populations.
    # >> A DENOMINATOR SMALLER THAN ITS NUMERATOR, AND A NEGATIVE COUNT, ARE THE
    #    TELL. Neither needed a vendor to detect -- the arithmetic convicts
    #    itself, which is why a count that cannot be true is worth more than a
    #    count that is merely surprising.
    asked = [r for r in out if r.get("search_http") == 200]
    attempted_this_run = len(out) - len(carried)
    never_reached = max(0, len(targets) - attempted_this_run)
    notasked = (len(out) - len(asked)) + never_reached
    print("\nCALLS          %d (all free, direct, no quota)" % calls)
    print("POPULATION     %d carried + %d this batch = %d record(s)"
          % (len(carried), len(targets), len(carried) + len(targets)))
    print("ASKED          %d of %d" % (len(asked), len(carried) + len(targets)))
    print("NEVER REACHED  %d  <- the stop guard fired before these" % never_reached)
    print("NOT ASKED      %d search-refused + %d news-refused  <- vendor "
          "refusals, NOT findings about those names"
          % (notasked, not_asked_news))
    print("RESOLVED       %d of %d asked" % (resolved, len(asked)))
    # THE PRINT AND THE JSON MUST USE ONE FORMULA. They did not: the JSON
    # subtracted the news-refused and this line did not, so a NOT-ASKED was
    # printed as a REFUSAL -- the exact conflation the whole partition exists to
    # prevent, surviving in the line a reader actually looks at.
    print("REFUSED        %d of %d asked  <- a 0 here means the rule is NOT "
          "discriminating" % (len(asked) - resolved - not_asked_news, len(asked)))
    print("SERVEABLE      %d of %d asked  <- resolved AND clearing the density "
          "bar" % (served, len(asked)))

    # SELF-CHECK: refuse to write an artifact whose own arithmetic is
    # impossible. Cheaper than a reader discovering it later.
    assert len(asked) <= len(carried) + len(targets), "ASKED exceeds population"
    assert notasked >= 0, "negative NOT-ASKED"

    if args.out:
        json.dump({
            "artifact": "sa_symbol RESOLUTION + ARTICLE DENSITY PASS",
            "author": "4.0.0_SA_CRO~Z",
            "generated_at": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%MZ"),
            "provider": "seekingalpha.com/api/v3 -- DIRECT, unauthenticated, "
                        "NO VENDOR, no quota",
            "criterion": "HARVEST_BACKFILL_PLAN_20260911_Z.md s.18: accepted only "
                         "when SA's own company name carries a distinctive token "
                         "(a) AND a returned article title names the company (b). "
                         "Never by rank, never by relevance score.",
            "bars": {"window_days": WINDOW_DAYS, "density_min": DENSITY_MIN},
            "status_note": "INFERRED, not MEASURED: SA's own naming plus its own "
                           "article titles are two readings of ONE source. An "
                           "independent confirmation would be a second provider.",
            "denominator": {
                "universe": len(names),
                "population_this_output": len(carried) + len(targets),
                "ASKED": len(asked),
                "never_reached_stop_guard": never_reached,
                "NOT_ASKED_search_refused": notasked,
                "NOT_ASKED_news_refused": not_asked_news,
                "resolved_of_asked": resolved,
                "refused_on_evidence_of_asked": len(asked) - resolved
                                               - not_asked_news,
                "serveable_at_the_density_bar": served,
                "calls": calls,
                "partition_note": "A VENDOR REFUSAL AND A REFUSAL ON EVIDENCE "
                                  "ARE DIFFERENT FACTS. Collapsing them would "
                                  "report companies as having no SA symbol when "
                                  "nothing was ever asked about them.",
            },
            "records": out,
        }, open(args.out, "w", encoding="utf-8", newline="\n"),
            indent=2, ensure_ascii=True)
        print("WROTE          %s" % args.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
