"""cj1_census.py -- AMGT_HARVST HVST-cj-1 (round 95, CTO round-94 analysis item 1). READ-ONLY.

Which harvest tables hold which slash security keys, under which spelling.

RAW     = the prefix  <table>/security_key=<decoded key>/   (what a gateway builds from the typed key)
ENCODED = the prefix  <table>/security_key=<crosswalk.security_key_partition(decoded key)>/
          (what crosswalk.security_key_partition, and so store.entity_partition and write_one, build)

Steps (each line of the output is printed AND written to cj1_census.out, ASCII only):
  c. TABLE lines: every table under amgt/harvest/ and bloomberg/harvest/ (layers and tables FOUND by delimiter listing).
  d. SLASH KEYS FOUND by listing only: encoded children security_key=<X>/ with the -SLASH- token in X, and raw
     children security_key=<X>/ (no token) whose listing continues one more level (a nested raw key X/<sub>/).
  e. MATRIX: every found key x every keyed-by-security table, counted by a listing under the RAW and the ENCODED
     prefix. The silver research-report (date partitions, security in a column) is read by its security_key column.
  f. CONTROLS: the non-slash key UNH_US_Equity (raw prefix == encoded prefix), and the census's own classifier on
     four synthetic pairs.
  g. CENSUS-SLASH final line.

Budget: 12000 requests and 1 GiB of GET body bytes; a list page is one request. The census stops at the budget and
prints BUDGET-EXCEEDED instead of the final line.

Usage, from the worktree root:  python -u <this file>
"""

import io
import os
import re
import sys
import time
from collections import Counter, defaultdict

ROOT = os.getcwd()
sys.path.insert(0, ROOT)

import pyarrow.parquet as pq  # noqa: E402

from lib.research.harvest import store  # noqa: E402
from lib.research.identity import crosswalk  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(HERE, "cj1_census.out")
GATEWAY_PATH = os.path.join(ROOT, "infra", "aws", "ec2", "opal-gateway", "app", "harvest_research.py")

BUCKET = "opal-data-harvest"
ROOTS = ("amgt/harvest/", "bloomberg/harvest/")
SK = "security_key="
TOKEN = crosswalk.SLASH_SAFE_TOKEN
CONTROL_NAME = "UNH_US_Equity"
# A raw nested key continues with the tail of a canonical key (<ROOT>_<CC>_Equity): BP/ then _LN_Equity.
# A nested sub-folder that is not such a tail (a 16-hex source-hash folder) is counted as NESTED-OTHER, never a key.
KEY_TAIL = re.compile(r"[A-Z]{2}_Equity$")
SILVER_COLUMN_TABLE = "amgt/harvest/silver/research-report"
BUDGET_REQUESTS = 12000
BUDGET_BYTES = 1024 ** 3
GATEWAY_LINES = (40, 60)


class BudgetExceeded(Exception):
    pass


class Reader(object):
    """Read-only S3 access: list pages and get_object on the harvest bucket. No other operation exists here."""

    def __init__(self, client):
        self._client = client
        self.requests = 0
        self.bytes = 0

    def _spend(self, requests=1):
        self.requests += requests
        if self.requests > BUDGET_REQUESTS or self.bytes > BUDGET_BYTES:
            raise BudgetExceeded()

    def pages(self, prefix, delimiter=None):
        kwargs = {"Bucket": BUCKET, "Prefix": prefix}
        if delimiter is not None:
            kwargs["Delimiter"] = delimiter
        for page in self._client.get_paginator("list_objects_v2").paginate(**kwargs):
            self._spend()
            yield page

    def get(self, key):
        self._spend()
        resp = self._client.get_object(Bucket=BUCKET, Key=key)
        data = resp["Body"].read()
        self.bytes += len(data)
        if self.bytes > BUDGET_BYTES:
            raise BudgetExceeded()
        return data


def emit(lines, text):
    safe = text.encode("ascii", "backslashreplace").decode("ascii")
    print(safe, flush=True)
    lines.append(safe)


def children(reader, prefix):
    """(sub-prefixes, direct object keys) of prefix from one delimiter listing (all pages)."""
    subs, objs = [], []
    for page in reader.pages(prefix, delimiter="/"):
        subs += [c["Prefix"] for c in page.get("CommonPrefixes", []) or []]
        objs += [o["Key"] for o in page.get("Contents", []) or [] if o["Key"] != prefix]
    return sorted(set(subs)), sorted(objs)


def all_objects(reader, prefix):
    """(key, size) of every object under prefix, recursively (all pages)."""
    out = []
    for page in reader.pages(prefix):
        out += [(o["Key"], o.get("Size", 0)) for o in page.get("Contents", []) or [] if o["Key"] != prefix]
    return out


def classify(raw_n, enc_n):
    """The census's one classifier: two object counts (or row counts) to raw | encoded | both | none."""
    if raw_n > 0 and enc_n > 0:
        return "both"
    if raw_n > 0:
        return "raw"
    if enc_n > 0:
        return "encoded"
    return "none"


def encoded_prefix_part(key):
    return crosswalk.security_key_partition(key)


def gateway_constants():
    """(name, template) for the P_ constants at harvest_research.py lines 40-60, read from the file."""
    out = []
    with open(GATEWAY_PATH, "r", encoding="utf-8") as fh:
        for number, line in enumerate(fh, start=1):
            if GATEWAY_LINES[0] <= number <= GATEWAY_LINES[1]:
                m = re.match(r'^(P_[A-Z_]+)\s*=\s*"([^"]+)"', line)
                if m:
                    out.append((m.group(1), m.group(2)))
    return out


def discover_tables(reader, out):
    """Layers and tables of both roots, by delimiter listing."""
    tables = []
    for root in ROOTS:
        layer_subs, root_objs = children(reader, root)
        out("ROOT %s layers=%d direct_objects=%d" % (root.rstrip("/"), len(layer_subs), len(root_objs)))
        for layer in layer_subs:
            table_subs, layer_objs = children(reader, layer)
            out("LAYER %s tables=%d direct_objects=%d" % (layer.rstrip("/"), len(table_subs), len(layer_objs)))
            tables += table_subs
    return sorted(set(tables))


def main():
    started = time.time()
    lines = []
    out_handle = open(OUT_PATH, "w", encoding="utf-8", newline="\n")

    def out(text):
        emit(lines, text)
        out_handle.write(lines[-1] + "\n")
        out_handle.flush()

    reader = Reader(store._default_client())
    out("CENSUS-HEADER HVST-cj-1 slash-key census (round 95, CTO round-94 analysis item 1); READ-ONLY list and get "
        "on bucket %s only" % BUCKET)
    out("CENSUS-HEADER budget_requests=%d budget_bytes=%d; a list page is one request; bytes counts GET body bytes only"
        % (BUDGET_REQUESTS, BUDGET_BYTES))
    out("CENSUS-HEADER raw_prefix=security_key=<decoded>/ encoded_prefix=crosswalk.security_key_partition(decoded)/")

    try:
        # c. discovery of tables
        tables = discover_tables(reader, out)
        keyed = []   # (table prefix, security partition count, [security child prefixes])
        date_only = []
        empty = []
        for tp in tables:
            subs, objs = children(reader, tp)
            sk_children = [s for s in subs if s[len(tp):].startswith(SK)]
            date_children = [s for s in subs if s[len(tp):].startswith("date=")]
            other_children = [s for s in subs if s not in sk_children and s not in date_children]
            keyed_flag = "yes" if sk_children else "no"
            out("TABLE %s keyed_by_security=%s security_partitions=%d" % (tp.rstrip("/"), keyed_flag, len(sk_children)))
            out("TABLE-DETAIL %s date_partitions=%d other_children=%d direct_objects=%d"
                % (tp.rstrip("/"), len(date_children), len(other_children), len(objs)))
            if sk_children:
                keyed.append((tp, sk_children))
            elif date_children:
                date_only.append(tp)
            else:
                empty.append(tp)
                out("EMPTY-TABLE %s no security partitions, no date partitions, direct_objects=%d -- a none on this "
                    "table is NOT an absence from the world" % (tp.rstrip("/"), len(objs)))
        out("DENOMINATOR tables=%d keyed_by_security=%d date_partitioned_only=%d empty=%d"
            % (len(tables), len(keyed), len(date_only), len(empty)))

        # d. slash keys found by listing: recursive listing of each keyed table
        found = defaultdict(set)            # decoded key -> set of table prefixes where discovered
        discovery = defaultdict(Counter)    # (decoded key, table) -> Counter of discovery kind
        for tp, sk_children in keyed:
            objects = all_objects(reader, tp)
            nested = defaultdict(Counter)   # raw segment X (no token) -> Counter of next-level sub segment
            deep = 0
            for key, _size in objects:
                rest = key[len(tp):]
                if not rest.startswith(SK):
                    continue
                seg = rest[len(SK):].split("/")
                if len(seg) >= 3:
                    if TOKEN in seg[0]:
                        continue
                    nested[seg[0]][seg[1]] += 1
                    if len(seg) >= 4:
                        deep += 1
            for child in sk_children:
                x = child[len(tp) + len(SK):].rstrip("/")
                if TOKEN in x:
                    try:
                        decoded = crosswalk.security_key_from_slash_safe(x)
                    except crosswalk.SlashSafeKeyError as exc:
                        out("DECODE-REFUSED %s child=%s: %s" % (tp.rstrip("/"), x, str(exc)[:120]))
                        continue
                    if "/" in decoded:
                        found[decoded].add(tp)
                        discovery[(decoded, tp)]["encoded-child"] += 1
            other_pairs = 0
            other_objects = 0
            other_sample = None
            for x, subs in nested.items():
                for sub, n in subs.items():
                    if not KEY_TAIL.search(sub):
                        other_pairs += 1
                        other_objects += n
                        other_sample = other_sample or ("%s/%s" % (x, sub))
                        continue
                    decoded = "%s/%s" % (x, sub)
                    found[decoded].add(tp)
                    discovery[(decoded, tp)]["raw-nested"] += n
            if other_pairs:
                out("NESTED-OTHER %s pairs=%d objects=%d sample=%s (not a key tail; not counted as a key)"
                    % (tp.rstrip("/"), other_pairs, other_objects, other_sample))
            if deep:
                out("DEEP-NESTING %s objects_below_third_segment=%d" % (tp.rstrip("/"), deep))

        keys = sorted(found)
        for decoded in keys:
            out("SLASHKEY-FOUND %s" % decoded)
        for decoded in keys:
            for tp in sorted(found[decoded]):
                kinds = ",".join("%s=%d" % (k, v) for k, v in sorted(discovery[(decoded, tp)].items()))
                out("DISCOVERED %s table=%s %s" % (decoded, tp.rstrip("/"), kinds))
        tables_with_keys = len(set(tp for k in keys for tp in found[k]))
        out("DENOMINATOR slash_keys=%d found_in_tables=%d" % (len(keys), tables_with_keys))
        out("DENOMINATOR-DEF found_in_tables = keyed-by-security tables in which a slash key was discovered by listing")

        # e. matrix over keyed tables (listing under each prefix)
        matrix_forms = Counter()
        matrix_lines = []
        for decoded in keys:
            raw_part = SK + decoded + "/"
            enc_part = encoded_prefix_part(decoded) + "/"
            for tp, _sk in keyed:
                raw_n = len(all_objects(reader, tp + raw_part))
                enc_n = len(all_objects(reader, tp + enc_part))
                form = classify(raw_n, enc_n)
                matrix_forms[form] += 1
                matrix_lines.append("SLASHKEY %s table=%s form=%s raw_objects=%d encoded_objects=%d"
                                    % (decoded, tp.rstrip("/"), form, raw_n, enc_n))
        for line in matrix_lines:
            out(line)

        # e (column). Date-partitioned silver research-report: the security_key column of each parquet part.
        column_forms = Counter()
        col_prefix = SILVER_COLUMN_TABLE + "/"
        col_subs, col_objs = children(reader, col_prefix)
        col_dates = [s for s in col_subs if s[len(col_prefix):].startswith("date=")]
        parts = [(k, s) for k, s in all_objects(reader, col_prefix)]
        parquet = sorted((k, s) for k, s in parts if k.endswith(".parquet"))
        non_parquet = len(parts) - len(parquet)
        total_part_bytes = sum(s for _k, s in parquet)
        out("COLUMN-TABLE %s date_partitions=%d objects=%d parquet_parts=%d non_parquet=%d part_bytes=%d"
            % (SILVER_COLUMN_TABLE, len(col_dates), len(parts), len(parquet), non_parquet, total_part_bytes))
        if total_part_bytes > BUDGET_BYTES - reader.bytes:
            raise BudgetExceeded()
        raw_rows = Counter()
        enc_rows = Counter()
        slash_values = Counter()
        enc_value = {}
        for decoded in keys:
            enc_value[decoded] = crosswalk.slash_safe_key(decoded)
        parts_read = 0
        rows_total = 0
        for part_key, _size in parquet:
            data = reader.get(part_key)
            parts_read += 1
            try:
                table = pq.read_table(io.BytesIO(data), columns=["security_key"])
            except Exception as exc:  # recorded, never silently dropped
                out("COLUMN-READ-ERROR part=%s %s: %s" % (part_key.rsplit("/", 1)[-1], type(exc).__name__, str(exc)[:120]))
                continue
            values = table.column("security_key").to_pylist()
            rows_total += len(values)
            counted = Counter(v for v in values if isinstance(v, str))
            for decoded in keys:
                raw_rows[decoded] += counted.get(decoded, 0)
                enc_rows[decoded] += counted.get(enc_value[decoded], 0)
            for v, n in counted.items():
                if "/" in v or TOKEN in v:
                    slash_values[v] += n
        out("COLUMN-READ parts_read=%d parts_listed=%d rows_total=%d" % (parts_read, len(parquet), rows_total))
        for v in sorted(slash_values):
            out("COLUMN-SLASH-VALUE %s rows=%d known_key=%s" % (v, slash_values[v], "yes" if v in found or v in enc_value.values() else "no"))
        for decoded in keys:
            form = classify(raw_rows[decoded], enc_rows[decoded])
            column_forms[form] += 1
            out("SLASHKEY %s table=%s column_form=%s rows=%d raw_rows=%d encoded_rows=%d parts_read=%d"
                % (decoded, SILVER_COLUMN_TABLE, form, raw_rows[decoded] + enc_rows[decoded],
                   raw_rows[decoded], enc_rows[decoded], parts_read))

        # gateway constants versus the stored tables
        out("GATEWAY-CONSTANTS file=harvest_research.py lines=%d-%d" % GATEWAY_LINES)
        for name, template in gateway_constants():
            table_part = template.split(SK)[0].split("%s")[0]
            if not table_part.startswith(ROOTS):
                out("GATEWAY-CONSTANT %s prefix=%s census_root=no" % (name, template))
                continue
            table_path = table_part.rstrip("/")
            listed = any(tp.rstrip("/") == table_path for tp in tables)
            form = "raw-key-builder" if "%s" in template else "no-key"
            out("GATEWAY-CONSTANT %s table=%s table_listed=%s builds=%s" % (name, table_path, "yes" if listed else "no", form))
        for tp in date_only:
            if tp.rstrip("/") != SILVER_COLUMN_TABLE:
                out("DATE-ONLY-NOT-COLUMN-CHECKED %s (the column check is bound to the silver research-report by the order)"
                    % tp.rstrip("/"))

        # f. controls
        raw_c = SK + CONTROL_NAME + "/"
        enc_c = encoded_prefix_part(CONTROL_NAME) + "/"
        out("CONTROL-POSITIVE %s raw_equals_encoded=%s" % (CONTROL_NAME, "yes" if raw_c == enc_c else "no"))
        pairs = [(3, 0), (0, 3), (2, 2), (0, 0)]
        results = [classify(r, e) for r, e in pairs]
        out("CONTROL-NEGATIVE synthetic raw_only=%s encoded_only=%s both=%s neither=%s"
            % (results[0], results[1], results[2], results[3]))

        # g. final line
        cells = len(keys) * (len(keyed) + 1)
        raw_n = matrix_forms["raw"] + column_forms["raw"]
        enc_n = matrix_forms["encoded"] + column_forms["encoded"]
        both_n = matrix_forms["both"] + column_forms["both"]
        none_n = matrix_forms["none"] + column_forms["none"]
        out("CENSUS-SLASH slash_keys=%d tables=%d cells=%d raw=%d encoded=%d both=%d none=%d gets=%d bytes=%d"
            % (len(keys), len(keyed), cells, raw_n, enc_n, both_n, none_n, reader.requests, reader.bytes))
        out("ELAPSED seconds=%d" % int(time.time() - started))
    except BudgetExceeded:
        out("BUDGET-EXCEEDED gets=%d bytes=%d -- census stopped at the budget; no final line" % (reader.requests, reader.bytes))
        out_handle.close()
        return 2
    out_handle.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
