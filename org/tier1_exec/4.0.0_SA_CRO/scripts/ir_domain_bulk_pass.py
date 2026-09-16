#!/usr/bin/env python
"""
ir_domain_bulk_pass.py -- resolve ir_domain for the AMGT_RESAPP 89-name universe
via Google Custom Search, under the acceptance criterion forced by the probe.

AUTHORITY
    Andrew-direct 2026-09-13 ~04:0xZ, card 4 of "all recs approved":
    the investor-relations and blog search runs on the Google Custom Search key
    the estate already holds -- IR pages and company blogs, SEARCH ONLY, and the
    prove-the-shape-first rule applies. A per-use word for ONE provider for ONE
    purpose. It does NOT widen to Bright Data or any other vendor.

THE ACCEPTANCE CRITERION (HARVEST_BACKFILL_PLAN_20260911_Z.md s.13)
    An ir_domain value is accepted ONLY if the returned domain is independently
    tied to the subject company -- NEVER by rank position. At least one of:
      (a) the registrable domain carries a distinctive token of the company name
      (b) two or more returned results share that same registrable domain
      (c) the domain matches a value already held for that company from another key
    Where none holds, the value is UNRESOLVED, not a guess.

    Reason it exists: on the single probe call, result #4 for "AstraZeneca
    investor relations" was investor.kyntrabio.com -- A DIFFERENT COMPANY'S IR
    PAGE. A top-hit rule would have passed its own test and then silently
    assigned a wrong IR domain to some other name in the 89.

BOUNDS
    - ONE provider (googleapis.com/customsearch/v1), ONE purpose (search).
      No scrape, no fetch of any result page, no other host.
    - THE KEY IS READ FROM STDIN AND NEVER WRITTEN. No key or cx value reaches
      an output file, a log line or an exception message.
    - ONE CALL PER COMPANY. num=10 costs the same one query as num=5 and gives
      the agreement test more to work with, so it is the parsimonious choice,
      not a wider one (Andrew-direct ~03:3xZ: "be parsimonious about pulls").
    - The universe file is READ ONLY. It is a worker proof artifact.

USAGE
    # 0 calls -- prints the derived query for every name, for review
    python ir_domain_bulk_pass.py --dry-run

    # N calls -- key piped in, never on the command line, never on disk
    bash -c '.tools/aws secretsmanager get-secret-value --secret-id google-cse-config \
             --query SecretString --output text' \
      | python ir_domain_bulk_pass.py --limit 5 --out <path>
"""

from __future__ import annotations

import argparse
import collections
import datetime
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

UNIVERSE = os.path.join(
    "org", "missions", "D5", "AMGT", "AMGT_RESAPP", "deliverables",
    "0.9.0_WK_AMGT_RESAPP~4", "universe.json",
)

ENDPOINT = "https://www.googleapis.com/customsearch/v1"

# ---------------------------------------------------------------- name tokens

# Tokens that carry no identity: they appear in thousands of unrelated domains,
# so allowing one to satisfy test (a) would re-create exactly the wrong-company
# acceptance the criterion exists to refuse.
STOP_TOKENS = frozenset({
    "group", "holding", "holdings", "company", "companies", "corporation",
    "corp", "incorporated", "international", "financial", "finance",
    "industries", "industrial", "limited", "technologies", "technology",
    "systems", "solutions", "services", "global", "national", "general",
    "energies", "energy", "resources", "products", "brands", "stores",
    "motor", "motors", "bank", "banking", "insurance", "capital", "partners",
})

# Registrable-domain suffixes with two labels. Not the full Public Suffix List
# -- a vendored PSL is a dependency this pass does not need -- but every
# multi-label suffix that actually occurs in this universe's jurisdictions.
TWO_LABEL_SUFFIXES = frozenset({
    "co.uk", "org.uk", "ac.uk", "co.jp", "or.jp", "ne.jp", "com.au",
    "com.br", "com.mx", "com.ar", "com.cn", "com.hk", "com.sg", "com.tw",
    "com.tr", "co.kr", "co.in", "co.za", "co.nz", "com.ph", "com.my",
    "com.vn", "co.il", "com.co", "com.pe", "co.th", "com.sa",
    # MEASURED 2026-09-13, and it is the one defect this pass found in its OWN
    # instrument rather than in the world. '.bank.in' is the Reserve Bank of
    # India's exclusive domain for Indian banks, so 'icici.bank.in' is ICICI's
    # registrable domain -- but with 'bank.in' missing from this set the rule
    # returned 'bank.in' and DISCARDED THE ONE LABEL THAT NAMES THE COMPANY.
    # Four results collapsed onto a suffix and test (b) duly elected it.
    # >> The criterion caught it anyway: test (a) named icicibank.com, the two
    #    disagreed, and the conflict branch REFUSED. An extractor defect became
    #    a refusal rather than a wrong answer, which is what fail-closed means.
    "bank.in",
})

# Aggregators, exchanges, social networks and news. A page here is ABOUT the
# company; it is never the company's own IR site.
#
# THIS SET IS A CORRECTION TO THE CRITERION AS WRITTEN, NOT AN EMBELLISHMENT.
# Test (b) says "two or more results share that same registrable domain". Run
# literally, a query returning three LinkedIn posts elects linkedin.com as the
# IR domain -- with the agreement test firing exactly as specified. The
# criterion's INTENT is a domain the company itself operates; the text does not
# say so, and the probe's own result list contained a linkedin.com hit that
# would have been eligible. Disclosed rather than folded in silently.
NON_COMPANY_DOMAINS = frozenset({
    "linkedin.com", "facebook.com", "twitter.com", "x.com", "instagram.com",
    "youtube.com", "tiktok.com", "reddit.com", "wikipedia.org", "wikiwand.com",
    "bloomberg.com", "reuters.com", "ft.com", "wsj.com", "cnbc.com",
    "seekingalpha.com", "marketscreener.com", "investing.com", "yahoo.com",
    "finance.yahoo.com", "nasdaq.com", "nyse.com", "londonstockexchange.com",
    "sec.gov", "stockanalysis.com", "tipranks.com", "simplywall.st",
    "morningstar.com", "zacks.com", "barrons.com", "fool.com", "gurufocus.com",
    "investor.gov", "annualreports.com", "wsj.com", "macrotrends.net",
    "companiesmarketcap.com", "craft.co", "pitchbook.com", "crunchbase.com",
    "glassdoor.com", "indeed.com", "bing.com", "google.com", "msn.com",
    "quartr.com", "sharesmagazine.co.uk", "hl.co.uk", "ii.co.uk",
    "investorrelations.com", "q4inc.com", "notifyir.com", "irmagazine.com",
    # PRESS-RELEASE WIRES. Added 2026-09-13 after the first full pass: a wire
    # carries the company's OWN releases, so it clears the agreement test
    # exactly like a real IR site and is the single most convincing wrong
    # answer available. 'newsfilecorp.com' reached n=2 on Telefonica Brazil and
    # was one result away from being elected.
    "newsfilecorp.com", "globenewswire.com", "prnewswire.com",
    "businesswire.com", "accesswire.com", "einpresswire.com",
    "prnewswire.co.uk", "sec.report",
})


# FOUND BY THE DRY RUN, WHICH IS WHY THE DRY RUN EXISTS. The name rule strips
# trailing Bloomberg-shaped tokens; twice in 89 the stripped token WAS the
# company's identity and what remained was not a company name at all. Both were
# visible in the printed query list before a single call was spent.
#
# These are not a forward list written from recall -- they are the result of
# INSPECTING the printed 89, which is the only reading of Rule 24 that holds.
# Anything not listed here took the rule's output unmodified.
NAME_OVERRIDES = {
    # 'Koninklijke' is Dutch for 'Royal' -- a title carried by Philips, Ahold,
    # KLM and KPN alike. Stripping 'KPN' as an exchange-shaped token left the
    # adjective and discarded the company.
    "Koninklijke KPN NA": ("KPN", "'Koninklijke' is a Dutch honorific shared "
                                  "by many listed companies; 'KPN' is the name"),
    # 'MER' is Meralco's root. Stripped, the query became a city.
    "Manila MER PER": ("Manila Electric", "'Manila' alone is a city; the "
                                          "company is Manila Electric (Meralco)"),
}


def is_root_token(tok: str) -> bool:
    """A Bloomberg-shaped trailing token: all-caps/digits, <=10 chars."""
    return tok == tok.upper() and bool(re.fullmatch(r"[A-Z0-9./]{1,10}", tok))


def company_name(folder: str) -> str:
    """
    The company name is the folder name with its trailing Bloomberg-shaped
    tokens removed -- the exact complement of the identity fallback rule that
    reads those same tokens as a ticker.

        'Adobe ADBE US'                          -> 'Adobe'
        'Mitsubishi UFJ Financial Group 8306 JP' -> 'Mitsubishi UFJ Financial Group'
        'ASML NA'                                -> 'ASML'
        'Nokia FH'                               -> 'Nokia'

    Never strips to empty: a single-token folder keeps its token.

    NAME_OVERRIDES wins where the rule demonstrably produced a non-name.
    """
    if folder in NAME_OVERRIDES:
        return NAME_OVERRIDES[folder][0]
    toks = folder.split()
    while len(toks) > 1 and is_root_token(toks[-1]):
        toks.pop()
    return " ".join(toks)


def name_tokens(name: str) -> list:
    """
    Distinctive tokens for test (a): every word of length >= 4 that is not a
    corporate-furniture word, PLUS the whole name concatenated (so 'Air Liquide'
    matches airliquide.com, which no single word does).
    """
    words = [w for w in re.split(r"[^a-z0-9]+", name.lower()) if w]
    toks = [w for w in words if len(w) >= 4 and w not in STOP_TOKENS]
    concat = "".join(words)
    if len(concat) >= 4 and concat not in toks:
        toks.append(concat)
    # A short one-word name ('ASML', 'SAP', 'Visa') yields nothing above; keep
    # it, because for those the whole name IS the distinctive token.
    if not toks and concat:
        toks.append(concat)
    return toks


def registrable(url: str):
    """eTLD+1 of a result URL, lowercased, 'www.' stripped. None if unparseable."""
    try:
        host = urllib.parse.urlsplit(url).hostname
    except ValueError:
        return None
    if not host:
        return None
    host = host.lower().rstrip(".")
    labels = host.split(".")
    if len(labels) < 2:
        return None
    if len(labels) >= 3 and ".".join(labels[-2:]) in TWO_LABEL_SUFFIXES:
        return ".".join(labels[-3:])
    return ".".join(labels[-2:])


# ------------------------------------------------------------------ the rules

def adjudicate(name: str, results: list, held_domain):
    """
    Apply the s.13 criterion to one company's result list.

    Returns (domain_or_None, status, reasons_dict). The reasons dict is the
    evidence: it names which tests fired, on what, and why anything was
    excluded -- so a reviewer can re-derive the verdict without re-running the
    call that produced it.
    """
    ranked = []
    excluded = []
    for item in results:
        dom = registrable(item.get("link", ""))
        if dom is None:
            continue
        if dom in NON_COMPANY_DOMAINS:
            excluded.append(dom)
            continue
        ranked.append(dom)

    counts = collections.Counter(ranked)
    toks = name_tokens(name)

    # (a) distinctive name token inside the registrable domain
    a_hits = []
    for dom in counts:
        stem = dom.split(".")[0].replace("-", "")
        if any(t in stem for t in toks):
            a_hits.append(dom)

    # (b) two or more surviving results on one registrable domain
    b_hits = [d for d, c in counts.items() if c >= 2]
    top_b = None
    if b_hits:
        best = max(counts[d] for d in b_hits)
        tied = [d for d in b_hits if counts[d] == best]
        top_b = tied[0] if len(tied) == 1 else None

    # (c) a domain already held for this company from another key
    c_hit = held_domain if (held_domain and held_domain in counts) else None

    reasons = {
        "distinctive_tokens": toks,
        "domains_ranked": ranked,
        "domain_counts": dict(counts),
        "excluded_non_company": sorted(set(excluded)),
        "test_a_name_token": sorted(a_hits),
        "test_b_agreement": {d: counts[d] for d in sorted(b_hits)},
        "test_b_tie_unresolved": bool(b_hits and top_b is None),
        "test_c_held_value": c_hit,
    }

    # Conflict: (a) and (b) both fire, on different domains and with no overlap.
    # Neither is trusted over the other -- that is exactly the situation the
    # criterion exists for, so it refuses.
    if a_hits and top_b and top_b not in a_hits:
        reasons["verdict"] = (
            "REFUSED -- test (a) named %s and test (b) named %s; the two "
            "independent tests disagree, so neither is taken."
            % (sorted(a_hits), top_b)
        )
        return None, "UNRESOLVED", reasons

    if a_hits and top_b and top_b in a_hits:
        reasons["verdict"] = "ACCEPTED by (a) AND (b) agreeing on %s" % top_b
        return top_b, "INFERRED", reasons

    if a_hits:
        # More than one domain carries the name token (e.g. a country site and
        # the group site). Prefer the one with the most results; a tie refuses.
        best = max(counts[d] for d in a_hits)
        tied = [d for d in a_hits if counts[d] == best]
        if len(tied) != 1:
            reasons["verdict"] = (
                "REFUSED -- test (a) matched %s with no result-count "
                "separation between them." % sorted(tied)
            )
            return None, "UNRESOLVED", reasons
        reasons["verdict"] = "ACCEPTED by (a) name token in %s" % tied[0]
        return tied[0], "INFERRED", reasons

    if top_b:
        reasons["verdict"] = (
            "ACCEPTED by (b) agreement: %d of %d surviving results on %s"
            % (counts[top_b], len(ranked), top_b)
        )
        return top_b, "INFERRED", reasons

    if c_hit:
        reasons["verdict"] = "ACCEPTED by (c) held value %s present in results" % c_hit
        return c_hit, "INFERRED", reasons

    reasons["verdict"] = (
        "REFUSED -- no test fired. %d result(s) survived exclusion, none "
        "carrying a name token and none appearing twice." % len(ranked)
    )
    return None, "UNRESOLVED", reasons


# ---------------------------------------------------------------- blog branch

# A path or host segment that says "this is the company's own editorial feed".
BLOG_MARKERS = ("blog", "blogs", "news", "newsroom", "stories", "press",
                "insights", "media", "articles")

# A RECRUITING BLOG IS REAL COMPANY CONTENT OF THE WRONG KIND, AND THE MARKER
# TEST CANNOT TELL THE DIFFERENCE. Measured over the first full blog pass: 9 of
# 52 accepted roots were careers or jobs sites --
#     careers.mastercard.com/us/en/blog | jobs.uber.com/en/people-stories
#     careers.msci.com/articles | careers.sse.com/blogs
#     careers.intuitive.com/en/employee-stories
# Every one carries a genuine blog marker AND sits on the company's own domain,
# so both of the rule's tests pass. They are simply not what s.11's chatter axis
# consumes: employee stories do not move a security, and feeding them into a
# market-chatter signal is a CORRECTNESS defect, not untidiness.
# >> INVESTOR-RELATIONS paths are deliberately NOT in this set. A press release
#    IS market-relevant, so investors.intuit.com/news-events stays.
RECRUITING = ("careers", "career", "jobs", "job", "recruiting", "recruitment",
              "talent", "hiring")


def _marks(segment: str) -> bool:
    """
    True if this host label or path segment IS a blog marker, reading a
    hyphen/underscore-joined segment as the words it is made of.

    An EXACT segment match is too strict and an unanchored SUBSTRING match is
    too loose. Measured on the first blog batch: 'press-releases' and
    'media-centre' are unmistakably editorial and fail an exact match, while a
    bare substring test would accept 'newsagents' or 'expressway'. Splitting on
    the separators the segment already uses is the reading that matches how
    these URLs are actually built.
    """
    return any(w in BLOG_MARKERS
               for w in re.split(r"[-_]+", segment) if w)


def adjudicate_blog(held_domain, results: list):
    """
    THE BLOG RULE IS TIGHTER THAN THE IR RULE, AND DELIBERATELY SO.

    By the time this runs the company's registrable domain is ALREADY HELD from
    the IR pass. So test (c) -- 'the domain matches a value already held for
    that company from another key' -- stops being the dead branch it was on the
    IR pass and becomes the PRIMARY and only test:

        A BLOG URL IS ACCEPTED ONLY IF ITS REGISTRABLE DOMAIN EQUALS THE HELD
        ir_domain. Everything else is discarded, whatever its rank.

    That is not a heuristic. It is an identity constraint, and it makes the
    wrong-company failure mode -- the one that forced this whole criterion --
    STRUCTURALLY IMPOSSIBLE here rather than merely unlikely.

    The cost is an honest narrowing: a company with no held ir_domain cannot
    have a blog resolved either, so this layer's denominator is the IR pass's
    resolved count, NOT 89. Said here so the smaller number is not read as a
    worse result.
    """
    if not held_domain:
        return [], "UNRESOLVED", {
            "verdict": "REFUSED -- no ir_domain is held for this company, so "
                       "the only test available cannot run. Resolving the IR "
                       "domain is the prerequisite, not more searching.",
            "held_domain": None,
        }

    on_domain, off_domain = [], []
    for item in results:
        link = item.get("link", "")
        dom = registrable(link)
        if dom == held_domain:
            on_domain.append(link)
        elif dom:
            off_domain.append(dom)

    hosts = []
    recruiting = []
    for link in on_domain:
        parts = urllib.parse.urlsplit(link)
        host = (parts.hostname or "").lower()
        segs = [s for s in (parts.path or "").lower().split("/") if s]

        # A recruiting site disqualifies the root outright, however good its
        # blog marker is. Recorded separately rather than dropped silently,
        # so the count of what was excluded is visible.
        words = [w for part in host.split(".") + segs
                 for w in re.split(r"[-_]+", part) if w]
        if any(w in RECRUITING for w in words):
            recruiting.append(link)
            continue

        # A marker in the HOST makes the whole host the blog root.
        if any(_marks(lbl) for lbl in host.split(".")):
            root = host
        else:
            # A marker in the PATH makes the root the prefix UP TO AND
            # INCLUDING that segment.
            #
            # THIS USED TO TAKE segs[0] AND THAT WAS WRONG IN 3 OF THE FIRST 7.
            # On a localized site the first segment is the LOCALE, not the
            # blog: asml.com/en/news/... yielded 'www.asml.com/en', and
            # astrazeneca.com/content/.../news yielded '.../content'. Each is a
            # real URL prefix, so nothing errored and nothing looked wrong --
            # the value was simply not a blog. Found by reading the seven
            # outputs instead of reading the "4 of 7 accepted" line above them.
            idx = next((k for k, sg in enumerate(segs) if _marks(sg)), None)
            if idx is None:
                continue
            root = host + "/" + "/".join(segs[:idx + 1])
        if root not in hosts:
            hosts.append(root)

    reasons = {
        "held_domain": held_domain,
        "results_on_held_domain": len(on_domain),
        "results_off_held_domain": sorted(set(off_domain)),
        # STORED so a later repair to this rule can be replayed offline at ZERO
        # call cost -- which is exactly what the IR pass's stored domain list
        # bought, and what this branch did not have when it needed it.
        "on_domain_links": on_domain,
        "excluded_recruiting": recruiting,
        "blog_roots": hosts,
    }
    if hosts:
        reasons["verdict"] = (
            "ACCEPTED -- %d blog root(s) on the held domain %s, out of %d "
            "result(s) that were on it at all." % (len(hosts), held_domain,
                                                   len(on_domain))
        )
        return hosts, "INFERRED", reasons
    reasons["verdict"] = (
        "REFUSED -- %d result(s) landed on the held domain %s but none carried "
        "a blog/news/press marker in its host or path. A company may simply not "
        "run a public editorial feed; that is a finding, not a gap."
        % (len(on_domain), held_domain)
    )
    return [], "UNRESOLVED", reasons


# ------------------------------------------------------------------- the call

def cse_search(key: str, cx: str, query: str, num: int = 10):
    params = urllib.parse.urlencode(
        {"key": key, "cx": cx, "q": query, "num": num}
    )
    req = urllib.request.Request(
        ENDPOINT + "?" + params,
        headers={"User-Agent": "opal-cro-ir-pass/1.0"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        # The URL carries the key. Never let it into an error string.
        raise RuntimeError(
            "HTTP %s from customsearch (body withheld: the request URL "
            "carries the key)" % exc.code
        ) from None
    except Exception as exc:
        raise RuntimeError("%s from customsearch" % type(exc).__name__) from None
    return payload


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true",
                    help="derive and print every query; make NO call")
    ap.add_argument("--limit", type=int, default=0, help="0 = all")
    ap.add_argument("--offset", type=int, default=0)
    ap.add_argument("--folders", default="",
                    help="path to a newline-delimited list of folder names -- "
                         "for running a deliberately ADVERSARIAL first batch "
                         "rather than an alphabetical one")
    ap.add_argument("--exclude-done", default="",
                    help="path to a prior output JSON; its folders are skipped "
                         "so no name is paid for twice")
    ap.add_argument("--out", default="")
    ap.add_argument("--sleep", type=float, default=0.3)
    ap.add_argument("--mode", choices=("ir", "blog"), default="ir",
                    help="blog mode REQUIRES --held-domains: a company with no "
                         "resolved ir_domain cannot have a blog resolved, so "
                         "the blog denominator is the IR pass's resolved "
                         "count, never 89")
    ap.add_argument("--held-domains", default="",
                    help="path to the IR pass output, read for its resolved "
                         "ir_domain values")
    args = ap.parse_args()

    universe = json.load(open(UNIVERSE, encoding="utf-8"))
    names = universe["names"]

    by_folder = {r["folder"]: r for r in names}

    held_domains = {}
    if args.mode == "blog":
        if not args.held_domains:
            print("ERROR: --mode blog requires --held-domains.", file=sys.stderr)
            return 2
        prior = json.load(open(args.held_domains, encoding="utf-8"))
        for r in prior["records"]:
            v = (r.get("ir_domain") or {}).get("value")
            if v:
                held_domains[r["folder"]] = v
        print("HELD DOMAINS   %d of %d -- THE BLOG DENOMINATOR IS %d, NOT %d. "
              "A name with no resolved ir_domain cannot have a blog resolved."
              % (len(held_domains), len(names), len(held_domains), len(names)))

    if args.folders:
        wanted = [ln.strip() for ln in
                  open(args.folders, encoding="utf-8").read().splitlines()
                  if ln.strip()]
        missing = [w for w in wanted if w not in by_folder]
        if missing:
            print("ERROR: %d folder(s) not in the universe: %s"
                  % (len(missing), missing), file=sys.stderr)
            return 2
        targets = [by_folder[w] for w in wanted]
    else:
        targets = names[args.offset:]
        if args.limit:
            targets = targets[:args.limit]

    if args.mode == "blog":
        before = len(targets)
        targets = [t for t in targets if t["folder"] in held_domains]
        print("NO HELD DOMAIN %d target(s) dropped -- refused by the IR "
              "pass, so not paid for again here" % (before - len(targets)))

    skipped = 0
    if args.exclude_done:
        prior = json.load(open(args.exclude_done, encoding="utf-8"))
        # SKIP ONLY WHAT WAS GENUINELY ANSWERED. This limb used to skip every
        # folder PRESENT in the prior output, which silently included the ones
        # the vendor had refused -- so a resume would carry a quota wall forward
        # forever as though it were a finding. Sixth instance of this class in
        # one session, and this time in the script the others copied it FROM.
        key = "blog_roots" if args.mode == "blog" else "ir_domain"
        done = {r["folder"] for r in prior["records"]
                if not str((r.get(key) or {}).get("evidence", ""))
                .lstrip().upper().startswith(("NOT ASKED", "GOOGLE CSE CALL FAILED"))}
        retried = len(prior["records"]) - len(done)
        before = len(targets)
        targets = [t for t in targets if t["folder"] not in done]
        skipped = before - len(targets)
        print("CARRIED        %d already-ANSWERED folder(s) skipped" % len(done))
        print("RETRIED        %d folder(s) the vendor refused -- never answered"
              % retried)

    print("UNIVERSE       %s" % UNIVERSE)
    print("DENOMINATOR    %d folders" % len(names))
    print("THIS BATCH     %d (offset %d, limit %s, already-done skipped %d)"
          % (len(targets), args.offset, args.limit or "none", skipped))
    if NAME_OVERRIDES:
        print("NAME OVERRIDES %d of %d, each from dry-run inspection:"
              % (len(NAME_OVERRIDES), len(names)))
        for folder, (nm, why) in sorted(NAME_OVERRIDES.items()):
            print("               %-24s -> %-18s (%s)" % (folder, nm, why))

    if args.dry_run:
        print("MODE           DRY RUN -- zero calls\n")
        for rec in targets:
            nm = company_name(rec["folder"])
            if args.mode == "blog":
                print("  %-42s -> q=%-26s held=%s"
                      % (rec["folder"], '"%s blog"' % nm,
                         held_domains.get(rec["folder"])))
            else:
                print("  %-42s -> q=%-38s tokens=%s"
                      % (rec["folder"], '"%s investor relations"' % nm,
                         name_tokens(nm)))
        return 0

    raw = sys.stdin.read().strip()
    if not raw:
        print("ERROR: no secret on stdin.", file=sys.stderr)
        return 2
    try:
        secret = json.loads(raw)
        key, cx = secret["google_api_key"], secret["google_cse_id"]
    except Exception:
        print("ERROR: stdin was not the expected google-cse-config JSON "
              "(value withheld).", file=sys.stderr)
        return 2
    del raw, secret

    print("MODE           LIVE -- one call per name, num=10\n")
    out = []
    spent = 0
    accepted = 0
    failed = 0
    for i, rec in enumerate(targets, 1):
        folder = rec["folder"]
        nm = company_name(folder)
        held = held_domains.get(folder) if args.mode == "blog" \
            else (rec.get("ir_domain") or {}).get("value")
        key_name = "blog_roots" if args.mode == "blog" else "ir_domain"
        query = ("%s blog" % nm) if args.mode == "blog" \
            else ("%s investor relations" % nm)
        try:
            payload = cse_search(key, cx, query)
            spent += 1
        except RuntimeError as exc:
            print("  [%2d] %-40s CALL FAILED: %s" % (i, folder, exc))
            out.append({
                "folder": folder, "company_name": nm, "query": query,
                key_name: {
                    "value": None, "status": "UNRESOLVED",
                    "evidence": "Google CSE call failed: %s" % exc,
                    "resolved_at": datetime.datetime.utcnow()
                                   .strftime("%Y-%m-%dT%H:%MZ"),
                },
            })
            failed += 1
            if failed >= 3:
                print("\n  STOPPING: 3 consecutive-or-more call failures. A "
                      "quota wall or a credential fault is not something to "
                      "spend the rest of the batch discovering one call at a "
                      "time.")
                break
            continue
        failed = 0

        items = payload.get("items", []) or []
        total = (payload.get("searchInformation", {}) or {}).get("totalResults")
        if args.mode == "blog":
            dom, status, reasons = adjudicate_blog(held, items)
            crit = ("the blog root's registrable domain must EQUAL the "
                    "ir_domain already held for this company -- test (c) of "
                    "s.13, which the IR pass could not use and this pass can.")
        else:
            dom, status, reasons = adjudicate(nm, items, held)
            crit = ("a domain is accepted only if independently tied to the "
                    "company, never by rank.")
        if status == "INFERRED":
            accepted += 1

        evidence = (
            "Google Custom Search (customsearch/v1), SEARCH ONLY, under "
            "Andrew-direct 2026-09-13 ~04:0xZ card 4. Query %r, %d result(s) "
            "returned of %s reported. Acceptance criterion "
            "HARVEST_BACKFILL_PLAN_20260911_Z.md s.13: %s %s"
            % (query, len(items), total, crit, reasons["verdict"])
        )
        out.append({
            "folder": folder,
            "company_name": nm,
            "query": query,
            "results_returned": len(items),
            key_name: {
                "value": dom,
                "status": status,
                "evidence": evidence,
                "resolved_at": datetime.datetime.utcnow()
                               .strftime("%Y-%m-%dT%H:%MZ"),
            },
            "adjudication": reasons,
        })
        shown = dom if isinstance(dom, str) else (
            ", ".join(dom)[:28] if dom else None)
        print("  [%2d] %-40s %-28s %s"
              % (i, folder, shown or "-- UNRESOLVED --", reasons["verdict"][:70]))
        if args.sleep:
            time.sleep(args.sleep)

    print("\nCALLS SPENT    %d" % spent)
    print("ACCEPTED       %d of %d" % (accepted, len(out)))
    print("REFUSED        %d of %d  <- a 0 here means the criterion is NOT "
          "discriminating" % (len(out) - accepted, len(out)))

    if args.out:
        with open(args.out, "w", encoding="utf-8", newline="\n") as fh:
            json.dump({
                "artifact": ("blog_roots DISCOVERY PASS" if args.mode == "blog"
                             else "ir_domain RESOLUTION PASS")
                            + " -- Google Custom Search",
                "author": "4.0.0_SA_CRO~Z",
                "generated_at": datetime.datetime.utcnow()
                                .strftime("%Y-%m-%dT%H:%MZ"),
                "authority": "Andrew-direct 2026-09-13 ~04:0xZ, card 4 of "
                             "'all recs approved': the Google Custom Search "
                             "key for IR and blog search, SEARCH ONLY.",
                "criterion": "HARVEST_BACKFILL_PLAN_20260911_Z.md s.13",
                "provider": "googleapis.com/customsearch/v1 -- ONE provider, "
                            "ONE purpose. No result page was fetched.",
                "universe": UNIVERSE,
                "name_derivation": "the company name is the folder name with "
                                   "its trailing Bloomberg-shaped tokens "
                                   "removed -- the complement of the identity "
                                   "fallback rule that reads those same tokens "
                                   "as a ticker.",
                "name_overrides": {k: {"name": v[0], "reason": v[1]}
                                   for k, v in NAME_OVERRIDES.items()},
                "name_overrides_note": "found by the zero-call dry run over all "
                                       "89 derived queries, not by recall: in "
                                       "two folders the stripped token WAS the "
                                       "company's identity and the residual was "
                                       "not a company name.",
                "excluded_non_company_domains": sorted(NON_COMPANY_DOMAINS),
                "excluded_note": "test (b) as written in s.13 says only 'two or "
                                 "more results share that same registrable "
                                 "domain'. Run literally it would elect "
                                 "linkedin.com for a company with three "
                                 "LinkedIn hits. Aggregators, exchanges, social "
                                 "networks and news are excluded before the "
                                 "tests run. THIS IS A CORRECTION TO THE "
                                 "CRITERION, disclosed rather than folded in.",
                "denominator": {
                    "universe": len(names),
                    "batch": len(out),
                    "offset": args.offset,
                    "calls_spent": spent,
                    "accepted": accepted,
                    "refused": len(out) - accepted,
                },
                "records": out,
            }, fh, indent=2, ensure_ascii=True)
        print("WROTE          %s" % args.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
