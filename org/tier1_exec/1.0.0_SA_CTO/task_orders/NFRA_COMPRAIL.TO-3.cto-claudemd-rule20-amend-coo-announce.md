<to_id>NFRA_COMPRAIL.TO-3</to_id>
<project>NFRA_COMPRAIL</project>
<title>CLAUDE.md Rule-20 amendment (comp-which-first + hive-brain why + permission/override convention) [CTO] + fabric announcement BEFORE the gate enables [COO]</title>
<assigned_to>1.0.0_SA_CTO (rule-amendment leg) + 2.0.0_SA_COO (announce-broadcast leg)</assigned_to>
<issued_by>2.0.0_SA_COO (PRD decomposition, 2026-06-18; hardened per CTO DELTA 49b236dea)</issued_by>
<issued_date>2026-06-18</issued_date>
<status>complete</status>
<!-- COMPLETE 2026-06-22: LEG A (ea0570377) + LEG B (COO announce broadcast to all 7 live agents) both done.
     Downstream TO-4 ENABLED + LIVE same day (3741da067 + 89217d3ad). -->
<!-- LEG A (CTO rule-amend) COMPLETE 2026-06-22, commit ea0570377: CLAUDE.md NEW Rule 21 (comp-which-first
     DEFAULT + hive-brain why + GATED-not-banned 3-surface model: Bash raw repo-grep/find + raw-aws-inspection
     deny unless inline `# rail-checked: <why>` marker [audited]; native Grep/Glob nudge-and-proceed [own light
     escape, Andrew 2026-06-22 'native escape is fine']; native Read + operational aws + pipe-greps free) +
     comp-grep/comp-glob row in the situation->command table. PRD reconciled to the same model (resolves the
     COO-flagged §4/§8 self-contradiction): §3 refinement banner + native row -> nudge-and-proceed; §8 harness-fit;
     §9 AC2. The OVERRIDE-MARKER single-source-of-truth = `# rail-checked: <why no comp-tool fits this exact search>`.
     Rule 21 IS the durable note (loaded every session) for sessions cycling in after the live broadcast.
     LEG B (COO announce-broadcast) PENDING -- dispatched to COO; fires BEFORE TO-4 enables. -->
<!-- TO stays pending until Leg B (COO announce) fires. -->

<priority>HIGH — announce-then-enforce (PRD rollout step 3). The gate (TO-4) must NOT be a surprise wall: every agent must know the comp-which-first rule + that native Grep/Glob is now GATED + the override-marker escape BEFORE enforcement. CTO rule-amend leg can begin in parallel with TO-2. COO announce-leg fires AFTER TO-2 (comp-which proven complete-enough) lands AND the CLAUDE.md amendment lands. GO'd NOW (CTO leg).</priority>

<references>
  <ref type="prd">docs/architecture/NFRA_COMPRAIL_PRD.md (49b236dea) — §2 (the hive-brain why), §3 (hardened table: native Grep/Glob GATED, Read FREER) + §3 Permission/override section, §6 rollout step 3, AC3</ref>
  <ref type="rule-of-record">CLAUDE.md Rule 20 (the dependency-graph / comp-tool rule) + the Compiler-Tools situation->command section + the NFRA_TOOLHUD comp-which note already there.</ref>
  <ref type="floor">c985b8d9e (FLOOR) + the NFRA_TOOLHUD HUD-hook note — the existing salience layer this amendment hardens into law.</ref>
</references>

<scope>
**LEG A — CLAUDE.md Rule-20 amendment (CTO, rule-author + the gate):**
Amend CLAUDE.md to document the HARDENED rule + the escape, so the fabric has the rule-of-record BEFORE the gate:
- comp-which / a comp-tool is the DEFAULT for every search + inspection; raw grep/aws + NATIVE Grep/Glob are the EXCEPTION — used ONLY when comp-which confirms no tool fits the exact use.
- The HIVE-BRAIN why (PRD §2, the load-bearing rationale): raw grep is text-local + connection-blind; in a coupled estate it MISSES connected things; the graph/comp-tools are the SHARED cognition substrate so every agent reasons from the SAME complete connected picture, not N private grep-views. A native grep is "leaving the shared brain" — a rare, justified, on-record exception.
- The HARDENED 3-surface model (PRD §3): HARD-BLOCK raw-aws-INSPECTION + repo-file-grep in Bash; **native Grep/Glob now GATED (deny-by-default + permission/override)** — NOT mandate+nudge anymore; native **Read FREER** (not gated — reading a known file is not a search); EXEMPT operational aws + pipe-greps.
- The PERMISSION/OVERRIDE convention (PRD §3 permission section): the auditable override-marker (e.g. trailing `# rail-checked: <why no comp-tool fits this exact search>`; exact convention from the TO-4 build) IS the scalable "ask permission for a turn of grep" — deny-by-default, proceed only with the logged justification; a REPEAT override for the same intent = coverage-gap -> build the tool. (Optional true human-ask `permissionDecision:"ask"` is wired only for Andrew's own interactive sessions.)
Keep it to CLAUDE.md rule-shape (imperative + gate + PRD pointer; the why/history lives in the PRD §2). CTO owns the rule wording + the gate.

**LEG B — fabric announcement (COO, the announce-broadcast — MY leg):**
Broadcast to EVERY live agent (+ a durable note for sessions that cycle in later) BEFORE the gate enables:
- The comp-which-first rule is now law + the hive-brain why (cite the amended CLAUDE.md Rule 20).
- The HARDENED model: native Grep/Glob is now GATED (not just nudged) — what will deny soon (raw-aws-inspection + repo-file-grep in Bash, THEN native Grep/Glob LAST) vs what stays free (native Read, operational aws, pipe-greps).
- The override-marker escape — exactly how to proceed when comp-which confirms no tool fits (deny-by-default + the logged marker), so no one is surprise-walled or stalled.
- WHEN enforcement lands (after TO-2 proven-complete + this announce; TO-4 is the enable, native LAST).
The announce is the "no surprise wall" guarantee — it MUST precede TO-4. Given native Grep/Glob gating is a big behavior change for every agent, the announce must be especially clear on the override mechanics.
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before the announce (COO leg)">
    <step>
      <run>comp-which against a sample of the real high-traffic intents the announce will tell agents to use (IAM / gold-id / S3 served key / portal data props / a deliberately tool-less search) — confirm the rail ROUTES or RUNS-the-primitive (never dead-ends) AND is proven complete-enough (TO-2 accepted)</run>
      <expect>comp-which answers each — TO-2 has landed + proven complete-enough — so the announce points agents at a rail that actually works for the searches they'll be gated out of. If TO-2 not yet accepted, HOLD the announce leg.</expect>
      <if_mismatch>Do NOT announce "native grep is gated, rely on comp-which" until TO-2 confirms the rail is proven complete-enough. The announce HARD-gates on TO-2 — else agents get walled with no working alternative.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="CTO rule-amend leg, before commit">
    <step>
      <run>safe-commit surface-check + a read-back that the amended Rule 20 states default/exception + the hive-brain why-pointer + the hardened 3-surface model (native GATED, Read FREER) + the permission/override marker, in rule-shape</run>
      <expect>Rule reads as law, points to PRD §2 for the why, names the override-marker, and is explicit that native Grep/Glob is now gated (the change agents most need to know). No prose bloat.</expect>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
- **HARD land-order (CTO DELTA, firm):** TO-2 (comp-which proven complete-enough) lands -> CLAUDE.md amendment (Leg A) lands -> COO announce (Leg B) fires -> ONLY THEN TO-4 (gate) enables, native Grep/Glob LAST. The announce is the gate between "documented" and "enforced." Do NOT let a gate-tier start before its rail-coverage is proven.
- **CTO (Leg A) + COO (Leg B) split:** CTO owns the rule wording + the gate; COO owns the broadcast + the durable note. The override-marker exact convention is defined in the TO-4 build; the rule + announce must quote the SAME marker (single source of truth).
- **Whole-fabric audience:** native Grep/Glob gating changes EVERY agent's search reflex — the announce touches the whole fabric (why it's a COO leg). One broadcast + a durable doc/registry note for later-cycling sessions.
- **TO-4 (CTO) reads this as its gate** — TO-4 verifies the announce fired before enabling any deny, and native Grep/Glob enables only after TO-3 + the coverage-proof.
- **PRD CLEANUP (flag to CTO):** PRD §4 last sentence + §8 "Harness-fit" line still say "native Grep stays the sanctioned fast path (mandate+nudge, not blocked) / never block native Grep" — stale leftovers contradicting the hardened §3 table + AC2. Reconcile so the rule + announce don't quote the stale framing.
</cross_domain_coordination>

<acceptance_criteria>
- AC3 (PRD §9): CLAUDE.md Rule 20 amended (comp-which-first default/exception + hive-brain why + hardened 3-surface model with native Grep/Glob GATED + Read FREER + permission/override convention) AND the fabric announced BEFORE the gate enables.
- The announce names: the rule + the hive-brain why, what gates (incl. native Grep/Glob, enabling LAST) vs what stays free (Read, operational aws, pipe-greps), the override-marker escape mechanics, and the enable-timing — so no agent is surprise-walled or stalled.
- The override-marker quoted in the rule + announce MATCHES the marker TO-4 implements (single source of truth).
- A durable note exists for sessions that cycle in after the live broadcast.
- The 2 stale PRD sentences (§4 / §8) flagged to CTO for reconcile.
- Session logs (both legs) reproduce the Compiler Tools `<run>` checks with pass/fail.
</acceptance_criteria>

<data_reprocess_scope><no_reprocess_needed>Documentation (CLAUDE.md) + a fabric broadcast. No code, no served artifact, no pipeline.</no_reprocess_needed></data_reprocess_scope>
