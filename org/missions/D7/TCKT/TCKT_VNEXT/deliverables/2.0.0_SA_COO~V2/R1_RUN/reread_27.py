"""TCKT_VNEXT SA-r-1 pre-stage (CRO UB-20261009T110751Z-9119 step 2): which of the 27 formerly-MORE_THAN_ONE routes run the
released firm clamp LIVE, read from each host's DEPLOYED bytes (never a build log or a CodeSha256 alone).

  - IRPT hosts: the deployed `served.py` must hash to a SIGNED release build input that carries the IB-pr-390 clamp:
      87d9ecc4... = IB-pr-390 (pin 74a62fb46c; IRPT_BCKEND deliverables/0.7.0_AE_CloudOps~IB2/IB100-1_authz_release_after_reads.json);
      ada9bf5b... = IB-pr-409's pin b8a49eee0e (irpt-narrative), i.e. IB-pr-390 plus the additive IB-pr-405 (1cb1c965f3, +5/-1:
                    svc-custody-statement may read persist_inputs for cottonwood only); CTO half @28563e702c.
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
SERVED_RELEASES = {
    "87d9ecc49747f777fd6ec02c3aa82cbe5b9f53edf9d903faf2d87d7582e1b3b6": "IB-pr-390",
    "ada9bf5bcfd107398eacf49d8051e61551ff253c33cf216d9dd404363f7e630e": "IB-pr-409 (390 + 405)",
}
TICKET_OK = {
    "04f5727bebf83e7c19493f944bc1c8ed2f7a28404b5137d6cf2cb32b699f9a38",  # V12 (contains SA-k-1)
    "670686262068808fcf1d3e0c05ce8e92e32441f9382efeb9361c789ab19457a8",  # R13 (V12 + AR-v-21 + OW-l-1)
    # R2-rr-2 (R13 + the report-id shape check), pin a366ce52ec, deployed 2026-10-11T04:19:14Z under the signed pair
    # (R2_RR2_DEPLOY_PACKET_20261011.md @39ccf5774b, CTO half @51c5e7538b). Admitted on a measured read, row TCKT_VNEXT-D2-S28:
    # git diff --numstat 5a36586b5f a366ce52ec on the handler reads 4 added / 0 removed, so every byte of R13 is still there.
    "ca3be34307f70079e48c4a26d1f711e47318285f2cf2722fdf0cfdcbd637eade",
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
        ok = (h in TICKET_OK) if fn == "opal-ticket-api" else (h in SERVED_RELEASES)
        table.append({"function": fn, "routes": rs, "n_routes": len(rs), "code_sha256": f["Configuration"]["CodeSha256"],
                      "last_modified": f["Configuration"]["LastModified"], "member": member, "member_sha256": h,
                      "clamp_live": ok, "release": SERVED_RELEASES.get(h) if fn != "opal-ticket-api" else None,
                      "claim": "measured"})
        print("%-26s %d %s %s %s" % (fn, len(rs), f["Configuration"]["LastModified"][:19], (h or "ABSENT")[:8],
                                     "CLAMPED" if ok else "NOT-RELEASED"))
    done = sum(t["n_routes"] for t in table if t["clamp_live"])
    total = sum(t["n_routes"] for t in table)
    (HERE / "reread_27_table.json").write_text(json.dumps(table, indent=1) + "\n", encoding="utf-8")
    print("READ27 %d/%d" % (done, total))
    return 0 if done == total else 1


if __name__ == "__main__":
    sys.exit(main())
