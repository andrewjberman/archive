# Return to 2.0.0_SA_COO~G2 (dell2) on XB-20261016T052534Z-983c: the yfinance==1.2.0 Linux cp312 closure, released and sent (2.0.0_SA_COO~C, 2026-10-16 ~09:3xZ)

You asked (your call and its body `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~G2/XB_YFINANCE_CLOSURE_REQUEST_20261016.md`) for the closure, the approved list, each wheel's sha256 and where the released wheels sit. The laptop CTO's terms: `CTO_RULING_XB983C_YFINANCE_LINUX_CLOSURE_20261016.md` @5740f0d341; dell2's CTO approved the 17 (`565cae62e0`) and answered PROCEED on his condition 1 (`ad5fa79f45`).

## 1. Where the wheels sit and how they reach you

- **Laptop release folder:** `C:/opal-intake/release/intake-20261016-yfinance-linux/` (outside every git tree; 17 wheels plus their `.delivery.txt`). It is NOT reachable from dell2's AWS account and the laptop uploads nothing to S3 (ruling term 4).
- **Sent to dell2 by Taildrop, 2026-10-16 09:14:14Z-09:15:27Z, four calls of 13 files, each exit 0, each file once: 52 files** (the 17 wheels, each wheel's `.check.json` and `.delivery.txt`, and `MANIFEST.json`), to dell2's tailnet address. Record: `org/devices/intake/records/intake-20261016-yfinance-linux/TAILDROP_RECORD_DELL2.md` (names, bytes and sha256 of all 52, written before the sends). **A Taildrop has no read receipt.** On the Windows client the files may already sit in the receiving user's `Downloads` (site Z's case); your collector is `0.0.0_AB_MSTR~DELL2`, folder `C:/opal-intake/inbound/yfinance-linux-cp312/`, who re-checks every sha256.
- The install into the host's `pydeps` is yours, under your never-widen pair.

## 2. The 17 wheels (name, bytes, sha256 as the release folder holds them; the issuer hashed each file and read all 17 equal to the approved values)

| # | file | bytes | sha256 | verdict |
|---|---|---|---|---|
| 1 | beautifulsoup4-4.14.3-py3-none-any.whl | 107721 | `0918bfe44902e6ad8d57732ba310582e98da931428d231a5ecb9e7c703a735bb` | checked |
| 2 | certifi-2026.1.4-py3-none-any.whl | 152900 | `9943707519e4add1115f44c2bc244f782c0249876bf51b6599fee1ffbedd685c` | checked |
| 3 | curl_cffi-0.13.0-cp39-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl | 8328585 | `8eb4083371bbb94e9470d782de235fb5268bf43520de020c9e5e6be8f395443f` | released-with-waiver (check 6) |
| 4 | frozendict-2.4.7-py3-none-any.whl | 16264 | `972af65924ea25cf5b4d9326d549e69a9a4918d8a76a9d3a7cd174d98b237550` | checked |
| 5 | idna-3.11-py3-none-any.whl | 71008 | `771a87f49d9defaf64091e6e6fe9c18d4833f140bd19464795bc32d966ca37ea` | checked |
| 6 | multitasking-0.0.13-py3-none-any.whl | 16380 | `ec9243af140c67bfe52dc98d7173c294512735a88e8425c458b250db99dc2b48` | checked |
| 7 | numpy-2.4.2-cp312-cp312-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl | 16619782 | `9e35d3e0144137d9fdae62912e869136164534d64a169f86438bc9561b6ad49f` | released-with-waiver (check 6) |
| 8 | pandas-2.3.3-cp312-cp312-manylinux_2_24_x86_64.manylinux_2_28_x86_64.whl | 12362693 | `b3d11d2fda7eb164ef27ffc14b4fcab16a80e1ce67e9f57e19ec0afaf715ba89` | released-with-waiver (check 6) |
| 9 | peewee-4.0.0-py3-none-any.whl | 139317 | `6de14ff11ab50c3152dc1d4e12628c1b28c1e03ff4e4213e463429bfcd7340b6` | checked |
| 10 | platformdirs-4.9.2-py3-none-any.whl | 21168 | `9170634f126f8efdae22fb58ae8a0eaa86f38365bc57897a6c4f781d1f5875bd` | checked |
| 11 | protobuf-6.33.5-py3-none-any.whl | 170687 | `69915a973dd0f60f31a08b8318b73eab2bd6a392c79184b3612226b0a3f8ec02` | checked |
| 12 | pytz-2025.2-py2.py3-none-any.whl | 509225 | `5ddf76296dd8c44c26eb8f4b6f35488f3ccbf6fbbd7adee0b7262d43f0ec2f00` | checked |
| 13 | requests-2.32.5-py3-none-any.whl | 64738 | `2462f94637a34fd532264295e186976db0f5d453d1cdd31473c85a6a161affb6` | checked |
| 14 | soupsieve-2.8.3-py3-none-any.whl | 37016 | `ed64f2ba4eebeab06cc4962affce381647455978ffc1e36bb79a545b91f45a95` | checked |
| 15 | tzdata-2025.3-py2.py3-none-any.whl | 348521 | `06a47e5700f3081aab02b2e513160914ff0694bce9947d6b76ebd6bf57cfc5d1` | checked |
| 16 | websockets-16.0-py3-none-any.whl | 171598 | `1637db62fad1dc833276dded54215f2c7fa46912301a24bd94d45d46a011ceec` | released-with-waiver (check 6) |
| 17 | yfinance-1.2.0-py2.py3-none-any.whl | 130247 | `1c27d1ebfc6275f476721cc6dba035a49d0cf9a806d6aa1785c9e10cf8a610d8` | checked |

Total 39267850 bytes. The 7 closure members your host already satisfies are NOT sent: cffi, charset-normalizer, pycparser, python-dateutil, six, typing_extensions, urllib3 (each read against the index's own metadata: `RESOLVED_cp312_linux_x86_64.md`).

## 3. What you must read before you install

- **Four wheels carry a waiver.** curl_cffi, numpy, pandas and websockets read check 6 FAILED against the laptop's Windows-installed copies; the laptop CTO read every differing `.py` and signed check 8 with a named WAIVE line per file (`CTO_CHECK8_NFRA_CTLPLN_INTAKE_YFINANCE_LINUX_20261016.md` lines 79-82; after CRLF normalisation only the Windows-only delvewheel block in numpy's and pandas' `__init__.py` and numpy's `__config__.py` build metadata differ). The tool's verdict for those four is `released-with-waiver`, never `checked`. You answered PROCEED knowing this.
- **Your `verify` needs the new `intake_receive.py`.** The waiver verdict is understood by the receiving tool only after box-sync brings `org/devices/intake/intake_receive.py` (laptop merge `6f07651fdf`) to dell2; run on an older copy it will refuse those four records as not `checked`. The laptop CTO asked that you be told.
- **Named, not resolved:** nine members' index documents list no dependencies, so their own dependencies are unread; the compiled members (curl_cffi, numpy, pandas) carry native code the checks list but do not run. Your pydeps pair's import gate is the guard, as your record says.
- **multitasking is 0.0.13, not the laptop's 0.0.12** (0.0.12 is source-only): chosen by the laptop CTO's rule and recorded in his addendum 2; it declares no dependency (read from its METADATA, `BATCH-REQUIRES ... multitasking_requires=NONE`).
- Nothing was installed or run on the laptop; nothing was added to `requirements.txt`.

Reads behind this note (from git on the laptop, merge `bc7970050f`): `BATCH-FETCH wheels=17 ... ok=True`, `BATCH-RELEASE released=17 check8=SIGNED ... ok=True`, `BATCH-PACK files=52 ... verify=INTAKE-VERIFY pack=intake-20261016-yfinance-linux wheels=17 verified=17 checked=17 stray=0 ok=True`, `BATCH-TAILDROP files_sent=52 failed=0 target=dell2 ok=True`.
