# VERIFY #17 -- target: unknown

- is_real: **False**
- confidence: **refuted**
- corrected_severity: low

## Reasoning
The flag's core mechanism ("null household_id -> whole column reads back as float64 -> astype(str) yields '12345.0' -> guard passes it -> key platinum/clients/12345.0/... and JSON household_id='12345.0' -> mass 404s") is refuted at its load-bearing step: the household_id column is pandas nullable Int64, not numpy float64.

Trace: INF_D_06 loads the primary dim from silver/api_dims/household (load_household_dim, line 190-196) via _read_s3_parquet -> pd.read_parquet(BytesIO(...)) (lines 111-113). That silver artifact is written by build_household, which calls coerce_silver_ids(merged) immediately before return (convert_orion_api_to_silver.py:180); coerce_silver_ids does pd.to_numeric(...).astype('Int64') (_orion_api_silver_lib.py:255-270) per the codified "SILVER ID DTYPE CONVENTION: all _id columns MUST be Int64 (nullable)". The write path is pa.Table.from_pandas(df, preserve_index=False)+pq.write_table (_orion_api_silver_lib.py:340-341), which embeds pandas extension-type metadata, so pd.read_parquet restores Int64 (NOT float64).

I reproduced the EXACT write->read->astype->guard->key path (with a null household row present) on pandas 2.3.3 / pyarrow 18.1.0: post-read dtype is Int64; hd['household_id'].astype(str) (line 365) yields '12345' for populated ids (not '12345.0'); so at line 537 '12345'.isdigit() is True -> int(12345), and line 541 key is correctly platinum/clients/12345/timeseries.json with JSON household_id=12345 (int). The flagged '12345.0' path and the resulting 404 cannot fire.

The fallback path (line 204) is also Int64 (INF_A_00 coerces household_id to Int64 at lines 238-239 and coerce_id_columns at save) and only runs if the primary load throws.

Residual, adjacent (NOT the flagged defect, hence severity low not zero): a genuinely null household_id renders under Int64.astype(str) as the string '<NA>' (not 'nan'); the guard passes it through, so a null-household account would land in a phantom platinum/clients/<NA>/timeseries.json. This is a real but much milder, contingent edge behavior with a different token that does not affect any populated household and does not match the flag's claim of every populated household being mis-keyed to '<id>.0'.
