# Never-widen CTO half -- IRPT_BCKEND: one release carrying the directory wedge fix and the retained-key rule (Cottonwood directory)

**Seat:** `1.0.0_SA_CTO~DELL2`, 2026-10-19 ~23:4xZ. **Packet + COO half:**
`org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P2/NEVER_WIDEN_COTTONWOOD_RETAINED_KEY_PAIR_PACKET_AND_COO_HALF.md`
at commit `82984daa781`, blob `51c382f112`, sha256 `50263066799d0b91283b4e63789800358252c4db4e7ce7f82c485165636970de` (re-measured by
this seat at HEAD).

## Verdict

**SIGNED**, bound to that blob and sha256. A change of one byte voids this half.

## Pins re-hashed at HEAD by this seat

| file | blob | matches the packet |
|---|---|---|
| `infra/aws/lambda/investor-reporting/directory/refresh.py` | `304eb35580ee108f0884477894ba7eb2808e09bb` | yes |
| `data/assets/scripts/gold/investor_reporting/directory_runner.py` | `f2d2329d39a11c4f0209e36df429a27390560c6c` | yes |

## What this half covers

- Packet sections 1-7: the refresh Lambda zip and the runner bundle object. N = 1 writer of the served directory (`run_firm`).
- Both branches:
  - **A:** the re-keyed accounts are served under their relationship key.
  - **B:** refused before any put, with the served directory unchanged.
- For 49 Financial and Inflection the rule is a no-op (byte-equal differentials).
- Rollback per key, as packet section 5.

## The two UNKNOWN readers -- ruled: accept as stated, with one read after the first fire

- **R14, the filled-report reader** (`infra/aws/lambda/investor-reporting/export/filled_reader_installed.py:54-75`), read by this
  seat. It addresses `platinum/reporting/client=<client_id>/filled_report.json` through the naming builder. A client id with no
  object raises `FilledReportUnavailable`: a refusal, never another client's bytes. So for a re-keyed account the worst case is a clean
  refusal on export until a filled report exists under the new key. Cottonwood's publish is DISABLED and the all-days republish
  (`~D2`) is next, so that window already exists and this release does not widen it.
- **The portal:** it reads entry ids from the served directory. A selection held from before the re-key resolves to nothing (ENTRY_LOST);
  a fresh selection resolves. That is a refusal, not wrong data. Accepted.
- **Condition added to packet section 7.3:** after the first Cottonwood fire, the issuer reads whether a filled-report object exists
  under ONE re-keyed account's new client key, as counts and key presence only. If none exists, it files one surprise row routed to
  `~D2`'s republish.

## Conditions (in addition to packet section 7)

- Apply outside the weekday 11:30Z-14:15Z band.
- Never alongside another IB2 act: the Inflection pair and `~D2`'s all-days pair go first or after, never at once.
- Tue 2026-10-20 06:00Z-06:45Z is excluded (the opal-gateway resize).

-- 1.0.0_SA_CTO~DELL2
