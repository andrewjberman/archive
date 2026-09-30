"""IRPT_DASHBD round 1 AC (DB-b-3, C-FLOWTIME) -- the winning flow-timing convention and the proposed tie-out tolerance are WRITTEN
where the method lives: the method contract file and the served dim_return_method row agree with the record.

Usage: python p1_3_ac2_method_winner_written.py <worktree root>
Reads the tie-out record (flow_convention_winner, proposed_tieout_tolerance), org/standards/IRPT_DASHBD_DIM_RETURN_METHOD_CONTRACT.json
(method_versions[0].flow_convention and .tieout_tolerance_proposed) and gold dim_return_method/method_version=1 on S3
(flow_convention, tieout_tolerance_proposed). All three agree.
Pass line: DB-3-AC2 PASS. Base (at the cut): FAIL -- no record.
"""
import io
import json
import sys
from pathlib import Path

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
sys.path.insert(0, str(root))
REC = root / "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.4.0_DS_ClientPlatform~S/tieout/TIEOUT_49F_BLACKDIAMOND_R1.json"
CON = root / "org/standards/IRPT_DASHBD_DIM_RETURN_METHOD_CONTRACT.json"


def fail(msg):
    print("DB-3-AC2 FAIL: " + msg)
    sys.exit(1)


if not REC.exists():
    fail("record absent: %s" % REC)
rec = json.loads(REC.read_text(encoding="utf-8"))
win, tol = rec.get("flow_convention_winner"), rec.get("proposed_tieout_tolerance")
if not CON.exists():
    fail("method contract absent")
con = json.loads(CON.read_text(encoding="utf-8"))
mv = (con.get("method_versions") or [{}])[0]
if mv.get("flow_convention") != win or mv.get("tieout_tolerance_proposed") != tol:
    fail("contract method_versions[0] reads flow_convention %r tieout_tolerance_proposed %r; record %r %r" % (
        mv.get("flow_convention"), mv.get("tieout_tolerance_proposed"), win, tol))
from lib import opal_naming as on  # noqa: E402
import boto3  # noqa: E402
import pyarrow.parquet as pq  # noqa: E402

b, k = (on.address("irpt", "49financial", "gold", "dim_return_method", "method_version=1") + "/data.parquet")[5:].split("/", 1)
row = pq.read_table(io.BytesIO(boto3.client("s3", region_name="us-east-1").get_object(Bucket=b, Key=k)["Body"].read())).to_pylist()[0]
if row.get("flow_convention") != win or row.get("tieout_tolerance_proposed") is None or abs(float(row["tieout_tolerance_proposed"]) - float(tol)) > 1e-12:
    fail("served dim_return_method row reads flow_convention %r tieout_tolerance_proposed %r; record %r %r" % (
        row.get("flow_convention"), row.get("tieout_tolerance_proposed"), win, tol))
print("  contract and served row agree: flow_convention %s, tieout_tolerance_proposed %s" % (win, tol))
print("DB-3-AC2 PASS")
