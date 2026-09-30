"""HVST-n-1 AC2: TWO SAME-DAY RUNS through the collector (Worker.run over the real Publisher
discovery/fetch code) with a COUNTING stub transport over recorded fixtures and a temp-dir store.

  run 1: every fixture article is fetched (count printed)
  run 2: an already-held key fetches 0; ONE planted NEW key fetches exactly 1
  each run writes a run record with keys fetched and keys skipped, both printed
  CONTROL: run 2's fixtures against a FRESH store fetch every article -- proves the counter
  counts and that the held-key zero is the collector's doing, not a counter that never moves.

No vendor call, no S3 client of any kind, no deploy. PASS only if held = 0 and new = 1.
"""

import datetime
import json
from pathlib import Path
import shutil
import sys
import tempfile


def _repo_root():
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "lib" / "opal_data_harvest" / "worker.py").exists():
            return parent
    raise SystemExit("ERROR: repo root not found above %s" % here)


ROOT = _repo_root()
sys.path.insert(0, str(ROOT))

from lib.opal_data_harvest import test_n1_received_bytes_and_run_record as n1  # noqa: E402

OUT = Path(__file__).resolve().parent.parent / "n1_ac2_output.json"
PUBLISHERS = list(n1.PUBLISHERS)


def fixtures_for(new_sa_ids):
    fixtures = {pub: n1.build_fixture(pub, ["1", "2"]) for pub in PUBLISHERS}
    fixtures["sa"] = n1.build_fixture("sa", new_sa_ids)
    return fixtures


def total_article_gets(fixtures, inners):
    return sum(n1.article_gets(fixtures, inners, pub) for pub in PUBLISHERS)


def read_records(root):
    records = [json.loads(p.read_text(encoding="utf-8")) for p in (Path(root) / "run_records").glob("*.json")]
    return sorted(records, key=lambda r: r["started_at"])


def summarise(record):
    return {"run_id": record["run_id"], "started_at": record["started_at"], "counts": record["counts"],
            "keys_fetched": sorted(record["keys_fetched"]),
            "keys_skipped_as_held": sorted(e["key"] for e in record["keys_skipped_as_held"]),
            "skip_reasons": sorted({e["why"] for e in record["keys_skipped_as_held"]})}


def main():
    root = Path(tempfile.mkdtemp(prefix="n1_ac2_"))
    control_root = Path(tempfile.mkdtemp(prefix="n1_ac2_control_"))
    try:
        run1_fixtures = fixtures_for(["1", "2"])
        run2_fixtures = fixtures_for(["1", "2", "3"])
        held_urls = set().union(*(run1_fixtures[p]["article_urls"] for p in PUBLISHERS))
        new_urls = set().union(*(run2_fixtures[p]["article_urls"] for p in PUBLISHERS)) - held_urls

        worker, results1, inners1 = n1.collect(root, run1_fixtures, PUBLISHERS)
        worker.close()
        run1_fetches = total_article_gets(run1_fixtures, inners1)
        print("RUN 1 (fresh store): article GETs served by the counting transport = %d over %d fixture articles"
              % (run1_fetches, len(held_urls)))

        worker, results2, inners2 = n1.collect(root, run2_fixtures, PUBLISHERS)
        worker.close()
        calls2 = [url for pub in PUBLISHERS for inner in inners2.get(pub, []) for url in inner.calls]
        held_fetches = sum(1 for url in calls2 if url in held_urls)
        new_fetches = sum(1 for url in calls2 if url in new_urls)
        print("RUN 2 (same store, same day): GETs to already-held article keys = %d over %d held keys"
              % (held_fetches, len(held_urls)))
        print("RUN 2: GETs to the planted NEW key(s) = %d over %d planted (%s)"
              % (new_fetches, len(new_urls), ", ".join(sorted(new_urls))))

        records = read_records(root)
        for index, record in enumerate(records, start=1):
            print("RUN RECORD %d: %s" % (index, json.dumps(summarise(record), sort_keys=True)))

        c_worker, c_results, c_inners = n1.collect(control_root, run2_fixtures, PUBLISHERS)
        c_worker.close()
        control_fetches = total_article_gets(run2_fixtures, c_inners)
        print("CONTROL (run-2 fixtures, FRESH store): article GETs = %d (every article, held or not)" % control_fetches)

        same_day = (datetime.datetime.fromisoformat(records[0]["started_at"]).date()
                    == datetime.datetime.fromisoformat(records[1]["started_at"]).date()) if len(records) == 2 else False
        checks = {
            "run1_fetched_every_fixture_article": run1_fetches == len(held_urls) == 10,
            "run2_held_fetches_are_zero": held_fetches == 0,
            "run2_new_key_fetches_exactly_one": new_fetches == 1 and len(new_urls) == 1,
            "two_run_records_written": len(records) == 2,
            "run1_record_counts": len(records) == 2 and records[0]["counts"] == {"fetched": 10, "skipped_as_held": 0},
            "run2_record_counts": len(records) == 2 and records[1]["counts"] == {"fetched": 1, "skipped_as_held": 10},
            "run2_record_names_the_new_key": len(records) == 2 and records[1]["keys_fetched"] == ["sa:3"],
            "both_runs_same_utc_day": same_day,
            "control_counter_counts": control_fetches == 11,
        }
        for name, ok in checks.items():
            print("%s: %s" % ("PASS" if ok else "FAIL", name))
        verdict = all(checks.values())
        print("held = %d, new = %d -> %s" % (held_fetches, new_fetches, "PASS" if verdict else "FAIL"))
        OUT.write_text(json.dumps({"run1_fetches": run1_fetches, "held_fetches": held_fetches,
                                   "new_fetches": new_fetches, "control_fetches": control_fetches,
                                   "run_records": [summarise(r) for r in records], "checks": checks,
                                   "verdict": "PASS" if verdict else "FAIL"}, indent=2, sort_keys=True) + "\n",
                       encoding="utf-8")
        return 0 if verdict else 1
    finally:
        shutil.rmtree(root, ignore_errors=True)
        shutil.rmtree(control_root, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
