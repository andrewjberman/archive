# AMGT_RESAPP round 77 -- `AMGT-ba-21` ACT RECORD: the segments probe ran; BRANCH B; the pull did NOT run

`2.0.0_SA_COO~Z`, 2026-10-07 ~11:4xZ. Pair: COO half @68c7c203a1, CTO half @5907c4e544 (C1, C2).

## C1 -- the vehicle completed today (read before the probe, 11:30Z)

| read | value |
|---|---|
| `OPAL_BBGTML_daily_pull` | LastRunTime 2026-10-07 07:00:01 local, **LastTaskResult 0**, State Ready |
| its log `bbg_tplus1_20261007_070002.log` (last write 07:09 local) | PRECONDITION PASS (DAPI UP, an entitled session answered a real refdata request); PULL EXIT CODE 0; PUBLISH EXIT CODE 0; ETF LEG EXIT CODE 0; CONSTITUENTS LEG EXIT CODE 0; PRICE LEG EXIT CODE 0; RIVALFUNDS BLOOMBERG LEG EXIT CODE 90 (landed); RIVALFUNDS ENRICHMENT EXIT CODE 94 (landed) |
| `OPAL_BBGTML_freshness_check` (the 07:30 ET check) | LastRunTime 2026-10-07 07:30:01 local, LastTaskResult 0, State Ready at 07:30:33 local: finished, not running |

Branch (a): the vehicle completed and the check was over. The probe ran.

## The probe

`research_pulls.py run segments --probe "AMD US Equity"`, ONE `reference_data` call at 2026-10-07T11:32:01Z.
Driver line: `pulled 1 failed 0 calls 1 stopped None`, exit 0.

Landed as received: `s3://opal-data-harvest/bloomberg/harvest/bronze/segments/security_key=AMD_US_Equity/20261007T113201Z.json`,
458 B, VersionId `DfHqbZyXt1rt5KzVoGhwWuVWyTSnNBRh`, document-sha256 `f7129c78...`. Read back by this seat:

| field | result |
|---|---|
| `NAME` | `ADVANCED MICRO DEVICES` (the control: the request reached the security and a known field answered) |
| `SEGMENT_NAME` | `BAD_FLD` / `INVALID_FIELD`, code 9, "Field not valid" |
| `SEGMENT_REVENUE` | `BAD_FLD` / `INVALID_FIELD`, code 9, "Field not valid" |
| `GEOGRAPHIC_SEGMENT_NAME` | `BAD_FLD` / `INVALID_FIELD`, code 9, "Field not valid" |

## Verdict: BRANCH B -- no segment field is served by these names. Step 2 (the 85-name pull) did NOT run.

- What the refusal says (`integrations/bloomberg/READ_HERE.md` section 1 and 4): `INVALID_FIELD` means the mnemonic does not exist
  on the reference-data field surface. It is NOT an entitlement refusal and NOT "not applicable to this security": `NAME` answered
  on the same request. A different name may exist. The three names were proposed from a naming convention and were never read
  from a Bloomberg source (`research_pull_fields.json`), so this is the expected way for a guess to fail.
- It says nothing about whether Bloomberg HOLDS segment data, or about another surface (a bulk field, a historical request with
  overrides, BQL). READ_HERE section 4's rule: ask which surface refused before concluding what Bloomberg does not have.
- `research_pull_fields.json` is NOT edited: `probed` stays false, because no served segment field was found.
- Calls spent under this pair: 1 of at most 1 + 85. The pair is used up for the probe; a second probe with other field names is
  a NEW call and comes back to the CTO first (both halves say so).

## One instrument trap met on the way, no call spent

The first invocation ran under the shell's default interpreter (Python 3.14, which has no `blpapi`). The driver's `health()`
catches the import failure and returns false, so it stopped `TERMINAL_DOWN`, exit 5, `calls 0`, while the Terminal was up (the
vehicle had just completed against it). The same command under the vehicle's interpreter
(`...\Programs\Python\Python311\python.exe`, `blpapi 3.26.4.2`) made the call. A missing library and a signed-out Terminal read
identically in this driver. Surfaced as a row; the driver is not edited here.

## What is owed next (not under this pair)

The right mnemonics. That is a research question (Andrew's relaunch word routes research needs to the CRO): which Bloomberg
reference or bulk fields carry business-segment and geographic-segment revenue for an equity, read from a Bloomberg source and not
from a convention. With an answer in hand, a second one-name probe is asked of the CTO.
FWD-1 on AMD stays "SEGMENT PULL NOT YET RUN" for the round: the served reader of this bronze is uncut and has nothing to read.
