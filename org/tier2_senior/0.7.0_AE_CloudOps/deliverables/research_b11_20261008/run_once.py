"""Run the exact issuer-pinned research fold once; retain only count/key output."""

import json
import pathlib
import subprocess
import sys
import tempfile
import zipfile

import boto3

out = pathlib.Path(__file__).resolve().parent
repo = pathlib.Path.cwd().resolve()
assert not (out / "run-started.json").exists(), "Already started; no automatic rerun"
before = json.loads((out / "before-versions.json").read_text())
s3 = boto3.client("s3", region_name="us-east-1")
for key, version in before["versions"].items():
    assert (
        s3.head_object(Bucket="opal-data-transcripts", Key=key)["VersionId"] == version
    ), "Prior version moved"
for pin, tree in before["trees"].items():
    assert (
        subprocess.check_output(
            ["git", "rev-parse", pin + ":research_transcripts/structured"], text=True
        ).strip()
        == tree
    )
scratch = pathlib.Path(tempfile.mkdtemp(prefix="cloudops-b11-")).resolve()
archive = scratch / "source.zip"
paths = ["data/", "lib/", "infra/logic/registry/", "org/standards/NAMING_SCHEMA.json"]
subprocess.run(
    [
        "git",
        "archive",
        "--format=zip",
        "--output=" + str(archive),
        "9f8dddcb9b",
        *paths,
    ],
    check=True,
)
with zipfile.ZipFile(archive) as z:
    assert all((scratch / n).resolve().is_relative_to(scratch) for n in z.namelist())
    z.extractall(scratch)
record = {
    "source_commit": "9f8dddcb9b",
    "temp": str(scratch),
    "extracted_paths": paths,
    "source_tree": before["trees"]["HEAD"],
}
(out / "run-started.json").write_text(json.dumps(record, indent=2) + "\n")
command = [
    sys.executable,
    "-m",
    "data.transcripts.scripts.teams.research_fold",
    "--apply",
    "--verify",
    "--src",
    str(repo / "research_transcripts/structured"),
]
with (out / "run.txt").open("w", encoding="utf-8") as log:
    result = subprocess.run(command, cwd=scratch, stdout=log, stderr=subprocess.STDOUT)
record["exit_code"] = result.returncode
(out / "run-result.json").write_text(json.dumps(record, indent=2) + "\n")
print(json.dumps(record, indent=2))
raise SystemExit(result.returncode)
