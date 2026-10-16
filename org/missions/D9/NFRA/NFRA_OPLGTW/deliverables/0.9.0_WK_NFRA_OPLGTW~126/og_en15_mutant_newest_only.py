"""Planted defect for OG-en-15 (control only; the committed tree is unchanged): an increment window reads only the newest
partition of the window, the one-partition behaviour OG-en-15 replaces. Loaded with pytest -p from the gateway directory."""
from app import client_adapter_bd49f as bd

_orig_plan = bd._window_plan


def _newest_only(ctx, prefix, semantics, start, end, as_of):
    plan = _orig_plan(ctx, prefix, semantics, start, end, as_of)
    if plan is not None and semantics != "snapshot":
        plan["chosen"] = plan["chosen"][-1:]
        plan["newest"] = plan["chosen"][-1] if plan["chosen"] else plan["newest"]
    return plan


bd._window_plan = _newest_only
