"""CA-h-1 AC3: the folder a live run writes holds no key, token or client address. Denominator printed; zero files is
not a pass. Prints H1-CENSUS files=<n> hits=<n> ok=<bool>."""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _h1_cli  # noqa: E402

PATTERNS = {
    "aws_key": re.compile(rb"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b"),
    "pem": re.compile(rb"-----BEGIN [A-Z ]*(?:KEY|CERTIFICATE)"),
    "bearer": re.compile(rb"(?i)bearer\s+[a-z0-9._~+/=-]{20,}"),
    "jwt": re.compile(rb"\beyJ[A-Za-z0-9_-]{15,}\.[A-Za-z0-9_-]{10,}"),
    "email": re.compile(rb"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+\.[A-Za-z0-9.-]+"),
    "secret_assign": re.compile(rb"(?i)(?:secret|token|password|passwd|api[_-]?key)[\"']?\s*[:=]\s*[\"']?[A-Za-z0-9/+_=.-]{8,}"),
}
td, rc, tail = _h1_cli.run()
if td is None:
    print("H1-CENSUS files=0 hits=NA ok=False reason=%s" % tail)
    sys.exit(0)
files = [p for p in pathlib.Path(td.name).rglob("*") if p.is_file()]
hits = []
for p in files:
    b = p.read_bytes()
    for k, rx in PATTERNS.items():
        for _ in rx.finditer(b):
            hits.append((p.name, k))
ok = bool(files) and not hits and rc == 0
print("H1-CENSUS files=%d hits=%d ok=%s patterns=%d%s" % (len(files), len(hits), ok, len(PATTERNS),
                                                         (" first=%r" % (hits[:3],)) if hits else ""))
