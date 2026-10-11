"""IB-pr-426 replay: the CARRIED METHOD-CALL SITES of AMENDMENT 1, exercised one by one through ONE extracted tree. Run as
    python -I sites426.py <extracted_zip_dir> <label> <out_json>
The static method limb reads four name-based mismatches on the live package and the same four on the build. This probe CALLS each site
with in-memory fakes and records that the call was reached (sys.monitoring LINE events on the exact source line), the positional and
keyword arguments the callee was handed, and what came back. The callee is a FAKE shaped like the object the source injects there
(named in each detail); the injected object itself is not in this package, so what is observed is the call shape, not that object.
  publication.py   `_naming().lookup(firm)`          -> the REAL opal_naming.lookup (module function, in the package)
  publisher.py     `self.reports.validate("ANALYSIS", report)` twice (opal path, vendor path) -> a fake `reports` with validate(kind, payload)
  resident_worker  `self.transport.renew(ttl=900)`   -> the REAL broker._RecoveryObserver (in the package) over a fake transport with renew(*, ttl)
Offline: sockets refused, no AWS client. Synthetic ids and bytes only. ASCII only."""
import hashlib
import json
import os
import socket
import sys

zip_dir, label, out_path = sys.argv[1:4]
sys.dont_write_bytecode = True
sys.path.insert(0, zip_dir)
os.environ.update({"AWS_ACCESS_KEY_ID": "fake", "AWS_SECRET_ACCESS_KEY": "fake", "AWS_DEFAULT_REGION": "us-east-1"})


def _refuse(self, *a, **k):
    raise OSError("OFFLINE-GUARD")


socket.socket.connect = _refuse
_real_gai = socket.getaddrinfo
socket.getaddrinfo = lambda host, *a, **k: _real_gai(host, *a, **k) if host in (None, "localhost", "127.0.0.1", "::1", "") else (_ for _ in ()).throw(OSError("OFFLINE-GUARD"))

import linecache  # noqa: E402

mon = sys.monitoring
TOOL = mon.PROFILER_ID
mon.use_tool_id(TOOL, "sites426")
WANT = {("publication.py", "own = _naming().lookup(firm)"): 0, ("publisher.py", 'self.reports.validate("ANALYSIS", report)'): 0,
        ("resident_worker.py", "self.transport.renew(ttl=900)"): 0}
LINES = {}


def on_line(code, line):
    fn = os.path.basename(code.co_filename)
    if not any(k[0] == fn for k in WANT):
        return mon.DISABLE
    text = linecache.getline(code.co_filename, line)
    for k in WANT:
        if k[0] == fn and k[1] in text:
            WANT[k] += 1
            LINES.setdefault(k, set()).add(line)
            return None
    return mon.DISABLE


mon.register_callback(TOOL, mon.events.LINE, on_line)
mon.set_events(TOOL, mon.events.LINE)

import publication  # noqa: E402
import publisher  # noqa: E402
import repository  # noqa: E402
import resident_worker  # noqa: E402
from broker import _RecoveryObserver  # noqa: E402

out = {"label": label}

# ---- 1. publication: the REAL opal_naming.lookup, one positional argument
res = {}
for firm in ("cottonwood", "not-a-firm"):
    try:
        publication.foreign_firm_names(b"%PDF-1.4 synthetic", firm)
        res[firm] = "returned"
    except BaseException as exc:  # noqa: BLE001
        res[firm] = type(exc).__name__ + (":" + str(exc)[:40] if firm == "not-a-firm" else "")
out["publication_lookup"] = {"outcomes": res, "line_hits": WANT[("publication.py", "own = _naming().lookup(firm)")],
                             "lookup_signature": str(__import__("inspect").signature(publication._naming().lookup))}

# ---- 2. publisher: a fake `reports` whose validate takes (kind, payload) as repository.ReportRepository.validate does
FIRM, PRINCIPAL_ID = "49financial", "synthetic-principal"
RID = "REQ-" + "ab" * 12
OWNER = {"firm_id": FIRM, "principal_id": PRINCIPAL_ID, "advisor_id": PRINCIPAL_ID, "ownership_fingerprint": "b" * 64}
principal = {"firm_id": FIRM, "principal_id": PRINCIPAL_ID, "principal_class": "FIRM_USER"}
DATA = b"synthetic-pdf-bytes"
SHA = hashlib.sha256(DATA).hexdigest()
PDF_REF = {"artifact_id": "ART-" + "c" * 64, "family": None, "content_type": "application/pdf", "immutable": True,
           "retention_ref": {"id": "ret-pdf"}, "sha256": SHA, "byte_length": len(DATA)}
RECORD = {"identity": {"request_id": RID, "revision": 1}, "owner": OWNER, "composition_ref": {"sha256": "d" * 64, "artifact_id": "ART-x", "retention_ref": {"id": "ret-comp"}}}
REQUEST_REF = {"request_id": RID, "request_revision": 1}
REPORT_ID = repository._report_identity(OWNER, "ANALYSIS", REQUEST_REF)


class Rec:
    def __init__(self):
        self.calls = []


class FakeReports(Rec):
    """validate(kind, payload) is an INSTANCE ATTRIBUTE, as ReportRepository sets it (repository.py `self.validate = validate`)."""

    def __init__(self):
        super().__init__()
        self.index = type("I", (), {"report_id": REPORT_ID})()
        self.report = None

        def validate(kind, payload):
            self.calls.append(("validate", kind, type(payload).__name__))
            return True
        self.validate = validate

    def persist(self, *a, **k):
        self.report = a[4]
        return {"report_id": REPORT_ID, "revision": "r" * 64}

    def get(self, *a, **k):
        return {"ref": {"report_id": REPORT_ID, "revision": "r" * 64}, "report": self.report}


class FakeArtifacts:
    def __init__(self, ref):
        self.ref = ref
        self.retention = type("R", (), {"require_live": lambda *a, **k: {}})()
        self.index = type("I", (), {"get": lambda s, firm, key: {"owner": OWNER, "ref": ref}})()

    def get(self, principal_, artifact_id, **k):
        return {"data": DATA, "ref": self.ref}


def make_publisher(ref):
    pub = object.__new__(publisher.CertifiedReportPublisher)
    pub.reports = FakeReports()
    pub.requests = type("Q", (), {"artifacts": FakeArtifacts(ref),
                                  "acceptance": type("A", (), {"get": lambda s, firm, rid: RECORD})(),
                                  "_materialize": lambda *a, **k: None, "_final": lambda *a, **k: None})()
    pub.store = type("S", (), {"tenant": FIRM, "request_id": RID, "composition_sha256": "d" * 64, "assert_current": lambda s: None})()
    pub._guard = lambda *a, **k: None
    pub._promote_sources = lambda *a, **k: None
    pub._chosen_comparisons = lambda *a, **k: []
    return pub


publisher.foreign_firm_names = lambda data, firm: []                    # the PDF-text backend (PyMuPDF) is not on this box
publisher.build_publication = lambda *a, **k: {"fragment": {}}          # certification of a real PDF is out of scope here
pub_out = {}
# opal path
ref = dict(PDF_REF, family="YCHARTS_OPAL_REPORT")
pub = make_publisher(ref)
meta = {"provider": "OPAL_ENGINE", "request_ref": REQUEST_REF, "opal_artifact": {"sha256": SHA, "byte_length": len(DATA)},
        "effective_inputs": {}, "sections": [], "disclosures": [], "computation_validation": {}, "release": {}}
try:
    r = pub.publish(principal, RID, pdf_ref=ref, census={}, metadata=meta)
    pub_out["opal_path"] = {"outcome": "returned", "keys": sorted(r)}
except BaseException as exc:  # noqa: BLE001
    pub_out["opal_path"] = {"outcome": type(exc).__name__ + ":" + str(exc)[:50]}
pub_out["opal_path"]["validate_calls"] = list(pub.reports.calls)
# vendor path
ref2 = dict(PDF_REF, family="ORIGINAL_VENDOR_PDF")
pub2 = make_publisher(ref2)
meta2 = {"request_ref": REQUEST_REF, "vendor_artifact": {"sha256": SHA, "byte_length": len(DATA)}, "effective_inputs": {}, "release": {}}
try:
    r = pub2.publish(principal, RID, pdf_ref=ref2, census={}, metadata=meta2)
    pub_out["vendor_path"] = {"outcome": "returned", "keys": sorted(r)}
except BaseException as exc:  # noqa: BLE001
    pub_out["vendor_path"] = {"outcome": type(exc).__name__ + ":" + str(exc)[:50]}
pub_out["vendor_path"]["validate_calls"] = list(pub2.reports.calls)
pub_out["line_hits"] = WANT[("publisher.py", 'self.reports.validate("ANALYSIS", report)')]
pub_out["lines_reached"] = sorted(LINES.get(("publisher.py", 'self.reports.validate("ANALYSIS", report)'), []))
out["publisher_validate"] = pub_out


# ---- 3. resident_worker: guard() -> self.transport.renew(ttl=900) through the REAL broker._RecoveryObserver
class FakeTransport:
    """shaped like ycharts/session/operation_lease.py renew(self, *, ttl); not part of this package."""

    def __init__(self):
        self.renewed = []

    def renew(self, *, ttl):
        self.renewed.append(ttl)


class FakeStore:
    tenant, request_id, composition_sha256 = FIRM, RID, "d" * 64

    def __init__(self):
        self.renews = 0

    def renew(self):
        self.renews += 1

    def assert_current(self):
        pass


worker = object.__new__(resident_worker.ResidentGenerationWorker)
inner = FakeTransport()
worker.transport = _RecoveryObserver(inner)
worker.store = FakeStore()
worker.resolve_principal = lambda: principal
worker.heartbeat = lambda: None
worker.requests = type("Q", (), {"acceptance": type("A", (), {"get": lambda s, firm, rid: RECORD})(),
                                 "_materialize": lambda *a, **k: None, "_final": lambda *a, **k: None})()
try:
    got = worker.guard()
    rw = {"outcome": "returned", "store_renews": worker.store.renews, "transport_renewed_with_ttl": inner.renewed}
except BaseException as exc:  # noqa: BLE001
    rw = {"outcome": type(exc).__name__ + ":" + str(exc)[:60], "transport_renewed_with_ttl": inner.renewed}
rw["line_hits"] = WANT[("resident_worker.py", "self.transport.renew(ttl=900)")]
out["resident_renew"] = rw
json.dump(out, open(out_path, "w", encoding="utf-8"), indent=1, sort_keys=True)
print("OK: %s lookup_hits=%d validate_hits=%d renew_hits=%d" % (label, out["publication_lookup"]["line_hits"], pub_out["line_hits"], rw["line_hits"]))
