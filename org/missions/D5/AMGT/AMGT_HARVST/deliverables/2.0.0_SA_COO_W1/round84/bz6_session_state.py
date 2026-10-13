"""HVST-bz-6: the saved Dow Jones session state of one publisher, and, with --mint, ONE sign-in through the existing mechanism.

Default is READ ONLY: it prints whether the publisher's saved-session file exists and three non-secret fields of the
envelope. `--mint` calls `SessionManager.refresh(publisher)` once (lib/opal_data_harvest/auth.py), which runs the CRO's
dowjones_harvest_session.py with the credentials read BY NAME from the Secrets Manager secret `dowjones/credentials`.
This file reads no secret, prints no cookie, bundle, username, password or token, and parks nothing (no --park)."""
import argparse
import datetime as dt
import sys
from pathlib import Path

PUBLISHERS = ("wsj", "barrons")


def describe(envelope, now):
    """One non-secret line of the envelope: presence, subscriber, network_auth_corroborated, captured_at, age_days."""
    if not isinstance(envelope, dict):
        return "present=False subscriber=False network_auth_corroborated=False captured_at= age_days="
    evidence = envelope.get("auth_evidence") or {}
    captured = str(envelope.get("captured_at") or "")
    age = ""
    try:
        moment = dt.datetime.fromisoformat(captured.replace("Z", "+00:00"))
        age = "%.1f" % ((now - moment).total_seconds() / 86400.0)
    except ValueError:
        pass
    return "present=True subscriber=%s network_auth_corroborated=%s captured_at=%s age_days=%s" % (
        bool(evidence.get("subscriber")), bool(envelope.get("network_auth_corroborated")), captured, age)


def valid(envelope):
    return (isinstance(envelope, dict) and bool((envelope.get("auth_evidence") or {}).get("subscriber"))
            and bool(envelope.get("network_auth_corroborated")))


def main(argv=None, vault_factory=None, manager_factory=None, now=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("publisher", choices=PUBLISHERS)
    parser.add_argument("--runtime-root", required=True, type=Path)
    parser.add_argument("--mint", action="store_true", help="ONE sign-in if the saved session is absent or not valid")
    args = parser.parse_args(argv)
    now = now or dt.datetime.now(dt.timezone.utc)
    if vault_factory is None:
        from lib.opal_data_harvest.storage import SessionVault as vault_factory
    try:
        envelope = vault_factory(args.runtime_root).load(args.publisher)
    except Exception as exc:  # a DPAPI or JSON failure names its class, never its text
        print("STATE %s unreadable=%s" % (args.publisher, type(exc).__name__))
        envelope = None
    print("STATE %s %s VALID=%s" % (args.publisher, describe(envelope, now), valid(envelope)))
    if not args.mint:
        return 0
    if valid(envelope):
        print("MINT %s SKIPPED: the saved session is valid; no sign-in made" % args.publisher)
        return 0
    if manager_factory is None:
        from lib.opal_data_harvest.auth import SessionManager as manager_factory
    events = []

    def record(event):
        events.append({k: event[k] for k in ("event", "publisher", "network_auth_corroborated") if k in event})

    try:
        result = manager_factory(args.runtime_root, record).refresh(args.publisher)
    except Exception as exc:
        print("MINT %s REFUSED: %s" % (args.publisher, type(exc).__name__))
        return 3
    print("MINT %s DONE %s" % (args.publisher, describe(result, now)))
    return 0 if valid(result) else 3


if __name__ == "__main__":
    sys.exit(main())
