"""Append AMGT_HARVST-Z-W20-S1 INSIDE the first fenced json array. Never edits an existing row."""

import datetime
import json
import pathlib

PATH = pathlib.Path("org/missions/D5/AMGT/AMGT_HARVST/surprise-channel/investigations/INVESTIGATION_v1.md")

ROW = {
    "id": "AMGT_HARVST-Z-W20-S1",
    "project": "AMGT_HARVST",
    "fabric": "site-z",
    "surfaced_by": "0.9.0_WK_AMGT_HARVST~20",
    "surfaced_at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "one_line": (
        "HVST-s-1's ONE BOUNDED VENDOR ACT cannot be performed from a worker worktree: the producer's runtime "
        "root (session vault + local outbox) is DEVICE-LOCAL to the main workspace tree, which this order "
        "forbids touching and does not grant, so AC1a's literal invocation would not retry sa's listing "
        "capture at all -- worker.py:152 asks SessionManager.get('sa') first, the vault miss falls straight "
        "through to refresh(), and refresh() for sa launches a HEADED Chrome credentialed login against "
        "seekingalpha.com whose bot wall is solved by a third-party vision API, in a subprocess with no "
        "timeout and --trace-hold. AC1a was NOT RUN and is graded FAIL (BLOCKING)."
    ),
    "class": "BLOCKING",
    "hazard_standing": "ARMED",
    "grounding": {
        "status": "GROUNDED",
        "evidence": [
            "This worktree C:/tmp/wk-hvst-s1b (branch wk-harvst-6-20 @d170846523) has NO .runtime at all: "
            "`ls -la .runtime` -> 'No such file or directory'. lib/opal_data_harvest/publishers.py:22 sets "
            "ROOT = Path(__file__).resolve().parents[2] (the WORKTREE root) and lib/opal_data_harvest/config.json "
            "carries runtime_root '.runtime/opal-data-harvest', so `python -m lib.opal_data_harvest run` from "
            "here resolves its runtime root to C:/tmp/wk-hvst-s1b/.runtime/opal-data-harvest -- absent, hence "
            "no secrets/sa.dpapi and no progress.sqlite3 outbox.",
            "The sa session envelope exists ONLY in the main workspace tree: read-only `ls -la "
            "'C:/Users/Opal Bloomberg/Desktop/ajb_workspace/.runtime/opal-data-harvest/secrets/'` lists "
            "sa.dpapi (26438 bytes, 2026-09-15 00:37) beside barrons/bbg/ft/wsj.dpapi. That path is in neither "
            "this task order's <paths> nor the worker's write grant, and the worker prompt states 'Do NOT touch "
            "C:/Users/Opal Bloomberg/Desktop/ajb_workspace'.",
            "lib/opal_data_harvest/worker.py:151-152 -- `try:` then `envelope = self.sessions.get(publisher)` "
            "runs UNCONDITIONALLY, before the Publisher client is constructed and before any listing-bronze "
            "dedupe read; lib/opal_data_harvest/auth.py:22-24 `SessionManager.get` is `saved or "
            "self.refresh(publisher)`; lib/opal_data_harvest/storage.py:51-55 `SessionVault.load` returns None "
            "when secrets/<pub>.dpapi is absent. A vault miss therefore goes straight to refresh().",
            "lib/opal_data_harvest/auth.py:85-89: refresh() for a non-Dow-Jones publisher execs "
            "org/tier1_exec/4.0.0_SA_CRO/scripts/harvest_local_session.py `harvest(publisher, folder, "
            "max_steps=10, trace_hold=True)`, which at harvest_local_session.py:46-48 runs sa_harvest_session.py "
            "via `subprocess.run([...])` with NO timeout argument, passing --trace-hold (harvest_local_session.py"
            ":38-39). sa_harvest_session.py:380-384 launches `p.chromium.launch(channel='chrome', "
            "headless=HEADLESS ...)` with HEADLESS = '--headless' in argv (:42) = False on this path, logs in "
            "with the stored credential (`cred={cred_src} email={EMAIL}`, :405), and solves the Press-and-Hold "
            "bot wall with a vision model (`kimi={KIMI_MODEL}`, same log line; press_and_hold_adaptive :268-278). "
            "That is a credentialed interactive login plus THIRD-PARTY vendor egress -- not the cell's authorized "
            "bounded listing retry, and not bounded in time.",
            "AC0, measured live at this vintage (.scratch/s1/ac0_output.txt, rc=0): sa silver listing_hit rows = "
            "0 and bronze news_listing objects = 0; wsj 20 rows / 2 objects; barrons, bbg, ft all 0/0; "
            "denominator 5 publishers (SOURCE_FOR_PUBLISHER). The persist is confirmed deployed at "
            "lib/opal_data_harvest/worker.py:223 `finally:` with the Z-S10 guard `already_propagating = "
            "sys.exc_info()[0] is not None` at :244 ahead of the persist at :246.",
        ],
    },
    "disposition": "UNDER_INVESTIGATION",
    "spec_asserts": (
        "Section 0 clause 2: 'Every vendor byte in this cell comes from the EXISTING deterministic scripted "
        "producer invoked from the command line'; clause 3: 'ONE BOUNDED VENDOR ACT. --publishers sa and nothing "
        "else.' AC1a's invocation is literal and carries no --runtime-root, i.e. the order asserts that running "
        "`python -m lib.opal_data_harvest run --publishers sa --harvest-grammar --security-json ... --max-jobs 1` "
        "from the worktree root performs sa's listing retry."
    ),
    "world_is": (
        "From a worker worktree that invocation performs no listing retry and reaches no sa listing endpoint: "
        "the producer's session vault and local outbox live in the MAIN tree's .runtime, so the first thing the "
        "job does is miss the vault and fall into an unbounded headed re-auth with third-party vision egress. "
        "The act the order authorizes and the act the literal invocation would perform are different acts, so "
        "AC1a was not run; the retry class (a 502 outage) remains UNTESTED on this fabric rather than tested and "
        "recorded."
    ),
    "disarm_owner": "2.0.0_SA_COO~Y",
    "notes": (
        "Disarm options for the issuer, none of them a worker's to take: (a) re-cut AC1a with an explicit "
        "--runtime-root naming the device runtime root and add that path to the write grant; (b) issue this cell "
        "to a seat that works in the main tree where the vault and outbox already sit; (c) make seeding the "
        "worktree runtime root from the device vault an explicit, granted step of the order. THE SAME LOCALITY "
        "HITS AC1b: HarvestUploader drains harvest_listing_outbox out of the SAME runtime root, so whatever "
        "pages the original 502 run captured in the main tree are invisible from here and AC1b can only ever "
        "report an empty drain from this worktree. AC1b, AC2, AC3, AC4 and AC5 were still run and recorded."
    ),
}


def main():
    text = PATH.read_text(encoding="utf-8")
    fence = text.index("```json")
    end = text.index("\n```", fence)
    close = text.rindex("\n]", fence, end)
    body = json.dumps(ROW, indent=2, ensure_ascii=True)
    indented = "\n".join("  " + line for line in body.splitlines())
    updated = text[:close] + ",\n" + indented + text[close:]
    PATH.write_text(updated, encoding="utf-8", newline="\n")
    check = json.loads(updated[fence + 7:updated.index("\n```", fence)])
    print("rows now: %d ; last id: %s" % (len(check), check[-1]["id"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
