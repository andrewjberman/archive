"""TO-DB-b-73 step 3: round 30's runner (lots_750_run.py, default batch) for ONE named day -- imported, not restated; only its DAY constant is set.

Usage (worktree root, kit venv python): python <this file> <day> <outdir> <record.json>
"""
import importlib.util
import sys
from pathlib import Path

RUN = Path(__file__).resolve().parent.parent / "0.9.0_WK_IRPT_DASHBD~31" / "lots_750_run.py"


def main(day, outdir, record):
    spec = importlib.util.spec_from_file_location("lots_750_run", RUN)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.DAY = day
    mod.main("default", outdir, record)


if __name__ == "__main__":
    main(*sys.argv[1:4])
