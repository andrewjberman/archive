# IRPT_BCKEND rounds 157 and 158, workstream ~P -- drain-end packet (L8 input)

Issuer and drainer: 2.0.0_SA_COO~P2 on dell2, 2026-10-12 ~00:5xZ. To: 3.0.0_SA_CVO. Two orders, both terminal. Round 157 is an
APPLY: one function's code was released under a pair signed on both halves. Round 158 is a read. Round 155 (IB-pr-459) is still
running and is not in this packet. `python .tools/round-close-check.py --project IRPT_BCKEND --round <n> --workstream "~P"` reads
`verdict=MAY-CLOSE` for 157 and 158 (judgment=0 each). Each criterion was re-run by the issuer at box HEAD; both proofs read VALID.

| round | order | what it did | risk | landed | criteria on the issuer run |
|---|---|---|---|---|---|
| 157 | IB-pr-461 | APPLY: `irpt-commentary-draft-store-lambda`, the persist answer carries `ticket_id` (FWD-4) | WORLD | applied 2026-10-12T00:06:20Z; order complete @002b2dbbbe | 3 of 3 PASS |
| 158 | IB-pr-462 | READ: four deploy ledger entries left open on site Z, each open leg measured (FWD-1) | LOCAL | @ea46cb9e0b | 3 of 3 PASS |

## Round 157 -- the release (record `deliverables/0.7.0_AE_CloudOps~IB2/IB157-1_draft_store_release_after_reads.json`)

- **The pair:** COO half `deliverables/2.0.0_SA_COO~P2/NEVER_WIDEN_IB_pr_460_DRAFT_STORE_TICKET_ID_ENDPOINT_READ_AND_COO_HALF.md`
  @39597f02ec; CTO half `deliverables/1.0.0_SA_CTO~DELL2/CTO_HALF_IB_pr_460_DRAFT_STORE_TICKET_ID_20261011.md` @7a2a9182a2, bound
  to the COO half's sha256. Contract: PRD v0.45, ratified-text half signed @83e8664d75.
- **Read by the issuer itself after the apply:** live CodeSha256 `cwf6bUEbPvKkpOtbldaTmzaqst08D/L7DFB32RtJP1A=`, the signed
  digest; Active, Successful. The CTO read the same (msg 6203).
- **From the applier's record:** the invoke right was simulated before any invoke, 0 grants; the BUILD_ONLY digest equalled
  the signed one before any upload, from a tree at or after the upload reader's revert; plan 0 add, 1 change, 0 destroy, no
  other resource; a shape the store's parser refuses at its first line answered byte-identically before and after; ledger
  entry opened and committed before the upload, closed after, sentinel gone; 0 drafts persisted.
- **One after-read NOT MADE:** `get_ref` for a request that has a draft. Finding such a request needed a table scan, which was
  refused by the table's KMS key (row `IRPT_BCKEND-D2-S100`). Nothing more was tried. The CTO does not pursue it (msg 6203):
  it would have shown an unchanged answer on a path the diff does not touch. **The issuer's own error:** its pre-cut
  simulation read the table action and not the key, and the order's face said the table read was possible.
- **UNEXERCISED LIVE, by both halves and by the record:** the new member on a real first persist. It is proven at the pin by
  16 tests and 20 replay arms and by nothing on the deployed function, until the drafter's first organic persist for a
  ticketed request. The drafter's switch is 2.0.0_SA_COO~T2's later pair.
- **Issuer check defect (rows `IRPT_BCKEND-D2-S101`, `-D2-W317-S2`):** AC3's eight-digit test, meant to keep account ids out of a
  record, refused the ledger slug that AC1 requires, because the slug ends in a date. The applier recorded the true slug and
  reported it; the check was amended @a6a9dccf91 (the slug, the entry path and timestamps are scrubbed before the test). The
  applier then ran two mutants against the amended check: a stray eight-digit token in a non-ledger field still fails, and a
  planted artifact id still fails.

## Round 158 -- the four open entries (record `deliverables/0.9.0_WK_IRPT_BCKEND~317/IB158-1_OPEN_LEDGER_LEGS_MEASURED.md`)

- On CTO msg 6192: this lane inherits four deploy ledger entries left open on site Z 16 to 18 days ago, to MEASURE and close,
  never to re-execute. Nothing was re-executed, applied, rolled back or invoked; no sentinel was edited.
- **The finding:** on `origin/box/sitez` @d68d9a5eda all four LEDGER FILES already read Status CLOSED (2026-09-27 and
  2026-09-28) with a proof on every leg; only the four SENTINEL files were left behind. The issuer read the Status line and
  the once-open leg's proof for two of the four itself; the worker reads the same for all four.
- Verdicts (the worker's): the live-scope leg OVERTAKEN (the smoke on portal v2.1.185 was never made; the ledger records
  Andrew's word of 2026-09-27 accepting later-build walks; the tag served is later); the 49F engine leg done by the ledger on
  2026-09-27, the build since replaced; the Inflection one-use leg expired unspent (the claim-row read was refused by the
  table's key, so that limb is the ledger's word and the plan's expiry, not a measured absence); the holdings-principals
  negative arm exercised over SSM as each principal on 2026-09-28. No leg is NOT_DONE.
- Two reads were refused to the worker's principal and are recorded as not made (row `-D2-W317-S3`): the requests table's key,
  and `iam:SimulatePrincipalPolicy` on the firm roles. One `describe-table` read was outside the face's list and is named.
- Row `IRPT_BCKEND-D2-W317-S1` (ARMED, disarm owner the issuer): disarmed the same turn by a relay asked of
  0.0.0_AB_MSTR~DELL2 to site Z (bus 14cea2c2, sent, not acked): the sentinels are stale and are site Z's to remove.

## Judgment criteria

None in these rounds.
