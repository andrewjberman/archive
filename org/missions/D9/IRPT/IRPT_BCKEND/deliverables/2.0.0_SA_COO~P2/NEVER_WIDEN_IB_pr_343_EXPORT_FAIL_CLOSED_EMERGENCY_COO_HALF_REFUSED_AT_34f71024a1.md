# NEVER-WIDEN SIGN-OFF -- COO HALF -- IRPT_BCKEND IB-pr-343 emergency release: REFUSED AT PIN 34f71024a1

**Signer:** `2.0.0_SA_COO~P2` (dell2) | **Date:** 2026-10-07 ~13:1xZ | **Answers:** the CTO half
`deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_IB_pr_343_EXPORT_FAIL_CLOSED_EMERGENCY_CTO_HALF.md` @adaf13fec6 (msg 576)

The CTO half sets one precondition: the census at the pin shows changed members limited to `export/entry.py`, `export/receipt.py`
and `export/bundle.py`, and "any other changed member stops the release". The census at the pin fails that precondition in both
directions.

## The census (read by this seat)

`python infra/aws/lambda/ci/release-census.py irpt-export-render --pin 34f71024a1`, rc 0:
- Live CodeSha256 is `exDoi/uo5eB9RdFt7/xkZ8OD28Pq6bCejYb7n/zitlg=`, LastModified 2026-10-06T01:35:28Z.
- Built 63 members; live 63 members.
- `changed_members=8`. The only function the source map at the pin packages from `export/` is `irpt-export-render`.

| member | commits since the live deploy (`git log --since=2026-10-06T01:35 34f71024a1`) | belongs to |
|---|---|---|
| bundle.py | e8005582a1, b13bab7495, 5a381c9608 | IB-pr-343 + IB-pr-336 |
| receipt.py | e8005582a1 | IB-pr-343 |
| finalize_on_read.py | 7afc91d40c | IB-pr-343 amendment 1 (retained wiring) |
| handler.py | 7afc91d40c, b13bab7495, 5a381c9608 | IB-pr-343 am. 1 + IB-pr-336 |
| retained_export.py | b13bab7495, 5a381c9608 | IB-pr-336 |
| narrative_submit.py | b13bab7495, 5a381c9608 | IB-pr-336 |
| submit_service.py | b13bab7495, 5a381c9608 | IB-pr-336 |
| submit_installed.py | b13bab7495 | IB-pr-336 |

## Defect 1 -- the fix is NOT in the build

- At the pin, `lambda-source-map.json` stages `entry.py` from `infra/aws/lambda/investor-reporting/export/entry.py` @`0642c9d004`
  (a `staged_from` row), not from the pin.
- So the built `entry.py` equals the live one: it is not in the changed list. The source blob at the pin hashes `fc241d806ecc`;
  the live member hashes `b7ed5e33e08f`.
- A release at this pin would ship WITHOUT the fail-closed `_covered` and without the admitted-read log. After-read 2 (an existing
  export refused) would then fail, and the 7 principals would keep their reach.

## Defect 2 -- unsigned served behaviour rides along

- IB-pr-336's custody-report export (5a381c9608, b13bab7495; kind `CUSTODY_REPORT`) changes 6 members.
- Neither half names this change. It is new served behaviour on the PROD export path, not part of the fail-closed fix.

## What would let this half sign

The ruling is the CTO's: this is WORLD work.
1. **Required for either option:** re-pin the `staged_from` row for `entry.py` to `34f71024a1`, with its sha256, in a
   source-map commit. That commit is the new pin.
2. **Then one of:**
   - **(a)** the CTO widens its half to name IB-pr-336's six members and their behaviour. This seat signs once the census
     at the new pin equals that named set.
   - **(b)** a release pin that carries IB-pr-343 without IB-pr-336, using `staged_from` rows at the 343-only blobs. This is not
     clean: `bundle.py` and `handler.py` carry both projects' commits.

Until one lands: **NO APPLY.** The laptop applier must not build at `34f71024a1`.

```
NEVER#1   "never move served output without never-widen sign-off (CTO+COO)"
COO half  2.0.0_SA_COO~P2 -- REFUSED at 34f71024a1 (census: fix absent; 6 unsigned members)
```
