"""NFRA_GATSCP round 2 check helpers (issuer 2.0.0_SA_COO~N1). Re-exports the round-1 helpers and adds plumbing commits.

Every check plants in a PRIVATE COPY of the git index or in unreferenced commits; no working-tree file and no ref moves.
ASCII only. Python 3.9.
"""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "..", "..", "round1_prep", "checks"))

from r1_common import (ACT_DOC, ACT_ROW, BASELINE, BYSTANDER, BYSTANDER_DOC, BYSTANDER_ROW, ROOT, finish,  # noqa: E402,F401
                       git, git_bash, index_text, plant, plant_channel_failure, plant_row_drift, run, standing, tail,
                       temp_index)

PROBE = "org/missions/D0/NFRA/NFRA_GATSCP/deliverables/2.0.0_SA_COO~N1/round2_prep/probe_%s.md"
_DIRS = []


def build(parent, drift=False, channel=False, probe=None, tag=""):
    """An unreferenced commit on `parent`: optionally the bystander's row drift and/or channel failure, optionally one
    probe file. `tag` only changes the message, so two commits with one tree stay distinct."""
    d, env = temp_index()
    _DIRS.append(d)
    git(["read-tree", parent], env=env)
    if drift:
        plant_row_drift(env)
    if channel:
        plant_channel_failure(env)
    if probe:
        plant(env, PROBE % probe, "probe %s\n" % probe)
    tree = git(["write-tree"], env=env).stdout.strip()
    return git(["commit-tree", tree, "-p", parent, "-m", "probe %s %s" % (probe or "base", tag)]).stdout.strip()


def cleanup():
    import shutil
    for d in _DIRS:
        shutil.rmtree(d, ignore_errors=True)
