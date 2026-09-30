"""HVST-m-1 AC2 - FWD-2 MEASURED: the field names present in bronze (the received article) versus
the columns present in the silver row built from it, per publisher; the named fields (language,
paywall flags, ticker tags, sentiment, themes, summary) as SENT-AND-KEPT / SENT-AND-LOST / NOT SENT;
and one query by company and date over silver. READ-ONLY (list/get). Measures; grades nothing.

Field-set definitions (stated so the numbers can be re-derived):
  normalised_record JSON  -> the record's top-level keys.
  as_received / unlabelled SA JSON:API (data/included/meta) -> data.attributes.* names, the other
      data.* keys, the sub-keys of data.relationships, 'included' and 'meta.*'.
  as_received HTML (wsj)  -> NOT MEASURABLE HERE as a field set (raw page; fields exist only after
      extraction). For the named fields a TOKEN census over the raw text is printed and labelled so.
Kept means: a silver column of the same name in the part holding the row; a relationships sub-key is
kept if the silver 'relationships' cell names it; for HTML the token is kept if it also appears in the
silver row's string cells.
"""

import datetime
import json
import re

import m1_common as C

NAMED = (
    ("language", re.compile(r"^(language|lang|locale|inlanguage)$", re.I)),
    ("paywall flags", re.compile(r"paywall|locked|accessibleforfree", re.I)),
    ("ticker tags", re.compile(r"ticker|symbol|tag|securit|compan", re.I)),
    ("sentiment", re.compile(r"sentiment", re.I)),
    ("themes", re.compile(r"theme", re.I)),
    ("summary", re.compile(r"summary|description|standfirst|abstract|dek$", re.I)),
)
HTML_KEY = re.compile(r"""(?:\\?["'])([A-Za-z_][A-Za-z0-9_]{1,60})(?:\\?["'])\s*:""")


def bronze_fields(doc):
    """(field set, kind, relationships sub-keys) for a parsed JSON bronze document."""
    if isinstance(doc, dict) and "data" in doc and isinstance(doc["data"], dict):
        fields = set()
        rel = set()
        data = doc["data"]
        for k, v in data.items():
            if k == "attributes" and isinstance(v, dict):
                fields.update(v.keys())
            elif k == "relationships" and isinstance(v, dict):
                fields.add("relationships")
                rel.update(v.keys())
            else:
                fields.add(k)
        if "included" in doc:
            fields.add("included")
        meta = doc.get("meta")
        if isinstance(meta, dict):
            fields.update("meta." + k for k in meta.keys())
        elif meta is not None:
            fields.add("meta")
        return fields, "jsonapi", rel
    if isinstance(doc, dict):
        return set(doc.keys()), "record", set()
    return set(), "other", set()


def norm(v):
    if isinstance(v, datetime.datetime):
        return v.astimezone(datetime.timezone.utc).isoformat()
    if isinstance(v, (list, dict)):
        return json.dumps(v, sort_keys=True, default=str)
    return None if v is None else str(v)


def equal(bronze_v, silver_v):
    if isinstance(silver_v, datetime.datetime) and isinstance(bronze_v, str):
        try:
            b = datetime.datetime.fromisoformat(bronze_v.replace("Z", "+00:00"))
            if b.tzinfo is None:
                b = b.replace(tzinfo=datetime.timezone.utc)
            return b == silver_v
        except ValueError:
            return False
    return norm(bronze_v) == norm(silver_v)


def type_family(t):
    s = str(t)
    for fam in ("timestamp", "bool", "int", "double", "float", "list", "struct", "date"):
        if s.startswith(fam):
            return fam
    return "string" if "string" in s else s


def main():
    lines = ["FWD-2 MEASURED (read-only; bronze field names vs the silver row built from each article)"]
    result = {}
    for pub, store in C.PUBLISHERS:
        lines.append("")
        lines.append("=== publisher %s ===" % pub)
        arts = C.bronze_articles(store)
        silver, unreadable = C.silver_row_dicts(store)
        by_bronze = {}
        for pk, row, cols in silver:
            by_bronze[row.get("bronze_key")] = (row, cols)
        # silver schema variants
        variants = C.Counter()
        typefam = {}
        for _pk, tbl, _e in C.silver_rows(store):
            if tbl is None:
                continue
            sig = tuple(tbl.schema.names)
            variants[sig] += 1
            typefam[sig] = C.Counter(type_family(t) for t in tbl.schema.types)
        lines.append("silver article parts: %d; distinct column sets: %d (unreadable parts %d)" % (sum(variants.values()), len(variants), len(unreadable)))
        for sig, n in variants.items():
            lines.append("    column set of %d columns in %d parts; types: %s" % (len(sig), n, C.counter_line(typefam[sig])))
        rows = []
        for key, _size in arts:
            body, meta = C.get(key)
            form = C.received_form(meta)
            rows.append((key, body, form))
        n = len(rows)
        fieldrows = []  # (key, fields, kind, rel, form, body_text)
        html_n = 0
        unparsed = 0
        for key, body, form in rows:
            if body is None:
                unparsed += 1
                continue
            if key.endswith(".html"):
                html_n += 1
                fieldrows.append((key, None, "html", set(), form, body.decode("utf-8", "replace")))
                continue
            try:
                doc = json.loads(body)
            except ValueError:
                unparsed += 1
                continue
            f, kind, rel = bronze_fields(doc)
            fieldrows.append((key, f, kind, rel, form, doc))
        lines.append("bronze article objects: %d; parsed as JSON field sets: %d; raw HTML pages (field set NOT MEASURABLE HERE): %d; unparseable/unreadable: %d" % (
            n, len(fieldrows) - html_n, html_n, unparsed))
        kinds = C.Counter((r[4], r[2]) for r in fieldrows)
        lines.append("    by (received-form, kind): " + C.counter_line({"%s/%s" % k: v for k, v in kinds.items()}))

        # bronze vs silver field presence
        missing_count = 0
        measured = 0
        no_silver = 0
        miss_fields = C.Counter()
        diff_fields = C.Counter()
        all_equal = 0
        bronze_names = C.Counter()
        for key, f, kind, rel, form, doc in fieldrows:
            if f is None:
                continue
            bronze_names.update(f)
            hit = by_bronze.get(key)
            if hit is None:
                no_silver += 1
                continue
            srow, cols = hit
            measured += 1
            miss = [x for x in f if x not in cols]
            if miss:
                missing_count += 1
                miss_fields.update(miss)
            if kind == "record":
                d = [k for k in f if k in cols and not equal(doc.get(k), srow.get(k))]
                diff_fields.update(d)
                if not d:
                    all_equal += 1
        lines.append("FIELD PRESENCE (JSON bronze with a silver row; denominator %d of %d JSON-parsed bronze; %d JSON bronze have NO silver row):" % (measured, len(fieldrows) - html_n, no_silver))
        lines.append("    bronze distinct field names seen: %d" % len(bronze_names))
        lines.append("    articles missing >=1 bronze field in silver: %d of %d" % (missing_count, measured))
        lines.append("    most common missing fields: " + (", ".join("%s(%d)" % kv for kv in sorted(miss_fields.items(), key=lambda kv: (-kv[1], kv[0]))[:10]) or "(none)"))
        rec_n = sum(1 for r in fieldrows if r[2] == "record" and by_bronze.get(r[0]))
        lines.append("    VALUE check, normalised-record articles (silver value == bronze value over every shared field, ts parsed): all equal %d of %d; differing fields: %s" % (
            all_equal, rec_n, ", ".join("%s(%d)" % kv for kv in sorted(diff_fields.items(), key=lambda kv: (-kv[1], kv[0]))[:8]) or "(none)"))
        if html_n:
            hsilver = sum(1 for r in fieldrows if r[2] == "html" and by_bronze.get(r[0]))
            lines.append("    HTML pages with a silver row: %d of %d; silver holds them as blob columns articleData / page_config_json (see column set); the bronze-vs-silver field diff for them is NOT MEASURABLE HERE (no extraction parser is run by this cell)" % (hsilver, html_n))

        # named fields
        lines.append("NAMED FIELDS per article (SENT-AND-KEPT / SENT-AND-LOST / NOT SENT), denominator = %d bronze articles read:" % len(fieldrows))
        named_out = {}
        for label, rx in NAMED:
            cnt = C.Counter()
            seen_names = C.Counter()
            for key, f, kind, rel, form, doc in fieldrows:
                hit = by_bronze.get(key)
                if kind == "html":
                    names = set(m for m in HTML_KEY.findall(doc) if rx.search(m))
                    seen_names.update(names)
                    if not names:
                        cnt["NOT SENT (token census on raw HTML)"] += 1
                        continue
                    if not hit:
                        cnt["SENT-AND-LOST (token census; no silver row)"] += 1
                        continue
                    blob = " ".join(str(v) for v in hit[0].values() if isinstance(v, str))
                    kept = any(nm in blob for nm in names)
                    cnt["SENT-AND-KEPT (token census, in a silver blob cell)" if kept else "SENT-AND-LOST (token census)"] += 1
                    continue
                sent = [x for x in f if rx.search(x.split(".")[-1])] + [x for x in rel if rx.search(x)]
                if not sent:
                    cnt["NOT SENT (in bronze)"] += 1
                    continue
                if not hit:
                    cnt["SENT-AND-LOST (no silver row)"] += 1
                    continue
                srow, cols = hit
                relcell = str(srow.get("relationships"))
                kept_all = True
                for x in sent:
                    if x in f and x in cols:
                        continue
                    if x in rel and "relationships" in cols and x in relcell:
                        continue
                    kept_all = False
                cnt["SENT-AND-KEPT" if kept_all else "SENT-AND-LOST"] += 1
            named_out[label] = dict(cnt)
            lines.append("    %-14s %s" % (label, C.counter_line(cnt)))
            if seen_names:
                lines.append("        HTML key names matched (articles): " + ", ".join("%s(%d)" % kv for kv in sorted(seen_names.items(), key=lambda kv: (-kv[1], kv[0]))[:8]))
        lines.append("    (NOT SENT (in bronze) for a normalised_record object means the stored record carries no such field; the collector had already rebuilt the record, so it cannot show the publisher did not send it)")
        result[pub] = {"bronze_objects": n, "html_pages": html_n, "measured_with_silver": measured,
                       "missing_ge1_field": missing_count, "missing_fields": dict(miss_fields),
                       "value_diff_fields": dict(diff_fields), "named": named_out}

    # the one query: by company and date, from silver
    lines.append("")
    lines.append("QUERY by company and date over silver article tables (company = %s via discovered_for; all five publishers):" % C.VALIDATION_SECURITY)
    fetch_date = "2026-09-23"
    qrows = []
    # simple, explicit form of the query: partition date=<fetch_date> filter + discovered_for contains the security
    per_pub = {}
    for pub, store in C.PUBLISHERS:
        got = []
        for pk, row, _cols in C.silver_row_dicts(store)[0]:
            if "/date=%s/" % fetch_date not in pk:
                continue
            if C.VALIDATION_SECURITY in C.discovered_for_list(row.get("discovered_for")):
                got.append(row)
        per_pub[pub] = got
        qrows += [(pub, r) for r in got]
    lines.append("  partition date=%s, discovered_for contains %s -> rows returned: %d (%s)" % (
        fetch_date, C.VALIDATION_SECURITY, len(qrows), ", ".join("%s=%d" % (p, len(v)) for p, v in per_pub.items())))
    for pub, r in qrows[:40]:
        lines.append("    %s %s | %s | published_date_utc=%s | %s" % (pub, r.get("article_key"), str(r.get("title"))[:70], r.get("published_date_utc"), r.get("fetched_at")))
    # by published date (modal date among the security's rows)
    dates = C.Counter(str(r.get("published_date_utc")) for _p, r in qrows)
    if dates:
        d, dn = dates.most_common(1)[0]
        sel = [(p, r) for p, r in qrows if str(r.get("published_date_utc")) == d]
        lines.append("  second form: same company AND published_date_utc = %s -> rows returned: %d of %d company rows (date is the modal published date)" % (d, len(sel), len(qrows)))
    else:
        lines.append("  no rows for the company in that partition")
    lines.append("  silver has NO company column; the company is reachable only via discovered_for (a list of security keys) - printed as measured, not judged")
    result["query"] = {"fetch_date": fetch_date, "security": C.VALIDATION_SECURITY, "rows": len(qrows),
                       "per_publisher": {p: len(v) for p, v in per_pub.items()}}
    C.emit("ac2", "\n".join(lines), result)


if __name__ == "__main__":
    main()
