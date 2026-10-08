"""TO-DB-b-52 (E3): one run of round 28's runner (batched_e2_run.py, imported, not restated) at one batch size, or with NO batch size.

Usage (worktree root): python <this file> <batch_size|default> <outdir> <record.json>
'default' makes handler.local see batch_size=None (the producer's DEFAULT_BATCH_SIZE), exactly as a CLI run with no --batch-size does.
"""
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
RUNNER = HERE.parent / "0.9.0_WK_IRPT_DASHBD~27" / "batched_e2_run.py"
DAY = "2026-10-06"


def main(size, outdir, record):
    spec = importlib.util.spec_from_file_location("batched_e2_run", RUNNER)
    run = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(run)
    if size == "default":
        sys.path.insert(0, str(run.ROOT / "infra/aws/lambda/investor-reporting/reporting-gold"))
        import handler as h
        real = h.local

        def local_default(*a, **k):
            k["batch_size"] = None
            return real(*a, **k)
        h.local = local_default
        size = "0"
    run.main(DAY, size, outdir, record)


if __name__ == "__main__":
    main(*sys.argv[1:4])
