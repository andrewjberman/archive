# KIT_PYTHON312_PACK_RECORD -- the Python 3.12 kit: the whole dependency closure re-packed offline

Worker `0.9.0_WK_NFRA_CTLPLN~13`, task order `NFRA_CTLPLN.TO-CT-k-2` AMENDMENT 8, 2026-10-07. Claim: MEASURED on this machine (Python 3.12.10, Windows, 64-bit), no request to any index, nothing installed outside two scratch folders. The kit is NOT committed and NOT sent anywhere.

## 1. The kit

- Path: `C:/tmp/kit-python312-pack-20261007` (outside every git tree).
- Contents: 163 files = 161 wheels + `MANIFEST.json` + `requirements-kit.txt`.
- Total bytes: wheels 513,889,970; the folder 514,026,127 (du -sb).
- Target (read from the closure file): `cp312-win_amd64`; every wheel's tags were checked to fit it by `kit_python_wheels.py`'s tag logic.
- Closure file: `org/devices/intake/closure_cp312_win_amd64.json`; its saved last line: `INTAKE-CLOSURE target=cp312-win_amd64 lines=67 closure=162 dependencies_added=95 pure=114 fits=47 needs_fetch=1 unknown_not_installed=0 specifier_conflicts=2 fixed_point=True ok=True`
  The issuer's line (AMENDMENT 8): `INTAKE-CLOSURE target=cp312-win_amd64 lines=67 closure=162 dependencies_added=95 pure=114 fits=47 needs_fetch=1 unknown_not_installed=0 specifier_conflicts=2 fixed_point=True ok=True`. **Identical, character for character.**
- `requirements.txt` at commit `bc10584676`, sha256 7635687a9a31bb12, unchanged since the closure was read: True.

Wheels by class: PURE 114, FITS 47 (total 161 of the 162 closure members; the 162nd is `click`, below).

By tag: py3-none-any x 102; cp312-cp312-win_amd64 x 36; py2.py3-none-any x 12; cp39-abi3-win_amd64 x 3; cp37-abi3-win_amd64 x 2; cp310-abi3-win_amd64 x 2; py3-none-win_amd64 x 2; cp311-abi3-win_amd64 x 1; cp38-abi3-win_amd64 x 1.

By role: 67 requirement lines (kind `line`) first in the file's order, then 94 dependencies sorted by name; comment lines in `requirements-kit.txt` mark the two groups. The versions are the installed ones: `botocore==1.43.0`, not the specifier.

### Ten largest wheels

| wheel | bytes | class |
|---|---|---|
| `torch-2.10.0-cp312-cp312-win_amd64.whl` | 113,671,127 | FITS |
| `catboost-1.2.10-cp312-cp312-win_amd64.whl` | 98,007,425 | FITS |
| `playwright-1.58.0-py3-none-any.whl` | 36,808,327 | PURE |
| `scipy-1.17.1-cp312-cp312-win_amd64.whl` | 36,535,373 | FITS |
| `pyarrow-18.1.0-cp312-cp312-win_amd64.whl` | 25,092,322 | FITS |
| `pymupdf-1.27.1-cp310-abi3-win_amd64.whl` | 19,236,692 | FITS |
| `botocore-1.43.0-py3-none-any.whl` | 14,970,073 | PURE |
| `duckdb-1.5.0-cp312-cp312-win_amd64.whl` | 13,053,784 | FITS |
| `numpy-2.4.2-cp312-cp312-win_amd64.whl` | 12,298,119 | FITS |
| `ruff-0.15.11-py3-none-win_amd64.whl` | 11,270,717 | FITS |

## 2. Everything NOT carried, and why

- **`click` 8.3.1 (NO-METADATA)**: editable install (no wheel can be re-packed from it); needs the checked route (a file fetched and assessed)
- **specifier conflict, `botocore`**: installed and carried `botocore 1.43.0`; `awscli` (installed 1.44.44) requires `botocore ==1.42.54`. The kit carries what this machine runs and is not a consistent resolution for `awscli`; `pip check` on the receiver will say so.
- **specifier conflict, `botocore`**: installed and carried `botocore 1.43.0`; `boto3` (installed 1.42.54) requires `botocore <1.43.0,>=1.42.54`. The kit carries what this machine runs and is not a consistent resolution for `boto3`; `pip check` on the receiver will say so.
- MODIFIED packages (installed bytes differ from their own RECORD, or a listed file is missing): **0**. Failed packages: **0**.

Packed but PARTIAL (6): files RECORD lists outside `site-packages` (not scripts, not generated launchers) are not packed:

- `catboost`: 14 path(s), e.g. `../../etc/jupyter/nbconfig/notebook.d/catboost-widget.json`
- `hdbscan`: 1 path(s), e.g. `../../dist_metrics.pxd`
- `fonttools`: 1 path(s), e.g. `../../share/man/man1/ttx.1`
- `greenlet`: 1 path(s), e.g. `../../Include/greenlet/greenlet.h`
- `plotly`: 7 path(s), e.g. `../../share/jupyter/labextensions/jupyterlab-plotly/install.json`
- `sympy`: 1 path(s), e.g. `../../share/man/man1/isympy.1`

Scripts: launchers pip regenerates from entry points are not packed; real scripts and binaries go under `<name>-<version>.data/scripts/` (ruff.exe, aws, pdfminer and docutils tools). 18 scripts in 5 packages had their first line put back to `#!python` (row W13-S22).

## 3. Disk

- Estimate before the cut, from the RECORD sizes of the 161 selected packages: **1.667 GB installed**; kit at most that, the whole-kit scratch install that again; `estimate: ... worst case 27.14 GB would remain after kit plus scratch (floor 10.0 GB) -> OK` (free was 30.48 GB by disk_usage).
- Measured: kit 514,026,127 bytes (0.51 GB); each scratch install 2,075 MB.
- Free space on C: (df -k, KB available): 29 GB at the start; 20,299,636 before the first whole-kit install; 15,104,376 after it; 5,011,748 at its lowest (other work filling the disk -- row W13-S24); 16,155,076 before the second install; 14,611,388 at the end.
- **Scratch space returned: 0.** The recursive removal of the scratch folders was denied by the permission system twice and was not routed around (row W13-S20). Left: `C:/tmp/kit-python312-scratch-20261007` and `C:/tmp/kit-python312-scratch2-20261007` (2,075 MB each) and `C:/tmp/kit-repro-20261007` (21 MB). Deleting these three returns about 4.2 GB.

## 4. The tool's last lines on the real kit

```
PY-REPACK target=cp312-win_amd64 selected=161 built=161 verified=161 partial=6 modified=0 failed=0 bytes=513889970 ok=True
PY-KIT-VERIFY wheels=161 verified=161 stray=0 ok=True
PY-KIT-INSTALL-ALL python=3.12.10 wheels=161 installed=161 requirement_lines=67 imported=62 import_missing_dep=2 failed=3 ok=True
```

`ok=True` on the install line means every wheel installed (`installed == wheels`); the import counts are the finding, as in AMENDMENT 7. Reproducibility: the `pandas` wheel (10,973,660 bytes) was cut twice with the file's mtime unchanged between runs and once more as part of the kit; all three SHA-256 equal `fca31b73457d8249fbcbb9c3c16a27a42896f72a40a6cf49084a99fa0bdfeca2`.

The first whole-kit run (`install_check` as first written, before the two changes in row W13-S21) read: `PY-KIT-INSTALL-ALL python=3.12.10 wheels=161 installed=161 requirement_lines=67 imported=60 import_missing_dep=3 failed=4 ok=True`. It is kept here because the difference is the finding in that row: the isolation had to be corrected in two places that were the check's fault, not the kit's.

## 5. Requirement lines that did not fully import (isolated `python -I`, sys.path = scratch target + standard library)

5 of 67 lines; for each, the first error line as the tool printed it, and my classification. **Every module in the table also fails with a plain `python -c "import <module>"` on this machine's own environment with the same first line** (row W13-S23), so none is something the kit lost.

| requirement line | not imported | first error | class |
|---|---|---|---|
| `catboost==1.2.10` | `_catboost`, `_hnsw` | ModuleNotFoundError: No module named '_catboost' | other: names in `top_level.txt` that are not top-level modules; `catboost` itself imported |
| `pyarrow==18.1.0` | `__dummy__` | ModuleNotFoundError: No module named '__dummy__' | other: same kind; `pyarrow` itself imported |
| `duckdb==1.5.0` | `adbc_driver_duckdb` | ModuleNotFoundError: No module named 'adbc_driver_manager' | missing_dep: `adbc_driver_manager` is not installed here either and is not in the closure; `duckdb`, `_duckdb` imported |
| `uvicorn==0.42.0` | `uvicorn` | ModuleNotFoundError: No module named 'click' | missing_dep: `click` is the one package not carried; it is not importable on this machine either (editable install) |
| `pywin32==311` | 17 of 59: PyISAPI_loader, adsi, authorization, axcontrol, axdebug, axscript, bits, dde, directsound, exchange, ifilter, internet, mapi, perfmondata, propsys, shell, taskscheduler | ModuleNotFoundError: No module named 'PyISAPI_loader' (dde: ImportError: This must be an MFC application - try 'import win32ui' first) | other: `top_level.txt` names that are sub-modules of `win32com`/`win32comext`, not top-level; 42 modules incl. win32api, pythoncom, pywintypes imported |

No `dll_or_native` failure occurred. The other 62 lines imported all their modules, among them `torch`, `numpy`, `scipy`, `pandas`, `PyMuPDF`, `lxml`, `matplotlib`, `mcp` and `sentence-transformers`.

### The isolation control

`test_kit_python_repack.py` case 15: `pip` is installed only in this machine's real site-packages; a plain `python -c "import pip"` returns 0 (positive control), and `import_isolated(<empty scratch>, 'pip')` returns `('missing', 'pip', ...)`. A probe module in the target that asserts no `site-packages` entry is on `sys.path` (and that `ctypes`, `json`, `zipfile` import from the standard library) passes. A module that re-adds the real site-packages path and imports `pip` is reported `BorrowedModuleError` and fails. Case 17: a `.pth` inside the target is honoured; one that names a path outside it is refused (`ForeignPathError`).

Two deliberate departures from the strictest reading, both in row W13-S21: the target's own `.pth` files are processed (pywin32 needs it, and a real install does it), and `USERNAME`, `USERPROFILE`, `LOCALAPPDATA`, `APPDATA` stay in the scrubbed environment (torch calls `getpass.getuser()` at import). No `PYTHON*` variable and no machine path reaches the subprocess.

## 6. Per requirement line: the modules imported (run 2, the recorded run)

| line | result | modules |
|---|---|---|
| `anthropic==0.84.0` | imported | anthropic |
| `bcrypt==5.0.0` | imported | bcrypt |
| `beautifulsoup4==4.14.3` | imported | bs4 |
| `boto3==1.42.54` | imported | boto3 |
| `botocore==1.43.0` | imported | botocore |
| `catboost==1.2.10` | import_failed | [other]: _catboost: own module missing: _catboost  (imported 1 of 3 modules; not imported: _catboost[other],_hnsw[other]) |
| `curl_cffi==0.13.0` | imported | curl_cffi |
| `jsonschema==4.26.0` | imported | jsonschema |
| `lxml==6.0.2` | imported | lxml |
| `matplotlib==3.11.1` | imported | matplotlib,mpl_toolkits,pylab |
| `mcp==1.26.0` | imported | mcp |
| `openpyxl==3.1.5` | imported | openpyxl |
| `pandas==2.3.3` | imported | pandas |
| `pandas_market_calendars==5.4.0` | imported | pandas_market_calendars |
| `playwright==1.58.0` | imported | playwright |
| `psutil==7.2.2` | imported | psutil |
| `pyarrow==18.1.0` | import_failed | [other]: __dummy__: own module missing: __dummy__  (imported 1 of 2 modules; not imported: __dummy__[other]) |
| `PyMuPDF==1.27.1` | imported | fitz,pymupdf |
| `pypdf==6.12.2` | imported | pypdf |
| `pytest==9.0.2` | imported | _pytest,py,pytest |
| `PyYAML==6.0.3` | imported | _yaml,yaml |
| `requests==2.32.5` | imported | requests |
| `websockets==16.0` | imported | websockets |
| `ruff==0.15.11` | imported | ruff |
| `awscli==1.44.44` | imported | awscli |
| `pytest-cov==7.1.0` | imported | pytest_cov |
| `anyio==4.12.1` | imported | anyio |
| `awswrangler==3.11.0` | imported | awswrangler |
| `cryptography==48.0.1` | imported | cryptography |
| `duckdb==1.5.0` | import_missing_dep | : missing adbc_driver_manager (importing adbc_driver_duckdb)  (imported 2 of 3 modules; not imported: adbc_driver_duckdb) |
| `feedparser==6.0.12` | imported | feedparser |
| `hdbscan==0.8.41` | imported | hdbscan |
| `httpx==0.28.1` | imported | httpx |
| `kuzu==0.11.3` | imported | kuzu |
| `msal==1.39.0` | imported | msal |
| `numpy==2.4.2` | imported | numpy |
| `openai==2.24.0` | imported | openai |
| `pdfminer.six==20251230` | imported | pdfminer |
| `pdfplumber==0.11.9` | imported | pdfplumber |
| `pyiceberg==0.9.1` | imported | fb303,hive_metastore,pyiceberg |
| `PyJWT==2.11.0` | imported | jwt |
| `python-dateutil==2.9.0.post0` | imported | dateutil |
| `python-dotenv==1.2.2` | imported | dotenv |
| `python-jose==3.3.0` | imported | jose,jose.backends |
| `python-whois==0.9.6` | imported | whois |
| `pytz==2025.2` | imported | pytz |
| `pywin32==311` | import_failed | [other]: PyISAPI_loader: own module missing: PyISAPI_loader  (imported 42 of 59 modules; not imported: PyISAPI_loader[other],adsi[other],authorization[other],axcontrol[other],axdebug[other],axscript[other],bits[other],dde[other],directsound[other],exchange[other],ifilter[other],internet[other],mapi[other],perfmondata[other],propsys[other],shell[other],taskscheduler[other]) |
| `referencing==0.37.0` | imported | referencing |
| `scikit-learn==1.8.0` | imported | sklearn |
| `sentence-transformers==5.2.3` | imported | sentence_transformers |
| `starlette==0.52.1` | imported | starlette |
| `urllib3==2.6.3` | imported | urllib3 |
| `uvicorn==0.42.0` | import_missing_dep | : missing click (importing uvicorn)  (imported 0 of 1 modules; not imported: uvicorn) |
| `yfinance==1.2.0` | imported | yfinance |
| `model2vec==0.8.2` | imported | model2vec |
| `packaging==24.2` | imported | packaging |
| `pillow==12.1.1` | imported | PIL |
| `python-docx==1.2.0` | imported | docx |
| `python-pptx==1.0.2` | imported | pptx |
| `requests-aws4auth==1.3.2` | imported | requests_aws4auth |
| `rpds-py==0.30.0` | imported | rpds |
| `s3fs==2026.6.0` | imported | s3fs |
| `safetensors==0.7.0` | imported | safetensors |
| `scipy==1.17.1` | imported | scipy |
| `tokenizers==0.22.2` | imported | tokenizers |
| `torch==2.10.0` | imported | functorch,torch,torchgen |
| `transformers==5.3.0` | imported | transformers |

## 7. The commands another machine runs, in order, once its Python 3.12 is installed

The tool `org/devices/kit_python_repack.py` uses the standard library only on the receiving side; copy the kit folder `kit-python312-pack-20261007` and the repo checkout, then:

1. `python org/devices/kit_python_repack.py verify --from <kit folder>`  -- expect `PY-KIT-VERIFY wheels=161 verified=161 stray=0 ok=True`.
2. `python org/devices/kit_python_repack.py install-check --from <kit folder> --with-deps-from-kit --scratch <a NEW empty folder>`  -- one install of the whole kit into `<scratch>/all`, then each of the 67 requirement lines imported in isolation; expect `PY-KIT-INSTALL-ALL ... wheels=161 installed=161 requirement_lines=67 imported=62 import_missing_dep=2 failed=3 ok=True` (the same 5 lines as section 5, if the Dell behaves as this machine). Then delete the scratch folder.
3. On the receiver's own decision: `python -m pip install --no-index --no-deps --find-links <kit folder> -r <kit folder>/requirements-kit.txt --user`.
4. `click` is separate (not in the kit; the checked route). `python -m pip check` will report the two `botocore` conflicts (awscli, boto3): expected, see section 2.

## 8. What stays unproven

- This machine is not a Dell. A Dell's own run of the three commands is the proof there: its Python 3.12 patch level, its CPU (the compiled wheels were built for this machine's 64-bit Windows and are generic cp312 / abi3 wheels), and the Visual C++ runtime DLLs the compiled packages are likely to need, which the kit does not carry.
- Import is not use: 62 of 67 lines imported all their top-level modules; no function of any package was called. Packages that need a display, a service or a credential were not exercised.
- `pywin32`'s post-install step (COM registration, `pywin32_postinstall.py`) was not run; `pywintypes` and `win32api` imported through its `.pth` in the target, as in a real install; registration is a Dell decision.
- The 6 PARTIAL packages lack their non-library files (Jupyter lab extensions, man pages, one header); the Python modules are complete.
- The installed bytes of all 161 packages equal their own RECORD hashes (MODIFIED 0), but RECORD is the copy's own claim: that these bytes equal what an index published was not checked, and no index was asked.
- `click` and everything outside the 67 lines' closure (the portal's bun tree, Terraform providers) are other kits.
- The wheels were rebuilt, not downloaded: their SHA-256 differ from any index file by construction.

