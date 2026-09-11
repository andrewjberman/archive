# Session log -- `0.9.0_WK_IRPT_BCKEND~3` on `IRPT_BCKEND.TO-IB-s-6`

Worktree `/c/tmp/wk-irpt-1-3`, branch `wk-irpt_bckend-1-3`, re-cut from `95a34541f8`. Second order
in slot ~3, handed over after IB-s-8 drained and IB-s-5 merged.

## Order of acts

1. **The bar.** `git rev-parse --abbrev-ref HEAD` -> `wk-irpt_bckend-1-3`, HEAD `95a34541f8`;
   `test -d org && test -d .tools` -> `TREE-OK`; `_gate/gate.py` and the intake skeleton present.
   Wrote the gitignored `org/mcp/sessions/<session>.serial` before any apply.
2. **Re-grounded every premise the face names, before building.**
   - `_gate/gate.py` -- the four outcomes of `bind_firm` are a closed set; `destination_for`
     refuses a cross-firm destination BEFORE a key is built. Called, never reimplemented.
   - `_keys/keys.py` -- `quarantine_key`, and `queue_message`'s CLOSED value grammar. The latter
     refused `req-...` as a parameter value, which is why the request id is minted `REQ-...`:
     the transport's own shape, not a reshaping at the boundary.
   - `core/firm_destination_policy.json` + `layout.json` -- three firms, their intake templates,
     `opal_domain`, the quarantine prefix. The enumeration is read, never retyped.
   - `core/dynamodb.tf` -- `irpt-checkpoints` (source, cursor), `irpt-jobs` with
     `lease_owner`/`lease_expires_at`/`fence_token`, `irpt-outbox` (tenant, seq). **No new table
     was needed for the cursor, the marks, the lease or the outbox.**
   - Live: 4 `irpt-*` tables, 6 queues, `opal-data-ycharts` all applied.
3. **THE PHASE-1 INSPECTION the decomposition required**, recorded at
   `intake/ib_s_6_graph_inspection.md`: 10 artifacts, ending in an UNSCOPED corpus census for
   `ApplicationAccessPolicy|client_credentials|app-only Graph|application permission`. The scoped
   read (the gateway) could only have told me about the gateway, which was the domain whose
   completeness was the question. VERDICT: the model is DELEGATED per-user; no mailbox-restricted
   application grant exists; `Mail.Read` exists only as a delegated scope; recorded **UNVERIFIED
   with exactly what was read**.
4. **Built** `poller.py`, `graph_client.py`, `checkpoint.py`, `outbox.py`, the synthetic fixture
   set with its own SYNTHESIZED manifest, and the offline suite with its network guard.
5. **Deployed in the bound's order.** Source committed first (`1e1aeb1de4`) so the artifact is
   built from committed bytes; ledger `irpt-bckend-s6` opened (6 legs); zip uploaded with its
   `content-sha256` metadata; `safe-apply` -> `7 added, 0 changed, 0 destroyed`; verified
   CodeSha256, `State: DISABLED`, `No changes.`; legs closed; **the close committed
   (`61fbbd22ae`) BEFORE the grading reads.**
6. **Graded.** `S6-AC1` -> `IBS6-INTAKE-DURABLE`, 7 of 7 arms, rc 0. `S6-AC2` -> `No changes.`, rc 0.
7. **Controls.** Two mutants (both fired; M2 produced 10 queue sends for 5 messages) and a
   determinism pair (88 lines, byte-identical).

## Two things that did not hold, both filed rather than worked around

- **`IRPT_BCKEND-W3-S3`** -- the per-firm `execution_role`s the policy names trust only
  `lambda.amazonaws.com`, on the DESIRED **and** the APPLIED plane, so no running function can
  assume one and an ingestion poller cannot be one function per firm. Repairing the trust policy
  would be an edit to IB-s-5's root, outside this order's write grant. The poller therefore runs
  under one role narrowed to the INTAKE prefix family.
- **`IRPT_BCKEND-W3-S4`** -- the sentinel was never committed in its OPEN state; the bound's two
  clauses cannot both be met for a one-turn deploy without a commit between the open and the
  close. The battery PRINTS the disclosure rather than leaving it to an absence.

## Instruments, and which are independent

- `comp-read` on `gate.py`, `keys.py`, `config.py`, `commit-gate.sh`, and `--enumerate` on the
  build script's pipeline handling -- which is how I learned the pipeline argument is matched
  against `tf_file` and is NOT a closed enumeration, so a premise I was about to file as a row
  was false and was not filed.
- `comp-find --corpus all` for the app-only Graph census (an unscoped read with its denominator).
- `comp-iam service` / `gaps` for the new role on the DESIRED plane.
- `comp-adversary compose` on the poller.
- **Arm (g) carries a positive control** because the recorded transport and the network guard are
  NOT independent in the direction that matters: the transport can only see what it was asked for.
- **Arms (a), (c) and (e) each carry their own negative arm** (a kill vs no kill; a second delivery;
  a cross-firm destination request), so no arm rests on a single positive observation.

## Bounds held

No live mailbox read; no live vendor call; the scheduler applied and left DISABLED; no monitor,
alarm, SNS or SES; no cross-firm reach (the poller can write only the intake family and
quarantine); no served output touched; no secret value read, printed or committed; every file
written is inside this order's `<paths>` grant or this worker's deliverables folder.
