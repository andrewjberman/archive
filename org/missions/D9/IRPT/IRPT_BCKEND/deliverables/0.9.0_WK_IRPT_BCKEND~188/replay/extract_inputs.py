"""IB-pr-380 replay input extractor. AWS READS ONLY. Raw extracts are written OUTSIDE the worktree and deleted after.

Usage (from the repo root):
  python extract_inputs.py <live_zip_dir> <out_dir> <fire_date YYYY-MM-DD>

Per firm (inflection, cottonwood) it reads, from AWS:
  * the PREVIOUS READY build  -- the live zip's own `refresh.last_manifest` names its directory_key; that artifact's entries;
  * the NEW build             -- `latest.json` and the dated artifact it names (what the next fire would compare against);
  * the SOURCE SNAPSHOT       -- the runner's own source adapter (`directory_runner.SOURCE_SETS`) loads the snapshot the build read;
                                 the source client ids are every key the source holds, minted with the production opaque function
                                 (inflection: household ids of the household map and of accounts_v2, plus account ids;
                                 cottonwood: non-sentinel Relationship IDs plus AccountIDs).
It writes <out_dir>/inputs_<firm>.json (client entries inside: NEVER commit it) and prints only counts.
"""
import datetime as dt
import json
import os
import sys

zip_dir, out_dir, fire = sys.argv[1], sys.argv[2], sys.argv[3]
REPO = os.getcwd()
sys.path.insert(0, zip_dir)
sys.path.insert(0, os.path.join(REPO, "data", "assets", "scripts", "gold", "investor_reporting"))
import boto3  # noqa: E402
import refresh  # noqa: E402  (the LIVE zip's own module)
import directory_runner as dr  # noqa: E402

s3 = boto3.client("s3", region_name="us-east-1")
BUCKETS = {"inflection": "opal-data-inf", "cottonwood": "opal-data-cot"}
SENTINEL = "0"


def get(bucket, key):
    return json.loads(s3.get_object(Bucket=bucket, Key=key)["Body"].read().decode("utf-8"))


def source_ids_inf(data):
    firm = "inflection"
    acc, hh = data["accounts"], data["households"]
    raws = set(str(x) for x in hh["household_id"].dropna().astype(str))
    raws |= set(str(x) for x in acc["household_id"].dropna().astype(str))
    raws |= set(str(x) for x in acc["account_id"].dropna().astype(str))
    raws = {r for r in raws if r and r.lower() != "nan"}
    return sorted(dr.opaque_id("client", firm, r) for r in raws)


def source_ids_cot(data):
    firm = "cottonwood"
    alloc = data["allocations"]
    raws = set()
    for r in alloc.to_dict("records"):
        rid = dr._s(r.get("Relationship ID"))
        if rid not in ("", "nan", SENTINEL):
            raws.add(rid)
        aid = dr._s(r.get("AccountID"))
        if aid and aid != "nan":
            raws.add(aid)
    return sorted(dr.opaque_id("client", firm, r) for r in raws)


ADAPT = {"inflection": (dr.FirmINF, source_ids_inf), "cottonwood": (dr.FirmCOT, source_ids_cot)}


def main():
    now = dt.date.fromisoformat(fire)
    for firm, bucket in BUCKETS.items():
        prev = refresh.last_manifest(bucket, now, client=s3)
        prev_key = (prev.get("delta") or {}).get("directory_key")
        prev_art = get(bucket, prev_key)
        prev_entries = prev_art["entries"]
        pointer = get(bucket, "investor-reporting/directory/latest.json")
        body = get(bucket, pointer["key"])
        build_entries = body["entries"]
        cls, ids_fn = ADAPT[firm]
        src = cls()
        data = src.load(pointer["as_of_business_date"])
        source_ids = ids_fn(data)

        def kof(e):
            return (e.get("ids") or {}).get("client_id") or (e.get("ids") or {}).get("relationship_id")
        prev_keys, build_keys, src_keys = {kof(e) for e in prev_entries}, {kof(e) for e in build_entries}, set(source_ids)
        dropped = sorted(prev_keys - build_keys)
        # POSITIVE CONTROL: the source snapshot of the PREVIOUS build's date must hold the dropped ids, or the
        # source-id computation above could not have told "present" from "absent".
        try:
            older = ids_fn(cls().load(prev_art["as_of_business_date"]))
            control = {"snapshot": prev_art["as_of_business_date"], "dropped_ids_in_older_source": len(set(dropped) & set(older)),
                       "dropped": len(dropped)}
        except Exception as exc:  # noqa: BLE001
            control = {"snapshot": prev_art["as_of_business_date"], "error": type(exc).__name__}
        rec = {"firm": firm, "source_positive_control": control, "previous_manifest_as_of": prev.get("as_of_business_date"), "previous_directory_key": prev_key,
               "new_directory_key": pointer["key"], "as_of": pointer["as_of_business_date"],
               "source_completion_date": pointer.get("source_completion_date"),
               "directory_revision": pointer.get("directory_revision"),
               "source_snapshot_notes": src.notes,
               "previous_entries": prev_entries, "build_entries": build_entries,
               "source_client_ids": source_ids, "dropped_ids": dropped}
        with open(os.path.join(out_dir, "inputs_%s.json" % firm), "w", encoding="utf-8") as fh:
            json.dump(rec, fh)
        print("%s: previous=%d entries (%s), build=%d entries (%s), source ids=%d, dropped=%d, dropped in source=%d, "
              "build keys not in source=%d; positive control %s" % (firm, len(prev_entries), rec["previous_manifest_as_of"], len(build_entries),
                                              rec["as_of"], len(source_ids), len(dropped), len(set(dropped) & src_keys),
                                              len(build_keys - src_keys), control))


main()
