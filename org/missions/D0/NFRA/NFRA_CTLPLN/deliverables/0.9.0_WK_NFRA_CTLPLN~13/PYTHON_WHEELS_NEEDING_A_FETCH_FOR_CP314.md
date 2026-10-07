# Python wheels for Python 3.14 on 64-bit Windows: which packages in requirements.txt need a fetch

Task order NFRA_CTLPLN.TO-CT-k-2, amendment 6. Worker 0.9.0_WK_NFRA_CTLPLN~13. Generated from `org/devices/kit_python_wheels_cp314.json` (saved 2026-10-07T14:27:03Z). For the CTO (msg 106278).

## Result

The root `requirements.txt` has 67 installable lines. The target is Python 3.14 on win_amd64 (48 supported tags, computed with `packaging.tags` 24.2 for the target, not for the running 3.12). Nothing was fetched: the only pip calls were read-only (`pip --version`, `pip cache dir`, `pip cache list`, `pip config list`).

| Class | Count |
|---|---|
| WHEEL-ON-DISK | 0 |
| PURE-INSTALLED | 41 |
| ABI3-INSTALLED | 8 |
| NEEDS-FETCH | 18 |
| NOT-APPLICABLE | 0 |
| UNPARSED | 0 |

**No wheel FILE for any tag exists on this machine** (WHEEL-ON-DISK is 0): the pip cache holds 0 entries, and the kit pack output, the Downloads folder, this worktree and the base checkout hold no readable wheel (the one `.whl` under the repository is a 0-byte `numpy-1.26.4-cp312` file). So the 49 packages classed PURE-INSTALLED or ABI3-INSTALLED are re-packable from installed files only: that re-pack is NOT done in this pass. The tags are measured; that a re-packed wheel installs and imports on 3.14 is held, not proven.

## NEEDS-FETCH: 18 packages (a Dell cannot get these without a fetch or a wheel built elsewhere)

Every one is installed here only as a `cp312-cp312-win_amd64` build, which Python 3.14 refuses. None is absent from this machine.

| Package | Specifier | Version here | Why |
|---|---|---|---|
| catboost | ==1.2.10 | 1.2.10 | compiled for another Python only: cp312-cp312-win_amd64 |
| lxml | ==6.0.2 | 6.0.2 | compiled for another Python only: cp312-cp312-win_amd64 |
| matplotlib | ==3.11.1 | 3.11.1 | compiled for another Python only: cp312-cp312-win_amd64 |
| pandas | ==2.3.3 | 2.3.3 | compiled for another Python only: cp312-cp312-win_amd64 |
| pyarrow | ==18.1.0 | 18.1.0 | compiled for another Python only: cp312-cp312-win_amd64 |
| PyYAML | ==6.0.3 | 6.0.3 | compiled for another Python only: cp312-cp312-win_amd64 |
| websockets | ==16.0 | 16.0 | compiled for another Python only: cp312-cp312-win_amd64 |
| duckdb | ==1.5.0 | 1.5.0 | compiled for another Python only: cp312-cp312-win_amd64 |
| hdbscan | ==0.8.41 | 0.8.41 | compiled for another Python only: cp312-cp312-win_amd64 |
| kuzu | ==0.11.3 | 0.11.3 | compiled for another Python only: cp312-cp312-win_amd64 |
| numpy | ==2.4.2 | 2.4.2 | compiled for another Python only: cp312-cp312-win_amd64 |
| pyiceberg | ==0.9.1 | 0.9.1 | compiled for another Python only: cp312-cp312-win_amd64 |
| pywin32 | ==311 | 311 | compiled for another Python only: cp312-cp312-win_amd64 |
| scikit-learn | ==1.8.0 | 1.8.0 | compiled for another Python only: cp312-cp312-win_amd64 |
| pillow | ==12.1.1 | 12.1.1 | compiled for another Python only: cp312-cp312-win_amd64 |
| rpds-py | ==0.30.0 | 0.30.0 | compiled for another Python only: cp312-cp312-win_amd64 |
| scipy | ==1.17.1 | 1.17.1 | compiled for another Python only: cp312-cp312-win_amd64 |
| torch | ==2.10.0 | 2.10.0 | compiled for another Python only: cp312-cp312-win_amd64 |

The remedy for each is a cp314 win_amd64 wheel of the pinned version from an index, or a copy a Dell already holds. This document does not fetch, and does not test whether those wheels exist.

## PyMuPDF (the case that prompted this)

`PyMuPDF==1.27.1`: class **ABI3-INSTALLED**, installed here at 1.27.1 (satisfies the specifier: True), tags `cp310-abi3-win_amd64`. It is a stable-ABI build (`cp310-abi3-win_amd64`), so it fits Python 3.14 on win_amd64 and does NOT need a fetch; a build for 3.12 only would have. Evidence: `<site-packages:3.12>/pymupdf-1.27.1.dist-info`. Not proven: that this build imports on a real 3.14 (no 3.14 interpreter is on this machine).

## ABI3-INSTALLED: 8 (an installed build that fits 3.14; re-pack from RECORD, not done)

| Package | Specifier | Version here | Tags | Kind |
|---|---|---|---|---|
| bcrypt | ==5.0.0 | 5.0.0 | cp39-abi3-win_amd64 | abi3 |
| curl_cffi | ==0.13.0 | 0.13.0 | cp39-abi3-win_amd64 | abi3 |
| psutil | ==7.2.2 | 7.2.2 | cp37-abi3-win_amd64 | abi3 |
| PyMuPDF | ==1.27.1 | 1.27.1 | cp310-abi3-win_amd64 | abi3 |
| ruff | ==0.15.11 | 0.15.11 | py3-none-win_amd64 | no-abi-platform |
| cryptography | ==48.0.1 | 48.0.1 | cp311-abi3-win_amd64 | abi3 |
| safetensors | ==0.7.0 | 0.7.0 | cp38-abi3-win_amd64 | abi3 |
| tokenizers | ==0.22.2 | 0.22.2 | cp39-abi3-win_amd64 | abi3 |

`ruff` is `py3-none-win_amd64`, not stable-ABI: it fits 3.14 on win_amd64 and has no Python-version binding, and is classed here with a stated kind (row NFRA_CTLPLN-W13-S14). The CTO's msg 106117 says ruff was already sent to both Dells by Taildrop.

## PURE-INSTALLED: 41 (an installed pure-Python copy with a RECORD; re-pack offline, not done)

**Copies whose installed version does NOT satisfy the specifier: 0.**

Two lines carry no pin, so they satisfy trivially: botocore (installed 1.43.0); s3fs (installed 2026.6.0). The file's own header says the installed botocore 1.43.0 conflicts with boto3 1.42.54 (`pip check`), so a re-pack of the installed botocore would carry a version boto3 refuses; pin it before packing.

| Package | Specifier | Version here |
|---|---|---|
| anthropic | ==0.84.0 | 0.84.0 |
| beautifulsoup4 | ==4.14.3 | 4.14.3 |
| boto3 | ==1.42.54 | 1.42.54 |
| botocore | (none) | 1.43.0 |
| jsonschema | ==4.26.0 | 4.26.0 |
| mcp | ==1.26.0 | 1.26.0 |
| openpyxl | ==3.1.5 | 3.1.5 |
| pandas_market_calendars | ==5.4.0 | 5.4.0 |
| playwright | ==1.58.0 | 1.58.0 |
| pypdf | ==6.12.2 | 6.12.2 |
| pytest | ==9.0.2 | 9.0.2 |
| requests | ==2.32.5 | 2.32.5 |
| awscli | ==1.44.44 | 1.44.44 |
| pytest-cov | ==7.1.0 | 7.1.0 |
| anyio | ==4.12.1 | 4.12.1 |
| awswrangler | ==3.11.0 | 3.11.0 |
| feedparser | ==6.0.12 | 6.0.12 |
| httpx | ==0.28.1 | 0.28.1 |
| msal | ==1.39.0 | 1.39.0 |
| openai | ==2.24.0 | 2.24.0 |
| pdfminer.six | ==20251230 | 20251230 |
| pdfplumber | ==0.11.9 | 0.11.9 |
| PyJWT | ==2.11.0 | 2.11.0 |
| python-dateutil | ==2.9.0.post0 | 2.9.0.post0 |
| python-dotenv | ==1.2.2 | 1.2.2 |
| python-jose | ==3.3.0 | 3.3.0 |
| python-whois | ==0.9.6 | 0.9.6 |
| pytz | ==2025.2 | 2025.2 |
| referencing | ==0.37.0 | 0.37.0 |
| sentence-transformers | ==5.2.3 | 5.2.3 |
| starlette | ==0.52.1 | 0.52.1 |
| urllib3 | ==2.6.3 | 2.6.3 |
| uvicorn | ==0.42.0 | 0.42.0 |
| yfinance | ==1.2.0 | 1.2.0 |
| model2vec | ==0.8.2 | 0.8.2 |
| packaging | ==24.2 | 24.2 |
| python-docx | ==1.2.0 | 1.2.0 |
| python-pptx | ==1.0.2 | 1.0.2 |
| requests-aws4auth | ==1.3.2 | 1.3.2 |
| s3fs | (none) | 2026.6.0 |
| transformers | ==5.3.0 | 5.3.0 |

## Dependencies that are not lines of requirements.txt (73 names)

The tool does NOT follow dependencies: the file is stated to be the full list, and its own caveat is that a clean-start resolve is unverified. For each found copy (wheel or installed, of any class) the `Requires-Dist` names whose marker holds for the target and that are not a line of the file are listed below. This is the visible gap in a `pip install --no-index` of the file on a Dell.

Secondary read (not part of the saved JSON): the class of each undeclared dependency's installed copy on the 3.12 interpreter, by the same rules: ABI3-INSTALLED 2, NEEDS-FETCH 12, PURE-INSTALLED 59.

| Undeclared dependency | Installed copy here | Needed by |
|---|---|---|
| aiobotocore | PURE-INSTALLED: 3.7.0 py3-none-any | s3fs |
| aiohttp | NEEDS-FETCH: 3.14.1 compiled for another Python only: cp312-cp312-win_amd64 | s3fs |
| attrs | PURE-INSTALLED: 26.1.0 py3-none-any | jsonschema, referencing |
| cachetools | PURE-INSTALLED: 5.5.2 py3-none-any | pyiceberg |
| certifi | PURE-INSTALLED: 2026.1.4 py3-none-any | curl-cffi, httpx, requests |
| cffi | NEEDS-FETCH: 2.0.0 compiled for another Python only: cp312-cp312-win_amd64 | cryptography, curl-cffi |
| charset-normalizer | NEEDS-FETCH: 3.4.4 compiled for another Python only: cp312-cp312-win_amd64 | pdfminer-six, requests |
| click | NEEDS-FETCH: 8.3.1 editable install (no wheel can be re-packed from it) | pyiceberg, uvicorn |
| colorama | PURE-INSTALLED: 0.4.6 py2-none-any,py3-none-any | awscli, pytest |
| contourpy | NEEDS-FETCH: 1.3.3 compiled for another Python only: cp312-cp312-win_amd64 | matplotlib |
| coverage | NEEDS-FETCH: 7.13.5 compiled for another Python only: cp312-cp312-win_amd64 | pytest-cov |
| cycler | PURE-INSTALLED: 0.12.1 py3-none-any | matplotlib |
| distro | PURE-INSTALLED: 1.9.0 py3-none-any | anthropic, openai |
| docstring-parser | PURE-INSTALLED: 0.17.0 py3-none-any | anthropic |
| docutils | PURE-INSTALLED: 0.18.1 py2-none-any,py3-none-any | awscli |
| ecdsa | PURE-INSTALLED: 0.19.2 py2-none-any,py3-none-any | python-jose |
| et-xmlfile | PURE-INSTALLED: 2.0.0 py3-none-any | openpyxl |
| exchange-calendars | PURE-INSTALLED: 4.13.2 py3-none-any | pandas-market-calendars |
| filelock | PURE-INSTALLED: 3.25.2 py3-none-any | torch |
| fonttools | NEEDS-FETCH: 4.63.0 compiled for another Python only: cp312-cp312-win_amd64 | matplotlib |
| frozendict | PURE-INSTALLED: 2.4.7 py3-none-any | yfinance |
| fsspec | PURE-INSTALLED: 2026.6.0 py3-none-any | pyiceberg, s3fs, torch |
| graphviz | PURE-INSTALLED: 0.21 py3-none-any | catboost |
| greenlet | NEEDS-FETCH: 3.3.2 compiled for another Python only: cp312-cp312-win_amd64 | playwright |
| h11 | PURE-INSTALLED: 0.16.0 py3-none-any | uvicorn |
| httpcore | PURE-INSTALLED: 1.0.9 py3-none-any | httpx |
| httpx-sse | PURE-INSTALLED: 0.4.3 py3-none-any | mcp |
| huggingface-hub | PURE-INSTALLED: 1.6.0 py3-none-any | sentence-transformers, tokenizers, transformers |
| idna | PURE-INSTALLED: 3.11 py3-none-any | anyio, httpx, requests |
| iniconfig | PURE-INSTALLED: 2.3.0 py3-none-any | pytest |
| jinja2 | PURE-INSTALLED: 3.1.6 py3-none-any | model2vec, torch |
| jiter | NEEDS-FETCH: 0.13.0 compiled for another Python only: cp312-cp312-win_amd64 | anthropic, openai |
| jmespath | PURE-INSTALLED: 1.1.0 py3-none-any | boto3, botocore |
| joblib | PURE-INSTALLED: 1.5.3 py3-none-any | hdbscan, model2vec, scikit-learn |
| jsonschema-specifications | PURE-INSTALLED: 2025.9.1 py3-none-any | jsonschema |
| kiwisolver | NEEDS-FETCH: 1.5.0 compiled for another Python only: cp312-cp312-win_amd64 | matplotlib |
| mmh3 | NEEDS-FETCH: 5.2.1 compiled for another Python only: cp312-cp312-win_amd64 | pyiceberg |
| multitasking | PURE-INSTALLED: 0.0.12 py3-none-any | yfinance |
| networkx | PURE-INSTALLED: 3.6.1 py3-none-any | torch |
| peewee | PURE-INSTALLED: 4.0.0 py3-none-any | yfinance |
| platformdirs | PURE-INSTALLED: 4.9.2 py3-none-any | yfinance |
| plotly | PURE-INSTALLED: 6.9.0 py3-none-any | catboost |
| pluggy | PURE-INSTALLED: 1.6.0 py3-none-any | pytest, pytest-cov |
| protobuf | ABI3-INSTALLED: 6.33.5 cp310-abi3-win_amd64 | yfinance |
| pyasn1 | PURE-INSTALLED: 0.6.2 py3-none-any | python-jose |
| pydantic | PURE-INSTALLED: 2.12.5 py3-none-any | anthropic, mcp, openai, pyiceberg |
| pydantic-settings | PURE-INSTALLED: 2.13.1 py3-none-any | mcp |
| pyee | PURE-INSTALLED: 13.0.1 py3-none-any | playwright |
| pygments | PURE-INSTALLED: 2.19.2 py3-none-any | pytest |
| pyparsing | PURE-INSTALLED: 3.3.2 py3-none-any | matplotlib, pyiceberg |
| pypdfium2 | ABI3-INSTALLED: 5.7.1 py3-none-win_amd64 | pdfplumber |
| python-multipart | PURE-INSTALLED: 0.0.22 py3-none-any | mcp |
| regex | NEEDS-FETCH: 2026.2.28 compiled for another Python only: cp312-cp312-win_amd64 | transformers |
| rich | PURE-INSTALLED: 13.9.4 py3-none-any | pyiceberg |
| rsa | PURE-INSTALLED: 4.7.2 py3-none-any | awscli, python-jose |
| s3transfer | PURE-INSTALLED: 0.16.0 py3-none-any | awscli, boto3 |
| setuptools | PURE-INSTALLED: 82.0.1 py3-none-any | awswrangler, torch |
| sgmllib3k | PURE-INSTALLED: 1.0.0 py3-none-any | feedparser |
| six | PURE-INSTALLED: 1.17.0 py2-none-any,py3-none-any | catboost, python-dateutil |
| sniffio | PURE-INSTALLED: 1.3.1 py3-none-any | anthropic, openai |
| sortedcontainers | PURE-INSTALLED: 2.4.0 py2-none-any,py3-none-any | pyiceberg |
| soupsieve | PURE-INSTALLED: 2.8.3 py3-none-any | beautifulsoup4 |
| sse-starlette | PURE-INSTALLED: 3.3.3 py3-none-any | mcp |
| strictyaml | PURE-INSTALLED: 1.7.3 py3-none-any | pyiceberg |
| sympy | PURE-INSTALLED: 1.14.0 py3-none-any | torch |
| tenacity | PURE-INSTALLED: 9.1.4 py3-none-any | pyiceberg |
| threadpoolctl | PURE-INSTALLED: 3.6.0 py3-none-any | scikit-learn |
| tqdm | PURE-INSTALLED: 4.67.3 py3-none-any | model2vec, openai, sentence-transformers, transformers |
| typer | PURE-INSTALLED: 0.24.1 py3-none-any | transformers |
| typing-extensions | PURE-INSTALLED: 4.16.0 py3-none-any | anthropic, awswrangler, beautifulsoup4, mcp, openai, python-docx, python-pptx, sentence-transformers, torch |
| typing-inspection | PURE-INSTALLED: 0.4.2 py3-none-any | mcp |
| tzdata | PURE-INSTALLED: 2025.3 py2-none-any,py3-none-any | pandas |
| xlsxwriter | PURE-INSTALLED: 3.2.9 py3-none-any | python-pptx |

## Python interpreters this machine holds

- version 3.12: interpreter executable present: True; site-packages present: True; distributions read: 307; found by: py -0p, running interpreter, standard folder.
- version 3.14: interpreter executable present: False; site-packages present: True; distributions read: 0; found by: standard folder.
- version 3.12: interpreter executable present: True; site-packages present: True; distributions read: 7; found by: user site.
- Registry: HKCU PythonCore 3.12: InstallPath names a folder that does not exist; HKLM PythonCore 3.14: no InstallPath.
- A `Python314` folder exists under Program Files with an EMPTY site-packages and no `python.exe`: it is a shell, not an interpreter. This machine therefore cannot show what a 3.14 install holds (row NFRA_CTLPLN-W13-S15).

## What stays unread or unproven

- pip HTTP and wheel cache: 0 entries, 0 bytes; 0 read (0 bytes), 0 unreadable, 0 not read for budget. An empty cache is a measured zero, not an unreadable one.
- kit pack output (C:/tmp/kit-*): 14 directories walked, 0 `.whl` file(s) found, 0 identified as wheels, 0 unreadable, 0 not a wheel; walk cut by budget: False.
- user Downloads folder: 45597 directories walked, 0 `.whl` file(s) found, 0 identified as wheels, 0 unreadable, 0 not a wheel; walk cut by budget: False.
- repository (this worktree): 7584 directories walked, 1 `.whl` file(s) found, 0 identified as wheels, 0 unreadable, 1 not a wheel; walk cut by budget: False.
- repository (base checkout): 25564 directories walked, 1 `.whl` file(s) found, 0 identified as wheels, 0 unreadable, 1 not a wheel; walk cut by budget: False.
- Not read: any Dell's real interpreter and site-packages; wheels inside `.zip` archives; `node_modules` and `.git` trees (pruned from the repository walks); any index.
- Not proven: that a re-packed wheel (PURE or ABI3) installs and imports on 3.14; that cp314 wheels exist for the 18 NEEDS-FETCH pins; that the file resolves from a clean start.
- Compiled dependencies outside the list appear in the table above with their own class; each one marked NEEDS-FETCH there adds to the fetch list if the file is installed without a resolver.
