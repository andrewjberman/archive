# V leg grade -- IRPT_DASHBD.TO-DB-b-328 canary, on the issuer's own reads (2.0.0_SA_COO~S2, 2026-10-17 ~09:2xZ, dell2)

Canary client: digest12 `dde0e6ed7721` (the id travelled by broker only, msg 10457, and is not written here). Push state: LOCAL.

| step | grade | read |
|---|---|---|
| (1) the object exists | **PASS** | `head-object` on `irpt/49financial/platinum/reporting/client=<canary>/filled_report.json` in `opal-data-49financial`: ContentLength 52,718, one version (`ANqn9DlR...`), LastModified 2026-10-17T09:17:49Z, ContentType application/json. A streamed read-back (not written to a file) computed sha256 `2fb74e5d8087cf1e7b2891e144aaf0a3bbef97096512eb09a711776b3821d661` over 52,718 bytes, equal to ContentLength; top-level keys `household`, `values`. |
| (2) the route answers 200 with that sha256 for a covering viewer, and refuses a non-covering one | **OWED** | No covering and non-covering principal pair could be scoped without hand-typing a user-to-advisor link (IB2 msg 10457); IB2 minted nothing, as the order allows. |
| (3) one export renders a bundle whose filled body equals the same sha256 | **OWED** | The export submit sits behind edge JWT plus the API authorizer (`comp-routes auth-map`); I hold no session. The order's carve-out names step (2) only; this is the same cause, stated as a consequence. |

**What is and is not proven:** the object exists with a contract-shaped two-key body and a measured sha256. Not proven live: that the route returns these bytes to a covering viewer, that it refuses a non-covering viewer, and that an export of this client carries them. The unit tests and the estate's guard cover those paths; no live read does. I do not gate the full pass; `2.0.0_SA_COO~D2` and the CTO rule on it. I grade (2) and (3) when a viewer session exists.
