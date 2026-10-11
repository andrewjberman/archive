"""AMGT_CORPUS round 46, CRPS-av-4 leg p -- the whole-population post-act read. Issuer's file. READ-ONLY.

  PYTHONPATH=. python av4_population_read.py <pre capture.json> <post capture.json>

Both captures are av_capture.py's output over the LIVE function (pre: serving /11; post: after the redeploy). Per name, and over all names:
  stored   the live `model.team_sheet` equals the stored /12 dossier field (read now), whole
  others   every captured block other than `model.team_sheet` equals its pre-act value: the payload's fiscal_year_figures, fiscal_years,
           header_figures, check_face, posture, dossier_fields, model_status, status, and the `model` keys but team_sheet
  newkeys  the five keys row_classes, row_numbers, row_values, periods, row_counts are served
Every non-equal name and block is printed. Prints `av4pop stored <e>/<n> others_equal_vintage_masked <o>/<n> (unmasked <u>/<n>) newkeys <k>/<n>`, then the dossier-fed blocks unmasked.
A name still differing after the mask is a Bloomberg VALUE the daily pull moved, named, never hidden.
"""
import json
import sys

from lib.research.corpus import dossier
from lib.research.harvest import store

NEW = ("row_classes", "row_numbers", "row_values", "periods", "row_counts")
BLOCKS = ("status", "model_status", "fiscal_year_figures", "fiscal_years", "header_figures", "check_face", "posture", "dossier_fields")


def mask(v):
    """The Bloomberg `vintage` stamp is the daily pull's own mark (13:05Z); a capture taken before the pull differs from one taken after it
    in that stamp on every figure, so the comparison reads the figures with it removed AND the unmasked count is printed beside."""
    if isinstance(v, dict):
        return {k: mask(x) for k, x in v.items() if k != "vintage"}
    if isinstance(v, list):
        return [mask(x) for x in v]
    return v


def canon(v):
    return json.dumps(v, sort_keys=True, ensure_ascii=True)


def mcanon(v):
    return json.dumps(mask(v), sort_keys=True, ensure_ascii=True)


def main(argv):
    pre = json.load(open(argv[0], encoding="utf-8"))
    post = json.load(open(argv[1], encoding="utf-8"))
    client = store._default_client()
    dossier.METHOD_VERSION = "amgt-corpus-dossier/12"
    n = stored_eq = others_eq = newkeys = raw_equal = 0
    for key in sorted(post["keys"]):
        p, q = pre["keys"].get(key), post["keys"][key]
        n += 1
        ts = (q.get("model") or {}).get("team_sheet")
        doc = dossier.read_dossier(key, client=client)["document"]
        st = (doc.get("fields") or {}).get("team_sheet")
        if doc.get("method_version") == "amgt-corpus-dossier/12" and canon(ts) == canon(st):
            stored_eq += 1
        else:
            print("STORED-DIFFERS %s" % key)
        if isinstance(ts, dict) and all(k in ts for k in NEW):
            newkeys += 1
        else:
            print("NEWKEYS-MISSING %s" % key)
        bad = [b for b in BLOCKS if mcanon((p or {}).get(b)) != mcanon(q.get(b))]
        mp = {k: v for k, v in ((p or {}).get("model") or {}).items() if k != "team_sheet"}
        mq = {k: v for k, v in (q.get("model") or {}).items() if k != "team_sheet"}
        bad += ["model.%s" % k for k in sorted(set(mp) | set(mq)) if mcanon(mp.get(k)) != mcanon(mq.get(k))]
        raw_bad = [b for b in BLOCKS if canon((p or {}).get(b)) != canon(q.get(b))]
        raw_equal += int(not raw_bad and all(canon(mp.get(k)) == canon(mq.get(k)) for k in set(mp) | set(mq)))
        if bad:
            print("OTHERS-DIFFER-AFTER-VINTAGE-MASK %s %s" % (key, ",".join(bad)))
        else:
            others_eq += 1
    print("av4pop stored %d/%d others_equal_vintage_masked %d/%d (unmasked %d/%d) newkeys %d/%d" % (
        stored_eq, n, others_eq, n, raw_equal, n, newkeys, n))
    for b in ("dossier_fields", "posture"):
        e = sum(1 for k in post["keys"] if canon(pre["keys"].get(k, {}).get(b)) == canon(post["keys"][k].get(b)))
        print("av4pop dossier-fed block %s equal %d/%d (no mask)" % (b, e, n))
    return 0 if (stored_eq == n and others_eq == n and newkeys == n) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
