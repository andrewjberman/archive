<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-03-20-clspt2-003-ds</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-03-20</date>
    <status>complete</status>
    <project_code>ADVI_CLSPT2</project_code>
  </metadata>

  <objective>
    Migrate 12_build_composition_artifacts.py from the static ETF_CLASSIFICATIONS
    dict (~116 hardcoded items) to the DynamoDB-backed ETFClassifier. Without this,
    running classify_bd_securities.py (OpenAI enrichment) improves 06b mix output
    but has ZERO effect on script 12 composition output — the two scripts would
    diverge on classification of the same holdings.
  </objective>

  <context>
    File: data/black_diamond/scripts/gold/12_build_composition_artifacts.py

    Current state: Script 12 has its own inline classification system:
    - Lines 91-224: static ETF_CLASSIFICATIONS dict + ASSET_NAME_TO_TICKER + _OPAL_ETF_OVERRIDES
    - Lines 226-229: _TICKER_CLASS_MAP builder
    - Lines 232-296: classify_series() — 6-layer vectorized classifier using static dicts
    - Line 78-84: _ASSET_CLASS_LABELS with 5 classes (equity, fixed_income,
      structured_notes, cash, other)

    Target state: Same pattern as 06b_build_client_mix_timeseries.py:
    - `from lib.etf_classifier import ETFClassifier` (line 70 in 06b)
    - classify_series() delegates to ETFClassifier.instance().classify() per row
    - _ASSET_CLASS_LABELS updated to 4-class taxonomy matching 06b

    06b's approach (reference implementation):
    - _MIX_ASSET_CLASSES = ['equity', 'fixed_income', 'alternatives'] (line 146)
    - classify_holding() calls ETFClassifier.instance().classify(ticker, asset_name)
    - Returns 'equity' | 'fixed_income' | 'alternatives' | ''
    - '' means unclassified — treated as 'other' in composition context
    - Cash is residual in 06b (total - classified), but in script 12 composition
      it should remain an explicit class since holdings have explicit cash positions

    Taxonomy alignment (CRITICAL):
    - Current script 12 'structured_notes' -> new 'alternatives' (ETFClassifier
      returns 'alternatives' for SHIELD, ANNUIT, BUFFER, etc.)
    - Current script 12 'cash' -> stays 'cash' (ETFClassifier returns '' for
      CASH_USD, regex catches CASH/SWEEP/MONEY MARKET)
    - Current script 12 'other' -> stays 'other' (ETFClassifier '' for truly unknown)
    - This gives 5 composition classes: equity, fixed_income, alternatives, cash, other
  </context>

  <scope>
    <files>
      <file action="modify">data/black_diamond/scripts/gold/12_build_composition_artifacts.py</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      Add ETFClassifier import at the top of the file:
        from lib.etf_classifier import ETFClassifier

      This is the same import 06b uses (line 70). lib/etf_classifier.py and
      lib/__init__.py are already on S3 and deployed (CLSUNI).
    </requirement>

    <requirement id="2">
      Update _ASSET_CLASS_LABELS (line 78-84) to use 'alternatives' instead
      of 'structured_notes':

      _ASSET_CLASS_LABELS = {
          'equity':       'Equities',
          'fixed_income': 'Fixed Income',
          'alternatives': 'Alternatives',
          'cash':         'Cash',
          'other':        'Other',
      }

      The composition view keeps 5 classes (unlike 06b's 4-class + residual)
      because composition shows actual holdings per class and "Other" is a
      meaningful bucket for truly unclassifiable securities.
    </requirement>

    <requirement id="3">
      Replace the classify_series() function (lines 232-296) with an
      ETFClassifier-backed version. The new implementation should:

      def classify_series(ticker_series: pd.Series, name_series: pd.Series) -> pd.Series:
          classifier = ETFClassifier.instance()
          def _classify(ticker, asset_name):
              result = classifier.classify(ticker, asset_name)
              if not result:
                  # ETFClassifier returns '' for cash-like and unknown
                  # Distinguish: regex-matched cash items vs truly unknown
                  name = str(asset_name or '').upper()
                  if any(kw in name for kw in ('CASH', 'SWEEP', 'MONEY MARKET', 'MMKT')):
                      return 'cash'
                  return 'other'
              return result  # 'equity' | 'fixed_income' | 'alternatives'

          return pd.Series(
              [_classify(t, n) for t, n in zip(
                  ticker_series.fillna(''), name_series.fillna('')
              )],
              index=ticker_series.index,
              dtype='object'
          )

      This delegates to ETFClassifier (which reads bd-securities DynamoDB)
      and only adds the cash/other distinction that ETFClassifier doesn't make
      (it returns '' for both).
    </requirement>

    <requirement id="4">
      Remove ALL static classification data that is now redundant:
      - Lines 91-224: ETF_CLASSIFICATIONS dict, ASSET_NAME_TO_TICKER dict,
        _OPAL_ETF_OVERRIDES dict (all now in bd-securities DynamoDB)
      - Lines 226-229: _TICKER_CLASS_MAP builder
      - Any regex patterns used only by the old classify_series (_RE_STRUCTURED,
        _RE_CASH, _RE_FIXED_INCOME if they exist)

      Do NOT remove _ASSET_CLASS_LABELS or TOP_N or FIRM_ID or BUCKET constants.
      Do NOT remove _build_composition() or any other function besides classify_series.

      The _OPAL_ETF_OVERRIDES mappings (DIVZ, IDVZ, PFDE, PFOE, PCHI) are already
      in bd-securities as name_aliases — ETFClassifier Layer 2 handles them.
    </requirement>

    <requirement id="5">
      Verify the classify_series call site at line 550 is unchanged:
        lots['asset_class'] = classify_series(lots['ticker'], lots['asset_name'])
      This line should not need to change — same function signature, same output type.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">ETFClassifier imported from lib.etf_classifier</criterion>
    <criterion id="2">No static ETF_CLASSIFICATIONS dict in the file</criterion>
    <criterion id="3">No ASSET_NAME_TO_TICKER dict in the file</criterion>
    <criterion id="4">_ASSET_CLASS_LABELS uses 'alternatives' not 'structured_notes'</criterion>
    <criterion id="5">classify_series delegates to ETFClassifier.instance().classify()</criterion>
    <criterion id="6">Cash positions (CASH_USD, SWEEP, MONEY MARKET) classify as 'cash'</criterion>
    <criterion id="7">File runs without import errors when lib/__init__.py and lib/etf_classifier.py are present</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do NOT change _build_composition() — only the classification input changes</constraint>
    <constraint>Do NOT change the output shape of firm_composition.json or advisor composition.json</constraint>
    <constraint>Do NOT change 06b — it already uses ETFClassifier correctly</constraint>
    <constraint>Do NOT change lib/etf_classifier.py — it is deployed and live</constraint>
    <constraint>Commit with --author="0.4.0_DS_ClientPlatform &lt;0.4.0_DS_ClientPlatform@opal.agent&gt;"</constraint>
    <constraint>No emojis in code (CLAUDE.md rule 13)</constraint>
  </constraints>

  <dependencies>
    <dependency agent="none" status="clear">
      lib/etf_classifier.py exists on CLOUD (CLSUNI). lib/__init__.py exists.
      Both are on S3 at s3://opal-data-bd/code/gold/lib/. No blockers.
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="commit">Script 12 migrated to ETFClassifier, committed to CLOUD</deliverable>
  </deliverables>
</task_order>
