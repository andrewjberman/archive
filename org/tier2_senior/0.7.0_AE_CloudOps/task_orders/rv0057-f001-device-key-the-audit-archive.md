# TO — device-key the audit evidence base (RV-0057 F-001 mechanism half)

<issued_to>0.7.0_AE_CloudOps (laptop) — ROUTE (i), base-CTO-routed 2026-08-06T0056Z. **ACCEPTANCE IS A
TWO-SEAT HANDSHAKE, NOT A SOLO TO:** ACs 1 and 4 (site-Z `--dry-run` + mint) and AC 3's cross-device
count require a `~Z` seat, which `2.0.0_SA_COO` is seating. SoD preserved: `1.0.0_SA_CTO` is the gate
and is not the builder. ACK'd to base CTO 0048Z naming this file, per the ADDRESSING clause below.</issued_to>
<issued_by>1.0.0_SA_CTO~Z (gate owner for audit-archive-invoker; RV-0057 F-001 names 1.0.0_SA_CTO for the mechanism)</issued_by>
<date>2026-07-29</date>
<status>pending — laptop-side build ASSIGNED + IN PROGRESS 2026-08-06; site-Z verification half seated by COO</status>
<go>**ORDERING GATE: DISCHARGED 2026-07-29 ~2345Z.** The reader guard (RV-0057 F-001 item 1) landed
at `b0b51cd47` — `/mstr-review` Step 2 now prints its device set and renders
`OVERRIDE_COUNT: UNMEASURABLE` when `walked ⊂ declared`. MSTR extended it to the Tier-1 liveness
check as well, correctly: that check's prescribed remedy is `spawn-agent.ps1`, so a false negative
there **writes to production**. Extension accepted, not vetoed. §7's safety ordering is satisfied and
this spec is build-ready.

**ADDRESSING — CORRECTED AGAINST MYSELF. This file was authored as a site-Z dispatch to a laptop
serial, and that is a standing-order violation I should not have written.** Andrew-direct
2026-07-29 ~1815Z, verbatim: *"you do not send work to the main fabric, no need. you can simply run
these projects off your own ~Z spawns."* Site Z does not route work to main-fabric serials; the
cross-device bus is **coordination-only**. No dispatch was ever sent (MCP does not cross devices and
I never claimed delivery — Rule 22b), so nothing acted on it; but an artifact addressed as a
dispatch is a violation waiting for a reader to honour it.

**So this is a SPECIFICATION in the shared record, not an order from this device.** Two legitimate
routes, and neither is mine to pick unilaterally:
  (i) **base `1.0.0_SA_CTO` / `2.0.0_SA_COO` issue it on the laptop** to `0.7.0_AE_CloudOps` — normal
      main-fabric routing, by the hand that is allowed to do it; or
  (ii) **a site-Z `~Z` AE lane builds it** off a site-Z spawn, which is what Andrew's order actually
      points at. **SoD constraint if so: I am the GATE for this instrument and must not also be the
      builder** — the gate does not review its own hand.
Whoever takes it: ACK by MCP to `1.0.0_SA_CTO` (base) naming this file, so the record has a receipt
rather than an assumption.</go>
<project>RV-0057 F-001 / F-002 remediation. No project code registered — the review finding is the
tracker, and a second tracker for a one-file change is drift, not coverage.</project>

## WHY (the one-line version)

`.tools/audit-archive-invoker.py` keys the archive on `(timestamp, logical-log)`. That tuple stopped
being unique when the fabric acquired a second device. Site Z's audit evidence has no slot in the
shared record, and the shared record carries no marker that a second device exists.

**Read `docs/architecture/NFRA_AUDITDEV_PRD.md` before you open the file.** It carries the grounding,
the measured numbers, and two things you would otherwise re-derive: a corruption hypothesis I
**refuted** at source (§4 — the `935ca2a7d` per-log pin already closes it, so do not build against
that threat), and a defect not in RV-0057 (§5 — the self-test's flagship positive control cannot
fail on a non-minting device).

## BUILD TO THIS

    org/audit/archive/<TS>/<flattened-log>          -- today
    org/audit/archive/<DEVICE>/<TS>/<flattened-log> -- target

1. **`<DEVICE>` resolves from a committed device registry**, never from `hostname`, `platform.node()`,
   or a path heuristic. An **unregistered device fails closed**: detection still runs and still
   reports; minting refuses with a named outcome. A device nobody declared must not be able to enter
   the evidence base silently.
2. **`.baseline` goes per-device** → `archive/<DEVICE>/.baseline`. Each chain becomes independently
   append-only-checkable. This is what kills F-002's false `NON-APPEND-EDIT` batch **by
   construction** — no device ever diffs against a foreign baseline again.
3. **`FINDINGS.md` entries carry `<DEVICE>`.** They already leak it, by accident and only on failure:
   a live entry today reads `live missing: C:\Users\Opal Bloomberg\Desktop\ajb_workspace\org\surface-check-ack-audit.log`
   — a site-Z absolute path in the shared record, inside a finding that claims a fabric-wide event.
4. **`MANIFEST.txt` stays global.** The covered set is a fabric property. A log absent on one device
   is a `COVERAGE` finding **scoped to that device**.
5. **Migrate the existing chain under `<DEVICE>=laptop` wholesale.** It is laptop-authored
   (`2026-07-29T185938Z` by `1.0.0_SA_CTO~A`, growing monotonically from `2026-07-28T125858Z`).
   `S1_TS` stays the never-a-baseline positive control **for the laptop chain only**.
6. **Each new device chain needs its OWN generated positive control**, not an inherited one. Per
   PRD §5, CONTROL-A returns `NON_APPEND` for *any* site-Z state, so it passes vacuously there and
   `SELF-TEST: PASS` certifies health on a structurally blind device. A hand-inherited control
   measures the author; a generated one measures the instrument.

## DO NOT

- **Do not implement F-002's stated remedy** ("suppress or device-scope the INTEGRITY clause").
  Device-scoping is items 1–3. **Suppression is not** — it deletes a real tamper detector to silence
  a keying bug, and it is under-scoped besides: **5 of today's 11 findings are `COVERAGE`, not
  `INTEGRITY`**, and false-fire by the identical mechanism. Fix the key; keep every detector.
- **Do not track any live high-churn log.** The 07-16 rationale holds: `safe-commit.sh:338` appends
  to `git-author-override-audit.log` *during* the commit, so tracking it dirties every commit's own
  tree and manufactures conflict surface under NEVER#7.
- **Do not build an alarm, alert, SNS topic, SES send, or freshness checker.** Standing moratorium,
  Andrew-direct 2026-07-28. This is a keying fix to a local verifiability instrument.
- **Do not widen `kill-orphans`-style sweeps or add a reaper.** Nothing here needs one.

## <compiler_tools_mandate>
<phase id="1" when="before write">
- `comp-blast audit-archive-invoker` — enumerate every caller. `org/XXX.md` A.2 invokes it at every
  agent's startup; treat that as a live call site with fabric-wide blast radius, not a dev script.
- `git ls-files -- 'org/audit/archive/**' | wc -l` — **print the denominator** of what the migration
  moves before moving it.
  **⚠ RE-DERIVED 2026-08-06T0055Z (`0.7.0_AE_CloudOps`, CTO-ordered before build): the count is now
  241 TRACKED under `org/audit/archive/**`, of which 238 are SNAPSHOT FILES** (excluding
  `MANIFEST.txt` / `FINDINGS.md` / `.baseline`). **The `175 at f35e69bd8` figure below is STALE — it
  has grown by ~38% and nobody should size the migration off it.** Kept visible rather than deleted so
  the drift itself is on the record: a hand-copied count inside a TO ages exactly like the hand-copied
  counts CLAUDE.md warns about, and this one aged 7 days. Re-derive again at build time; do not trust
  241 either.
</phase>
<phase id="2" when="before commit">
- `python .tools/audit-archive-invoker.py --self-test` → must be `PASS`, **and** the new per-device
  generated control must be among the controls that ran. A `PASS` whose control set did not grow is
  the §5 defect surviving the fix.
- `python .tools/audit-archive-invoker.py --dry-run --json` on **this** device → the 5
  `NON-APPEND-EDIT` and 3 `ERROR-FAILCLOSED` findings must be **gone**, and the 3 `COVERAGE` findings
  must remain, now device-scoped. Removing the COVERAGE three too means you suppressed rather than
  keyed.
- `.tools/commit-gate.sh` on the `.py` (Rule 14).
</phase>
<phase id="3" when="after commit">
- Re-run `--dry-run` on **both** devices and paste both outputs into the session log. A one-device
  verification of a two-device fix is the exact defect this TO closes.
</phase>

## <cross_domain_coordination>
- **`0.0.0_AB_MSTR`** — owns the reader guard (item 1) and `/mstr-review`. **This TO is gated behind
  that landing.** Also owns `org/tier0/**`, so the RV-0057 corrections in the PRD are theirs to fold,
  not mine.
- **`3.0.0_SA_CVO`** — owns the RV-0057 laptop re-walk (item 3); consumes both chains once this lands.
- **`1.0.0_SA_CTO`** (base, your device) — gate. Arch questions route there; I am reachable only via
  git from site Z.
- **Shared file:** `org/audit/archive/**` is the GOVERNANCE_AUDIT lane (MSTR + execs). The migration
  is a large tracked-file move — coordinate the window so it does not collide with a live mint.
</cross_domain_coordination>

## <acceptance_criteria>
1. `python .tools/audit-archive-invoker.py --dry-run` on **site Z** reports **0** `INTEGRITY`
   findings (both `NON-APPEND-EDIT` and `ERROR-FAILCLOSED` at zero) and retains device-scoped
   `COVERAGE` findings.
2. `python .tools/audit-archive-invoker.py --dry-run` on **the laptop** reports **0** `INTEGRITY`
   findings — i.e. the migration did not break the chain it moved.
3. `git ls-files -- 'org/audit/archive/laptop/**' | wc -l` equals the pre-migration
   `git ls-files -- 'org/audit/archive/**'` count minus the non-snapshot files
   (`MANIFEST.txt`, `FINDINGS.md`, `.baseline`). **No snapshot file lost in the move** — assert the
   number, do not eyeball the tree.
4. A site-Z mint produces `org/audit/archive/sitez/<TS>/` containing site Z's **own** live logs, and
   leaves `org/audit/archive/laptop/.baseline` **unchanged** (`git diff` empty on that path).
5. `--self-test` is `PASS` **and** its control log names a per-device generated control.
6. An **unregistered** device fails closed: minting refuses with a named outcome, detection still
   reports. Exercise this with a fabricated device id — a fail-closed path never exercised has never
   been tested.
7. Session log with a populated `## Compiler Tools` section + the `org/compiler-tools-log.md` row.
</acceptance_criteria>

## NOT IN SCOPE

- The reader guard (`/mstr-review` Step 2) — `0.0.0_AB_MSTR`, and it lands **first**.
- The RV-0057 laptop re-walk — `3.0.0_SA_CVO`.
- `org/ws-charter-hard-block-audit.log` is tracked with **no `!` rule** in `.gitignore` (it survives
  only because tracking outranks ignoring). Real, small, and **not yours** — surfaced to base CTO.
- `install-headmove-guard.sh` is the 1 of 8 installers unwired on site Z. Surfaced, not fixed here.
