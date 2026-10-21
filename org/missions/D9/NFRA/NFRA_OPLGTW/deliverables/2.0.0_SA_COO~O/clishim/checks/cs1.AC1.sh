#!/usr/bin/env bash
# OPLGTW OG-cs-1 AC1 (cli-shim workstream, wave 1): the folder-grant decision, a pure function. app/folder_grant.py, in one fresh process (no AWS, no network):
#   folder_decision(is_master_admin, is_opal, rec, bucket, key) -> (allowed: bool, reason: str); SERVED_BUCKETS = ("opal-data-assets", "opal-data-etfs", "opal-data-portal-v2");
#   rec is a data_entitlement.PersonAccess or None. A "folder entry" is a channels_allow or channels_deny string naming a bucket or bucket/prefix.
# Eleven arms; every one must hold: master_admin with no record reads a served bucket; an unserved bucket (opal-data-harvest) is refused; bronze and raw paths are refused under EVERY grant (the CVO's v3.18 refusal);
# an Opal non-admin reads only inside an allowed folder; a prefix matches only at a path boundary; deny wins; a stopped or revoked record grants nothing; a non-Opal caller is refused; '..' and a leading '/' are refused.
. "$(dirname "$0")/../../r47/checks/_gwtests.sh"
res=$(python3 -I - "$(native "$GW")" <<'PYEOF'
import os, sys
G = sys.argv[1]
sys.path.insert(0, G)
os.environ["MOCK_GRAPH"] = "1"
import warnings
warnings.simplefilter("ignore")
ok = True


def say(label, cond):
    global ok
    ok = ok and bool(cond)
    print("%s: %s" % (label, "ok" if cond else "NOT OK"))


try:
    from app import data_entitlement as de, folder_grant as fg
except Exception as exc:  # noqa: BLE001
    print("import failed: %s: %s" % (type(exc).__name__, str(exc)[:80]))
    print("NO")
    sys.exit(0)


def rec(allow=(), deny=(), status="active", stopped=False):
    return de.PersonAccess(status, 3, stopped, frozenset(), frozenset(), frozenset(allow), frozenset(deny))


def d(admin, opal, r, bucket, key):
    try:
        res = fg.folder_decision(admin, opal, r, bucket, key)
        return bool(res[0]), str(res[1])
    except Exception as exc:  # noqa: BLE001
        return None, "%s: %s" % (type(exc).__name__, str(exc)[:60])


A, E, P, H = "opal-data-assets", "opal-data-etfs", "opal-data-portal-v2", "opal-data-harvest"
K = "schwab/08335338/silver/fact_trn/date=2026-10-20/x.parquet"
say("SERVED_BUCKETS is exactly the three buckets", tuple(getattr(fg, "SERVED_BUCKETS", ())) == (A, E, P))
say("master_admin with no record reads a served bucket", d(True, True, None, A, K)[0] is True)
say("an unserved bucket is refused for master_admin too (reason names the bucket)", d(True, True, None, H, "amgt/x")[0] is False and H in d(True, True, None, H, "amgt/x")[1])
say("bronze and raw paths are refused for master_admin and under a whole-bucket grant", all(d(a, True, rec(allow=[A]) if not a else None, A, k)[0] is False for a in (True, False) for k in ("schwab/08335338/bronze/a/b.csv", "raw/x/y.json", "orion/inflection/bronze/t")))
say("an Opal non-admin with allow [bucket] reads that bucket and not another", d(False, True, rec(allow=[E]), E, "funds/x.parquet")[0] is True and d(False, True, rec(allow=[E]), A, K)[0] is False)
r2 = rec(allow=["opal-data-assets/schwab/08335338/"])
say("a prefix grant matches inside the folder and not a sibling or a longer name", d(False, True, r2, A, K)[0] is True and d(False, True, r2, A, "schwab/08242234/silver/x")[0] is False and d(False, True, r2, A, "schwab/08335338x/silver/x")[0] is False)
r3 = rec(allow=[A], deny=["opal-data-assets/schwab/08403355/"])
say("deny wins over allow", d(False, True, r3, A, "schwab/08403355/silver/x")[0] is False and d(False, True, r3, A, K)[0] is True)
say("a stopped or revoked record grants nothing; no record grants nothing", d(False, True, rec(allow=[A], stopped=True), A, K)[0] is False and d(False, True, rec(allow=[A], status="revoked"), A, K)[0] is False and d(False, True, None, A, K)[0] is False)
say("a non-Opal caller is refused even with an allow", d(False, False, rec(allow=[A]), A, K)[0] is False)
say("'..' in the key and a leading '/' are refused", d(True, True, None, A, "schwab/../x")[0] is False and d(True, True, None, A, "/schwab/x")[0] is False)
say("a refusal carries a reason a person can act on (non-empty text)", all(len(d(False, True, None, A, K)[1]) >= 10 for _ in (0,)))
print("OK" if ok else "NO")
PYEOF
)
res=$(printf '%s' "$res" | tr -d '\r'); printf '%s\n' "$res" | sed '$d'
restore_audit
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
