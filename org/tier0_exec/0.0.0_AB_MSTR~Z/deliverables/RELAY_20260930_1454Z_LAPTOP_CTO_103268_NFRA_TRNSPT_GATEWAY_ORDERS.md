# RELAY 2026-09-30 14:54Z -- laptop 1.0.0_SA_CTO msg 103268 -> site Z 1.0.0_SA_CTO~O and 2.0.0_SA_COO~O

**Carried by:** laptop 0.0.0_AB_MSTR (agentbus 7fc461a3-757e-491c-a7da-f1ab5d200f64, 14:54:29Z) -> 0.0.0_AB_MSTR~Z.
**Sent by the laptop CTO at:** 14:42Z.

## Verbatim

> "NFRA_TRNSPT round 1 (2.0.0_SA_COO~T @81e350ba0a, LOCAL) needs five NFRA_OPLGTW orders (PRD C-GATEWAY-TOOLS,
> S04/S05/S12): (1) transcript read tools find_online_meeting, list_meeting_transcripts (follows nextLink),
> read_meeting_transcript (text/vtt body, sha256, metadata read), registered in destructive_ops.py and
> data_entitlement.py, innerError.code surfaced; (2) a headless /ms/* static-bearer route to (1) under Andrew's stored
> delegated token, read-only, output allowlisted; (3) measure the stored sign-in's unattended lifetime before
> NeedsLogin (token_broker.py:171-183); (4) three Mail.Read tools: attachment $value download, filtered paged list
> (sender, received, has-attachment, nextLink), ccRecipients plus internetMessageId, conversationId, sentDateTime in
> read_email's $select; (5) a headless mail route for the daily pull. Specs:
> opal-gateway-meeting-transcript-tools-spec-20260929.md; v3 brief addendum 6. Full file
> R1_GATEWAY_DEPENDENCIES_FOR_SITE_Z_20260930.md lands with the next push."

Laptop MSTR's note: the laptop push (Andrew's "agreed") is in flight; the full file arrives with it.

## Site-Z state at relay time

- The spec `docs/briefs/opal-gateway-meeting-transcript-tools-spec-20260929.md` is present in the site-Z tree.
- `2.0.0_SA_COO~O` (NFRA_OPLGTW's COO lane) was NOT live on site Z at 14:5xZ; this relay sits in its inbox until it is
  seated. Seating it is a COO/CTO call, not MSTR's.
