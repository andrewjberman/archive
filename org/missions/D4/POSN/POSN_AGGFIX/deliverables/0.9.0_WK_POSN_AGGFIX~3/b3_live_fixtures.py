#!/usr/bin/env python
"""
LIVE_FIXTURES_B3 -- POSN_AGGFIX.TO-B3-1, criterion B3-AC1.

Reads the PRIOR and NEW VersionIds of json/positioning/positioning_data.json FROM TO-A3-1's PROOF INSTANCE
(never from this worker's memory and never from a key-only read), fetches both objects BY VERSIONID, fetches
the live json/positioning/opal_aggregate.json with its VersionId, decompresses each, and writes the three
fixture files <FIVE_BOOKS_DOM_B> and <AGG_DOM_B2> read in B3-AC2 and B3-AC3.

GRAIN: the ids are taken from TWO acceptance rows of the same instance (A3-AC8's head reads and A3-AC9's
compare reads) and required to AGREE where both carry an id -- one instance, two loci.

A key-only read is never a substitute: it returns whatever is served that minute. The aggregate is fetched at
the VersionId the LIVE head reports, and that id is printed beside the one TO-A3-1 recorded, equal or not.

Writes (three fixtures, and the provenance manifest OUTSIDE the fixture directory so the directory holds
exactly the three):
    .scratch/b3_fixtures/prior_shared.json
    .scratch/b3_fixtures/new_shared.json
    .scratch/b3_fixtures/aggregate.json
    .scratch/b3_fixtures.manifest.json   (provenance, not a fixture)
"""
import gzip
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import timezone

BUCKET = "opal-data-portal-v2"
SHARED_KEY = "json/positioning/positioning_data.json"
AGG_KEY = "json/positioning/opal_aggregate.json"
A3_INSTANCE = ("org/missions/D4/POSN/POSN_AGGFIX/deliverables/0.9.0_WK_POSN_AGGFIX~1/"
               "POSN_AGGFIX.TO-A3-1.deploy-the-producer-and-read-the-served-result.proof_of_spec.json")
A3_DRIVE_STATE = ("org/missions/D4/POSN/POSN_AGGFIX/deliverables/0.9.0_WK_POSN_AGGFIX~1/"
                  "a3_drive_state.json")
MODEL_CODES = ["UST", "ST", "INT", "LT", "ULT"]
PRIOR_EXPECT = ["UST", "ST", "INT", "LT", "ULT", "AGG"]
NEW_EXPECT = ["UST", "ST", "INT", "LT", "ULT"]

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=HERE, capture_output=True,
                      text=True).stdout.strip()
CHECKS = []


def check(label, ok, detail=""):
    CHECKS.append((label, bool(ok)))
    print(("OK: " if ok else "ERROR: ") + label + (("  " + detail) if detail else ""))


def sha256(b):
    return hashlib.sha256(b).hexdigest()


def md5(b):
    return hashlib.md5(b).hexdigest()


def ids_from_compare_row(ev):
    """A3-AC9's read lines."""
    out = {}
    m = re.search(r"READ\s+json/positioning/positioning_data\.json\s+prior\s+VersionId\s+(\S+)", ev)
    if m:
        out["shared_prior"] = m.group(1)
    m = re.search(r"READ\s+json/positioning/positioning_data\.json\s+new\s+VersionId\s+(\S+)", ev)
    if m:
        out["shared_new"] = m.group(1)
    m = re.search(r"READ\s+json/positioning/opal_aggregate\.json\s+VersionId\s+(\S+)", ev)
    if m:
        out["agg"] = m.group(1)
    return out


def ids_from_head_row(ev):
    """A3-AC8's BEFORE/AFTER head reads -- the second locus."""
    out = {}
    m = re.search(r"BEFORE\s+HEAD\s+json/positioning/positioning_data\.json\s+VersionId\s+(\S+)", ev)
    if m:
        out["shared_prior"] = m.group(1)
    m = re.search(r"AFTER\s+HEAD\s+json/positioning/positioning_data\.json\s+VersionId\s+(\S+)", ev)
    if m:
        out["shared_new"] = m.group(1)
    m = re.search(r"AFTER\s+HEAD\s+json/positioning/opal_aggregate\.json\s+VersionId\s+(\S+)", ev)
    if m:
        out["agg"] = m.group(1)
    return out


def main():
    print("LIVE_FIXTURES_B3 at %s (workspace HEAD %s)" % (
        ROOT, subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True,
                             text=True).stdout.strip()))

    # ---- 1. THE IDS, FROM TO-A3-1'S PROOF INSTANCE -------------------------------------------------
    inst_path = os.path.join(ROOT, A3_INSTANCE)
    inst_commit = subprocess.run(["git", "log", "-1", "--format=%H", "--", A3_INSTANCE], cwd=ROOT,
                                 capture_output=True, text=True).stdout.strip()
    with open(inst_path, encoding="utf-8") as fh:
        inst = json.load(fh)
    rows = {r.get("criterion_id"): r for r in inst.get("acceptance", [])}
    print("SOURCE INSTANCE: %s @%s (acceptance rows %d)" % (A3_INSTANCE, inst_commit, len(rows)))

    loci = {}
    if "A3-AC9" in rows:
        loci["A3-AC9"] = ids_from_compare_row(rows["A3-AC9"].get("output_evidence", ""))
    if "A3-AC8" in rows:
        loci["A3-AC8"] = ids_from_head_row(rows["A3-AC8"].get("output_evidence", ""))
    for row_id in sorted(loci):
        print("  FROM %s: %s" % (row_id, json.dumps(loci[row_id], sort_keys=True)))

    merged, disagreements, compared = {}, [], 0
    for row_id in sorted(loci):
        for k, v in loci[row_id].items():
            if k in merged:
                compared += 1
                if merged[k] != v:
                    disagreements.append("%s: %s vs %s" % (k, merged[k], v))
            else:
                merged[k] = v
    check("the instance's two loci agree on every id they share",
          not disagreements,
          "ids compared across loci %d; disagreements %s" % (compared, disagreements or "none"))
    check("the instance carries the prior and the new VersionId of %s" % SHARED_KEY,
          bool(merged.get("shared_prior")) and bool(merged.get("shared_new")),
          "prior=%s new=%s" % (merged.get("shared_prior"), merged.get("shared_new")))
    if not (merged.get("shared_prior") and merged.get("shared_new")):
        print("CHECKS HOLD %d of %d" % (sum(1 for _, o in CHECKS if o), len(CHECKS)))
        return 1

    prior_id, new_id = merged["shared_prior"], merged["shared_new"]
    agg_id_recorded = merged.get("agg")
    print("VERSIONID shared PRIOR (read from the instance): %s" % prior_id)
    print("VERSIONID shared NEW   (read from the instance): %s" % new_id)
    print("VERSIONID aggregate    (recorded by TO-A3-1)   : %s" % agg_id_recorded)
    check("the prior and the new VersionId differ", prior_id != new_id)

    # SUPPLEMENTARY, a different artifact by the same worker -- corroboration, not the source.
    try:
        with open(os.path.join(ROOT, A3_DRIVE_STATE), encoding="utf-8") as fh:
            ds = json.load(fh)
        print("SUPPLEMENTARY a3_drive_state.json: prior=%s new=%s agg=%s (agrees with the instance: %s)" % (
            ds.get("shared_prior_version_id"), ds.get("shared_new_version_id"), ds.get("agg_version_id"),
            ds.get("shared_prior_version_id") == prior_id and ds.get("shared_new_version_id") == new_id))
    except Exception as exc:  # the instance is the source; this line is corroboration only
        print("SUPPLEMENTARY a3_drive_state.json unreadable: %s" % exc)

    # ---- 2. THE LIVE READS, BY VERSIONID -----------------------------------------------------------
    import boto3
    s3 = boto3.client("s3")

    def head(key, version_id):
        return s3.head_object(Bucket=BUCKET, Key=key, VersionId=version_id)

    def fetch(key, version_id, label):
        h = head(key, version_id)
        lm = h["LastModified"].astimezone(timezone.utc)
        body = s3.get_object(Bucket=BUCKET, Key=key, VersionId=version_id)["Body"].read()
        enc = h.get("ContentEncoding")
        print("FETCHED %-9s %s @%s  LastModified %s  ContentLength %s  ContentEncoding %s  stored md5=%s sha256=%s"
              % (label, key, version_id, lm.isoformat().replace("+00:00", "Z"), h["ContentLength"],
                 enc, md5(body), sha256(body)[:16]))
        check("%s: bytes fetched == ContentLength" % label, len(body) == h["ContentLength"],
              "%d of %d" % (len(body), h["ContentLength"]))
        raw = gzip.decompress(body) if enc == "gzip" else body
        doc = json.loads(raw.decode("utf-8"))
        return doc, lm, h, body, raw

    prior_doc, prior_lm, prior_h, prior_body, _ = fetch(SHARED_KEY, prior_id, "PRIOR")
    new_doc, new_lm, new_h, new_body, _ = fetch(SHARED_KEY, new_id, "NEW")
    check("the PRIOR version is EARLIER than the NEW version", prior_lm < new_lm,
          "prior %s < new %s" % (prior_lm.isoformat().replace("+00:00", "Z"),
                                 new_lm.isoformat().replace("+00:00", "Z")))

    # The aggregate: the LIVE head's VersionId is the one fetched, printed beside TO-A3-1's recorded id.
    agg_live = s3.head_object(Bucket=BUCKET, Key=AGG_KEY)
    agg_id_live = agg_live["VersionId"]
    print("VERSIONID aggregate    (LIVE head right now)   : %s  (equal to TO-A3-1's recorded id: %s)"
          % (agg_id_live, agg_id_live == agg_id_recorded))
    agg_doc, agg_lm, agg_h, agg_body, _ = fetch(AGG_KEY, agg_id_live, "AGG")

    # ---- 3. WHAT THE BYTES CARRY -------------------------------------------------------------------
    prior_keys = list((prior_doc.get("current_holdings") or {}).keys())
    new_keys = list((new_doc.get("current_holdings") or {}).keys())
    print("PRIOR current_holdings keys: %s" % prior_keys)
    print("NEW   current_holdings keys: %s" % new_keys)
    check("the PRIOR shared file carries current_holdings %s" % " ".join(PRIOR_EXPECT),
          sorted(prior_keys) == sorted(PRIOR_EXPECT), "read %s" % prior_keys)
    check("the NEW shared file carries current_holdings %s (no AGG)" % " ".join(NEW_EXPECT),
          sorted(new_keys) == sorted(NEW_EXPECT), "read %s" % new_keys)

    agg_holdings = ((agg_doc.get("current_holdings") or {}).get("AGG") or {}).get("holdings")
    agg_holdings = agg_holdings if isinstance(agg_holdings, list) else []
    print("AGGREGATE status=%s reason=%s data_as_of=%s generated_at=%s holdings=%d total_aum=%s"
          % (agg_doc.get("status"), agg_doc.get("reason"), agg_doc.get("data_as_of"),
             agg_doc.get("generated_at"), len(agg_holdings),
             ((agg_doc.get("current_holdings") or {}).get("AGG") or {}).get("total_aum")))
    print("AGGREGATE top-level keys (file order): %s" % list(agg_doc.keys()))
    check("the live aggregate's status is OK", agg_doc.get("status") == "OK",
          "status=%r" % agg_doc.get("status"))
    check("the live aggregate's current_holdings.AGG.holdings is non-empty", len(agg_holdings) > 0,
          "holdings=%d" % len(agg_holdings))
    if agg_holdings:
        h0 = agg_holdings[0]
        print("AGGREGATE holding[0] keys: %s" % list(h0.keys()))
        print("AGGREGATE holding[0] ticker=%s weight=%s model_breakdown=%s"
              % (h0.get("ticker"), h0.get("weight"), json.dumps(h0.get("model_breakdown"))))
        with_mb = sum(1 for h in agg_holdings if isinstance(h.get("model_breakdown"), dict)
                      and h["model_breakdown"])
        print("AGGREGATE holdings carrying a non-empty model_breakdown: %d of %d"
              % (with_mb, len(agg_holdings)))
        codes = sorted({c for h in agg_holdings for c in (h.get("model_breakdown") or {})})
        print("AGGREGATE model_breakdown codes across every holding: %s (the five: %s)"
              % (codes, MODEL_CODES))

    # ---- 4. THE THREE FIXTURE FILES ----------------------------------------------------------------
    fx_dir = os.path.join(ROOT, ".scratch", "b3_fixtures")
    os.makedirs(fx_dir, exist_ok=True)
    written = []
    for name, doc in (("prior_shared.json", prior_doc), ("new_shared.json", new_doc),
                      ("aggregate.json", agg_doc)):
        blob = (json.dumps(doc, indent=1, sort_keys=False) + "\n").encode("utf-8")
        dest = os.path.join(fx_dir, name)
        with open(dest, "wb") as fh:   # binary: a text-mode write CRLF-ifies on this device
            fh.write(blob)
        back = open(dest, "rb").read()
        ok = back == blob
        written.append({"file": name, "bytes": len(blob), "sha256": sha256(blob), "read_back_equal": ok})
        print("WROTE .scratch/b3_fixtures/%-17s %7d bytes  sha256=%s  read-back equal=%s"
              % (name, len(blob), sha256(blob)[:16], ok))
        check("%s read back byte-identical" % name, ok)

    on_disk = sorted(os.listdir(fx_dir))
    print("FIXTURE FILES WRITTEN %d of 3; the directory holds %d file(s): %s"
          % (len(written), len(on_disk), on_disk))
    check("the fixture directory holds exactly the three fixtures",
          on_disk == ["aggregate.json", "new_shared.json", "prior_shared.json"], "%s" % on_disk)

    manifest = {
        "written_by": "0.9.0_WK_POSN_AGGFIX~3", "to_id": "POSN_AGGFIX.TO-B3-1", "criterion": "B3-AC1",
        "source_instance": A3_INSTANCE, "source_instance_commit": inst_commit,
        "ids_by_locus": loci, "bucket": BUCKET,
        "shared_key": SHARED_KEY, "agg_key": AGG_KEY,
        "shared_prior": {"version_id": prior_id,
                         "last_modified": prior_lm.isoformat().replace("+00:00", "Z"),
                         "stored_bytes": len(prior_body), "stored_md5": md5(prior_body),
                         "current_holdings": prior_keys},
        "shared_new": {"version_id": new_id,
                       "last_modified": new_lm.isoformat().replace("+00:00", "Z"),
                       "stored_bytes": len(new_body), "stored_md5": md5(new_body),
                       "current_holdings": new_keys},
        "aggregate": {"version_id_live": agg_id_live, "version_id_recorded_by_a3": agg_id_recorded,
                      "last_modified": agg_lm.isoformat().replace("+00:00", "Z"),
                      "stored_bytes": len(agg_body), "stored_md5": md5(agg_body),
                      "status": agg_doc.get("status"), "holdings": len(agg_holdings)},
        "files": written,
    }
    man_path = os.path.join(ROOT, ".scratch", "b3_fixtures.manifest.json")
    with open(man_path, "wb") as fh:
        fh.write((json.dumps(manifest, indent=1) + "\n").encode("utf-8"))
    print("WROTE .scratch/b3_fixtures.manifest.json (provenance, NOT a fixture)")

    held = sum(1 for _, ok in CHECKS if ok)
    print("CHECKS HOLD %d of %d" % (held, len(CHECKS)))
    return 0 if held == len(CHECKS) else 1


if __name__ == "__main__":
    sys.exit(main())
