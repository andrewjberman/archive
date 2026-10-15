"""AR345-y-AC3 checker (0.9.0_WK_IRPT_ANLREQ~149): the mint helper's hash is a bcrypt cost-12 hash that verifies.

Imports hash_password from fwd1_driver/fwd1_mint.py (import-safe: no AWS, no boto3 at import), hashes a RANDOM password,
checks the $2b$12$ (or $2a$12$) prefix, verifies with Python bcrypt and, a negative control with a wrong password, and
verifies with bcryptjs through node when a bcryptjs package exists in the portal's or the auth handler's node_modules
(those two folders only; ABSENT is printed, not a failure). Prints HASH-OK scheme=.. cost=12 python=ok bcryptjs=<ok|ABSENT>;
otherwise HASH-BAD <why> and exit 1. It never prints the password or the hash.
"""
from __future__ import annotations

import importlib.util
import os
import secrets
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
MINT = HERE / "fwd1_driver" / "fwd1_mint.py"
# this folder sits six levels below the worktree root (org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/<serial>)
WORKTREE = HERE.parents[6]
BCRYPTJS_DIRS = (
    WORKTREE / "portal" / "node_modules" / "bcryptjs",
    WORKTREE / "infra" / "aws" / "opalinvest_dev" / "lambda" / "auth-handler" / "node_modules" / "bcryptjs",
)


def bad(why):
    print("HASH-BAD " + why)
    return 1


def main():
    spec = importlib.util.spec_from_file_location("fwd1_mint", str(MINT))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    import bcrypt

    pw = secrets.token_urlsafe(24)
    wrong = pw + "-x"
    h = mod.hash_password(pw)
    if h.startswith("$2b$12$"):
        scheme = "2b"
    elif h.startswith("$2a$12$"):
        scheme = "2a"
    else:
        return bad("prefix is not $2b$12$ or $2a$12$")
    if not bcrypt.checkpw(pw.encode("utf-8"), h.encode("ascii")):
        return bad("python bcrypt does not verify the hash")
    if bcrypt.checkpw(wrong.encode("utf-8"), h.encode("ascii")):
        return bad("python bcrypt verifies a wrong password (negative control)")
    present = [d for d in BCRYPTJS_DIRS if (d / "package.json").is_file()]
    if not present:
        js = "ABSENT"
    else:
        script = ("const b=require(process.argv[1]);"
                  "process.stdout.write(b.compareSync(process.env.FWD1_PW,process.env.FWD1_H)?'MATCH':'NOMATCH')")
        env = dict(os.environ)
        env["FWD1_PW"] = pw
        env["FWD1_H"] = h
        r = subprocess.run(["node", "-e", script, str(present[0])], env=env, capture_output=True, text=True, timeout=120)
        if r.stdout.strip() != "MATCH":
            return bad("bcryptjs does not verify the hash (rc=%d)" % r.returncode)
        js = "ok"
    print("HASH-OK scheme=%s cost=12 python=ok bcryptjs=%s" % (scheme, js))
    return 0


if __name__ == "__main__":
    sys.exit(main())
