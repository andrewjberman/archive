"""Planted defect for OG-en-15 (control only; the committed tree is unchanged): the superseded A1 rule, a second row with a
transaction_id already seen in the window is dropped. transaction_id is not a row key, so this loses real rows.
Loaded with pytest -p from the gateway directory."""
from app import client_adapter_bd49f as bd

_orig_read = bd._window_read


def _tid_rule(ctx, prefix, plan, columns):
    rows, partition_rows, excluded = _orig_read(ctx, prefix, plan, columns)
    seen, kept = set(), []
    for row in rows:
        tid = row.get("transaction_id")
        if tid is not None:
            if tid in seen:
                continue
            seen.add(tid)
        kept.append(row)
    return kept, partition_rows, excluded


bd._window_read = _tid_rule
