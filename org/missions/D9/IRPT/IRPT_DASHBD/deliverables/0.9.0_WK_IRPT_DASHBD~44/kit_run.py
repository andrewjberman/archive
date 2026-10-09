"""TO-DB-b-67 (E2): prints the run's own runtime versions, then runs round 30's lots_750_run.py (imported) in 'default' mode.

Usage (worktree root, kit venv python): python <this file> <outdir> <record.json> <runtime.json>
"""
import importlib.util
import json
import platform
import sys
from pathlib import Path

import numpy
import pandas
import pyarrow

HERE = Path(__file__).resolve().parent
RUN = HERE.parent / "0.9.0_WK_IRPT_DASHBD~31" / "lots_750_run.py"


def main(outdir, record, runtime_path):
    rt = {"python": platform.python_version(), "pandas": pandas.__version__, "numpy": numpy.__version__,
          "pyarrow": pyarrow.__version__}
    print("RUNTIME " + json.dumps(rt), flush=True)
    Path(runtime_path).write_text(json.dumps(rt) + "\n", encoding="utf-8")
    spec = importlib.util.spec_from_file_location("lots_750_run", RUN)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.main("default", outdir, record)


if __name__ == "__main__":
    main(*sys.argv[1:4])
