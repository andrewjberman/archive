"""IRPT_ANLREQ round 60 (issuer 2.0.0_SA_COO~G2): the admission replay of a Multi-Comp composition through a PACKAGED resident tree.
READ ONLY, offline. Run with a python that has jsonschema and referencing (not `-I`).

    python ar_admission_replay.py <resident tarball> [--trunk-submission]

Why: run 7H (a Multi-Comp filing on the r34p resident) was refused at the resident's replay of the frozen composition:
`COMPOSITION-REFUSED step=3 error_class=SubmissionRefused` -> CLOSED_COMPOSITION_REQUIRED. The cause (measured by this file's author on the
request-composition object that run left behind): the packaged `ycharts/generate/submission.py` (the base pin's, 2026-10-16) does not list
`commentary_requested` in PUBLIC_FIELDS, so its validate_public_request refuses a browser body that carries it
(UNKNOWN_OR_SERVER_OWNED_FIELD), while the packaged request schema and the accepting side know the field. The fixture is that run's own
composition (SYNTHETIC: a minted staff user, four public ETF tickers, no client data).
The replay runs the five steps of CompositionAdmission.validate with the tarball's own modules in a fresh interpreter. Prints one line:
AR-ADMIT-OK (all five steps pass) or AR-ADMIT-FAIL step=<n> <code>. With --trunk-submission the tree's submission.py is replaced by the
repository's HEAD copy first (the self-test: the failing tree must pass with the fixed module). ASCII only.
"""
import os
import re
import subprocess
import sys
import tarfile
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
FIXTURE = os.path.join(HERE, "fixtures", "composition_7h_synthetic.json")
SUB = "infra/aws/lambda/investor-reporting/ycharts/generate/submission.py"


def main():
    if len(sys.argv) < 2:
        print("usage: ar_admission_replay.py <resident tarball> [--trunk-submission]")
        sys.exit(2)
    tar, trunk = sys.argv[1], "--trunk-submission" in sys.argv[2:]
    with tempfile.TemporaryDirectory() as tmp:
        with tarfile.open(tar) as tf:
            tf.extractall(tmp)
        if trunk:
            data = subprocess.run(["git", "show", "HEAD:" + SUB], capture_output=True, check=True).stdout
            with open(tmp + "/ycharts/generate/submission.py", "wb") as fh:
                fh.write(data)
        code = (
            "import sys, json\n"
            "base = %r\n"
            "sys.path[:0] = [base + '/ycharts/generate', base + '/reports', base + '/intake', base + '/_scope', base + '/_ids',\n"
            "                base + '/_keys', base + '/_authz', base + '/lib', base]\n"
            "import composition_admission as ca\n"
            "doc = json.load(open(%r, encoding='utf-8'))\n"
            "adm = ca.CompositionAdmission(base + '/docs/contracts/investor-reporting/v1')\n"
            "try:\n"
            "    adm.validate(doc)\n"
            "    print('AR-ADMIT-OK')\n"
            "except Exception as e:\n"
            "    print('AR-ADMIT-EXC', type(e).__name__, str(e))\n" % (tmp, FIXTURE))
        r = subprocess.run([sys.executable, "-B", "-c", code], capture_output=True, text=True, cwd=tmp)
    out = r.stdout
    if "AR-ADMIT-OK" in out:
        print("AR-ADMIT-OK")
        return 0
    m = re.search(r"COMPOSITION-REFUSED step=(\d+) error_class=(\w+)", out)
    tail = (out.strip().splitlines() or [r.stderr.strip()[-160:] or "?"])[-1][:160]
    print("AR-ADMIT-FAIL step=%s %s" % (m.group(1) if m else "?", tail))
    return 1


if __name__ == "__main__":
    sys.exit(main())
