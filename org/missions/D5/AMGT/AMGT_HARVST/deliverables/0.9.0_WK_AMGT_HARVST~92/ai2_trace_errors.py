"""HVST-ai-2 EXPERIMENT (not product): run the collector CLI in-process and write the MESSAGE of any exception that leaves
TabSession.get to ai2_tab_errors.txt (the worker's job record keeps only the exception class, so a job that ends
`status=error` / `error_type=Error` cannot be told from its record). The exception is re-raised unchanged.
  python ai2_trace_errors.py <collector args...>
"""
import datetime as dt
import runpy
import sys
from pathlib import Path

sys.path.insert(0, ".")
from lib.opal_data_harvest import tab_transport  # noqa: E402

OUT = Path(__file__).with_name("ai2_tab_errors.txt")
_get = tab_transport.TabSession.get


def get(self, url, *a, **k):
    try:
        return _get(self, url, *a, **k)
    except Exception as exc:
        with OUT.open("a", encoding="utf-8") as fh:
            fh.write("%s %s %s: %s\n" % (dt.datetime.now(dt.timezone.utc).strftime("%H:%M:%SZ"), url[:90], type(exc).__name__, str(exc)[:600]))
        raise


tab_transport.TabSession.get = get
sys.argv = ["lib.opal_data_harvest"] + sys.argv[1:]
runpy.run_module("lib.opal_data_harvest", run_name="__main__", alter_sys=True)
