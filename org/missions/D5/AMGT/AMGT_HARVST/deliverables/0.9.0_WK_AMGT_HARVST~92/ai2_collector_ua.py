"""HVST-ai-2 EXPERIMENT (not product): run the collector CLI in-process with the persistent-profile launch given the
harvester's forced User-Agent (ft_harvest_session.UA), to test whether the ft session dies because the tab that uses it
presents a different User-Agent than the browser that created it. The repository's launch stays override-free
(test_ae2_one_identity pins it); this wrapper adds the kwarg at the Playwright call only for this process.
  python ai2_collector_ua.py <collector args...>
"""
import re
import runpy
import sys
from pathlib import Path

sys.path.insert(0, ".")
from playwright.sync_api import BrowserType  # noqa: E402

source = Path("org/tier1_exec/4.0.0_SA_CRO/scripts/ft_harvest_session.py").read_text(encoding="utf-8")
UA = re.search(r'^UA = "([^"]+)"', source, re.M).group(1)
_orig = BrowserType.launch_persistent_context


def _patched(self, *args, **kwargs):
    kwargs.setdefault("user_agent", UA)
    return _orig(self, *args, **kwargs)


BrowserType.launch_persistent_context = _patched
sys.argv = ["lib.opal_data_harvest"] + sys.argv[1:]
runpy.run_module("lib.opal_data_harvest", run_name="__main__", alter_sys=True)
