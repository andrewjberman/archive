"""Self-test for destructive_ops -- proves SAFE bypass, send-class tagging, fail-closed unknown."""
from __future__ import annotations

import sys

from destructive_ops import OpClass, classify, is_guarded, is_irreversible

CASES = []
def case(n, got, want): CASES.append((n, got, want))

# SAFE reads bypass the guard
case("read_email is SAFE", classify("read_email")["class"], OpClass.SAFE)
case("read_email not guarded", is_guarded("read_email"), False)
case("list_onedrive not irreversible", is_irreversible("list_onedrive"), False)

# create_draft = reversible write (guarded but not irreversible)
case("create_draft guarded", is_guarded("create_draft"), True)
case("create_draft NOT irreversible", is_irreversible("create_draft"), False)

# the 4 irreversible sends -> G3 always confirms
for t in ("send_email", "reply_email", "send_chat_message", "send_channel_message"):
    case(f"{t} irreversible", is_irreversible(t), True)
    case(f"{t} guarded", is_guarded(t), True)

# FAIL-CLOSED: an unknown/future tool (e.g. a delete tool) -> guarded + irreversible
case("unknown delete_item guarded (fail-closed)", is_guarded("delete_item"), True)
case("unknown delete_item irreversible (fail-closed)", is_irreversible("delete_item"), True)
case("unknown delete_item flagged unclassified", classify("delete_item").get("unclassified"), True)

fails = 0
for n, got, want in CASES:
    ok = got == want
    print(f"{'PASS' if ok else 'FAIL'}: {n} (got={got}, want={want})")
    fails += 0 if ok else 1
print(f"\n{len(CASES)-fails}/{len(CASES)} passed")
sys.exit(1 if fails else 0)
