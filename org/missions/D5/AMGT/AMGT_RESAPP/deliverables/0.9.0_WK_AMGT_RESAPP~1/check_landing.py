"""check_landing.py -- AC2: read back from S3 (never from the pull's own log) whether raw
landed before derived, with no overwrite, across the three securities this order touched.

Prints exactly one line:
    LANDING: raw <N> objects across <M> securities; derived <K> objects; raw-before-derived <bool>; overwrites <n>

CONSUMER SEMANTICS (STORE_CONTRACT.md section 4, rule 2 -- "a consumer reads the LATEST stamp
under a prefix"): this script reads the CURRENT landing state, i.e. the latest raw stamp and the
latest derived stamp per security, not every stamp ever written. `derive` is independently
re-runnable (C-STAGE-PERSISTS) and was in fact re-run here (once to embed a placeholder unit
pointer, once more after build_field_map.py existed, to embed the actual measured unit/sign) --
each re-run mints a fresh stamp rather than overwriting, so more than one derived stamp can exist
per security; the current landing is the latest one, per the contract's own reading rule.

- raw objects (current): the 2 artifacts (refdata.json, histdata.json) at each security's LATEST
  raw stamp.
- derived objects (current): the 1 artifact (model_block.json) at each security's LATEST derived
  stamp.
- raw-before-derived: for each security, the LATEST raw stamp must be < the LATEST derived stamp
  (stamps are UTC fixed-width so string comparison is chronological).
- overwrites: S3 object-VERSION count minus 1, summed over EVERY key ever written under the three
  securities' raw/derived prefixes (not just the latest stamp) -- a versioned bucket's own record
  of whether any single key was ever written to twice (STORE_CONTRACT.md section 4 rule 1: a
  correct writer never does this; a fresh stamp is a NEW key, not a second version of an old one;
  versioning is the safety net that would catch a writer that got this wrong).
"""
from __future__ import annotations

import boto3

BUCKET = "opal-data-research"
SECURITIES = ["SAP GY Equity", "BA US Equity", "BABA US Equity"]


def security_key(security: str) -> str:
    return security.replace(" ", "_")


def list_all_keys(s3, prefix: str) -> list[str]:
    keys = []
    token = None
    while True:
        kwargs = {"Bucket": BUCKET, "Prefix": prefix}
        if token:
            kwargs["ContinuationToken"] = token
        resp = s3.list_objects_v2(**kwargs)
        keys.extend(obj["Key"] for obj in resp.get("Contents", []))
        if resp.get("IsTruncated"):
            token = resp.get("NextContinuationToken")
        else:
            break
    return keys


def list_common_prefixes(s3, prefix: str) -> list[str]:
    resp = s3.list_objects_v2(Bucket=BUCKET, Prefix=prefix, Delimiter="/")
    return [cp["Prefix"][len(prefix):-1] for cp in resp.get("CommonPrefixes", [])]


def version_count(s3, key: str) -> int:
    resp = s3.list_object_versions(Bucket=BUCKET, Prefix=key)
    versions = [v for v in resp.get("Versions", []) if v["Key"] == key]
    return len(versions)


def main() -> int:
    s3 = boto3.client("s3")

    current_raw_objects: list[str] = []
    current_derived_objects: list[str] = []
    all_keys_ever: list[str] = []
    raw_before_derived = True
    securities_with_raw = set()

    for sec in SECURITIES:
        sec_key = security_key(sec)
        raw_prefix = f"raw/bloomberg/{sec_key}/"
        derived_prefix = f"derived/model_block/{sec_key}/"

        all_keys_ever.extend(list_all_keys(s3, raw_prefix))
        all_keys_ever.extend(list_all_keys(s3, derived_prefix))

        raw_stamps = sorted(list_common_prefixes(s3, raw_prefix))
        derived_stamps = sorted(list_common_prefixes(s3, derived_prefix))

        if raw_stamps:
            securities_with_raw.add(sec)
            latest_raw = raw_stamps[-1]
            current_raw_objects.extend(list_all_keys(s3, f"{raw_prefix}{latest_raw}/"))
        if derived_stamps:
            latest_derived = derived_stamps[-1]
            current_derived_objects.extend(list_all_keys(s3, f"{derived_prefix}{latest_derived}/"))

        if not raw_stamps or not derived_stamps:
            raw_before_derived = False
        elif not (raw_stamps[-1] < derived_stamps[-1]):
            raw_before_derived = False

    overwrites = 0
    for k in all_keys_ever:
        vc = version_count(s3, k)
        if vc > 1:
            overwrites += vc - 1

    print(
        f"LANDING: raw {len(current_raw_objects)} objects across {len(securities_with_raw)} securities; "
        f"derived {len(current_derived_objects)} objects; raw-before-derived {raw_before_derived}; "
        f"overwrites {overwrites}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
