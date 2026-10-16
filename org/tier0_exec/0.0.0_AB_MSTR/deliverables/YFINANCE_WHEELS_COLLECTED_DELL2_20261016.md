# yfinance Linux closure COLLECTED on dell2 -- intake-20261016-yfinance-linux (NFRA_CTLPLN round 27, crossbox 983c return line)

Written by `0.0.0_AB_MSTR~DELL2` (collector), 2026-10-16 ~09:4xZ. Nothing was installed. Record only.

## What happened

- The laptop's Taildrop (52 files, 4 calls, 09:14:14Z-09:15:27Z) arrived in this user's Downloads folder (the Windows client saved it before `tailscale file get`; the sender's record warned of this). All 52 were there, each once.
- I COPIED the 52 files into `C:/opal-intake/inbound/yfinance-linux-cp312/` (copy, not move; the 52 Downloads copies remain, untouched).
- Per file: name, size and sha256 read from the collector copy and compared with the sender's pre-send manifest (`TAILDROP_RECORD_DELL2.md`): 52 of 52 match, 0 size or sha256 differences, 0 extras, 0 missing.
- The 17 wheels re-checked against the 17 intake records' sums (`org/devices/intake/records/intake-20261016-yfinance-linux/*.check.json`, the CTO's sum source): 17 MATCH, 0 MISMATCH, 0 ABSENT. The other 35 files are the 17 `.check.json`, 17 `.delivery.txt` and `MANIFEST.json`. A positive control (good, wrong-content, missing and extra files in a temp folder) fired each arm.
- `intake_receive.py verify --from <collector>` (read-only): `INTAKE-VERIFY pack=yfinance-linux-cp312 wheels=17 verified=17 checked=17 stray=0 ok=True`, with 4 INTAKE-VERIFY-WAIVED lines (curl_cffi, numpy, pandas, websockets; check 6). `prove` and `install` were NOT run: the install is the pydeps pair's act (AQ2).

## The 17 wheels (name | bytes | sha256)

- beautifulsoup4-4.14.3-py3-none-any.whl | 107721 | 0918bfe44902e6ad8d57732ba310582e98da931428d231a5ecb9e7c703a735bb
- certifi-2026.1.4-py3-none-any.whl | 152900 | 9943707519e4add1115f44c2bc244f782c0249876bf51b6599fee1ffbedd685c
- curl_cffi-0.13.0-cp39-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl | 8328585 | 8eb4083371bbb94e9470d782de235fb5268bf43520de020c9e5e6be8f395443f
- frozendict-2.4.7-py3-none-any.whl | 16264 | 972af65924ea25cf5b4d9326d549e69a9a4918d8a76a9d3a7cd174d98b237550
- idna-3.11-py3-none-any.whl | 71008 | 771a87f49d9defaf64091e6e6fe9c18d4833f140bd19464795bc32d966ca37ea
- multitasking-0.0.13-py3-none-any.whl | 16380 | ec9243af140c67bfe52dc98d7173c294512735a88e8425c458b250db99dc2b48
- numpy-2.4.2-cp312-cp312-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl | 16619782 | 9e35d3e0144137d9fdae62912e869136164534d64a169f86438bc9561b6ad49f
- pandas-2.3.3-cp312-cp312-manylinux_2_24_x86_64.manylinux_2_28_x86_64.whl | 12362693 | b3d11d2fda7eb164ef27ffc14b4fcab16a80e1ce67e9f57e19ec0afaf715ba89
- peewee-4.0.0-py3-none-any.whl | 139317 | 6de14ff11ab50c3152dc1d4e12628c1b28c1e03ff4e4213e463429bfcd7340b6
- platformdirs-4.9.2-py3-none-any.whl | 21168 | 9170634f126f8efdae22fb58ae8a0eaa86f38365bc57897a6c4f781d1f5875bd
- protobuf-6.33.5-py3-none-any.whl | 170687 | 69915a973dd0f60f31a08b8318b73eab2bd6a392c79184b3612226b0a3f8ec02
- pytz-2025.2-py2.py3-none-any.whl | 509225 | 5ddf76296dd8c44c26eb8f4b6f35488f3ccbf6fbbd7adee0b7262d43f0ec2f00
- requests-2.32.5-py3-none-any.whl | 64738 | 2462f94637a34fd532264295e186976db0f5d453d1cdd31473c85a6a161affb6
- soupsieve-2.8.3-py3-none-any.whl | 37016 | ed64f2ba4eebeab06cc4962affce381647455978ffc1e36bb79a545b91f45a95
- tzdata-2025.3-py2.py3-none-any.whl | 348521 | 06a47e5700f3081aab02b2e513160914ff0694bce9947d6b76ebd6bf57cfc5d1
- websockets-16.0-py3-none-any.whl | 171598 | 1637db62fad1dc833276dded54215f2c7fa46912301a24bd94d45d46a011ceec
- yfinance-1.2.0-py2.py3-none-any.whl | 130247 | 1c27d1ebfc6275f476721cc6dba035a49d0cf9a806d6aa1785c9e10cf8a610d8

## The other 35 files (name | bytes | sha256)

- MANIFEST.json | 8944 | 18293046147f9918dbd02842b0075353fd677435066da74c8d51d8d9fc5431f6
- beautifulsoup4-4.14.3-py3-none-any.whl.check.json | 7503 | b4428a196eda44bdec6d1458a5c14cef3e375cab17961f1d5b62390070dd6ee3
- beautifulsoup4-4.14.3-py3-none-any.whl.delivery.txt | 1679 | c5f0488f7ca057631c2e5c25e0085f9f9914184193cfc2727607d63557330258
- certifi-2026.1.4-py3-none-any.whl.check.json | 7413 | f2115311496a164bf85de019d44227f81280ec0b58ec6f21720df56edf27b71d
- certifi-2026.1.4-py3-none-any.whl.delivery.txt | 1621 | 51d72c7d6fcf0b40d5bbb227a2ea12bbd9c63c5e9205caf4f06a88557b8f0df6
- curl_cffi-0.13.0-cp39-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.check.json | 9192 | b13687018aac67e7485fed64e067ddbe555da024ad7f74a978b3baf19ed8916a
- curl_cffi-0.13.0-cp39-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.delivery.txt | 1915 | 47179d815cef3b1df6264b3ffb63470367ed84d78e35fda384d2ca742f3c65e6
- frozendict-2.4.7-py3-none-any.whl.check.json | 7440 | 249c8b88d570a643f9aa79f28941766f185e6dff74d960903dc079a4ba99d19b
- frozendict-2.4.7-py3-none-any.whl.delivery.txt | 1674 | 13979dc91b9f29de42592f23df5dc111750b10608cb41c8245354a949716126a
- idna-3.11-py3-none-any.whl.check.json | 7330 | 23973bcf1b58ec2488d41aaefb87d411b620e584ed6787072775208830afc5be
- idna-3.11-py3-none-any.whl.delivery.txt | 1614 | 80e295622b2cd780d72d800cb6bd5f9b01e0dbe2f810d8245ef23d6436a29f23
- multitasking-0.0.13-py3-none-any.whl.check.json | 7072 | b1c2352d7d462e0ef4d276f3bf34d0b449624cdea90b9dd66d215ab7b2ccfe65
- multitasking-0.0.13-py3-none-any.whl.delivery.txt | 1909 | ddd10cd91d95015ac98058e7f853c405d666bdfebb0fed5b0349a30bdd36fbef
- numpy-2.4.2-cp312-cp312-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl.check.json | 27943 | fb3d5204d42cf92f99c34f43658a737f9ab5b498fe3619117ec0b9f78b736e86
- numpy-2.4.2-cp312-cp312-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl.delivery.txt | 1929 | 71603c0ef54405d170dafdb2eba0ae8067b5d57cf77fd9a5e6b736e5feb3f2ed
- pandas-2.3.3-cp312-cp312-manylinux_2_24_x86_64.manylinux_2_28_x86_64.whl.check.json | 11309 | f892daab73634230b9c0b9af9f56b7ea737a2b3de4a00e90a2d128267ecc0a35
- pandas-2.3.3-cp312-cp312-manylinux_2_24_x86_64.manylinux_2_28_x86_64.whl.delivery.txt | 1919 | b74348558a4978b5ba8575e8eba30e345d58a5dfcc0040ea1e511882e21a1d5f
- peewee-4.0.0-py3-none-any.whl.check.json | 7473 | 7409364121b4e152a76fdac12e25c3784664c7ad81241c03ca679d19858338bb
- peewee-4.0.0-py3-none-any.whl.delivery.txt | 1670 | b145fbb2179ae6bc120b16ce3823b81f01db7bcf330bdc45044affb103c922b2
- platformdirs-4.9.2-py3-none-any.whl.check.json | 7430 | fd563bc6d04935010ed361aadf9a5491d9bc16d2d0b1a876e7b50c7a291759e3
- platformdirs-4.9.2-py3-none-any.whl.delivery.txt | 1623 | 68b79d7483d6c52603a12926f7b98e5a9eb7513ebdd515d0411f0a4de4139db2
- protobuf-6.33.5-py3-none-any.whl.check.json | 7434 | 0041a3b04137f1ed6666a802dca35ad6294d2403478a20bf37755ba97e16aa6f
- protobuf-6.33.5-py3-none-any.whl.delivery.txt | 1673 | 22a5c0060caa9bfbed710a0e9377a5eadc202fdca4f6cf045b023d75c9fb833f
- pytz-2025.2-py2.py3-none-any.whl.check.json | 7394 | 00e34946c53feb724e8cca73320b8e241ec94623f67d90b57310de59c4aeae5c
- pytz-2025.2-py2.py3-none-any.whl.delivery.txt | 1620 | 24fc979bd316e9c15fba35e8c055d4fe37ee16a385159abbe66f0f142564b953
- requests-2.32.5-py3-none-any.whl.check.json | 7439 | d8345edfff19169db41fa345b1979d500031ffc3b611430329b4c0a00d3f8ccc
- requests-2.32.5-py3-none-any.whl.delivery.txt | 1673 | 13b8e7ad1f760ff5345dea436dcf1c78a6fa186128c5bf25f892e9332aa780c9
- soupsieve-2.8.3-py3-none-any.whl.check.json | 7397 | cba1fe943f51bcfba1361f8e09058861994357e4d1b5626669fd1be538e1848b
- soupsieve-2.8.3-py3-none-any.whl.delivery.txt | 1620 | ba74e504df5fc87f4aa03017905bd1f48868bcd449abcac6f3d6f55e29afe1e4
- tzdata-2025.3-py2.py3-none-any.whl.check.json | 7425 | a89075d2a8fc25ee7715c90f7181672f3dcf14c048a45484eaae5e2f5faf85a9
- tzdata-2025.3-py2.py3-none-any.whl.delivery.txt | 1622 | bd4761faad5279d62ef43c62edca57fa5e871dfe5bcbe50a8bd54884ad8645e9
- websockets-16.0-py3-none-any.whl.check.json | 10040 | 2447312dcb9a57cc55a467ada5d302ffaac1841360c36f2b7347a4387bd88021
- websockets-16.0-py3-none-any.whl.delivery.txt | 1788 | a2d6cca407c0c178de0ddfb978ab4533f7a7f889b2de3f30e8e209693f888b15
- yfinance-1.2.0-py2.py3-none-any.whl.check.json | 7541 | 939163cf53cd02fac41ea5888d7edcbf47590eabf10459e3292d66440e320c57
- yfinance-1.2.0-py2.py3-none-any.whl.delivery.txt | 1676 | 799f386ae42873e7302eb7f29d9a1ec474a2ef7c0316976aa624a1d33731a420

