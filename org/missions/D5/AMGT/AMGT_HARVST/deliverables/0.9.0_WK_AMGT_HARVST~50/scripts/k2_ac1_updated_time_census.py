"""HVST-k-2 AC1: the updated-time census over silver `article` rows and the bronze objects they point to.

READ ONLY: S3 GET/LIST on Opal's own harvest bucket. No PUT, no vendor call, no code change elsewhere.
Silver is read the way publication_gold reads it: store.silver_latest per source (latest row per
article_key). Bronze is read ONLY through the `bronze_key` each silver row records.

Prints (a) the silver time fields per publisher, (b) the bronze time fields per publisher with read /
unreadable counts, (c) HD_US_Equity's served-event lead(s) with every time value found, (d) a one-line
summary per publisher. Every count carries its denominator. Output is also written to k2_ac1_output.txt.
"""

import collections
import datetime
import io
import json
import os
import re
import sys

import pyarrow.parquet as pq

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), *([".."] * 8)))
sys.path.insert(0, REPO)

import lib.research.harvest.store as store  # noqa: E402
import lib.research.harvest.publication_gold as pg  # noqa: E402
from lib.opal_data_harvest.harvest_grammar import SOURCE_FOR_PUBLISHER  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(HERE, "..", "k2_ac1_output.txt")
PUBLISHER_ORDER = ["barrons", "bbg", "ft", "sa", "wsj"]

_ISO = re.compile(r"^\d{4}-\d\d-\d\d([T ]\d\d:\d\d(:\d\d(\.\d+)?)?\s*(Z|[+-]\d\d:?\d\d)?)?$")
_COMPACT = re.compile(r"^\d{8}T\d{6}Z$")
_UPDATED_NAME = re.compile(r"(updat|modif)", re.I)
_TIMEY_NAME = re.compile(r"(date|time|updat|modif|publish|creat|pubbed|live)", re.I)
# Classes are assigned by FIELD NAME only, printed with every row; the class never changes a count.
_RETRIEVAL = ("fetched_at", "first_discovered_at", "run_stamp")

LINES = []


def out(text=""):
    text = text.encode("ascii", "backslashreplace").decode("ascii")
    LINES.append(text)
    print(text)


def field_class(path):
    leaf = re.split(r"[.\[:]", path.rstrip("]"))[-1] if path else path
    if leaf in _RETRIEVAL:
        return "RETRIEVAL-CLOCK"
    if _UPDATED_NAME.search(leaf) or leaf == "dateLastPubbed":
        return "UPDATED"
    if re.search(r"(publish|created|creat|live)", leaf, re.I):
        return "PUBLISHED"
    return "OTHER-TIME"


def parse_time(v):
    """-> (kind, comparable) or None. kind: instant (tz-aware), naive (no tz), date."""
    if isinstance(v, datetime.datetime):
        if v.tzinfo is None:
            return ("naive", v)
        return ("instant", v.astimezone(datetime.timezone.utc))
    if isinstance(v, datetime.date):
        return ("date", v)
    if isinstance(v, str):
        s = v.strip()
        if _COMPACT.match(s):
            return ("instant", datetime.datetime.strptime(s, "%Y%m%dT%H%M%SZ").replace(tzinfo=datetime.timezone.utc))
        if _ISO.match(s):
            t = s.replace("Z", "+00:00").replace(" ", "T", 1) if "T" not in s else s.replace("Z", "+00:00")
            try:
                d = datetime.datetime.fromisoformat(t)
            except ValueError:
                try:
                    return ("date", datetime.date.fromisoformat(s[:10]))
                except ValueError:
                    return None
            if len(s) == 10:
                return ("date", d.date())
            if d.tzinfo is None:
                return ("naive", d)
            return ("instant", d.astimezone(datetime.timezone.utc))
    return None


def parse_epoch(name, v):
    """A numeric under an updated/modified-named key that looks like epoch seconds or ms."""
    if isinstance(v, bool) or not isinstance(v, (int, float)) or not _UPDATED_NAME.search(name):
        return None
    x = float(v)
    if x > 1e11:
        x = x / 1000.0
    if 1.0e9 <= x <= 4.0e9:
        return ("instant", datetime.datetime.fromtimestamp(x, datetime.timezone.utc))
    return None


def walk_times(obj, path, found, skipped):
    """Collect {path: raw value} for every time-bearing leaf reachable WITHOUT descending into a list
    (a list member is another object's field -- a related story, an author -- and is counted in
    `skipped`, never in the per-article census). JSON-in-a-string is opened once."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            walk_times(v, path + "." + str(k) if path else str(k), found, skipped)
        return
    if isinstance(obj, list):
        n = _count_times(obj)
        if n:
            skipped[path] += n
        return
    if obj is None:
        return
    if isinstance(obj, str):
        if parse_time(obj):
            found[path] = obj
            return
        if obj[:1] in "{[" and len(obj) > 1:
            try:
                inner = json.loads(obj)
            except ValueError:
                return
            walk_times(inner, path + "{json}", found, skipped)
        return
    if hasattr(obj, "isoformat"):
        found[path] = obj
        return
    leaf = path.rsplit(".", 1)[-1]
    if parse_epoch(leaf, obj):
        found[path] = obj


def _count_times(obj):
    if isinstance(obj, dict):
        return sum(_count_times(v) for v in obj.values())
    if isinstance(obj, list):
        return sum(_count_times(v) for v in obj)
    if isinstance(obj, str):
        if parse_time(obj):
            return 1
        if obj[:1] in "{[" and len(obj) > 1:
            try:
                return _count_times(json.loads(obj))
            except ValueError:
                return 0
        return 0
    return 1 if hasattr(obj, "isoformat") else 0


def as_time(raw, path):
    t = parse_time(raw)
    if t is None:
        t = parse_epoch(path.rsplit(".", 1)[-1], raw)
    return t


def differs(t, pub):
    """True/False whether the value differs from published_utc; None if not comparable."""
    if t is None or pub is None:
        return None
    kind, val = t
    if kind == "instant":
        return val != pub
    return val.date() != pub.date() if kind == "naive" else val != pub.date()


def html_times(text):
    """Page-level time fields of an HTML bronze object: <meta> tags whose name/property/itemprop is
    time-named and whose content is a timestamp, plus time-named keys on the TOP-LEVEL objects of each
    application/ld+json block. Values embedded elsewhere in the page belong to other stories."""
    found = collections.OrderedDict()
    for m in re.finditer(r"<meta\b[^>]*>", text):
        tag = m.group(0)
        nm = re.search(r'(?i)\b(?:name|property|itemprop)\s*=\s*"([^"]+)"', tag)
        ct = re.search(r'(?i)\bcontent\s*=\s*"([^"]*)"', tag)
        if nm and ct and _TIMEY_NAME.search(nm.group(1)) and parse_time(ct.group(1)):
            key = "meta[%s]" % nm.group(1)
            found.setdefault(key, ct.group(1))
    for block in re.findall(r'<script[^>]*application/ld\+json[^>]*>(.*?)</script>', text, re.S):
        try:
            j = json.loads(block)
        except ValueError:
            continue
        for item in (j if isinstance(j, list) else [j]):
            if isinstance(item, dict):
                for k, v in item.items():
                    if isinstance(v, str) and _TIMEY_NAME.search(k) and parse_time(v):
                        found.setdefault("ldjson." + k, v)
    return found


def load_silver(client):
    rows = []
    for pub in PUBLISHER_ORDER:
        src = SOURCE_FOR_PUBLISHER[pub]
        latest = store.silver_latest(src, "article", ("article_key",), client=client)
        for r in latest.values():
            rows.append((pub, r))
    return rows


def census(title, per_pub_rows, times_of, denominators):
    """per_pub_rows: {pub: [(article_key, {path: raw}, published_utc)]}. Prints the table; returns
    {pub: {path: stats}}."""
    result = {}
    out(title)
    for pub in PUBLISHER_ORDER:
        rows = per_pub_rows.get(pub, [])
        n = denominators.get(pub, len(rows))
        stats = collections.OrderedDict()
        for ak, found, pubutc in rows:
            for path, raw in found.items():
                t = as_time(raw, path)
                st = stats.setdefault(path, {"present": 0, "vals": set(), "differs": 0, "uncomp": 0, "kinds": set()})
                st["present"] += 1
                st["vals"].add(str(raw))
                if t:
                    st["kinds"].add(t[0])
                d = differs(t, pubutc)
                if d is None:
                    st["uncomp"] += 1
                elif d:
                    st["differs"] += 1
        result[pub] = stats
        out("  publisher %s: %d articles" % (pub, n))
        if not stats:
            out("    (no time-bearing field found)")
        for path, st in sorted(stats.items(), key=lambda kv: (field_class(kv[0]), kv[0])):
            out("    %-64s class=%-15s kind=%-13s PRESENT %d of %d | DISTINCT-VALUES %d | DIFFERS-FROM-published_utc %d of %d present%s" % (
                path, field_class(path), "/".join(sorted(st["kinds"])) or "unparsed", st["present"], n,
                len(st["vals"]), st["differs"], st["present"],
                (" (%d not comparable)" % st["uncomp"]) if st["uncomp"] else ""))
    return result


def read_bronze(client, key):
    body = client.get_object(Bucket=store.HARVEST_BUCKET, Key=key)["Body"].read()
    return body


def bronze_times(key, body):
    found = collections.OrderedDict()
    skipped = collections.Counter()
    if key.endswith(".json"):
        j = json.loads(body.decode("utf-8"))
        if isinstance(j, dict):
            walk_times(j, "", found, skipped)
        else:
            raise ValueError("bronze json is not an object")
    else:
        text = body.decode("utf-8", "replace")
        found.update(html_times(text))
    return found, skipped


def main():
    client = store._default_client()
    silver = load_silver(client)
    n_by_pub = collections.Counter(p for p, _ in silver)
    out("HVST-k-2 AC1 -- the updated-time census (read only; harvest bucket %s)" % store.HARVEST_BUCKET)
    out("SILVER ARTICLES AS LANDED (store.silver_latest per source, latest row per article_key): %d total; per publisher: %s" % (
        len(silver), ", ".join("%s=%d" % (p, n_by_pub[p]) for p in PUBLISHER_ORDER)))
    out("classes are by field NAME only (RETRIEVAL-CLOCK = fetched_at/first_discovered_at/run_stamp; UPDATED = name has updat|modif, or dateLastPubbed;")
    out("PUBLISHED = publish|creat|live; OTHER-TIME = the rest). kind: instant = tz-aware; naive = no zone; date = day only (compared on the UTC day).")
    out("A list member's times belong to another object (related story, author) and are counted in 'NOT COUNTED', never in a field row.")
    out("")

    # ---- (a) silver
    silver_rows = collections.defaultdict(list)
    silver_skipped = collections.defaultdict(collections.Counter)
    for pub, r in silver:
        found = collections.OrderedDict()
        skipped = collections.Counter()
        for col, val in r.items():
            walk_times(val, col, found, skipped)
        silver_rows[pub].append((r["article_key"], found, parse_time(r.get("published_utc"))[1] if parse_time(r.get("published_utc")) else None))
        silver_skipped[pub].update(skipped)
    census("(a) SILVER time-bearing fields per publisher", silver_rows, None, n_by_pub)
    for pub in PUBLISHER_ORDER:
        if silver_skipped[pub]:
            out("  NOT COUNTED (times inside list members, silver, %s): %s" % (
                pub, "; ".join("%s x%d" % (k, v) for k, v in sorted(silver_skipped[pub].items()))))
    out("")

    # ---- (b) bronze, read only through the key silver records
    bronze_rows = collections.defaultdict(list)
    unread = []
    read_n = collections.Counter()
    for pub, r in silver:
        key = r.get("bronze_key")
        pubutc = parse_time(r.get("published_utc"))
        pubutc = pubutc[1] if pubutc else None
        try:
            if not key:
                raise ValueError("silver row has no bronze_key")
            body = read_bronze(client, key)
            found, _sk = bronze_times(key, body)
            read_n[pub] += 1
            bronze_rows[pub].append((r["article_key"], found, pubutc))
        except Exception as exc:  # named, never swallowed
            unread.append((pub, r["article_key"], key, "%s: %s" % (type(exc).__name__, exc)))
    out("(b) BRONZE objects read through silver's bronze_key: %d of %d read; %d could not be read" % (
        sum(read_n.values()), len(silver), len(unread)))
    out("    per publisher read: %s" % ", ".join("%s=%d of %d" % (p, read_n[p], n_by_pub[p]) for p in PUBLISHER_ORDER))
    fmt = collections.Counter()
    for pub, r in silver:
        fmt[(pub, (r.get("bronze_key") or "").rsplit(".", 1)[-1])] += 1
    out("    bronze formats by silver key: %s" % ", ".join("%s.%s=%d" % (p, e, n) for (p, e), n in sorted(fmt.items())))
    for pub, ak, key, why in unread:
        out("    UNREADABLE %s %s key=%s reason=%s" % (pub, ak, key, why))
    if not unread:
        out("    UNREADABLE: none")
    census("    BRONZE time-bearing fields per publisher (denominator = silver articles for that publisher; unreadable ones are absent)",
                          bronze_rows, None, n_by_pub)
    out("")

    # ---- (c) HD served-event lead(s)
    out("(c) HD_US_Equity served event(s)")
    events = pg._latest_gold_snapshot_rows("chatter_event", client=client)
    hd_now = [e for e in events if e.get("security_key") == "HD_US_Equity"]
    prefix = store.table_prefix("amgt", "gold", "chatter_event")
    parts = []
    for page in client.get_paginator("list_objects_v2").paginate(Bucket=store.HARVEST_BUCKET, Prefix=prefix):
        for o in page.get("Contents", []) or []:
            if o["Key"].endswith(".parquet"):
                parts.append(o["Key"])
    parts.sort(key=lambda k: (re.search(r"date=(\d{4}-\d{2}-\d{2})", k).group(1), k))
    out("    chatter_event parts on the bucket: %d; the newest is %s" % (len(parts), parts[-1].rsplit("/", 1)[-1] if parts else "none"))
    barrons_led = collections.OrderedDict()
    hist = []
    for k in parts:
        rows = pq.read_table(io.BytesIO(client.get_object(Bucket=store.HARVEST_BUCKET, Key=k)["Body"].read())).to_pylist()
        for e in rows:
            if e.get("security_key") == "HD_US_Equity":
                hist.append((k.rsplit("/", 1)[-1], e))
                if str(e.get("lead_article_key", "")).startswith("barrons:"):
                    barrons_led.setdefault(e["lead_article_key"], []).append(k.rsplit("/", 1)[-1])
    for part, e in hist:
        out("    part %s: HD event days %s..%s lead=%s articles=%s" % (
            part, e["first_day"], e["last_day"], e["lead_article_key"], ",".join(e["article_keys"])))
    out("    HD events in the NEWEST snapshot: %d; HD parts scanned: %d; parts whose HD lead is a barrons article: %d" % (
        len(hd_now), len({p for p, _ in hist}), len({p for k in barrons_led for p in barrons_led[k]})))
    silver_by_key = {r["article_key"]: (pub, r) for pub, r in silver}
    to_detail = []
    for e in hd_now:
        for ak in e["article_keys"]:
            to_detail.append(("NEWEST-SNAPSHOT MEMBER%s" % (" (LEAD)" if ak == e["lead_article_key"] else ""), ak))
    for ak, ps in barrons_led.items():
        to_detail.append(("BARRONS LEAD of HD event in parts %s" % ",".join(ps), ak))
    # the HD mention rows also name the barrons tier-A candidate
    for label, ak in to_detail:
        pub_r = silver_by_key.get(ak)
        if not pub_r:
            out("    %s: %s -- NOT in the silver as landed" % (label, ak))
            continue
        pub, r = pub_r
        found = collections.OrderedDict()
        skipped = collections.Counter()
        for col, val in r.items():
            walk_times(val, col, found, skipped)
        out("    %s: %s headline=%s" % (label, ak, ascii(r.get("title"))))
        out("      SILVER time values (%d fields):" % len(found))
        for path, raw in found.items():
            out("        %-56s = %s [%s]" % (path, raw, field_class(path)))
        key = r.get("bronze_key")
        try:
            bf, _sk = bronze_times(key, read_bronze(client, key))
            out("      BRONZE %s time values (%d fields):" % (key, len(bf)))
            for path, raw in bf.items():
                out("        %-56s = %s [%s]" % (path, raw, field_class(path)))
        except Exception as exc:
            out("      BRONZE %s UNREADABLE: %s: %s" % (key, type(exc).__name__, exc))
    out("")

    # ---- (d) one line per publisher
    out("(d) SUMMARY per publisher (an UPDATED-class field with a value counts as available; DIFFERS = value not equal to published_utc)")
    for pub in PUBLISHER_ORDER:
        n = n_by_pub[pub]
        s_ok = {}
        b_ok = {}
        for layer, rows, ok in (("silver", silver_rows[pub], s_ok), ("bronze", bronze_rows[pub], b_ok)):
            for ak, found, pubutc in rows:
                for path, raw in found.items():
                    if field_class(path) == "UPDATED":
                        d = differs(as_time(raw, path), pubutc)
                        cur = ok.get(ak)
                        ok[ak] = (cur or False) or bool(d)
        both = set(s_ok) | set(b_ok)
        diff_any = sum(1 for ak in both if s_ok.get(ak) or b_ok.get(ak))
        if both:
            out("  %s: UPDATED-TIME AVAILABLE on %d of %d articles (silver %d, bronze %d; differs from published_utc on %d)" % (
                pub, len(both), n, len(s_ok), len(b_ok), diff_any))
        else:
            out("  %s: NONE (0 of %d articles carry an updated or modified time in silver or in the bronze read)" % (pub, n))
    out("")
    sections = all(any(ln.startswith(m) for ln in LINES) for m in ("(a)", "(b)", "(c)", "(d)"))
    out("SECTIONS PRINTED (a)(b)(c)(d): %s; denominator %d silver articles, %d bronze read, %d unreadable" % (
        "YES" if sections else "NO", len(silver), sum(read_n.values()), len(unread)))
    with open(OUT_PATH, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(LINES) + "\n")
    return 0 if sections else 1


if __name__ == "__main__":
    raise SystemExit(main())
