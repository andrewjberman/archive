# Factor Scanner v2.1 - System Reference

**Generated from actual code**: November 3, 2025
**Source of truth**: Active scripts + Factor_Scanning_Model.xlsm

---

## System Overview

**Factor Scanner v2.1** is an Excel-based quantitative screening tool that:
1. Lets users select factors and weights in Excel
2. Automatically updates rankings when weights change
3. Supports 6 universes (S&P 500, Russell 1000, MSCI EAFE, etc.)
4. Covers 255 factors across 11 categories

**Key File**: `Factor_Scanning_Model.xlsm`

---

## How It Works

### User Workflow

1. **Select Universe** (Tab 1, Cell C2)
   - Choose from: S&P 500, Russell 1000, Russell 1000 Value, MSCI ACWI ex-US, MSCI EAFE, MSCI EAFE Value

2. **Select Factors** (Tab 1, Factor Bank)
   - Toggle YES/NO in "Active" column for any of 255 factors
   - Save and close Excel file

3. **Run Update** (Windows Explorer)
   - Double-click `02_MODEL_REFRESH.bat`
   - Script detects changes and updates Excel file

4. **Adjust Weights** (Tab 4, Column B)
   - Change weight percentages (must sum to 100%)
   - Rankings auto-update instantly (if VBA enabled)

### File Structure

```
Factor_Scanner.V2/
├── Factor_Scanning_Model.xlsm      # Main Excel file
├── 02_MODEL_REFRESH.bat            # Quick update launcher
├── data_tables/
│   └── Screening_DIVZ_IDVZ_20251028.xlsx  # Source data (255 factors)
└── scripts/
    ├── python/                     # Python automation scripts
    └── vba/                        # Excel VBA macros
```

---

## Excel File Structure

### Tab 1: 1-Configuration
**Purpose**: Factor selection interface

**Key Areas**:
- Cell C2: Universe dropdown
- Selected Factors table: Current active factors
- Factor Bank: All 255 factors with YES/NO toggles

**User edits**: Toggle YES/NO, select universe

### Tab 2: 2-Ranked Securities
**Purpose**: Final ranked list (read-only)

**Columns**:
- Ticker, Name, Composite Score
- Individual factor percentile ranks

**Updated by**: Python script (quick_update_weights.py)

### Tab 3: 3-Factor Data
**Purpose**: Complete factor dataset (read-only)

**Contains**: All securities × all selected factors
**Source**: Copied from `data_tables/Screening_DIVZ_IDVZ_20251028.xlsx`

### Tab 4: 4-Security Scanner
**Purpose**: **PRIMARY SCORING TAB** - Interactive weights

**Key Features**:
- Column B (rows 6-12): Weight percentages (user editable)
- Composite scores: Excel formulas that auto-recalculate
- Auto-sort: VBA sorts by composite score when weights change

**User edits**: Change weights, watch scores update

---

## Active Scripts

### Python Scripts (6 files)

#### 1. `quick_update_weights.py` ⭐ PRIMARY SCRIPT
**What it does**: Intelligent decision tree for model updates

**4 Operations**:
1. **Both universe + factors changed** → Full rebuild (Tab 2 + Tab 4)
2. **Universe changed only** → Update Tab 2, switch Tab 4 universe
3. **Factors changed only** → Ensure Tab 2 current, rebuild Tab 4
4. **No changes** → Re-sort Tab 4 only

**When to run**: After changing factors or universe in Tab 1

**How to run**: Double-click `02_MODEL_REFRESH.bat`

**Input**: Reads Tab 1 (selected factors, universe)
**Output**: Updates Tab 2 and Tab 4
**Key fix**: Composite scores use Excel formulas (not static values)

#### 2. `surgical_repair.py` ⭐ EMERGENCY REPAIR
**What it does**: Rebuilds Tab 4 from scratch if corrupted

**When to use**:
- Composite scores show static values instead of formulas
- Tab 1/Tab 4 out of sync
- Corrupted worksheet data

**How to run**: `python scripts/python/surgical_repair.py`

**What it fixes**:
- Restores Excel formulas for composite scores
- Rebuilds factor columns from Tab 3
- Applies proper formatting

#### 3. `canonical_factor_mapping.py` (utility)
**What it does**: Maps factor codes ↔ display names ↔ data columns

**Problem solved**: Three-way naming:
- Tab 1 uses codes: `bv`, `sales_gr_1yr`
- Tab 4 uses display names: `Book Value`, `Sales Growth (1 Year)`
- Tab 3 uses column headers: `Book Value`, `Sales Growth\n(1 Year)`

**Used by**: quick_update_weights.py, surgical_repair.py

#### 4. `factor_definitions_registry.py` (utility)
**What it does**: Provides descriptions for all 255 factors

**Example**:
```python
'bv': 'Book value of equity; total assets minus total liabilities'
'sales_gr_1yr': 'One-year historical sales growth; year-over-year revenue growth'
```

**Used by**: export_factor_descriptions.py

#### 5. `export_factor_descriptions.py` (utility)
**What it does**: Exports factor definitions to Excel/CSV for reference

**When to use**: Need factor descriptions outside Excel

#### 6. `calculate_predictive_power_score.py` (analysis)
**What it does**: Calculates PPS (Predictive Power Score) for factors

**When to use**: Quality analysis of factor predictive power

### VBA Scripts (4 files)

#### 1. `Tab1_Combined_VBA.vba`
**What it does**: Tab 1 automation

**Features**:
- Auto-updates "Selected Factors" table when YES/NO changes
- Green highlighting for selected factors
- Popup reminder to run 02_MODEL_REFRESH.bat after changes

#### 2. `Tab3_Combined_VBA.vba`
**What it does**: Tab 3 formatting

**Features**:
- Alternating row colors
- Conditional formatting for percentile ranks

#### 3. `Tab4_Combined_VBA.vba` ⭐ AUTO-SORT
**What it does**: Tab 4 auto-reranking

**Key feature**: `Worksheet_Calculate` event
- Triggers when weights change
- Automatically re-sorts table by composite score
- Updates rank numbers in real-time

**User experience**: Change weight → scores recalculate → table auto-sorts

#### 4. `Workbook_Open_VBA.vba`
**What it does**: Welcome message on workbook open

### Batch Files (2 files)

#### 1. `01_INSTALL_PYTHON_AND_LIBRARIES.bat`
**What it does**: One-time Python setup

**Installs**: Python, pandas, numpy, openpyxl

#### 2. `02_MODEL_REFRESH.bat` ⭐ PRIMARY LAUNCHER
**What it does**: Runs quick_update_weights.py with safety checks

**Safety features**:
- Checks Python is installed
- Auto-installs required libraries if missing
- Reminds user to close Excel file first

---

## Data Flow

```
User changes factors/universe in Tab 1
    ↓
Save & close Excel
    ↓
Run 02_MODEL_REFRESH.bat
    ↓
quick_update_weights.py reads Tab 1
    ↓
Script determines operation (1, 2, 3, or 4)
    ↓
Script updates Tab 2 and/or Tab 4
    ↓
User reopens Excel
    ↓
User changes weights in Tab 4
    ↓
Excel formulas recalculate composite scores
    ↓
VBA auto-sorts table (if enabled)
    ↓
User sees updated rankings instantly
```

---

## Key Technical Details

### Composite Score Formula (Tab 4)
**Formula structure** (example with 3 factors):
```
= (I9*$B$6 + K9*$B$7 + M9*$B$8) / 100
```

Where:
- I9, K9, M9 = Factor percentile scores (0-100)
- $B$6, $B$7, $B$8 = Weight percentages (must sum to 100%)
- Result: Weighted composite score (0-100)

**Why formulas, not static values**: Instant recalculation when weights change

### Universe Column Mapping
```python
UNIVERSE_OPTIONS = {
    'S&P 500': 'wt_ivv',
    'Russell 1000': 'wt_iwb',
    'Russell 1000 Value': 'wt_iwd',
    'MSCI ACWI ex-US': 'wt_acwx',
    'MSCI EAFE': 'wt_efa',
    'MSCI EAFE Value': 'wt_efv'
}
```

### Data Source
**File**: `data_tables/Screening_DIVZ_IDVZ_20251028.xlsx`
**Date**: October 28, 2025
**Factors**: 255 factors across 11 categories
**Securities**: ~3,000+ securities
**Update frequency**: Monthly (date in filename)

---

## Factor Categories (11)

1. **Size** (11 factors): mkt_val, bv, ev, sales, assets, etc.
2. **Efficiency** (11 factors): asset_turn_chg_1yr, receiv_turn_chg_1yr, etc.
3. **Growth** (25 factors): sales_gr_1yr, eps_gr_1yr, ocf_gr_1yr, etc.
4. **Management** (11 factors): asset_gr_1yr, capex_gr_1yr, debt_iss_gr_1yr, etc.
5. **Profitability** (28 factors): roe, roa, roic, ebit_margin, etc.
6. **Quality** (26 factors): accruals, fcf_accruals, asset_quality, etc.
7. **Sentiment** (29 factors): earn_rev_up, earn_rev_down, rec_chg, etc.
8. **Systematic** (38 factors): beta, vol, mom, reversal, etc.
9. **Value** (30 factors): ev_ebit, pe, pb, pcf, etc.
10. **Yield** (27 factors): div_yld, fcf_yld, earn_yld, etc.
11. **Institutional** (19 factors): active_pctout, passive_pctout, hedge_pctout, etc.

**Total**: 255 factors

---

## Troubleshooting

### "No changes detected"
**Cause**: Script didn't detect factor or universe changes
**Fix**: Verify Tab 1 Active column or universe was actually changed and saved

### Composite scores don't recalculate
**Cause**: Formulas replaced with static values
**Fix**: Run `surgical_repair.py` to restore formulas

### Table doesn't auto-sort
**Cause**: VBA macros not enabled
**Fix**: Enable macros when opening Excel, or sort manually

### "Permission denied" error
**Cause**: Excel file is still open
**Fix**: Close all Excel files, run script again

### Wrong factors in Tab 4
**Cause**: Tab 1/Tab 4 out of sync
**Fix**: Run `surgical_repair.py` to rebuild from Tab 1

---

## Version History

### v2.1 (November 3, 2025) - Current
- ✅ Intelligent decision tree (4 operations)
- ✅ Excel formulas for composite scores
- ✅ Non-destructive updates (preserves VBA)
- ✅ Canonical factor mapping (100% coverage)
- ✅ Tab 1/Tab 4 synchronization validation

### v2.0 (October 30, 2025)
- ✅ Surgical repair script
- ✅ Formula-based composite scores
- ✅ Efficient bulk operations

### v1.0 (Pre-October 2025)
- Initial release
- Basic factor selection and ranking

---

## File Locations

### Active Files
```
scripts/python/
├── quick_update_weights.py          ⭐ Primary update script
├── surgical_repair.py               ⭐ Emergency repair
└── utils/
    ├── canonical_factor_mapping.py  (Factor code ↔ name mapping)
    ├── factor_definitions_registry.py (255 factor descriptions)
    └── export_factor_descriptions.py (Export definitions)

scripts/vba/
├── Tab1_Combined_VBA.vba           (Factor selection automation)
├── Tab3_Combined_VBA.vba           (Tab 3 formatting)
├── Tab4_Combined_VBA.vba           ⭐ Auto-sort on weight change
└── Workbook_Open_VBA.vba           (Welcome message)

Root:
├── Factor_Scanning_Model.xlsm      ⭐ Main Excel file
├── 02_MODEL_REFRESH.bat            ⭐ Update launcher
└── 01_INSTALL_PYTHON_AND_LIBRARIES.bat (One-time setup)
```

### Archived Files
```
scripts/python/archive/              (36+ old Python scripts)
scripts/python/archive_2025_fixes/   (Development scripts)
scripts/vba/archive/                 (Old VBA versions)
```

---

**Last Updated**: November 3, 2025
**Version**: v2.1 (Non-Destructive Architecture)
**Maintained By**: Quantitative Analytics Team
