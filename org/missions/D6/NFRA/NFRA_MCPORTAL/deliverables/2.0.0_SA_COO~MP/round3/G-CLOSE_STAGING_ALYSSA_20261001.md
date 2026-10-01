# NFRA_MCPORTAL round 3 -- G-CLOSE staging (MP-c-1), colleague = Alyssa -- `2.0.0_SA_COO~MP`

**archetype:** STAGE (read-only against the world; no grant write, no invoke)
**Authority:** Andrew-direct 2026-10-01 ~15:51Z, verbatim "4.) We can do this with Alyssa." Record
`org/tier1_exec/4.0.0_SA_CRO~O/deliverables/ANDREW_DIRECT_20261001_1551Z_FABRIC_STATUS_ANSWERS_GPUSH_ALYSSA_D6.md`
@53ad7cb452; seat ask `1.0.0_SA_CTO~O` msg 27936. The quote does NOT cover G-2ND (MP-v-1); MP-v-1 stays staged.
**Time:** Andrew sets it (msg 27936). Nothing below is executed until he does.

## 1. Live reads, 2026-10-01 ~16:2xZ (identifiers withheld; principal named by partition hash prefix only)

| read | value |
|---|---|
| `gateway-access-state-table` POLICY# items / scanned | 13 / 336 |
| principal partitions whose records name Alyssa | 1 (pk sha256 prefix `2c61471b14`) |
| her `principal_profile` | `active`, `restricted`, `grant_revision` 2 |
| her `data_entitlement` revisions | 2, both `active`; rev 2 is the live grant |
| rev 2 scope (shape) | ops describe/list/query; datasets dim_asset, dim_balance, dim_position, dim_transaction; masters 2; accounts keyed by both masters (~7.5k each); dates rolling_complete_window; 10 portal channels |
| rev 2 origin (her `operator_audit`) | 2026-09-30T19:15:29Z, "ONE new Schwab grant (NFRA_MCPINDEX MX-r-6 A5/A6)" |
| `mcportal-grant-writer-lambda` | Active, LastModified 2026-09-30T10:58:57Z (MCPMSP MS-w-1 register_tenant redeploy) |
| writer owner config after that redeploy | claim `sub`, key present, 43 chars (= the G-SUB value's length) |
| `mcportal-grant-changes-table` items | 1: `narrow` REFUSED NO-OWNER-HEADER 2026-09-29T05:00Z (MP-a-2's arm); no colleague write yet |

## 2. The collision this staging found

Alyssa's ONLY data grant is the one NFRA_MCPINDEX r6.J1 (her cold run, MXV7-J2) runs through. G-CLOSE narrows that
same grant. If the narrow lands before or during r6.J1, the cold run grades a narrowed grant and MCPINDEX's FWD-1
judgment is contaminated. **Order inside ONE Alyssa sitting: r6.J1 first, then G-CLOSE.** The widen-back restores the
rev-2 scope, so r6.J1's grant is whole again when G-CLOSE ends. Coordination with `2.0.0_SA_COO~MI` (r6.J1 waits on MX-r-8
serving).

## 3. The run sheet (Andrew at mcp.opalinvest.dev, Entitlements tab; Alyssa in her Claude client with the Opal connector)

0. r6.J1 is finished (COO~MI confirms). The issuer writes down `t0` (UTC) when Andrew starts.
1. **Narrow:** on Alyssa's grant, keep ONE master and its accounts (drop the other master). Datasets and operations
   stay unchanged. The narrowed answer stays REAL (fewer accounts and rows), never a refusal. AC3 needs that.
2. **Ask (after narrow):** Alyssa asks one question that spans both masters, e.g. "How many Schwab accounts can you see,
   and what is the total market value of positions across them as of the latest date?" Expected: an answer over one
   master only.
3. **Widen back:** restore the dropped master and its accounts, so the scope equals rev 2.
4. **Ask again:** the same question, word for word. Expected: both masters, matching the BEFORE answer.
5. The issuer writes down `t1`. Alyssa sends Andrew the BEFORE (optional, from r6.J1), AFTER-narrow and AFTER-widen
   exchanges, as copied text or a chat export. They go to an OFF-repo folder (`raw_dir`); nothing raw is committed.

Then the issuer writes `deliverables/0.9.0_WK_NFRA_MCPORTAL~1/c1_run.json` {t0, t1, principal_sha256, raw_dir}, flips
MP-c-1 staged -> pending, and spawns slot ~1 (the order's three spawn conditions: MP-a-2 drained @d01a0c99c4, Z-S10
ruled by msg 26207, G-CLOSE done).

## 4. Not staged here

- G-2ND (MP-v-1): no Andrew word; stays staged.
- The v0.4 C4 addendum (register_tenant) is built by NFRA_MCPMSP's cell under this project's writer paths (PRD v0.4
  C4); it opens no NFRA_MCPORTAL cell.
