"""HARVST round 44 HVST-aq-1 -- FWD-2 field census (READ ONLY: S3 list/get only, no write, no vendor call).

FWD-2 DONE WHEN: "every field present in the received article (including language, paywall flags, the publisher's own
ticker tags, sentiment, themes and summary where sent) appears typed in the queryable table, rebuilt from the stored
original, and a query by company and date returns it".

For each publisher (harvest_grammar.SOURCE_FOR_PUBLISHER):
1. LIST every bronze `article` object (the stored originals); take a bounded, deterministic sample (<= 50, stratified by
   extension, evenly spaced over the sorted keys). The denominator is printed.
2. Parse each sampled original into field LEAVES (path, value). JSON objects: the whole document. HTML pages: the embedded
   `__NEXT_DATA__` JSON, every JSON-LD object, the <meta> tags and the <html lang> attribute.
   Each leaf is classed (A) ARTICLE -- inside the subtree the silver builder treats as the article -- or (B) PAGE -- the rest
   of the page the publisher sent alongside it.
3. Stream every silver `article` part and keep the row whose `bronze_key` is the sampled object (the row REBUILT from
   that stored original).
4. A leaf is KEPT TYPED when the silver row carries a typed leaf with the same final field name and the same value (a
   timestamp string matches its parsed datetime; an empty struct matches the null the builder writes), KEPT AS TEXT when it
   is found only inside a JSON-text column (`page_config_json`), else MISSING.
5. The named kinds (language, paywall flags, ticker tags, sentiment, themes, summary) are matched by final field name.
6. Query by company and date: one sampled article per publisher is fetched through the gold `article_security_mention`
   pairs for one (security_key, UTC date) and `silver_from_bronze.rows_by_company_mention`, and its named-kind fields are
   printed from the returned row.

Writes `round44/aq-1.field_census.json`; prints the summary (redirect to `aq-1.field_census.out`).
"""
import collections
import datetime
import io
import json
import math
import os
import re
import subprocess
import sys

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip()
sys.path.insert(0, ROOT)
HERE = os.path.dirname(os.path.abspath(__file__))

import pyarrow.parquet as pq  # noqa: E402
from bs4 import BeautifulSoup  # noqa: E402

from lib.opal_data_harvest import harvest_grammar as hg  # noqa: E402
from lib.opal_data_harvest import silver_from_bronze as sfb  # noqa: E402
from lib.opal_data_harvest.publishers import json_fields  # noqa: E402
from lib.research.harvest import publication_gold as pg  # noqa: E402
from lib.research.harvest import store  # noqa: E402

SAMPLE = 50
OUT = os.path.join(HERE, "aq-1.field_census.json")
DERIVED = {"article_key", "publisher", "article_id", "title", "text_blocks", "published_utc", "published_offset_min",
           "published_date_utc", "published_precision", "bronze_key", "fetched_at", "retrieval_mode", "run_stamp",
           "first_discovered_at", "retrieval_rung", "search_query", "search_rank", "search_page", "discovered_for",
           "record_hash", "page_config_json"}
KINDS = {
    "language": re.compile(r"^(lang|language|inlanguage|locale|html_lang)$|language", re.I),
    "paywall": re.compile(r"paywall|accessibleforfree|accesslevel|premium|locked|isfree|subscriber|metered|access_?type"
                          r"|^ispro$|^pro$|prostatus", re.I),
    "ticker_tags": re.compile(r"ticker|symbol|instrument|isin|cusip|figi|securit", re.I),
    "sentiment": re.compile(r"sentiment|bullish|bearish", re.I),
    "themes": re.compile(r"theme|topic|keyword|^tags?$|section|categor|subject", re.I),
    "summary": re.compile(r"summary|abstract|^dek$|description|teaser|standfirst|synopsis|subhead|^lede$", re.I),
}
_ISO = re.compile(r"^\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}")


def leaves(obj, prefix=""):
    if isinstance(obj, dict):
        if not obj:
            yield prefix, {}
        for k, v in obj.items():
            yield from leaves(v, "%s.%s" % (prefix, k) if prefix else str(k))
    elif isinstance(obj, list):
        if not obj:
            yield prefix, []
        for v in obj:
            yield from leaves(v, prefix + "[]")
    else:
        yield prefix, obj


def last_key(path):
    p = path
    while p.endswith("[]"):
        p = p[:-2]
    return p.rsplit(".", 1)[-1]


def segments(path):
    return [s for s in re.sub(r"\[[^\]]*\]", "", path).split(".") if s]


def variants(v):
    out = set()
    if v is None or v == {}:
        out.add(("null",))
    elif isinstance(v, bool):
        out.add(("b", v))
    elif isinstance(v, (int, float)):
        f = float(v)
        out.add(("n", "nan" if math.isnan(f) else repr(f)))
    elif isinstance(v, datetime.datetime):
        dt = v if v.tzinfo else v.replace(tzinfo=datetime.timezone.utc)
        out.add(("t", dt.timestamp()))
    elif isinstance(v, datetime.date):
        out.add(("s", v.isoformat()))
    elif isinstance(v, list) and not v:
        out.add(("[]",))
    elif isinstance(v, bytes):
        out.add(("s", v.decode("utf-8", "replace")))
    else:
        s = str(v)
        out.add(("s", s))
        if _ISO.match(s):
            try:
                out.add(("t", hg.parse_timestamp(s).timestamp()))
            except (ValueError, TypeError):
                pass
    return out


def index(row_obj):
    idx = set()
    for path, v in leaves(row_obj):
        k = last_key(path)
        for var in variants(v):
            idx.add((k, var))
    return idx


def received_leaves(pub, key, body, form):
    """[(path, value, cls)] -- cls 'A' (article subtree the builder reads) or 'B' (rest of the page)."""
    ext = key.rsplit(".", 1)[-1]
    out = []
    if ext == "json":
        doc = json.loads(body.decode("utf-8"))
        return [(p, v, "A") for p, v in leaves(doc)], ext
    html = body.decode("utf-8", "replace")
    soup = BeautifulSoup(html, "html.parser")
    tag = soup.find("html")
    if tag is not None and tag.get("lang"):
        out.append(("html_lang", tag.get("lang"), "B"))
    for m in soup.find_all("meta"):
        name = m.get("name") or m.get("property") or m.get("itemprop")
        if name and m.get("content") is not None:
            out.append(("html_meta.%s" % name, m.get("content"), "B"))
    node = soup.select_one("script#__NEXT_DATA__")
    nd = None
    if node:
        try:
            nd = json.loads(node.string or node.get_text())
        except (ValueError, TypeError):
            nd = None
    article_prefix = None
    if pub == "wsj":
        article_prefix = "__NEXT_DATA__.props.pageProps.articleData"
    elif pub == "bbg" and nd is not None:
        story = ((nd.get("props") or {}).get("pageProps") or {}).get("story")
        if isinstance(story, dict) and story:
            article_prefix = "__NEXT_DATA__.props.pageProps.story"
    if nd is not None:
        for p, v in leaves(nd, "__NEXT_DATA__"):
            out.append((p, v, "A" if article_prefix and (p == article_prefix or p.startswith(article_prefix + "."))
                        else "B"))
    ld_article_done = False
    for i, item in enumerate(json_fields(html)):
        is_article = (not ld_article_done and isinstance(item.get("articleBody"), str) and item["articleBody"].strip()
                      and (pub == "ft" or (pub == "bbg" and article_prefix is None)))
        if is_article:
            ld_article_done = True
        for p, v in leaves(item, "ld[%d]" % i):
            out.append((p, v, "A" if is_article else "B"))
    return out, ext


def sample_keys(keys):
    by_ext = collections.defaultdict(list)
    for k in sorted(keys):
        by_ext[k.rsplit(".", 1)[-1]].append(k)
    total = len(keys)
    picked = []
    for ext, ks in sorted(by_ext.items()):
        n = min(len(ks), max(3, round(SAMPLE * len(ks) / total)))
        step = len(ks) / n
        picked += [ks[int(i * step)] for i in range(n)]
    return picked[:max(SAMPLE, len(by_ext) * 3)]


def list_keys(client, prefix):
    keys = []
    for page in client.get_paginator("list_objects_v2").paginate(Bucket=store.HARVEST_BUCKET, Prefix=prefix):
        keys += [o["Key"] for o in page.get("Contents", []) or []]
    return keys


def main():
    client = store._default_client()
    mention = pg._latest_gold_snapshot_rows(pg.GOLD_TABLE)
    mention_by_key = collections.defaultdict(list)
    for r in mention:
        mention_by_key[r.get("article_key")].append(r)
    result = {"measured_at": datetime.datetime.now(datetime.timezone.utc).isoformat(), "sample_cap": SAMPLE,
              "gold_mention_rows": len(mention), "publishers": {}}
    for pub, src in sorted(hg.SOURCE_FOR_PUBLISHER.items()):
        bronze_keys = [k for k in list_keys(client, store.table_prefix(src, "bronze", "article"))
                       if not k.endswith("/")]
        picked = sample_keys(bronze_keys)
        # silver: stream every part, keep the rows rebuilt from a picked bronze object
        want = set(picked)
        silver_by_bronze = {}
        silver_parts = [k for k in list_keys(client, store.table_prefix(src, "silver", "article")) if k.endswith(".parquet")]
        silver_columns = set()
        for sk in silver_parts:
            raw = client.get_object(Bucket=store.HARVEST_BUCKET, Key=sk)["Body"].read()
            table = pq.read_table(io.BytesIO(raw))
            silver_columns.update(table.column_names)
            if "bronze_key" not in table.column_names:
                continue
            for row in table.to_pylist():
                bk = row.get("bronze_key")
                if bk in want and (bk not in silver_by_bronze or str(row.get("run_stamp")) > str(silver_by_bronze[bk].get("run_stamp"))):
                    silver_by_bronze[bk] = row
        paths = collections.defaultdict(lambda: {"cls": None, "carried": 0, "typed": 0, "text_only": 0, "elsewhere": 0,
                                                 "missing": 0, "missing_example": None})
        forms = collections.Counter()
        exts = collections.Counter()
        no_silver = []
        parse_errors = []
        for bk in picked:
            obj = client.get_object(Bucket=store.HARVEST_BUCKET, Key=bk)
            body = obj["Body"].read()
            form = store.classify_bronze_form(obj.get("Metadata"))
            forms[form] += 1
            try:
                rec, ext = received_leaves(pub, bk, body, form)
            except Exception as exc:  # noqa: BLE001 -- a parse failure is reported, never hidden
                parse_errors.append([bk, type(exc).__name__])
                continue
            exts[ext] += 1
            srow = silver_by_bronze.get(bk)
            if srow is None:
                no_silver.append(bk)
                continue
            typed_idx = index({k: v for k, v in srow.items() if k != "page_config_json"})
            typed_values = {x for _k, x in typed_idx}
            text_idx = set()
            if isinstance(srow.get("page_config_json"), str):
                try:
                    text_idx = index(json.loads(srow["page_config_json"]))
                except ValueError:
                    pass
            per_path = collections.defaultdict(lambda: {"cls": None, "states": set(), "value": None})
            for path, v, cls in rec:
                k = last_key(path)
                vs = variants(v)
                if any((k, x) in typed_idx for x in vs):
                    st = "typed"
                elif any((k, x) in text_idx for x in vs):
                    st = "text"
                elif isinstance(v, str) and len(v) >= 8 and ("s", v) in typed_values:
                    st = "elsewhere"
                else:
                    st = "missing"
                norm_path = re.sub(r"ld\[\d+\]", "ld[article]" if cls == "A" else "ld[other]", path)
                pp = per_path[norm_path]
                pp["cls"] = pp["cls"] or cls
                pp["states"].add(st)
                if st == "missing" and pp["value"] is None:
                    pp["value"] = str(v)[:80]
            for path, pp in per_path.items():
                agg = paths[path]
                agg["cls"] = agg["cls"] or pp["cls"]
                agg["carried"] += 1
                if "missing" in pp["states"]:
                    agg["missing"] += 1
                    agg["missing_example"] = agg["missing_example"] or pp["value"]
                elif "elsewhere" in pp["states"]:
                    agg["elsewhere"] += 1
                elif "text" in pp["states"]:
                    agg["text_only"] += 1
                else:
                    agg["typed"] += 1
        compared = len(picked) - len(no_silver) - len(parse_errors)
        a_missing = {p: d for p, d in paths.items() if d["cls"] == "A" and d["missing"]}
        a_groups = collections.Counter(segments(p)[0] if segments(p) else p for p in a_missing)
        b_missing = {p: d for p, d in paths.items() if d["cls"] == "B" and (d["missing"] or d["text_only"] or d["elsewhere"])}
        kinds = {}
        for kind, rx in KINDS.items():
            hits = {p: d for p, d in paths.items() if any(rx.search(seg) for seg in segments(p))}
            kinds[kind] = {
                "paths_sent": len(hits),
                "paths_typed_everywhere": sorted(p for p, d in hits.items() if d["typed"] == d["carried"]),
                "paths_not_typed": {p: {k: d[k] for k in ("cls", "carried", "typed", "text_only", "elsewhere",
                                                            "missing", "missing_example")}
                                    for p, d in hits.items() if d["typed"] < d["carried"]},
            }
        # query by company and date (step 6)
        query = None
        for bk in picked:
            srow = silver_by_bronze.get(bk)
            if srow is None:
                continue
            pairs = mention_by_key.get(srow.get("article_key")) or []
            if not pairs:
                continue
            sec = pairs[0]["security_key"]
            day = str(pairs[0].get("published_utc"))[:10]
            day_pairs = [r for r in mention if r.get("security_key") == sec and str(r.get("published_utc"))[:10] == day]
            got, unjoined = sfb.rows_by_company_mention(sec, day_pairs, list(silver_by_bronze.values()))
            hit = next((r for r in got if r.get("article_key") == srow.get("article_key")), None)
            named = {}
            if hit is not None:
                for path, v in leaves({k: v for k, v in hit.items() if k not in DERIVED}):
                    for kind, rx in KINDS.items():
                        if any(rx.search(seg) for seg in segments(path)) and v not in (None, [], {}, ""):
                            named.setdefault(kind, set()).add(re.sub(r"\[\]", "", path))
            query = {"security_key": sec, "utc_date": day, "mention_pairs_that_day": len(day_pairs),
                     "article_key": srow.get("article_key"), "returned": hit is not None,
                     "title": (hit or {}).get("title"),
                     "named_kind_fields_non_null": {k: sorted(v)[:12] for k, v in named.items()}}
            break
        result["publishers"][pub] = {
            "source": src, "bronze_objects": len(bronze_keys), "sampled": len(picked), "sample_exts": dict(exts),
            "sample_forms": dict(forms), "silver_parts_read": len(silver_parts), "silver_columns": len(silver_columns),
            "no_silver_row_for_sampled_bronze": no_silver, "parse_errors": parse_errors, "compared": compared,
            "distinct_paths": len(paths),
            "article_paths": sum(1 for d in paths.values() if d["cls"] == "A"),
            "article_missing_top_level_groups": dict(a_groups.most_common()),
            "article_paths_missing": {p: {k: d[k] for k in ("carried", "missing", "missing_example")}
                                      for p, d in sorted(a_missing.items())},
            "page_paths": sum(1 for d in paths.values() if d["cls"] == "B"),
            "page_paths_not_typed": len(b_missing),
            "page_paths_not_typed_sample": {p: {k: d[k] for k in ("carried", "text_only", "elsewhere", "missing",
                                                                  "missing_example")}
                                            for p, d in sorted(b_missing.items())[:60]},
            "named_kinds": kinds, "query_by_company_and_date": query,
        }
        r = result["publishers"][pub]
        print("=== %s (%s): bronze %d, sampled %d %s forms %s; silver parts %d; no silver row %d; parse errors %d; compared %d"
              % (pub, src, r["bronze_objects"], r["sampled"], r["sample_exts"], r["sample_forms"], r["silver_parts_read"],
                 len(no_silver), len(parse_errors), compared))
        print("  paths: %d distinct; ARTICLE %d (missing in >=1 object: %d); PAGE %d (not typed: %d)"
              % (r["distinct_paths"], r["article_paths"], len(a_missing), r["page_paths"], r["page_paths_not_typed"]))
        print("  ARTICLE missing top-level groups (%d): %s" % (len(a_groups), dict(a_groups.most_common(40))))
        for p, d in list(sorted(a_missing.items(), key=lambda x: -x[1]["missing"]))[:15]:
            print("    ARTICLE MISSING %s  missing %d/%d  e.g. %r" % (p, d["missing"], d["carried"], d["missing_example"]))
        for kind, kd in kinds.items():
            nt = kd["paths_not_typed"]
            print("  %-11s sent paths %d; typed everywhere %d; NOT typed %d %s"
                  % (kind, kd["paths_sent"], len(kd["paths_typed_everywhere"]), len(nt),
                     ["%s[%s m%d e%d t%d/%d]" % (p, d["cls"], d["missing"], d["elsewhere"], d["text_only"], d["carried"])
                      for p, d in list(nt.items())[:8]]))
        print("  query by company+date: %s" % json.dumps(query, default=str)[:600])
    json.dump(result, open(OUT, "w", encoding="utf-8"), indent=1, default=str)
    print("RECORD:", OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
