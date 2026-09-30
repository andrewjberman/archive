"""HVST-n-2 AC2 -- the REAL served sa bronze objects rebuilt IN MEMORY by the new silver builder.

READ-ONLY: S3 GET/LIST only. Nothing is written to S3; the only files written are this cell's own
n2_ac2_output.txt / n2_ac2_result.json beside the scripts.

WHAT IT DOES
  1. Lists every sa bronze article object (seeking-alpha/harvest/bronze/article/), GETs each with its
     `received-form` metadata (absent = "unlabelled"), and reads every served sa silver article row.
  2. Rebuilds one silver row per bronze object with lib/opal_data_harvest/silver_from_bronze.article_rows
     (the working-tree builder). A served object's lineage (fetched_at, retrieval_mode, run_stamp and the
     discovery record) is passed from its served silver row so that only the BUILDER's change can move a
     value; an unlabelled object (no served row) gets fetched_at/run_stamp from its bronze key's stamp and
     retrieval_mode "backfill" (not derivable from bronze; printed as assumed).
  3. FIELDS: for the JSON:API objects, the bronze field set (data.attributes.*, the other data.* keys,
     'included', meta.*) against the silver row, BEFORE (served row) and AFTER (rebuilt row). A meta.X
     field is kept when the row's `meta` struct holds X. Value-equal check on the six named fields.
  4. UNLABELLED: each of the objects with no served row -> a row, or the reason it gets none.
  5. WOULD-MOVE: for every served silver row (denominator printed), whether the rebuilt row differs from the
     served row on any column (value-level, datetimes as UTC instants) and whether store.record_hash(rebuilt)
     differs from the served record_hash (the mechanism silver_append uses to skip an unchanged row), with a
     positive control: how many served rows re-hash to their own stored record_hash when read back.
  6. WRITABLE: the rows that would be appended are pushed through pa.Table.from_pylist + pq.write_table in
     memory, grouped by fetch date as store.silver_append groups them.
"""
import collections
import io
import json
import re

import pyarrow as pa
import pyarrow.parquet as pq

import n2_common as C

from lib.opal_data_harvest import harvest_grammar  # noqa: E402
from lib.opal_data_harvest import silver_from_bronze as sfb  # noqa: E402
from lib.research.harvest import store  # noqa: E402

STORE = "seeking-alpha"
NAMED = ("links", "type", "meta.path", "meta.page", "meta.redirectPath", "meta.proStatus")
STAMP_RE = re.compile(r"/(\d{8}T\d{6}Z)\.json$")


def bronze_fields(doc):
    """Bronze field set of a JSON:API article document."""
    fields = set()
    data = doc["data"]
    for k, v in data.items():
        if k == "attributes" and isinstance(v, dict):
            fields.update(v.keys())
        else:
            fields.add(k)
    if "included" in doc:
        fields.add("included")
    meta = doc.get("meta")
    if isinstance(meta, dict):
        fields.update("meta." + k for k in meta)
    elif meta is not None:
        fields.add("meta")
    return fields


def has_field(row, name):
    if name.startswith("meta."):
        return isinstance(row.get("meta"), dict) and name[5:] in row["meta"]
    return name in row


def bronze_value(doc, name):
    if name.startswith("meta."):
        return doc["meta"][name[5:]]
    return doc["data"][name]


def row_value(row, name):
    if name.startswith("meta."):
        return row["meta"][name[5:]]
    return row[name]


def main():
    L = []
    keys = C.list_keys("%s/harvest/bronze/article/" % STORE)
    L.append("AC2 - REAL sa bronze objects rebuilt IN MEMORY by the new builder (S3 GET/LIST only; nothing written)")
    L.append("sa bronze article objects listed: %d" % len(keys))

    served = {}
    served_rows_total = 0
    served_by_article = collections.defaultdict(list)
    for _pk, rows in C.silver_parts(STORE):
        for r in rows:
            served_rows_total += 1
            served[r["bronze_key"]] = r
            served_by_article[r["article_key"]].append(r["bronze_key"])
    L.append("served sa silver article rows read: %d (distinct bronze_key %d, distinct article_key %d)"
             % (served_rows_total, len(served), len(served_by_article)))

    objs = []
    for k in keys:
        body, meta = C.get(k)
        objs.append((k, body, C.received_form(meta)))
    form_of = {k: f for k, _b, f in objs}
    forms = collections.Counter(form_of.values())
    L.append("bronze objects by received-form: " + ", ".join("%s=%d" % kv for kv in sorted(forms.items())))
    no_row = [o for o in objs if o[0] not in served]
    L.append("bronze objects with a served silver row: %d; WITHOUT: %d" % (len(objs) - len(no_row), len(no_row)))

    rebuilt = {}
    for k, body, form in objs:
        s = served.get(k)
        if s is not None:
            fetched_at, mode, run_stamp = s["fetched_at"], s["retrieval_mode"], s["run_stamp"]
            discovery = {f: s.get(f) for f in ("first_discovered_at", "retrieval_rung", "search_query",
                                               "search_rank", "search_page", "discovered_for")}
        else:
            stamp = STAMP_RE.search(k).group(1)
            fetched_at = harvest_grammar.parse_timestamp(
                "%s-%s-%sT%s:%s:%sZ" % (stamp[0:4], stamp[4:6], stamp[6:8], stamp[9:11], stamp[11:13], stamp[13:15]))
            mode, run_stamp, discovery = "backfill", stamp, None
        rebuilt[k] = sfb.article_rows("sa", body, form, k, fetched_at, mode, run_stamp, discovery=discovery)
    L.append("rebuilt in memory: %d rows (one per bronze object)" % len(rebuilt))

    jsonapi = []
    for k, body, form in objs:
        doc = json.loads(body)
        if isinstance(doc.get("data"), dict):
            jsonapi.append((k, doc, form))
    L.append("")
    L.append("FIELDS (JSON:API bronze = data/included/meta envelope: %d of %d objects; the other %d are normalised_record objects)"
             % (len(jsonapi), len(objs), len(objs) - len(jsonapi)))
    before_missing, after_missing = collections.Counter(), collections.Counter()
    b_articles = a_articles = measured_before = 0
    for k, doc, form in jsonapi:
        fields = bronze_fields(doc)
        s = served.get(k)
        if s is not None:
            measured_before += 1
            miss = [f for f in fields if not has_field(s, f)]
            if miss:
                b_articles += 1
                before_missing.update(miss)
        miss_a = [f for f in fields if not has_field(rebuilt[k], f)]
        if miss_a:
            a_articles += 1
            after_missing.update(miss_a)
    L.append("BEFORE (served silver rows): articles missing >=1 bronze field: %d of %d served JSON:API rows; fields: %s"
             % (b_articles, measured_before, ", ".join("%s(%d)" % kv for kv in sorted(before_missing.items())) or "(none)"))
    L.append("AFTER  (rebuilt in memory): articles missing >=1 bronze field: %d of %d JSON:API objects rebuilt (as_received + unlabelled); fields: %s"
             % (a_articles, len(jsonapi), ", ".join("%s(%d)" % kv for kv in sorted(after_missing.items())) or "(none)"))
    asr = [(k, doc) for k, doc, f in jsonapi if f == "as_received"]
    L.append("missing count over the %d as_received articles: BEFORE %d -> AFTER %d" % (
        len(asr),
        sum(1 for k, doc in asr if any(not has_field(served[k], x) for x in bronze_fields(doc))),
        sum(1 for k, doc in asr if any(not has_field(rebuilt[k], x) for x in bronze_fields(doc)))))
    L.append("the six named fields: rebuilt row value == bronze value, per JSON:API object (BEFORE = present in the served row):")
    named_ok = collections.Counter()
    named_before = collections.Counter()
    for k, doc, form in jsonapi:
        for name in NAMED:
            if has_field(rebuilt[k], name) and C.norm(bronze_value(doc, name)) == C.norm(row_value(rebuilt[k], name)):
                named_ok[name] += 1
            if k in served and has_field(served[k], name):
                named_before[name] += 1
    for name in NAMED:
        L.append("    %-18s AFTER kept-and-equal in %d of %d rebuilt JSON:API rows; BEFORE present in %d of %d served JSON:API rows"
                 % (name, named_ok[name], len(jsonapi), named_before[name], measured_before))
    sample = rebuilt[jsonapi[0][0]]
    tbl = pa.Table.from_pylist([sample])
    L.append("    arrow types of the new columns: links=%s, type=%s, meta=%s" % (
        tbl.schema.field("links").type, tbl.schema.field("type").type, tbl.schema.field("meta").type))

    L.append("")
    L.append("THE %d bronze objects with NO served silver row:" % len(no_row))
    unl = []
    for k, body, form in no_row:
        doc = json.loads(body)
        r = rebuilt[k]
        is_article = isinstance(doc.get("data"), dict) and doc["data"].get("type") == "fullArticle"
        other = served_by_article.get(r["article_key"])
        unl.append({"bronze_key": k, "received_form": form, "data.type": doc["data"].get("type"),
                    "is_article": is_article, "row_built": True, "article_key": r["article_key"],
                    "title": r["title"], "text_blocks": len(r["text_blocks"]),
                    "article_key_already_served_from": other})
        L.append("    %s | form=%s | data.type=%s | article=%s | ROW BUILT %s | %s | text_blocks=%d | article_key already in served silver: %s"
                 % (k.split("/")[-1], form, doc["data"].get("type"), is_article, r["article_key"],
                    str(r["title"])[:56], len(r["text_blocks"]), other or "no"))
    L.append("unlabelled objects: %d; articles (data.type fullArticle) -> a row built: %d; not an article (no row, reason named): %d"
             % (len(unl), sum(1 for u in unl if u["is_article"]), sum(1 for u in unl if not u["is_article"])))
    L.append("ASSUMED for these rows (not derivable from bronze): retrieval_mode='backfill', fetched_at/run_stamp = the stamp in the bronze key, discovery = none (discovered_for null)")

    L.append("")
    L.append("SERVED ROWS THAT WOULD MOVE (denominator = %d served sa silver article rows; each compared with the row rebuilt from its own bronze object):" % len(served))
    moved_value = []
    moved_hash = []
    reproduced = 0
    diff_cols = collections.Counter()
    for bk, s in sorted(served.items()):
        r = rebuilt[bk]
        cols = set(s) | set(r)
        differing = sorted(c for c in cols if c != "record_hash" and C.norm(s.get(c)) != C.norm(r.get(c)))
        if differing:
            moved_value.append((bk, differing))
            diff_cols.update(differing)
        if store.record_hash(s) == s.get("record_hash"):
            reproduced += 1
        if store.record_hash(r) != s.get("record_hash"):
            moved_hash.append(bk)
    moved_set = {bk for bk, _c in moved_value}
    L.append("  value-level: served rows whose rebuilt row differs on >=1 column: %d of %d; unchanged: %d of %d"
             % (len(moved_value), len(served), len(served) - len(moved_value), len(served)))
    L.append("  columns that differ (rows): " + (", ".join("%s(%d)" % kv for kv in sorted(diff_cols.items())) or "(none)"))
    for bk, cols in moved_value:
        L.append("    MOVES %s (%s) | %s" % (served[bk]["article_key"], form_of[bk], ", ".join(cols)))
    L.append("  hash-level (the silver_append skip test): store.record_hash(rebuilt) != served record_hash: %d of %d" % (len(moved_hash), len(served)))
    L.append("  positive control: served rows whose OWN read-back re-hash equals their stored record_hash: %d of %d" % (reproduced, len(served)))
    hashonly = [bk for bk in moved_hash if bk not in moved_set]
    L.append("  rows whose hash differs but no column value does (read-back drift, not a builder change): %d" % len(hashonly))
    by_form = collections.Counter(form_of[bk] for bk in moved_set)
    L.append("  moved rows by received-form: " + (", ".join("%s=%d" % kv for kv in sorted(by_form.items())) or "(none)"))
    L.append("  every OTHER served row unchanged: %d of %d" % (len(served) - len(moved_set), len(served)))
    L.append("  rows ADDED by the rebuild (bronze objects with no served row): %d -> served silver rows %d -> %d if applied"
             % (len(no_row), len(served), len(served) + len(no_row)))

    L.append("")
    changed_keys = sorted(moved_set | {u["bronze_key"] for u in unl})
    by_date = collections.defaultdict(list)
    for k in changed_keys:
        by_date[rebuilt[k]["fetched_at"].date()].append(rebuilt[k])
    ok = 0
    for _d, rows in sorted(by_date.items()):
        buf = io.BytesIO()
        pq.write_table(pa.Table.from_pylist(rows), buf)
        back = pq.read_table(io.BytesIO(buf.getvalue())).to_pylist()
        ok += len(back) == len(rows)
    L.append("WRITABLE in memory: rows that would be appended (moved + new) = %d, in %d fetch-date group(s); %d of %d groups round-trip through pa.Table.from_pylist + pq.write_table"
             % (len(changed_keys), len(by_date), ok, len(by_date)))

    result = {
        "bronze_objects": len(objs), "served_rows": len(served), "received_forms": dict(forms),
        "before_missing_articles": b_articles, "after_missing_articles": a_articles,
        "before_missing_fields": dict(before_missing), "after_missing_fields": dict(after_missing),
        "unlabelled": unl, "served_rows_moving_value_level": len(moved_value),
        "served_rows_moving_hash_level": len(moved_hash), "moved_columns": dict(diff_cols),
        "control_rehash_reproduced": reproduced, "rows_added": len(no_row),
    }
    C.emit("ac2", "\n".join(L), result)


if __name__ == "__main__":
    main()
