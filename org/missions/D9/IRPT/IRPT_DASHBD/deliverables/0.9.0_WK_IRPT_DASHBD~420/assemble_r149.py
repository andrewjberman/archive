"""IRPT_DASHBD round 149, TO DB-c-29, worker 0.9.0_WK_IRPT_DASHBD~420 -- assembles FWD10_49F_CENSUS_R149.json from the three measurement outputs.

Usage: python assemble_r149.py <gold.json> <series.json> <page.json> <read_utc> <record_path>

Each input is the ONE JSON line printed by its script (gold_census_r149.py, read_publish_r149.py, page_read_r149.ts).
It copies their numbers into the record's fixed fields and writes nothing else. It holds no identifier and no value of its own.
"""
import json
import sys
from pathlib import Path


def last_json_line(path):
    lines = [x for x in Path(path).read_text(encoding="utf-8").splitlines() if x.strip()]
    return json.loads(lines[-1])


def main(argv):
    gold_path, series_path, page_path, read_utc, record_path = argv
    gold = last_json_line(gold_path)
    series = last_json_line(series_path)
    page = last_json_line(page_path)
    reads = {
        "s3_list_calls": gold["reads"]["s3_list_calls"] + series["reads"]["s3_list_calls"],
        "s3_get_calls": series["reads"]["s3_get_calls"],
        "writes": 0,
        "invokes": 0,
    }
    record = {
        "label": "TEST READ -- not a serve, not a production run",
        "read_utc": read_utc,
        "firm_scope": "49financial",
        "gold": gold["gold"],
        "series_truth": series["series_truth"],
        "page": page,
        "reads": reads,
        "claim": "measured",
        "ids_recorded": False,
        "pushed": False,
        "deployed": False,
    }
    Path(record_path).write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("wrote record keys=%d" % len(record))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
