"""IB-pr-473: write the persisted receipt of the PLANTED run, exactly as host_capture persisted it.

Run from the worktree root:  python <this file>
Uses the session tests' fake-wrapper harness (no bash, no browser, no vendor); every value is SYNTHETIC.
Also prints the planted strings to stdout as JSON (for the record) and checks none is in the written file.
"""
import json
from pathlib import Path
import sys
import tempfile

ROOT = Path.cwd()
SESSION = ROOT / 'infra/aws/lambda/investor-reporting/ycharts/session'
sys.path.insert(0, str(SESSION))
sys.path.insert(0, str(SESSION / 'tests'))
import host_capture  # noqa: E402
from test_capture_receipt_per_step import planted_challenge_receipt  # noqa: E402
from test_capture_receipt_persisted import PLANTED_SECRETS, run_one, runner_output  # noqa: E402

OUT = ROOT / 'org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~328/IB165-3_persisted_receipt_sample.json'

receipt = planted_challenge_receipt()
# The sample shows the probe steps (each carries the five per-step members); the sign-in form step has no probe.
receipt['record']['steps'] = [s for s in receipt['record']['steps'] if 'body_marker' in s]
with tempfile.TemporaryDirectory() as tmp:
    token = run_one(Path(tmp), runner_output(receipt))
    text = (Path(tmp) / host_capture.RECEIPT_NAME).read_text()
assert all(s not in text for s in PLANTED_SECRETS)
OUT.write_text(text, encoding='ascii', newline='\n')
print(json.dumps({'failure_token': token, 'bytes': len(text), 'planted_secrets': PLANTED_SECRETS}))
