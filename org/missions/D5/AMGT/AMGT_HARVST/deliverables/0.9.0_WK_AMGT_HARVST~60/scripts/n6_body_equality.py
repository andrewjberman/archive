"""HVST-n-6: writes ../n6_ac3_body_equality.txt -- the 3 named real days (+ the extra 992_HK day with
articles) served by the OLD path (verbatim copy of the @d357a9e247 loaders), the NEW path (the repo code
as it stands), and the DEPLOYED route (read-only Invoke), with the sha256 of each body; plus the census
the publisher-pruning rests on (every silver article_key's prefix names the source it sits in).
READ-ONLY: S3 LIST/GET, read-only Invokes."""
import collections
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import n6_common as c  # noqa: E402

OUT = os.path.join(os.path.dirname(c.HERE), "n6_ac3_body_equality.txt")


def census():
    sys.path.insert(0, c.ROOT)
    import boto3
    import pyarrow.parquet as pq
    from lib.opal_data_harvest.harvest_grammar import SOURCE_FOR_PUBLISHER
    from lib.research.harvest import store

    cl = boto3.client("s3", region_name="us-east-1")
    code_of = {src: code for code, src in SOURCE_FOR_PUBLISHER.items()}
    total = mismatch = parts = 0
    seen = collections.defaultdict(set)
    for src in sorted(code_of):
        prefix = store.table_prefix(src, "silver", "article")
        for page in cl.get_paginator("list_objects_v2").paginate(Bucket=store.HARVEST_BUCKET, Prefix=prefix):
            for o in page.get("Contents", []) or []:
                if not o["Key"].endswith(".parquet"):
                    continue
                parts += 1
                raw = cl.get_object(Bucket=store.HARVEST_BUCKET, Key=o["Key"])["Body"].read()
                for k in pq.read_table(io.BytesIO(raw), columns=["article_key"]).column("article_key").to_pylist():
                    total += 1
                    seen[k].add(src)
                    if not isinstance(k, str) or k.split(":", 1)[0] != code_of[src]:
                        mismatch += 1
    multi = sum(1 for v in seen.values() if len(v) > 1)
    return parts, total, mismatch, multi, len(seen)


def main():
    lines = ["HVST-n-6 AC3 body equality: OLD path (n6_old_path.py, lib @d357a9e247 verbatim) vs NEW path (repo code) "
             "vs DEPLOYED route (opal-amgt-scoped-api)", ""]
    ok = 0
    for key, day in c.ALL_DAYS:
        old, old_body = c.spawn("old", key, day, 1)
        new, new_body = c.spawn("new", key, day, 1)
        _w, _rep, status, dep_body = c.invoke_deployed(key, day)
        eq = old_body == new_body
        eq_dep = new_body == dep_body
        ok += 1 if eq else 0
        tag = "" if (key, day) in c.NAMED_DAYS else "  [EXTRA day, not named by the TO]"
        lines.append("%s %s%s  articles=%s" % (key, day, tag, new[0]["articles"]))
        lines.append("  OLD  sha256 %s  len %d" % (c.sha256_text(old_body), len(old_body)))
        lines.append("  NEW  sha256 %s  len %d" % (c.sha256_text(new_body), len(new_body)))
        lines.append("  DEPL sha256 %s  len %d  (status %s)" % (c.sha256_text(dep_body), len(dep_body), status))
        lines.append("  OLD==NEW byte-equal: %s   NEW==DEPLOYED byte-equal: %s" % (eq, eq_dep))
    lines.append("")
    lines.append("OLD==NEW byte-equal on %d of %d days" % (ok, len(c.ALL_DAYS)))
    parts, total, mismatch, multi, distinct = census()
    lines.append("")
    lines.append("PUBLISHER-PRUNING PREMISE (article_key prefix names its silver source): %d silver article parts, "
                 "%d rows, %d distinct article_keys; rows whose prefix != the source they sit in: %d of %d; "
                 "article_keys present in more than one source: %d of %d" % (
                     parts, total, distinct, mismatch, total, multi, distinct))
    text = "\n".join(lines) + "\n"
    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
    print(text)
    print("wrote %s" % OUT)


if __name__ == "__main__":
    main()
