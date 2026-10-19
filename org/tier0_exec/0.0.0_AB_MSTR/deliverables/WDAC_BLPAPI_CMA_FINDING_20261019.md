# Site Z: why the cma interpreter cannot import blpapi (WinError 4551), answer to 1.0.0_SA_CTO~Z msg 35940

Author 0.0.0_AB_MSTR~Z, 2026-10-19 ~11:15-11:45Z. Session not elevated. All times below are stated with their zone.

## MEASURED

1. **Reproduced.** `C:\Anaconda\envs\cma\python.exe -c "import blpapi"` raises `OSError: [WinError 4551] An Application Control policy has blocked this file`.
   `C:\Users\Opal Bloomberg\AppData\Local\Programs\Python\Python311\python.exe` (PY_AWS) imports the same package.
2. **The policy is Smart App Control in ENFORCE mode.** `HKLM\SYSTEM\CurrentControlSet\Control\CI\Policy` `VerifiedAndReputablePolicyState` = 1 (0 off, 1 enforce, 2 evaluation).
   Code Integrity events 3077 and 3033 (Microsoft-Windows-CodeIntegrity/Operational) name the policy id beginning `{0283ac0f-fff1-`; `C:\Windows\System32\CodeIntegrity\CiPolicies\Active\{0283AC0F-FFF1-49AE-ADA1-8A933130CAD6}.cip` exists (dated 2024-04-01).
3. **The blocked file is `ffiutils.cp311-win_amd64.pyd`** (15,360 bytes, NOT signed), loaded by `C:\Anaconda\envs\cma\python.exe` (validly signed, Anaconda Inc.). `blpapi3_64.dll` itself is validly signed.
4. **The decision is not about the bytes or the path.**
   - cma's `ffiutils` and PY_AWS's `ffiutils` have the SAME SHA-256 (4348BF23...4748). One loads, one is blocked.
   - A copy of cma's blpapi package under `%TEMP%` is blocked under the cma interpreter AND under the PY_AWS interpreter.
   - The PY_AWS instance, loaded IN PLACE by the cma interpreter (importlib from its own folder), loads: `OK ... blpapi 3.26.4.2`.
   So the allowed thing is that specific file instance, not the content, the location class or the loading process.
5. **Since when.** Daily-pull logs in `%USERPROFILE%\opal_bbg_logs`: `bbg_tplus1_20261018_070002.log` (2026-10-18 07:03 local) ran the cma pull with DAPI UP and no 4551. `bbg_tplus1_20261019_070002.log` (2026-10-19 07:01 local = 11:01Z) is the first log with 4551. Only two logs in the 38 held contain it (the second is the manual recovery log).
6. **What changed in that window (local time):** no reboot (boot 2026-10-15 21:48); no CI policy file written after 2026-10-13; latest hotfixes 2026-10-14 and 2026-10-16; two Defender security-intelligence updates (2026-10-18 21:58 and 2026-10-19 03:02).

## NOT DETERMINED

- WHY cma's instance was allowed on 10-18 and is not on 10-19. Smart App Control judges an unsigned file by cloud reputation and a per-file verdict it caches. A flipped or expired verdict is consistent with 3 and 4 but is NOT shown here. The Defender updates are a coincidence of timing, not a cause.
- The Code Integrity log holds 393 block/audit events, oldest 2026-10-19 07:16 local, so it rolls over faster than the first block of this morning; it cannot date the flip.

## WHAT IS NEEDED (nothing below was done)

- Smart App Control cannot be turned back on once off without resetting Windows. Do NOT switch it off to fix this; that is Andrew's call.
- Working route without any policy change: have the cma interpreter load the PY_AWS instance in place before `tia` imports blpapi (an importlib preload, tested above), for example a `sitecustomize.py` in the cma env or a line at the top of `bbgtml_meter.py`. It rests on the PY_AWS instance staying trusted. The owner of the cma environment and the pull script (0.0.3_BG_BBGTerminal) decides; I did not edit either.
- Separate row, filed by the BBG seat: `scheduled_daily_pull.cmd` line 115 `goto :prune` skips the isolated legs when the precondition fails.
