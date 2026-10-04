"""Round 45 HVST-ar-1: the SERVED silver re-derivation, under a never-widen pair (issuer act).

Two modes over the SAME plan:
  --dry-run   the signing gate: reads only (S3 list/get), writes the plan record, prints the gate verdict.
  --write     re-runs the identical plan, refuses unless its digest equals --expect-digest (the digest the
              halves signed), then appends ONE batch per source through the uploader's own retrying
              writer (`uploads._silver_append_retrying_object_name` -> `store.silver_append`).

THE PLAN, per publisher (barrons, bbg, ft, wsj):
  served row = the reader's own rule (`store.supersedes`: newest fetched_at per article_key, a tie to the later
  part). For each stored original whose bronze_key IS the served row of its article_key, the row is rebuilt by
  this checkout's `silver_from_bronze.article_rows` with the served row's own arguments (fetched_at,
  retrieval_mode, run_stamp, discovery fields). It is planned only when its record_hash differs from the served
  row's (silver_append skips the rest by itself).
  An original whose article_key has NO served row is planned as a new row (built as a backfill from its key's
  stamp). An original that is neither (an older or newer fetch of an article another bronze serves) is NOT
  planned: re-deriving it could change which fetch serves.

THE GATE (all must hold):
  CHANGED 0 -- every pre-existing served column keeps its value (record_hash excepted: it re-hashes by design);
  GONE 0    -- every planned rebuilt row keeps its article_key's served position (same fetched_at);
  BUILD 0   -- 0 build errors, and each publisher's batch builds one parquet table per fetch date.
The run_stamp of each source's batch is the greatest part stamp it supersedes, so the written part name sorts
at or after every part it replaces (a name collision gets the -rN suffix, which sorts after its base).
"""

import argparse
import collections
import datetime
import hashlib
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, *([os.pardir] * 8)))
sys.path.insert(0, ROOT)

import pyarrow as pa  # noqa: E402
import pyarrow.parquet as pq  # noqa: E402

from lib.opal_data_harvest import harvest_grammar as hg  # noqa: E402
from lib.opal_data_harvest import silver_from_bronze as sfb  # noqa: E402
from lib.opal_data_harvest import uploads  # noqa: E402
from lib.research.harvest import store  # noqa: E402

PUBLISHERS = ("barrons", "bbg", "ft", "wsj")
DISCOVERY_FIELDS = ("first_discovered_at", "retrieval_rung", "search_query", "search_rank", "search_page", "discovered_for")
RECORD = os.path.join(HERE, "ar-1.rederive_plan.json")


def same(a, b):
    """Value equality across the parquet round trip (the worker manifest's rule): a missing struct key equals None."""
    if a is None or b is None:
        return a is None and b is None
    if isinstance(a, dict) or isinstance(b, dict):
        if not isinstance(a, dict) or not isinstance(b, dict):
            return False
        return all(same(a.get(k), b.get(k)) for k in set(a) | set(b))
    if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
        return len(a) == len(b) and all(same(x, y) for x, y in zip(a, b))
    if isinstance(a, float) and isinstance(b, float) and a != a and b != b:
        return True
    num = (int, float)
    if type(a) is not type(b) and not (isinstance(a, num) and isinstance(b, num)
                                       and not isinstance(a, bool) and not isinstance(b, bool)):
        return False
    return a == b


def list_keys(client, prefix):
    out = []
    for page in client.get_paginator("list_objects_v2").paginate(Bucket=store.HARVEST_BUCKET, Prefix=prefix):
        out += [o["Key"] for o in page.get("Contents", []) or [] if not o["Key"].endswith("/")]
    return out


def served_by_article(client, src):
    """{article_key: (row, part_key)} by store.supersedes -- the rule every silver reader shares."""
    latest, held = {}, {}
    for key in list_keys(client, store.table_prefix(src, "silver", "article")):
        if not key.endswith(".parquet"):
            continue
        raw = client.get_object(Bucket=store.HARVEST_BUCKET, Key=key)["Body"].read()
        for row in pq.read_table(io.BytesIO(raw)).to_pylist():
            ak = row.get("article_key")
            prior = latest.get(ak)
            if prior is None or store.supersedes(row["fetched_at"], key, prior["fetched_at"], held[ak]):
                latest[ak], held[ak] = row, key
    return {ak: (latest[ak], held[ak]) for ak in latest}


def plan_publisher(client, pub):
    src = hg.SOURCE_FOR_PUBLISHER[pub]
    served = served_by_article(client, src)
    served_bronze = {row.get("bronze_key"): ak for ak, (row, _k) in served.items()}
    out = {"originals": 0, "planned_rebuilt": 0, "planned_new": 0, "unchanged": 0, "not_served_fetch": 0,
           "changed": [], "gone": [], "errors": [], "new_keys": [], "parts_superseded": set(), "rows": []}
    for bk in sorted(list_keys(client, store.table_prefix(src, "bronze", "article"))):
        out["originals"] += 1
        obj = client.get_object(Bucket=store.HARVEST_BUCKET, Key=bk)
        body, form = obj["Body"].read(), store.classify_bronze_form(obj.get("Metadata"))
        received = "normalised_record" if form == store.FORM_NORMALISED else "as_received"
        ak_served = served_bronze.get(bk)
        try:
            if ak_served is not None:
                srow, part = served[ak_served]
                discovery = {f: srow.get(f) for f in DISCOVERY_FIELDS}
                new = sfb.article_rows(pub, body, received, bk, srow["fetched_at"],
                                       srow.get("retrieval_mode") or "backfill", srow.get("run_stamp"), discovery=discovery)
            else:
                stem = bk.rsplit("/", 1)[-1].rsplit(".", 1)[0]
                fetched = datetime.datetime.strptime(stem[:15], "%Y%m%dT%H%M%S").replace(tzinfo=datetime.timezone.utc)
                new = sfb.article_rows(pub, body, received, bk, fetched, "backfill", stem, discovery=None)
        except Exception as exc:  # noqa: BLE001 -- reported, never hidden
            out["errors"].append([bk, "%s: %s" % (type(exc).__name__, str(exc)[:200])])
            continue
        if ak_served is None:
            if new.get("article_key") in served:
                out["not_served_fetch"] += 1          # another fetch of a served article: never planned
                continue
            out["planned_new"] += 1
            out["new_keys"].append(bk)
            out["rows"].append(new)
            continue
        srow, part = served[ak_served]
        changed = [c for c in srow if c not in ("record_hash",) and srow.get(c) is not None and not same(srow.get(c), new.get(c))]
        if changed:
            out["changed"].append({"bronze_key": bk, "columns": sorted(changed)})
            continue
        if new["fetched_at"] != srow["fetched_at"]:
            out["gone"].append(bk)
            continue
        if store.record_hash(new) == srow.get("record_hash"):
            out["unchanged"] += 1
            continue
        out["planned_rebuilt"] += 1
        out["parts_superseded"].add(part)
        out["rows"].append(new)
    # BINS: silver_append builds ONE parquet table per fetch date per call, and rows that never shared a served part
    # can disagree on a value's type (bbg `duration` int vs str, wsj `caption` list vs str; row Z-W93-S2). Per fetch
    # date, a row joins the FIRST bin whose table still builds with it (pa.Table.from_pylist + write, exactly as
    # silver_append builds it); else it opens a new bin. One append per bin, so every call writes one date partition.
    by_date = collections.defaultdict(list)
    for r in sorted(out["rows"], key=lambda r: r["bronze_key"]):
        by_date[r["fetched_at"].date()].append(r)
    out["table_errors"] = []
    out["bins"] = []
    for d, rows in sorted(by_date.items()):
        bins = []
        for r in rows:
            for b in bins:
                try:
                    pq.write_table(pa.Table.from_pylist(b + [r]), io.BytesIO())
                except (pa.ArrowInvalid, pa.ArrowTypeError):
                    continue
                b.append(r)
                break
            else:
                try:
                    pq.write_table(pa.Table.from_pylist([r]), io.BytesIO())
                    bins.append([r])
                except Exception as exc:  # noqa: BLE001 -- a row that cannot build alone is a gate failure
                    out["table_errors"].append([d.isoformat(), r["bronze_key"], "%s: %s" % (type(exc).__name__, str(exc)[:300])])
        out["bins"] += bins
    out["bin_sizes"] = [len(b) for b in out["bins"]]
    stamps = [store.part_order_key(p)[0] for p in out["parts_superseded"]]
    stamps += [r["run_stamp"] for r in out["rows"] if r["bronze_key"] in set(out["new_keys"])]
    out["batch_run_stamp"] = max(stamps) if stamps else None
    out["digest"] = hashlib.sha256(json.dumps([sorted((r["bronze_key"], store.record_hash(r)) for r in b)
                                               for b in out["bins"]]).encode()).hexdigest()
    return src, out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--expect-digest", default=None)
    ap.add_argument("--publishers", default=",".join(PUBLISHERS))
    a = ap.parse_args()
    if a.dry_run == a.write:
        ap.error("exactly one of --dry-run / --write")
    client = store._default_client()
    plans, ok = {}, True
    for pub in a.publishers.split(","):
        src, p = plan_publisher(client, pub)
        plans[pub] = (src, p)
        gate = not p["changed"] and not p["gone"] and not p["errors"] and not p["table_errors"]
        ok = ok and gate
        print("=== %s: originals %d; rebuilt %d; new %d; unchanged %d; other-fetch not planned %d; CHANGED %d; GONE %d; "
              "errors %d; table errors %d; parts superseded %d; batch run_stamp %s; bins %s; gate %s"
              % (pub, p["originals"], p["planned_rebuilt"], p["planned_new"], p["unchanged"], p["not_served_fetch"],
                 len(p["changed"]), len(p["gone"]), len(p["errors"]), len(p["table_errors"]), len(p["parts_superseded"]),
                 p["batch_run_stamp"], p["bin_sizes"], "HOLDS" if gate else "FAILS"))
        for x in (p["changed"][:5] + p["gone"][:5] + p["errors"][:5] + p["table_errors"][:5]):
            print("   ", x)
    digest = hashlib.sha256(json.dumps({pub: plans[pub][1]["digest"] for pub in sorted(plans)}).encode()).hexdigest()
    record = {"measured_at": datetime.datetime.now(datetime.timezone.utc).isoformat(), "mode": "write" if a.write else "dry-run",
              "plan_digest": digest, "gate": "HOLDS" if ok else "FAILS",
              "publishers": {pub: {k: (sorted(v) if isinstance(v, set) else v) for k, v in p.items() if k not in ("rows", "bins")}
                             for pub, (_s, p) in plans.items()}}
    print("PLAN DIGEST: %s" % digest)
    print("GATE: %s" % record["gate"])
    if a.write:
        if not ok:
            print("REFUSED: the gate fails; nothing written")
            return 1
        if a.expect_digest != digest:
            print("REFUSED: plan digest %s != signed %s; nothing written" % (digest, a.expect_digest))
            return 1
        written = {}
        for pub, (src, p) in plans.items():
            if not p["rows"]:
                written[pub] = None
                continue
            res = []
            for b in p["bins"]:
                res.append(uploads._silver_append_retrying_object_name(client, src, "article", b, ("article_key",),
                                                                      p["batch_run_stamp"]))
            written[pub] = res
            print("WRITTEN %s: %d bins, rows %d, parts %s" % (pub, len(res), sum(x.get("written_rows", 0) for x in res),
                                                              [pt for x in res for pt in x.get("parts", [])]))
        record["written"] = written
        # VERIFY on the served plane: every planned row is now the row its article_key serves.
        verify = {}
        for pub, (src, p) in plans.items():
            now = served_by_article(client, src)
            want = {r["article_key"]: store.record_hash(r) for r in p["rows"]}
            serving = sum(1 for ak, h in want.items() if ak in now and now[ak][0].get("record_hash") == h)
            verify[pub] = {"planned": len(want), "serving": serving}
            print("VERIFY %s: planned %d, now serving %d" % (pub, len(want), serving))
            ok = ok and serving == len(want)
        record["verify"] = verify
        record["gate"] = "HOLDS" if ok else "FAILS"
        print("VERIFY: %s" % record["gate"])
    out = RECORD if a.dry_run else RECORD.replace(".json", ".written.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(record, fh, indent=1, default=str)
    print("RECORD: %s" % out)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
