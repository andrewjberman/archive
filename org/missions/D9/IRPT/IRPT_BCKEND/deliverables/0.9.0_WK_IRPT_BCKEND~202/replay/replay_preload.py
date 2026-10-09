"""pytest plugin (IB-pr-391 replay): make the repo's own tests exercise a PACKAGED module directory instead of the tree.

Env REPLAY_MODULES = the extracted zip directory (flat). The plugin
  1. puts it first on sys.path and imports repository, retention, composition, commentary_composition (and, when present,
     acceptance, submission, keys, opal_naming) from it, asserting each module file is inside that directory;
  2. wraps importlib.util.spec_from_file_location so a test that loads <repo>/reports/<name>.py BY PATH (test_repository does)
     is given the packaged copy of <name>.py instead (the substitutions are counted in REPLAY_SUBSTITUTIONS);
  3. appends the repo's reports/tests directory (fixtures and fakes) AFTER the package directory.
Nothing is written into the tree. ASCII only.
"""
import importlib
import importlib.util
import os
import sys
from pathlib import Path

PKG = Path(os.environ["REPLAY_MODULES"]).resolve()
REPO = Path(os.environ["REPLAY_REPO"]).resolve()
REPORTS = REPO / "infra" / "aws" / "lambda" / "investor-reporting" / "reports"
LOADED = {}
REPLAY_SUBSTITUTIONS = []

sys.path.insert(0, str(PKG))
if (PKG / "lib").is_dir():
    sys.path.insert(1, str(PKG / "lib"))

for name in ("repository", "retention", "composition", "acceptance", "submission", "keys", "opal_naming",
             "commentary_composition"):
    if not (PKG / (name + ".py")).is_file() and not (PKG / "lib" / (name + ".py")).is_file():
        continue
    try:
        mod = importlib.import_module(name)
    except Exception as exc:  # recorded, not hidden: the plugin continues so the run states WHICH import failed
        LOADED[name] = "IMPORT-FAILED %s: %s" % (type(exc).__name__, str(exc)[:160])
        continue
    origin = Path(mod.__file__).resolve()
    assert PKG in origin.parents, "%s loaded from %s, not the package %s" % (name, origin, PKG)
    LOADED[name] = str(origin.relative_to(PKG)).replace("\\", "/")

_real = importlib.util.spec_from_file_location


def _spec(name, location=None, *args, **kw):
    try:
        loc = Path(location).resolve() if location is not None else None
    except OSError:
        loc = None
    if loc is not None and loc.parent == REPORTS and (PKG / loc.name).is_file():
        REPLAY_SUBSTITUTIONS.append(loc.name)
        location = str(PKG / loc.name)
    return _real(name, location, *args, **kw)


importlib.util.spec_from_file_location = _spec
sys.path.append(str(REPORTS / "tests"))


def pytest_report_header(config):
    return ["replay package: %s" % PKG, "replay modules: %s" % LOADED]


def pytest_sessionfinish(session, exitstatus):
    out = os.environ.get("REPLAY_PLUGIN_OUT")
    if out:
        import json
        Path(out).write_text(json.dumps({"loaded": LOADED, "substituted": REPLAY_SUBSTITUTIONS}, indent=1), encoding="ascii")
