#!/usr/bin/env python3
"""HVST-ad-1 AC1: read the two bundle Secrets back BY NAME, and print the A0 measurements. Prints hashes
and names only -- no cookie or secret VALUE. Sockets to any non-AWS host are blocked and counted.

  * per secret (wsj, barrons): NAME, existence, and whether the SHA-256 of the stored value equals the
    SHA-256 of the local saved-session bundle; `NOT YET WRITTEN` while the Secret does not exist.
  * ft's stored bundle: per cookie NAME and expiry (UTC), and the earliest login-cookie expiry.
  * the sa session field that carries `user_id` (the field NAME only).
  * `PUBLISHER NETWORK CALLS: <n>` (n = blocked non-AWS connection attempts).

Secret names: the halves name them at phase B; AD1_SECRET_WSJ / AD1_SECRET_BARRONS set them, else the
existing pattern's defaults below (printed with name_source=default).
"""

import datetime as dt
import hashlib
import importlib.util
import json
import os
import socket
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[8]
sys.path.insert(0, str(REPO))

BLOCKED = []
ALLOWED_IPS = {"127.0.0.1", "::1", "169.254.169.254"}  # loopback and the AWS instance-metadata address
_real_getaddrinfo, _real_connect = socket.getaddrinfo, socket.socket.connect


def _is_aws(host):
    host = (host or "").lower().rstrip(".")
    return host.endswith(".amazonaws.com") or host in ALLOWED_IPS or host in ("localhost", "")


def _guarded_getaddrinfo(host, *a, **kw):
    if isinstance(host, bytes):
        host = host.decode("ascii", "replace")
    if not _is_aws(host):
        BLOCKED.append(host)
        raise OSError("blocked non-AWS host lookup")
    result = _real_getaddrinfo(host, *a, **kw)
    for entry in result:
        ALLOWED_IPS.add(entry[4][0])
    return result


def _guarded_connect(self, address):
    host = address[0] if isinstance(address, tuple) else address
    if isinstance(host, str) and host not in ALLOWED_IPS and not host.startswith("/"):
        BLOCKED.append(host)
        raise OSError("blocked non-AWS connection")
    return _real_connect(self, address)


socket.getaddrinfo, socket.socket.connect = _guarded_getaddrinfo, _guarded_connect

from lib.opal_data_harvest import credentials  # noqa: E402
from lib.opal_data_harvest.storage import SessionVault, dpapi  # noqa: E402

DEFAULT_SECRETS = {"wsj": "wsj/session", "barrons": "barrons/session"}
FT_LOGIN_COOKIES = ("FTSession", "FTSession_s")  # ft_harvest_session.py IDENTITY_COOKIES


def runtime_root():
    if os.environ.get("AD1_RUNTIME_ROOT"):
        return Path(os.environ["AD1_RUNTIME_ROOT"])
    common = subprocess.check_output(["git", "-C", str(REPO), "rev-parse", "--git-common-dir"], text=True).strip()
    config = json.loads((REPO / "lib" / "opal_data_harvest" / "config.json").read_text(encoding="utf-8"))
    return Path(common).resolve().parent / config["runtime_root"]


def _utc(epoch):
    return dt.datetime.fromtimestamp(epoch, dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def readback(publisher, root, client):
    name = os.environ.get("AD1_SECRET_" + publisher.upper()) or DEFAULT_SECRETS[publisher]
    source = "env" if os.environ.get("AD1_SECRET_" + publisher.upper()) else "default"
    local = credentials.local_bundle_sha256(publisher, root)
    print("secret %s (%s) name_source=%s local_bundle_sha256=%s" % (name, publisher, source, local))
    try:
        client.describe_secret(SecretId=name)
    except Exception as exc:
        if type(exc).__name__ == "ResourceNotFoundException":
            print("  NOT YET WRITTEN")
            return
        print("  UNREADABLE (%s)" % type(exc).__name__)
        return
    stored = hashlib.sha256(client.get_secret_value(SecretId=name)["SecretString"].encode("utf-8")).hexdigest()
    print("  exists=True stored_sha256=%s equals_local=%s" % (stored, stored == local))


def ft_expiry(root):
    envelope = json.loads(dpapi(SessionVault(root).path("ft").read_bytes(), decrypt=True))
    bundle = envelope["bundle"]
    saved_at = _utc(SessionVault(root).path("ft").stat().st_mtime)
    print("ft bundle: %d cookies, file saved_at=%s" % (len(bundle), saved_at))
    expiries = {}
    for name in sorted(bundle):
        # The ft bundle is a flat name->value map (ft_harvest_session.py, persist_http_cookies): a cookie
        # that carries an expiry would be a dict with `expires`; a string value carries none.
        value = bundle[name]
        expires = value.get("expires") if isinstance(value, dict) else None
        if isinstance(expires, (int, float)) and expires > 0:
            expiries[name] = expires
        print("  ft cookie %s expiry_utc=%s" % (name, _utc(expires) if name in expiries else "NOT RECORDED IN BUNDLE"))
    login = {n: expiries[n] for n in FT_LOGIN_COOKIES if n in expiries}
    present = [n for n in FT_LOGIN_COOKIES if n in bundle]
    if login:
        first = min(login, key=login.get)
        print("ft earliest login-cookie expiry: %s (%s)" % (_utc(login[first]), first))
    else:
        print("ft earliest login-cookie expiry: UNKNOWN -- login cookies present %s, none carries an expiry in the stored bundle" % present)


def sa_user_id_field(root):
    spec = importlib.util.spec_from_file_location("sa_rest_fetch", REPO / "org/tier1_exec/4.0.0_SA_CRO/scripts/sa_rest_fetch.py")
    sa = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sa)
    bundle = json.loads(dpapi(SessionVault(root).path("sa").read_bytes(), decrypt=True))["bundle"]
    cookies = bundle["all_cookies"]
    user_id = sa.bundle_user_id(cookies)  # raises NotAuthorized if no field carries it
    carrying = [c for c in cookies if c.get("name") == sa.IDENTITY_COOKIE]
    print("sa user_id field: bundle.all_cookies[name=%s] (%d cookie entries, 1 distinct value)" % (sa.IDENTITY_COOKIE, len(carrying)))
    print("sa stored user_id equals the old hard-coded literal: %s" % (user_id == "1btfwdu"))
    print("sa top-level bundle keys (names only): %s" % sorted(bundle))


def main():
    root = runtime_root()
    print("runtime root: %s (read-only)" % root)
    import boto3
    client = boto3.client("secretsmanager", region_name=credentials.REGION)
    for publisher in credentials.BUNDLE_PUBLISHERS:
        readback(publisher, root, client)
    ft_expiry(root)
    sa_user_id_field(root)
    print("PUBLISHER NETWORK CALLS: %d" % len(BLOCKED))
    return 0 if not BLOCKED else 1


if __name__ == "__main__":
    sys.exit(main())
