"""IB126 capture plugin (worker 0.9.0_WK_IRPT_BCKEND~287, IRPT_BCKEND.TO-IB-pr-428). READ ONLY, LOCAL ONLY.

A pytest plugin that lets an EXISTING handler test run unaltered while recording what the handler's
boundary returned. It wraps ONE callable (named by IB126_WRAP) just before the test body runs, and
saves the first returned envelope whose `operation` equals IB126_OP, which carries `data` and which
satisfies the optional IB126_MATCH ('a.b=<json literal>', read from the envelope) to IB126_OUT. Nothing is stubbed, patched or replaced: the wrapper calls the original and returns its
value unchanged. The recorded file holds synthetic test-fake values and lives in .scratch/ (git-ignored);
no value from it is ever copied into a deliverable.

IB126_WRAP forms:
  "<attr.path>"           resolved from the test module, e.g.  call   or   entry.ENTRY.handle
  "sys:<module>.<a>.<b>"  resolved from sys.modules,       e.g.  sys:served.Entry.handle
"""
import functools
import importlib
import json
import os
import sys

import pytest

_SEEN = {"calls": 0, "captured": 0}


def _resolve(item, spec):
    if spec.startswith("sys:"):
        parts = spec[4:].split(".")
        obj = sys.modules.get(parts[0]) or importlib.import_module(parts[0])
        parts = parts[1:]
    else:
        parts = spec.split(".")
        obj = item.module
    for name in parts[:-1]:
        obj = getattr(obj, name)
    return obj, parts[-1]


def _matches(result, match):
    """IB126_MATCH = 'a.b=<json literal>' read from the envelope; empty means any."""
    if not match:
        return True
    path, _, literal = match.partition("=")
    node = result
    for part in path.split("."):
        if not isinstance(node, dict) or part not in node:
            return False
        node = node[part]
    return node == json.loads(literal)


def _wrap(original, op, out):
    @functools.wraps(original)
    def wrapper(*args, **kwargs):
        result = original(*args, **kwargs)
        _SEEN["calls"] += 1
        if (isinstance(result, dict) and result.get("operation") == op and "data" in result
                and result.get("ok") is not False and not os.path.exists(out)
                and _matches(result, os.environ.get("IB126_MATCH", ""))):
            with open(out, "w", encoding="utf-8") as fh:
                json.dump(result, fh)
            _SEEN["captured"] += 1
        return result
    return wrapper


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_call(item):
    spec = os.environ.get("IB126_WRAP")
    if not spec:
        return
    holder, name = _resolve(item, spec)
    setattr(holder, name, _wrap(getattr(holder, name), os.environ["IB126_OP"], os.environ["IB126_OUT"]))


def pytest_terminal_summary(terminalreporter):
    terminalreporter.write_line("IB126-CAPTURE calls=%d captured=%d" % (_SEEN["calls"], _SEEN["captured"]))
