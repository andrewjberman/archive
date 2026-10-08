"""HVST-bn-1 (round 69): AIG's stored name made its full legal name, the three names left cut repaired or each said why not,
and the FINAL rank-universe files built by ONE script.

Three modes (run from the repo root of the worktree: PYTHONPATH=. python <this file> [mode]):

  (no argument)  BUILD, offline and deterministic. Reads the round-47 files, the frozen inputs beside this file
                 (`bn1_stored_sources.json`, `bn1_article_scan.json`), `lib/research/identity/registrations.json`,
                 `lib/research/harvest/universe_securities.py` and the collector's own `publishers.slug_query` /
                 `slug_queries`. Writes `rank_universe_20261008.json` and `rank_universe_identity_20261008.json` into
                 `0.9.0_WK_AMGT_HARVST~120/` (the dated final files; round 47 and `config.json` are never written), then
                 prints the report. Running it twice yields the same bytes.
  --fetch-stored READ-ONLY S3 GETs (the pool universe `universe/v1/2026-10-06.json`, the latest crosswalk) and a run of
                 `bm1_three_universes.py` into a SCRATCH directory (so the 8 added records are re-derived, not copied);
                 writes `bn1_stored_sources.json`.
  --fetch-scan   READ-ONLY: every silver article through `publication_gold._iter_latest_articles()`; writes
                 `bn1_article_scan.json` (all titles + the raw spans that begin with each cut value). ~15-20 minutes.

NO put, NO delete, NO vendor, NO publisher, NO Bloomberg, NO collector / driver / emitter / job.
"""

import collections
import contextlib
import hashlib
import importlib.util
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, *([os.pardir] * 7)))
sys.path.insert(0, ROOT)

DELIV = os.path.join(ROOT, "org", "missions", "D5", "AMGT", "AMGT_HARVST", "deliverables")
W120 = os.path.join(DELIV, "0.9.0_WK_AMGT_HARVST~120")
R47 = os.path.join(DELIV, "2.0.0_SA_COO_H", "round47")
R47_SNAPSHOT = os.path.join(R47, "rank_universe_20261005.json")
R47_IDENTITY = os.path.join(R47, "rank_universe_identity_20261005.json")
W94_IDENTITY = os.path.join(DELIV, "0.9.0_WK_AMGT_HARVST~94", "rank_universe_identity_20260916.json")
NEW_SNAPSHOT = os.path.join(W120, "rank_universe_20261008.json")
NEW_IDENTITY = os.path.join(W120, "rank_universe_identity_20261008.json")
BM1_SCRIPT = os.path.join(W120, "bm1_three_universes.py")
BM2_SCRIPT = os.path.join(W120, "bm2_truncated_names.py")
REGISTRATIONS = os.path.join(ROOT, "lib", "research", "identity", "registrations.json")
STORED_SOURCES = os.path.join(HERE, "bn1_stored_sources.json")
ARTICLE_SCAN = os.path.join(HERE, "bn1_article_scan.json")
OUT_FILE = os.path.join(HERE, "bn1_names_made_whole.out")

AUTHOR = "0.9.0_WK_AMGT_HARVST~121"
BUCKET = "opal-data-harvest"
UNIVERSE_KEY = "universe/v1/2026-10-06.json"
MIN_ARTICLES = 3
AIG = "AIG_US_Equity"
THREE_CUT = ("ICT_US_Equity", "OMAB_US_Equity", "OMAB_MM_Equity")
KEYS = (AIG,) + THREE_CUT
CUT_VALUE = {  # the value each record stores in the round-47 file (read back and compared in build())
    "AIG_US_Equity": "American International Group I",
    "ICT_US_Equity": "International Container Termin",
    "OMAB_US_Equity": "Grupo Aeroportuario del Centro",
    "OMAB_MM_Equity": "Grupo Aeroportuario del Centro",
}
ADJACENT = {"ICT_US_Equity": "ICT_PM_Equity"}  # a key that is named, never used as a source
SEP = r"[\s,.\-]+"
HIT_TAIL = 110  # characters of text kept after the matched prefix in the scan

# a token whose letters-only fold is one of these ends a corporate name; `de` + one of them continues it (S.A.B. de C.V.)
TERMINATORS = {"inc", "incorporated", "corp", "corporation", "co", "company", "ltd", "limited", "plc", "llc", "lp",
               "sa", "sab", "cv", "ag", "nv", "ab", "asa", "oyj", "spa", "se", "bv", "gmbh", "kk", "pcl", "tbk"}
CONNECTORS = {"de", "del", "of", "and", "y", "the", "la", "el", "&"}


# ---------------------------------------------------------------------------------------------------------------------
# small helpers
# ---------------------------------------------------------------------------------------------------------------------
def load(path):
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def dump(value):
    return json.dumps(value, indent=2, ensure_ascii=True) + "\n"


def _refuse_live_collector_pointer(path):
    """Row AMGT_HARVST-Z-W120-S3, disarmed by row AMGT_HARVST-Z-S105 (2.0.0_SA_COO~H): a file that
    lib/opal_data_harvest/config.json names is the LIVE collector list, and re-running this record script would silently
    revert the repairs made to it after this script ran. Writing it is refused."""
    root = os.path.dirname(os.path.abspath(__file__))
    while not os.path.exists(os.path.join(root, "lib", "opal_data_harvest", "config.json")):
        parent = os.path.dirname(root)
        if parent == root:
            return
        root = parent
    with open(os.path.join(root, "lib", "opal_data_harvest", "config.json"), encoding="utf-8") as handle:
        config = json.load(handle)
    target = os.path.normcase(os.path.abspath(path))
    for value in config.values():
        if isinstance(value, str) and target == os.path.normcase(os.path.abspath(os.path.join(root, value))):
            raise SystemExit("REFUSED: %s is a live collector pointer in config.json (row AMGT_HARVST-Z-W120-S3)" % path)


def write_text(path, text):
    _refuse_live_collector_pointer(path)
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)


def fold(text):
    return re.sub(r"[^a-z0-9]+", " ", str(text).lower()).strip()


def import_file(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def prefix_pattern(value):
    """Regex for the cut value as it may be WRITTEN in text: words in order, any run of space/comma/period/hyphen between
    them, the LAST word as a prefix of a word (the cut value may end inside one: `Group I` -> `Group, Inc.`)."""
    words = re.findall(r"[A-Za-z0-9]+", value)
    body = SEP.join(re.escape(w) for w in words[:-1]) + (SEP if len(words) > 1 else "")
    return re.compile(r"(?<![A-Za-z0-9])" + body + re.escape(words[-1]) + r"[A-Za-z0-9]*", re.IGNORECASE)


PATTERNS = {value: prefix_pattern(value) for value in sorted(set(CUT_VALUE.values()))}


def block_text(block):
    if isinstance(block, str):
        return block
    if isinstance(block, dict):
        for field in ("text", "content", "value"):
            if isinstance(block.get(field), str):
                return block[field]
    return ""


# ---------------------------------------------------------------------------------------------------------------------
# --fetch-scan: the silver read
# ---------------------------------------------------------------------------------------------------------------------
def fetch_scan():
    from lib.research.harvest import publication_gold

    needles = {value: value.split()[0].lower() for value in PATTERNS}
    titles, hits = [], {value: [] for value in PATTERNS}
    per_publisher = collections.Counter()
    total = 0
    for row in publication_gold._iter_latest_articles():
        total += 1
        per_publisher[row.get("publisher") or "?"] += 1
        key = row.get("article_key")
        title = row.get("title") if isinstance(row.get("title"), str) else ""
        titles.append([key, title])
        pieces = [title] + [block_text(b) for b in (row.get("text_blocks") or [])]
        for value, pattern in PATTERNS.items():
            found = 0
            for piece in pieces:
                if needles[value] not in piece.lower():
                    continue
                for match in pattern.finditer(piece):
                    tail = piece[match.start():match.end() + HIT_TAIL]
                    hits[value].append([key, re.sub(r"\s+", " ", tail)])
                    found += 1
                    if found >= 6:
                        break
                if found >= 6:
                    break
        if total % 1000 == 0:
            print("scanned %d articles" % total, flush=True)
    doc = {"artifact": "HVST-bn-1 silver scan (read-only; lib.research.harvest.publication_gold._iter_latest_articles)",
           "author": AUTHOR, "articles": total, "per_publisher": dict(sorted(per_publisher.items())),
           "patterns": {v: p.pattern for v, p in PATTERNS.items()}, "hit_tail_characters": HIT_TAIL,
           "titles": titles, "hits": hits}
    write_text(ARTICLE_SCAN, dump(doc))
    print("WROTE %s: %d articles, hits per cut value %s"
          % (os.path.basename(ARTICLE_SCAN), total, {v: len(h) for v, h in hits.items()}))
    return 0



# ---------------------------------------------------------------------------------------------------------------------
# --fetch-stored: the pool + crosswalk reads, and bm-1 re-run into a scratch directory
# ---------------------------------------------------------------------------------------------------------------------
FROZEN_KEYS = KEYS + ("ICT_PM_Equity", "KCDMY_US_Equity")


def fetch_stored():
    import boto3
    from lib.research.identity import crosswalk as crosswalk_mod

    client = boto3.client("s3", region_name="us-east-1")
    body = client.get_object(Bucket=BUCKET, Key=UNIVERSE_KEY)["Body"].read()
    pool = json.loads(body.decode("utf-8"))
    cw_doc, cw_key = crosswalk_mod._read_pool_latest(client)
    pool_by = {}
    for record in pool["names"]:
        if record.get("security_key") in FROZEN_KEYS:
            pool_by.setdefault(record["security_key"], []).append(record)
    cw_by = {r["security_key"]: r for r in cw_doc["records"] if r["security_key"] in FROZEN_KEYS}
    roots = {k.split("_")[0] for k in FROZEN_KEYS}
    keyless = [{"ticker": n.get("ticker"), "name": n.get("name"), "source": n.get("source"), "resolution": n.get("resolution")}
               for n in pool["names"] if not n.get("security_key") and n.get("ticker") in roots]
    crosswalk = {}
    for key, rec in sorted(cw_by.items()):
        crosswalk[key] = {"legal_name": rec.get("legal_name"),
                          "coverage_source": rec["source_row"].get("coverage_source"),
                          "bloomberg_ticker_evidence": rec["source_row"]["bloomberg_ticker"].get("evidence")}

    scratch = os.path.join(ROOT, ".scratch", "bn1_stage")
    os.makedirs(scratch, exist_ok=True)
    bm1 = import_file("bm1_three_universes", BM1_SCRIPT)
    bm1.NEW_SNAPSHOT = os.path.join(scratch, "rank_universe_20261008.json")
    bm1.NEW_IDENTITY = os.path.join(scratch, "rank_universe_identity_20261008.json")
    sink = io.StringIO()
    with contextlib.redirect_stdout(sink):
        rc = bm1.main()
    last = [line for line in sink.getvalue().splitlines() if line.strip()][-1]
    old_snap, old_ident = load(R47_SNAPSHOT), load(R47_IDENTITY)
    stage_snap, stage_ident = load(bm1.NEW_SNAPSHOT), load(bm1.NEW_IDENTITY)
    n_s, n_i = len(old_snap["entries"]), len(old_ident["records"])
    if rc != 0 or last != "RECONCILE OK":
        raise SystemExit("ERROR: bm-1 re-run did not reconcile: rc=%s last line %r" % (rc, last))
    if stage_snap["entries"][:n_s] != old_snap["entries"] or stage_ident["records"][:n_i] != old_ident["records"]:
        raise SystemExit("ERROR: the bm-1 re-run changed a round-47 entry or record")
    snapshot_doc = dict(stage_snap)
    snapshot_doc["entries"] = stage_snap["entries"][n_s:]
    identity_doc = dict(stage_ident)
    identity_doc["records"] = stage_ident["records"][n_i:]
    doc = {
        "artifact": "HVST-bn-1 frozen stored sources (read-only GETs; bm-1 re-derived into a scratch directory)",
        "author": AUTHOR,
        "pool": {"s3": "s3://%s/%s" % (BUCKET, UNIVERSE_KEY), "sha256": hashlib.sha256(body).hexdigest(),
                 "names": len(pool["names"]), "records": {k: pool_by.get(k, []) for k in FROZEN_KEYS},
                 "keyless_holdings_for_these_roots": keyless},
        "crosswalk": {"s3": "s3://%s/%s" % (BUCKET, cw_key), "as_of": cw_doc.get("as_of"),
                      "records_in_object": len(cw_doc["records"]), "records": crosswalk,
                      "sha256_of_the_frozen_records": hashlib.sha256(dump(crosswalk).encode("utf-8")).hexdigest()},
        "bm1_rerun": {"last_line": last, "round47_entries": n_s, "round47_records": n_i,
                      "added_entries": len(snapshot_doc["entries"]), "added_records": len(identity_doc["records"])},
        "snapshot_doc": snapshot_doc,
        "identity_doc": identity_doc,
    }
    write_text(STORED_SOURCES, dump(doc))
    print("WROTE %s: pool %d names (sha256 %s), crosswalk %s (%d records), bm-1 re-run: %s, %d entries and %d records added"
          % (os.path.basename(STORED_SOURCES), len(pool["names"]), doc["pool"]["sha256"], cw_key,
             len(cw_doc["records"]), last, len(snapshot_doc["entries"]), len(identity_doc["records"])))
    return 0


# ---------------------------------------------------------------------------------------------------------------------
# article completions (from the frozen scan)
# ---------------------------------------------------------------------------------------------------------------------
def _letters(token):
    return re.sub(r"[^a-z]", "", token.lower())


def parse_completion(raw, value):
    """The company name as WRITTEN, starting at the cut value: `raw` begins at the matched prefix. The span runs on through
    capitalised words (and the connectors de/del/of/and) to a corporate suffix (`Inc.`, `S.A.B. de C.V.`), or to the end of
    the name: a lower-case word, a bracket, or a comma not followed by a corporate suffix. Returns the written name or None."""
    match = PATTERNS[value].match(raw)
    if not match:
        return None
    end = match.end()
    last_word = re.findall(r"[A-Za-z0-9]+", match.group(0))[-1]
    terminated = _letters(last_word) in TERMINATORS
    if terminated and raw[end:end + 1] == ".":
        end += 1
    rest = raw[end:]
    consumed = 0
    previous_comma = False
    tokens = list(re.finditer(r"\S+", rest))
    index = 0
    while index < len(tokens) and consumed < 8:
        token = tokens[index]
        text = token.group(0)
        core = text.strip(".,;:\"'")
        folded = _letters(core)
        if not core or text.startswith("("):
            break
        next_folded = _letters(tokens[index + 1].group(0)) if index + 1 < len(tokens) else ""
        if terminated:
            ok = folded in TERMINATORS or (folded == "de" and next_folded in TERMINATORS)
        elif folded in TERMINATORS:
            ok = True
        elif folded in CONNECTORS:
            ok = True
        else:
            ok = core[0].isupper() or core[0].isdigit()
        if previous_comma and folded not in TERMINATORS:
            ok = False
        if not ok:
            break
        if folded in TERMINATORS:
            terminated = True
        end = (len(raw) - len(rest)) + token.end()
        consumed += 1
        index += 1
        previous_comma = text.endswith(",")
        if text.endswith(".") and folded not in TERMINATORS and folded not in CONNECTORS and not core.isupper():
            break  # a sentence-final period after a capitalised word that is not a legal form
        if text[-1:] in ";:)":
            break
    span = raw[:end].strip()
    if _letters(span.split()[-1]) in TERMINATORS:
        span = span.rstrip(",;:")
    else:
        span = span.rstrip(".,;:")
    return span


def article_completions(scan, value):
    """{folded completion: {"count": distinct articles, "articles": sorted keys, "forms": Counter of written forms}}"""
    out = {}
    for key, raw in scan["hits"].get(value, []):
        span = parse_completion(raw, value)
        if not span:
            continue
        item = out.setdefault(fold(span), {"articles": set(), "forms": collections.Counter()})
        item["articles"].add(key)
        item["forms"][span] += 1
    result = {}
    for folded, item in out.items():
        form = sorted(item["forms"].items(), key=lambda kv: (-kv[1], kv[0]))[0][0]
        result[folded] = {"count": len(item["articles"]), "articles": sorted(item["articles"]), "form": form}
    return result


def ranked(completions):
    return sorted(completions.values(), key=lambda c: (-c["count"], c["form"]))


# ---------------------------------------------------------------------------------------------------------------------
# the sources, in the order the cell names them
# ---------------------------------------------------------------------------------------------------------------------
SEC_QUOTE = re.compile(r"cik \d+ from the SEC ticker-to-CIK table on root '[^']*' \('([^']*)'\)")


def is_completion(cut, name):
    return isinstance(name, str) and len(fold(name)) > len(fold(cut)) and fold(name).startswith(fold(cut))


def why_not(cut, name):
    if fold(name) == fold(cut):
        return "same as the stored value: not a fuller name"
    if len(fold(name)) < len(fold(cut)):
        return "SHORTER than the stored value (itself cut): not a source"
    return "does not begin with the stored value: not a completion"


def stored_candidates(key, cut, ss, registrations, old94, snap_entry=None, clean=None):
    """[{"n", "label", "held", "note", "usable"}] in the cell's order: the pool record (its name, then the SEC name its
    resolution_reason quotes), the pool record as the round-47 collector snapshot read it, registrations.json, the crosswalk
    record (legal_name, then the SEC name its evidence quotes), the older identity file. `held` is the string the source
    holds for this EXACT key, or None (ABSENT); a pool name has its trailing ticker removed by the builder's own
    `clean_company`, as `bm2_truncated_names.py` does."""
    clean = clean or (lambda name, ticker: name)
    out = []
    pool = ss["pool"]["records"].get(key) or []
    pool_rec = pool[0] if pool else None
    ticker = (pool_rec or {}).get("ticker")
    raw = (pool_rec or {}).get("name")
    note = "pool record present, name null" if pool_rec and not raw else ("no pool record for this key" if not pool_rec else "")
    out.append({"n": "1", "label": "pool record name (%s names[] key %s, source=%s)"
                % (ss["pool"]["s3"], key, (pool_rec or {}).get("source", "n/a")),
                "held": clean(raw, ticker) if raw else None, "note": note})
    quote = SEC_QUOTE.search((pool_rec or {}).get("resolution_reason") or "")
    out.append({"n": "1b", "label": "same pool record, resolution_reason: the SEC ticker-to-CIK name it quotes",
                "held": quote.group(1) if quote else None, "note": ""})
    snap_name = (snap_entry or {}).get("name")
    out.append({"n": "1c", "label": "pool record as the round-47 snapshot read it (rank_universe_20261005.json entries[].name, from "
                "universe/v1/2026-09-16.json), trailing ticker removed",
                "held": clean(snap_name, (snap_entry or {}).get("ticker")) if snap_name else None, "note": ""})
    reg = registrations.get(key)
    out.append({"n": "2", "label": "lib/research/identity/registrations.json identity.name",
                "held": ((reg or {}).get("identity") or {}).get("name"), "note": "" if reg else "no registration for this key"})
    cw = ss["crosswalk"]["records"].get(key)
    legal = ((cw or {}).get("legal_name") or {}).get("value")
    out.append({"n": "3", "label": "crosswalk record legal_name (%s, via lib/research/identity/crosswalk.py)"
                % ss["crosswalk"]["s3"], "held": legal, "note": ""})
    quote = SEC_QUOTE.search((cw or {}).get("bloomberg_ticker_evidence") or "")
    out.append({"n": "3b", "label": "crosswalk record source_row.bloomberg_ticker.evidence: the SEC ticker-to-CIK name it quotes",
                "held": quote.group(1) if quote else None, "note": ""})
    old = old94.get(key)
    out.append({"n": "4", "label": "older identity file 0.9.0_WK_AMGT_HARVST~94/rank_universe_identity_20260916.json company.value",
                "held": (old or {}).get("company", {}).get("value"), "note": "" if old else "no record for this key"})
    for item in out:
        item["usable"] = is_completion(cut, item["held"])
    return out


def agreeing(cut, completions):
    """(chosen completion dict | None, reason). A completion is a span that EXTENDS the cut value; the same completion
    (folded) must stand in at least MIN_ARTICLES distinct articles, and be the only one that does."""
    extended = {f: c for f, c in completions.items() if len(f) > len(fold(cut))}
    order = ranked(extended)
    strong = [c for c in order if c["count"] >= MIN_ARTICLES]
    listing = "; ".join("%r in %d articles" % (c["form"], c["count"]) for c in order[:8])
    if not extended:
        return None, "none found"
    if not strong:
        return None, "completions found [%s] none reaches %d distinct articles" % (listing, MIN_ARTICLES)
    if len(strong) > 1:
        return None, "completions found [%s] do not agree" % listing
    return strong[0], "agree"


def analyse_key(key, ss, scan, registrations, old94, snap_entry, clean):
    cut = CUT_VALUE[key]
    candidates = stored_candidates(key, cut, ss, registrations, old94, snap_entry, clean)
    completions = article_completions(scan, cut)
    chosen, why = agreeing(cut, completions)
    usable = [c for c in candidates if c["usable"]]
    result = {"key": key, "cut": cut, "candidates": candidates, "completions": completions, "agreement": why}
    if usable:
        first = usable[0]
        written = [c for f, c in completions.items() if f == fold(first["held"]) and c["count"] >= MIN_ARTICLES]
        name = written[0]["form"] if written else first["held"]
        result.update(repaired=True, name=name, source=first["n"] + " " + first["label"], held=first["held"],
                      corroborated=written[0] if written else None, article_only=False)
    elif chosen:
        result.update(repaired=True, name=chosen["form"], source="5 article spans (silver)", held=None,
                      corroborated=chosen, article_only=True)
    else:
        result.update(repaired=False, name=None, source=None, held=None, corroborated=None, article_only=False)
    return result


def verdict_line(res):
    if res["repaired"]:
        text = '%s: REPAIRED to "%s" -- source %s' % (res["key"], res["name"], res["source"])
        if res["article_only"]:
            text += " evidenced by article spans only; articles %s" % ", ".join(res["corroborated"]["articles"][:MIN_ARTICLES])
        elif res["corroborated"]:
            text += "; written form read from %d articles, e.g. %s" % (
                res["corroborated"]["count"], ", ".join(res["corroborated"]["articles"][:MIN_ARTICLES]))
        return text
    return "%s: NOT REPAIRED -- no stored source carries it; %s" % (res["key"], res["agreement"])


def evidence_text(res):
    cut = res["cut"]
    base = "HVST-bn-1: the stored value %r (%d characters, the identity record's cut length) is completed to its full name" % (
        cut, len(cut))
    if res["article_only"]:
        return ("%s; no stored source carries it; evidenced by article spans only: the same completion %r in %d distinct "
                "silver articles (%s)" % (base, res["name"], res["corroborated"]["count"],
                                          ", ".join(res["corroborated"]["articles"][:MIN_ARTICLES])))
    text = "%s; source %s holds %r" % (base, res["source"], res["held"])
    if res["corroborated"]:
        text += ("; the written form %r is the form %d distinct silver articles carry for the same name (%s)"
                 % (res["name"], res["corroborated"]["count"], ", ".join(res["corroborated"]["articles"][:MIN_ARTICLES])))
    else:
        text += "; the stored source's own string is used as written"
    return text


def made_whole(record, res):
    rec = json.loads(json.dumps(record))
    rec["company"] = {"value": res["name"], "status": "DERIVED", "evidence": evidence_text(res)}
    rec["aliases"] = {"value": [res["name"]], "status": "DERIVED",
                      "evidence": "the repaired company name alone (build_rank_identity.py rule for a non-pilot record)"}
    return rec


# ---------------------------------------------------------------------------------------------------------------------
# the query shown to match
# ---------------------------------------------------------------------------------------------------------------------
def core_name(name):
    words = re.findall(r"[A-Za-z0-9]+", name)
    while len(words) > 1 and _letters(words[-1]) in TERMINATORS:
        words.pop()
    return " ".join(words)


def query_block(res, scan, publishers):
    name = res["name"]
    lines = []
    q = publishers.slug_query(name)
    qs = publishers.slug_queries({"company": name, "aliases": [name]})
    lines.append("  slug_query(%r) = %r" % (name, q))
    lines.append("  slug_queries({'company': %r, 'aliases': [%r]}) = %r" % (name, name, qs))
    qwords = fold(q).split()
    phrase = fold(core_name(name))
    pattern = re.compile(r"(?<![a-z0-9])" + re.escape(phrase) + r"(?![a-z0-9])")
    carry, others = [], []
    for key, title in scan["titles"]:
        folded = fold(title)
        has_all = all(w in set(folded.split()) for w in qwords)
        if pattern.search(folded):
            carry.append((key, title, has_all))
        elif has_all:
            others.append((key, title))
    n = sum(1 for _k, _t, h in carry if h)
    spans = len(scan["hits"].get(res["cut"], []))
    lines.append("  QUERY MATCHES: %d of %d held article titles that carry the full name (%r, legal form dropped) contain "
                 "every query word (%s)" % (n, len(carry), core_name(name), ", ".join(qwords)))
    if not carry:
        lines.append("  NO HELD TITLE CARRIES THE FULL NAME, so there is nothing to show the query matching in the %d held "
                     "titles (the scan found %d spans beginning with the cut value in title or body text)"
                     % (len(scan["titles"]), spans))
    for key, title, _h in sorted(carry)[:5]:
        lines.append("    carry: [%s] %s" % (key, title[:150]))
    if res["article_only"]:
        title_of = dict((k, ttl) for k, ttl in scan["titles"])
        arts = res["corroborated"]["articles"]
        full = sum(1 for a in arts if all(w in set(fold(title_of.get(a, "")).split()) for w in qwords))
        lines.append("  ARTICLES CARRYING THE FULL NAME ANYWHERE IN TITLE OR BODY (the completion read from them): %d; of those, "
                     "titles containing every query word: %d" % (len(arts), full))
    lines.append("  OTHER COMPANIES' TITLES CONTAINING EVERY QUERY WORD: %d (of the %d held titles, those that contain every "
                 "query word and do not carry the full name)" % (len(others), len(scan["titles"])))
    for key, title in sorted(others)[:5]:
        lines.append("    other: [%s] %s" % (key, title[:150]))
    dropped = [w for w in fold(core_name(name)).split() if w not in qwords]
    limit = bool(dropped) or len(others) >= max(len(carry), 1)
    if limit:
        reasons = []
        if dropped:
            reasons.append("the query DROPS %s of the full name (publishers._LEGAL_SUFFIX strips trailing legal-suffix words, "
                           "`group` among them)" % ", ".join(repr(w) for w in dropped))
        if len(others) >= max(len(carry), 1):
            reasons.append("%d titles contain every query word without the full name against %d that carry it"
                           % (len(others), len(carry)))
        lines.append("  THE QUERY IS STILL NOT SPECIFIC: " + "; ".join(reasons) + ". lib/opal_data_harvest is NOT changed here "
                     "(a collector code change is a different cell).")
        lines.append("  STORED FIELDS THAT COULD CARRY A BETTER SEARCH FORM UNDER THE BUILDER'S OWN RULES: none that narrows. "
                     "`company` is always the first query; `aliases` (and a plane=slug brand in whole_brand_aliases.json) each pass "
                     "through the same slug_query and are tried as ADDITIONAL queries, a slug being a candidate when it matches "
                     "ANY ONE (publishers.slug_queries, discovery.discover), so an alias can only widen the search, never narrow it.")
    else:
        lines.append("  THE QUERY IS SPECIFIC: it keeps every word of the full name and few other titles contain all its words.")
    return lines, {"query": q, "queries": qs, "n": n, "m": len(carry), "k": len(others), "limit": limit}


# ---------------------------------------------------------------------------------------------------------------------
# BUILD
# ---------------------------------------------------------------------------------------------------------------------
def git_show(rel):
    import subprocess
    done = subprocess.run(["git", "show", "HEAD:" + rel], cwd=ROOT, capture_output=True)
    if done.returncode != 0:
        raise SystemExit("ERROR: git show HEAD:%s rc=%d" % (rel, done.returncode))
    return done.stdout


def compute():
    """Pure: reads the frozen inputs and the round-47 files, returns the two files' bytes and the report. No writes."""
    from lib.opal_data_harvest import publishers
    from lib.research.harvest import universe_securities as gold

    ss, scan = load(STORED_SOURCES), load(ARTICLE_SCAN)
    old_snap, old_ident = load(R47_SNAPSHOT), load(R47_IDENTITY)
    registrations = {r["security_key"]: r for r in load(REGISTRATIONS)["registrations"] if r.get("security_key")}
    old94 = {r["security_key"]: r for r in load(W94_IDENTITY)["records"]}
    bm2 = import_file("bm2_truncated_names", BM2_SCRIPT)
    clean = bm2._builder().clean_company
    snap_by = {e["security_key"]: e for e in old_snap["entries"]}
    r47_by = {r["security_key"]: r for r in old_ident["records"]}
    for key, cut in CUT_VALUE.items():
        if r47_by[key]["company"]["value"] != cut:
            raise SystemExit("ERROR: round-47 %s holds %r, expected %r" % (key, r47_by[key]["company"]["value"], cut))

    out = []
    say = out.append
    say("HVST-bn-1 -- stored names made whole, from stored sources only (no vendor, no publisher, no Bloomberg, no job)")
    say("DENOMINATORS: round-47 identity records %d, entries %d; silver articles scanned %d (%s); pool names %d; crosswalk "
        "records %d (%s)" % (len(old_ident["records"]), len(old_snap["entries"]), scan["articles"],
                             ", ".join("%s %d" % kv for kv in scan["per_publisher"].items()), ss["pool"]["names"],
                             ss["crosswalk"]["records_in_object"], ss["crosswalk"]["s3"]))
    say("FROZEN INPUTS: %s (pool sha256 %s; crosswalk as_of %s; bm-1 re-run: %s), %s"
        % (os.path.basename(STORED_SOURCES), ss["pool"]["sha256"], ss["crosswalk"]["as_of"], ss["bm1_rerun"]["last_line"],
           os.path.basename(ARTICLE_SCAN)))
    say("ARTICLE RULE: a span begins with the cut value (words in order, any space/comma/period between, the last word as a "
        "word prefix) and runs through capitalised words and de/del/of/and to a corporate suffix (Inc., Corp., S.A.B. de "
        "C.V.) or to the end of the name; the SAME completion (case/punctuation folded) in at least %d distinct articles, "
        "and no other completion that reaches %d." % (MIN_ARTICLES, MIN_ARTICLES))
    results = {}
    verdicts = []
    for key in KEYS:
        res = analyse_key(key, ss, scan, registrations, old94, snap_by.get(key), clean)
        results[key] = res
        say("")
        say("== %s == stored (round 47): %r (%d characters)" % (key, res["cut"], len(res["cut"])))
        for item in res["candidates"]:
            if item["held"] is None:
                state = "ABSENT" + (" (%s)" % item["note"] if item["note"] else "")
            elif item["usable"]:
                state = "%r -- COMPLETES the stored value" % item["held"]
            else:
                state = "%r -- %s" % (item["held"], why_not(res["cut"], item["held"]))
            say("  source %s %s: %s" % (item["n"], item["label"], state))
        for held in ss["pool"].get("keyless_holdings_for_these_roots", []):
            if held["ticker"] == key.split("_")[0]:
                say("  (not this exact key: a key-less pool holding record for ticker root %r, resolution %s, source %s, holds %r%s)"
                    % (held["ticker"], held["resolution"], held["source"], held["name"],
                       " -- the same cut string, no fuller name" if held["name"] == res["cut"] else ""))
        comps = res["completions"]
        hits = len(scan["hits"].get(res["cut"], []))
        say("  source 5 article spans (silver, %d articles; scan hits for this cut value: %d): %s"
            % (scan["articles"], hits,
               "; ".join("%r in %d articles" % (c["form"], c["count"]) for c in ranked(comps)[:10]) or "none found"))
        say("  article agreement: %s" % res["agreement"])
        if key == "ICT_US_Equity":
            adj = ss["pool"]["records"].get(ADJACENT[key]) or []
            reg = registrations.get(ADJACENT[key])
            say("  ALREADY RULED: whether ICT_US_Equity and %s are one issuer is not shown by any field and is not inferred; a "
                "name read for the Manila listing is not a source for the US key. Named, NOT used: %s pool name %r, "
                "registrations.json identity.name %r." % (ADJACENT[key], ADJACENT[key], adj[0].get("name") if adj else None,
                                                          ((reg or {}).get("identity") or {}).get("name")))
        verdicts.append(verdict_line(res))
        say("  VERDICT " + verdicts[-1])

    # ---- the files ---------------------------------------------------------------------------------------------
    records = []
    changed = []
    for rec in old_ident["records"]:
        new = rec
        key = rec["security_key"]
        if key == "KCDMY_US_Equity":  # bm-2 rule B, the same function calls: the suffix fragment dropped
            value = rec["company"]["value"]
            if gold.suffix_fragment(value) is None or any(
                    c["usable"] for c in stored_candidates(key, value, ss, registrations, old94, snap_by.get(key), clean)):
                raise SystemExit("ERROR: KCDMY_US_Equity is not the cut-fragment case bm-2 repaired")
            name, fragment = gold.cut_legal_name_fragment(value, value)
            new = bm2.rebuilt(rec, name, "suffix fragment %r dropped by universe_securities.cut_legal_name_fragment" % fragment,
                              "cut inside a corporate suffix, no stored source carries a fuller name")
        elif key in results and results[key]["repaired"]:
            if (rec["aliases"].get("evidence") or "").startswith(bm2.PILOT_EVIDENCE):
                raise SystemExit("ERROR: %s is a config.json pilot record" % key)
            new = made_whole(rec, results[key])
        if new is not rec:
            changed.append(key)
        records.append(new)

    snapshot = dict(ss["snapshot_doc"])
    snapshot["entries"] = old_snap["entries"] + ss["snapshot_doc"]["entries"]
    ident = dict(ss["identity_doc"])
    added = ss["identity_doc"]["records"]
    ident["records"] = records + added
    repaired_now = sorted(k for k in KEYS if results[k]["repaired"])
    ident["rules"] = list(ident["rules"]) + [
        "",
        "HVST-bn-1 (round 69, %s): this file and rank_universe_20261008.json are now built in ONE run by" % AUTHOR,
        "0.9.0_WK_AMGT_HARVST~121/bn1_names_made_whole.py from the round-47 files, bm-1's 8 added records, bm-2's KCDMY repair",
        "(suffix fragment dropped) and N2: a record whose company is cut at 30 characters takes the FULL name from, in order, the",
        "pool record, registrations.json identity.name, the crosswalk record, the older identity file, and last the company's own",
        "name in at least %d distinct silver articles (evidence says `evidenced by article spans only`); a source that is itself" % MIN_ARTICLES,
        "cut shorter than the stored value is not a source. A record with no such source stays as stored and is listed NOT REPAIRED.",
    ]
    ident["name_repairs"] = {"cells": ["HVST-bm-2", "HVST-bn-1"], "built_by": "0.9.0_WK_AMGT_HARVST~121/bn1_names_made_whole.py",
                             "changed_against_round47": sorted(changed),
                             "made_whole_by_bn1": repaired_now,
                             "not_repaired_by_bn1": sorted(k for k in KEYS if not results[k]["repaired"])}
    files = {NEW_SNAPSHOT: dump(snapshot).encode("utf-8"), NEW_IDENTITY: dump(ident).encode("utf-8")}

    say("")
    say("RECORDS CHANGED AGAINST ROUND 47: %d %s" % (len(changed), ", ".join(sorted(changed))))
    for key in sorted(changed):
        before = r47_by[key]["company"]["value"]
        after = next(r for r in records if r["security_key"] == key)["company"]["value"]
        say("  %s: company %r -> %r" % (key, before, after))
    say("RECORDS ADDED: %d" % len(added))
    if len(snapshot["entries"]) != len(ident["records"]) or snapshot["names_considered"] != len(snapshot["entries"]):
        raise SystemExit("ERROR: snapshot and identity do not cover the same count")

    queries = {}
    for key in KEYS:
        res = results[key]
        if not res["repaired"]:
            continue
        say("")
        say("QUERY FOR %s (stored name %r):" % (key, res["name"]))
        lines, facts = query_block(res, scan, publishers)
        out.extend(lines)
        queries[key] = facts
    return {"files": files, "report": out, "results": results, "verdicts": verdicts, "changed": changed,
            "added": len(added), "queries": queries, "records": ident["records"]}


def main():
    if "--fetch-scan" in sys.argv:
        return fetch_scan()
    if "--fetch-stored" in sys.argv:
        return fetch_stored()
    first = compute()
    second = compute()
    identical = first["files"] == second["files"] and first["report"] == second["report"]
    for path, data in first["files"].items():
        with open(path, "wb") as handle:
            handle.write(data)
    again = {}
    for path in first["files"]:
        with open(path, "rb") as handle:
            again[path] = handle.read()
    identical = identical and again == first["files"]
    lines = list(first["report"])
    lines.append("")
    lines.append("BUILD TWICE: %s (sha256 %s)" % ("byte-identical" if identical else "DIFFERENT",
                                                  ", ".join("%s %s" % (os.path.basename(p), hashlib.sha256(d).hexdigest())
                                                            for p, d in sorted(first["files"].items()))))
    untouched = True
    for rel in ("lib/opal_data_harvest/config.json",
                "org/missions/D5/AMGT/AMGT_HARVST/deliverables/2.0.0_SA_COO_H/round47/rank_universe_20261005.json",
                "org/missions/D5/AMGT/AMGT_HARVST/deliverables/2.0.0_SA_COO_H/round47/rank_universe_identity_20261005.json"):
        with open(os.path.join(ROOT, rel.replace("/", os.sep)), "rb") as handle:
            same = git_show(rel) == handle.read()
        untouched = untouched and same
        lines.append("UNCHANGED against git show HEAD: %s: %s" % (rel, same))
    failures = []
    aig = first["results"][AIG]
    if not aig["repaired"]:
        failures.append("AIG_US_Equity not repaired: " + aig["agreement"])
    for key in THREE_CUT:
        if not any(v.startswith(key + ": ") for v in first["verdicts"]):
            failures.append("no verdict line for " + key)
    if not identical:
        failures.append("the two builds are not byte-identical")
    if not untouched:
        failures.append("config.json or a round-47 file differs from HEAD")
    if first["added"] != 8:
        failures.append("RECORDS ADDED %d != 8" % first["added"])
    lines.append("NAMES OK" if not failures else "NAMES FAIL: " + "; ".join(failures))
    text = "\n".join(lines) + "\n"
    write_text(OUT_FILE, text)
    sys.stdout.write(text)
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
