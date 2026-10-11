"""AMGT_CORPUS round 46, CRPS-av-7 -- FWD-15's two missing reads (PRD:485-487). Issuer's file. READ-ONLY (S3 reads of the stored
posture objects; the live capture is av_capture.py's output).

  PYTHONPATH=. python av7_posture_reads.py <capture.json>

DONE WHEN: both (the fund of record and the last stated position) render cited on the header posture line and the Posture tab, and the
machine verdict is byte-unchanged by their presence.
  verdict  per name, the served `posture.verdict` and `posture.as_of` equal the STORED posture object's (`posture/v1/<key>/<as_of>.json`,
           read now through scoped_amgt.read_pool_object): the verdict the page serves is the machine's, with the dossier citations
           present beside it. A name with no stored object and a live block that is not SERVED reads "absent both".
           Prints `av7 verdict equal <e>, absent both live and stored <a>, of <n>`.
  cited    over the names, how many serve a `dossier_fields.fund_of_record` and a `last_stated_position` that carry a citation (a
           report key and a passage), and how many serve neither. Prints `av7 cited fund <a> position <b> of <n>`.
"""
import json
import sys

from lib.research.api import scoped_amgt


def has_cite(block):
    cite = block.get("citation") if isinstance(block, dict) else None
    return bool(isinstance(cite, dict) and cite.get("report_key") and cite.get("passage"))


def main(argv):
    cap = json.load(open(argv[0], encoding="utf-8"))
    keys = sorted(cap["keys"])
    equal = 0
    both_absent = 0
    unequal = []
    unread = []
    fund = pos = 0
    for key in keys:
        rec = cap["keys"][key]
        post = rec.get("posture") or {}
        df = rec.get("dossier_fields") or {}
        fund += 1 if has_cite(df.get("fund_of_record")) else 0
        pos += 1 if has_cite(df.get("last_stated_position")) else 0
        doc, record = scoped_amgt.read_pool_object(scoped_amgt.POSTURE_PREFIX, key, as_of=post.get("as_of"))
        if not isinstance(doc, dict):
            # no stored object: consistent when the live block is itself not SERVED; otherwise a read failure to be named
            if str(post.get("status")) != "SERVED" and (record or {}).get("status") == "ABSENT":
                both_absent += 1
            else:
                unread.append("%s:%s/%s" % (key, (record or {}).get("status"), post.get("status")))
            continue
        if str(doc.get("verdict")) == str(post.get("verdict")) and str(doc.get("as_of")) == str(post.get("as_of")):
            equal += 1
        else:
            unequal.append(key)
    print("capture function CodeSha256 %s LastModified %s" % (cap["function"]["CodeSha256"], cap["function"]["LastModified"]))
    print("av7 verdict equal %d, absent both live and stored %d, of %d%s%s" % (equal, both_absent, len(keys),
          (" UNEQUAL " + ",".join(unequal[:6])) if unequal else "",
          (" UNREAD %d: %s" % (len(unread), ",".join(unread[:6]))) if unread else ""))
    print("av7 cited fund %d position %d of %d" % (fund, pos, len(keys)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
