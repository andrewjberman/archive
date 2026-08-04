# CRO State Contract — the anti-"remembering" surface

**Authority:** Andrew-direct 2026-08-04 (~1815Z, this session): formalize the process state
so counts/lists/queues are officially enumerated somewhere persistent instead of carried in
prose. Extends the estate law "a predicate is not a roster" (banked 08-04, CTO-ratified)
from tool universes to PROCESS STATE.

## The disease this contract treats

Ten measured instances in one night of a number or list carried in PROSE (handoff text,
commit subject, message body, informal artifact name) diverging from the committed truth:
CONTESTED-306 (non-rederivable), 7031-ARCHIVE (stale 17), ~1100-threads (1,064),
16-then-14 commits (unchecked filters), 337/228 subject (333/224), "DRY" (0+1-routed),
machine-table vs prose (71-vs-75), v2=e94cd09f (stamps said c4259ace), 75-tools (18 at
measure), 5715-MIGRATE (5,717). Root cause every time: **the number traveled without its
derivation.**

## The contract

1. **A count is a CACHED OBSERVATION, never a fact.** Every number recorded here carries
   its PREDICATE (the exact derivation command), its VINTAGE (HEAD short-sha + timestamp),
   and its OWNER. A reader re-derives; a writer never edits a cached count in place —
   append a fresh observation.
2. **Load-bearing state NEVER lives in the session scratchpad.** Derivation scripts,
   exclusion lists, queue state: committed here. The scratchpad holds only transient
   intermediates whose durable form is elsewhere (e.g. batch path-lists, whose durable
   copy is the BATCHES.jsonl row that hashes them).
3. **The artifact's own stamp outranks any name for it.** Model versions come from
   `model_version` fields inside prediction rows, never from filenames or recollection
   (the v2/c4259ace lesson).
4. **Prose numbers cite this surface or re-derive inline.** A handoff, commit subject, or
   MCP message quoting a count names the QUEUE entry or prints the fresh derivation. A
   bare number in prose is a defect under CLAUDE.md rule 24's spirit at process grain.
5. **Files here are append-only JSONL** (except this contract and README-grade docs) —
   last-row-wins per key, same convention as the rcg ledgers, so history is retained and
   the manifest/append-only discipline transfers.

## The files

| File | Contract |
|---|---|
| `QUEUE.jsonl` | open work items: `{key, predicate, last_observed:{value, head, ts}, owner, status, evidence}` — last-row-wins per key |
| `exclusions.jsonl` | paths excluded from CRO batch derivation: `{path, reason, routed_to, status, evidence, date}` — consumed by derivations/derive_batch.py |
| `derivations/` | the promoted derivation scripts (WS-anchored, output dir via RCG_OUT_DIR env, default system temp) — any session re-runs them identically |

## What stays OUT

Ledger truth (rcg/ledger/* is the authority for labels/batches/evals — this surface never
duplicates it); anything derivable in one command with no carried state; other agents'
lane state (their folders, their contracts).
