"""AMGT_CORPUS round 14, CRPS-p-1 -- the issuer's run of readonly_proof inside its ruled bound (read-only to the worker).

  python p1_run.py negative-control -> 'p1 negative_control rc R ingest_rc I put_performed P temp_new_entries N'
  python p1_run.py code-census      -> 'p1 code_census rc R library_write_calls L temp_new_entries N'

The bound (round-13 analysis ruling 2): every write of the arm goes under ONE tempfile.mkdtemp(prefix="amgt_corpus_")
directory that is gone at exit. temp_new_entries counts the amgt_corpus* entries in the system temp dir that exist after the
run and did not before. The negative-control arm copies the whole library (~308 MB), so it is REFUSED here, unrun, while
negative_control() carries no mkdtemp scratch directory.
"""
import inspect
import os
import re
import subprocess
import sys
import tempfile

from lib.research.corpus import readonly_proof


def _temp_entries():
    return {n for n in os.listdir(tempfile.gettempdir()) if n.startswith("amgt_corpus")}


def _run(flag):
    proc = subprocess.run([sys.executable, "-m", "lib.research.corpus.readonly_proof", flag],
                          capture_output=True, text=True, encoding="utf-8", errors="replace")
    return proc.returncode, proc.stdout + proc.stderr


def main(mode):
    if mode == "negative-control" and "mkdtemp" not in inspect.getsource(readonly_proof.negative_control):
        print("p1 negative_control bound_absent: negative_control() carries no mkdtemp scratch directory; not run")
        return 1
    before = _temp_entries()
    rc, out = _run("--" + mode)
    new = sorted(_temp_entries() - before)
    if mode == "negative-control":
        m = re.search(r"ingest_rc (\d+) stored \d+ put_performed (\d+)", out)
        ingest_rc, put = (m.group(1), m.group(2)) if m else ("absent", "absent")
        print("p1 negative_control rc %d ingest_rc %s put_performed %s temp_new_entries %d" % (rc, ingest_rc, put, len(new)))
    else:
        m = re.search(r"library_write_calls (\d+)", out)
        print("p1 code_census rc %d library_write_calls %s temp_new_entries %d" % (rc, m.group(1) if m else "absent", len(new)))
    for name in new:
        print("new_temp_entry " + name)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
