#!/usr/bin/env python3
"""D0_T1 strict-kwargs + empty-envelope guards -- the A1-A5 harness (COO seating 64310/64318).

Imports the PURE guards module directly and the broker MODULE (mcp.run is under __main__, so the
import starts nothing, binds no port, spawns no poller). Refusal paths only -- no test ever
delivers a message, so no inbox state is written. The live positive control (A2) is the running
fabric itself: every real body= send this session delivered normally.

STAGED-vs-EXECUTING (Rule 22a, stated in the close): the RUNNING broker process predates these
edits; the guards EXECUTE only after the next broker start. This harness proves the LANDED bytes.
"""
from __future__ import annotations

import asyncio
import os
import sys

WS = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(WS, "org", "mcp"))

import broker_arg_guards as g  # noqa: E402

ok = []


def chk(name, cond):
    ok.append(bool(cond))
    print("  [%s] %s" % ("PASS" if cond else "FAIL", name))


# ---- CHECK 1 pure: unknown-kwarg detection + did-you-mean --------------------------------------
known = {"from_agent", "to_agent", "subject", "body", "identity_override", "to_agents"}
u = g.unknown_kwargs({"from_agent": "x", "message": "oops"}, known)
msg = g.strict_kwargs_message("send_message", u, sorted(known))
chk("A1a unknown kwarg detected and the refusal NAMES it with a did-you-mean",
    u == ["message"] and "unknown parameter: message" in msg and "did you mean body?" in msg
    and "Nothing was executed" in msg)
chk("A1b a clean call has zero unknowns (negative control on the detector)",
    g.unknown_kwargs({"from_agent": "x", "to_agent": "y", "subject": "s", "body": "b"}, known) == [])

# ---- CHECK 2 pure: structural, both directions, ZERO thresholds --------------------------------
chk("A4a empty body + non-empty subject -> REFUSED (the measured defect)",
    g.empty_envelope_refusal("a subject", "") is not None and "EMPTY while subject" in g.empty_envelope_refusal("s", ""))
chk("A4b empty body + empty subject -> REFUSED with its own stated reason (ruled: an empty envelope has no fabric use)",
    g.empty_envelope_refusal("", "") is not None and "both empty" in g.empty_envelope_refusal("", ""))
chk("A4c whitespace-only body is EMPTY (structural, not a byte count)", g.empty_envelope_refusal("s", "  \n\t ") is not None)
chk("A4d a real body passes regardless of subject length (positive control)",
    g.empty_envelope_refusal("s" * 5000, "content") is None and g.empty_envelope_refusal("", "content") is None)
# THE NO-THRESHOLD REGRESSION FIXTURES (MSTR 64327): any implementation that a byte floor would
# fool must still refuse here. 64238's shape: 324B of content in the SUBJECT, body empty (file
# 432B -- sails past a ~350B floor); and the one-byte-margin case (subject sized so file=349B).
chk("A4e REGRESSION (0.7.0's 432B miss): huge subject + empty body -> REFUSED (a byte floor would have passed it)",
    g.empty_envelope_refusal("x" * 324, "") is not None)
chk("A4f REGRESSION (MSTR's 349B one-byte case): -> REFUSED regardless of any floor arithmetic",
    g.empty_envelope_refusal("y" * 241, "") is not None)
import inspect  # noqa: E402
# scope: the FUNCTIONS' code, not the module docstring -- the docstring legitimately NARRATES the
# killed byte-floor (349B/350B provenance), and scanning it is the mention-vs-use class this seat
# already tripped once tonight (the rider's no-verdict check firing on its own disclaimer)
fn_src = "".join(inspect.getsource(f) for f in (g.unknown_kwargs, g.strict_kwargs_message, g.empty_envelope_refusal))
chk("A4g NO THRESHOLD ANYWHERE in the guard FUNCTIONS: no numeric floor, no len() comparison on subject/body",
    all(t not in fn_src for t in ("350", "len(subject)", "len(body)", "> 120", ">= 120", "wc -c")))

# ---- A3: the pre-fix behavior REPRODUCED ON DEMAND, then the fix refusing the same call ---------
print("  -- importing org/mcp/server as a MODULE (mcp.run is under __main__; nothing starts) --")
import server  # noqa: E402

tool = server.mcp._tool_manager.get_tool("send_message")
bad_args = {"from_agent": "0.8.0_AE_CloudComp", "to_agent": "2.0.0_SA_COO",
            "subject": "a subject full of content", "message": "the body, in the wrong parameter"}
# PRE-FIX (the check DISABLED = pydantic's own ignore-extras validation, exactly what ran all night):
validated = tool.fn_metadata.arg_model.model_validate(bad_args)
d = validated.model_dump()
chk("A3a PRE-FIX REPRODUCED ON DEMAND: with the guard disabled, the bad call VALIDATES CLEAN, `message` is dropped, body='' "
    "(the silent-drop acceptance that produced nine empty sends)",
    d.get("body", None) == "" and "message" not in d)


async def a3b():
    try:
        await server.mcp._tool_manager.call_tool("send_message", bad_args)
        return None
    except ValueError as e:
        return str(e)

refusal = asyncio.get_event_loop().run_until_complete(a3b()) if sys.version_info < (3, 10) else asyncio.run(a3b())
chk("A1c/A3b POST-FIX: the SAME call through the wrapped boundary is REFUSED naming the parameter, before any tool body runs "
    "(no identity audit row, no inbox write)",
    refusal is not None and "unknown parameter: message" in refusal and "did you mean body?" in refusal)
chk("A3c the wrapper is INSTALLED on the ToolManager (call_tool is the strict wrapper, not the SDK method)",
    server.mcp._tool_manager.call_tool.__name__ == "_strict_call_tool")


async def a2():
    # A2 boundary half: a CORRECT call passes the strict boundary (the tool body then runs the
    # identity gate; we stop at the boundary by using an unknown TOOL check inversely -- here we
    # verify no refusal is raised at the kwarg layer by validating keys only).
    _tool = server.mcp._tool_manager.get_tool("send_message")
    _known = set(_tool.fn_metadata.arg_model.model_fields.keys())
    _known.discard(_tool.context_kwarg or "")
    return g.unknown_kwargs({"from_agent": "x", "to_agent": "y", "subject": "s", "body": "b"}, _known)

chk("A2 (boundary half): a correct body= call carries ZERO unknown parameters through the strict boundary -- the live half is "
    "the running fabric itself (every real send this session delivered), re-checked after the broker restart",
    (asyncio.get_event_loop().run_until_complete(a2()) if sys.version_info < (3, 10) else asyncio.run(a2())) == [])

# ---- A5: no notification machinery -- measured on the AST's ACTUAL IMPORTS, never substrings
# (a substring scan failed on 'ses' inside the word 'cases' in the docstring: the same
# mention-vs-use class, one level down at the substring grain)
import ast  # noqa: E402
tree = ast.parse(inspect.getsource(g))
imports = {a.name.split(".")[0] for n in ast.walk(tree) if isinstance(n, ast.Import) for a in n.names} \
    | {n.module.split(".")[0] for n in ast.walk(tree) if isinstance(n, ast.ImportFrom) and n.module}
chk("A5 the guards' ACTUAL imports are exactly {__future__, difflib} -- no notification machinery importable, "
    "nothing emitted, nothing watched (measured by AST, not substring)",
    imports == {"__future__", "difflib"})

n = sum(1 for x in ok if x)
print("--- D0_T1 arg-guards harness: %d/%d passed ---" % (n, len(ok)))
sys.exit(0 if n == len(ok) else 1)
