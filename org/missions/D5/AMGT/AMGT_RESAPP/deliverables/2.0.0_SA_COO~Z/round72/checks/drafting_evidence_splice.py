"""AMGT_RESAPP round 72 -- av-8's drafting leg, NARROWED: splice ONLY the driver-chart point passages into the stored drafting
documents, never a full rebuild.

A full `drafting_build --rebuild-pool` re-applies the whole gate. Measured 2026-10-05 ~23:0xZ against the stored objects:
- BA: it adds `anchored` / `text_original` to every drafted sentence, beside the 3 new evidence records;
- ASML: it DELETES `thesis_driver_provenance`.
That is wider than the act. This splice changes exactly two things per document:
- `evidence_records` gains the records whose `id` the current producer (`build_drafting_document`, av-3) emits and the stored
  document lacks;
- `denominators.evidence_records` is set to the new length.

  python drafting_evidence_splice.py --keys BA_US_Equity,ASML_NA_Equity --dry-run
  python drafting_evidence_splice.py --keys BA_US_Equity,ASML_NA_Equity --write --pre-act-dir <dir>

Per key it prints the records added, the paths that differ between stored and spliced (must be exactly the two above), the
stored sha256 and, on --write, the new VersionId. --write saves each key's pre-act bytes to --pre-act-dir before its write.
Exit 0 only when every key's diff is exactly the two paths and at least one record was added.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys

BUCKET = "opal-data-harvest"


def _diff(a, b, path="", out=None):
    out = [] if out is None else out
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a or k not in b:
                out.append(f"{path}.{k}")
            else:
                _diff(a[k], b[k], f"{path}.{k}", out)
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            out.append(path)
        else:
            for i, (x, y) in enumerate(zip(a, b)):
                _diff(x, y, path, out)
    elif a != b:
        out.append(path)
    return sorted(set(out))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--keys", required=True)
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--write", action="store_true")
    ap.add_argument("--pre-act-dir", default=None)
    a = ap.parse_args()
    if a.write and not a.pre_act_dir:
        ap.error("--write requires --pre-act-dir")
    import boto3
    from lib.research.filings import drafting_build as db

    s3 = boto3.client("s3", region_name="us-east-1")
    ok = True
    for key in [k for k in a.keys.split(",") if k]:
        dkey = db._drafting_pool_key(key)
        raw = s3.get_object(Bucket=BUCKET, Key=dkey)["Body"].read()
        stored = json.loads(raw)
        rebuilt = db.build_drafting_document(db._get_json_object(s3, db._newest_analysis_key(s3, key)))
        have = {r.get("id") for r in stored.get("evidence_records") or []}
        add = [r for r in rebuilt.get("evidence_records") or [] if r.get("id") not in have]
        spliced = json.loads(raw)
        spliced["evidence_records"] = list(stored.get("evidence_records") or []) + add
        spliced.setdefault("denominators", {})["evidence_records"] = len(spliced["evidence_records"])
        paths = _diff(stored, spliced)
        # serialize exactly as the stored object was: the options that round-trip its bytes, or refuse
        fmt = None
        for indent in (2, 1, None):
            for ascii_ in (True, False):
                for sk in (False, True):
                    for nl in (b"", b"\n"):
                        if json.dumps(stored, indent=indent, ensure_ascii=ascii_, sort_keys=sk).encode("utf-8") + nl == raw:
                            fmt = (indent, ascii_, sk, nl)
        good = bool(add) and paths == [".denominators.evidence_records", ".evidence_records"] and fmt is not None
        ok = ok and good
        print(f"{key}: object {dkey} stored_sha256 {hashlib.sha256(raw).hexdigest()} records {len(have)} -> "
              f"{len(spliced['evidence_records'])} added {[r.get('id') for r in add]} diff_paths {paths} format {fmt} {'OK' if good else 'REFUSED'}")
        if a.write and good:
            os.makedirs(a.pre_act_dir, exist_ok=True)
            with open(os.path.join(a.pre_act_dir, key + ".json"), "wb") as fh:
                fh.write(raw)
            body = json.dumps(spliced, indent=fmt[0], ensure_ascii=fmt[1], sort_keys=fmt[2]).encode("utf-8") + fmt[3]
            put = s3.put_object(Bucket=BUCKET, Key=dkey, Body=body, ContentType="application/json")
            print(f"   WROTE {dkey} VersionId {put.get('VersionId')} bytes {len(body)}")
    print("SPLICE:", "YES" if ok else "NO")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
