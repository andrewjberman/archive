"""Compose IB93-1_release_replay.json from the three replay outputs (counts only; no id, no name).

Usage: python -I compose_replay.py <scratch_dir> <pin> <out.json> <built_refresh_sha256_b64> <runner_bundle_sha256_hex> <live_refresh_codesha256_b64>
"""
import json
import os
import sys

scratch, pin, out_path, refresh_sha, bundle_sha, live_sha = sys.argv[1:7]
runner = json.load(open(os.path.join(scratch, "runner_result.json"), encoding="utf-8"))
built = json.load(open(os.path.join(scratch, "refresh_built.json"), encoding="utf-8"))
live = json.load(open(os.path.join(scratch, "refresh_live.json"), encoding="utf-8"))
prev = json.load(open(os.path.join(scratch, "prev_keys.json"), encoding="utf-8"))


def pick(a, *keys):
    return {k: a.get(k) for k in keys}


FIELDS = ("reason_code", "terminated_count", "terminated_new", "added", "disappeared", "previous_entry_count",
          "current_entry_count", "carried_in_landed", "marked_entries_in_landed")
firms = {}
for firm in ("inflection", "cottonwood"):
    b, lv, rr = built["firms"][firm], live["firms"][firm], runner["firms"][firm]
    seeded = b["seeded_1008"]
    rec = {
        # THE ARM THE AFTER-READ NEEDS: the one-time reconciling runner run (previous = the last accounted-completion build)
        # landed, then the built refresh on it.
        "built": dict(pick(seeded, *FIELDS), arm="seeded runner landing + built refresh, fire 2026-10-08",
                      carried_in_landed=rr["seeded"]["carried_in_landed"]),
        "live": pick(lv["fire_20261008"], "reason_code", "terminated_count", "disappeared"),
        # WHAT A SCHEDULED RUN DOES TODAY: previous = the served directory, which has already lost the entry (row D2-W189-S1).
        "built_unseeded_served_previous": {
            "runner": rr["served"], "refresh_fire_20261008": pick(b["served_1008"], *FIELDS),
            "refresh_fire_20261009": pick(b["served_1009"], *FIELDS)},
        "negative_in_source_but_missing_from_build": {
            "runner": rr["negative"], "refresh_fire_20261008": pick(b["negative_1008"], *FIELDS)},
        "unseeded_landing_refresh": {"fire_20261008": pick(b["unseeded_landing_1008"], *FIELDS),
                                     "fire_20261009": pick(b["unseeded_landing_1009"], *FIELDS)},
        "seeded_fire_20261009": pick(b["seeded_1009"], *FIELDS),
        "runner_seeded": rr["seeded"],
        "served_directory_before": rr["served_directory_read"],
        "last_accounted_completion_build": {k: (v or {}).get("manifest_as_of") for k, v in prev[firm].items()},
    }
    if firm == "inflection":
        f9 = b["served_1009"]
        rec["fire_20261009"] = {"previous_found": f9["previous_found"], "false_additions": f9["false_additions"],
                                "previous_manifest_as_of": f9["previous_manifest_as_of"],
                                "previous_entry_count": f9["previous_entry_count"], "reason_code": f9["reason_code"],
                                "note": "last_manifest (unchanged by this release) finds no manifest for this fire (the 2026-09-25 build is the 11th trading day back): "
                                        "the built code reads the served directory as the previous state"}
    firms[firm] = rec
out = {"pin": pin, "to_id": "IRPT_BCKEND.TO-IB-pr-381",
       "built_refresh_zip_sha256_b64": refresh_sha, "built_runner_bundle_sha256": bundle_sha,
       "live_refresh_codesha256_b64": live_sha,
       "method": "built runner bundle (BUILD_ONLY from the clean tree at the pin, extracted) driven by replay_runner.py on the real source "
                 "snapshots and real previous directories; built and live refresh zips driven by replay_refresh.py through lambda_handler on "
                 "the real bucket state with a read-only S3 client (puts captured, never sent) and a stub SSM. AWS reads only.",
       "firms": firms}
with open(out_path, "w", encoding="utf-8") as fh:
    json.dump(out, fh, indent=1, sort_keys=True)
print("wrote", out_path)
