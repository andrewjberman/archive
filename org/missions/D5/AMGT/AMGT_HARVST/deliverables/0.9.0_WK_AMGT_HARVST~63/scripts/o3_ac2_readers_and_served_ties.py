"""HVST-o-3 AC2: (1) the census of every newest-wins silver reader under lib/, with file:line and the
patterns searched (denominator printed); (2) over the SERVED silver of every source and table, the count of
record keys whose newest fetched_at is TIED across parts, with the row the OLD and the NEW rule pick for
each; (3) the /timeline/day body sha256 for four named days under the OLD rule and the NEW rule.

READ-ONLY: S3 LIST/GET only (a metering proxy exposes nothing else). No PUT, no DELETE, no vendor call.
Writes ../o3_ac2_output.txt (the same text it prints)."""
import ast
import collections
import hashlib
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, *([".."] * 8)))
OUT = os.path.join(os.path.dirname(HERE), "o3_ac2_output.txt")
sys.path.insert(0, ROOT)
os.chdir(ROOT)

LINES = []


def say(text=""):
    LINES.append(text)
    print(text)


# ---------------------------------------------------------------- (1) reader census

PATTERNS = [
    ("P1 fetched_at compared with < or >", re.compile(r"""fetched_at["']?\)?\]?\s*[<>]""")),
    ("P2 call or def of silver_latest", re.compile(r"\bsilver_latest\b")),
    ("P3 max()/sorted() keyed on fetched_at", re.compile(r"(max|sorted)\(.{0,120}fetched_at")),
    ("P4 store.supersedes( / store.part_order_key( call, or their def (the shared comparator)", re.compile(r"(store\.(supersedes|part_order_key)\(|def (supersedes|part_order_key)\()")),
]
# classification of the enclosing function of a hit; anything not listed prints UNCLASSIFIED
CLASS = {
    ("lib/research/harvest/store.py", "supersedes"): "COMPARATOR: the one shared newest-wins rule",
    ("lib/research/harvest/store.py", "part_order_key"): "COMPARATOR helper: run_stamp of a part name",
    ("lib/research/harvest/store.py", "silver_latest"): "READER (newest-wins over parts) -> calls store.supersedes",
    ("lib/research/harvest/store.py", "silver_append"): "CALLER of silver_latest (dedupe read, no pick of its own)",
    ("lib/research/harvest/publication_gold.py", "_iter_latest_articles"): "READER -> delegates to store.silver_latest",
    ("lib/research/harvest/publication_gold.py", "_latest_articles_for_keys"): "READER (newest-wins over parts) -> calls store.supersedes",
    ("lib/research/harvest/lusha.py", "already_fetched"):
        "CONSUMER: a `fetched_at >= since` threshold on store.silver_latest's output, no pick of its own",
    ("lib/opal_data_harvest/silver_from_bronze.py", "rows_by_company_mention"):
        "OUTSIDE PATHS: pure function over rows ALREADY read (no part names) -> surprise row, not an edit",
}
CALLER_FUNCS_NOTE = "any other function whose hit is only `store.silver_latest(` / `hstore.silver_latest(` is a CALLER"


def _enclosing(tree, lineno):
    best = None
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            end = getattr(node, "end_lineno", node.lineno)
            if node.lineno <= lineno <= end and (best is None or node.lineno >= best.lineno):
                best = node
    return best.name if best else "<module>"


def census_readers():
    files = []
    for dp, dn, fn in os.walk(os.path.join(ROOT, "lib")):
        dn[:] = [d for d in dn if d not in ("__pycache__", ".git", "node_modules")]
        for f in fn:
            if f.endswith(".py"):
                files.append(os.path.join(dp, f))
    files.sort()
    say("== (1) NEWEST-WINS SILVER READER CENSUS under lib/ ==")
    say("denominator: %d .py files scanned under lib/ (tests included in the scan, marked TEST)" % len(files))
    for name, rx in PATTERNS:
        say("pattern searched: %s   /%s/" % (name, rx.pattern))
    hits = []
    for path in files:
        rel = os.path.relpath(path, ROOT).replace(os.sep, "/")
        with open(path, encoding="utf-8", errors="replace") as fh:
            src = fh.read()
        try:
            tree = ast.parse(src)
        except SyntaxError:
            tree = None
        for i, line in enumerate(src.splitlines(), 1):
            for name, rx in PATTERNS:
                if rx.search(line):
                    func = _enclosing(tree, i) if tree else "?"
                    hits.append((rel, i, func, name.split()[0], line.strip()))
    is_test = lambda rel: ("/tests/" in rel or os.path.basename(rel).startswith("test_"))  # noqa: E731
    prod = [h for h in hits if not is_test(h[0])]
    tests = [h for h in hits if is_test(h[0])]
    say("hits: %d in production files, %d in test files" % (len(prod), len(tests)))
    say("-- production hits (file:line  function  pattern  classification) --")
    unclassified = 0
    readers = set()
    for rel, i, func, pat, text in prod:
        cls = CLASS.get((rel, func))
        if cls is None:
            if pat == "P2" and "silver_latest(" in text:
                cls = "CALLER of store.silver_latest (inherits the rule)"
            elif pat == "P2":
                cls = "mention of silver_latest (docstring/comment)"
            else:
                cls = "UNCLASSIFIED"
                unclassified += 1
        if cls.startswith("READER") or cls.startswith("OUTSIDE"):
            readers.add((rel, func))
        say("  %s:%d  %s  %s  %s" % (rel, i, func, pat, cls))
    say("-- newest-wins readers (distinct) --")
    for rel, func in sorted(readers):
        say("  %s::%s" % (rel, func))
    say("UNCLASSIFIED production hits: %d  (%s)" % (unclassified, CALLER_FUNCS_NOTE))
    say("test-file hits: %d (not readers; listed by count per file)" % len(tests))
    for f, n in sorted(collections.Counter(h[0] for h in tests).items()):
        say("  %s: %d" % (f, n))
    say("")


# ---------------------------------------------------------------- (2) served ties

class ReadOnlyClient:
    """Exposes ONLY list_objects_v2 (paginator and direct) and get_object; parts are read once and reused."""

    def __init__(self):
        import boto3
        self._c = boto3.client("s3", region_name="us-east-1")
        self._cache = {}
        self.gets = 0
        self.lists = 0

    def get_paginator(self, name):
        if name != "list_objects_v2":
            raise RuntimeError("read-only proxy: %r refused" % name)
        outer = self

        class _P:
            def paginate(self, **kw):
                outer.lists += 1
                return outer._c.get_paginator("list_objects_v2").paginate(**kw)

        return _P()

    def list_objects_v2(self, **kw):
        self.lists += 1
        return self._c.list_objects_v2(**kw)

    def get_object(self, Bucket, Key, **kw):
        if Key not in self._cache:
            self.gets += 1
            self._cache[Key] = self._c.get_object(Bucket=Bucket, Key=Key)["Body"].read()
        return {"Body": io.BytesIO(self._cache[Key])}


def old_silver_latest(store, source, table, record_key_fields, client):
    """store.silver_latest as of the base (65aa9251bc), verbatim: strictly-newer fetched_at only."""
    import pyarrow.parquet as pq
    prefix = store.table_prefix(source, "silver", table)
    latest = {}
    for page in client.get_paginator("list_objects_v2").paginate(Bucket=store.HARVEST_BUCKET, Prefix=prefix):
        for obj in page.get("Contents", []) or []:
            key = obj["Key"]
            if not key.endswith(".parquet"):
                continue
            raw = client.get_object(Bucket=store.HARVEST_BUCKET, Key=key)["Body"].read()
            for row in pq.read_table(io.BytesIO(raw)).to_pylist():
                rk = tuple(row.get(f) for f in record_key_fields)
                prior = latest.get(rk)
                if prior is None or row["fetched_at"] > prior["fetched_at"]:
                    latest[rk] = row
    return latest


def _differs(a, b):
    keys = sorted(set(a) | set(b))
    return [k for k in keys if a.get(k) != b.get(k) and k not in ("record_hash",)]


def served_ties(client):
    import pyarrow.parquet as pq
    from lib.research.corpus import typed
    from lib.research.harvest import store

    say("== (2) SERVED SILVER: record keys whose newest fetched_at is tied across parts ==")
    top = []
    for page in client.get_paginator("list_objects_v2").paginate(Bucket=store.HARVEST_BUCKET, Delimiter="/"):
        top += [p["Prefix"] for p in page.get("CommonPrefixes", [])]
    key_fields = {"article": ("article_key",), "filing_source": ("security_key", "accession"),
                  typed.TABLE: tuple(typed.RECORD_KEY_FIELDS)}
    tables = []
    for t in top:
        for page in client.get_paginator("list_objects_v2").paginate(
                Bucket=store.HARVEST_BUCKET, Prefix=t + "harvest/silver/", Delimiter="/"):
            for p in page.get("CommonPrefixes", []):
                tables.append((t.rstrip("/"), p["Prefix"].rstrip("/").rsplit("/", 1)[-1]))
    say("denominator: %d bucket top-level prefixes listed; %d (source, silver table) pairs hold silver" % (len(top), len(tables)))
    total_keys = total_ties = total_pick_moves = 0
    all_ties = {}  # (source, table, record_key) -> info
    for source, table in tables:
        if table not in key_fields:
            say("  %s/%s: no newest-wins reader collapses this table to one row per key (a hit table; "
                "publication_gold._listing_hit_rows keeps every row) -- SKIPPED, not counted" % (source, table))
            continue
        fields = key_fields[table]
        prefix = store.table_prefix(source, "silver", table)
        parts = []
        for page in client.get_paginator("list_objects_v2").paginate(Bucket=store.HARVEST_BUCKET, Prefix=prefix):
            parts += [o["Key"] for o in page.get("Contents", []) or [] if o["Key"].endswith(".parquet")]
        seen = collections.defaultdict(list)  # rk -> [(fetched_at, part_key, listing_idx, row)]
        for idx, pk in enumerate(parts):
            raw = client.get_object(Bucket=store.HARVEST_BUCKET, Key=pk)["Body"].read()
            for row in pq.read_table(io.BytesIO(raw)).to_pylist():
                seen[tuple(row.get(f) for f in fields)].append((row["fetched_at"], pk, idx, row))
        new = store.silver_latest(source, table, fields, client=client)
        old = old_silver_latest(store, source, table, fields, client)
        ties = 0
        same_part_dupes = 0
        moves = 0
        ctrl_bad = 0
        for rk, entries in seen.items():
            mx = max(e[0] for e in entries)
            top_e = [e for e in entries if e[0] == mx]
            if len({e[1] for e in top_e}) > 1:
                ties += 1
                old_pick = min(top_e, key=lambda e: e[2])[1]
                new_pick = max(top_e, key=lambda e: store.part_order_key(e[1]))[1]
                rows_differ = _differs(top_e[0][3], top_e[-1][3])
                moved = old_pick != new_pick
                moves += 1 if moved else 0
                all_ties[(source, table, rk)] = {"old": old_pick, "new": new_pick, "moved": moved, "differ": rows_differ}
                say("    TIE %s/%s %r  tied parts=%d  OLD picks %s  NEW picks %s  pick moves=%s  fields differing between tied rows=%s"
                    % (source, table, rk, len({e[1] for e in top_e}), old_pick, new_pick, moved, rows_differ))
            elif len(top_e) > 1:
                same_part_dupes += 1
            if new[rk]["fetched_at"] != mx or old[rk]["fetched_at"] != mx:
                ctrl_bad += 1
        # control: both real readers return, for every key, a row carrying the max fetched_at seen in the parts
        ok_ctrl = ctrl_bad == 0 and len(new) == len(seen) == len(old)
        say("  %s/%s: parts=%d  record keys=%d  tied newest-fetched_at across parts=%d  (same-part duplicates at max=%d)  "
            "keys whose picked part moves old->new=%d  [control: store.silver_latest and old rule both cover all %d keys: %s]"
            % (source, table, len(parts), len(seen), ties, same_part_dupes, moves, len(seen), ok_ctrl))
        total_keys += len(seen)
        total_ties += ties
        total_pick_moves += moves
    say("TOTAL over %d (source, table) pairs read: record keys=%d  tied across parts=%d  picks that move old->new=%d"
        % (len([1 for s, t in tables if t in key_fields]), total_keys, total_ties, total_pick_moves))
    say("")
    return all_ties


# ---------------------------------------------------------------- (3) /timeline/day bodies

DAYS = [("AMZN_US_Equity", "2026-09-07"), ("HD_US_Equity", "2026-08-18"),
        ("992_HK_Equity", "2026-08-13"), ("992_HK_Equity", "2026-09-23")]


def body_for(key, day):
    from lib.research.api import scoped_amgt
    from lib.research.harvest import timeline_api
    body = timeline_api.get_timeline_day(key, day, scoped_amgt._timeline_daily_loader, scoped_amgt._timeline_article_loader)
    return scoped_amgt._timeline_response(body)["body"]


def legacy_body_for(key, day):
    sys.path.insert(0, os.path.join(ROOT, "org", "missions", "D5", "AMGT", "AMGT_HARVST", "deliverables",
                                    "0.9.0_WK_AMGT_HARVST~60", "scripts"))
    import n6_old_path
    from lib.research.api import scoped_amgt
    return scoped_amgt._timeline_response(n6_old_path.get_day(key, day))["body"]


def day_bodies(client, all_ties):
    from lib.research.harvest import publication_gold, store

    say("== (3) /timeline/day body sha256 under the OLD rule and the NEW rule (local route calls, read-only) ==")
    store._default_client = lambda: client  # every route/loader read goes through the read-only, cached client
    strict = lambda f, pk, pf, ppk: f > pf  # noqa: E731  the OLD rule
    real = store.supersedes
    tied_article_keys = {rk[0] for (s, t, rk) in all_ties if t == "article"}
    say("tied article_keys in the served silver: %d" % len(tied_article_keys))
    equal = 0
    for key, day in DAYS:
        publication_gold._SILVER_PART_CACHE.clear()
        store.supersedes = strict
        old_body = body_for(key, day)
        legacy_old = legacy_body_for(key, day)
        store.supersedes = real
        publication_gold._SILVER_PART_CACHE.clear()
        new_body = body_for(key, day)
        legacy_new = legacy_body_for(key, day)
        doc = json.loads(new_body)
        keys_in_day = sorted({a.get("article_key") for a in doc.get("articles") or []})
        touched = sorted(set(keys_in_day) & tied_article_keys)
        sha = lambda s: hashlib.sha256(s.encode("utf-8")).hexdigest()  # noqa: E731
        eq = old_body == new_body
        equal += 1 if eq else 0
        say("%s %s  articles=%d  tied article_keys touching this day=%d %s" % (key, day, len(keys_in_day), len(touched), touched))
        say("  OLD rule  route sha256 %s  len %d" % (sha(old_body), len(old_body)))
        say("  NEW rule  route sha256 %s  len %d" % (sha(new_body), len(new_body)))
        say("  legacy _iter_latest_articles loaders: OLD rule %s  NEW rule %s" % (sha(legacy_old), sha(legacy_new)))
        say("  OLD==NEW byte-equal: %s   route==legacy under NEW rule: %s   route==legacy under OLD rule: %s"
            % (eq, new_body == legacy_new, old_body == legacy_old))
        if not eq and not touched:
            say("  WARN: bodies differ but no tied key touches the day")
    say("OLD==NEW byte-equal on %d of %d named days" % (equal, len(DAYS)))
    say("")


def main():
    census_readers()
    client = ReadOnlyClient()
    ties = served_ties(client)
    day_bodies(client, ties)
    say("S3 calls made: %d LIST, %d GET (read-only proxy; no PUT/DELETE/vendor call is reachable)" % (client.lists, client.gets))
    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(LINES) + "\n")
    say("wrote %s" % OUT)


if __name__ == "__main__":
    main()
