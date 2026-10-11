"""AMGT_CORPUS round 46, CRPS-av-10 PRE-READ -- what the rendered census WILL read once the API serves /12. Issuer's file. READ-ONLY.

  PYTHONPATH=. python av10_preread_inject.py <live capture.json> <out.json>

Takes av_capture.py's output over the LIVE function (serving /11) and replaces each name's `model.team_sheet` with the STORED /12 dossier field
(`read_dossier` at METHOD /12 -- exactly what `_team_sheet_from_dossier` will return once the redeployed API picks the /12 objects). The result is
fed to av10_rendered_census.cjs as a prediction; the real read is taken on the live function after the redeploy. Prints `preread names <n> injected <k>`.
"""
import json
import sys

from lib.research.corpus import dossier
from lib.research.harvest import store


def main(argv):
    cap = json.load(open(argv[0], encoding="utf-8"))
    client = store._default_client()
    dossier.METHOD_VERSION = "amgt-corpus-dossier/12"
    injected = 0
    for key, rec in cap["keys"].items():
        doc = dossier.read_dossier(key, client=client)["document"]
        if doc.get("method_version") != "amgt-corpus-dossier/12":
            continue
        rec["model"]["team_sheet"] = (doc.get("fields") or {}).get("team_sheet")
        injected += 1
    cap["function"] = dict(cap["function"], injected="stored /12 team_sheet (a prediction, not the live function)")
    json.dump(cap, open(argv[1], "w", encoding="utf-8"), sort_keys=True, ensure_ascii=True)
    print("preread names %d injected %d" % (len(cap["keys"]), injected))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
