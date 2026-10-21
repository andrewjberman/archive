"""IRPT_ANLREQ round 60 (issuer 2.0.0_SA_COO~G2): the one read of row S222 on the CURRENT code (CTO msg 11961). READ ONLY, offline, no AWS.
Needs a python with jsonschema and referencing (not `-I`).

    python s222_replay.py <resident tarball>

S222: on the r34l resident a request filed with `commentary_requested` OMITTED passed the composition step and was then retained for retry with
`RecipeRefused code=-` (run 5C). This replays run 7J's retained synthetic composition (fixtures/composition_7i_synthetic.json is 7I's, the same
shape) through the tarball's OWN modules in a fresh interpreter, twice: as filed (with the field) and with the field REMOVED from the browser body
(and the binding digests recomputed over the changed body so the stubs stay self-consistent), through (1) CompositionAdmission.validate and (2) the
frozen worker's `prepare(upload=False)` over the checker stubs (ar_prepare_checks.stub_worker). It prints one closed line per step and case:
S222 <case> admission=<..> prepare_opal=<..> prepare_vendor_default=<..> (the vendor default is `prepare()` with its upload built). ASCII only.
"""
import os
import subprocess
import sys
import tarfile
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
FIXTURE = os.path.join(HERE, "fixtures", "composition_7i_synthetic.json")

CODE = r'''
import sys, json, copy
base = sys.argv[1]
fixture = sys.argv[2]
here = sys.argv[3]
sys.path[:0] = [base + '/ycharts/generate', base + '/ops', base + '/reports', base + '/intake', base + '/_scope', base + '/_ids', base + '/_keys',
                base + '/_authz', base + '/ycharts/research', base + '/ycharts/session', base + '/ycharts/extract', base + '/lib', base, here]
import submission
import composition_admission as ca
import ar_prepare_checks as ap
doc0 = json.load(open(fixture, encoding='utf-8'))


def first_words(exc):
    return ' '.join(str(exc).replace('\n', ' ').split()[:6])[:60]


def run(tag, doc):
    adm_res, prep_res = 'OK', 'OK'
    try:
        ca.CompositionAdmission(base + '/docs/contracts/investor-reporting/v1').validate(doc)
    except Exception as e:
        adm_res = 'REFUSED:%s:%s' % (type(e).__name__, first_words(e))
    try:
        worker, principal, request_id = ap.stub_worker(doc, submission)
        out = worker.prepare(principal, request_id, upload=False)
        if out.get('upload') is not None:
            prep_res = 'REFUSED:UploadNotNone'
    except Exception as e:
        prep_res = 'REFUSED:%s:%s' % (type(e).__name__, first_words(e))
    dflt = 'OK'
    try:
        worker, principal, request_id = ap.stub_worker(doc, submission)
        worker.prepare(principal, request_id)
    except Exception as e:
        dflt = 'REFUSED:%s:%s' % (type(e).__name__, first_words(e))
    print('S222 %s admission=%s prepare_opal=%s prepare_vendor_default=%s' % (tag, adm_res, prep_res, dflt))


run('field_present', copy.deepcopy(doc0))
doc1 = copy.deepcopy(doc0)
had = 'commentary_requested' in doc1['browser']
doc1['browser'].pop('commentary_requested', None)
print('S222 browser_had_field=%s' % had)
run('field_omitted', doc1)
'''


def main():
    if len(sys.argv) < 2:
        print("usage: s222_replay.py <resident tarball>")
        sys.exit(2)
    with tempfile.TemporaryDirectory() as tmp:
        with tarfile.open(sys.argv[1]) as tf:
            tf.extractall(tmp)
        r = subprocess.run([sys.executable, "-B", "-c", CODE, tmp, FIXTURE, HERE], capture_output=True, text=True, cwd=tmp)
    out = [ln for ln in r.stdout.splitlines() if ln.startswith("S222")]
    if not out:
        print("S222 NO-OUTPUT rc=%d %s" % (r.returncode, (r.stderr.strip().splitlines() or ["?"])[-1][:200]))
        sys.exit(1)
    print("\n".join(out))


if __name__ == "__main__":
    main()
