"""IB-pr-381 offline replay of the directory REFRESH LAMBDA, ONE zip per process (run with python -I). AWS READS ONLY.

Usage:
  python -I replay_refresh.py prev <zip_dir> <scratch_dir>
      writes <scratch>/prev_keys.json: per firm, the artifact key the zip's own `last_manifest` names as the previous accounted-completion
      build for a fire dated 2026-10-08 and for one dated 2026-10-09 (None = outside the walk window). Keys and dates only.
  python -I replay_refresh.py run <live|built> <zip_dir> <scratch_dir> <out.json>
      drives the ZIP'S OWN `refresh.lambda_handler` for inflection and cottonwood against the REAL bucket state, through a read-only S3
      client: every read is real, every put (the manifest the fire would write) is CAPTURED in memory and never sent, SSM is a stub that
      records what would have been dispatched. An OVERLAY substitutes the directory the runner replay landed (runner_replay.py) for the
      served directory, to read the after-state without writing it.
Arms:
  live mode  -- fire_20261008: the live zip on the real served directory.
  built mode -- served_*: the built zip on the real served directory (fire 10-08 and 10-09);
                seeded_*: the built zip with the seeded landed directory overlaid as the served one (the after-read, simulated);
                negative_*: the same with the negative-arm landed directory (a key in the source but missing from the build);
                unseeded_landing_*: the same with the runner landing that carried from the served directory (what the next scheduled run lands).
Output carries reason codes, counts and booleans only: no id, no name. (The previous manifests are real; the manifest each fire would write
is read back from the captured put.)
"""
import datetime as dt
import io
import json
import os
import sys
from contextlib import redirect_stdout

mode = sys.argv[1]
zip_dir, scratch = sys.argv[3 if mode == "run" else 2], sys.argv[4 if mode == "run" else 3]
which = sys.argv[2] if mode == "run" else None
sys.path.insert(0, zip_dir)
import boto3  # noqa: E402
import refresh  # noqa: E402  (this zip's own module)

assert os.path.dirname(os.path.abspath(refresh.__file__)) == os.path.abspath(zip_dir), "refresh resolved outside the zip"
REAL = boto3.client("s3", region_name="us-east-1")
BUCKETS = {"inflection": "opal-data-inf", "cottonwood": "opal-data-cot"}
PREFIX = "investor-reporting/directory"


class ReadOnlyS3(object):
    """Real reads; an optional overlay of {(bucket, key): bytes}; puts are captured, never sent."""

    def __init__(self, overlay=None):
        self.overlay = overlay or {}
        self.writes = []

    def list_objects_v2(self, **kw):
        return REAL.list_objects_v2(**kw)

    def get_object(self, Bucket, Key):
        if (Bucket, Key) in self.overlay:
            data = self.overlay[(Bucket, Key)]

            class _Body(object):
                def read(self_inner):
                    return data

            return {"Body": _Body()}
        return REAL.get_object(Bucket=Bucket, Key=Key)

    def put_object(self, Bucket, Key, Body, ContentType=None):
        self.writes.append((Bucket, Key, Body))


class StubSSM(object):
    def __init__(self):
        self.sent = []

    def get_command_invocation(self, CommandId, InstanceId):
        return {"Status": "Success"}

    def describe_instance_information(self, Filters):
        return {"InstanceInformationList": [{"PingStatus": "Online"}]}

    def send_command(self, **kw):
        self.sent.append(kw.get("Comment"))
        return {"Command": {"CommandId": "replay-cmd-%d" % len(self.sent)}}


STUB = StubSSM()


def _client(kind, client=None):
    if client is not None:
        return client
    if kind == "ssm":
        return STUB
    raise AssertionError("the replay must not need a %r client" % kind)


refresh._client = _client


def get_json(bucket, key):
    return json.loads(REAL.get_object(Bucket=bucket, Key=key)["Body"].read().decode("utf-8"))


def prev_mode():
    out = {}
    ro = ReadOnlyS3()
    for firm, bucket in BUCKETS.items():
        out[firm] = {}
        for fire in ("2026-10-08", "2026-10-09"):
            m = refresh.last_manifest(bucket, dt.date.fromisoformat(fire), client=ro)
            out[firm]["fire_" + fire.replace("-", "")] = (
                None if m is None else {"manifest_as_of": m.get("as_of_business_date"), "reason_code": m.get("reason_code"),
                                        "key": (m.get("delta") or {}).get("directory_key")})
    with open(os.path.join(scratch, "prev_keys.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
    print(json.dumps({f: {k: (v or {}).get("manifest_as_of") for k, v in r.items()} for f, r in out.items()}))


def overlay_from(landed_dir, bucket):
    """{(bucket, key): bytes} for the dated directory.json and latest.json the runner replay landed locally."""
    root = os.path.join(landed_dir, bucket, "investor-reporting", "directory")
    ov = {}
    for dirpath, _dirs, files in os.walk(root):
        for f in files:
            rel = os.path.relpath(os.path.join(dirpath, f), os.path.join(landed_dir, bucket)).replace("\\", "/")
            with open(os.path.join(dirpath, f), "rb") as fh:
                ov[(bucket, rel)] = fh.read()
    return ov


def fire(firm, fire_date, overlay=None):
    os.environ["IRPT_DIRECTORY_BUCKET_MAP"] = json.dumps({firm: BUCKETS[firm]})
    os.environ["IRPT_DIRECTORY_RUNNER_INSTANCE_ID"] = "i-replay"
    os.environ["IRPT_DIRECTORY_BUNDLE_URI"] = "s3://replay/bundle.tar.gz"
    ro = ReadOnlyS3(overlay)
    buf = io.StringIO()
    with redirect_stdout(buf):
        out = refresh.lambda_handler({"business_date": fire_date}, client=ro)
    row = out["results"][0]
    mans = [json.loads(w[2].decode("utf-8")) for w in ro.writes if w[1] == row.get("manifest_key")]
    man = mans[0]
    d = man.get("delta") or {}
    landed_key = d.get("directory_key")
    marked = None
    if landed_key:
        body = json.loads(ro.get_object(BUCKETS[firm], landed_key)["Body"].read().decode("utf-8"))
        marked = sum(1 for e in body.get("entries") or []
                     if (e.get("termination") or {}).get("indicator") == "TERMINATED"
                     and any(isinstance(f, str) and f.startswith("source_removed_on=")
                             for f in (e.get("cohort") or {}).get("capability_facts") or []))
    return {"fire_date": fire_date, "reason_code": man["reason_code"], "state": man["state"],
            "terminated_count": d.get("terminated_count"), "terminated_new": d.get("terminated_new"),
            "added": d.get("added"), "disappeared": d.get("disappeared"),
            "previous_entry_count": d.get("previous_entry_count"), "current_entry_count": d.get("current_entry_count"),
            "previous_found": bool(d.get("previous_entry_count")), "false_additions": d.get("added"),
            "previous_manifest_as_of": row.get("previous_manifest_as_of"),
            "carried_in_landed": (marked or 0) > 0, "marked_entries_in_landed": marked,
            "printed": [ln for ln in buf.getvalue().splitlines() if ln.startswith("irpt-directory-refresh")],
            "dispatches_that_would_be_sent": len(STUB.sent)}


def run_mode():
    out = {"mode": which, "refresh_py": os.path.basename(refresh.__file__), "firms": {}}
    for firm, bucket in BUCKETS.items():
        arms = {}
        if which == "live":
            arms["fire_20261008"] = fire(firm, "2026-10-08")
        else:
            arms["served_1008"] = fire(firm, "2026-10-08")
            arms["served_1009"] = fire(firm, "2026-10-09")
            # (landed directory in scratch, arm name): "served" is the runner landing WITHOUT the seed, i.e. what the next
            # scheduled run lands after the release (it states the source and carries nothing).
            for landed, name in (("seeded", "seeded"), ("negative", "negative"), ("served", "unseeded_landing")):
                ov = overlay_from(os.path.join(scratch, "landed_" + landed), bucket)
                arms[name + "_1008"] = fire(firm, "2026-10-08", ov)
                arms[name + "_1009"] = fire(firm, "2026-10-09", ov)
        out["firms"][firm] = arms
    with open(sys.argv[5], "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
    print(json.dumps({f: {a: (v["reason_code"], v["terminated_count"], v["carried_in_landed"]) for a, v in r.items()}
                      for f, r in out["firms"].items()}))


if mode == "prev":
    prev_mode()
else:
    run_mode()
