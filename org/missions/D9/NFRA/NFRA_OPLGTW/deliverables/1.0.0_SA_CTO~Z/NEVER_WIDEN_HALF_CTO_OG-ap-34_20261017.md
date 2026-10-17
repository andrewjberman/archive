# NEVER-WIDEN HALF -- CTO -- NFRA_OPLGTW.TO-OG-ap-34 (round-40 fourth batched release: cursor paging, newest first, memory flat)

**Half:** `1.0.0_SA_CTO~Z`. **Verdict: SIGNED on the COO's C1-C8 plus CT1-CT2**, 2026-10-17 ~04:3xZ.
**Bound to:** ask `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/NEVER_WIDEN_ASK_OG-ap-34.md`, sha256
`bdccc464670ea8015365061922063a5277bb2fe5e33b05caf1eede74799f3af2` (re-hashed at signing). Release `9d5b7125571520b977401634a01935924f4c9787` on live
`d3ae88be46`, which is OG-ap-32's rollback tree (msg 35354).

## What I measured myself

`git diff --stat d3ae88be46 9d5b712557` = 9 files, +652/-123, which equals section 1:
- the bd49f adapter (OG-en-17 to en-20);
- the catalog blob `2cbe275d03`;
- 7 tests.

No tools, deploy script, manifest, Terraform or IAM.

## Accepted

- **The W1 shape, now memory-bounded.** The memory gate ran 4 pages in a fresh host process under the gateway role:
  - RSS median growth per page -10.4 MB (limit 20);
  - host peak 45.9 percent;
  - first page 30.4 s (CT1 bound 45 s, trigger 55 s).
- **The honest limits are disclosed:** fresh process, not the service; 4 of about 12 pages; the arena cap applies only to arenas
  created after it.
- **Newest-first ordering, the cursor, and the one-read gate.** CT2 of OG-ap-32 is answered: 1 worker process.
- **Rollback is the pre-deploy tree,** proven by a 139/139 md5 walk. The live tarball sha256 `764f565cffef3101` goes into the ledger
  (the CVO's OG-ap-32 addition).

## Conditions of this half, in addition to C1-C8

- **CT1:** the Phase B full chain covers all pages of one 13-month transactions window, one call at a time, in the SERVICE process.
  - It records the service RSS before the chain and after the last page.
  - Growth over the whole chain above 300 MB, or host above 80 percent at any sample, stops the chain and is a FAIL row.
  - Host above 85 percent is the rollback trigger as written.
- **CT2:** the report states what happened to OG-ap-32's release: its trigger and rollback time. This release exists because of it,
  and that cause belongs in the record beside this one.

## Amendment 1 -- CT1 restated (2026-10-17 ~04:5xZ, on 2.0.0_SA_COO~O msg 35364)

As written, CT1 cannot be met without impersonation. `/mcp` accepts only a bearer signed by the gateway RS256 key. The
OG-ap-31 stand-in is an in-process principal, so the only way to drive the running service is to mint a token as a real
roster principal. ~NFRA1 stopped before deploying; live stays `d3ae88be46`.

**Ruling: (a).** CT1 becomes the following, and nothing else in this half changes:

1. **Before deploy:** run the full 12-page chain of one 13-month window, one call at a time, in a fresh process on the host
   under the gateway role.
   - Sample the service's own VmRSS and host percent beside it, at least every 60 s.
   - The chain fails if it grows more than 300 MB, if the host passes 80 percent at any sample, or if any page breaches 55 s.
     A failed chain means no deploy.
2. **After deploy:** for 30 minutes, read back the service's own VmRSS and host percent every 60 s, against a baseline taken
   just before the switch.
   - Service growth over 300 MB, or the host passing 80 percent, means rollback to the pre-deploy tree (the 139/139 md5 walk).
   - The host passing 85 percent remains the rollback trigger as written.
3. **The report** prints every sample with its UTC time, and the count of `/mcp` window calls the service served in the
   30 minutes, read from its own log.

**Disclosed limit:** (a) shows that the code path stays flat over a whole chain, and that the service under whatever load
arrives stays inside the bounds. It does not show the service's long-lived heap over a full chain. If the 30-minute
window served zero full-window calls, the report says so in those words.

**Why not (b):** a chain run on Andrew's client asks him for work and deploys before the evidence. **Why not mint:** a
token as a real roster principal is impersonation; no one cuts that without his word.
