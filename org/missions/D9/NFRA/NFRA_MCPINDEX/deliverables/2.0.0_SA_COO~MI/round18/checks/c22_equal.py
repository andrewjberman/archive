"""c22_equal.py -- the difference control of MX-c-22 (etfs_get_positioning extension), from the repo root.

  python c22_equal.py probe <gateway root>     (internal) prints, as one JSON line, the answers of the tree at <gateway root> for the EXISTING inputs
  python c22_equal.py ac1                      runs the probe under the BASE tree (git ref BASE_REF, extracted) and under the NEW tree (infra/aws/ec2/opal-gateway, or
                                               C22_GW for a planted tree) and requires the two JSON lines byte-equal: the existing answer is unchanged for an existing input

The probe calls portal_index.answer('etfs_get_positioning', getter, principal, as_of=...) with a canned positioning object for the key the tree's own catalog resolves, for:
as_of empty, as_of equal to the object's date, as_of a different date (the no_data answer), and an internal principal and a firm principal (the gate's refusal text).
Exit 0 PASS, 1 FAIL, 9 no run."""
import json
import os
import subprocess
import sys
import tempfile

BASE_REF = "06cfb6db64"
GW = "infra/aws/ec2/opal-gateway"
NEWGW = os.environ.get("C22_GW") or GW
HERE = os.path.dirname(os.path.abspath(__file__))
OBJ_DATE = "2026-10-13"


def probe(root):
    root = os.path.abspath(root)
    sys.path.insert(0, root)
    os.chdir(root)
    os.environ.setdefault("MOCK_GRAPH", "1")
    from app.graphql_plumbing import catalog_gate
    from app.integrations.portal_index import integration as pi
    loaded = pi.runtime_catalog()
    canned = json.dumps({"data_as_of": OBJ_DATE, "as_of": OBJ_DATE, "funds": [{"ticker": "DIVZ", "aum": 1.0}, {"ticker": "IDVZ", "aum": 2.0}],
                         "_provenance": {"source_vintages": {}}}).encode("utf-8")
    seen = []

    def getter(bucket, key):
        seen.append([bucket, key])
        return canned

    out = {}
    for label, principal, as_of in (("internal-empty", (catalog_gate.OPAL_INTERNAL, ""), ""), ("internal-same-day", (catalog_gate.OPAL_INTERNAL, ""), OBJ_DATE),
                                    ("internal-other-day", (catalog_gate.OPAL_INTERNAL, ""), "2026-01-02"), ("firm", ("firm", "nosuchfirm"), "")):
        try:
            a = pi.answer("etfs_get_positioning", getter, principal, as_of=as_of, loaded=loaded)
        except Exception as exc:   # a refusal is an answer: its type and text are part of the contract
            a = {"raised": type(exc).__name__, "text": str(exc)}
        out[label] = a
    out["reads"] = seen
    print(json.dumps(out, sort_keys=True))


def run(root):
    r = subprocess.run([sys.executable, os.path.join(HERE, "c22_equal.py"), "probe", root], capture_output=True, text=True, timeout=200)
    lines = [ln for ln in (r.stdout or "").splitlines() if ln.startswith("{")]
    if r.returncode != 0 or not lines:
        print("ERROR: probe under %s rc %d: %s" % (root, r.returncode, (r.stderr or r.stdout)[-300:]))
        sys.exit(9)
    return lines[-1]


def ac1():
    d = tempfile.mkdtemp(prefix="c22_base_")
    p = subprocess.run("git archive %s %s | tar -x -C %s" % (BASE_REF, GW, d.replace("\\", "/")), shell=True, capture_output=True)
    if p.returncode != 0:
        print("ERROR: git archive %s failed: %s" % (BASE_REF, p.stderr[-200:]))
        return 9
    base, new = run(os.path.join(d, GW)), run(NEWGW)
    b, n = json.loads(base), json.loads(new)
    same = base == new
    print("DENOMINATOR cases %d (internal empty, same day, other day, firm); base reads %d, new reads %d" % (len(b) - 1, len(b["reads"]), len(n["reads"])))
    for k in sorted(b):
        print("CHECK %s: %s" % ("ok  " if b[k] == n.get(k) else "FAIL", k))
    print("RESULT: %s" % ("PASS" if same else "FAIL"))
    return 0 if same else 1


def main():
    if len(sys.argv) >= 3 and sys.argv[1] == "probe":
        probe(sys.argv[2])
        return 0
    if len(sys.argv) >= 2 and sys.argv[1] == "ac1":
        return ac1()
    print(__doc__)
    return 9


if __name__ == "__main__":
    sys.exit(main())
