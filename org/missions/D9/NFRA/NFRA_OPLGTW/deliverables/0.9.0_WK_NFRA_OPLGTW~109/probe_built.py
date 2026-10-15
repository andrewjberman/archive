"""OG-gp-1 probe: each BUILT tool against the REAL bucket, with the box's own credentials (INTERNAL_READER_ROLE_ARN unset).

For the one BUILT tool, mdpf_get_model_composition:
  - the Opal stand-in principal calls it for real: the envelope must be complete and the body non-empty or carry absent_reason;
  - a non-Opal stand-in principal calls it with the S3 client replaced by a counter that raises on any access: the refusal
    must be typed_opal_only and the count of S3 touches must be 0.

Prints ONE line per tool and no object content. Audit records go to a scratch file in the worktree, never a tracked file.
"""
import os
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[7]            # the worktree root (org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/<serial>/)
GW = ROOT / "infra" / "aws" / "ec2" / "opal-gateway"
os.environ["AUDIT_PATH"] = str(ROOT / ".scratch" / "probe_gp1_audit.jsonl")
os.environ["AUDIT_S3_BUCKET"] = ""
sys.path[:0] = [str(GW), str(ROOT)]

from app import context, identity_scope  # noqa: E402
from app import portal_served as ps  # noqa: E402

OID = "00000000-0000-0000-0000-0000000090f1"
ENVELOPE = ("as_of", "source_keys", "denominator", "absent_reason")
SCOPE = "49financial"


class _Counter:
    """Stands in for the S3 client on the refusal arm: any attribute access is one S3 touch, and it raises."""
    touches = 0

    def __getattr__(self, name):
        _Counter.touches += 1
        raise RuntimeError("S3 touched on a refusal path")


def main() -> int:
    real_client = ps._client
    context.set_current_principal(context.make_principal(context.MOCK_TENANT_ID, OID,
                                                         "gp1.probe@" + identity_scope.OPAL_USERS_DOMAIN))
    ans = ps.mdpf_get_model_composition(SCOPE)
    complete = all(k in ans for k in ENVELOPE)
    non_empty = bool(ans.get("rows")) or bool(ans.get("absent_reason"))
    answered = bool(complete and not ans.get("code") and non_empty)
    print("probe detail: scope=%s rows=%s as_of=%s absent_reason_set=%s" % (
        SCOPE, (ans.get("denominator") or {}).get("rows"), ans.get("as_of"), bool(ans.get("absent_reason"))))

    context.set_current_principal(context.make_principal(context.MOCK_TENANT_ID, OID,
                                                         "gp1.probe@example.invalid"))
    ps._client = lambda: _Counter()
    try:
        refused = ps.mdpf_get_model_composition(SCOPE)
    finally:
        ps._client = real_client
    non_opal_refused = refused.get("code") == "typed_opal_only"
    reads_on_refusal = _Counter.touches

    print("probe built: mdpf_get_model_composition answered %s; non_opal_refused %s; reads_on_refusal %d"
          % (answered, non_opal_refused, reads_on_refusal))
    return 0 if (answered and non_opal_refused and reads_on_refusal == 0) else 1


if __name__ == "__main__":
    sys.exit(main())
