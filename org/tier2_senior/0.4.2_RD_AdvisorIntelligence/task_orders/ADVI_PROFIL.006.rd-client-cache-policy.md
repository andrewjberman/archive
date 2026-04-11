<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-10-profil-cache-policy</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <date>2026-04-10</date>
    <status>complete</status>
    <project_code>ADVI_PROFIL</project_code>
  </metadata>

  <objective>
    Apply a client-data caching policy to the cache keys in `AdvisorBookView.tsx`, `AdvisorBookClientDetail.tsx`, and `AdvisorBookAccountDetail.tsx` based on an Andrew/COO decision from one of three options: (a) match existing 5-min stale, (b) PII-sensitive `staleTime: 30_000` `gcTime: 0`, (c) split — advisor-level book 5-min + client-detail `gcTime: 0`. This is a one-line change per affected key once the policy is chosen. Blocked on .001 + .005 + Andrew decision.
  </objective>

  <context>
    RD briefing §5.7 flagged that client data has different sensitivity than firm analytics. Andrew mentioned "different caching policy for client data" during the architecture discussion but did not commit to a specific value.

    Options:

    **Option (a) Match existing:** Advisor-level book cache + client-level cache both use `staleTime: 5 * 60 * 1000`, `gcTime` default (5 min). Fastest toggles. Data persists across advisor switches within 5 min. Risk: someone walking past an unlocked laptop can see cached client names/PII in React Query devtools or on a fresh render.

    **Option (b) PII-sensitive:** Both advisor-level and client-level cache use `staleTime: 30_000`, `gcTime: 0`. Instant eviction on unmount. Refetch on every reopen. Safer against walk-by exposure. Slower UX.

    **Option (c) Split level:** Advisor-level book stays at 5-min stale (matching the rest of the page for analytics continuity). Client-detail (L3 from .005) uses `gcTime: 0`, no persistence across unmounts. Account-detail (L4) same — `gcTime: 0`. This is the "right" answer if PII concern is primarily about client/account-level data rather than advisor roll-ups.

    **DECISION: Option (c) — split level.** Andrew confirmed via main chat on 2026-04-10, ~16:35 EDT, relayed by 0.4.0_DT_ClientPlatform. Advisor-level book `useQuery` stays at `staleTime: 5 * 60 * 1000` (matches page analytics continuity). Client-detail L3 (`AdvisorBookClientDetail.tsx`) and Account-detail L4 (`AdvisorBookAccountDetail.tsx`) use `gcTime: 0` with default staleTime, no persistence across unmounts. Rationale: treats PII sensitivity as a layered property rather than a blunt toggle; isolates walk-by exposure risk to the client/account layer where real names + account numbers live; scales cleanly for tighter-PII partner firms in the future without touching advisor-level caching.

    RD must also audit whether any other page-level cache key touches client-specific data and should follow the same policy (per the last paragraph of this context).

    The actual code change is trivial: per cache key in the AdvisorBookView flow, update `staleTime` and/or `gcTime` props in the `useQuery` call. Each key is one line.

    If option (c) is picked, RD must also audit whether any other page-level cache key touches client-specific data and should follow the same policy.
  </context>

  <compiler_tools_mandate>
    Phase 1 (before writing):
    - Verify .005 has landed in the portal DEV working tree (or on DEV branch if .005 has been committed).
    - Wait for Andrew/COO decision on a/b/c. Decision communication channel: broker message from COO or Andrew direct input. Do NOT guess.
    - `comp-cache` — list all cache keys under `portal/src/pages/AdvisorIntelligence/` and flag any that touch client-specific data. If option (c) is picked, all of them need review.

    Phase 2 (during implementation):
    - Update the affected cache keys per the decision. One line per key.
    - If option (c), also add a code comment at each updated key: `// Client-level PII: gcTime 0 per ADVI_PROFIL.006 decision (2026-04-{NN})`. Include the decision date.
    - Preserve the existing `refetchOnMount: false`, `refetchOnWindowFocus: false` behavior unless the decision explicitly changes them.

    Phase 3 (after implementation):
    - `bun run tsc -b` exit 0
    - `bun run eslint` clean
    - `comp-cache` re-run — verify the policy is applied consistently to the intended keys and no unintended keys were affected.
    - RD does NOT push. Hand off to DT for commit+push.
  </compiler_tools_mandate>

  <cross_domain_coordination>
    shared_resource: Cache keys in `AdvisorBookView.tsx`, `AdvisorBookClientDetail.tsx`, `AdvisorBookAccountDetail.tsx`. .005 creates them; .006 tunes them.
    last_write_owner: 0.4.2_RD_AdvisorIntelligence.
    required_action: "Wait for COO or Andrew to deliver the decision. Do NOT start until the decision message is in your inbox. Decision must be one of a/b/c verbatim — no partial picks or compromise options without explicit Andrew sign-off."
  </cross_domain_coordination>

  <acceptance_criteria>
    1. **Decision received:** Broker message from COO or Andrew direct specifies one of option (a), (b), or (c). Decision documented in the session log with the source message.
    2. **Cache keys updated:** Per the decision, every affected `useQuery` call has the correct `staleTime` and `gcTime`. One-line change per key.
    3. **Comments added:** If option (b) or (c), a code comment at each updated key explains the policy and cites ADVI_PROFIL.006 with the decision date.
    4. **Other behavior preserved:** `refetchOnMount: false`, `refetchOnWindowFocus: false`, and any other existing useQuery config is unchanged unless the decision explicitly overrides.
    5. **tsc + eslint clean.**
    6. **comp-cache confirms:** Only the intended keys are affected. No accidental widening.
    7. **Session log:** Documents the decision source (message SHA or Andrew quote), the affected keys, the before/after values, and the Compiler Tools section.
    8. **Handoff to DT:** Broker message to 0.4.0_DT_ClientPlatform.
  </acceptance_criteria>

  <scope>
    <files>
      <file action="modify">portal/src/pages/AdvisorIntelligence/AdvisorBookView.tsx</file>
      <file action="modify">portal/src/pages/AdvisorIntelligence/AdvisorBookClientDetail.tsx (from .005)</file>
      <file action="modify">portal/src/pages/AdvisorIntelligence/AdvisorBookAccountDetail.tsx (from .005)</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">Do NOT start until the decision is delivered. Do NOT pick a default and ship it.</requirement>
    <requirement id="2">The decision must be one of a/b/c verbatim. No partial or compromise options without Andrew sign-off.</requirement>
    <requirement id="3">One-line change per key. Do not refactor surrounding code.</requirement>
    <requirement id="4">Preserve all other useQuery config (refetchOnMount, refetchOnWindowFocus, etc.) unless the decision explicitly overrides.</requirement>
    <requirement id="5">Hand off to DT for commit+push. Do NOT commit or push yourself.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="code">Updated cache key config in 3 files (working tree, RD-authored, staged for DT pickup).</deliverable>
    <deliverable type="document">Session log at `org/tier2_senior/0.4.2_RD_AdvisorIntelligence/logs/2026-04-{NN}/advi_profil_006_cache_policy.md` with the decision source, the key diff summary, and the Compiler Tools section.</deliverable>
    <deliverable type="message">Broker message to 0.4.0_DT_ClientPlatform for commit+push.</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT start without the decision message in your inbox.</rule>
    <rule>Do NOT guess a default. Ask via broker message if the decision is not delivered.</rule>
    <rule>Do NOT refactor surrounding code. Strictly one-line-per-key.</rule>
    <rule>Do NOT commit or push.</rule>
  </do_not>
</task_order>
