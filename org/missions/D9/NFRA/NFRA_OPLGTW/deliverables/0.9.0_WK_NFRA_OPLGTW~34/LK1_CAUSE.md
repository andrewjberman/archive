# LK1_CAUSE -- audit/dt=2026-10-07/-321b3117.jsonl

Object readable: yes (one read, 557 bytes, one JSON line; temp copy outside the repo, deleted). No field value recorded here.

- `tool` name: NONE. The record has no `tool` field.
- Field NAMES: request_id, caller_capability_label, delegated_identity_ref (an object), operation, item_id, sheet,
  snapshot_id, etag, observed_at, result, latency_ms.
- Time field: `ts` is ABSENT (not empty). `observed_at` is present and non-empty, but `_emit` reads only `ts`.
- Writing function: `_audit` in `infra/aws/ec2/opal-gateway/app/taxsma_workbook.py` line 491 (the `audit._emit({...})`
  call at line 492), which builds a record without a `ts` field and hands it to `_emit` (app/audit.py).
- Key builder (before the fix): `_emit` in `app/audit.py`, `ts = str(record.get("ts", ""))` then
  `key = f"audit/dt={day}/{ts}-{id}.jsonl"` gave an empty time part for a record with no `ts`.
- Caller without a time field: yes (`_audit` in taxsma_workbook.py). NOT fixed: not a one-line change (the record's
  fields are not to change, and adding `ts` would add a field to the record). The writer fix covers it.
- Fix: `_lake_key` in `app/audit.py`; a record without a usable `ts` is keyed with the writer's current UTC isoformat time.
