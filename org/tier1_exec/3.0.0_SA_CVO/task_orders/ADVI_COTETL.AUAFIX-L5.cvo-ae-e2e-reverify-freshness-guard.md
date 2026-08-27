<to_id>ADVI_COTETL.AUAFIX-L5</to_id>
<project>ADVI_COTETL</project>
<title>Comprehensive end-to-end re-verify + standing cot-AUA-freshness guard (the closeout cert)</title>
<assigned_to>3.0.0_SA_CVO (cert lead) + 0.7.0_AE_CloudOps (AE side)</assigned_to>
<issued_by>2.0.0_SA_COO (AUAFIX PRD decomposition, 2026-06-18; CTO PRD ef04a08cc)</issued_by>
<issued_date>2026-06-18</issued_date>
<status>complete -- SPRING-CLEAN 2026-08-25: closed WITH its project ADVI_COTETL, which was closed the same day for having no directive attachment. Closed as a record act, not a work verdict; the work is recoverable by re-minting the project. Prior status: staged</status>
<priority>MEDIUM -- the CLOSEOUT gate. GATED on L1-L4 landing. CVO certifies. No leg self-reports DONE; L5 is the independent end-to-end re-verify on the SERVED artifacts + the standing guard that makes a future freeze impossible-to-be-silent.</priority>

<references>
  <ref type="prd">docs/architecture/ADVI_COTETL_AUAFIX_PRD.md (ef04a08cc) -- §5 L5, §6 closeout, §7 AC5</ref>
  <ref type="verify-discipline">verify-channel discipline: read the SERVED artifact / live state, never self-report / rc=0. The 4-check + sharpest-test-binds.</ref>
</references>

<scope>
Once L1-L4 land, independently re-verify the WHOLE fix end-to-end + stand up the guard:
1. **Chain fires** (L1): the cot silver->gold->AUA chain fires on a real nightly; AUA data_as_of advances. Verified on SERVED artifacts.
2. **Basis current-or-correctly-held** (L2): the AUA basis is either current OR documented correctly-periodic-by-design with honest served-cadence (per the CTO determination). NOT a silent stale-implying-fresh.
3. **firm_id correct** (L3): all cot served JSONs carry firm_id=cottonwood, 0 residual.
4. **Alert delivers** (L4): a synthetic freeze fires a DELIVERED alert (Delivered>0, not publish-accepted); cot AUA has a live freshness oracle.
5. **Standing AUA-freshness guard:** the oracle + alarm registered as a CRITICAL-SURFACE (comp-surface-check / critical-surfaces.yaml + the critical-paths ledger) so cot AUA freshness is a must-always-be-right surface going forward. CVO certifies the guard is live + fires.
CVO cert = the close-gate. AE side = the infra/alarm/oracle verification support.
</scope>

<compiler_tools_mandate>
  <phase id="1" when="the end-to-end re-verify">
    <step>
      <run>Per-leg SERVED-artifact verification: comp-pipescript deployed cot (chain) + read served AUA data_as_of (L1) + the basis as-of vs CTO cadence ruling (L2) + firm_id on all served JSONs (L3) + synthetic-freeze NumberOfNotificationsDelivered>0 (L4)</run>
      <expect>All four legs verified on SERVED/live state, not self-report. Any leg that only self-reports DONE is REWORK.</expect>
      <if_mismatch>Any leg failing its served-artifact check -> route back to that leg's owner; L5 does not certify until all four are served-verified.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="the standing guard">
    <step>
      <run>comp-surface-check (register cot AUA freshness as a critical surface) + verify the guard fires on a synthetic freeze (oracle flags stale + alarm delivers)</run>
      <expect>cot AUA freshness is a live critical-surface with a delivering alarm -- a future freeze cannot be silent. Guard certified.</expect>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
- **GATED on L1-L4** -- L5 is the closeout; it certifies only after all four legs land. Coordinate with each leg owner (L1 AE+DS, L2 DS+AE+CTO-cadence, L3 DS, L4 AE) for the served-artifact evidence.
- **CVO independence (Art. XIV):** L5 is CVO's independent re-verify -- not a rubber-stamp of the leg owners' self-reports. Sharpest-test-binds.
- **Standing guard ties to critical-surfaces** (comp-surface-check / critical-surfaces.yaml / critical-paths ledger) -- the no-silent-freeze-again structural backstop.
- **CVO #9 nightly served-verify** (NNA+COTETL, tomorrow-AM) is CVO's adjacent event-gated work -- L5's chain-verify can ride the same nightly review.
</cross_domain_coordination>

<acceptance_criteria>
- AC5 (PRD): CVO end-to-end re-verify GREEN (chain fires + basis current-or-correctly-held + firm_id correct + alert delivers -- all on SERVED/live state) + the standing AUA-freshness guard LIVE (oracle + delivering alarm as a critical-surface).
- No leg accepted on self-report -- every leg served-artifact-verified.
- The guard demonstrably fires on a synthetic freeze (a future multi-day freeze cannot be silent).
- Session log Compiler Tools section reproduces every `<run>` with served-artifact evidence + pass/fail; CVO cert recorded.
</acceptance_criteria>

<data_reprocess_scope><no_reprocess_needed>Verification + a standing freshness guard (oracle + alarm + critical-surface registration). No served-data reprocessing.</no_reprocess_needed></data_reprocess_scope>
