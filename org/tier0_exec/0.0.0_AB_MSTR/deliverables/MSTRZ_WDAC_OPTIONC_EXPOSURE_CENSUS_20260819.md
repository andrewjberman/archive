# WDAC Option-C exposure census — site Z Bloomberg box, 2026-08-19 ~13:4xZ

**Authorization (Andrew-direct at the MSTR~Z console, 2026-08-19, verbatim):** *"No i dont
feel like dealing with IT right now let's just scan via Option C and identify if there is
anything else on this device we need to address"* — MSP exemption DEFERRED by his word;
Option C (trusted-wheel hygiene) adopted; this census is the identification deliverable.
Read-only throughout; env untouched pending the 08-20 07:00 acceptance.

## Sweep 1 — Code Integrity event history (the bouncer's own record)

Window: **08-04 10:30 → 08-19 08:49 ET** (full log retention, 1,329 events; absence claims
beyond 08-04 are UNMEASURED). Block/audit events: 195, fully attributed:

| count | file | verdict |
|---|---|---|
| 8 | `cma\...\psutil\_psutil_windows.pyd` | all 08-19 (incident + repros); REMEDIATED (pip wheel) |
| 2 | `cma\...\win32\pywintypes313.dll` | 08-19 07:00 only; UNREMEDIATED (dodging via `pywin32_system32\` copy) |
| 176 | `SentinelOne\...\SentinelAmsi64.dll` (via svchost) + 9 via SecurityHealthService | MSP's own EDR agent vs the policy, since 08-04. Not ours; zero pipeline impact; hand to MSP whenever that talk happens |

**No other file has ever been flagged in the window.** The Opal-pipeline exposure that has
actually FIRED is exactly the two known members.

## Sweep 2 — native-binary census by env

**cma env (Bloomberg pull): 412 binaries / 40 packages.** Mechanism refinement: most conda
builds are Authenticode-SIGNED and pass outright (numpy, pandas, scipy, mkl, matplotlib,
sklearn, zmq, tornado, bottleneck, PyQt6, ...). blpapi3_64.dll is SIGNED (Bloomberg). The
exposed class is the UNSIGNED minority, cross-referenced against the pull's real import
chain (notebook imports measured: pandas/numpy/matplotlib/seaborn/sklearn/scipy/
statsmodels/tia — NO cvxpy/solvers/debugpy):

| unsigned member | in pull chain? | state |
|---|---|---|
| psutil (pip 7.2.2) | YES (ipykernel) | passing via reputation — the 08-19 fix |
| pywin32 family (`win32\`, `pywin32_system32\`, `win32comext\` — pywintypes/pythoncom, conda-owned) | YES (jupyter_core on win) | **P1: one member already blocked once; swap to PyPI pywin32 wheel post-acceptance** |
| debugpy (conda, pydevd .pyds) | lazy (ipykernel debug only) | P3 optional pip swap; loads only if debugging activates |
| rpds, markupsafe (pip wheels) | nbclient/jinja chain | passing (mainstream wheels); no action |
| cvxpy solver stack (_cvxcore, scs, clarabel, osqp, qdldl), isapi, pythonwin | NO | out of chain; leave |

**Python311 env (vendor_watch hourly + fabric tooling): 493 binaries / 61 packages,
essentially ALL unsigned** (PyPI wheels are not Authenticode-signed). Protection = ISG
reputation only. EXERCISED passing post-policy: vendor_watch ran clean 10:09 ET today
(rc=0, watermarks read); comp-tools/fabric python ran all day. Residual with **no local
remedy**: the niche-wheel tail (kuzu, faiss, duckdb, curl_cffi, pyroaring, mmh3, hf_xet,
winpty) has thinner distribution → less certain reputation; if one is ever blocked, that IS
the MSP conversation — nothing Option C can do pre-emptively.

## Sweep 3 — unattended surfaces (non-Microsoft scheduled tasks)

Opal-owned: `OPAL_BBGTML_daily_pull` (cma; the incident), `OPAL_vendor_watch` (Python311;
exercised clean today), `OPAL_autolaunch_agents` (powershell+wt, signed),
`OPAL_BLOOMBERG-FreezeTripwire` (wscript, signed). Vendor: Bloomberg Updater, OneDrive,
Take Control (N-able), Chrome PEH, SharePoint_Timer bat. No other Python-loading
unattended surface found.

## The plan (post-acceptance, one act, per the adopted Option C)

AFTER the 08-20 07:00 scheduled fire is read (env frozen until then):
1. **P1** pip force-reinstall pywin32 in cma (closes the known-blocked member #2).
2. **P2** reconcile conda-meta vs disk for psutil (+ pywin32 after swap) so no conda
   operation can silently resurrect blocked binaries; pin pip-owned.
3. **P3 (optional, cheap)** pip swap debugpy.
4. Re-exercise: full ad-hoc end-to-end run + zero new CodeIntegrity events = PASS.

**Honest bound on Option C:** it rides Microsoft's reputation graph, which we do not
control. It closes the two fired members and the resurrection path; it cannot pre-clear
the niche tail, and a policy tightening from reputation to signature-required breaks all
unsigned wheels at once. The MSP path (deferred by Andrew's word) remains the only class
close. Detection stays the schedule's exit contract + daily guardrail (moratorium: no new
monitors built).
