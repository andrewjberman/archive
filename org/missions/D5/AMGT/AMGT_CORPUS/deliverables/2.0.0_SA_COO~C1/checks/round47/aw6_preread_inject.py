"""AMGT_CORPUS round 47, CRPS-aw-6 PRE-READ -- what the rendered census WILL read once the API serves /13. Issuer's file. READ-ONLY.

  PYTHONPATH=. python aw6_preread_inject.py <live capture.json> <out.json>

Takes aw4_capture.py's output over the LIVE function (serving /12) and replaces each name's `model.team_sheet` with the STORED /13 dossier field
(`read_dossier` at METHOD /13 -- exactly what `_team_sheet_from_dossier` will return once the redeployed API picks the /13 objects). The result is
fed to aw6_rendered_census.cjs as a prediction; the real read is taken on the live function after the redeploy. Prints `preread names <n> injected <k>`.
"""
import json
import sys

from lib.research.corpus import dossier
from lib.research.harvest import store


def main(argv):
    cap = json.load(open(argv[0], encoding="utf-8"))
    client = store._default_client()
    dossier.METHOD_VERSION = "amgt-corpus-dossier/13"
    injected = 0
    for key, rec in cap["keys"].items():
        doc = dossier.read_dossier(key, client=client)["document"]
        if doc.get("method_version") != "amgt-corpus-dossier/13":
            continue
        rec["model"]["team_sheet"] = (doc.get("fields") or {}).get("team_sheet")
        injected += 1
    cap["function"] = dict(cap["function"], injected="stored /13 team_sheet (a prediction, not the live function)")
    json.dump(cap, open(argv[1], "w", encoding="utf-8"), sort_keys=True, ensure_ascii=True)
    print("preread names %d injected %d" % (len(cap["keys"]), injected))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
