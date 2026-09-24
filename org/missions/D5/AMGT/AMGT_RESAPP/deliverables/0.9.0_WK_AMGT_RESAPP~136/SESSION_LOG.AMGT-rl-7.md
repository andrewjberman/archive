SESSION LOG -- 0.9.0_WK_AMGT_RESAPP~136 on AMGT_RESAPP.TO-AMGT-rl-7 (Posture: the verdict as a headline
tile, the reasons as numbered cards with cites folded, an unresolved cite as an icon beside navy text)

worktree C:/tmp/wk-amgt-37-136, branch wk-AMGT_RESAPP-136-portal; outer branch wk-AMGT_RESAPP-136
(portal_ref 513bb3c5, node_modules linked).

1. Tree check: `git rev-parse --abbrev-ref HEAD` -> wk-AMGT_RESAPP-136-portal is the PORTAL branch (the
   outer worktree resolves the outer branch name separately, standard for this nested-repo setup);
   TREE-OK; INSTRUMENT-OK (portal/scripts/ui-class-census.mjs present).
2. Premises re-grounded: read `portal/src/pages/SecurityAnalysis/tabs/PostureTab.tsx` (393 lines, the
   AMGT-rj-12 build, Panel variant="mixed", 29-35 forbidden idioms per ui-class-census.mjs) and
   `postureCites.ts` (already idiom-clean, 223 lines). Confirmed `posture.harness.cjs` ENOENTs at DEV
   HEAD c1ac41ec on `.scratch/posture_BABA_US_Equity.json` in this fresh worktree, as the cell's note
   warned. Read the S3 objects live: `.tools/aws s3 ls s3://opal-data-harvest/posture/v1/ --recursive`
   still carries `BABA_US_Equity/2026-09-15.json` (19515 B) and `BA_US_Equity/2026-09-15.json` (21419 B)
   at the same bytes worker ~18 fetched by hand for rj-12 (sha256 match: c250400d..., d7b2426e...); also
   noted HD_US_Equity now carries a LIVE posture object (2026-09-16, unrelated to this cell) -- confirmed
   IRRELEVANT to the harness's no-object arm because that arm reads a TEMPORARY LOCAL POOL that never
   gets an HD_US_Equity entry, never the live bucket directly.
3. Root cause of the ENOENT: posture.harness.cjs's docstring already described "the two O-1 objects
   fetched from s3://... into <workspace>/.scratch/posture_<KEY>.json" but no code in the file performed
   that fetch -- SESSION_LOG.AMGT-rj-12.txt step 2 shows the previous worker fetched them BY HAND
   (`.tools/aws s3api get-object`) before ever running the harness. Fixed by adding a python/boto3
   fetch step (list under each key's prefix, newest date wins, GET, write to .scratch/) directly inside
   posture.harness.cjs, ahead of the .scratch read loop; the harness's ARMS (served/no-object/emptied/
   refused) and EXPECTATIONS (the 32 named checks) were not touched. Verified with a clean .scratch:
   ENOENT before, CHECKS-OK 32 of 32 rc=0 after, on three separate runs.
4. PostureTab.tsx rewritten to portal/DESIGN.md's light contract (C3/C6/C9/C11/C12), matching the
   ratified `Panel variant="nested"` + dark `PanelHeader` pattern already live at
   `InvestorReporting/export/ExportModal.tsx` (PanelHeader.tsx is unconditionally dark -- not in this
   cell's <paths> -- and this precedent shows that combination is the accepted shape, not a defect to
   route around). Verdict tile (13px/700 label via MachineMarker, 1.5169rem/700 navy value, a navy
   comparable link + as-of beside it); basis claims as pillar-cards (`rounded-[4px] border
   border-[hsl(var(--hairline))]`, a navy numeral header strip, no shadow anywhere); a native
   `<details>`/`<summary>` "cites N" disclosure per card, collapsed by default (verified: no `open`
   attribute emitted, and SSR still serialises the full child markup regardless -- confirmed by the
   harness's own countOf checks passing); a resolved cite's `text` (postureCites.ts UNCHANGED, byte-
   identical to HEAD) is split PRESENTATION-ONLY on the trailing `: "..."` quote and a leading `(accession
   ...)` clause so the quote renders at body size and the accession at footnote size, with the whole
   original string still rendered verbatim for any cite kind that carries no quote; an unresolved cite
   keeps the exact `cite not resolved -- <reason>` text (posture.harness.cjs's `unresolvedSaySo` check
   depends on this literal) and adds a `lucide-react` `AlertTriangle` icon (`data-cite-icon="warning"`,
   `text-[hsl(var(--status-warning))]`) with NO amber class anywhere in the file. The four states
   (`@/ui/components/states`: PanelEmpty/PanelLoading/PanelError) replace the old bare `<p>` renders for
   no-securityKey, NOT_READ, READ_FAILED and ABSENT (C12). The FWD-19 disclaimer sentence moved to
   PanelHeader's `subtitle` ONCE; the served object's own duplicate `notice` field (which restates the
   same opening clause -- confirmed on the live BABA_US_Equity/BA_US_Equity objects) is no longer echoed
   on the tile, so the sentence never prints twice (measured: 0 occurrences before this fix, since the
   `notice` field renders whenever present and both real objects carry it).
5. `usePeerSet`/`useThesisBundle` calls for subject then comparable (PostureTab.tsx today's :339/:347,
   now inside `PostureTab`) are BYTE-IDENTICAL to the pre-edit code -- confirmed by diff against the
   pre-edit file beyond the two renamed helper extractions (`verdictWord` is NEW and ADDITIVE,
   `postureVerdictSentence` untouched).
6. Instrument: `portal/src/pages/SecurityAnalysis/__harness__/posturePattern.harness.cjs` (NEW), same
   fetch-then-pool technique as posture.harness.cjs, real `read_posture('BABA_US_Equity')` (6 basis
   claims, 17 cites, 2 real unresolved E: cites -- no cite fabricated) and the real no-object
   `read_posture('HD_US_Equity')` over the SAME temporary pool (which never gets an HD_US_Equity entry).
   13 checks, all 13 named in the task order's own AC1 text (see row AMGT_RESAPP-W136-S1: the same
   sentence names 13 checks but states "CHECKS-OK 12 of 12" -- built all 13, true count reported).
   Two debugging false negatives before green, both root-caused and fixed:
     - `machine_sentence_once` read 0: react-dom/server HTML-escapes the apostrophe in "machine's" to
       `&#x27;s`; the check's literal needle carried a raw apostrophe. Fixed the needle to the escaped
       form (verified against a two-line node repro of `renderToStaticMarkup` on the literal string).
     - `unresolved_cite_icon_not_amber_text` read false: the `AlertTriangle` SVG's opening tag (path
       data, `xmlns`, `viewBox`, etc.) pushed `data-cite-icon="warning"` past a 400-character window from
       the `data-cite-resolved="false"` split point; widened to 800 (measured actual offset: 434).
   Verified: mutant control (below), determinism control (below), and a clean re-run with debug output
   removed: CHECKS-OK 13 of 13, exit 0, three separate runs.
7. Controls.
   MUTANT: temporarily replaced the warning icon's colour class with `text-amber-300` in the committed
   PostureTab.tsx and re-ran `ui-class-census.mjs` -- idiom count went 0 -> 1 (FIRED-AS-EXPECTED). Reverted
   via `git checkout --`; content-equality to the pre-mutation file confirmed by a newline-normalised
   read (the raw `diff` disagreed only on CRLF/LF, not content -- `git status --porcelain` reported CLEAN
   and `ui-class-census.mjs` reported idiom=0 again after revert).
   DETERMINISM: two back-to-back runs of posturePattern.harness.cjs, CHECK/CHECKS-OK lines diffed --
   identical.
8. Criteria run under their bounds (timeout 120), exact invocations, from a clean `.scratch`:
   AC1 `node src/pages/SecurityAnalysis/__harness__/posturePattern.harness.cjs` -> CHECKS-OK 13 of 13,
   exit 0. AC2 `node scripts/ui-class-census.mjs .../PostureTab.tsx .../postureCites.ts` -> both files
   idiom=0 size=0 weight=0 radius=0 shadow=0, FILES 2 TOTAL 0. AC3
   `node src/pages/SecurityAnalysis/__harness__/posture.harness.cjs; echo "exit=$?"` -> CHECKS-OK 32 of
   32, exit=0 (the two S3 keys and byte sizes print inside the JSON `objects` block: BABA_US_Equity
   19515 B, BA_US_Equity 21419 B, both from posture/v1/<key>/2026-09-15.json).
9. `tsc --noEmit -p tsconfig.app.json` clean (no output, rc 0) after the rewrite. No install run; no vite
   dev server; no vendor/Bloomberg call; the harnesses' only network act is the two declared S3 GETs.
10. Portal commit b5ed3a05 (branch wk-AMGT_RESAPP-136-portal, on 513bb3c5); one surprise row filed
    (AMGT_RESAPP-W136-S1, OBSERVATION/INERT) for the AC1 text's own 13-named-checks-vs-"12 of 12" count
    mismatch -- built all 13, did not drop one to force the literal count.

Bound respected: `postureCites.ts` is UNCHANGED (byte-identical to HEAD at every commit in this session --
its resolution, the bundles it reads and the counts it reports are all KEPT); `IdentityLine`,
`CheckFaceBadge` render unchanged (only `IdentityLine` is actually used on this tab, same call site, same
props); `PeersTab.tsx`, `src/ui/**`, `src/components/**`, `src/api/**`, `lib/research/api/scoped_amgt.py`
not touched. REFUSE, not rescue: no install, no vendor call, no S3 write/delete, no key hunting.
