@echo off
REM OPAL_BBGTML /bbg-pull -- double-click daily runner (leg 1 + leg 2 tripwire).
REM Requires: Bloomberg Terminal running + logged in on this machine.
REM Conda env: set BBG_CONDA_ENV to override; defaults to "cma" (Yang's env name).

set "ENVNAME=%BBG_CONDA_ENV%"
if "%ENVNAME%"=="" set "ENVNAME=cma"

call conda activate %ENVNAME% 2>nul
if errorlevel 1 (
  echo ERROR: could not activate conda env "%ENVNAME%".
  echo        If your env has a different name, set BBG_CONDA_ENV and rerun,
  echo        e.g.:  set BBG_CONDA_ENV=myenv ^&^& run_daily_pull.bat
  pause
  exit /b 1
)

python "%~dp0run_daily_pull.py" %*
set "RC=%ERRORLEVEL%"
echo.
if "%RC%"=="0" (echo DONE: pull + tripwire PASS. Next: /bbg-send in Claude.) else (echo FAILED: read the messages above.)
pause
exit /b %RC%
