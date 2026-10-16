"""MX-c-28 mutant control (scratch only): the floor step removed (as_floor replaced by the identity), then the AC2 predicate run
unchanged from the checks folder. The mutant must FAIL the predicate (rc=1) for the control to have fired."""
import os
import sys

ROOT = "C:/tmp/wk-mx20-51"
os.environ["C28_ROOT"] = ROOT
AD = os.path.join(ROOT, "workflows", "atom_decomposition")
sys.path.insert(0, AD)
import emit_catalog_v02 as em  # noqa: E402

em.as_floor = lambda claim: claim   # the mutant: no depth_kind, no measured_at
CHK = os.path.join(ROOT, "org", "missions", "D9", "NFRA", "NFRA_MCPINDEX", "deliverables", "2.0.0_SA_COO~MI", "round20", "checks")
sys.path.insert(0, CHK)
import c28_check  # noqa: E402

rc = c28_check.ac2()
print("MUTANT-RUN rc=%d" % rc)
