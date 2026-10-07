# /bbg-pull + /bbg-send — Alyssa's daily Bloomberg dashboard update (OPAL_BBGTML)

Every trading morning, two steps. Step 1 runs on the Bloomberg terminal machine; step 2 is one
tool call in Claude. Total hands-on time: under a minute (the pull itself takes a few minutes
of unattended runtime).

## Step 1 — /bbg-pull (on the terminal machine)

**Pre-req:** Bloomberg Terminal is running and you are logged in.

Double-click **`tools\run_daily_pull.bat`** in the project folder
(`Opal Capital\Shared - Documents\OCIO Models\Dashboard\202511 Model Portfolio Exposure`).

What it does, in order:
1. Runs Yang's two notebooks exactly as-is (they call the Terminal; a few minutes).
   Both are idempotent — if today's files already exist they are reused, so re-running
   after a hiccup is always safe.
2. Runs the **tripwire** on the two output files (`data YYYYMMDD v1.pkl` +
   `model YYYYMMDD v1.pkl`): expected keys, no duplicate rows, correct as-of date,
   row counts in the normal band.
3. Prints **`RESULT: PASS -- both PKLs safe to send`** — or a list of `FAIL:` reasons.

**If it FAILS:** read the reasons. The two common ones:
- `Bloomberg ... failed` → Terminal not running / not logged in. Fix, rerun.
- `as-of ... not in expected` after a market holiday → rerun as
  `run_daily_pull.bat --allow-stale 1`.
Anything else: send the printed output to Andrew's team — do NOT send the files.

**Env note (first run only):** the runner assumes the conda env `cma`. If your machine's env
has a different name: `set BBG_CONDA_ENV=<name>` then rerun.

## Step 2 — /bbg-send (in Claude, connected to the Opal gateway)

Wait ~1 minute after PASS (OneDrive syncs the output folder), then ask Claude:

> Send today's Bloomberg PKLs to the portal — run opal_data_refresh_upload with confirm.

What the tool does (all server-side — the big files never pass through the chat):
1. Finds today's two PKLs in the SharePoint output folder (your own SharePoint access).
2. Uploads them through the portal's /data-refresh channel.
3. Triggers the Yang data pipeline and **returns right after the trigger** (it does not wait
   for the run; the client connection drops near 120 s).

You get back the uploaded files, the `upload_id` and the `execution_id`. **Then read
`opal_data_refresh_status` with that execution id** until the run is terminal: it returns the
run's status and the LIVE portal manifest's displayed date, so you confirm **uploaded ✓ → pipeline ✓ →
displayed ✓**. If `opal_data_refresh_status` is not available to your identity, read the portal's
displayed date instead. If any leg fails, the tool says which and why — nothing half-lands silently.

Never re-send on a dropped transport.

A dropped reply does not mean the send failed: the
send landed. A repeat `confirm` of the same two files inside 30 minutes returns the first
execution id and fires nothing.

**Safe practice run:** `opal_data_refresh_upload with dry_run=true` uploads to the staging
area WITHOUT running the pipeline — use this the first time, or any time you want to test.

## What never changes

- Yang's notebooks are untouched — this wraps them.
- Bloomberg is only ever called from the terminal machine, same as clicking by hand.
- If the tripwire fails, nothing is sent. If the pipeline fails, the tool reports it —
  the portal keeps serving the previous day until a clean run lands.
