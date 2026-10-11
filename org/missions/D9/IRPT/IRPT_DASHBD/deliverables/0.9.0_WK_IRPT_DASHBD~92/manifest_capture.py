"""TO-DB-b-117: capture EVERY object the reporting-gold handler's run would write, from a kit's OWN handler, with no write.

Usage: python <this file> <kit_dir> <day> <raw_out.json>

The kit's handler.run_backfill() runs UNCHANGED (the handler's own code path, the arguments the handler actually passes to
ard.emit_day, acd.emit_class_day, aal.emit_day) for ONE already-landed day, accounts="population". The S3 client it receives is a
GUARD: reads are delegated to the real client (S3 GETs / LISTs only); put_object is CAPTURED (key and body kept, never sent); any other
write verb raises. The data write (ard.sp.stream_to_parquet, shared by all three producers) is replaced by a stub that returns a
fixed result and counts its calls, so no object lands. record_lots_status is then called once more with a forced refusal (the run
itself states nothing: every lots day lands) so the status record's shape is captured for both kits.

The raw output holds the manifest bodies, which carry account ids: it is written OUTSIDE the repo and never committed. The
field-level record that goes in the repo is made by manifest_compare.py, which hashes anything account-keyed or a client figure.
"""
import json
import sys
from pathlib import Path

WRITE_VERBS = ("create_multipart_upload", "upload_part", "complete_multipart_upload", "abort_multipart_upload", "upload_file",
               "upload_fileobj", "put_object_acl", "delete_object", "delete_objects", "copy_object", "copy", "put_object_tagging")


class Guard:
    def __init__(self, real):
        self._real = real
        self.captured = {}
        self.puts = 0

    def put_object(self, **k):
        self.puts += 1
        self.captured[k["Bucket"] + "/" + k["Key"]] = k["Body"]
        return {}

    def __getattr__(self, name):
        if name in WRITE_VERBS:
            raise SystemExit("REFUSED by the capture guard: %s" % name)
        return getattr(self._real, name)


def main(kit, day, raw_out):
    import boto3
    from botocore.config import Config
    root = Path(kit).resolve()
    sys.path.insert(0, str(root))
    import handler as h
    if Path(h.__file__).resolve().parent != root:
        raise SystemExit("REFUSED: handler imported from %s, not the kit %s" % (h.__file__, root))
    stream_calls = []

    def stream_stub(tables, schema, s3, bucket, key, **k):
        for _ in tables:
            pass
        stream_calls.append(bucket + "/" + key)
        return {"etag": None, "bytes": 0}

    h.ard.sp.stream_to_parquet = stream_stub
    g = Guard(boto3.client("s3", config=Config(max_pool_connections=32, retries={"max_attempts": 6, "mode": "adaptive"})))
    event = {"backfill": {"start": day, "end": day}, "accounts": "population"}
    res = h.run_backfill(g, event)
    run_keys = sorted(g.captured)
    run_bodies = {k: g.captured[k].decode("utf-8") for k in run_keys}
    # the status record: forced refusal, because the run states nothing when every day lands
    doc = h.ard.load_declaration()
    firm = h.ard.firm_scope(h.ard.source_entry(doc, h.ard.declared_sources(doc)[0]))

    class NoPrior:
        def __init__(self, cap):
            self.cap = cap

        def get_object(self, **k):
            class NoSuchKey(Exception):
                pass
            raise NoSuchKey("no prior status")

        def put_object(self, **k):
            self.cap[k["Bucket"] + "/" + k["Key"]] = k["Body"]
            return {}

    status = {}
    h.record_lots_status(NoPrior(status), firm, set(), {day: "forced refusal (capture harness)"}, True)
    out = {"kit": root.name, "day": day, "handler_sha": None, "run_summary_keys": sorted(res),
           "run_put_count": g.puts, "stream_calls": sorted(stream_calls), "run_keys": run_keys, "run_bodies": run_bodies,
           "status_forced": {k: v.decode("utf-8") for k, v in status.items()},
           "lots_status_written_by_the_run": any("_status" in k for k in run_keys)}
    Path(raw_out).write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    print("DONE puts=%d stream_calls=%d keys=%d" % (g.puts, len(stream_calls), len(run_keys)), flush=True)


if __name__ == "__main__":
    main(*sys.argv[1:4])
