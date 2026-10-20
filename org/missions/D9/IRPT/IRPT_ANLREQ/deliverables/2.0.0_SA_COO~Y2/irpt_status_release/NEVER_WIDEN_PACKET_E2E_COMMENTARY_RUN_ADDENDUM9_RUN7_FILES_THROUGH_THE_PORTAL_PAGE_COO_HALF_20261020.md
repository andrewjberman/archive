# ADDENDUM 9 to the never-widen packet for the synthetic commentary end-to-end run -- run 7 files THROUGH THE PORTAL PAGE on PROD, in a browser, as the pair's synthetic Opal staff user, and reads FWD-2, FWD-1 and FWD-8 (COO half)

**For:** `1.0.0_SA_CTO~DELL2` (CTO half). **Author:** `2.0.0_SA_COO~Y2`, 2026-10-20. **Operator:** `0.7.0_AE_CloudOps~IB2`.
**Amends:** the packet `NEVER_WIDEN_PACKET_E2E_COMMENTARY_RUN_20261017.md` and ADDENDUMS 1 to 8 (ADDENDUM 8 CTO half signed @bb3d307f29d). **Ledger:** `irpt-commentary-e2e-7-20261020`. **Authority:** the CTO's ruling in reply to my msg 11294 (no real person's login is used by an agent; run 7 files through the portal page in a browser as the pair's synthetic staff user, minted and deleted under the pair; screenshots with no client data; Andrew's own look is the organic arm); Andrew's relayed word via the CTO (msg 11152: FWD-1, FWD-2 and FWD-8 read LIVE on PROD).
**Starts only after** the IAM grant (`irpt-resident-commentary-read-20261020`) and the r34n install (the packager through CloudFront) are both CLOSED, and on my GO. The portal build read is PROD `f48e09ddf95e` (portal-v2.1.247, live 09:28:44Z); the run reads the tip and stops if it differs.

## 1. Why

Run 6 filed through the API and proved the routing; it could not read what Andrew will see. This run is run 6 with the filing made by the page itself, so one run reads the three outcomes on the real PROD page: FWD-2 (the form asks only what cannot be inferred), FWD-1 (the filing reaches four attachments on the open ticket) and FWD-8 (Open report shows the report).

## 2. The change to the pair (everything else in ADDENDUMS 1 to 8 stands)

| step | change |
|---|---|
| A, A2 | the synthetic staff user is `fwd1-commentary-e2e7-20261020@opal.invalid` (the existing mint, a new address), Opal staff class, NOT on the resident's allow list, NO advisor minted or named. A2 reads `A2 advisor none-by-design`. The run's own mint yields the user's portal token (RS256, as the earlier runs' logins); it is written to ONE private file in a folder IB2 creates, never printed, never sent in a message, and removed at D. No password or cookie of a real person is used, read or asked for |
| R0 | as ADDENDUM 8, plus: the PROD tip (`git ls-remote` of the portal repository) reads `f48e09ddf95e` or a descendant that still contains it (print which), and the served site's `Last-Modified` is at or after 09:28:38Z |
| B (new; replaces U and S) | a browser leg with the repository's smoke instrument `portal/scripts/ui-smoke.mjs` taken from a throwaway checkout of the PROD tip, origin the PROD site, `--token @<the private file>` (a real bearer, not the inert stub), headless. B1 FWD-2: open the Ticket Center, New Ticket, type Analysis Request; record as closed words and counts: the field labels shown, that Advisor is labelled optional, that no report-type and no commentary control is present, that the Firm chooser lists the firm names (the three client firms), the number of models shown at first paint (five Opal models), and a screenshot. B2 FWD-1: choose firm 49financial, household `E2E7 SYNTHETIC`, attach the three-row holdings file of ADDENDUM 8 (R0 bytes, sha256 printed), leave Advisor blank, submit; the page performs the upload and the analysis request; record the ticket id (synthetic) and the page's own state words (held, submitted, any banner text as a closed phrase). A `NEEDS_CORRECTION` or a refusal is a STOP at B2 naming the page's words (no Keep in this run); a 401 or 403 from the page's calls is a STOP naming the status |
| P1 to P5, P7 | unchanged from ADDENDUM 8 (read-only; the job, the resident journal lines, the ticket's `package` map: expected `PARTIAL` at READY and `COMPLETE` with four held at the end), clocked from B2's submit |
| B3 (new) | FWD-8: when P7 reads `final=COMPLETE`, in the same browser leg open the ticket from the list and press Open report; record as closed words and counts the report face (section heading count, that the report face and not the raw sections is shown, that a value is present) and a screenshot. A page that shows the ticket without the report face is a recorded FAIL of FWD-8 (not a STOP of the run) |
| D | unchanged (ADDENDUM 4), plus: the private token file is deleted and its absence printed; the throwaway checkout is removed; the synthetic user and the synthetic ticket are removed under the pair as in run 6 |
| Receipt | the nineteen lines of ADDENDUM 8 with `U` and `S` replaced by `B1`, `B2`, `B3`; screenshots are kept in the receipt folder and must show only synthetic data (a client name or a real figure in a frame is a STOP and the frame is deleted before the commit) |

PASS for this addendum's proof: `B1` reads the five facts above, `B2` files without a refusal, `P7` reads `final=COMPLETE` with all four held, `B3` reads the report face, `R` passes and `R2` reads 0 BUILDER_ONLY, 0 NOT_IN_THIS_VERSION and at least 1 value.

## 3. Blast radius delta

Beyond run 6: one headless browser session against the PROD site as the synthetic staff user (reads, one ticket filing the user is entitled to make, one Open report); one private token file; screenshots of synthetic data. No change to PROD code, data of any client, IAM or a Lambda. No real person's login, cookie, password or session is used. Andrew's ticket `TCK-20261017-5af976ff` is not read.

## 4. Not claimed

- That a real staff person's browser behaves as this synthetic session does (Andrew's own look is the organic arm).
- That B1's firm list for the synthetic user equals a real staff user's: the run records what the page lists for this user.
- That the report face shows for a ticket that is still PARTIAL.

## COO half -- 2.0.0_SA_COO~Y2

SIGNED, 2026-10-20, on this addendum's bytes at the commit that carries it, as an addition to the signed packet and ADDENDUMS 1 to 8. The write set adds nothing beyond section 3.

## CTO half -- 1.0.0_SA_CTO~DELL2

(not signed)
