"""Round 21 AC1 (IB-pr-211) -- the release re-check resolves the selection WITH the request, so a RENDER_DELEGATE's
re-check can name its grant (window 21 K8: adapter corr-d490a5849a80, PerformanceAccessRefused 'a render read carries
no request to name its grant', performance/entry.py:61 calling _resolve_selected without the request).

Usage: python p21_1_ac1_release_passes_request.py <worktree root>
Arm A: entry._authorize_release(REQUEST, ctx, ref, selected, boundary) hands REQUEST itself to _resolve_selected.
Arm B (control): a scope whose selection differs from `selected` still refuses 'computed selection no longer matches'.
"""
import sys
from pathlib import Path
from types import SimpleNamespace

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
sys.path.insert(0, str(root / "infra/aws/lambda/investor-reporting/performance"))
import entry  # noqa: E402

REQUEST, SCOPE, CTX = object(), {"principal_class": "RENDER_DELEGATE"}, SimpleNamespace(tenant="t", opal_principal_ids=("p",))
seen = {}


class Enforcer:
    def resolve_now(self, request):
        return SCOPE, None


boundary = SimpleNamespace(enforcer_for=lambda tenant, ids: (Enforcer(), CTX))


def fake(scope, ctx, reference, request=None):
    seen["request"] = request
    return {"selected_account_ids": seen.get("answer", ["acc_1"])}


entry._resolve_selected = fake
ok = True
entry._authorize_release(REQUEST, CTX, "sel_x", ["acc_1"], boundary)
a = seen.get("request") is REQUEST
print("arm A: request handed to _resolve_selected: %s" % a)
seen["answer"] = ["acc_2"]
try:
    entry._authorize_release(REQUEST, CTX, "sel_x", ["acc_1"], boundary)
    b = False
except entry.PerformanceAccessRefused as exc:
    b = "no longer matches" in str(exc)
print("arm B: a changed selection still refuses: %s" % b)
ok = a and b
print("P21-1-AC1 PASS" if ok else "P21-1-AC1 FAIL")
sys.exit(0 if ok else 1)
