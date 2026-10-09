"""TCKT_VNEXT SA-r-1 pre-stage (CRO UB-20261009T110751Z-9119 step 2): which of the 27 formerly-MORE_THAN_ONE routes run the
released firm clamp LIVE, read from each host's DEPLOYED bytes (never a build log or a CodeSha256 alone).

  - IRPT hosts: the deployed `served.py` must hash to the IB-pr-390 release build input (pin 74a62fb46c, sha256 87d9ecc4...,
    from IRPT_BCKEND deliverables/0.7.0_AE_CloudOps~IB2/IB100-1_authz_release_after_reads.json `served_py_build_input`).
  - opal-ticket-api: the deployed `lambda_function.py` must carry the SA-k-1 clamp; its live file is checked against the
    V12 pin's bytes (04f5727b..., which contain SA-k-1) or, after R13, against R13's (67068626...).

Prints one line per host and READ27 <clamped>/<total>; writes the table as JSON beside this file. Exit 0 only at 27/27.
Run from the workspace root with the `.tools/aws` shim on PATH (read-only: lambda get-function and the presigned download).
"""
import collections
import hashlib
import io
import json
import subprocess
import sys
import urllib.request
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
CENSUS = Path("org/missions/D7/TCKT/TCKT_VNEXT/deliverables/0.9.0_WK_TCKT_VNEXT~6/SA_ROUTE_CENSUS.json")
SERVED_RELEASE = "87d9ecc49747f777fd6ec02c3aa82cbe5b9f53edf9d903faf2d87d7582e1b3b6"
TICKET_OK = {
    "04f5727bebf83e7c19493f944bc1c8ed2f7a28404b5137d6cf2cb32b699f9a38",  # V12 (contains SA-k-1)
    "670686262068808fcf1d3e0c05ce8e92e32441f9382efeb9361c789ab19457a8",  # R13 (V12 + AR-v-21 + OW-l-1)
}


def _function(name):
    r = subprocess.run(["bash", ".tools/aws", "lambda", "get-function", "--function-name", name, "--output", "json"],
                       capture_output=True, text=True, timeout=120)
    if r.returncode != 0:
        raise SystemExit("READ27-FAIL get-function %s rc=%d %s" % (name, r.returncode, r.stderr.strip()[:200]))
    return json.loads(r.stdout)


def main():
    census = json.loads(CENSUS.read_text(encoding="utf-8"))
    routes = collections.defaultdict(list)
    for row in census["rows"]:
        if any(v.get("verdict") == "MORE_THAN_ONE" for v in row["per_token"].values()):
            routes[row["function"]].append(row["method"] + " " + row["route"])
    table = []
    for fn, rs in sorted(routes.items()):
        f = _function(fn)
        z = zipfile.ZipFile(io.BytesIO(urllib.request.urlopen(f["Code"]["Location"], timeout=120).read()))
        member = "lambda_function.py" if fn == "opal-ticket-api" else "served.py"
        h = hashlib.sha256(z.read(member)).hexdigest() if member in z.namelist() else None
        ok = (h in TICKET_OK) if fn == "opal-ticket-api" else (h == SERVED_RELEASE)
        table.append({"function": fn, "routes": rs, "n_routes": len(rs), "code_sha256": f["Configuration"]["CodeSha256"],
                      "last_modified": f["Configuration"]["LastModified"], "member": member, "member_sha256": h,
                      "clamp_live": ok, "claim": "measured"})
        print("%-26s %d %s %s %s" % (fn, len(rs), f["Configuration"]["LastModified"][:19], (h or "ABSENT")[:8],
                                     "CLAMPED" if ok else "NOT-RELEASED"))
    done = sum(t["n_routes"] for t in table if t["clamp_live"])
    total = sum(t["n_routes"] for t in table)
    (HERE / "reread_27_table.json").write_text(json.dumps(table, indent=1) + "\n", encoding="utf-8")
    print("READ27 %d/%d" % (done, total))
    return 0 if done == total else 1


if __name__ == "__main__":
    sys.exit(main())
