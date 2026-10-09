"""GS-f-1 AC1 (rows D1-S4, D1-S11; ruling R2): the row gate's open-order census never counts a seat-home POINTER file as
an open task order, and still counts a real open order.

Plant (private index only): a POINTER file for NFRA_GATSCP in the CloudOps seat home, modelled on the live
MDPF_DEMQUE.R4-ZQ.POINTER.md (no <status>, a `# pipeline-override: this file is a POINTER ...` line), and one real
non-terminal tree order for NFRA_GATSCP (<status>pending</status>).
`surprise-row-gate.py` `_open_tos_census(root, "NFRA_GATSCP", merging=True)` reads the index.
Arm 1 (the negative arm, R2): the real open order is in the open list.
Arm 2 (the build): the POINTER is not.
"""
import importlib.util
import os
import shutil
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "..", "..", "round1_prep", "checks"))
from r1_common import ROOT, finish, plant, temp_index  # noqa: E402

PTR = "org/tier2_senior/0.7.0_AE_CloudOps/task_orders/NFRA_GATSCP.R3-ZZ.POINTER.md"
OPEN = "org/missions/D0/NFRA/NFRA_GATSCP/task-orders/NFRA_GATSCP.TO-GS-zz-9.r3-probe-open.md"
PTR_TEXT = ("# POINTER (not an order) -- NFRA_GATSCP probe held by 0.7.0_AE_CloudOps~ZZ\n"
            "# pipeline-override: this file is a POINTER in the CloudOps lane task_orders/ home for site Z lane ~ZZ, "
            "not a task order; the mission-tree order is the authority\n\n"
            "Issuer `2.0.0_SA_COO~N1`. This file carries no criteria and is never flipped.\n")
OPEN_TEXT = ("# TO NFRA_GATSCP.TO-GS-zz-9 -- probe\n\n<to_id>NFRA_GATSCP.TO-GS-zz-9</to_id>\n<project>NFRA_GATSCP</project>\n"
             "<issued_to>0.9.0_WK_NFRA_GATSCP~99</issued_to>\n<status>pending</status>\n")

d, env = temp_index()
try:
    plant(env, PTR, PTR_TEXT)
    plant(env, OPEN, OPEN_TEXT)
    os.environ["GIT_INDEX_FILE"] = env["GIT_INDEX_FILE"]
    spec = importlib.util.spec_from_file_location("srg", os.path.join(ROOT, ".tools", "surprise-row-gate.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    open_ids, n, note = mod._open_tos_census(ROOT, "NFRA_GATSCP", merging=True)
    labels = open_ids or []
    has_open = any(os.path.basename(OPEN) in x for x in labels)
    has_ptr = any(os.path.basename(PTR) in x for x in labels)
    arms = [
        ("real-open-order-counted", open_ids is not None and has_open, "census=%s of %s :: %s" % (len(labels), n, labels[:4])),
        ("pointer-not-counted", open_ids is not None and not has_ptr, "pointer_in_open_list=%s note=%s" % (has_ptr, (note or "")[:80])),
    ]
    sys.exit(finish("GS-F1-POINTER", arms))
finally:
    os.environ.pop("GIT_INDEX_FILE", None)
    shutil.rmtree(d, ignore_errors=True)
