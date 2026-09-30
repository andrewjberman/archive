"""IRPT_DASHBD round 1 AC (DB-b-2, FWD-1 hop 2 / C-SEAM) -- the thread account's series and manifest exist at the builder's
addresses and carry every field the SERIES contract declares required, arrays of one length.

Usage: python p1_2_ac1_series_manifest.py <worktree root>
Reads org/standards/IRPT_DASHBD_SERIES_CONTRACT.json ({"series": {"required": [...], "optional": [...]}, "manifest": {"required": [...]}})
then GetObject series.json.gz (gunzip, JSON) and manifest.json for account 0027265115 via lib.opal_naming.address(). Every required
series key is present; every present array key has the same length as `date`; `date` is strictly increasing; the manifest carries
its required keys and a byte size for the series equal to the object's ContentLength. Prints gz size, inflated size and row count.
Pass line: DB-2-AC1 PASS. Base (at the cut): FAIL -- no SERIES contract and no objects.
"""
import gzip
import json
import sys
from pathlib import Path

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
sys.path.insert(0, str(root))
THREAD = "0027265115"


def fail(msg):
    print("DB-2-AC1 FAIL: " + msg)
    sys.exit(1)


cp = root / "org/standards/IRPT_DASHBD_SERIES_CONTRACT.json"
if not cp.exists():
    fail("SERIES contract absent: %s" % cp)
c = json.loads(cp.read_text(encoding="utf-8"))
req = c.get("series", {}).get("required") or []
mreq = c.get("manifest", {}).get("required") or []
if not req or not mreq:
    fail("SERIES contract declares no required series or manifest keys")
for must in ("date", "value", "total_return_daily", "return_basis", "day_quality", "external_flow", "income", "method_version", "as_of", "first_data_date", "drawdown_episodes"):
    if must not in req:
        fail("SERIES contract's required list lacks %s (C-SERVE / C-SEAM)" % must)

from lib import opal_naming as on  # noqa: E402
import boto3  # noqa: E402

s3 = boto3.client("s3", region_name="us-east-1")


def get(uri):
    b, k = uri[5:].split("/", 1)
    o = s3.get_object(Bucket=b, Key=k)
    return o["Body"].read(), o["ContentLength"]


try:
    raw, gz_len = get(on.address("irpt", "49financial", "platinum", "reporting", "account=%s" % THREAD, "series.json.gz"))
    mraw, _ = get(on.address("irpt", "49financial", "platinum", "reporting", "account=%s" % THREAD, "manifest.json"))
except Exception as exc:  # noqa: BLE001
    fail("objects unreadable: %s" % str(exc)[:160])
inflated = gzip.decompress(raw)
series = json.loads(inflated)
manifest = json.loads(mraw)
missing = [k for k in req if k not in series]
if missing:
    fail("series lacks required keys %s" % missing)
n = len(series["date"])
if n == 0:
    fail("series has 0 dates")
for k, v in series.items():
    if isinstance(v, list) and k not in ("drawdown_episodes",) and len(v) != n:
        fail("series array %s has %d entries, date has %d" % (k, len(v), n))
if any(series["date"][i] >= series["date"][i + 1] for i in range(n - 1)):
    fail("series dates are not strictly increasing")
mm = [k for k in mreq if k not in manifest]
if mm:
    fail("manifest lacks required keys %s" % mm)
sizes = manifest.get("byte_sizes") or {}
if int(sizes.get("series.json.gz", -1)) != int(gz_len):
    fail("manifest byte_sizes['series.json.gz'] %r != object ContentLength %d" % (sizes.get("series.json.gz"), gz_len))
print("  series: %d days, gz %d bytes, inflated %d bytes, first %s last %s, method_version %s, episodes %d" % (
    n, gz_len, len(inflated), series["date"][0], series["date"][-1], series.get("method_version"), len(series.get("drawdown_episodes") or [])))
print("DB-2-AC1 PASS")
