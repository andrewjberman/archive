"""IB-pr-380 offline replay of the directory refresh, ONE zip per process (run with python -I). No network, no AWS.

Usage: python -I replay_zip.py <live|built> <unzipped_zip_dir> <inputs_dir> <out.json>

Drives the ZIP'S OWN `refresh.refresh_firm` with each firm's real inputs from `extract_inputs.py`:
  previous_entries = the previous READY build; build = the latest landed build; source_client_ids = the source snapshot.
  * live  mode: the live zip, given the real input (it has no source-removal rule, so it must fail on the dropped entry);
  * built mode: the built zip on the same input (the rule: READY + terminated_count), then the NEGATIVE ARM -- the same input
                with the dropped id put back into the source ONLY (the entry stays missing from the build: REFRESH_FAILED).
The output carries reason codes and counts only: no id, no name.
"""
import io
import json
import os
import sys
from contextlib import redirect_stdout

mode, zip_dir, in_dir, out_path = sys.argv[1:5]
sys.path.insert(0, zip_dir)
import refresh  # noqa: E402  (this zip's own module)

assert os.path.dirname(os.path.abspath(refresh.__file__)) == os.path.abspath(zip_dir), "refresh resolved outside the zip"


def drive(rec, source_ids):
    built = {"entries": list(rec["build_entries"]), "business_date": rec["as_of"],
             "source_completion_date": rec["source_completion_date"], "directory_revision": rec["directory_revision"]}
    if source_ids is not None:
        built["source_client_ids"] = list(source_ids)
    buf = io.StringIO()
    with redirect_stdout(buf):
        env, man = refresh.refresh_firm(rec["firm"], rec["fire_date"], build_fn=lambda f, d: built,
                                        previous_entries=rec["previous_entries"])
    delta = man.get("delta") or {}
    marked = [e for e in built["entries"]
              if (e.get("termination") or {}).get("indicator") == "TERMINATED"
              and getattr(refresh, "source_removed_on_of", lambda x: None)(e)]
    return {"reason_code": man["reason_code"], "state": man["state"], "terminated_count": delta.get("terminated_count"),
            "disappeared": delta.get("disappeared"), "previous_entry_count": delta.get("previous_entry_count"),
            "current_entry_count": delta.get("current_entry_count"), "added": delta.get("added"),
            "carried_marked_entries_in_build": len(marked), "printed": buf.getvalue().strip()}


out = {"mode": mode, "zip_refresh_py": refresh.__file__.replace("\\", "/").rsplit("/", 1)[-1], "firms": {}}
for firm in ("inflection", "cottonwood"):
    with open(os.path.join(in_dir, "inputs_%s.json" % firm), "r", encoding="utf-8") as fh:
        rec = json.load(fh)
    rec["fire_date"] = "2026-10-08"
    res = {"inputs": {"previous_entries": len(rec["previous_entries"]), "build_entries": len(rec["build_entries"]),
                      "source_client_ids": len(rec["source_client_ids"]), "dropped": len(rec["dropped_ids"])},
           "source_positive_control": rec.get("source_positive_control")}
    res["run"] = drive(rec, rec["source_client_ids"])
    if mode == "built":
        res["negative"] = drive(rec, sorted(set(rec["source_client_ids"]) | set(rec["dropped_ids"])))
        res["unknown_source"] = drive(rec, None)
    out["firms"][firm] = res
with open(out_path, "w", encoding="utf-8") as fh:
    json.dump(out, fh, indent=1, sort_keys=True)
print(json.dumps({f: {k: (v["reason_code"], v["terminated_count"]) if k != "inputs" and isinstance(v, dict) and "reason_code" in v else None
                      for k, v in r.items() if isinstance(v, dict) and "reason_code" in v} for f, r in out["firms"].items()}))
