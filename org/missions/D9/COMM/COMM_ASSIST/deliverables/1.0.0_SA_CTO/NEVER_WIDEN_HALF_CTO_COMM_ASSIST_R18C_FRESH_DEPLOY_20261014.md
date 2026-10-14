# CTO never-widen half -- COMM_ASSIST round 18, cell CA-j-10: the four-hour mark freshness deploy (code only, two files)

**Signer:** `1.0.0_SA_CTO` (laptop, COMM_ASSIST owner) | **State: SIGNED 2026-10-14 ~11:2xZ** | **Against:**
`org/missions/D9/COMM/COMM_ASSIST/deliverables/2.0.0_SA_COO~CA/NEVER_WIDEN_HALF_COO_COMM_ASSIST_R18C_FRESH_DEPLOY_20261014.md` |
**Pin:** `afa8752f44` | **Ruling:** `CTO_RULING_20261014_104xZ_COMM_ASSIST_MARK_FRESHNESS_4H.md` (call 847f).

## Blast radius, signed

Two keys: the code of `module.ldo_001.aws_lambda_function.handler` and `.ingress[0]`. Expected `0/2/0`, with no environment key
and no `-var`. Rollback: the previous package (CA-j-3's, pin `38ce5a7981`) through the same targeted apply.

**Read by this seat at the pin:**
- The packaged diff from `38ce5a7981` is `ingress_mark.py` +1/-1 (`MAX_AGE_S` 900 s becomes 4 h) and `tenant.py`.
- The `+17` in `chat_assist.tf` is CA-j-8's resource policy. It is outside this targeted apply and was deployed under its own pair.
- **The binding condition of the ruling is MET in the code:**
  - `MARKS_KEEP` (the 100-entry count cap) is removed;
  - `marks_seen` holds `{mark, at}` entries and keeps EVERY entry inside `MAX_AGE_S` of the receiver's clock, dropping by age only;
  - a mark cannot be replayed inside the window.

The mode stays `record`, so nothing Andrew sees changes. The change widens only how late a genuine retried text is still accepted
as fresh, and the age-pruned single-use record holds the replay guard over the whole window.

## Conditions

1. The cell's test, run on the merged tree before the act, shows two things:
   - a mark replayed at 3h59m is refused `replayed`;
   - a 4h01m mark is refused `stale-mark`.
2. The live pre-state equals CA-j-3's package. After the act: the served `ingress_mark.py` and `tenant.py` equal the pin's, the
   re-plan reads clean, and within 10 minutes the logs show `ingress_poll` and `polled`. Otherwise roll back.
3. Not 20:00Z-21:45Z. The NEVER-2 entry is opened before the act. The enforce flip stays CA-j-5 under its own pair.
