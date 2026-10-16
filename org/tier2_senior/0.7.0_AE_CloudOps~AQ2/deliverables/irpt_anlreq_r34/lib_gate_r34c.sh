set -u
# IRPT_ANLREQ TO-APPLY-R34C step 1 (READ ONLY): the library gate. Through the resident's interpreter with pydeps APPENDED to the import path (as the resident does), import yfinance, pandas, numpy and requests; print versions and where they came from. No network, no write.
PY=/usr/bin/python3.12
PYD=/opt/investor-reporting-ycharts/pydeps
$PY - "$PYD" <<'PYEOF'
import sys
pyd = sys.argv[1]
sys.path.append(pyd)
bad = 0
for name in ("yfinance", "pandas", "numpy", "requests"):
    try:
        m = __import__(name)
        print("GATE IMPORT OK %s %s under_pydeps=%s" % (name, getattr(m, "__version__", "?"), str(getattr(m, "__file__", "")).startswith(pyd)))
    except Exception as e:
        bad += 1
        print("GATE IMPORT FAIL %s %s" % (name, type(e).__name__))
print("GATE RESULT %s" % ("OK" if not bad else "FAIL"))
PYEOF
