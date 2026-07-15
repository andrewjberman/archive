"""PROPOSED NEW FILE: app/integrations/opal_portal/integration.py  (OPAL_BBGTML B3)

Opal Portal integration -- ONE mutating tool, `opal_data_refresh_upload`, that sends the
day's two Bloomberg PKLs through the LIVE /data-refresh portal channel backend
(opal-data-refresh-api, data-refresh-v2.2.0) and confirms upload -> pipeline -> display.

THIS FILE IS A PROPOSAL. It lives in the OPAL_BBGTML deliverables folder and is NOT
applied to the gateway tree -- the m365 gateway is shared infrastructure; per the
sovereign-delegate briefing Rule 5 the exact diff goes to CTO for routing first.
See DIFF.md alongside this file for the full 6-part enablement (registry line, env,
secret, IAM grant, service-user provisioning, deploy).

Design decisions (grounded 2026-07-15):
- HYBRID auth. SharePoint locate/download of the PKLs uses the CALLER's own delegated
  Graph token (Alyssa already has access to the 'Shared' site; Microsoft enforces her
  scope). The portal API calls use a SHARED_SECRET service credential (a dedicated
  portal user with userType 'Dev' -- the opal-portal-authorizer + the Lambda's
  validate_user_type() gate requires it; grounded at
  infra/aws/lambda/data_refresh/lambda_function.py:89-114).
- The gateway NEVER UNPICKLES (unpickling is code execution; the box carries no pandas
  by design). Gateway-side checks are structural: exact filenames, plausible sizes.
  The full leg-2 tripwire (keys/dupes/as-of/row-bands) runs LOCALLY pre-send
  (tools/bbg_pkl_tripwire.py on the terminal machine).
- Big files NEVER ride the MCP channel: Graph download -> presigned PUT, all
  server-side (the OPAL_TAXSMA attachment-tools precedent).
- MUTATING integration => read_only=False, min_tier='standard' (the base.py validator
  refuses a read_only default on a harm surface), and the trigger leg is
  confirm-gated: dry_run exercises auth+upload into pending/ WITHOUT firing the
  yang-pipeline; the real send requires confirm=True.
- NEVER#5-safe confirmation: the pipeline run confirmed is the REAL run the upload
  triggers; 'displayed' is read from the served manifest, never a self-report.
"""
from __future__ import annotations

import datetime as dt
import json
import time
from typing import Optional

import httpx

from ..base import (
    AuthKind,
    Integration,
    IntegrationAuthError,
    IntegrationError,
    IntegrationSpec,
    SecretsCredential,
    run_integration_tool,
)

# The Shared site + project folder (grounded: the notebooks' output/ OneDrive-syncs here).
SHARED_SITE_HOSTPATH = "opalinvest.sharepoint.com:/sites/Shared"
PROJECT_FOLDER = "OCIO Models/Dashboard/202511 Model Portfolio Exposure/output"
# Portal API bases (same as portal/src/api/portal-proxy.ts).
PORTAL_API_BASE = "https://7k3ed8px20.execute-api.us-east-1.amazonaws.com"
UPLOAD_URLS_PATH = "/prod/api/scoped/data-refresh/upload-urls"
TRIGGER_PATH = "/prod/api/scoped/data-refresh/trigger"
STATUS_PATH = "/prod/api/scoped/data-refresh/status/{execution_id}"
MANIFEST_PATH = "/prod/api/general/json/latest/manifest.json"
LOGIN_PATH = "/auth/login"   # CTO review pin: confirm exact route + body shape at apply time
SIZE_BOUNDS_MB = (2.0, 60.0)  # structural sanity only; the real shape gate is the local tripwire

SPEC = IntegrationSpec(
    id="opal_portal",
    display_name="Opal Portal Data Refresh",
    description="Send the daily Bloomberg PKL pair through the /data-refresh portal channel "
                "(upload-urls -> presigned PUT -> trigger -> status -> served-manifest confirm).",
    auth_kind=AuthKind.SHARED_SECRET,
    tool_prefix="opal_",
    secret_id="opal/portal/svc-data-refresh",   # {"email": ..., "password": ...} (service user, userType Dev)
    read_only=False,                             # MUTATING: fires the yang-pipeline
    min_tier="standard",                         # validator requires elevated tier on a mutating integration
    hosts=("7k3ed8px20.execute-api.us-east-1.amazonaws.com", "graph.microsoft.com"),
)


def _expected_stamp() -> str:
    """The notebooks' own rule: date_end = today - 1 business day (naive BDay; the local
    tripwire owns holiday nuance via --allow-stale)."""
    d = dt.date.today()
    back = 1
    cur = d
    while back:
        cur = cur - dt.timedelta(days=1)
        if cur.weekday() < 5:
            back -= 1
    return cur.strftime("%Y%m%d")


class _PortalSession:
    """Service login -> cached JWT. Invalidate-and-retry-once on 401."""

    def __init__(self, cred: SecretsCredential):
        self._cred = cred
        self._jwt: Optional[str] = None
        self._at: float = 0.0

    def token(self, force: bool = False) -> str:
        if self._jwt and not force and (time.time() - self._at) < 540:  # <10 min cache
            return self._jwt
        secret = self._cred.get()  # {"email","password"}
        r = httpx.post(PORTAL_API_BASE + LOGIN_PATH,
                       json={"email": secret["email"], "password": secret["password"]},
                       timeout=30)
        if r.status_code != 200:
            raise IntegrationAuthError(f"portal login {r.status_code}")
        tok = r.json().get("accessToken") or r.json().get("token")
        if not tok:
            raise IntegrationAuthError("portal login returned no token")
        self._jwt, self._at = tok, time.time()
        return tok


class OpalPortalIntegration(Integration):
    spec = SPEC

    def __init__(self):
        self._session = _PortalSession(SecretsCredential(
            SPEC.secret_id, region="us-east-1",
            parse=lambda raw: json.loads(raw), ttl_s=300))

    # -- Graph helpers (DELEGATED: the caller's own token) ---------------------------------
    @staticmethod
    def _graph_find_pkl(user_token: str, name: str) -> dict:
        """Resolve the drive item for output/<name> on the Shared site; return id+size+url."""
        h = {"Authorization": f"Bearer {user_token}"}
        site = httpx.get(f"https://graph.microsoft.com/v1.0/sites/{SHARED_SITE_HOSTPATH}",
                         headers=h, timeout=30)
        if site.status_code != 200:
            raise IntegrationError(f"Graph site resolve {site.status_code}")
        site_id = site.json()["id"]
        item = httpx.get(
            f"https://graph.microsoft.com/v1.0/sites/{site_id}/drive/root:/{PROJECT_FOLDER}/{name}",
            headers=h, timeout=30)
        if item.status_code == 404:
            raise IntegrationError(
                f"'{name}' not found in the SharePoint output folder -- run /bbg-pull first "
                "(and give OneDrive a minute to sync)")
        if item.status_code != 200:
            raise IntegrationError(f"Graph item resolve {item.status_code}")
        j = item.json()
        return {"id": j["id"], "size": j["size"], "site_id": site_id, "name": name}

    @staticmethod
    def _graph_download(user_token: str, site_id: str, item_id: str) -> bytes:
        r = httpx.get(
            f"https://graph.microsoft.com/v1.0/sites/{site_id}/drive/items/{item_id}/content",
            headers={"Authorization": f"Bearer {user_token}"},
            follow_redirects=True, timeout=300)
        if r.status_code != 200:
            raise IntegrationError(f"Graph download {r.status_code}")
        return r.content

    # -- registration ----------------------------------------------------------------------
    def register(self, mcp) -> list[str]:
        session = self._session
        find_pkl, download = self._graph_find_pkl, self._graph_download

        @mcp.tool()
        def opal_data_refresh_upload(date: str = "", dry_run: bool = False,
                                     confirm: bool = False) -> dict:
            """Send the day's two Bloomberg PKLs (data/model 'YYYYMMDD v1.pkl') from the
            SharePoint output folder through the portal /data-refresh channel.
            dry_run=True uploads into pending/ WITHOUT triggering the pipeline (safe
            exercise). The real send fires the yang-pipeline and requires confirm=True.
            Returns uploaded/pipeline/displayed confirmations."""
            args = {"date": date, "dry_run": dry_run, "confirm": confirm}

            def fn(_credential) -> dict:
                stamp = date or _expected_stamp()
                names = [f"data {stamp} v1.pkl", f"model {stamp} v1.pkl"]
                if not dry_run and not confirm:
                    return {"confirm_required": True,
                            "message": f"This fires the LIVE yang-pipeline with vintage {stamp}. "
                                       "Re-invoke with confirm=true (or use dry_run=true to "
                                       "exercise upload only)."}
                # 1) locate + structural checks via the CALLER's delegated Graph token
                from ...context import get_current_email  # caller identity for the delegated leg
                from ...token_broker import get_token
                user_token = get_token(get_current_email())
                items = [find_pkl(user_token, n) for n in names]
                for it in items:
                    mb = it["size"] / 1e6
                    if not (SIZE_BOUNDS_MB[0] <= mb <= SIZE_BOUNDS_MB[1]):
                        raise IntegrationError(
                            f"'{it['name']}' size {mb:.1f}MB outside plausible bounds "
                            f"{SIZE_BOUNDS_MB} -- run the local tripwire; not sending")
                # 2) portal service JWT + presigned upload urls
                jwt = session.token()
                ph = {"Authorization": f"Bearer {jwt}"}
                r = httpx.post(PORTAL_API_BASE + UPLOAD_URLS_PATH,
                               headers=ph, json={"files": names}, timeout=60)
                if r.status_code == 401:
                    jwt = session.token(force=True)
                    ph = {"Authorization": f"Bearer {jwt}"}
                    r = httpx.post(PORTAL_API_BASE + UPLOAD_URLS_PATH,
                                   headers=ph, json={"files": names}, timeout=60)
                if r.status_code != 200:
                    raise IntegrationError(f"upload-urls {r.status_code}: {r.text[:200]}")
                grant = r.json()
                upload_id = grant.get("uploadId")
                url_map = {u["fileName"]: u["url"] for u in grant.get("urls", [])} \
                    if isinstance(grant.get("urls"), list) else grant.get("uploadUrls", {})
                # 3) stream each PKL Graph -> presigned PUT (never through the MCP channel)
                uploaded = []
                for it in items:
                    blob = download(user_token, it["site_id"], it["id"])
                    put = httpx.put(url_map[it["name"]], content=blob,
                                    headers={"Content-Type": "application/octet-stream"},
                                    timeout=300)
                    if put.status_code not in (200, 204):
                        raise IntegrationError(f"PUT '{it['name']}' {put.status_code}")
                    uploaded.append({"name": it["name"], "bytes": len(blob)})
                if dry_run:
                    return {"dry_run": True, "upload_id": upload_id, "uploaded": uploaded,
                            "note": "files staged in pending/ only; pipeline NOT triggered"}
                # 4) trigger the pipeline
                r = httpx.post(PORTAL_API_BASE + TRIGGER_PATH, headers=ph,
                               json={"uploadId": upload_id}, timeout=60)
                if r.status_code != 200:
                    raise IntegrationError(f"trigger {r.status_code}: {r.text[:200]}")
                execution_id = r.json().get("executionId", "")
                # 5) poll the run to a terminal state (the REAL production run)
                status = "UNKNOWN"
                for _ in range(45):  # ~15 min at 20s
                    time.sleep(20)
                    s = httpx.get(PORTAL_API_BASE + STATUS_PATH.format(execution_id=execution_id),
                                  headers=ph, timeout=30)
                    if s.status_code == 200:
                        status = s.json().get("status", "UNKNOWN")
                        if status in ("SUCCEEDED", "FAILED", "TIMED_OUT", "ABORTED"):
                            break
                # 6) display confirmation from the SERVED manifest (never a self-report)
                m = httpx.get(PORTAL_API_BASE + MANIFEST_PATH, timeout=30)
                manifest_note = f"manifest HTTP {m.status_code}"
                if m.status_code == 200:
                    manifest_note = str(m.json())[:300]
                return {
                    "uploaded": uploaded, "upload_id": upload_id,
                    "pipeline": {"execution_id": execution_id, "status": status},
                    "displayed": manifest_note,
                    "confirmation": ("uploaded OK; pipeline " + status +
                                     "; check the manifest vintage above matches " + stamp),
                }

            return run_integration_tool(SPEC, "opal_data_refresh_upload", args, fn,
                                        credential_provider=self._session._cred.get)

        return ["opal_data_refresh_upload"]
