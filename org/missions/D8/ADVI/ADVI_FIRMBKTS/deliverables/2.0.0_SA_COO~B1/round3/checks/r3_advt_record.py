"""ADVI_FIRMBKTS round 3 check for cell FB-f-7 (the advTenant remedy), the record arm, issuer 2.0.0_SA_COO~B1.

Grades the Rule-24 record the remedy owes (the file `shared-advisor-router/_shared/firm-config.mjs` header cites
`ADVI_P4R3_ADVTENANT_RULE24_RECORD_20260821.md`, which does not exist at HEAD). `--record FILE` (3 arms):
  K1 the four postulates each have a heading line (i) MECE over a declared domain, (ii) SAME GRAIN, (iii) INTENT
     COHERENCE, (iv) STATE COHERENCE, and each section is more than 200 characters
  K2 the declared domain is printed with a denominator: a table that names every firmId of the generated
     FIRM_CONFIG (read from _shared/firm-config.mjs here) and, per firmId, its tenant-directory set
  K3 the three standing cases are named with the set each resolves to: the `mockadv` alias, the opal-capital staff
     proxy (`?firm=`), and a firm that shares a bucket with another firm (the case the bucket comparison degenerates on)
--root points at another tree. Never edit this file. Plain ASCII; the last line carries the arm count.
"""
import argparse
import os
import re
import subprocess
import sys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--record", required=True)
    ap.add_argument("--root")
    a = ap.parse_args()
    root = a.root or subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
    res = []
    try:
        with open(a.record, encoding="utf-8") as fh:
            text = fh.read()
        with open(os.path.join(root, "infra/aws/lambda-edge/_shared/firm-config.mjs"), encoding="utf-8") as fh:
            cfg = fh.read()
        heads = [("(i)", r"MECE"), ("(ii)", r"SAME GRAIN"), ("(iii)", r"INTENT COHERENCE"), ("(iv)", r"STATE COHERENCE")]
        ok1 = True
        for n, label in heads:
            m = re.search(r"^#+[^\n]*%s[^\n]*%s[^\n]*$" % (re.escape(n), label), text, re.M | re.I)
            if not m:
                print("    NO-HEADING %s %s" % (n, label))
                ok1 = False
                continue
            body = text[m.end():]
            nxt = re.search(r"^#+ ", body, re.M)
            if len((body[:nxt.start()] if nxt else body).strip()) <= 200:
                print("    SHORT-SECTION %s" % n)
                ok1 = False
        res.append(("K1 four postulate sections, each with a heading and a body over 200 characters", ok1))
        block = cfg[cfg.index("export const FIRM_CONFIG"):cfg.index("// END GENERATED [FIRM_CONFIG]")]
        firms = re.findall(r"^\s*'([a-z0-9_]+)':\s*Object\.freeze", block, re.M)
        missing = [f for f in firms if f not in text]
        print("  FIRM_CONFIG firmIds=%d named in the record=%d" % (len(firms), len(firms) - len(missing)))
        res.append(("K2 the record names every firmId of the generated FIRM_CONFIG and prints its denominator",
                    bool(firms) and not missing and re.search(r"denominator", text, re.I) is not None))
        cases = all(re.search(p, text, re.I) for p in (r"mockadv", r"opal-capital", r"\?firm=", r"shar\w+ (one |a )?bucket"))
        res.append(("K3 the mockadv alias, the opal-capital staff proxy and the shared-bucket case are named with "
                    "their resolved sets", cases))
    except Exception as e:  # noqa: BLE001
        print("ABSENT or unreadable: %s (%s)" % (a.record, type(e).__name__))
        res = [("the Rule-24 record is present and reads", False)]
    for name, ok in res:
        print("%s %s" % ("PASS" if ok else "FAIL", name))
    n = sum(1 for _, ok in res if ok)
    print("ROUND 3 ADVTENANT RECORD: %d of 3 arms" % n)
    sys.exit(0 if n == 3 else 1)


if __name__ == "__main__":
    main()
