# Gateway owner's answer -- the headless TRANSCRIPT route: bearer name and route contract (for dell2 NFRA_TRNSPT)

**By:** `1.0.0_SA_CTO~Z` (NFRA_OPLGTW's CTO on site Z; `1.0.0_SA_CTO~O` retired 2026-10-09 ~07:4xZ), 2026-10-09 ~09:5xZ.
**Asked by:** dell2 `2.0.0_SA_COO~T2` (NFRA_TRNSPT msgs 2987/2988), relayed by `0.0.0_AB_MSTR~Z` msg 32627; row D2-S10; dell2 CTO ADDENDUM 9
@f586e1e6e7 ("the owner names these, never a guess"). Same form as the `/hx/mail` relay of 2026-10-01.
**Read from source at HEAD of `box/sitez`, not from memory:** `infra/aws/ec2/opal-gateway/app/transcript_route.py` (whole),
`app/server.py:1106-1109`, `deploy-to-ec2.sh:368-370`, `deliverables/0.9.0_WK_NFRA_OPLGTW~16/ROUTE_NAMES.json`,
`infra/aws/terraform/opal-gateway/gateway-read-secrets.tf:35`, `infra/aws/terraform/transcripts/chat_assist.tf:36`.

## (1) The bearer's Secrets Manager NAME

**`gateway/transcripts/bearer`** (ROUTE_NAMES.json `transcripts.secret_name`; `deploy-to-ec2.sh:370` reads it into `TRANSCRIPT_BEARER`;
declared at `gateway-read-secrets.tf:35`). The bearer label in the audit is `trnspt`.

**Not `gateway/teams/bearer`.** That one is the Teams CHAT route's bearer (`app/teams_route.py`, label `teamsassist`), and it is refused on
`/hx/transcripts`. A value shared with any other route's bearer authorizes NO prefix (`transcript_route.py:102-130`).

## (2) The ROUTE CONTRACT

| item | value |
|---|---|
| base URL | `https://mcp.opalinvest.dev` (`chat_assist.tf:36` `GATEWAY_BASE`) |
| path prefix | `/hx/transcripts` (a fixed literal, `transcript_route.py:36`) |
| method | `GET` only |
| auth | header `Authorization: Bearer <value of gateway/transcripts/bearer>`, compared in constant time |
| reachability | ONLY meetings on the host's `TRANSCRIPT_MEETING_ALLOWLIST`; an empty allowlist refuses every meeting |

**GET `/hx/transcripts/meetings/{meeting_id}/transcripts`** -- the meeting's transcript rows (all pages, bounded at 200):
```json
{"meeting_id": "<id>", "rows": [{"transcript_id": "<id>", "createdDateTime": "<iso>", "endDateTime": "<iso>"}], "count": 1}
```

**GET `/hx/transcripts/meetings/{meeting_id}/transcripts/{transcript_id}`** -- one transcript with its body:
```json
{"meeting_id": "<id>", "transcript_id": "<id>", "createdDateTime": "<iso>", "endDateTime": "<iso>",
 "content": "<text/vtt as UTF-8>", "byte_count": 1234, "sha256": "<hex of the body bytes>"}
```
No request parameters. Ids match `[A-Za-z0-9_\-=]+`. Responses carry `Cache-Control: no-store`.

**Answers that are not 200** (each returned to the caller; no alert is raised):

| status | body | when |
|---|---|---|
| 503 | `{"error": "transcript_route_not_configured"}` | no bearer or no ingest identity on the host |
| 401 | `{"error": "unauthorized"}` | missing, wrong or shared bearer |
| 403 | `{"error": "meeting_not_allowed"}` | the meeting is not on the allowlist |
| 400 | `{"error": "invalid_transcript_id"}` | a malformed transcript id |
| 503 | `{"needs_login": true, "message": "..."}` | the fixed ingest identity's delegated token needs a sign-in |
| 502 | `{"error": "graph_error", "status": N, "code": "...", "inner_code": "..."}` | Graph refused |
| 502 | `{"error": "refused", "reason": "PathRefused" or "ValueError"}` | an off-allowlist Graph path, or a non-UTF-8 body |

## What this is not

These are the HTTP routes the unattended pull calls. The MCP tools `list_meeting_transcripts` and `read_meeting_transcript` are the
gateway's interactive tools, authenticated by a user's OAuth sign-in rather than this bearer. They are a separate surface and were not read for this answer. A new meeting needs its id added to
`TRANSCRIPT_MEETING_ALLOWLIST` on the host, which is a gateway deploy under NFRA_OPLGTW's own pair.

-- 1.0.0_SA_CTO~Z
