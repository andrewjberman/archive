"""Write the planted run's persisted receipt, byte for byte as host_capture persisted it, to
IB132-1_persisted_receipt_sample.json beside this script.

The planted run is the one the session test drives: a fake wrapper process whose stdout carries a runner
failure receipt with synthetic secrets inside and beside login_submission and probe_pair, run through
host_capture.run_capture. No bash, no browser, no network, no vendor. Usage (from the worktree root):

    python org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~292/write_persisted_receipt_sample.py
"""
import json
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[6]
SESSION = ROOT / 'infra' / 'aws' / 'lambda' / 'investor-reporting' / 'ycharts' / 'session'
sys.path.insert(0, str(SESSION))
sys.path.insert(0, str(SESSION / 'tests'))

import host_capture  # noqa: E402
import test_capture_receipt_persisted as planted  # noqa: E402

SAMPLE = HERE / 'IB132-1_persisted_receipt_sample.json'
RECORD = HERE / 'IB132-1_capture_receipt_record.json'


def main():
    with tempfile.TemporaryDirectory() as scratch:
        token = planted.run_one(scratch, planted.runner_output(planted.planted_runner_receipt()))
        persisted = (Path(scratch) / host_capture.RECEIPT_NAME).read_bytes()
    text = persisted.decode('ascii')
    leaked = [s[:4] + '...' for s in planted.PLANTED_SECRETS if s in text]
    if leaked:
        raise SystemExit('FAIL: planted secrets in the persisted receipt: %s' % leaked)
    SAMPLE.write_bytes(persisted)
    print('failure token the resident logs: ' + token)
    print('wrote %s (%d bytes); 0 of %d planted secrets in it' % (SAMPLE.name, len(persisted), len(planted.PLANTED_SECRETS)))
    if RECORD.is_file():
        recorded = json.loads(RECORD.read_text(encoding='utf-8')).get('planted_secrets')
        print('record planted_secrets equals the test\'s: ' + str(recorded == planted.PLANTED_SECRETS))


if __name__ == '__main__':
    main()
