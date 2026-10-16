#!/usr/bin/env python3
"""gen_function_map.py -- one-time generator of infra/aws/lambda/ci/function-map/ from the BASE map (TO-CT-ca-1 step 2).

Worker 0.9.0_WK_NFRA_CTLPLN~145. Standard library only, ASCII only. Reads the map AT THE BASE commit (BASE.txt) through
`git show`, never the working copy. Writes one <function-name>.json per key of the map's `functions` (the entry object
alone, json.dumps(indent=2, sort_keys=False, ensure_ascii=True) + newline) and README.md with the map's metadata
(_description, _note, _updated). `_last_deploy_recorded` is DROPPED (CTO round-29 ruling 2).

Self-check: every file is read back and must equal its source entry; the file count must equal the map's function count.
Last line: FUNCTION-MAP-GEN files=<n> equal=<e> map_functions=<m> ok=<True|False>
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=HERE, capture_output=True).stdout.decode("utf-8").strip()
MAP_REL = "infra/aws/lambda/ci/lambda-source-map.json"
FOLDER = os.path.join(ROOT, "infra", "aws", "lambda", "ci", "function-map")


def base_commit():
    with open(os.path.join(HERE, "BASE.txt"), encoding="ascii") as f:
        return f.read().split()[0]


def main():
    r = subprocess.run(["git", "show", "%s:%s" % (base_commit(), MAP_REL)], cwd=ROOT, capture_output=True)
    if r.returncode != 0:
        raise SystemExit("ERROR: git show base map rc=%d" % r.returncode)
    doc = json.loads(r.stdout.decode("utf-8"))
    funcs = doc["functions"]
    os.makedirs(FOLDER, exist_ok=True)
    # remove only files this generator owns: function json files and the README
    for fn in os.listdir(FOLDER):
        if fn.endswith(".json") or fn == "README.md":
            os.remove(os.path.join(FOLDER, fn))
    for name, entry in funcs.items():
        if "/" in name or "\\" in name or name.startswith("."):
            raise SystemExit("ERROR: function name is not a file stem: %r" % name)
        text = json.dumps(entry, indent=2, sort_keys=False, ensure_ascii=True) + "\n"
        with open(os.path.join(FOLDER, name + ".json"), "w", encoding="ascii", newline="") as f:
            f.write(text)
    readme = [
        "# function-map -- one JSON file per Lambda function",
        "",
        "This folder replaces the single file `infra/aws/lambda/ci/lambda-source-map.json` (retired by TO-CT-ca-1,",
        "NFRA_CTLPLN round 30). Each `<function-name>.json` holds the entry object of that function, with no wrapper.",
        "The file name is the function name. Readers load the folder: `lib/opal_lambda_map.py` (`load_all`, `load_entry`),",
        "and Terraform reads it with `fileset` (`locals.tf` of the three investor-reporting roots).",
        "",
        "## Metadata carried from the retired map (documentation; read by no consumer)",
        "",
        "- `_description`: " + str(doc.get("_description", "")),
        "- `_updated`: " + str(doc.get("_updated", "")),
        "- `_note`: " + str(doc.get("_note", "")),
        "- `_last_deploy_recorded`: DROPPED (CTO round-29 ruling 2). The deploy ledger under",
        "  `org/critical_paths/change_management/` is the record of deploys.",
        "",
        "Base of the split: the commit named in `org/missions/D0/NFRA/NFRA_CTLPLN/deliverables/0.9.0_WK_NFRA_CTLPLN~145/BASE.txt`.",
        "",
    ]
    with open(os.path.join(FOLDER, "README.md"), "w", encoding="ascii", newline="") as f:
        f.write("\n".join(readme))
    # self-check
    files = sorted(fn for fn in os.listdir(FOLDER) if fn.endswith(".json"))
    equal = 0
    for name, entry in funcs.items():
        with open(os.path.join(FOLDER, name + ".json"), encoding="ascii") as f:
            if json.load(f) == entry:
                equal += 1
    ok = len(files) == len(funcs) and equal == len(funcs)
    print("FUNCTION-MAP-GEN files=%d equal=%d map_functions=%d ok=%s" % (len(files), equal, len(funcs), ok))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
