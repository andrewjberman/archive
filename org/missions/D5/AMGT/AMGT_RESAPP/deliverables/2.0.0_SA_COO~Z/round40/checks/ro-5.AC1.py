"""AMGT_RESAPP round 40, AMGT-ro-5 AC1 -- posture's absence reason carries NO repository path: load_model_block on a
key with no landed block returns a reason a user can read, with no path separator and no 'org' / 'deliverables'
segment. usage (repo root): PYTHONPATH="$(pwd)" python <this>"""
import sys

from lib.research.posture import packs

block, reason = packs.load_model_block("NOPE_US_Equity")
bad = [tok for tok in ("\\\\", "/", "org", "deliverables", "model_block_") if tok in (reason or "")]
print("block=%r reason=%r path-tokens=%s" % (block, reason, bad or "none"))
sys.exit(0 if block is None and reason and not bad else 1)
