"""TO-DB-b-113 AMENDMENT 1 item 3: what the returns manifest says on each kit, MEASURED by calling the kit's own emit_day.

Usage: python <this file> <kit_dir> <returns.parquet of that kit's run> <out.json>

The kit's handler is imported (handler.py at the kit top). The day's returns frame is read back from the run's own
returns.parquet, and the producer's own emit_day() is called with EXACTLY the arguments handler.py:579 / :620 pass (no `src`),
upload=True, against a stub S3 whose put_object CAPTURES the manifest body and whose stream_to_parquet (the data write) is
replaced by a no-op: no network, no S3 write. first_data_date is passed empty (it is a manifest field unrelated to the method
fields). The record carries the manifest's method fields and the `method` sentence only: no account number, no client figure.
"""
import json
import sys
from pathlib import Path

FIELDS = ("method_version", "valuation_source", "fee_treatment", "price_basis")


class CaptureS3:
    def __init__(self):
        self.bodies = {}

    def put_object(self, **k):
        self.bodies[k["Key"]] = k["Body"]
        return {}


def main(kit, returns_parquet, out_json):
    import pandas as pd
    root = Path(kit).resolve()
    sys.path.insert(0, str(root))
    import handler as h
    if Path(h.__file__).resolve().parent != root:
        raise SystemExit("REFUSED: handler imported from %s, not the kit %s" % (h.__file__, root))
    ard = h.ard
    frame = pd.read_parquet(returns_parquet)
    day = str(frame["business_date"].iloc[0])
    doc = ard.load_declaration()
    firm = ard.firm_scope(ard.source_entry(doc, ard.declared_sources(doc)[0]))
    ard.sp.stream_to_parquet = lambda *a, **k: {"etag": None, "bytes": 0}
    s3 = CaptureS3()
    res = ard.emit_day(s3, frame, firm, day, upload=True, thresholds=h.load_thresholds(), first_data_date={})
    keys = [k for k in s3.bodies if k.endswith("manifest.json")]
    if len(keys) != 1:
        raise SystemExit("REFUSED: %d manifest bodies captured" % len(keys))
    m = json.loads(s3.bodies[keys[0]].decode("utf-8"))
    rec = {"kit": root.name, "day": day, "rows": int(len(frame)), "emit_day_called_without_src": True,
           "manifest_keys_present": {f: (f in m) for f in FIELDS},
           "manifest_method_fields": {f: m.get(f, "<key not in the manifest>") for f in FIELDS},
           "method_sentence": m.get("method"),
           "manifest_key_count": len(m), "res_landed": res.get("landed")}
    Path(out_json).write_text(json.dumps(rec, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(rec["manifest_method_fields"]))


if __name__ == "__main__":
    main(*sys.argv[1:4])
