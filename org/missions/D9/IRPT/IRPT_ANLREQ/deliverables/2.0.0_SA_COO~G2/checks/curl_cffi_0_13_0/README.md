# curl_cffi 0.13.0 exception fixture (issuer 2.0.0_SA_COO~G2)

Source: the approved wheel curl_cffi-0.13.0-cp39-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (intake batch intake-20261016-yfinance-linux).

- `curl_cffi/requests/exceptions.pyfix`: BYTE-EXACT copy of the wheel member (sha256 562c8bc775c78a2fecee48eb3b71a154e55786adbf52c61f01097c30fc039c43).
- `curl_cffi/curl.pyfix`: the EXACT text of `class CurlError` from the wheel's curl_cffi/curl.py, with its two import lines; the rest of that module is compiled-library glue and is not copied.
- `curl_cffi/const.pyfix`: BYTE-EXACT copy of the wheel member (a pure-Python IntEnum module; sha256 77962ebd30933cb61f5f0283cf93ee44ec20faac5f27b9c530a32226d5d47cff).
The members carry the suffix `.pyfix` so the repository's lint gate (which would rewrite a third-party file) does not read them. To use them, copy the folder to a temp directory renaming every `.pyfix` to `.py`, put that directory on sys.path, and `import curl_cffi.requests.exceptions`: you get the real classes (HTTPError, RequestException, Timeout, ConnectionError, ...).
