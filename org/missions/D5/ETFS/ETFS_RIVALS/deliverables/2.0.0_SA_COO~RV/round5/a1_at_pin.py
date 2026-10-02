"""Run the three A1 producers' handler_entry at one extracted package pin over an overlay (S3 reads, local writes) and
pickle each output frame. usage: python a1_at_pin.py <pkg_scripts_dir> <day> <out_dir>"""
import io
import pathlib
import sys
import tempfile

pkg, day, out = sys.argv[1], sys.argv[2], pathlib.Path(sys.argv[3])
sys.path.insert(0, pkg)
sys.path.insert(1, "C:/Users/Opal Bloomberg/Desktop/ajb_workspace")  # lib.opal_naming
import pyarrow.parquet as pq  # noqa: E402

from rivalfunds import gold_buying_trend, gold_holding_contribution, gold_input_census, sinks  # noqa: E402

assert pathlib.Path(gold_buying_trend.__file__).resolve().is_relative_to(pathlib.Path(pkg).resolve()), gold_buying_trend.__file__


class Overlay:
    kind = "overlay"

    def __init__(self, base, local):
        self.base, self.local = base, local

    def get(self, uri):
        return self.local.get(uri) if self.local.exists(uri) else self.base.get(uri)

    def exists(self, uri):
        return self.local.exists(uri) or self.base.exists(uri)

    def list(self, prefix):
        return sorted(set(self.base.list(prefix)) | set(self.local.list(prefix)))

    def put(self, uri, data, content_type=None):
        return self.local.put(uri, data, content_type)


real = sinks.get_sink
ov = Overlay(real("s3"), sinks.LocalSink(tempfile.mkdtemp(prefix="rv_a1pin_")))
sinks.get_sink = lambda spec: ov if spec in ("overlay", "s3") else real(spec)
out.mkdir(parents=True, exist_ok=True)
for table, mod in (("holding_contribution", gold_holding_contribution), ("buying_trend", gold_buying_trend),
                   ("input_census", gold_input_census)):
    res = mod.handler_entry({"date": day, "sink": "overlay"})
    nu = (res.get("outputs") or [None])[0]
    df = pq.read_table(io.BytesIO(ov.get(nu))).to_pandas() if nu else None
    print(table, res.get("status"), None if df is None else len(df))
    if df is not None:
        df.to_pickle(out / f"{table}.pkl")
