"""AMGT_CORPUS round 49, CRPS-ay-5 PRE-READ -- what the rendered census WILL read once the API serves /15. Issuer's file. READ-ONLY.

  PYTHONPATH=. python ay5_preread_inject.py <live capture.json> <out.json>

Takes aw4_capture.py's output over the LIVE function (serving an earlier method) and replaces each name's `model.team_sheet` with the STORED /15 dossier field
(`read_dossier` at METHOD /15 -- exactly what `_team_sheet_from_dossier` will return once the redeployed API picks the /15 objects). The result is
fed to ay5_rendered_census.cjs as a prediction; the real read is taken on the live function after the redeploy. Prints `preread names <n> injected <k>`.
"""
import json
import sys

from lib.research.corpus import dossier
from lib.research.harvest import store


def main(argv):
    cap = json.load(open(argv[0], encoding="utf-8"))
    client = store._default_client()
    dossier.METHOD_VERSION = "amgt-corpus-dossier/15"
    injected = 0
    for key, rec in cap["keys"].items():
        doc = dossier.read_dossier(key, client=client)["document"]
        if doc.get("method_version") != "amgt-corpus-dossier/15":
            continue
        rec["model"]["team_sheet"] = (doc.get("fields") or {}).get("team_sheet")
        injected += 1
    cap["function"] = dict(cap["function"], injected="stored /15 team_sheet (a prediction, not the live function)")
    json.dump(cap, open(argv[1], "w", encoding="utf-8"), sort_keys=True, ensure_ascii=True)
    print("preread names %d injected %d" % (len(cap["keys"]), injected))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
