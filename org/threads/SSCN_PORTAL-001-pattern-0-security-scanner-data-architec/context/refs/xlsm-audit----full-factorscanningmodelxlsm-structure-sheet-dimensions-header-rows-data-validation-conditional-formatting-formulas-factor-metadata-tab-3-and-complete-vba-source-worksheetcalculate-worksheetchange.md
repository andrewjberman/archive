## Sheet Structure

### Sheet: `1-Configuration`

- **Dimensions:** A1:K303
- **Max row:** 303
- **Max col:** 11
- **Merged cells:** 15
  - `A4:B4`
  - `A5:C5`
  - `A8:C8`
  - `E5:J5`
  - `A6:C6`
  - `H8:J8`
  - `E8:G8`
  - `A10:J10`
  - `A2:J2`
  - `E4:J4`
  - `A7:C7`
  - `E6:J6`
  - `C9:G9`
  - `A33:J33`
  - `E7:J7`

### Sheet: `2-Universe Data`

- **Dimensions:** A1:XFD508
- **Max row:** 508
- **Max col:** 16384
- **Merged cells:** 4
  - `A3:F3`
  - `A1:XFD1`
  - `A2:D2`
  - `A4:F4`

### Sheet: `3-Factor Data`

- **Dimensions:** A1:N293
- **Max row:** 293
- **Max col:** 14
- **Merged cells:** 4
  - `A4:B4`
  - `A3:B3`
  - `A2:B2`
  - `A1:B1`

### Sheet: `4-Security Scanner`

- **Dimensions:** A1:XFD531
- **Max row:** 531
- **Max col:** 16384
- **Merged cells:** 22
  - `R28:S28`
  - `J28:K28`
  - `L28:M28`
  - `V28:W28`
  - `X28:Y28`
  - `AD28:AE28`
  - `AJ28:AK28`
  - `AL28:AM28`
  - `AR28:AS28`
  - `A1:XFD1`
  - `A3:H3`
  - `N28:O28`
  - `P28:Q28`
  - `H28:I28`
  - `Z28:AA28`
  - `AB28:AC28`
  - `T28:U28`
  - `AF28:AG28`
  - `A2:D2`
  - `AH28:AI28`
  - ... and 2 more


---

## Header Rows (first 3 rows per sheet)

### Sheet `1-Configuration`

```
Row 1:  |  |  |  |  |  |  |  |  |  | 
Row 2:  |  |  |  |  |  |  |  |  |  | 
Row 3:  |  |  |  |  |  |  |  |  |  | 
```

### Sheet `2-Universe Data`

```
Row 1:  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 
Row 2: Complete Index Data |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 
Row 3: All securities available fo... |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 
  ... (16354 more columns)
```

### Sheet `3-Factor Data`

```
Row 1:  |  |  |  |  |  |  |  |  |  |  |  |  | 
Row 2: Factor Intelligence Library |  |  |  |  |  |  |  |  |  |  |  |  | 
Row 3: View universal factor detai... |  |  |  |  |  |  |  |  |  |  |  |  | 
```

### Sheet `4-Security Scanner`

```
Row 1:  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 
Row 2: S&P 500 Security Scoring & ... |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 
Row 3: Adjust factor weights (must... |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 
  ... (16354 more columns)
```

## Defined Names

(none)

## Data Validation Rules

### Sheet `1-Configuration` -- cells `C4`

- **Type:** list
- **Allow blank:** True
- **Formula1:** `"S&P 500,Russell 1000,Russell 1000 Value,MSCI ACWI ex-US,MSCI EAFE,MSCI EAFE Value"`

## Conditional Formatting Rules

### Sheet `1-Configuration` -- `F12:F30 F35:F302`

- **Type:** cellIs
- **Priority:** 49
- **Formula:** `['"Yes"']`
- **Fill color:** FFC6EFCE
- **Font color:** FF006100

### Sheet `1-Configuration` -- `H12:H30 H35:H302`

- **Type:** cellIs
- **Priority:** 50
- **Formula:** `['"Positive"']`
- **Fill color:** FFC6EFCE
- **Font color:** FF006100

### Sheet `1-Configuration` -- `H12:H30 H35:H302`

- **Type:** cellIs
- **Priority:** 51
- **Formula:** `['"Inverse"']`
- **Fill color:** FFFFC7CE
- **Font color:** FF9C0006

### Sheet `1-Configuration` -- `G12:G30 G35:G302`

- **Type:** expression
- **Priority:** 191
- **Formula:** `['AND(G12>=PERCENTILE($G$31:$G$302,0),G12<PERCENTILE($G$31:$G$302,0.2))']`
- **Fill color:** FFF8696B

### Sheet `1-Configuration` -- `G12:G30 G35:G302`

- **Type:** expression
- **Priority:** 192
- **Formula:** `['AND(G12>=PERCENTILE($G$31:$G$302,0.2),G12<PERCENTILE($G$31:$G$302,0.4))']`
- **Fill color:** FFFFA500

### Sheet `1-Configuration` -- `G12:G30 G35:G302`

- **Type:** expression
- **Priority:** 193
- **Formula:** `['AND(G12>=PERCENTILE($G$31:$G$302,0.4),G12<PERCENTILE($G$31:$G$302,0.6))']`
- **Fill color:** FFFFEB84

### Sheet `1-Configuration` -- `G12:G30 G35:G302`

- **Type:** expression
- **Priority:** 194
- **Formula:** `['AND(G12>=PERCENTILE($G$31:$G$302,0.6),G12<PERCENTILE($G$31:$G$302,0.8))']`
- **Fill color:** FF9ACD32

### Sheet `1-Configuration` -- `G12:G30 G35:G302`

- **Type:** expression
- **Priority:** 195
- **Formula:** `['AND(G12>=PERCENTILE($G$31:$G$302,0.8))']`
- **Fill color:** FF63BE7B

### Sheet `1-Configuration` -- `I12:I30 I35:I302`

- **Type:** expression
- **Priority:** 206
- **Formula:** `['AND(I12>=PERCENTILE($I$31:$I$302,0),I12<PERCENTILE($I$31:$I$302,0.2))']`
- **Fill color:** FFF8696B

### Sheet `1-Configuration` -- `I12:I30 I35:I302`

- **Type:** expression
- **Priority:** 207
- **Formula:** `['AND(I12>=PERCENTILE($I$31:$I$302,0.2),I12<PERCENTILE($I$31:$I$302,0.4))']`
- **Fill color:** FFFFA500

### Sheet `1-Configuration` -- `I12:I30 I35:I302`

- **Type:** expression
- **Priority:** 208
- **Formula:** `['AND(I12>=PERCENTILE($I$31:$I$302,0.4),I12<PERCENTILE($I$31:$I$302,0.6))']`
- **Fill color:** FFFFEB84

### Sheet `1-Configuration` -- `I12:I30 I35:I302`

- **Type:** expression
- **Priority:** 209
- **Formula:** `['AND(I12>=PERCENTILE($I$31:$I$302,0.6),I12<PERCENTILE($I$31:$I$302,0.8))']`
- **Fill color:** FF9ACD32

### Sheet `1-Configuration` -- `I12:I30 I35:I302`

- **Type:** expression
- **Priority:** 210
- **Formula:** `['AND(I12>=PERCENTILE($I$31:$I$302,0.8))']`
- **Fill color:** FF63BE7B

### Sheet `1-Configuration` -- `J12:J30 J35:J302`

- **Type:** expression
- **Priority:** 221
- **Formula:** `['AND(J12>=PERCENTILE($J$31:$J$302,0),J12<PERCENTILE($J$31:$J$302,0.2))']`
- **Fill color:** FFF8696B

### Sheet `1-Configuration` -- `J12:J30 J35:J302`

- **Type:** expression
- **Priority:** 222
- **Formula:** `['AND(J12>=PERCENTILE($J$31:$J$302,0.2),J12<PERCENTILE($J$31:$J$302,0.4))']`
- **Fill color:** FFFFA500

### Sheet `1-Configuration` -- `J12:J30 J35:J302`

- **Type:** expression
- **Priority:** 223
- **Formula:** `['AND(J12>=PERCENTILE($J$31:$J$302,0.4),J12<PERCENTILE($J$31:$J$302,0.6))']`
- **Fill color:** FFFFEB84

### Sheet `1-Configuration` -- `J12:J30 J35:J302`

- **Type:** expression
- **Priority:** 224
- **Formula:** `['AND(J12>=PERCENTILE($J$31:$J$302,0.6),J12<PERCENTILE($J$31:$J$302,0.8))']`
- **Fill color:** FF9ACD32

### Sheet `1-Configuration` -- `J12:J30 J35:J302`

- **Type:** expression
- **Priority:** 225
- **Formula:** `['AND(J12>=PERCENTILE($J$31:$J$302,0.8))']`
- **Fill color:** FF63BE7B

### Sheet `3-Factor Data` -- `N1:N1048576`

- **Type:** cellIs
- **Priority:** 3
- **Formula:** `['"Yes"']`
- **Fill color:** 00000000
- **Font color:** FF006100

### Sheet `3-Factor Data` -- `N1:N1048576`

- **Type:** cellIs
- **Priority:** 4
- **Formula:** `['"Yes"']`
- **Fill color:** 00000000

### Sheet `3-Factor Data` -- `D7:D293`

- **Type:** cellIs
- **Priority:** 1
- **Formula:** `['"Positive"']`
- **Fill color:** 00000000
- **Font color:** FF006100

### Sheet `3-Factor Data` -- `D7:D293`

- **Type:** cellIs
- **Priority:** 2
- **Formula:** `['"Inverse"']`
- **Fill color:** 00000000
- **Font color:** FF9C0006

### Sheet `4-Security Scanner` -- `D30:D713`

- **Type:** colorScale
- **Priority:** 102
- **Color scale:** <openpyxl.formatting.rule.ColorScale object>
Parameters:
cfvo=[<openpyxl.formatting.rule.FormatObject object>
Parameters:
type='min', val=None, gte=None, <openpyxl.formatting.rule.FormatObject object>
Parameters:
type='percentile', val=50.0, gte=None, <openpyxl.formatting.rule.FormatObject object>
Parameters:
type='max', val=None, gte=None], color=[<openpyxl.styles.colors.Color object>
Parameters:
rgb='FFF8696B', indexed=None, auto=None, theme=None, tint=0.0, type='rgb', <openpyxl.styles.colors.Color object>
Parameters:
rgb='FFFFEB84', indexed=None, auto=None, theme=None, tint=0.0, type='rgb', <openpyxl.styles.colors.Color object>
Parameters:
rgb='FF63BE7B', indexed=None, auto=None, theme=None, tint=0.0, type='rgb']

### Sheet `4-Security Scanner` -- `H30:H713`

- **Type:** cellIs
- **Priority:** 103
- **Formula:** `['0', '20']`
- **Fill color:** FFF8696B

### Sheet `4-Security Scanner` -- `H30:H713`

- **Type:** cellIs
- **Priority:** 104
- **Formula:** `['20', '40']`
- **Fill color:** FFFFA500

### Sheet `4-Security Scanner` -- `H30:H713`

- **Type:** cellIs
- **Priority:** 105
- **Formula:** `['40', '60']`
- **Fill color:** FFFFEB84

### Sheet `4-Security Scanner` -- `H30:H713`

- **Type:** cellIs
- **Priority:** 106
- **Formula:** `['60', '80']`
- **Fill color:** FF9ACD32

### Sheet `4-Security Scanner` -- `H30:H713`

- **Type:** cellIs
- **Priority:** 107
- **Formula:** `['80', '100']`
- **Fill color:** FF63BE7B

### Sheet `4-Security Scanner` -- `J30:J713`

- **Type:** cellIs
- **Priority:** 108
- **Formula:** `['0', '20']`
- **Fill color:** FFF8696B

### Sheet `4-Security Scanner` -- `J30:J713`

- **Type:** cellIs
- **Priority:** 109
- **Formula:** `['20', '40']`
- **Fill color:** FFFFA500

### Sheet `4-Security Scanner` -- `J30:J713`

- **Type:** cellIs
- **Priority:** 110
- **Formula:** `['40', '60']`
- **Fill color:** FFFFEB84

### Sheet `4-Security Scanner` -- `J30:J713`

- **Type:** cellIs
- **Priority:** 111
- **Formula:** `['60', '80']`
- **Fill color:** FF9ACD32

### Sheet `4-Security Scanner` -- `J30:J713`

- **Type:** cellIs
- **Priority:** 112
- **Formula:** `['80', '100']`
- **Fill color:** FF63BE7B

### Sheet `4-Security Scanner` -- `L30:L713`

- **Type:** cellIs
- **Priority:** 113
- **Formula:** `['0', '20']`
- **Fill color:** FFF8696B

### Sheet `4-Security Scanner` -- `L30:L713`

- **Type:** cellIs
- **Priority:** 114
- **Formula:** `['20', '40']`
- **Fill color:** FFFFA500

### Sheet `4-Security Scanner` -- `L30:L713`

- **Type:** cellIs
- **Priority:** 115
- **Formula:** `['40', '60']`
- **Fill color:** FFFFEB84

### Sheet `4-Security Scanner` -- `L30:L713`

- **Type:** cellIs
- **Priority:** 116
- **Formula:** `['60', '80']`
- **Fill color:** FF9ACD32

### Sheet `4-Security Scanner` -- `L30:L713`

- **Type:** cellIs
- **Priority:** 117
- **Formula:** `['80', '100']`
- **Fill color:** FF63BE7B

### Sheet `4-Security Scanner` -- `N30:N713`

- **Type:** cellIs
- **Priority:** 118
- **Formula:** `['0', '20']`
- **Fill color:** FFF8696B

### Sheet `4-Security Scanner` -- `N30:N713`

- **Type:** cellIs
- **Priority:** 119
- **Formula:** `['20', '40']`
- **Fill color:** FFFFA500

### Sheet `4-Security Scanner` -- `N30:N713`

- **Type:** cellIs
- **Priority:** 120
- **Formula:** `['40', '60']`
- **Fill color:** FFFFEB84

### Sheet `4-Security Scanner` -- `N30:N713`

- **Type:** cellIs
- **Priority:** 121
- **Formula:** `['60', '80']`
- **Fill color:** FF9ACD32

### Sheet `4-Security Scanner` -- `N30:N713`

- **Type:** cellIs
- **Priority:** 122
- **Formula:** `['80', '100']`
- **Fill color:** FF63BE7B

### Sheet `4-Security Scanner` -- `P30:P713`

- **Type:** cellIs
- **Priority:** 123
- **Formula:** `['0', '20']`
- **Fill color:** FFF8696B

### Sheet `4-Security Scanner` -- `P30:P713`

- **Type:** cellIs
- **Priority:** 124
- **Formula:** `['20', '40']`
- **Fill color:** FFFFA500

### Sheet `4-Security Scanner` -- `P30:P713`

- **Type:** cellIs
- **Priority:** 125
- **Formula:** `['40', '60']`
- **Fill color:** FFFFEB84

### Sheet `4-Security Scanner` -- `P30:P713`

- **Type:** cellIs
- **Priority:** 126
- **Formula:** `['60', '80']`
- **Fill color:** FF9ACD32

### Sheet `4-Security Scanner` -- `P30:P713`

- **Type:** cellIs
- **Priority:** 127
- **Formula:** `['80', '100']`
- **Fill color:** FF63BE7B

### Sheet `4-Security Scanner` -- `R30:R713`

- **Type:** cellIs
- **Priority:** 128
- **Formula:** `['0', '20']`
- **Fill color:** FFF8696B

### Sheet `4-Security Scanner` -- `R30:R713`

- **Type:** cellIs
- **Priority:** 129
- **Formula:** `['20', '40']`
- **Fill color:** FFFFA500

### Sheet `4-Security Scanner` -- `R30:R713`

- **Type:** cellIs
- **Priority:** 130
- **Formula:** `['40', '60']`
- **Fill color:** FFFFEB84

### Sheet `4-Security Scanner` -- `R30:R713`

- **Type:** cellIs
- **Priority:** 131
- **Formula:** `['60', '80']`
- **Fill color:** FF9ACD32

### Sheet `4-Security Scanner` -- `R30:R713`

- **Type:** cellIs
- **Priority:** 132
- **Formula:** `['80', '100']`
- **Fill color:** FF63BE7B

### Sheet `4-Security Scanner` -- `T30:T713`

- **Type:** cellIs
- **Priority:** 133
- **Formula:** `['0', '20']`
- **Fill color:** FFF8696B

### Sheet `4-Security Scanner` -- `T30:T713`

- **Type:** cellIs
- **Priority:** 134
- **Formula:** `['20', '40']`
- **Fill color:** FFFFA500

### Sheet `4-Security Scanner` -- `T30:T713`

- **Type:** cellIs
- **Priority:** 135
- **Formula:** `['40', '60']`
- **Fill color:** FFFFEB84

### Sheet `4-Security Scanner` -- `T30:T713`

- **Type:** cellIs
- **Priority:** 136
- **Formula:** `['60', '80']`
- **Fill color:** FF9ACD32

### Sheet `4-Security Scanner` -- `T30:T713`

- **Type:** cellIs
- **Priority:** 137
- **Formula:** `['80', '100']`
- **Fill color:** FF63BE7B

### Sheet `4-Security Scanner` -- `V30:V713`

- **Type:** cellIs
- **Priority:** 138
- **Formula:** `['0', '20']`
- **Fill color:** FFF8696B

### Sheet `4-Security Scanner` -- `V30:V713`

- **Type:** cellIs
- **Priority:** 139
- **Formula:** `['20', '40']`
- **Fill color:** FFFFA500

### Sheet `4-Security Scanner` -- `V30:V713`

- **Type:** cellIs
- **Priority:** 140
- **Formula:** `['40', '60']`
- **Fill color:** FFFFEB84

### Sheet `4-Security Scanner` -- `V30:V713`

- **Type:** cellIs
- **Priority:** 141
- **Formula:** `['60', '80']`
- **Fill color:** FF9ACD32

### Sheet `4-Security Scanner` -- `V30:V713`

- **Type:** cellIs
- **Priority:** 142
- **Formula:** `['80', '100']`
- **Fill color:** FF63BE7B

### Sheet `4-Security Scanner` -- `X30:X713`

- **Type:** cellIs
- **Priority:** 143
- **Formula:** `['0', '20']`
- **Fill color:** FFF8696B

### Sheet `4-Security Scanner` -- `X30:X713`

- **Type:** cellIs
- **Priority:** 144
- **Formula:** `['20', '40']`
- **Fill color:** FFFFA500

### Sheet `4-Security Scanner` -- `X30:X713`

- **Type:** cellIs
- **Priority:** 145
- **Formula:** `['40', '60']`
- **Fill color:** FFFFEB84

### Sheet `4-Security Scanner` -- `X30:X713`

- **Type:** cellIs
- **Priority:** 146
- **Formula:** `['60', '80']`
- **Fill color:** FF9ACD32

### Sheet `4-Security Scanner` -- `X30:X713`

- **Type:** cellIs
- **Priority:** 147
- **Formula:** `['80', '100']`
- **Fill color:** FF63BE7B

### Sheet `4-Security Scanner` -- `Z30:Z713`

- **Type:** cellIs
- **Priority:** 148
- **Formula:** `['0', '20']`
- **Fill color:** FFF8696B

### Sheet `4-Security Scanner` -- `Z30:Z713`

- **Type:** cellIs
- **Priority:** 149
- **Formula:** `['20', '40']`
- **Fill color:** FFFFA500

### Sheet `4-Security Scanner` -- `Z30:Z713`

- **Type:** cellIs
- **Priority:** 150
- **Formula:** `['40', '60']`
- **Fill color:** FFFFEB84

### Sheet `4-Security Scanner` -- `Z30:Z713`

- **Type:** cellIs
- **Priority:** 151
- **Formula:** `['60', '80']`
- **Fill color:** FF9ACD32

### Sheet `4-Security Scanner` -- `Z30:Z713`

- **Type:** cellIs
- **Priority:** 152
- **Formula:** `['80', '100']`
- **Fill color:** FF63BE7B

### Sheet `4-Security Scanner` -- `AB30:AB713`

- **Type:** cellIs
- **Priority:** 153
- **Formula:** `['0', '20']`
- **Fill color:** FFF8696B

### Sheet `4-Security Scanner` -- `AB30:AB713`

- **Type:** cellIs
- **Priority:** 154
- **Formula:** `['20', '40']`
- **Fill color:** FFFFA500

### Sheet `4-Security Scanner` -- `AB30:AB713`

- **Type:** cellIs
- **Priority:** 155
- **Formula:** `['40', '60']`
- **Fill color:** FFFFEB84

### Sheet `4-Security Scanner` -- `AB30:AB713`

- **Type:** cellIs
- **Priority:** 156
- **Formula:** `['60', '80']`
- **Fill color:** FF9ACD32

### Sheet `4-Security Scanner` -- `AB30:AB713`

- **Type:** cellIs
- **Priority:** 157
- **Formula:** `['80', '100']`
- **Fill color:** FF63BE7B

### Sheet `4-Security Scanner` -- `AD30:AD713`

- **Type:** cellIs
- **Priority:** 158
- **Formula:** `['0', '20']`
- **Fill color:** FFF8696B

### Sheet `4-Security Scanner` -- `AD30:AD713`

- **Type:** cellIs
- **Priority:** 159
- **Formula:** `['20', '40']`
- **Fill color:** FFFFA500

### Sheet `4-Security Scanner` -- `AD30:AD713`

- **Type:** cellIs
- **Priority:** 160
- **Formula:** `['40', '60']`
- **Fill color:** FFFFEB84

### Sheet `4-Security Scanner` -- `AD30:AD713`

- **Type:** cellIs
- **Priority:** 161
- **Formula:** `['60', '80']`
- **Fill color:** FF9ACD32

### Sheet `4-Security Scanner` -- `AD30:AD713`

- **Type:** cellIs
- **Priority:** 162
- **Formula:** `['80', '100']`
- **Fill color:** FF63BE7B

### Sheet `4-Security Scanner` -- `AF30:AF713`

- **Type:** cellIs
- **Priority:** 163
- **Formula:** `['0', '20']`
- **Fill color:** FFF8696B

### Sheet `4-Security Scanner` -- `AF30:AF713`

- **Type:** cellIs
- **Priority:** 164
- **Formula:** `['20', '40']`
- **Fill color:** FFFFA500

### Sheet `4-Security Scanner` -- `AF30:AF713`

- **Type:** cellIs
- **Priority:** 165
- **Formula:** `['40', '60']`
- **Fill color:** FFFFEB84

### Sheet `4-Security Scanner` -- `AF30:AF713`

- **Type:** cellIs
- **Priority:** 166
- **Formula:** `['60', '80']`
- **Fill color:** FF9ACD32

### Sheet `4-Security Scanner` -- `AF30:AF713`

- **Type:** cellIs
- **Priority:** 167
- **Formula:** `['80', '100']`
- **Fill color:** FF63BE7B

### Sheet `4-Security Scanner` -- `AH30:AH713`

- **Type:** cellIs
- **Priority:** 168
- **Formula:** `['0', '20']`
- **Fill color:** FFF8696B

### Sheet `4-Security Scanner` -- `AH30:AH713`

- **Type:** cellIs
- **Priority:** 169
- **Formula:** `['20', '40']`
- **Fill color:** FFFFA500

### Sheet `4-Security Scanner` -- `AH30:AH713`

- **Type:** cellIs
- **Priority:** 170
- **Formula:** `['40', '60']`
- **Fill color:** FFFFEB84

### Sheet `4-Security Scanner` -- `AH30:AH713`

- **Type:** cellIs
- **Priority:** 171
- **Formula:** `['60', '80']`
- **Fill color:** FF9ACD32

### Sheet `4-Security Scanner` -- `AH30:AH713`

- **Type:** cellIs
- **Priority:** 172
- **Formula:** `['80', '100']`
- **Fill color:** FF63BE7B

### Sheet `4-Security Scanner` -- `AJ30:AJ713`

- **Type:** cellIs
- **Priority:** 173
- **Formula:** `['0', '20']`
- **Fill color:** FFF8696B

### Sheet `4-Security Scanner` -- `AJ30:AJ713`

- **Type:** cellIs
- **Priority:** 174
- **Formula:** `['20', '40']`
- **Fill color:** FFFFA500

### Sheet `4-Security Scanner` -- `AJ30:AJ713`

- **Type:** cellIs
- **Priority:** 175
- **Formula:** `['40', '60']`
- **Fill color:** FFFFEB84

### Sheet `4-Security Scanner` -- `AJ30:AJ713`

- **Type:** cellIs
- **Priority:** 176
- **Formula:** `['60', '80']`
- **Fill color:** FF9ACD32

### Sheet `4-Security Scanner` -- `AJ30:AJ713`

- **Type:** cellIs
- **Priority:** 177
- **Formula:** `['80', '100']`
- **Fill color:** FF63BE7B

### Sheet `4-Security Scanner` -- `AL30:AL713`

- **Type:** cellIs
- **Priority:** 178
- **Formula:** `['0', '20']`
- **Fill color:** FFF8696B

### Sheet `4-Security Scanner` -- `AL30:AL713`

- **Type:** cellIs
- **Priority:** 179
- **Formula:** `['20', '40']`
- **Fill color:** FFFFA500

### Sheet `4-Security Scanner` -- `AL30:AL713`

- **Type:** cellIs
- **Priority:** 180
- **Formula:** `['40', '60']`
- **Fill color:** FFFFEB84

### Sheet `4-Security Scanner` -- `AL30:AL713`

- **Type:** cellIs
- **Priority:** 181
- **Formula:** `['60', '80']`
- **Fill color:** FF9ACD32

### Sheet `4-Security Scanner` -- `AL30:AL713`

- **Type:** cellIs
- **Priority:** 182
- **Formula:** `['80', '100']`
- **Fill color:** FF63BE7B

### Sheet `4-Security Scanner` -- `AN30:AN713`

- **Type:** cellIs
- **Priority:** 183
- **Formula:** `['0', '20']`
- **Fill color:** FFF8696B

### Sheet `4-Security Scanner` -- `AN30:AN713`

- **Type:** cellIs
- **Priority:** 184
- **Formula:** `['20', '40']`
- **Fill color:** FFFFA500

### Sheet `4-Security Scanner` -- `AN30:AN713`

- **Type:** cellIs
- **Priority:** 185
- **Formula:** `['40', '60']`
- **Fill color:** FFFFEB84

### Sheet `4-Security Scanner` -- `AN30:AN713`

- **Type:** cellIs
- **Priority:** 186
- **Formula:** `['60', '80']`
- **Fill color:** FF9ACD32

### Sheet `4-Security Scanner` -- `AN30:AN713`

- **Type:** cellIs
- **Priority:** 187
- **Formula:** `['80', '100']`
- **Fill color:** FF63BE7B

### Sheet `4-Security Scanner` -- `AP30:AP713`

- **Type:** cellIs
- **Priority:** 188
- **Formula:** `['0', '20']`
- **Fill color:** FFF8696B

### Sheet `4-Security Scanner` -- `AP30:AP713`

- **Type:** cellIs
- **Priority:** 189
- **Formula:** `['20', '40']`
- **Fill color:** FFFFA500

### Sheet `4-Security Scanner` -- `AP30:AP713`

- **Type:** cellIs
- **Priority:** 190
- **Formula:** `['40', '60']`
- **Fill color:** FFFFEB84

### Sheet `4-Security Scanner` -- `AP30:AP713`

- **Type:** cellIs
- **Priority:** 191
- **Formula:** `['60', '80']`
- **Fill color:** FF9ACD32

### Sheet `4-Security Scanner` -- `AP30:AP713`

- **Type:** cellIs
- **Priority:** 192
- **Formula:** `['80', '100']`
- **Fill color:** FF63BE7B

### Sheet `4-Security Scanner` -- `AR30:AR713`

- **Type:** cellIs
- **Priority:** 193
- **Formula:** `['0', '20']`
- **Fill color:** FFF8696B

### Sheet `4-Security Scanner` -- `AR30:AR713`

- **Type:** cellIs
- **Priority:** 194
- **Formula:** `['20', '40']`
- **Fill color:** FFFFA500

### Sheet `4-Security Scanner` -- `AR30:AR713`

- **Type:** cellIs
- **Priority:** 195
- **Formula:** `['40', '60']`
- **Fill color:** FFFFEB84

### Sheet `4-Security Scanner` -- `AR30:AR713`

- **Type:** cellIs
- **Priority:** 196
- **Formula:** `['60', '80']`
- **Fill color:** FF9ACD32

### Sheet `4-Security Scanner` -- `AR30:AR713`

- **Type:** cellIs
- **Priority:** 197
- **Formula:** `['80', '100']`
- **Fill color:** FF63BE7B

## Formulas

### Sheet `1-Configuration` (1148 formulas)

| Cell | Formula |
|------|---------|
| `G12` | `=IFERROR(ROUND(VLOOKUP(E12,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H12` | `=IFERROR(VLOOKUP(E12,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I12` | `=IFERROR(ROUND(VLOOKUP(E12,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J12` | `=IFERROR(VLOOKUP(E12,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G13` | `=IFERROR(ROUND(VLOOKUP(E13,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H13` | `=IFERROR(VLOOKUP(E13,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I13` | `=IFERROR(ROUND(VLOOKUP(E13,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J13` | `=IFERROR(VLOOKUP(E13,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G14` | `=IFERROR(ROUND(VLOOKUP(E14,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H14` | `=IFERROR(VLOOKUP(E14,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I14` | `=IFERROR(ROUND(VLOOKUP(E14,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J14` | `=IFERROR(VLOOKUP(E14,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G15` | `=IFERROR(ROUND(VLOOKUP(E15,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H15` | `=IFERROR(VLOOKUP(E15,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I15` | `=IFERROR(ROUND(VLOOKUP(E15,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J15` | `=IFERROR(VLOOKUP(E15,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G16` | `=IFERROR(ROUND(VLOOKUP(E16,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H16` | `=IFERROR(VLOOKUP(E16,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I16` | `=IFERROR(ROUND(VLOOKUP(E16,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J16` | `=IFERROR(VLOOKUP(E16,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G17` | `=IFERROR(ROUND(VLOOKUP(E17,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H17` | `=IFERROR(VLOOKUP(E17,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I17` | `=IFERROR(ROUND(VLOOKUP(E17,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J17` | `=IFERROR(VLOOKUP(E17,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G18` | `=IFERROR(ROUND(VLOOKUP(E18,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H18` | `=IFERROR(VLOOKUP(E18,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I18` | `=IFERROR(ROUND(VLOOKUP(E18,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J18` | `=IFERROR(VLOOKUP(E18,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G19` | `=IFERROR(ROUND(VLOOKUP(E19,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H19` | `=IFERROR(VLOOKUP(E19,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I19` | `=IFERROR(ROUND(VLOOKUP(E19,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J19` | `=IFERROR(VLOOKUP(E19,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G20` | `=IFERROR(ROUND(VLOOKUP(E20,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H20` | `=IFERROR(VLOOKUP(E20,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I20` | `=IFERROR(ROUND(VLOOKUP(E20,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J20` | `=IFERROR(VLOOKUP(E20,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G21` | `=IFERROR(ROUND(VLOOKUP(E21,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H21` | `=IFERROR(VLOOKUP(E21,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I21` | `=IFERROR(ROUND(VLOOKUP(E21,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J21` | `=IFERROR(VLOOKUP(E21,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G22` | `=IFERROR(ROUND(VLOOKUP(E22,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H22` | `=IFERROR(VLOOKUP(E22,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I22` | `=IFERROR(ROUND(VLOOKUP(E22,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J22` | `=IFERROR(VLOOKUP(E22,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G23` | `=IFERROR(ROUND(VLOOKUP(E23,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H23` | `=IFERROR(VLOOKUP(E23,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I23` | `=IFERROR(ROUND(VLOOKUP(E23,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J23` | `=IFERROR(VLOOKUP(E23,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G24` | `=IFERROR(ROUND(VLOOKUP(E24,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H24` | `=IFERROR(VLOOKUP(E24,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I24` | `=IFERROR(ROUND(VLOOKUP(E24,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J24` | `=IFERROR(VLOOKUP(E24,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G25` | `=IFERROR(ROUND(VLOOKUP(E25,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H25` | `=IFERROR(VLOOKUP(E25,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I25` | `=IFERROR(ROUND(VLOOKUP(E25,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J25` | `=IFERROR(VLOOKUP(E25,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G26` | `=IFERROR(ROUND(VLOOKUP(E26,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H26` | `=IFERROR(VLOOKUP(E26,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I26` | `=IFERROR(ROUND(VLOOKUP(E26,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J26` | `=IFERROR(VLOOKUP(E26,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G27` | `=IFERROR(ROUND(VLOOKUP(E27,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H27` | `=IFERROR(VLOOKUP(E27,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I27` | `=IFERROR(ROUND(VLOOKUP(E27,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J27` | `=IFERROR(VLOOKUP(E27,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G28` | `=IFERROR(ROUND(VLOOKUP(E28,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H28` | `=IFERROR(VLOOKUP(E28,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I28` | `=IFERROR(ROUND(VLOOKUP(E28,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J28` | `=IFERROR(VLOOKUP(E28,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G29` | `=IFERROR(ROUND(VLOOKUP(E29,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H29` | `=IFERROR(VLOOKUP(E29,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I29` | `=IFERROR(ROUND(VLOOKUP(E29,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J29` | `=IFERROR(VLOOKUP(E29,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G30` | `=IFERROR(ROUND(VLOOKUP(E30,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H30` | `=IFERROR(VLOOKUP(E30,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I30` | `=IFERROR(ROUND(VLOOKUP(E30,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J30` | `=IFERROR(VLOOKUP(E30,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G35` | `=IFERROR(ROUND(VLOOKUP(E35,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H35` | `=IFERROR(VLOOKUP(E35,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I35` | `=IFERROR(ROUND(VLOOKUP(E35,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J35` | `=IFERROR(VLOOKUP(E35,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G36` | `=IFERROR(ROUND(VLOOKUP(E36,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H36` | `=IFERROR(VLOOKUP(E36,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I36` | `=IFERROR(ROUND(VLOOKUP(E36,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J36` | `=IFERROR(VLOOKUP(E36,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G37` | `=IFERROR(ROUND(VLOOKUP(E37,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H37` | `=IFERROR(VLOOKUP(E37,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I37` | `=IFERROR(ROUND(VLOOKUP(E37,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J37` | `=IFERROR(VLOOKUP(E37,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G38` | `=IFERROR(ROUND(VLOOKUP(E38,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H38` | `=IFERROR(VLOOKUP(E38,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I38` | `=IFERROR(ROUND(VLOOKUP(E38,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J38` | `=IFERROR(VLOOKUP(E38,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G39` | `=IFERROR(ROUND(VLOOKUP(E39,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H39` | `=IFERROR(VLOOKUP(E39,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I39` | `=IFERROR(ROUND(VLOOKUP(E39,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J39` | `=IFERROR(VLOOKUP(E39,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G40` | `=IFERROR(ROUND(VLOOKUP(E40,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H40` | `=IFERROR(VLOOKUP(E40,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I40` | `=IFERROR(ROUND(VLOOKUP(E40,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J40` | `=IFERROR(VLOOKUP(E40,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G41` | `=IFERROR(ROUND(VLOOKUP(E41,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H41` | `=IFERROR(VLOOKUP(E41,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I41` | `=IFERROR(ROUND(VLOOKUP(E41,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J41` | `=IFERROR(VLOOKUP(E41,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G42` | `=IFERROR(ROUND(VLOOKUP(E42,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H42` | `=IFERROR(VLOOKUP(E42,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I42` | `=IFERROR(ROUND(VLOOKUP(E42,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J42` | `=IFERROR(VLOOKUP(E42,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G43` | `=IFERROR(ROUND(VLOOKUP(E43,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H43` | `=IFERROR(VLOOKUP(E43,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I43` | `=IFERROR(ROUND(VLOOKUP(E43,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J43` | `=IFERROR(VLOOKUP(E43,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G44` | `=IFERROR(ROUND(VLOOKUP(E44,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H44` | `=IFERROR(VLOOKUP(E44,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I44` | `=IFERROR(ROUND(VLOOKUP(E44,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J44` | `=IFERROR(VLOOKUP(E44,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G45` | `=IFERROR(ROUND(VLOOKUP(E45,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H45` | `=IFERROR(VLOOKUP(E45,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I45` | `=IFERROR(ROUND(VLOOKUP(E45,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J45` | `=IFERROR(VLOOKUP(E45,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G46` | `=IFERROR(ROUND(VLOOKUP(E46,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H46` | `=IFERROR(VLOOKUP(E46,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I46` | `=IFERROR(ROUND(VLOOKUP(E46,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J46` | `=IFERROR(VLOOKUP(E46,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G47` | `=IFERROR(ROUND(VLOOKUP(E47,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H47` | `=IFERROR(VLOOKUP(E47,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I47` | `=IFERROR(ROUND(VLOOKUP(E47,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J47` | `=IFERROR(VLOOKUP(E47,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G48` | `=IFERROR(ROUND(VLOOKUP(E48,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H48` | `=IFERROR(VLOOKUP(E48,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I48` | `=IFERROR(ROUND(VLOOKUP(E48,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J48` | `=IFERROR(VLOOKUP(E48,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G49` | `=IFERROR(ROUND(VLOOKUP(E49,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H49` | `=IFERROR(VLOOKUP(E49,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I49` | `=IFERROR(ROUND(VLOOKUP(E49,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J49` | `=IFERROR(VLOOKUP(E49,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G50` | `=IFERROR(ROUND(VLOOKUP(E50,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H50` | `=IFERROR(VLOOKUP(E50,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I50` | `=IFERROR(ROUND(VLOOKUP(E50,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J50` | `=IFERROR(VLOOKUP(E50,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G51` | `=IFERROR(ROUND(VLOOKUP(E51,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H51` | `=IFERROR(VLOOKUP(E51,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I51` | `=IFERROR(ROUND(VLOOKUP(E51,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J51` | `=IFERROR(VLOOKUP(E51,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G52` | `=IFERROR(ROUND(VLOOKUP(E52,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H52` | `=IFERROR(VLOOKUP(E52,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I52` | `=IFERROR(ROUND(VLOOKUP(E52,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J52` | `=IFERROR(VLOOKUP(E52,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G53` | `=IFERROR(ROUND(VLOOKUP(E53,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H53` | `=IFERROR(VLOOKUP(E53,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I53` | `=IFERROR(ROUND(VLOOKUP(E53,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J53` | `=IFERROR(VLOOKUP(E53,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G54` | `=IFERROR(ROUND(VLOOKUP(E54,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H54` | `=IFERROR(VLOOKUP(E54,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I54` | `=IFERROR(ROUND(VLOOKUP(E54,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J54` | `=IFERROR(VLOOKUP(E54,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G55` | `=IFERROR(ROUND(VLOOKUP(E55,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H55` | `=IFERROR(VLOOKUP(E55,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I55` | `=IFERROR(ROUND(VLOOKUP(E55,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J55` | `=IFERROR(VLOOKUP(E55,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G56` | `=IFERROR(ROUND(VLOOKUP(E56,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H56` | `=IFERROR(VLOOKUP(E56,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I56` | `=IFERROR(ROUND(VLOOKUP(E56,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J56` | `=IFERROR(VLOOKUP(E56,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G57` | `=IFERROR(ROUND(VLOOKUP(E57,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H57` | `=IFERROR(VLOOKUP(E57,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I57` | `=IFERROR(ROUND(VLOOKUP(E57,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J57` | `=IFERROR(VLOOKUP(E57,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G58` | `=IFERROR(ROUND(VLOOKUP(E58,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H58` | `=IFERROR(VLOOKUP(E58,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I58` | `=IFERROR(ROUND(VLOOKUP(E58,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J58` | `=IFERROR(VLOOKUP(E58,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G59` | `=IFERROR(ROUND(VLOOKUP(E59,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H59` | `=IFERROR(VLOOKUP(E59,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I59` | `=IFERROR(ROUND(VLOOKUP(E59,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J59` | `=IFERROR(VLOOKUP(E59,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G60` | `=IFERROR(ROUND(VLOOKUP(E60,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H60` | `=IFERROR(VLOOKUP(E60,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I60` | `=IFERROR(ROUND(VLOOKUP(E60,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J60` | `=IFERROR(VLOOKUP(E60,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G61` | `=IFERROR(ROUND(VLOOKUP(E61,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H61` | `=IFERROR(VLOOKUP(E61,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I61` | `=IFERROR(ROUND(VLOOKUP(E61,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J61` | `=IFERROR(VLOOKUP(E61,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G62` | `=IFERROR(ROUND(VLOOKUP(E62,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H62` | `=IFERROR(VLOOKUP(E62,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I62` | `=IFERROR(ROUND(VLOOKUP(E62,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J62` | `=IFERROR(VLOOKUP(E62,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G63` | `=IFERROR(ROUND(VLOOKUP(E63,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H63` | `=IFERROR(VLOOKUP(E63,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I63` | `=IFERROR(ROUND(VLOOKUP(E63,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J63` | `=IFERROR(VLOOKUP(E63,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G64` | `=IFERROR(ROUND(VLOOKUP(E64,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H64` | `=IFERROR(VLOOKUP(E64,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I64` | `=IFERROR(ROUND(VLOOKUP(E64,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J64` | `=IFERROR(VLOOKUP(E64,'3-Factor Data'!C:N,10,FALSE),"")` |
| `G65` | `=IFERROR(ROUND(VLOOKUP(E65,'3-Factor Data'!C:N,9,FALSE),2),"")` |
| `H65` | `=IFERROR(VLOOKUP(E65,'3-Factor Data'!C:N,2,FALSE),"")` |
| `I65` | `=IFERROR(ROUND(VLOOKUP(E65,'3-Factor Data'!C:N,3,FALSE),2),"")` |
| `J65` | `=IFERROR(VLOOKUP(E65,'3-Factor Data'!C:N,10,FALSE),"")` |

... and 948 more formulas (truncated)

### Sheet `4-Security Scanner` (503 formulas)

| Cell | Formula |
|------|---------|
| `C26` | `=SUM(C7:C25)` |
| `D30` | `=(H30*$C$7+J30*$C$8+L30*$C$9+N30*$C$10+P30*$C$11+R30*$C$12+T30*$C$13+V30*$C$14+X30*$C$15+Z30*$C$16+AB30*$C$17+AD30*$C$18+AF30*$C$19+AH30*$C$20+AJ30*$C$21+AL30*$C$22+AN30*$C$23+AP30*$C$24+AR30*$C$25...` |
| `D31` | `=(H31*$C$7+J31*$C$8+L31*$C$9+N31*$C$10+P31*$C$11+R31*$C$12+T31*$C$13+V31*$C$14+X31*$C$15+Z31*$C$16+AB31*$C$17+AD31*$C$18+AF31*$C$19+AH31*$C$20+AJ31*$C$21+AL31*$C$22+AN31*$C$23+AP31*$C$24+AR31*$C$25...` |
| `D32` | `=(H32*$C$7+J32*$C$8+L32*$C$9+N32*$C$10+P32*$C$11+R32*$C$12+T32*$C$13+V32*$C$14+X32*$C$15+Z32*$C$16+AB32*$C$17+AD32*$C$18+AF32*$C$19+AH32*$C$20+AJ32*$C$21+AL32*$C$22+AN32*$C$23+AP32*$C$24+AR32*$C$25...` |
| `D33` | `=(H33*$C$7+J33*$C$8+L33*$C$9+N33*$C$10+P33*$C$11+R33*$C$12+T33*$C$13+V33*$C$14+X33*$C$15+Z33*$C$16+AB33*$C$17+AD33*$C$18+AF33*$C$19+AH33*$C$20+AJ33*$C$21+AL33*$C$22+AN33*$C$23+AP33*$C$24+AR33*$C$25...` |
| `D34` | `=(H34*$C$7+J34*$C$8+L34*$C$9+N34*$C$10+P34*$C$11+R34*$C$12+T34*$C$13+V34*$C$14+X34*$C$15+Z34*$C$16+AB34*$C$17+AD34*$C$18+AF34*$C$19+AH34*$C$20+AJ34*$C$21+AL34*$C$22+AN34*$C$23+AP34*$C$24+AR34*$C$25...` |
| `D35` | `=(H35*$C$7+J35*$C$8+L35*$C$9+N35*$C$10+P35*$C$11+R35*$C$12+T35*$C$13+V35*$C$14+X35*$C$15+Z35*$C$16+AB35*$C$17+AD35*$C$18+AF35*$C$19+AH35*$C$20+AJ35*$C$21+AL35*$C$22+AN35*$C$23+AP35*$C$24+AR35*$C$25...` |
| `D36` | `=(H36*$C$7+J36*$C$8+L36*$C$9+N36*$C$10+P36*$C$11+R36*$C$12+T36*$C$13+V36*$C$14+X36*$C$15+Z36*$C$16+AB36*$C$17+AD36*$C$18+AF36*$C$19+AH36*$C$20+AJ36*$C$21+AL36*$C$22+AN36*$C$23+AP36*$C$24+AR36*$C$25...` |
| `D37` | `=(H37*$C$7+J37*$C$8+L37*$C$9+N37*$C$10+P37*$C$11+R37*$C$12+T37*$C$13+V37*$C$14+X37*$C$15+Z37*$C$16+AB37*$C$17+AD37*$C$18+AF37*$C$19+AH37*$C$20+AJ37*$C$21+AL37*$C$22+AN37*$C$23+AP37*$C$24+AR37*$C$25...` |
| `D38` | `=(H38*$C$7+J38*$C$8+L38*$C$9+N38*$C$10+P38*$C$11+R38*$C$12+T38*$C$13+V38*$C$14+X38*$C$15+Z38*$C$16+AB38*$C$17+AD38*$C$18+AF38*$C$19+AH38*$C$20+AJ38*$C$21+AL38*$C$22+AN38*$C$23+AP38*$C$24+AR38*$C$25...` |
| `D39` | `=(H39*$C$7+J39*$C$8+L39*$C$9+N39*$C$10+P39*$C$11+R39*$C$12+T39*$C$13+V39*$C$14+X39*$C$15+Z39*$C$16+AB39*$C$17+AD39*$C$18+AF39*$C$19+AH39*$C$20+AJ39*$C$21+AL39*$C$22+AN39*$C$23+AP39*$C$24+AR39*$C$25...` |
| `D40` | `=(H40*$C$7+J40*$C$8+L40*$C$9+N40*$C$10+P40*$C$11+R40*$C$12+T40*$C$13+V40*$C$14+X40*$C$15+Z40*$C$16+AB40*$C$17+AD40*$C$18+AF40*$C$19+AH40*$C$20+AJ40*$C$21+AL40*$C$22+AN40*$C$23+AP40*$C$24+AR40*$C$25...` |
| `D41` | `=(H41*$C$7+J41*$C$8+L41*$C$9+N41*$C$10+P41*$C$11+R41*$C$12+T41*$C$13+V41*$C$14+X41*$C$15+Z41*$C$16+AB41*$C$17+AD41*$C$18+AF41*$C$19+AH41*$C$20+AJ41*$C$21+AL41*$C$22+AN41*$C$23+AP41*$C$24+AR41*$C$25...` |
| `D42` | `=(H42*$C$7+J42*$C$8+L42*$C$9+N42*$C$10+P42*$C$11+R42*$C$12+T42*$C$13+V42*$C$14+X42*$C$15+Z42*$C$16+AB42*$C$17+AD42*$C$18+AF42*$C$19+AH42*$C$20+AJ42*$C$21+AL42*$C$22+AN42*$C$23+AP42*$C$24+AR42*$C$25...` |
| `D43` | `=(H43*$C$7+J43*$C$8+L43*$C$9+N43*$C$10+P43*$C$11+R43*$C$12+T43*$C$13+V43*$C$14+X43*$C$15+Z43*$C$16+AB43*$C$17+AD43*$C$18+AF43*$C$19+AH43*$C$20+AJ43*$C$21+AL43*$C$22+AN43*$C$23+AP43*$C$24+AR43*$C$25...` |
| `D44` | `=(H44*$C$7+J44*$C$8+L44*$C$9+N44*$C$10+P44*$C$11+R44*$C$12+T44*$C$13+V44*$C$14+X44*$C$15+Z44*$C$16+AB44*$C$17+AD44*$C$18+AF44*$C$19+AH44*$C$20+AJ44*$C$21+AL44*$C$22+AN44*$C$23+AP44*$C$24+AR44*$C$25...` |
| `D45` | `=(H45*$C$7+J45*$C$8+L45*$C$9+N45*$C$10+P45*$C$11+R45*$C$12+T45*$C$13+V45*$C$14+X45*$C$15+Z45*$C$16+AB45*$C$17+AD45*$C$18+AF45*$C$19+AH45*$C$20+AJ45*$C$21+AL45*$C$22+AN45*$C$23+AP45*$C$24+AR45*$C$25...` |
| `D46` | `=(H46*$C$7+J46*$C$8+L46*$C$9+N46*$C$10+P46*$C$11+R46*$C$12+T46*$C$13+V46*$C$14+X46*$C$15+Z46*$C$16+AB46*$C$17+AD46*$C$18+AF46*$C$19+AH46*$C$20+AJ46*$C$21+AL46*$C$22+AN46*$C$23+AP46*$C$24+AR46*$C$25...` |
| `D47` | `=(H47*$C$7+J47*$C$8+L47*$C$9+N47*$C$10+P47*$C$11+R47*$C$12+T47*$C$13+V47*$C$14+X47*$C$15+Z47*$C$16+AB47*$C$17+AD47*$C$18+AF47*$C$19+AH47*$C$20+AJ47*$C$21+AL47*$C$22+AN47*$C$23+AP47*$C$24+AR47*$C$25...` |
| `D48` | `=(H48*$C$7+J48*$C$8+L48*$C$9+N48*$C$10+P48*$C$11+R48*$C$12+T48*$C$13+V48*$C$14+X48*$C$15+Z48*$C$16+AB48*$C$17+AD48*$C$18+AF48*$C$19+AH48*$C$20+AJ48*$C$21+AL48*$C$22+AN48*$C$23+AP48*$C$24+AR48*$C$25...` |
| `D49` | `=(H49*$C$7+J49*$C$8+L49*$C$9+N49*$C$10+P49*$C$11+R49*$C$12+T49*$C$13+V49*$C$14+X49*$C$15+Z49*$C$16+AB49*$C$17+AD49*$C$18+AF49*$C$19+AH49*$C$20+AJ49*$C$21+AL49*$C$22+AN49*$C$23+AP49*$C$24+AR49*$C$25...` |
| `D50` | `=(H50*$C$7+J50*$C$8+L50*$C$9+N50*$C$10+P50*$C$11+R50*$C$12+T50*$C$13+V50*$C$14+X50*$C$15+Z50*$C$16+AB50*$C$17+AD50*$C$18+AF50*$C$19+AH50*$C$20+AJ50*$C$21+AL50*$C$22+AN50*$C$23+AP50*$C$24+AR50*$C$25...` |
| `D51` | `=(H51*$C$7+J51*$C$8+L51*$C$9+N51*$C$10+P51*$C$11+R51*$C$12+T51*$C$13+V51*$C$14+X51*$C$15+Z51*$C$16+AB51*$C$17+AD51*$C$18+AF51*$C$19+AH51*$C$20+AJ51*$C$21+AL51*$C$22+AN51*$C$23+AP51*$C$24+AR51*$C$25...` |
| `D52` | `=(H52*$C$7+J52*$C$8+L52*$C$9+N52*$C$10+P52*$C$11+R52*$C$12+T52*$C$13+V52*$C$14+X52*$C$15+Z52*$C$16+AB52*$C$17+AD52*$C$18+AF52*$C$19+AH52*$C$20+AJ52*$C$21+AL52*$C$22+AN52*$C$23+AP52*$C$24+AR52*$C$25...` |
| `D53` | `=(H53*$C$7+J53*$C$8+L53*$C$9+N53*$C$10+P53*$C$11+R53*$C$12+T53*$C$13+V53*$C$14+X53*$C$15+Z53*$C$16+AB53*$C$17+AD53*$C$18+AF53*$C$19+AH53*$C$20+AJ53*$C$21+AL53*$C$22+AN53*$C$23+AP53*$C$24+AR53*$C$25...` |
| `D54` | `=(H54*$C$7+J54*$C$8+L54*$C$9+N54*$C$10+P54*$C$11+R54*$C$12+T54*$C$13+V54*$C$14+X54*$C$15+Z54*$C$16+AB54*$C$17+AD54*$C$18+AF54*$C$19+AH54*$C$20+AJ54*$C$21+AL54*$C$22+AN54*$C$23+AP54*$C$24+AR54*$C$25...` |
| `D55` | `=(H55*$C$7+J55*$C$8+L55*$C$9+N55*$C$10+P55*$C$11+R55*$C$12+T55*$C$13+V55*$C$14+X55*$C$15+Z55*$C$16+AB55*$C$17+AD55*$C$18+AF55*$C$19+AH55*$C$20+AJ55*$C$21+AL55*$C$22+AN55*$C$23+AP55*$C$24+AR55*$C$25...` |
| `D56` | `=(H56*$C$7+J56*$C$8+L56*$C$9+N56*$C$10+P56*$C$11+R56*$C$12+T56*$C$13+V56*$C$14+X56*$C$15+Z56*$C$16+AB56*$C$17+AD56*$C$18+AF56*$C$19+AH56*$C$20+AJ56*$C$21+AL56*$C$22+AN56*$C$23+AP56*$C$24+AR56*$C$25...` |
| `D57` | `=(H57*$C$7+J57*$C$8+L57*$C$9+N57*$C$10+P57*$C$11+R57*$C$12+T57*$C$13+V57*$C$14+X57*$C$15+Z57*$C$16+AB57*$C$17+AD57*$C$18+AF57*$C$19+AH57*$C$20+AJ57*$C$21+AL57*$C$22+AN57*$C$23+AP57*$C$24+AR57*$C$25...` |
| `D58` | `=(H58*$C$7+J58*$C$8+L58*$C$9+N58*$C$10+P58*$C$11+R58*$C$12+T58*$C$13+V58*$C$14+X58*$C$15+Z58*$C$16+AB58*$C$17+AD58*$C$18+AF58*$C$19+AH58*$C$20+AJ58*$C$21+AL58*$C$22+AN58*$C$23+AP58*$C$24+AR58*$C$25...` |
| `D59` | `=(H59*$C$7+J59*$C$8+L59*$C$9+N59*$C$10+P59*$C$11+R59*$C$12+T59*$C$13+V59*$C$14+X59*$C$15+Z59*$C$16+AB59*$C$17+AD59*$C$18+AF59*$C$19+AH59*$C$20+AJ59*$C$21+AL59*$C$22+AN59*$C$23+AP59*$C$24+AR59*$C$25...` |
| `D60` | `=(H60*$C$7+J60*$C$8+L60*$C$9+N60*$C$10+P60*$C$11+R60*$C$12+T60*$C$13+V60*$C$14+X60*$C$15+Z60*$C$16+AB60*$C$17+AD60*$C$18+AF60*$C$19+AH60*$C$20+AJ60*$C$21+AL60*$C$22+AN60*$C$23+AP60*$C$24+AR60*$C$25...` |
| `D61` | `=(H61*$C$7+J61*$C$8+L61*$C$9+N61*$C$10+P61*$C$11+R61*$C$12+T61*$C$13+V61*$C$14+X61*$C$15+Z61*$C$16+AB61*$C$17+AD61*$C$18+AF61*$C$19+AH61*$C$20+AJ61*$C$21+AL61*$C$22+AN61*$C$23+AP61*$C$24+AR61*$C$25...` |
| `D62` | `=(H62*$C$7+J62*$C$8+L62*$C$9+N62*$C$10+P62*$C$11+R62*$C$12+T62*$C$13+V62*$C$14+X62*$C$15+Z62*$C$16+AB62*$C$17+AD62*$C$18+AF62*$C$19+AH62*$C$20+AJ62*$C$21+AL62*$C$22+AN62*$C$23+AP62*$C$24+AR62*$C$25...` |
| `D63` | `=(H63*$C$7+J63*$C$8+L63*$C$9+N63*$C$10+P63*$C$11+R63*$C$12+T63*$C$13+V63*$C$14+X63*$C$15+Z63*$C$16+AB63*$C$17+AD63*$C$18+AF63*$C$19+AH63*$C$20+AJ63*$C$21+AL63*$C$22+AN63*$C$23+AP63*$C$24+AR63*$C$25...` |
| `D64` | `=(H64*$C$7+J64*$C$8+L64*$C$9+N64*$C$10+P64*$C$11+R64*$C$12+T64*$C$13+V64*$C$14+X64*$C$15+Z64*$C$16+AB64*$C$17+AD64*$C$18+AF64*$C$19+AH64*$C$20+AJ64*$C$21+AL64*$C$22+AN64*$C$23+AP64*$C$24+AR64*$C$25...` |
| `D65` | `=(H65*$C$7+J65*$C$8+L65*$C$9+N65*$C$10+P65*$C$11+R65*$C$12+T65*$C$13+V65*$C$14+X65*$C$15+Z65*$C$16+AB65*$C$17+AD65*$C$18+AF65*$C$19+AH65*$C$20+AJ65*$C$21+AL65*$C$22+AN65*$C$23+AP65*$C$24+AR65*$C$25...` |
| `D66` | `=(H66*$C$7+J66*$C$8+L66*$C$9+N66*$C$10+P66*$C$11+R66*$C$12+T66*$C$13+V66*$C$14+X66*$C$15+Z66*$C$16+AB66*$C$17+AD66*$C$18+AF66*$C$19+AH66*$C$20+AJ66*$C$21+AL66*$C$22+AN66*$C$23+AP66*$C$24+AR66*$C$25...` |
| `D67` | `=(H67*$C$7+J67*$C$8+L67*$C$9+N67*$C$10+P67*$C$11+R67*$C$12+T67*$C$13+V67*$C$14+X67*$C$15+Z67*$C$16+AB67*$C$17+AD67*$C$18+AF67*$C$19+AH67*$C$20+AJ67*$C$21+AL67*$C$22+AN67*$C$23+AP67*$C$24+AR67*$C$25...` |
| `D68` | `=(H68*$C$7+J68*$C$8+L68*$C$9+N68*$C$10+P68*$C$11+R68*$C$12+T68*$C$13+V68*$C$14+X68*$C$15+Z68*$C$16+AB68*$C$17+AD68*$C$18+AF68*$C$19+AH68*$C$20+AJ68*$C$21+AL68*$C$22+AN68*$C$23+AP68*$C$24+AR68*$C$25...` |
| `D69` | `=(H69*$C$7+J69*$C$8+L69*$C$9+N69*$C$10+P69*$C$11+R69*$C$12+T69*$C$13+V69*$C$14+X69*$C$15+Z69*$C$16+AB69*$C$17+AD69*$C$18+AF69*$C$19+AH69*$C$20+AJ69*$C$21+AL69*$C$22+AN69*$C$23+AP69*$C$24+AR69*$C$25...` |
| `D70` | `=(H70*$C$7+J70*$C$8+L70*$C$9+N70*$C$10+P70*$C$11+R70*$C$12+T70*$C$13+V70*$C$14+X70*$C$15+Z70*$C$16+AB70*$C$17+AD70*$C$18+AF70*$C$19+AH70*$C$20+AJ70*$C$21+AL70*$C$22+AN70*$C$23+AP70*$C$24+AR70*$C$25...` |
| `D71` | `=(H71*$C$7+J71*$C$8+L71*$C$9+N71*$C$10+P71*$C$11+R71*$C$12+T71*$C$13+V71*$C$14+X71*$C$15+Z71*$C$16+AB71*$C$17+AD71*$C$18+AF71*$C$19+AH71*$C$20+AJ71*$C$21+AL71*$C$22+AN71*$C$23+AP71*$C$24+AR71*$C$25...` |
| `D72` | `=(H72*$C$7+J72*$C$8+L72*$C$9+N72*$C$10+P72*$C$11+R72*$C$12+T72*$C$13+V72*$C$14+X72*$C$15+Z72*$C$16+AB72*$C$17+AD72*$C$18+AF72*$C$19+AH72*$C$20+AJ72*$C$21+AL72*$C$22+AN72*$C$23+AP72*$C$24+AR72*$C$25...` |
| `D73` | `=(H73*$C$7+J73*$C$8+L73*$C$9+N73*$C$10+P73*$C$11+R73*$C$12+T73*$C$13+V73*$C$14+X73*$C$15+Z73*$C$16+AB73*$C$17+AD73*$C$18+AF73*$C$19+AH73*$C$20+AJ73*$C$21+AL73*$C$22+AN73*$C$23+AP73*$C$24+AR73*$C$25...` |
| `D74` | `=(H74*$C$7+J74*$C$8+L74*$C$9+N74*$C$10+P74*$C$11+R74*$C$12+T74*$C$13+V74*$C$14+X74*$C$15+Z74*$C$16+AB74*$C$17+AD74*$C$18+AF74*$C$19+AH74*$C$20+AJ74*$C$21+AL74*$C$22+AN74*$C$23+AP74*$C$24+AR74*$C$25...` |
| `D75` | `=(H75*$C$7+J75*$C$8+L75*$C$9+N75*$C$10+P75*$C$11+R75*$C$12+T75*$C$13+V75*$C$14+X75*$C$15+Z75*$C$16+AB75*$C$17+AD75*$C$18+AF75*$C$19+AH75*$C$20+AJ75*$C$21+AL75*$C$22+AN75*$C$23+AP75*$C$24+AR75*$C$25...` |
| `D76` | `=(H76*$C$7+J76*$C$8+L76*$C$9+N76*$C$10+P76*$C$11+R76*$C$12+T76*$C$13+V76*$C$14+X76*$C$15+Z76*$C$16+AB76*$C$17+AD76*$C$18+AF76*$C$19+AH76*$C$20+AJ76*$C$21+AL76*$C$22+AN76*$C$23+AP76*$C$24+AR76*$C$25...` |
| `D77` | `=(H77*$C$7+J77*$C$8+L77*$C$9+N77*$C$10+P77*$C$11+R77*$C$12+T77*$C$13+V77*$C$14+X77*$C$15+Z77*$C$16+AB77*$C$17+AD77*$C$18+AF77*$C$19+AH77*$C$20+AJ77*$C$21+AL77*$C$22+AN77*$C$23+AP77*$C$24+AR77*$C$25...` |
| `D78` | `=(H78*$C$7+J78*$C$8+L78*$C$9+N78*$C$10+P78*$C$11+R78*$C$12+T78*$C$13+V78*$C$14+X78*$C$15+Z78*$C$16+AB78*$C$17+AD78*$C$18+AF78*$C$19+AH78*$C$20+AJ78*$C$21+AL78*$C$22+AN78*$C$23+AP78*$C$24+AR78*$C$25...` |
| `D79` | `=(H79*$C$7+J79*$C$8+L79*$C$9+N79*$C$10+P79*$C$11+R79*$C$12+T79*$C$13+V79*$C$14+X79*$C$15+Z79*$C$16+AB79*$C$17+AD79*$C$18+AF79*$C$19+AH79*$C$20+AJ79*$C$21+AL79*$C$22+AN79*$C$23+AP79*$C$24+AR79*$C$25...` |
| `D80` | `=(H80*$C$7+J80*$C$8+L80*$C$9+N80*$C$10+P80*$C$11+R80*$C$12+T80*$C$13+V80*$C$14+X80*$C$15+Z80*$C$16+AB80*$C$17+AD80*$C$18+AF80*$C$19+AH80*$C$20+AJ80*$C$21+AL80*$C$22+AN80*$C$23+AP80*$C$24+AR80*$C$25...` |
| `D81` | `=(H81*$C$7+J81*$C$8+L81*$C$9+N81*$C$10+P81*$C$11+R81*$C$12+T81*$C$13+V81*$C$14+X81*$C$15+Z81*$C$16+AB81*$C$17+AD81*$C$18+AF81*$C$19+AH81*$C$20+AJ81*$C$21+AL81*$C$22+AN81*$C$23+AP81*$C$24+AR81*$C$25...` |
| `D82` | `=(H82*$C$7+J82*$C$8+L82*$C$9+N82*$C$10+P82*$C$11+R82*$C$12+T82*$C$13+V82*$C$14+X82*$C$15+Z82*$C$16+AB82*$C$17+AD82*$C$18+AF82*$C$19+AH82*$C$20+AJ82*$C$21+AL82*$C$22+AN82*$C$23+AP82*$C$24+AR82*$C$25...` |
| `D83` | `=(H83*$C$7+J83*$C$8+L83*$C$9+N83*$C$10+P83*$C$11+R83*$C$12+T83*$C$13+V83*$C$14+X83*$C$15+Z83*$C$16+AB83*$C$17+AD83*$C$18+AF83*$C$19+AH83*$C$20+AJ83*$C$21+AL83*$C$22+AN83*$C$23+AP83*$C$24+AR83*$C$25...` |
| `D84` | `=(H84*$C$7+J84*$C$8+L84*$C$9+N84*$C$10+P84*$C$11+R84*$C$12+T84*$C$13+V84*$C$14+X84*$C$15+Z84*$C$16+AB84*$C$17+AD84*$C$18+AF84*$C$19+AH84*$C$20+AJ84*$C$21+AL84*$C$22+AN84*$C$23+AP84*$C$24+AR84*$C$25...` |
| `D85` | `=(H85*$C$7+J85*$C$8+L85*$C$9+N85*$C$10+P85*$C$11+R85*$C$12+T85*$C$13+V85*$C$14+X85*$C$15+Z85*$C$16+AB85*$C$17+AD85*$C$18+AF85*$C$19+AH85*$C$20+AJ85*$C$21+AL85*$C$22+AN85*$C$23+AP85*$C$24+AR85*$C$25...` |
| `D86` | `=(H86*$C$7+J86*$C$8+L86*$C$9+N86*$C$10+P86*$C$11+R86*$C$12+T86*$C$13+V86*$C$14+X86*$C$15+Z86*$C$16+AB86*$C$17+AD86*$C$18+AF86*$C$19+AH86*$C$20+AJ86*$C$21+AL86*$C$22+AN86*$C$23+AP86*$C$24+AR86*$C$25...` |
| `D87` | `=(H87*$C$7+J87*$C$8+L87*$C$9+N87*$C$10+P87*$C$11+R87*$C$12+T87*$C$13+V87*$C$14+X87*$C$15+Z87*$C$16+AB87*$C$17+AD87*$C$18+AF87*$C$19+AH87*$C$20+AJ87*$C$21+AL87*$C$22+AN87*$C$23+AP87*$C$24+AR87*$C$25...` |
| `D88` | `=(H88*$C$7+J88*$C$8+L88*$C$9+N88*$C$10+P88*$C$11+R88*$C$12+T88*$C$13+V88*$C$14+X88*$C$15+Z88*$C$16+AB88*$C$17+AD88*$C$18+AF88*$C$19+AH88*$C$20+AJ88*$C$21+AL88*$C$22+AN88*$C$23+AP88*$C$24+AR88*$C$25...` |
| `D89` | `=(H89*$C$7+J89*$C$8+L89*$C$9+N89*$C$10+P89*$C$11+R89*$C$12+T89*$C$13+V89*$C$14+X89*$C$15+Z89*$C$16+AB89*$C$17+AD89*$C$18+AF89*$C$19+AH89*$C$20+AJ89*$C$21+AL89*$C$22+AN89*$C$23+AP89*$C$24+AR89*$C$25...` |
| `D90` | `=(H90*$C$7+J90*$C$8+L90*$C$9+N90*$C$10+P90*$C$11+R90*$C$12+T90*$C$13+V90*$C$14+X90*$C$15+Z90*$C$16+AB90*$C$17+AD90*$C$18+AF90*$C$19+AH90*$C$20+AJ90*$C$21+AL90*$C$22+AN90*$C$23+AP90*$C$24+AR90*$C$25...` |
| `D91` | `=(H91*$C$7+J91*$C$8+L91*$C$9+N91*$C$10+P91*$C$11+R91*$C$12+T91*$C$13+V91*$C$14+X91*$C$15+Z91*$C$16+AB91*$C$17+AD91*$C$18+AF91*$C$19+AH91*$C$20+AJ91*$C$21+AL91*$C$22+AN91*$C$23+AP91*$C$24+AR91*$C$25...` |
| `D92` | `=(H92*$C$7+J92*$C$8+L92*$C$9+N92*$C$10+P92*$C$11+R92*$C$12+T92*$C$13+V92*$C$14+X92*$C$15+Z92*$C$16+AB92*$C$17+AD92*$C$18+AF92*$C$19+AH92*$C$20+AJ92*$C$21+AL92*$C$22+AN92*$C$23+AP92*$C$24+AR92*$C$25...` |
| `D93` | `=(H93*$C$7+J93*$C$8+L93*$C$9+N93*$C$10+P93*$C$11+R93*$C$12+T93*$C$13+V93*$C$14+X93*$C$15+Z93*$C$16+AB93*$C$17+AD93*$C$18+AF93*$C$19+AH93*$C$20+AJ93*$C$21+AL93*$C$22+AN93*$C$23+AP93*$C$24+AR93*$C$25...` |
| `D94` | `=(H94*$C$7+J94*$C$8+L94*$C$9+N94*$C$10+P94*$C$11+R94*$C$12+T94*$C$13+V94*$C$14+X94*$C$15+Z94*$C$16+AB94*$C$17+AD94*$C$18+AF94*$C$19+AH94*$C$20+AJ94*$C$21+AL94*$C$22+AN94*$C$23+AP94*$C$24+AR94*$C$25...` |
| `D95` | `=(H95*$C$7+J95*$C$8+L95*$C$9+N95*$C$10+P95*$C$11+R95*$C$12+T95*$C$13+V95*$C$14+X95*$C$15+Z95*$C$16+AB95*$C$17+AD95*$C$18+AF95*$C$19+AH95*$C$20+AJ95*$C$21+AL95*$C$22+AN95*$C$23+AP95*$C$24+AR95*$C$25...` |
| `D96` | `=(H96*$C$7+J96*$C$8+L96*$C$9+N96*$C$10+P96*$C$11+R96*$C$12+T96*$C$13+V96*$C$14+X96*$C$15+Z96*$C$16+AB96*$C$17+AD96*$C$18+AF96*$C$19+AH96*$C$20+AJ96*$C$21+AL96*$C$22+AN96*$C$23+AP96*$C$24+AR96*$C$25...` |
| `D97` | `=(H97*$C$7+J97*$C$8+L97*$C$9+N97*$C$10+P97*$C$11+R97*$C$12+T97*$C$13+V97*$C$14+X97*$C$15+Z97*$C$16+AB97*$C$17+AD97*$C$18+AF97*$C$19+AH97*$C$20+AJ97*$C$21+AL97*$C$22+AN97*$C$23+AP97*$C$24+AR97*$C$25...` |
| `D98` | `=(H98*$C$7+J98*$C$8+L98*$C$9+N98*$C$10+P98*$C$11+R98*$C$12+T98*$C$13+V98*$C$14+X98*$C$15+Z98*$C$16+AB98*$C$17+AD98*$C$18+AF98*$C$19+AH98*$C$20+AJ98*$C$21+AL98*$C$22+AN98*$C$23+AP98*$C$24+AR98*$C$25...` |
| `D99` | `=(H99*$C$7+J99*$C$8+L99*$C$9+N99*$C$10+P99*$C$11+R99*$C$12+T99*$C$13+V99*$C$14+X99*$C$15+Z99*$C$16+AB99*$C$17+AD99*$C$18+AF99*$C$19+AH99*$C$20+AJ99*$C$21+AL99*$C$22+AN99*$C$23+AP99*$C$24+AR99*$C$25...` |
| `D100` | `=(H100*$C$7+J100*$C$8+L100*$C$9+N100*$C$10+P100*$C$11+R100*$C$12+T100*$C$13+V100*$C$14+X100*$C$15+Z100*$C$16+AB100*$C$17+AD100*$C$18+AF100*$C$19+AH100*$C$20+AJ100*$C$21+AL100*$C$22+AN100*$C$23+AP10...` |
| `D101` | `=(H101*$C$7+J101*$C$8+L101*$C$9+N101*$C$10+P101*$C$11+R101*$C$12+T101*$C$13+V101*$C$14+X101*$C$15+Z101*$C$16+AB101*$C$17+AD101*$C$18+AF101*$C$19+AH101*$C$20+AJ101*$C$21+AL101*$C$22+AN101*$C$23+AP10...` |
| `D102` | `=(H102*$C$7+J102*$C$8+L102*$C$9+N102*$C$10+P102*$C$11+R102*$C$12+T102*$C$13+V102*$C$14+X102*$C$15+Z102*$C$16+AB102*$C$17+AD102*$C$18+AF102*$C$19+AH102*$C$20+AJ102*$C$21+AL102*$C$22+AN102*$C$23+AP10...` |
| `D103` | `=(H103*$C$7+J103*$C$8+L103*$C$9+N103*$C$10+P103*$C$11+R103*$C$12+T103*$C$13+V103*$C$14+X103*$C$15+Z103*$C$16+AB103*$C$17+AD103*$C$18+AF103*$C$19+AH103*$C$20+AJ103*$C$21+AL103*$C$22+AN103*$C$23+AP10...` |
| `D104` | `=(H104*$C$7+J104*$C$8+L104*$C$9+N104*$C$10+P104*$C$11+R104*$C$12+T104*$C$13+V104*$C$14+X104*$C$15+Z104*$C$16+AB104*$C$17+AD104*$C$18+AF104*$C$19+AH104*$C$20+AJ104*$C$21+AL104*$C$22+AN104*$C$23+AP10...` |
| `D105` | `=(H105*$C$7+J105*$C$8+L105*$C$9+N105*$C$10+P105*$C$11+R105*$C$12+T105*$C$13+V105*$C$14+X105*$C$15+Z105*$C$16+AB105*$C$17+AD105*$C$18+AF105*$C$19+AH105*$C$20+AJ105*$C$21+AL105*$C$22+AN105*$C$23+AP10...` |
| `D106` | `=(H106*$C$7+J106*$C$8+L106*$C$9+N106*$C$10+P106*$C$11+R106*$C$12+T106*$C$13+V106*$C$14+X106*$C$15+Z106*$C$16+AB106*$C$17+AD106*$C$18+AF106*$C$19+AH106*$C$20+AJ106*$C$21+AL106*$C$22+AN106*$C$23+AP10...` |
| `D107` | `=(H107*$C$7+J107*$C$8+L107*$C$9+N107*$C$10+P107*$C$11+R107*$C$12+T107*$C$13+V107*$C$14+X107*$C$15+Z107*$C$16+AB107*$C$17+AD107*$C$18+AF107*$C$19+AH107*$C$20+AJ107*$C$21+AL107*$C$22+AN107*$C$23+AP10...` |
| `D108` | `=(H108*$C$7+J108*$C$8+L108*$C$9+N108*$C$10+P108*$C$11+R108*$C$12+T108*$C$13+V108*$C$14+X108*$C$15+Z108*$C$16+AB108*$C$17+AD108*$C$18+AF108*$C$19+AH108*$C$20+AJ108*$C$21+AL108*$C$22+AN108*$C$23+AP10...` |
| `D109` | `=(H109*$C$7+J109*$C$8+L109*$C$9+N109*$C$10+P109*$C$11+R109*$C$12+T109*$C$13+V109*$C$14+X109*$C$15+Z109*$C$16+AB109*$C$17+AD109*$C$18+AF109*$C$19+AH109*$C$20+AJ109*$C$21+AL109*$C$22+AN109*$C$23+AP10...` |
| `D110` | `=(H110*$C$7+J110*$C$8+L110*$C$9+N110*$C$10+P110*$C$11+R110*$C$12+T110*$C$13+V110*$C$14+X110*$C$15+Z110*$C$16+AB110*$C$17+AD110*$C$18+AF110*$C$19+AH110*$C$20+AJ110*$C$21+AL110*$C$22+AN110*$C$23+AP11...` |
| `D111` | `=(H111*$C$7+J111*$C$8+L111*$C$9+N111*$C$10+P111*$C$11+R111*$C$12+T111*$C$13+V111*$C$14+X111*$C$15+Z111*$C$16+AB111*$C$17+AD111*$C$18+AF111*$C$19+AH111*$C$20+AJ111*$C$21+AL111*$C$22+AN111*$C$23+AP11...` |
| `D112` | `=(H112*$C$7+J112*$C$8+L112*$C$9+N112*$C$10+P112*$C$11+R112*$C$12+T112*$C$13+V112*$C$14+X112*$C$15+Z112*$C$16+AB112*$C$17+AD112*$C$18+AF112*$C$19+AH112*$C$20+AJ112*$C$21+AL112*$C$22+AN112*$C$23+AP11...` |
| `D113` | `=(H113*$C$7+J113*$C$8+L113*$C$9+N113*$C$10+P113*$C$11+R113*$C$12+T113*$C$13+V113*$C$14+X113*$C$15+Z113*$C$16+AB113*$C$17+AD113*$C$18+AF113*$C$19+AH113*$C$20+AJ113*$C$21+AL113*$C$22+AN113*$C$23+AP11...` |
| `D114` | `=(H114*$C$7+J114*$C$8+L114*$C$9+N114*$C$10+P114*$C$11+R114*$C$12+T114*$C$13+V114*$C$14+X114*$C$15+Z114*$C$16+AB114*$C$17+AD114*$C$18+AF114*$C$19+AH114*$C$20+AJ114*$C$21+AL114*$C$22+AN114*$C$23+AP11...` |
| `D115` | `=(H115*$C$7+J115*$C$8+L115*$C$9+N115*$C$10+P115*$C$11+R115*$C$12+T115*$C$13+V115*$C$14+X115*$C$15+Z115*$C$16+AB115*$C$17+AD115*$C$18+AF115*$C$19+AH115*$C$20+AJ115*$C$21+AL115*$C$22+AN115*$C$23+AP11...` |
| `D116` | `=(H116*$C$7+J116*$C$8+L116*$C$9+N116*$C$10+P116*$C$11+R116*$C$12+T116*$C$13+V116*$C$14+X116*$C$15+Z116*$C$16+AB116*$C$17+AD116*$C$18+AF116*$C$19+AH116*$C$20+AJ116*$C$21+AL116*$C$22+AN116*$C$23+AP11...` |
| `D117` | `=(H117*$C$7+J117*$C$8+L117*$C$9+N117*$C$10+P117*$C$11+R117*$C$12+T117*$C$13+V117*$C$14+X117*$C$15+Z117*$C$16+AB117*$C$17+AD117*$C$18+AF117*$C$19+AH117*$C$20+AJ117*$C$21+AL117*$C$22+AN117*$C$23+AP11...` |
| `D118` | `=(H118*$C$7+J118*$C$8+L118*$C$9+N118*$C$10+P118*$C$11+R118*$C$12+T118*$C$13+V118*$C$14+X118*$C$15+Z118*$C$16+AB118*$C$17+AD118*$C$18+AF118*$C$19+AH118*$C$20+AJ118*$C$21+AL118*$C$22+AN118*$C$23+AP11...` |
| `D119` | `=(H119*$C$7+J119*$C$8+L119*$C$9+N119*$C$10+P119*$C$11+R119*$C$12+T119*$C$13+V119*$C$14+X119*$C$15+Z119*$C$16+AB119*$C$17+AD119*$C$18+AF119*$C$19+AH119*$C$20+AJ119*$C$21+AL119*$C$22+AN119*$C$23+AP11...` |
| `D120` | `=(H120*$C$7+J120*$C$8+L120*$C$9+N120*$C$10+P120*$C$11+R120*$C$12+T120*$C$13+V120*$C$14+X120*$C$15+Z120*$C$16+AB120*$C$17+AD120*$C$18+AF120*$C$19+AH120*$C$20+AJ120*$C$21+AL120*$C$22+AN120*$C$23+AP12...` |
| `D121` | `=(H121*$C$7+J121*$C$8+L121*$C$9+N121*$C$10+P121*$C$11+R121*$C$12+T121*$C$13+V121*$C$14+X121*$C$15+Z121*$C$16+AB121*$C$17+AD121*$C$18+AF121*$C$19+AH121*$C$20+AJ121*$C$21+AL121*$C$22+AN121*$C$23+AP12...` |
| `D122` | `=(H122*$C$7+J122*$C$8+L122*$C$9+N122*$C$10+P122*$C$11+R122*$C$12+T122*$C$13+V122*$C$14+X122*$C$15+Z122*$C$16+AB122*$C$17+AD122*$C$18+AF122*$C$19+AH122*$C$20+AJ122*$C$21+AL122*$C$22+AN122*$C$23+AP12...` |
| `D123` | `=(H123*$C$7+J123*$C$8+L123*$C$9+N123*$C$10+P123*$C$11+R123*$C$12+T123*$C$13+V123*$C$14+X123*$C$15+Z123*$C$16+AB123*$C$17+AD123*$C$18+AF123*$C$19+AH123*$C$20+AJ123*$C$21+AL123*$C$22+AN123*$C$23+AP12...` |
| `D124` | `=(H124*$C$7+J124*$C$8+L124*$C$9+N124*$C$10+P124*$C$11+R124*$C$12+T124*$C$13+V124*$C$14+X124*$C$15+Z124*$C$16+AB124*$C$17+AD124*$C$18+AF124*$C$19+AH124*$C$20+AJ124*$C$21+AL124*$C$22+AN124*$C$23+AP12...` |
| `D125` | `=(H125*$C$7+J125*$C$8+L125*$C$9+N125*$C$10+P125*$C$11+R125*$C$12+T125*$C$13+V125*$C$14+X125*$C$15+Z125*$C$16+AB125*$C$17+AD125*$C$18+AF125*$C$19+AH125*$C$20+AJ125*$C$21+AL125*$C$22+AN125*$C$23+AP12...` |
| `D126` | `=(H126*$C$7+J126*$C$8+L126*$C$9+N126*$C$10+P126*$C$11+R126*$C$12+T126*$C$13+V126*$C$14+X126*$C$15+Z126*$C$16+AB126*$C$17+AD126*$C$18+AF126*$C$19+AH126*$C$20+AJ126*$C$21+AL126*$C$22+AN126*$C$23+AP12...` |
| `D127` | `=(H127*$C$7+J127*$C$8+L127*$C$9+N127*$C$10+P127*$C$11+R127*$C$12+T127*$C$13+V127*$C$14+X127*$C$15+Z127*$C$16+AB127*$C$17+AD127*$C$18+AF127*$C$19+AH127*$C$20+AJ127*$C$21+AL127*$C$22+AN127*$C$23+AP12...` |
| `D128` | `=(H128*$C$7+J128*$C$8+L128*$C$9+N128*$C$10+P128*$C$11+R128*$C$12+T128*$C$13+V128*$C$14+X128*$C$15+Z128*$C$16+AB128*$C$17+AD128*$C$18+AF128*$C$19+AH128*$C$20+AJ128*$C$21+AL128*$C$22+AN128*$C$23+AP12...` |
| `D129` | `=(H129*$C$7+J129*$C$8+L129*$C$9+N129*$C$10+P129*$C$11+R129*$C$12+T129*$C$13+V129*$C$14+X129*$C$15+Z129*$C$16+AB129*$C$17+AD129*$C$18+AF129*$C$19+AH129*$C$20+AJ129*$C$21+AL129*$C$22+AN129*$C$23+AP12...` |
| `D130` | `=(H130*$C$7+J130*$C$8+L130*$C$9+N130*$C$10+P130*$C$11+R130*$C$12+T130*$C$13+V130*$C$14+X130*$C$15+Z130*$C$16+AB130*$C$17+AD130*$C$18+AF130*$C$19+AH130*$C$20+AJ130*$C$21+AL130*$C$22+AN130*$C$23+AP13...` |
| `D131` | `=(H131*$C$7+J131*$C$8+L131*$C$9+N131*$C$10+P131*$C$11+R131*$C$12+T131*$C$13+V131*$C$14+X131*$C$15+Z131*$C$16+AB131*$C$17+AD131*$C$18+AF131*$C$19+AH131*$C$20+AJ131*$C$21+AL131*$C$22+AN131*$C$23+AP13...` |
| `D132` | `=(H132*$C$7+J132*$C$8+L132*$C$9+N132*$C$10+P132*$C$11+R132*$C$12+T132*$C$13+V132*$C$14+X132*$C$15+Z132*$C$16+AB132*$C$17+AD132*$C$18+AF132*$C$19+AH132*$C$20+AJ132*$C$21+AL132*$C$22+AN132*$C$23+AP13...` |
| `D133` | `=(H133*$C$7+J133*$C$8+L133*$C$9+N133*$C$10+P133*$C$11+R133*$C$12+T133*$C$13+V133*$C$14+X133*$C$15+Z133*$C$16+AB133*$C$17+AD133*$C$18+AF133*$C$19+AH133*$C$20+AJ133*$C$21+AL133*$C$22+AN133*$C$23+AP13...` |
| `D134` | `=(H134*$C$7+J134*$C$8+L134*$C$9+N134*$C$10+P134*$C$11+R134*$C$12+T134*$C$13+V134*$C$14+X134*$C$15+Z134*$C$16+AB134*$C$17+AD134*$C$18+AF134*$C$19+AH134*$C$20+AJ134*$C$21+AL134*$C$22+AN134*$C$23+AP13...` |
| `D135` | `=(H135*$C$7+J135*$C$8+L135*$C$9+N135*$C$10+P135*$C$11+R135*$C$12+T135*$C$13+V135*$C$14+X135*$C$15+Z135*$C$16+AB135*$C$17+AD135*$C$18+AF135*$C$19+AH135*$C$20+AJ135*$C$21+AL135*$C$22+AN135*$C$23+AP13...` |
| `D136` | `=(H136*$C$7+J136*$C$8+L136*$C$9+N136*$C$10+P136*$C$11+R136*$C$12+T136*$C$13+V136*$C$14+X136*$C$15+Z136*$C$16+AB136*$C$17+AD136*$C$18+AF136*$C$19+AH136*$C$20+AJ136*$C$21+AL136*$C$22+AN136*$C$23+AP13...` |
| `D137` | `=(H137*$C$7+J137*$C$8+L137*$C$9+N137*$C$10+P137*$C$11+R137*$C$12+T137*$C$13+V137*$C$14+X137*$C$15+Z137*$C$16+AB137*$C$17+AD137*$C$18+AF137*$C$19+AH137*$C$20+AJ137*$C$21+AL137*$C$22+AN137*$C$23+AP13...` |
| `D138` | `=(H138*$C$7+J138*$C$8+L138*$C$9+N138*$C$10+P138*$C$11+R138*$C$12+T138*$C$13+V138*$C$14+X138*$C$15+Z138*$C$16+AB138*$C$17+AD138*$C$18+AF138*$C$19+AH138*$C$20+AJ138*$C$21+AL138*$C$22+AN138*$C$23+AP13...` |
| `D139` | `=(H139*$C$7+J139*$C$8+L139*$C$9+N139*$C$10+P139*$C$11+R139*$C$12+T139*$C$13+V139*$C$14+X139*$C$15+Z139*$C$16+AB139*$C$17+AD139*$C$18+AF139*$C$19+AH139*$C$20+AJ139*$C$21+AL139*$C$22+AN139*$C$23+AP13...` |
| `D140` | `=(H140*$C$7+J140*$C$8+L140*$C$9+N140*$C$10+P140*$C$11+R140*$C$12+T140*$C$13+V140*$C$14+X140*$C$15+Z140*$C$16+AB140*$C$17+AD140*$C$18+AF140*$C$19+AH140*$C$20+AJ140*$C$21+AL140*$C$22+AN140*$C$23+AP14...` |
| `D141` | `=(H141*$C$7+J141*$C$8+L141*$C$9+N141*$C$10+P141*$C$11+R141*$C$12+T141*$C$13+V141*$C$14+X141*$C$15+Z141*$C$16+AB141*$C$17+AD141*$C$18+AF141*$C$19+AH141*$C$20+AJ141*$C$21+AL141*$C$22+AN141*$C$23+AP14...` |
| `D142` | `=(H142*$C$7+J142*$C$8+L142*$C$9+N142*$C$10+P142*$C$11+R142*$C$12+T142*$C$13+V142*$C$14+X142*$C$15+Z142*$C$16+AB142*$C$17+AD142*$C$18+AF142*$C$19+AH142*$C$20+AJ142*$C$21+AL142*$C$22+AN142*$C$23+AP14...` |
| `D143` | `=(H143*$C$7+J143*$C$8+L143*$C$9+N143*$C$10+P143*$C$11+R143*$C$12+T143*$C$13+V143*$C$14+X143*$C$15+Z143*$C$16+AB143*$C$17+AD143*$C$18+AF143*$C$19+AH143*$C$20+AJ143*$C$21+AL143*$C$22+AN143*$C$23+AP14...` |
| `D144` | `=(H144*$C$7+J144*$C$8+L144*$C$9+N144*$C$10+P144*$C$11+R144*$C$12+T144*$C$13+V144*$C$14+X144*$C$15+Z144*$C$16+AB144*$C$17+AD144*$C$18+AF144*$C$19+AH144*$C$20+AJ144*$C$21+AL144*$C$22+AN144*$C$23+AP14...` |
| `D145` | `=(H145*$C$7+J145*$C$8+L145*$C$9+N145*$C$10+P145*$C$11+R145*$C$12+T145*$C$13+V145*$C$14+X145*$C$15+Z145*$C$16+AB145*$C$17+AD145*$C$18+AF145*$C$19+AH145*$C$20+AJ145*$C$21+AL145*$C$22+AN145*$C$23+AP14...` |
| `D146` | `=(H146*$C$7+J146*$C$8+L146*$C$9+N146*$C$10+P146*$C$11+R146*$C$12+T146*$C$13+V146*$C$14+X146*$C$15+Z146*$C$16+AB146*$C$17+AD146*$C$18+AF146*$C$19+AH146*$C$20+AJ146*$C$21+AL146*$C$22+AN146*$C$23+AP14...` |
| `D147` | `=(H147*$C$7+J147*$C$8+L147*$C$9+N147*$C$10+P147*$C$11+R147*$C$12+T147*$C$13+V147*$C$14+X147*$C$15+Z147*$C$16+AB147*$C$17+AD147*$C$18+AF147*$C$19+AH147*$C$20+AJ147*$C$21+AL147*$C$22+AN147*$C$23+AP14...` |
| `D148` | `=(H148*$C$7+J148*$C$8+L148*$C$9+N148*$C$10+P148*$C$11+R148*$C$12+T148*$C$13+V148*$C$14+X148*$C$15+Z148*$C$16+AB148*$C$17+AD148*$C$18+AF148*$C$19+AH148*$C$20+AJ148*$C$21+AL148*$C$22+AN148*$C$23+AP14...` |
| `D149` | `=(H149*$C$7+J149*$C$8+L149*$C$9+N149*$C$10+P149*$C$11+R149*$C$12+T149*$C$13+V149*$C$14+X149*$C$15+Z149*$C$16+AB149*$C$17+AD149*$C$18+AF149*$C$19+AH149*$C$20+AJ149*$C$21+AL149*$C$22+AN149*$C$23+AP14...` |
| `D150` | `=(H150*$C$7+J150*$C$8+L150*$C$9+N150*$C$10+P150*$C$11+R150*$C$12+T150*$C$13+V150*$C$14+X150*$C$15+Z150*$C$16+AB150*$C$17+AD150*$C$18+AF150*$C$19+AH150*$C$20+AJ150*$C$21+AL150*$C$22+AN150*$C$23+AP15...` |
| `D151` | `=(H151*$C$7+J151*$C$8+L151*$C$9+N151*$C$10+P151*$C$11+R151*$C$12+T151*$C$13+V151*$C$14+X151*$C$15+Z151*$C$16+AB151*$C$17+AD151*$C$18+AF151*$C$19+AH151*$C$20+AJ151*$C$21+AL151*$C$22+AN151*$C$23+AP15...` |
| `D152` | `=(H152*$C$7+J152*$C$8+L152*$C$9+N152*$C$10+P152*$C$11+R152*$C$12+T152*$C$13+V152*$C$14+X152*$C$15+Z152*$C$16+AB152*$C$17+AD152*$C$18+AF152*$C$19+AH152*$C$20+AJ152*$C$21+AL152*$C$22+AN152*$C$23+AP15...` |
| `D153` | `=(H153*$C$7+J153*$C$8+L153*$C$9+N153*$C$10+P153*$C$11+R153*$C$12+T153*$C$13+V153*$C$14+X153*$C$15+Z153*$C$16+AB153*$C$17+AD153*$C$18+AF153*$C$19+AH153*$C$20+AJ153*$C$21+AL153*$C$22+AN153*$C$23+AP15...` |
| `D154` | `=(H154*$C$7+J154*$C$8+L154*$C$9+N154*$C$10+P154*$C$11+R154*$C$12+T154*$C$13+V154*$C$14+X154*$C$15+Z154*$C$16+AB154*$C$17+AD154*$C$18+AF154*$C$19+AH154*$C$20+AJ154*$C$21+AL154*$C$22+AN154*$C$23+AP15...` |
| `D155` | `=(H155*$C$7+J155*$C$8+L155*$C$9+N155*$C$10+P155*$C$11+R155*$C$12+T155*$C$13+V155*$C$14+X155*$C$15+Z155*$C$16+AB155*$C$17+AD155*$C$18+AF155*$C$19+AH155*$C$20+AJ155*$C$21+AL155*$C$22+AN155*$C$23+AP15...` |
| `D156` | `=(H156*$C$7+J156*$C$8+L156*$C$9+N156*$C$10+P156*$C$11+R156*$C$12+T156*$C$13+V156*$C$14+X156*$C$15+Z156*$C$16+AB156*$C$17+AD156*$C$18+AF156*$C$19+AH156*$C$20+AJ156*$C$21+AL156*$C$22+AN156*$C$23+AP15...` |
| `D157` | `=(H157*$C$7+J157*$C$8+L157*$C$9+N157*$C$10+P157*$C$11+R157*$C$12+T157*$C$13+V157*$C$14+X157*$C$15+Z157*$C$16+AB157*$C$17+AD157*$C$18+AF157*$C$19+AH157*$C$20+AJ157*$C$21+AL157*$C$22+AN157*$C$23+AP15...` |
| `D158` | `=(H158*$C$7+J158*$C$8+L158*$C$9+N158*$C$10+P158*$C$11+R158*$C$12+T158*$C$13+V158*$C$14+X158*$C$15+Z158*$C$16+AB158*$C$17+AD158*$C$18+AF158*$C$19+AH158*$C$20+AJ158*$C$21+AL158*$C$22+AN158*$C$23+AP15...` |
| `D159` | `=(H159*$C$7+J159*$C$8+L159*$C$9+N159*$C$10+P159*$C$11+R159*$C$12+T159*$C$13+V159*$C$14+X159*$C$15+Z159*$C$16+AB159*$C$17+AD159*$C$18+AF159*$C$19+AH159*$C$20+AJ159*$C$21+AL159*$C$22+AN159*$C$23+AP15...` |
| `D160` | `=(H160*$C$7+J160*$C$8+L160*$C$9+N160*$C$10+P160*$C$11+R160*$C$12+T160*$C$13+V160*$C$14+X160*$C$15+Z160*$C$16+AB160*$C$17+AD160*$C$18+AF160*$C$19+AH160*$C$20+AJ160*$C$21+AL160*$C$22+AN160*$C$23+AP16...` |
| `D161` | `=(H161*$C$7+J161*$C$8+L161*$C$9+N161*$C$10+P161*$C$11+R161*$C$12+T161*$C$13+V161*$C$14+X161*$C$15+Z161*$C$16+AB161*$C$17+AD161*$C$18+AF161*$C$19+AH161*$C$20+AJ161*$C$21+AL161*$C$22+AN161*$C$23+AP16...` |
| `D162` | `=(H162*$C$7+J162*$C$8+L162*$C$9+N162*$C$10+P162*$C$11+R162*$C$12+T162*$C$13+V162*$C$14+X162*$C$15+Z162*$C$16+AB162*$C$17+AD162*$C$18+AF162*$C$19+AH162*$C$20+AJ162*$C$21+AL162*$C$22+AN162*$C$23+AP16...` |
| `D163` | `=(H163*$C$7+J163*$C$8+L163*$C$9+N163*$C$10+P163*$C$11+R163*$C$12+T163*$C$13+V163*$C$14+X163*$C$15+Z163*$C$16+AB163*$C$17+AD163*$C$18+AF163*$C$19+AH163*$C$20+AJ163*$C$21+AL163*$C$22+AN163*$C$23+AP16...` |
| `D164` | `=(H164*$C$7+J164*$C$8+L164*$C$9+N164*$C$10+P164*$C$11+R164*$C$12+T164*$C$13+V164*$C$14+X164*$C$15+Z164*$C$16+AB164*$C$17+AD164*$C$18+AF164*$C$19+AH164*$C$20+AJ164*$C$21+AL164*$C$22+AN164*$C$23+AP16...` |
| `D165` | `=(H165*$C$7+J165*$C$8+L165*$C$9+N165*$C$10+P165*$C$11+R165*$C$12+T165*$C$13+V165*$C$14+X165*$C$15+Z165*$C$16+AB165*$C$17+AD165*$C$18+AF165*$C$19+AH165*$C$20+AJ165*$C$21+AL165*$C$22+AN165*$C$23+AP16...` |
| `D166` | `=(H166*$C$7+J166*$C$8+L166*$C$9+N166*$C$10+P166*$C$11+R166*$C$12+T166*$C$13+V166*$C$14+X166*$C$15+Z166*$C$16+AB166*$C$17+AD166*$C$18+AF166*$C$19+AH166*$C$20+AJ166*$C$21+AL166*$C$22+AN166*$C$23+AP16...` |
| `D167` | `=(H167*$C$7+J167*$C$8+L167*$C$9+N167*$C$10+P167*$C$11+R167*$C$12+T167*$C$13+V167*$C$14+X167*$C$15+Z167*$C$16+AB167*$C$17+AD167*$C$18+AF167*$C$19+AH167*$C$20+AJ167*$C$21+AL167*$C$22+AN167*$C$23+AP16...` |
| `D168` | `=(H168*$C$7+J168*$C$8+L168*$C$9+N168*$C$10+P168*$C$11+R168*$C$12+T168*$C$13+V168*$C$14+X168*$C$15+Z168*$C$16+AB168*$C$17+AD168*$C$18+AF168*$C$19+AH168*$C$20+AJ168*$C$21+AL168*$C$22+AN168*$C$23+AP16...` |
| `D169` | `=(H169*$C$7+J169*$C$8+L169*$C$9+N169*$C$10+P169*$C$11+R169*$C$12+T169*$C$13+V169*$C$14+X169*$C$15+Z169*$C$16+AB169*$C$17+AD169*$C$18+AF169*$C$19+AH169*$C$20+AJ169*$C$21+AL169*$C$22+AN169*$C$23+AP16...` |
| `D170` | `=(H170*$C$7+J170*$C$8+L170*$C$9+N170*$C$10+P170*$C$11+R170*$C$12+T170*$C$13+V170*$C$14+X170*$C$15+Z170*$C$16+AB170*$C$17+AD170*$C$18+AF170*$C$19+AH170*$C$20+AJ170*$C$21+AL170*$C$22+AN170*$C$23+AP17...` |
| `D171` | `=(H171*$C$7+J171*$C$8+L171*$C$9+N171*$C$10+P171*$C$11+R171*$C$12+T171*$C$13+V171*$C$14+X171*$C$15+Z171*$C$16+AB171*$C$17+AD171*$C$18+AF171*$C$19+AH171*$C$20+AJ171*$C$21+AL171*$C$22+AN171*$C$23+AP17...` |
| `D172` | `=(H172*$C$7+J172*$C$8+L172*$C$9+N172*$C$10+P172*$C$11+R172*$C$12+T172*$C$13+V172*$C$14+X172*$C$15+Z172*$C$16+AB172*$C$17+AD172*$C$18+AF172*$C$19+AH172*$C$20+AJ172*$C$21+AL172*$C$22+AN172*$C$23+AP17...` |
| `D173` | `=(H173*$C$7+J173*$C$8+L173*$C$9+N173*$C$10+P173*$C$11+R173*$C$12+T173*$C$13+V173*$C$14+X173*$C$15+Z173*$C$16+AB173*$C$17+AD173*$C$18+AF173*$C$19+AH173*$C$20+AJ173*$C$21+AL173*$C$22+AN173*$C$23+AP17...` |
| `D174` | `=(H174*$C$7+J174*$C$8+L174*$C$9+N174*$C$10+P174*$C$11+R174*$C$12+T174*$C$13+V174*$C$14+X174*$C$15+Z174*$C$16+AB174*$C$17+AD174*$C$18+AF174*$C$19+AH174*$C$20+AJ174*$C$21+AL174*$C$22+AN174*$C$23+AP17...` |
| `D175` | `=(H175*$C$7+J175*$C$8+L175*$C$9+N175*$C$10+P175*$C$11+R175*$C$12+T175*$C$13+V175*$C$14+X175*$C$15+Z175*$C$16+AB175*$C$17+AD175*$C$18+AF175*$C$19+AH175*$C$20+AJ175*$C$21+AL175*$C$22+AN175*$C$23+AP17...` |
| `D176` | `=(H176*$C$7+J176*$C$8+L176*$C$9+N176*$C$10+P176*$C$11+R176*$C$12+T176*$C$13+V176*$C$14+X176*$C$15+Z176*$C$16+AB176*$C$17+AD176*$C$18+AF176*$C$19+AH176*$C$20+AJ176*$C$21+AL176*$C$22+AN176*$C$23+AP17...` |
| `D177` | `=(H177*$C$7+J177*$C$8+L177*$C$9+N177*$C$10+P177*$C$11+R177*$C$12+T177*$C$13+V177*$C$14+X177*$C$15+Z177*$C$16+AB177*$C$17+AD177*$C$18+AF177*$C$19+AH177*$C$20+AJ177*$C$21+AL177*$C$22+AN177*$C$23+AP17...` |
| `D178` | `=(H178*$C$7+J178*$C$8+L178*$C$9+N178*$C$10+P178*$C$11+R178*$C$12+T178*$C$13+V178*$C$14+X178*$C$15+Z178*$C$16+AB178*$C$17+AD178*$C$18+AF178*$C$19+AH178*$C$20+AJ178*$C$21+AL178*$C$22+AN178*$C$23+AP17...` |
| `D179` | `=(H179*$C$7+J179*$C$8+L179*$C$9+N179*$C$10+P179*$C$11+R179*$C$12+T179*$C$13+V179*$C$14+X179*$C$15+Z179*$C$16+AB179*$C$17+AD179*$C$18+AF179*$C$19+AH179*$C$20+AJ179*$C$21+AL179*$C$22+AN179*$C$23+AP17...` |
| `D180` | `=(H180*$C$7+J180*$C$8+L180*$C$9+N180*$C$10+P180*$C$11+R180*$C$12+T180*$C$13+V180*$C$14+X180*$C$15+Z180*$C$16+AB180*$C$17+AD180*$C$18+AF180*$C$19+AH180*$C$20+AJ180*$C$21+AL180*$C$22+AN180*$C$23+AP18...` |
| `D181` | `=(H181*$C$7+J181*$C$8+L181*$C$9+N181*$C$10+P181*$C$11+R181*$C$12+T181*$C$13+V181*$C$14+X181*$C$15+Z181*$C$16+AB181*$C$17+AD181*$C$18+AF181*$C$19+AH181*$C$20+AJ181*$C$21+AL181*$C$22+AN181*$C$23+AP18...` |
| `D182` | `=(H182*$C$7+J182*$C$8+L182*$C$9+N182*$C$10+P182*$C$11+R182*$C$12+T182*$C$13+V182*$C$14+X182*$C$15+Z182*$C$16+AB182*$C$17+AD182*$C$18+AF182*$C$19+AH182*$C$20+AJ182*$C$21+AL182*$C$22+AN182*$C$23+AP18...` |
| `D183` | `=(H183*$C$7+J183*$C$8+L183*$C$9+N183*$C$10+P183*$C$11+R183*$C$12+T183*$C$13+V183*$C$14+X183*$C$15+Z183*$C$16+AB183*$C$17+AD183*$C$18+AF183*$C$19+AH183*$C$20+AJ183*$C$21+AL183*$C$22+AN183*$C$23+AP18...` |
| `D184` | `=(H184*$C$7+J184*$C$8+L184*$C$9+N184*$C$10+P184*$C$11+R184*$C$12+T184*$C$13+V184*$C$14+X184*$C$15+Z184*$C$16+AB184*$C$17+AD184*$C$18+AF184*$C$19+AH184*$C$20+AJ184*$C$21+AL184*$C$22+AN184*$C$23+AP18...` |
| `D185` | `=(H185*$C$7+J185*$C$8+L185*$C$9+N185*$C$10+P185*$C$11+R185*$C$12+T185*$C$13+V185*$C$14+X185*$C$15+Z185*$C$16+AB185*$C$17+AD185*$C$18+AF185*$C$19+AH185*$C$20+AJ185*$C$21+AL185*$C$22+AN185*$C$23+AP18...` |
| `D186` | `=(H186*$C$7+J186*$C$8+L186*$C$9+N186*$C$10+P186*$C$11+R186*$C$12+T186*$C$13+V186*$C$14+X186*$C$15+Z186*$C$16+AB186*$C$17+AD186*$C$18+AF186*$C$19+AH186*$C$20+AJ186*$C$21+AL186*$C$22+AN186*$C$23+AP18...` |
| `D187` | `=(H187*$C$7+J187*$C$8+L187*$C$9+N187*$C$10+P187*$C$11+R187*$C$12+T187*$C$13+V187*$C$14+X187*$C$15+Z187*$C$16+AB187*$C$17+AD187*$C$18+AF187*$C$19+AH187*$C$20+AJ187*$C$21+AL187*$C$22+AN187*$C$23+AP18...` |
| `D188` | `=(H188*$C$7+J188*$C$8+L188*$C$9+N188*$C$10+P188*$C$11+R188*$C$12+T188*$C$13+V188*$C$14+X188*$C$15+Z188*$C$16+AB188*$C$17+AD188*$C$18+AF188*$C$19+AH188*$C$20+AJ188*$C$21+AL188*$C$22+AN188*$C$23+AP18...` |
| `D189` | `=(H189*$C$7+J189*$C$8+L189*$C$9+N189*$C$10+P189*$C$11+R189*$C$12+T189*$C$13+V189*$C$14+X189*$C$15+Z189*$C$16+AB189*$C$17+AD189*$C$18+AF189*$C$19+AH189*$C$20+AJ189*$C$21+AL189*$C$22+AN189*$C$23+AP18...` |
| `D190` | `=(H190*$C$7+J190*$C$8+L190*$C$9+N190*$C$10+P190*$C$11+R190*$C$12+T190*$C$13+V190*$C$14+X190*$C$15+Z190*$C$16+AB190*$C$17+AD190*$C$18+AF190*$C$19+AH190*$C$20+AJ190*$C$21+AL190*$C$22+AN190*$C$23+AP19...` |
| `D191` | `=(H191*$C$7+J191*$C$8+L191*$C$9+N191*$C$10+P191*$C$11+R191*$C$12+T191*$C$13+V191*$C$14+X191*$C$15+Z191*$C$16+AB191*$C$17+AD191*$C$18+AF191*$C$19+AH191*$C$20+AJ191*$C$21+AL191*$C$22+AN191*$C$23+AP19...` |
| `D192` | `=(H192*$C$7+J192*$C$8+L192*$C$9+N192*$C$10+P192*$C$11+R192*$C$12+T192*$C$13+V192*$C$14+X192*$C$15+Z192*$C$16+AB192*$C$17+AD192*$C$18+AF192*$C$19+AH192*$C$20+AJ192*$C$21+AL192*$C$22+AN192*$C$23+AP19...` |
| `D193` | `=(H193*$C$7+J193*$C$8+L193*$C$9+N193*$C$10+P193*$C$11+R193*$C$12+T193*$C$13+V193*$C$14+X193*$C$15+Z193*$C$16+AB193*$C$17+AD193*$C$18+AF193*$C$19+AH193*$C$20+AJ193*$C$21+AL193*$C$22+AN193*$C$23+AP19...` |
| `D194` | `=(H194*$C$7+J194*$C$8+L194*$C$9+N194*$C$10+P194*$C$11+R194*$C$12+T194*$C$13+V194*$C$14+X194*$C$15+Z194*$C$16+AB194*$C$17+AD194*$C$18+AF194*$C$19+AH194*$C$20+AJ194*$C$21+AL194*$C$22+AN194*$C$23+AP19...` |
| `D195` | `=(H195*$C$7+J195*$C$8+L195*$C$9+N195*$C$10+P195*$C$11+R195*$C$12+T195*$C$13+V195*$C$14+X195*$C$15+Z195*$C$16+AB195*$C$17+AD195*$C$18+AF195*$C$19+AH195*$C$20+AJ195*$C$21+AL195*$C$22+AN195*$C$23+AP19...` |
| `D196` | `=(H196*$C$7+J196*$C$8+L196*$C$9+N196*$C$10+P196*$C$11+R196*$C$12+T196*$C$13+V196*$C$14+X196*$C$15+Z196*$C$16+AB196*$C$17+AD196*$C$18+AF196*$C$19+AH196*$C$20+AJ196*$C$21+AL196*$C$22+AN196*$C$23+AP19...` |
| `D197` | `=(H197*$C$7+J197*$C$8+L197*$C$9+N197*$C$10+P197*$C$11+R197*$C$12+T197*$C$13+V197*$C$14+X197*$C$15+Z197*$C$16+AB197*$C$17+AD197*$C$18+AF197*$C$19+AH197*$C$20+AJ197*$C$21+AL197*$C$22+AN197*$C$23+AP19...` |
| `D198` | `=(H198*$C$7+J198*$C$8+L198*$C$9+N198*$C$10+P198*$C$11+R198*$C$12+T198*$C$13+V198*$C$14+X198*$C$15+Z198*$C$16+AB198*$C$17+AD198*$C$18+AF198*$C$19+AH198*$C$20+AJ198*$C$21+AL198*$C$22+AN198*$C$23+AP19...` |
| `D199` | `=(H199*$C$7+J199*$C$8+L199*$C$9+N199*$C$10+P199*$C$11+R199*$C$12+T199*$C$13+V199*$C$14+X199*$C$15+Z199*$C$16+AB199*$C$17+AD199*$C$18+AF199*$C$19+AH199*$C$20+AJ199*$C$21+AL199*$C$22+AN199*$C$23+AP19...` |
| `D200` | `=(H200*$C$7+J200*$C$8+L200*$C$9+N200*$C$10+P200*$C$11+R200*$C$12+T200*$C$13+V200*$C$14+X200*$C$15+Z200*$C$16+AB200*$C$17+AD200*$C$18+AF200*$C$19+AH200*$C$20+AJ200*$C$21+AL200*$C$22+AN200*$C$23+AP20...` |
| `D201` | `=(H201*$C$7+J201*$C$8+L201*$C$9+N201*$C$10+P201*$C$11+R201*$C$12+T201*$C$13+V201*$C$14+X201*$C$15+Z201*$C$16+AB201*$C$17+AD201*$C$18+AF201*$C$19+AH201*$C$20+AJ201*$C$21+AL201*$C$22+AN201*$C$23+AP20...` |
| `D202` | `=(H202*$C$7+J202*$C$8+L202*$C$9+N202*$C$10+P202*$C$11+R202*$C$12+T202*$C$13+V202*$C$14+X202*$C$15+Z202*$C$16+AB202*$C$17+AD202*$C$18+AF202*$C$19+AH202*$C$20+AJ202*$C$21+AL202*$C$22+AN202*$C$23+AP20...` |
| `D203` | `=(H203*$C$7+J203*$C$8+L203*$C$9+N203*$C$10+P203*$C$11+R203*$C$12+T203*$C$13+V203*$C$14+X203*$C$15+Z203*$C$16+AB203*$C$17+AD203*$C$18+AF203*$C$19+AH203*$C$20+AJ203*$C$21+AL203*$C$22+AN203*$C$23+AP20...` |
| `D204` | `=(H204*$C$7+J204*$C$8+L204*$C$9+N204*$C$10+P204*$C$11+R204*$C$12+T204*$C$13+V204*$C$14+X204*$C$15+Z204*$C$16+AB204*$C$17+AD204*$C$18+AF204*$C$19+AH204*$C$20+AJ204*$C$21+AL204*$C$22+AN204*$C$23+AP20...` |
| `D205` | `=(H205*$C$7+J205*$C$8+L205*$C$9+N205*$C$10+P205*$C$11+R205*$C$12+T205*$C$13+V205*$C$14+X205*$C$15+Z205*$C$16+AB205*$C$17+AD205*$C$18+AF205*$C$19+AH205*$C$20+AJ205*$C$21+AL205*$C$22+AN205*$C$23+AP20...` |
| `D206` | `=(H206*$C$7+J206*$C$8+L206*$C$9+N206*$C$10+P206*$C$11+R206*$C$12+T206*$C$13+V206*$C$14+X206*$C$15+Z206*$C$16+AB206*$C$17+AD206*$C$18+AF206*$C$19+AH206*$C$20+AJ206*$C$21+AL206*$C$22+AN206*$C$23+AP20...` |
| `D207` | `=(H207*$C$7+J207*$C$8+L207*$C$9+N207*$C$10+P207*$C$11+R207*$C$12+T207*$C$13+V207*$C$14+X207*$C$15+Z207*$C$16+AB207*$C$17+AD207*$C$18+AF207*$C$19+AH207*$C$20+AJ207*$C$21+AL207*$C$22+AN207*$C$23+AP20...` |
| `D208` | `=(H208*$C$7+J208*$C$8+L208*$C$9+N208*$C$10+P208*$C$11+R208*$C$12+T208*$C$13+V208*$C$14+X208*$C$15+Z208*$C$16+AB208*$C$17+AD208*$C$18+AF208*$C$19+AH208*$C$20+AJ208*$C$21+AL208*$C$22+AN208*$C$23+AP20...` |
| `D209` | `=(H209*$C$7+J209*$C$8+L209*$C$9+N209*$C$10+P209*$C$11+R209*$C$12+T209*$C$13+V209*$C$14+X209*$C$15+Z209*$C$16+AB209*$C$17+AD209*$C$18+AF209*$C$19+AH209*$C$20+AJ209*$C$21+AL209*$C$22+AN209*$C$23+AP20...` |
| `D210` | `=(H210*$C$7+J210*$C$8+L210*$C$9+N210*$C$10+P210*$C$11+R210*$C$12+T210*$C$13+V210*$C$14+X210*$C$15+Z210*$C$16+AB210*$C$17+AD210*$C$18+AF210*$C$19+AH210*$C$20+AJ210*$C$21+AL210*$C$22+AN210*$C$23+AP21...` |
| `D211` | `=(H211*$C$7+J211*$C$8+L211*$C$9+N211*$C$10+P211*$C$11+R211*$C$12+T211*$C$13+V211*$C$14+X211*$C$15+Z211*$C$16+AB211*$C$17+AD211*$C$18+AF211*$C$19+AH211*$C$20+AJ211*$C$21+AL211*$C$22+AN211*$C$23+AP21...` |
| `D212` | `=(H212*$C$7+J212*$C$8+L212*$C$9+N212*$C$10+P212*$C$11+R212*$C$12+T212*$C$13+V212*$C$14+X212*$C$15+Z212*$C$16+AB212*$C$17+AD212*$C$18+AF212*$C$19+AH212*$C$20+AJ212*$C$21+AL212*$C$22+AN212*$C$23+AP21...` |
| `D213` | `=(H213*$C$7+J213*$C$8+L213*$C$9+N213*$C$10+P213*$C$11+R213*$C$12+T213*$C$13+V213*$C$14+X213*$C$15+Z213*$C$16+AB213*$C$17+AD213*$C$18+AF213*$C$19+AH213*$C$20+AJ213*$C$21+AL213*$C$22+AN213*$C$23+AP21...` |
| `D214` | `=(H214*$C$7+J214*$C$8+L214*$C$9+N214*$C$10+P214*$C$11+R214*$C$12+T214*$C$13+V214*$C$14+X214*$C$15+Z214*$C$16+AB214*$C$17+AD214*$C$18+AF214*$C$19+AH214*$C$20+AJ214*$C$21+AL214*$C$22+AN214*$C$23+AP21...` |
| `D215` | `=(H215*$C$7+J215*$C$8+L215*$C$9+N215*$C$10+P215*$C$11+R215*$C$12+T215*$C$13+V215*$C$14+X215*$C$15+Z215*$C$16+AB215*$C$17+AD215*$C$18+AF215*$C$19+AH215*$C$20+AJ215*$C$21+AL215*$C$22+AN215*$C$23+AP21...` |
| `D216` | `=(H216*$C$7+J216*$C$8+L216*$C$9+N216*$C$10+P216*$C$11+R216*$C$12+T216*$C$13+V216*$C$14+X216*$C$15+Z216*$C$16+AB216*$C$17+AD216*$C$18+AF216*$C$19+AH216*$C$20+AJ216*$C$21+AL216*$C$22+AN216*$C$23+AP21...` |
| `D217` | `=(H217*$C$7+J217*$C$8+L217*$C$9+N217*$C$10+P217*$C$11+R217*$C$12+T217*$C$13+V217*$C$14+X217*$C$15+Z217*$C$16+AB217*$C$17+AD217*$C$18+AF217*$C$19+AH217*$C$20+AJ217*$C$21+AL217*$C$22+AN217*$C$23+AP21...` |
| `D218` | `=(H218*$C$7+J218*$C$8+L218*$C$9+N218*$C$10+P218*$C$11+R218*$C$12+T218*$C$13+V218*$C$14+X218*$C$15+Z218*$C$16+AB218*$C$17+AD218*$C$18+AF218*$C$19+AH218*$C$20+AJ218*$C$21+AL218*$C$22+AN218*$C$23+AP21...` |
| `D219` | `=(H219*$C$7+J219*$C$8+L219*$C$9+N219*$C$10+P219*$C$11+R219*$C$12+T219*$C$13+V219*$C$14+X219*$C$15+Z219*$C$16+AB219*$C$17+AD219*$C$18+AF219*$C$19+AH219*$C$20+AJ219*$C$21+AL219*$C$22+AN219*$C$23+AP21...` |
| `D220` | `=(H220*$C$7+J220*$C$8+L220*$C$9+N220*$C$10+P220*$C$11+R220*$C$12+T220*$C$13+V220*$C$14+X220*$C$15+Z220*$C$16+AB220*$C$17+AD220*$C$18+AF220*$C$19+AH220*$C$20+AJ220*$C$21+AL220*$C$22+AN220*$C$23+AP22...` |
| `D221` | `=(H221*$C$7+J221*$C$8+L221*$C$9+N221*$C$10+P221*$C$11+R221*$C$12+T221*$C$13+V221*$C$14+X221*$C$15+Z221*$C$16+AB221*$C$17+AD221*$C$18+AF221*$C$19+AH221*$C$20+AJ221*$C$21+AL221*$C$22+AN221*$C$23+AP22...` |
| `D222` | `=(H222*$C$7+J222*$C$8+L222*$C$9+N222*$C$10+P222*$C$11+R222*$C$12+T222*$C$13+V222*$C$14+X222*$C$15+Z222*$C$16+AB222*$C$17+AD222*$C$18+AF222*$C$19+AH222*$C$20+AJ222*$C$21+AL222*$C$22+AN222*$C$23+AP22...` |
| `D223` | `=(H223*$C$7+J223*$C$8+L223*$C$9+N223*$C$10+P223*$C$11+R223*$C$12+T223*$C$13+V223*$C$14+X223*$C$15+Z223*$C$16+AB223*$C$17+AD223*$C$18+AF223*$C$19+AH223*$C$20+AJ223*$C$21+AL223*$C$22+AN223*$C$23+AP22...` |
| `D224` | `=(H224*$C$7+J224*$C$8+L224*$C$9+N224*$C$10+P224*$C$11+R224*$C$12+T224*$C$13+V224*$C$14+X224*$C$15+Z224*$C$16+AB224*$C$17+AD224*$C$18+AF224*$C$19+AH224*$C$20+AJ224*$C$21+AL224*$C$22+AN224*$C$23+AP22...` |
| `D225` | `=(H225*$C$7+J225*$C$8+L225*$C$9+N225*$C$10+P225*$C$11+R225*$C$12+T225*$C$13+V225*$C$14+X225*$C$15+Z225*$C$16+AB225*$C$17+AD225*$C$18+AF225*$C$19+AH225*$C$20+AJ225*$C$21+AL225*$C$22+AN225*$C$23+AP22...` |
| `D226` | `=(H226*$C$7+J226*$C$8+L226*$C$9+N226*$C$10+P226*$C$11+R226*$C$12+T226*$C$13+V226*$C$14+X226*$C$15+Z226*$C$16+AB226*$C$17+AD226*$C$18+AF226*$C$19+AH226*$C$20+AJ226*$C$21+AL226*$C$22+AN226*$C$23+AP22...` |
| `D227` | `=(H227*$C$7+J227*$C$8+L227*$C$9+N227*$C$10+P227*$C$11+R227*$C$12+T227*$C$13+V227*$C$14+X227*$C$15+Z227*$C$16+AB227*$C$17+AD227*$C$18+AF227*$C$19+AH227*$C$20+AJ227*$C$21+AL227*$C$22+AN227*$C$23+AP22...` |
| `D228` | `=(H228*$C$7+J228*$C$8+L228*$C$9+N228*$C$10+P228*$C$11+R228*$C$12+T228*$C$13+V228*$C$14+X228*$C$15+Z228*$C$16+AB228*$C$17+AD228*$C$18+AF228*$C$19+AH228*$C$20+AJ228*$C$21+AL228*$C$22+AN228*$C$23+AP22...` |

... and 303 more formulas (truncated)

## Factor Metadata Sample

Source sheet: `3-Factor Data`

Headers: ['col_1', 'col_2', 'col_3', 'col_4', 'col_5', 'col_6', 'col_7', 'col_8', 'col_9', 'col_10', 'col_11', 'col_12', 'col_13', 'col_14']

Total rows: 292 (excluding header)

First 20 factors:

| col_1 | col_2 | col_3 | col_4 | col_5 | col_6 | col_7 | col_8 | col_9 | col_10 | col_11 | col_12 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Factor Intelligence Li... |  |  |  |  |  |  |  |  |  |  |  |
| View universal factor ... |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |
| Category | Factor Name | Factor Code | Relationship | IC | IC T-stat | Top Quintile Return (%) | Top Quintile IR | Q1-Q5 Spread Return (%) | Spread IR | Coverage (%) | Autocorrelation (%) |
| Filter | Filter | Filter | Filter | Filter | Filter | Filter | Filter | Filter | Filter | Filter | Filter |
| efficiency | Equity Turnover | equity_turn | Positive | 1.37521935778231 | 4.25170163083262 | 1.92115311826781 | 0.482617897348461 | 2.77941208067995 | 0.412785509962611 | 97.3561150126597 | 0.9886501543931481 |
| size | Book Value | bv | Inverse | 1.89339286807129 | 4.69039938853598 | 4.88241242968992 | 1.05565279769077 | 7.80311452584383 | 1.03655210845247 | 99.1208861940505 | 0.991878640544131 |
| technical | On-Balance Volume (252D) | obv_252d | Positive | 1.90055885729556 | 3.15891474215683 | 3.08990485270934 | 0.531265284760733 | 4.47505669138757 | 0.375751022248153 | 99.9984798513716 | 0.889912065722666 |
| size | Midcap | midcap | Inverse | 1.4028351989317 | 2.45433238898501 | 4.65256215074325 | 0.664012077674092 | 7.63072597281469 | 0.67666721623283 | 100 | 0.994198267671694 |
| short | Days to Cover | days_to_cover | Inverse | 1.75111125670913 | 5.52855617780306 | 1.49536943131652 | 0.431788979296344 | 3.31099550999251 | 0.588924156308917 | 72.3991104182622 | 0.773713896304915 |
| crowding | Passive Percentage Out... | passive_pctout | Inverse | 2.56960270499106 | 6.13719456425249 | 2.911511645942 | 0.789761246123792 | 7.5037442756398 | 1.07035810150214 | 16.9773865716076 | 0.989905356398842 |
| crowding | Hedge Fund Percentage ... | hf_pcprt | Positive | 2.81953086361645 | 5.19530178876076 | 3.35649498161615 | 0.642865788034959 | 6.45699844669216 | 0.667472220035522 | 16.9741080956005 | 0.9678108866681719 |
| momentum | Return Momentum (252D) | ret_mom_252d | Positive | 1.91382890581844 | 2.30260946195158 | 2.71078407028806 | 0.363479677027832 | 3.48861162889146 | 0.21083365617963 | 99.237482475989 | 0.885121644089437 |
| size | Assets | assets | Inverse | 1.4507225015952 | 3.12001152152347 | 3.67473827142265 | 0.756356753045383 | 6.52444826510831 | 0.824747024775652 | 99.3653336178145 | 0.9946631496287109 |
| efficiency | Asset Turnover | asset_turn | Positive | 1.35744886164547 | 3.64004591600206 | 1.62196716975107 | 0.438898117061167 | 2.76818155431744 | 0.458515354454842 | 99.0396567435576 | 0.9909652351849719 |
| value | Free Cash Flow to Ente... | fcf_ev | Positive | 1.17381073881098 | 2.73446357502335 | 2.08302508469067 | 0.484769858941515 | 2.7534882435871 | 0.362024536084877 | 89.9770369611535 | 0.92715974392477 |
| management | CAPEX to Depreciation | capex_depr | Inverse | 0.899988501973998 | 2.94753836080475 | 0.846640700048699 | 0.257577712903933 | 0.896065558219938 | 0.15148637230969 | 94.0652814744603 | 0.968640939156991 |
| profitability | Cash Flow Return on In... | cfroic | Positive | 1.41943971800185 | 3.41461844605571 | 1.32799395317609 | 0.344314111560683 | 2.18053075017633 | 0.260997170621121 | 98.3197273825373 | 0.9640618544699019 |
| short | Short Interest / Share... | short_pct_chg_12m | Inverse | 1.18256526083126 | 3.84484116797243 | 1.54383760101692 | 0.444327545203067 | 3.80309225196508 | 0.701081198230951 | 69.2252136691015 | 0.771929702412614 |
| profitability | Cash Flow Return on Eq... | cfroe | Positive | 1.27798249868379 | 3.68904030708186 | 0.853945206618869 | 0.264464000943632 | 1.56959311122992 | 0.223499287661771 | 96.2932518079149 | 0.957706294237733 |

## VBA Source Code

### Module: `Sheet1.cls`

- **Stream:** `VBA/Sheet1`
- **File:** `xl/vbaProject.bin`

```vb
Attribute VB_Name = "Sheet1"
Attribute VB_Base = "0{00020820-0000-0000-C000-000000000046}"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = True
Attribute VB_TemplateDerived = False
Attribute VB_Customizable = True
'========================================
' Tab 1 (1-Configuration) - COMBINED VBA
'========================================
' HIERARCHICAL ORGANIZATION (Bottom to Top - Operational Order):
'
' USER-FACING MACROS (ordered by execution sequence):
'   1. Tab1_01_ClearFormattingAroundFactorBank      - Lowest level: Clear protected rows
'   2. Tab1_02_ApplyAlternatingRowsToFactorBank     - Base layer: Alternating rows (A-F)
'   3. Tab1_03_ApplyAlternatingRowsToSelectedFactors - Base layer: Alternating rows (A-F)
'   4. Tab1_04_ReapplyYellowHighlighting            - Top layer: Yellow highlighting (B-E)
'   5. Tab1_05_ApplySystematicFactorsFormatting     - Top layer: Red "No" formatting (F)
'   6. Tab1_06_RefreshAllTab1Formatting             - Master: Calls all in correct order
'
' FORMATTING LAYERS:
'   Columns A-F: Alternating rows (base) + Yellow (B-E) + Systematic Factors formatting (F) on top
'   Column F: "Yes" (default) or "No" (red background + dark red text)
'   Columns G-J: Conditional formatting ONLY (no direct fills)
'
' AUTOMATIC EVENT HANDLERS (run automatically):
'   - Worksheet_Change                  - Handles YES/NO factor selection
'   - Worksheet_Activate                - Runs when sheet activated
'
' INTERNAL SUBROUTINES (called by events):
'   - HandleFactorSelection             - Process factor selection
'   - MoveFromBankToSelected            - Move factor to Selected
'   - MoveFromSelectedToBank            - Move factor to Bank
'
'========================================

Option Explicit

'========================================
' PART 1: USER-FACING MACROS (Operational Order: Bottom to Top)
'========================================

Sub Tab1_01_ClearFormattingAroundFactorBank()
    '=====================================================================
    ' STEP 1 (Lowest Level): Clear conditional formatting from protected rows
    ' Protected: 2 rows above FACTOR BANK (blank) and 1 row below (header)
    '=====================================================================

    On Error Resume Next

    Dim ws As Worksheet
    Set ws = Me

    Dim factorBankRow As Long
    factorBankRow = 0

    ' Find "FACTOR BANK" in Column A
    Dim r As Long
    For r = 1 To 100
        Dim cellText As String
        cellText = Trim(UCase(CStr(ws.Cells(r, 1).Value)))

        If InStr(cellText, "FACTOR BANK") > 0 Then
            factorBankRow = r
            Exit For
        End If
    Next r

    ' If not found, exit
    If factorBankRow = 0 Then Exit Sub

    ' Clear conditional formatting from:
    ' - 2 rows above FACTOR BANK (blank rows)
    ' - 1 row below FACTOR BANK (header row)
    Dim protectedRows As Variant
    protectedRows = Array(factorBankRow - 2, factorBankRow - 1, factorBankRow + 1)

    Dim protRow As Variant
    For Each protRow In protectedRows
        If protRow > 0 And protRow <= ws.Rows.Count Then
            ' Clear conditional formatting from columns G, H, I, J
            ws.Range("G" & protRow & ":J" & protRow).FormatConditions.Delete
        End If
    Next protRow

End Sub

Sub Tab1_02_ApplyAlternatingRowsToFactorBank()
    '=====================================================================
    ' STEP 2 (Base Layer): Alternating white/gray rows for Factor Bank (columns A-F)
    ' Column F will have conditional formatting (green for "Yes") applied on top
    ' Columns G-J have conditional formatting (quintiles, relationship colors)
    ' PRESERVES yellow highlighting on columns B-E for highest IC factors
    '=====================================================================
    Dim ws As Worksheet
    Dim bankStart As Long
    Dim bankEnd As Long
    Dim i As Long
    Dim rowIdx As Long
    Dim col As Long
    Dim cell As Range
    Dim isYellowRow As Boolean

    ' Reference to this worksheet
    Set ws = Me

    ' Find Factor Bank start
    bankStart = 0
    For i = 1 To 200
        If InStr(1, UCase(ws.Cells(i, 1).Value), "FACTOR BANK") > 0 Then
            bankStart = i + 2  ' Data starts 2 rows after header
            Exit For
        End If
    Next i

    If bankStart = 0 Then
        MsgBox "Could not find FACTOR BANK section", vbCritical
        Exit Sub
    End If

    ' Find Factor Bank end (first empty row in column E)
    bankEnd = bankStart
    For i = bankStart To 500
        If ws.Cells(i, 5).Value = "" Then
            bankEnd = i - 1
            Exit For
        End If
    Next i

    ' Define colors
    Const COLOR_WHITE As Long = 16777215        ' RGB(255, 255, 255)
    Const COLOR_LIGHT_GRAY As Long = 15921906   ' RGB(242, 242, 242)
    Const COLOR_YELLOW As Long = 65535          ' RGB(255, 255, 0)
    Const COLOR_GREEN As Long = 13434828        ' RGB(200, 230, 201) - Light green for "Yes"

    ' Apply alternating rows to columns A-F
    For rowIdx = 0 To (bankEnd - bankStart)
        i = bankStart + rowIdx

        ' Check if this row has yellow highlighting (check column B)
        isYellowRow = (ws.Cells(i, 2).Interior.Color = COLOR_YELLOW)

        ' Check if column F has green highlighting (for "Yes")
        Dim isGreenActive As Boolean
        isGreenActive = (ws.Cells(i, 6).Interior.Color = COLOR_GREEN)

        ' Determine alternating color (even rows = white, odd rows = gray)
        Dim rowColor As Long
        If rowIdx Mod 2 = 0 Then
            rowColor = COLOR_WHITE
        Else
            rowColor = COLOR_LIGHT_GRAY
        End If

        ' Apply to columns A-F
        For col = 1 To 6
            Set cell = ws.Cells(i, col)

            ' Preserve yellow highlighting for columns B-E
            If isYellowRow And (col >= 2 And col <= 5) Then
                cell.Interior.Color = COLOR_YELLOW
            ' Preserve green highlighting for column F
            ElseIf isGreenActive And col = 6 Then
                cell.Interior.Color = COLOR_GREEN
            Else
                ' Apply alternating color
                cell.Interior.Color = rowColor
            End If
        Next col

        ' DO NOT touch columns G-J (7-10) - they have conditional formatting (quintiles, relationship)
    Next rowIdx

End Sub

Sub Tab1_03_ApplyAlternatingRowsToSelectedFactors()
    '=====================================================================
    ' STEP 3 (Base Layer): Alternating white/gray rows for Selected Factors (columns A-F)
    ' Column F will have conditional formatting (green for "Yes") applied on top
    ' Columns G-J have conditional formatting (quintiles, relationship colors)
    ' PRESERVES yellow highlighting on columns B-E for highest IC factors
    '=====================================================================
    Dim ws As Worksheet
    Dim selectedStart As Long
    Dim selectedEnd As Long
    Dim i As Long
    Dim rowIdx As Long
    Dim col As Long
    Dim cell As Range
    Dim isYellowRow As Boolean

    ' Reference to this worksheet
    Set ws = Me

    ' Find Selected Factors start
    selectedStart = 0
    For i = 1 To 200
        If InStr(1, UCase(ws.Cells(i, 1).Value), "SELECTED FACTORS") > 0 Then
            selectedStart = i + 2  ' Data starts 2 rows after header
            Exit For
        End If
    Next i

    If selectedStart = 0 Then Exit Sub

    ' Find Selected Factors end (first empty row in column E)
    selectedEnd = selectedStart
    For i = selectedStart To 500
        If ws.Cells(i, 5).Value = "" Then
            selectedEnd = i - 1
            Exit For
        End If
    Next i

    ' If no data, exit
    If selectedEnd < selectedStart Then Exit Sub

    ' Define colors
    Const COLOR_WHITE As Long = 16777215        ' RGB(255, 255, 255)
    Const COLOR_LIGHT_GRAY As Long = 15921906   ' RGB(242, 242, 242)
    Const COLOR_YELLOW As Long = 65535          ' RGB(255, 255, 0)
    Const COLOR_GREEN As Long = 13434828        ' RGB(200, 230, 201) - Light green for "Yes"

    ' Apply alternating rows to columns A-F
    For rowIdx = 0 To (selectedEnd - selectedStart)
        i = selectedStart + rowIdx

        ' Check if this row has yellow highlighting (check column B)
        isYellowRow = (ws.Cells(i, 2).Interior.Color = COLOR_YELLOW)

        ' Check if column F has green highlighting (for "Yes")
        Dim isGreenActive As Boolean
        isGreenActive = (ws.Cells(i, 6).Interior.Color = COLOR_GREEN)

        ' Determine alternating color (even rows = white, odd rows = gray)
        Dim rowColor As Long
        If rowIdx Mod 2 = 0 Then
            rowColor = COLOR_WHITE
        Else
            rowColor = COLOR_LIGHT_GRAY
        End If

        ' Apply to columns A-F
        ' Column F will have conditional formatting (green for "Yes") applied on top
        For col = 1 To 6
            Set cell = ws.Cells(i, col)

            ' Preserve yellow highlighting for columns B-E
            If isYellowRow And (col >= 2 And col <= 5) Then
                cell.Interior.Color = COLOR_YELLOW
            ' Preserve green highlighting for column F
            ElseIf isGreenActive And col = 6 Then
                cell.Interior.Color = COLOR_GREEN
            Else
                ' Apply alternating color
                cell.Interior.Color = rowColor
            End If
        Next col

        ' DO NOT touch columns G-J (7-10)
        ' Column G: Coverage (conditional: percentile-based quintile colors)
        ' Column H: Relationship (conditional: green for "Positive", red for "Inverse")
        ' Column I: IC (conditional: percentile-based quintile colors)
        ' Column J: Autocorrelation (conditional: percentile-based quintile colors)
        '
        ' Applying direct cell fills to these columns would HIDE the conditional formatting
        ' By leaving them untouched, Excel displays conditional formatting on top of no fill
    Next rowIdx

End Sub

Sub Tab1_04_ReapplyYellowHighlighting()
    '=====================================================================
    ' STEP 4 (Top Layer): Apply yellow highlighting to highest IC factors
    ' Searches BOTH Selected Factors AND Factor Bank sections
    ' Yellow highlighting follows the factor regardless of which section it's in
    ' MUST run AFTER alternating rows to sit on top of base formatting
    '=====================================================================
    Dim ws As Worksheet
    Dim selectedStart As Long, selectedEnd As Long
    Dim bankStart As Long, bankEnd As Long
    Dim i As Long
    Dim categories As Object
    Dim category As String
    Dim factorCode As String
    Dim icValue As Variant
    Dim bestIC As Double
    Dim bestRow As Long

    Set ws = Me
    Set categories = CreateObject("Scripting.Dictionary")

    ' Find Selected Factors start
    selectedStart = 0
    For i = 1 To 200
        If InStr(1, UCase(ws.Cells(i, 1).Value), "SELECTED FACTORS") > 0 Then
            selectedStart = i + 2
            Exit For
        End If
    Next i

    ' Find Factor Bank start
    bankStart = 0
    For i = 1 To 200
        If InStr(1, UCase(ws.Cells(i, 1).Value), "FACTOR BANK") > 0 Then
            bankStart = i + 2
            Exit For
        End If
    Next i

    If bankStart = 0 Then Exit Sub

    ' Find Selected Factors end (if exists)
    If selectedStart > 0 Then
        selectedEnd = selectedStart
        For i = selectedStart To bankStart - 3
            If ws.Cells(i, 5).Value = "" Then
                selectedEnd = i - 1
                Exit For
            End If
        Next i
        If selectedEnd < selectedStart Then selectedEnd = selectedStart - 1
    Else
        selectedEnd = 0
    End If

    ' Find Factor Bank end
    bankEnd = bankStart
    For i = bankStart To 500
        If ws.Cells(i, 5).Value = "" Then
            bankEnd = i - 1
            Exit For
        End If
    Next i

    ' Find highest IC in each category across BOTH sections
    ' First check Selected Factors
    If selectedStart > 0 And selectedEnd >= selectedStart Then
        For i = selectedStart To selectedEnd
            category = Trim(CStr(ws.Cells(i, 2).Value))
            factorCode = Trim(CStr(ws.Cells(i, 5).Value))

            If category = "" Or factorCode = "" Then GoTo NextSelectedFactor

            ' Get IC value from column I (9)
            icValue = ws.Cells(i, 9).Value

            If IsNumeric(icValue) Then
                If Not categories.Exists(category) Then
                    categories.Add category, Array(i, CDbl(icValue))
                Else
                    If CDbl(icValue) > categories(category)(1) Then
                        categories(category) = Array(i, CDbl(icValue))
                    End If
                End If
            End If

NextSelectedFactor:
        Next i
    End If

    ' Then check Factor Bank
    For i = bankStart To bankEnd
        category = Trim(CStr(ws.Cells(i, 2).Value))
        factorCode = Trim(CStr(ws.Cells(i, 5).Value))

        If category = "" Or factorCode = "" Then GoTo NextBankFactor

        ' Get IC value from column I (9)
        icValue = ws.Cells(i, 9).Value

        If IsNumeric(icValue) Then
            If Not categories.Exists(category) Then
                categories.Add category, Array(i, CDbl(icValue))
            Else
                If CDbl(icValue) > categories(category)(1) Then
                    categories(category) = Array(i, CDbl(icValue))
                End If
            End If
        End If

NextBankFactor:
    Next i

    ' Clear all yellow highlighting from BOTH sections
    Const COLOR_WHITE As Long = 16777215
    Const COLOR_LIGHT_GRAY As Long = 15921906

    ' Clear Selected Factors
    If selectedStart > 0 And selectedEnd >= selectedStart Then
        For i = selectedStart To selectedEnd
            Dim selectedIdx As Long
            selectedIdx = i - selectedStart

            Dim selectedColor As Long
            If selectedIdx Mod 2 = 0 Then
                selectedColor = COLOR_WHITE
            Else
                selectedColor = COLOR_LIGHT_GRAY
            End If

            ws.Cells(i, 2).Interior.Color = selectedColor
            ws.Cells(i, 3).Interior.Color = selectedColor
            ws.Cells(i, 4).Interior.Color = selectedColor
            ws.Cells(i, 5).Interior.Color = selectedColor
        Next i
    End If

    ' Clear Factor Bank
    For i = bankStart To bankEnd
        Dim bankIdx As Long
        bankIdx = i - bankStart

        Dim bankColor As Long
        If bankIdx Mod 2 = 0 Then
            bankColor = COLOR_WHITE
        Else
            bankColor = COLOR_LIGHT_GRAY
        End If

        ws.Cells(i, 2).Interior.Color = bankColor
        ws.Cells(i, 3).Interior.Color = bankColor
        ws.Cells(i, 4).Interior.Color = bankColor
        ws.Cells(i, 5).Interior.Color = bankColor
    Next i

    ' Apply yellow highlighting to highest IC factors (in either section)
    Const COLOR_YELLOW As Long = 65535

    Dim key As Variant
    For Each key In categories.Keys
        bestRow = categories(key)(0)

        ' Apply yellow to columns B-E
        ws.Cells(bestRow, 2).Interior.Color = COLOR_YELLOW
        ws.Cells(bestRow, 3).Interior.Color = COLOR_YELLOW
        ws.Cells(bestRow, 4).Interior.Color = COLOR_YELLOW
        ws.Cells(bestRow, 5).Interior.Color = COLOR_YELLOW
    Next key

End Sub

Sub Tab1_05_ApplySystematicFactorsFormatting()
    '=====================================================================
    ' STEP 5: Apply "Systematic Factors" column formatting (Column F)
    ' - Applies red background + dark red text (regular weight) to "No" values
    ' - Matches "Inverse" formatting style from column H (Relationship)
    ' Excel default red: Background #FFC7CE, Text #9C0006, Regular (not bold)
    '=====================================================================
    Dim ws As Worksheet
    Dim selectedStart As Long, selectedEnd As Long
    Dim bankStart As Long, bankEnd As Long
    Dim i As Long

    Set ws = Me

    ' Define Excel's default red conditional formatting colors (matches "Inverse" in column H)
    Const COLOR_RED_BG As Long = 13551615      ' RGB(255, 199, 206) = #FFC7CE
    Const COLOR_RED_TEXT As Long = 393372     ' RGB(156, 0, 6) = #9C0006
    Const COLOR_BLACK_TEXT As Long = 0         ' RGB(0, 0, 0) = Black

    ' Find Selected Factors start
    selectedStart = 0
    For i = 1 To 200
        If InStr(1, UCase(ws.Cells(i, 1).Value), "SELECTED FACTORS") > 0 Then
            selectedStart = i + 2  ' Data starts 2 rows after header
            Exit For
        End If
    Next i

    ' Find Factor Bank start
    bankStart = 0
    For i = 1 To 200
        If InStr(1, UCase(ws.Cells(i, 1).Value), "FACTOR BANK") > 0 Then
            bankStart = i + 2  ' Data starts 2 rows after header
            Exit For
        End If
    Next i

    If bankStart = 0 Then Exit Sub

    ' Find Selected Factors end (if exists)
    If selectedStart > 0 Then
        selectedEnd = selectedStart
        For i = selectedStart To bankStart - 3
            If ws.Cells(i, 5).Value = "" Then
                selectedEnd = i - 1
                Exit For
            End If
        Next i
        If selectedEnd < selectedStart Then selectedEnd = 0
    Else
        selectedEnd = 0
    End If

    ' Find Factor Bank end
    bankEnd = bankStart
    For i = bankStart To 500
        If ws.Cells(i, 5).Value = "" Then
            bankEnd = i - 1
            Exit For
        End If
    Next i

    ' Apply formatting to Selected Factors section
    If selectedStart > 0 And selectedEnd >= selectedStart Then
        For i = selectedStart To selectedEnd
            Dim cellValue As String
            cellValue = Trim(UCase(CStr(ws.Cells(i, 6).Value)))

            ' Apply formatting based on value (do not modify cell values)
            If cellValue = "NO" Then
                ws.Cells(i, 6).Interior.Color = COLOR_RED_BG
                ws.Cells(i, 6).Font.Color = COLOR_RED_TEXT
                ws.Cells(i, 6).Font.Bold = False  ' Regular weight, not bold
            ElseIf cellValue = "YES" Then
                ' Reset to default (alternating row color will be applied by other functions)
                ws.Cells(i, 6).Font.Color = COLOR_BLACK_TEXT
                ws.Cells(i, 6).Font.Bold = False
            End If
        Next i
    End If

    ' Apply formatting to Factor Bank section
    For i = bankStart To bankEnd
        cellValue = Trim(UCase(CStr(ws.Cells(i, 6).Value)))

        ' Apply formatting based on value (do not modify cell values)
        If cellValue = "NO" Then
            ws.Cells(i, 6).Interior.Color = COLOR_RED_BG
            ws.Cells(i, 6).Font.Color = COLOR_RED_TEXT
            ws.Cells(i, 6).Font.Bold = False  ' Regular weight, not bold
        ElseIf cellValue = "YES" Then
            ' Reset to default (alternating row color will be applied by other functions)
            ws.Cells(i, 6).Font.Color = COLOR_BLACK_TEXT
            ws.Cells(i, 6).Font.Bold = False
        End If
    Next i

End Sub

Sub Tab1_06_RefreshAllFormatting()
    '=====================================================================
    ' STEP 6 (Master Function): Refresh ALL Tab 1 formatting in correct order
    ' Call this after any sorting operation or data changes
    ' Executes all formatting steps in proper sequence
    '=====================================================================
    Call Tab1_01_ClearFormattingAroundFactorBank
    Call Tab1_02_ApplyAlternatingRowsToFactorBank
    Call Tab1_03_ApplyAlternatingRowsToSelectedFactors
    Call Tab1_04_ReapplyYellowHighlighting
    Call Tab1_05_ApplySystematicFactorsFormatting
End Sub

'========================================
' PART 2: AUTOMATIC EVENT HANDLERS
'========================================

Private Sub Worksheet_Change(ByVal Target As Range)
    On Error GoTo ErrorHandler

    ' Handle Column A changes (YES/NO factor selection)
    If Target.Column = 1 And Target.Cells.Count = 1 Then
        Call HandleFactorSelection(Target)
    End If

    ' Handle Column G-J changes (clear formatting around FACTOR BANK)
    If Target.Column >= 7 And Target.Column <= 10 Then
        Call Tab1_01_ClearFormattingAroundFactorBank
    End If

    Exit Sub

ErrorHandler:
    Application.EnableEvents = True
    Application.ScreenUpdating = True
    MsgBox "Error " & Err.Number & ": " & Err.Description, vbCritical
End Sub

Private Sub Worksheet_Activate()
    '=====================================================================
    ' Run when sheet is activated (clear formatting around FACTOR BANK)
    '=====================================================================
    On Error Resume Next
    Call Tab1_01_ClearFormattingAroundFactorBank
End Sub

'========================================
' PART 3: INTERNAL SUBROUTINES (Called by Events)
'========================================

Private Sub HandleFactorSelection(Target As Range)
    '=====================================================================
    ' Handle YES/NO changes in Column A
    '=====================================================================
    On Error GoTo ErrorHandler

    Application.EnableEvents = False
    Application.ScreenUpdating = False

    Dim changedRow As Long
    changedRow = Target.Row

    Dim factorCode As String
    factorCode = Trim(CStr(Me.Cells(changedRow, 5).Value))

    If factorCode = "" Or factorCode = "Code" Then GoTo Cleanup

    Dim newValue As String
    newValue = UCase(Trim(CStr(Target.Value)))

    Dim selectedStart As Long, bankStart As Long

    ' Find sections dynamically
    Dim r As Long
    selectedStart = 0
    bankStart = 0

    For r = 1 To 50
        On Error Resume Next
        Dim cellText As String
        cellText = ""
        cellText = CStr(Me.Cells(r, 1).Value)
        cellText = UCase(Trim(cellText))
        On Error GoTo ErrorHandler

        ' Exact match for "SELECTED FACTORS"
        If cellText = "SELECTED FACTORS" Then
            selectedStart = r + 2  ' Data starts 2 rows after header
        End If

        ' Exact match for "FACTOR BANK"
        If cellText = "FACTOR BANK" Then
            bankStart = r + 2
            Exit For
        End If
    Next r

    ' Validation
    If selectedStart = 0 Or bankStart = 0 Then
        MsgBox "Cannot find sections. Selected at row " & (selectedStart - 2) & ", Bank at row " & (bankStart - 2), vbCritical
        GoTo Cleanup
    End If

    If changedRow >= bankStart Then
        If newValue = "YES" Then
            Call MoveFromBankToSelected(Me, changedRow, selectedStart, bankStart)
        End If
    ElseIf changedRow >= selectedStart And changedRow < (bankStart - 2) Then
        If newValue = "NO" Then
            Call MoveFromSelectedToBank(Me, changedRow, selectedStart, bankStart)
        End If
    End If

Cleanup:
    Application.EnableEvents = True
    Application.ScreenUpdating = True
    Exit Sub

ErrorHandler:
    Application.EnableEvents = True
    Application.ScreenUpdating = True
    MsgBox "Error " & Err.Number & ": " & Err.Description & vbCrLf & "Row: " & changedRow, vbCritical
End Sub

Private Sub MoveFromBankToSelected(ws As Worksheet, sourceRow As Long, selectedStart As Long, bankStart As Long)
    Dim factorGroup As String
    Dim factorPPS As Double

    factorGroup = Trim(CStr(ws.Cells(sourceRow, 2).Value))
    factorPPS = Val(ws.Cells(sourceRow, 7).Value)

    Dim insertRow As Long
    insertRow = selectedStart

    Dim r As Long
    Dim selectedEnd As Long
    selectedEnd = bankStart - 3  ' End of Selected Factors is 3 rows before Factor Bank header

    Dim foundGroup As Boolean
    foundGroup = False

    For r = selectedStart To selectedEnd
        Dim checkCode As String
        checkCode = Trim(CStr(ws.Cells(r, 5).Value))

        If checkCode = "" Then
            insertRow = r
            Exit For
        End If

        Dim checkGroup As String
        checkGroup = Trim(CStr(ws.Cells(r, 2).Value))

        ' First: Find matching group
        If checkGroup = factorGroup Then
            foundGroup = True

            ' Second: Within group, sort by PPS (coverage) descending
            Dim checkPPS As Double
            checkPPS = Val(ws.Cells(r, 7).Value)

            If factorPPS > checkPPS Then
                insertRow = r
                Exit For
            End If

            insertRow = r + 1

        ' If we found the group but now see a different group, insert here (end of our group)
        ElseIf foundGroup = True Then
            insertRow = r
            Exit For
        End If
    Next r

    ws.Rows(sourceRow).Cut
    ws.Rows(insertRow).Insert Shift:=xlDown
    ws.Cells(insertRow, 1).Value = "YES"

    ' Refresh all formatting after move (uses master function)
    Call Tab1_06_RefreshAllFormatting
End Sub

Private Sub MoveFromSelectedToBank(ws As Worksheet, sourceRow As Long, selectedStart As Long, bankStart As Long)
    Dim factorGroup As String
    Dim factorPPS As Double

    factorGroup = Trim(CStr(ws.Cells(sourceRow, 2).Value))
    factorPPS = Val(ws.Cells(sourceRow, 7).Value)

    Dim insertRow As Long
    insertRow = bankStart

    Dim lastRow As Long
    lastRow = ws.Cells(ws.Rows.Count, 5).End(xlUp).Row

    Dim foundGroup As Boolean
    foundGroup = False

    Dim r As Long
    For r = bankStart To lastRow
        Dim checkCode As String
        checkCode = Trim(CStr(ws.Cells(r, 5).Value))

        If checkCode = "" Or checkCode = "Code" Then GoTo NextRow

        Dim checkGroup As String
        checkGroup = Trim(CStr(ws.Cells(r, 2).Value))

        If checkGroup = factorGroup Then
            foundGroup = True

            Dim checkPPS As Double
            checkPPS = Val(ws.Cells(r, 7).Value)

            If factorPPS > checkPPS Then
                insertRow = r
                Exit For
            End If

            insertRow = r + 1

        ElseIf foundGroup = True Then
            insertRow = r
            Exit For
        End If

NextRow:
    Next r

    ws.Rows(sourceRow).Cut
    ws.Rows(insertRow).Insert Shift:=xlDown
    ws.Cells(insertRow, 1).Value = "NO"

    ' Refresh all formatting after move (uses master function)
    Call Tab1_06_RefreshAllFormatting
End Sub


```

### Module: `ThisWorkbook.cls`

- **Stream:** `VBA/ThisWorkbook`
- **File:** `xl/vbaProject.bin`

```vb
Attribute VB_Name = "ThisWorkbook"
Attribute VB_Base = "0{00020819-0000-0000-C000-000000000046}"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = True
Attribute VB_TemplateDerived = False
Attribute VB_Customizable = True
Private Sub Workbook_Open()
    '=====================================================================
    ' Auto-Sort on File Open + Factor Status Cleanup
    '=====================================================================
    ' INSTALLATION: Copy this code into ThisWorkbook code window
    '
    ' WHAT IT DOES:
    ' - Cleans up Tab 1 factor status (Factor Bank = all NO, Selected Factors = all YES)
    ' - Sorts Tab 4 by composite score (descending)
    ' - Updates rank numbers (1, 2, 3...)
    '
    ' Version: 3.4
    ' Date: October 31, 2025
    ' Update: Added absolute path fallback for logo loading
    '=====================================================================

    On Error Resume Next

    Application.ScreenUpdating = False

    ' =====================================================================
    ' PART 0: Re-insert Logo to Tab 1 (Centered in merged A2:J2)
    ' =====================================================================
    Dim ws1 As Worksheet
    Set ws1 = Nothing

    ' Find Tab 1 ("1-Configuration")
    For Each ws1 In ThisWorkbook.Worksheets
        If InStr(ws1.Name, "Configuration") > 0 Or ws1.Name = "1-Configuration" Then
            Exit For
        End If
    Next ws1

    If Not ws1 Is Nothing Then
        ' Remove any existing pictures in Tab 1 to avoid duplicates
        Dim pic As Picture
        For Each pic In ws1.Pictures
            pic.Delete
        Next pic

        ' Insert logo - Relative path (portable across folders)
        Dim logoPath As String
        logoPath = ThisWorkbook.Path & "\scripts\dev_tools\logo.png"

        If Dir(logoPath) <> "" Then
            ' Set row heights
            ws1.Rows(1).RowHeight = 15  ' Row 1 default height
            ws1.Rows(2).RowHeight = 60  ' Row 2 for logo (merged A2:J2)
            ws1.Rows(3).RowHeight = 15  ' Row 3 default height

            ' Merge cells A2:J2 for logo placement
            On Error Resume Next
            ws1.Range("A2:J2").UnMerge  ' Unmerge first in case already merged
            ws1.Range("A2:J2").Merge
            On Error GoTo 0

            ' Insert picture in merged range A2:J2 (centered)
            Set pic = ws1.Pictures.Insert(logoPath)
            With pic
                ' Get the merged range dimensions
                Dim mergedRange As Range
                Set mergedRange = ws1.Range("A2:J2")

                Dim mergedWidth As Double
                Dim mergedHeight As Double
                mergedWidth = mergedRange.Width
                mergedHeight = mergedRange.Height

                ' Lock aspect ratio first to calculate proper dimensions
                .ShapeRange.LockAspectRatio = msoTrue

                ' Set height to match row height with padding, width will adjust proportionally
                Dim padding As Double
                padding = 5  ' Points padding

                .Height = mergedHeight - (padding * 2)
                ' Width automatically adjusts based on aspect ratio

                ' Center the image horizontally and vertically in the merged range
                .Top = mergedRange.Top + padding
                .Left = mergedRange.Left + (mergedWidth - .Width) / 2  ' Center horizontally

                ' Move and size with cells
                .Placement = xlMoveAndSize
            End With
        End If
    End If

    ' =====================================================================
    ' PART 1: Clean up Tab 1 Factor Status
    ' =====================================================================

    If Not ws1 Is Nothing Then
        Dim selectedStartRow As Long
        Dim bankStartRow As Long
        Dim bankEndRow As Long
        Dim activeCol As Long
        Dim codeCol As Long

        activeCol = 1  ' Column A
        codeCol = 5    ' Column E

        ' Find section boundaries
        Dim j As Long
        For j = 1 To 300
            If Not IsEmpty(ws1.Cells(j, activeCol)) Then
                If InStr(1, ws1.Cells(j, activeCol).Value, "SELECTED FACTORS", vbTextCompare) > 0 Then
                    selectedStartRow = j + 2
                ElseIf InStr(1, ws1.Cells(j, activeCol).Value, "FACTOR BANK", vbTextCompare) > 0 Then
                    bankStartRow = j + 2
                End If
            End If
        Next j

        bankEndRow = ws1.Cells(ws1.Rows.Count, codeCol).End(xlUp).Row

        ' Set all Factor Bank entries to NO
        Dim bankRow As Long
        For bankRow = bankStartRow To bankEndRow
            If ws1.Cells(bankRow, codeCol).Value <> "" And ws1.Cells(bankRow, codeCol).Value <> "Code" Then
                Dim cellValue As String
                cellValue = UCase(Trim(CStr(ws1.Cells(bankRow, activeCol).Value)))
                If cellValue = "YES" Or cellValue = "TRUE" Then
                    ws1.Cells(bankRow, activeCol).Value = "NO"
                End If
            End If
        Next bankRow

        ' Set all Selected Factors entries to YES
        Dim selectedRow As Long
        For selectedRow = selectedStartRow To selectedStartRow + 100
            If ws1.Cells(selectedRow, codeCol).Value = "" Then Exit For

            Dim selValue As String
            selValue = UCase(Trim(CStr(ws1.Cells(selectedRow, activeCol).Value)))
            If selValue = "NO" Or selValue = "FALSE" Or selValue = "" Then
                ws1.Cells(selectedRow, activeCol).Value = "YES"
            End If
        Next selectedRow
    End If

    ' =====================================================================
    ' PART 2: Auto-Sort Tab 4
    ' =====================================================================

    ' Find Tab 4 ("4-Security Scanner")
    Dim ws As Worksheet
    Dim foundSheet As Boolean
    foundSheet = False

    For Each ws In ThisWorkbook.Worksheets
        If InStr(ws.Name, "Scanner") > 0 Or ws.Name = "4-Security Scanner" Then
            foundSheet = True
            Exit For
        End If
    Next ws

    If Not foundSheet Then
        Application.ScreenUpdating = True
        Exit Sub
    End If

    ' Find header rows
    Dim headerRow1 As Long
    Dim i As Long
    headerRow1 = 0
    For i = 1 To 50
        If ws.Cells(i, 1).Value = "Ticker" Then
            headerRow1 = i
            Exit For
        End If
    Next i

    If headerRow1 = 0 Then
        Application.ScreenUpdating = True
        Exit Sub
    End If

    Dim headerRow2 As Long, dataStartRow As Long, dataEndRow As Long
    Dim compositeCol As Long, lastDataCol As Long

    headerRow2 = headerRow1 + 1
    dataStartRow = headerRow2 + 1
    compositeCol = 4  ' Column D - Composite score

    ' Find last row with data
    dataEndRow = ws.Cells(ws.Rows.Count, 1).End(xlUp).Row  ' Column A = Ticker

    If dataEndRow < dataStartRow Then
        Application.ScreenUpdating = True
        Exit Sub
    End If

    ' Find last data column
    lastDataCol = ws.Cells(headerRow2, ws.Columns.Count).End(xlToLeft).Column

    ' Sort by Composite Score (descending)
    ws.Sort.SortFields.Clear
    ws.Sort.SortFields.Add2 _
        key:=ws.Range(ws.Cells(dataStartRow, compositeCol), ws.Cells(dataEndRow, compositeCol)), _
        SortOn:=xlSortOnValues, _
        Order:=xlDescending, _
        DataOption:=xlSortNormal

    With ws.Sort
        .SetRange ws.Range(ws.Cells(dataStartRow, 1), ws.Cells(dataEndRow, lastDataCol))
        .Header = xlNo
        .MatchCase = False
        .Orientation = xlTopToBottom
        .SortMethod = xlPinYin
        .Apply
    End With

    ' Update rank column (1, 2, 3...)
    For i = 0 To (dataEndRow - dataStartRow)
        ws.Cells(dataStartRow + i, 3).Value = i + 1  ' Column C = Rank
    Next i

    Application.ScreenUpdating = True

End Sub



```

### Module: `Sheet4.cls`

- **Stream:** `VBA/Sheet4`
- **File:** `xl/vbaProject.bin`

```vb
Attribute VB_Name = "Sheet4"
Attribute VB_Base = "0{00020820-0000-0000-C000-000000000046}"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = True
Attribute VB_TemplateDerived = False
Attribute VB_Customizable = True
'========================================
' Tab 4 (4-Security Scanner) - COMBINED VBA
'========================================
' HIERARCHICAL ORGANIZATION (Bottom to Top - Operational Order):
'
' USER-FACING MACROS (ordered by execution sequence):
'   1. Tab4_01_ApplyAlternatingRows         - Base layer: Alternating white/gray rows
'   2. Tab4_02_RefreshAllFormatting         - Master: Calls all in correct order
'
' AUTOMATIC EVENT HANDLERS (run automatically):
'   - Worksheet_Calculate                   - Auto-sort when weights change
'   - Worksheet_Activate                    - Refresh formatting when activated
'
'========================================

Option Explicit

'========================================
' PART 1: USER-FACING MACROS (Operational Order: Bottom to Top)
'========================================

Sub Tab4_01_ApplyAlternatingRows()
    '=====================================================================
    ' STEP 1 (Base Layer): Apply alternating white/gray rows to data columns
    '
    ' Columns with ALTERNATING ROWS (base layer):
    '   A: Ticker
    '   B: Name
    '   C: Rank
    '   D: Composite (NO FILL - has conditional formatting)
    '   E: Mkt Val
    '   F: Country
    '   G: Industry Group
    '   H+: Factor columns (Score columns have conditional formatting, Value columns get fills)
    '
    ' Pattern: Even rows (0,2,4...) = White, Odd rows (1,3,5...) = Light Gray
    '=====================================================================
    Dim ws As Worksheet
    Dim dataStart As Long
    Dim dataEnd As Long
    Dim i As Long
    Dim rowIdx As Long
    Dim col As Long
    Dim cell As Range
    Dim numFactors As Long

    ' Reference to Tab 4
    Set ws = ThisWorkbook.Sheets("4-Security Scanner")

    ' Find data start (look for "Ticker" in column A, data starts 2 rows below)
    dataStart = 0
    For i = 1 To 50
        If ws.Cells(i, 1).Value = "Ticker" Then
            dataStart = i + 2  ' Skip header row and Filter row
            Exit For
        End If
    Next i

    If dataStart = 0 Then
        MsgBox "Error: Could not find data start row", vbCritical
        Exit Sub
    End If

    ' Find last row with data (Ticker column A)
    dataEnd = dataStart
    For i = dataStart To 2000
        If ws.Cells(i, 1).Value = "" Then
            dataEnd = i - 1
            Exit For
        End If
    Next i

    ' Count number of factors (look at weight table starting at row 7)
    numFactors = 0
    For i = 7 To 50
        If ws.Cells(i, 1).Value = "TOTAL" Then
            Exit For
        End If
        If ws.Cells(i, 2).Value <> "" Then
            numFactors = numFactors + 1
        End If
    Next i

    ' Define colors
    Const COLOR_WHITE As Long = 16777215        ' RGB(255, 255, 255)
    Const COLOR_LIGHT_GRAY As Long = 15921906   ' RGB(242, 242, 242)

    ' Apply alternating rows
    For rowIdx = 0 To (dataEnd - dataStart)
        i = dataStart + rowIdx

        ' Determine alternating color (even rows = white, odd rows = gray)
        Dim rowColor As Long
        If rowIdx Mod 2 = 0 Then
            rowColor = COLOR_WHITE
        Else
            rowColor = COLOR_LIGHT_GRAY
        End If

        ' Column A: Ticker
        ws.Cells(i, 1).Interior.Color = rowColor

        ' Column B: Name
        ws.Cells(i, 2).Interior.Color = rowColor

        ' Column C: Rank
        ws.Cells(i, 3).Interior.Color = rowColor

        ' Column D: Composite - DO NOT FILL (has conditional formatting)
        ' Leave as-is

        ' Column E: Mkt Val
        ws.Cells(i, 5).Interior.Color = rowColor

        ' Column F: Country
        ws.Cells(i, 6).Interior.Color = rowColor

        ' Column G: Industry Group
        ws.Cells(i, 7).Interior.Color = rowColor

        ' Factor columns start at H (column 8)
        ' Pattern: Score (H), Value (I), Score (J), Value (K), etc.
        ' Only apply fills to VALUE columns (odd positions: I, K, M, O, etc.)
        Dim factorCol As Long
        Dim factorIdx As Long
        For factorIdx = 0 To numFactors - 1
            ' Score column (H, J, L, N, etc.) - DO NOT FILL (has conditional formatting)
            ' Value column (I, K, M, O, etc.) - APPLY FILL
            factorCol = 8 + (factorIdx * 2)  ' Score column
            ' Skip Score column, fill Value column
            ws.Cells(i, factorCol + 1).Interior.Color = rowColor
        Next factorIdx
    Next rowIdx

End Sub

Sub Tab4_02_RefreshAllFormatting()
    '=====================================================================
    ' STEP 2 (Master Function): Refresh ALL Tab 4 formatting in correct order
    ' Call this after any data changes, sorting, or manual edits
    '=====================================================================
    Call Tab4_01_ApplyAlternatingRows
End Sub

'========================================
' PART 2: AUTOMATIC EVENT HANDLERS
'========================================

Private Sub Worksheet_Calculate()
    '=====================================================================
    ' Auto-Rerank v2.5 - Automatically sorts Tab 4 when weights change
    '=====================================================================
    ' WHAT IT DOES:
    ' - Detects when composite scores recalculate (due to weight changes)
    ' - Automatically sorts securities by composite score (descending)
    ' - Maintains rank numbers 1, 2, 3...
    ' - Refreshes alternating row formatting after sort
    '
    ' Column structure:
    ' - Ticker (A), Name (B), Rank (C), Composite (D), Mkt Val (E), Country (F), Industry Group (G)
    ' - Composite column is D (sorts descending)
    ' - Rank column is C (auto-updated after sort)
    ' - Factor columns start at column H (8)
    '=====================================================================

    On Error Resume Next

    ' Only run if this is the active sheet
    If ActiveSheet.Name <> Me.Name Then Exit Sub

    ' Prevent recursive calculation triggers
    Application.EnableEvents = False
    Application.ScreenUpdating = False

    Dim ws As Worksheet
    Set ws = Me

    Dim i As Long  ' Loop counter variable

    ' Find header row (look for "Ticker" in column A)
    Dim headerRow1 As Long
    headerRow1 = 0
    For i = 1 To 50
        If ws.Cells(i, 1).Value = "Ticker" Then
            headerRow1 = i
            Exit For
        End If
    Next i

    If headerRow1 = 0 Then
        Application.EnableEvents = True
        Application.ScreenUpdating = True
        Exit Sub
    End If

    Dim headerRow2 As Long
    Dim dataStartRow As Long
    Dim compositeCol As Long

    headerRow2 = headerRow1 + 1
    dataStartRow = headerRow2 + 1
    compositeCol = 4  ' Column D

    ' Find last row with data (Column A = Ticker)
    Dim dataEndRow As Long
    dataEndRow = ws.Cells(ws.Rows.Count, 1).End(xlUp).Row

    ' Verify we have data to sort
    If dataEndRow < dataStartRow Then
        Application.EnableEvents = True
        Application.ScreenUpdating = True
        Exit Sub
    End If

    ' Find last data column
    Dim lastDataCol As Long
    lastDataCol = ws.Cells(headerRow2, ws.Columns.Count).End(xlToLeft).Column

    ' Sort by Composite Score (descending)
    ws.Sort.SortFields.Clear
    ws.Sort.SortFields.Add2 _
        key:=ws.Range(ws.Cells(dataStartRow, compositeCol), ws.Cells(dataEndRow, compositeCol)), _
        SortOn:=xlSortOnValues, _
        Order:=xlDescending, _
        DataOption:=xlSortNormal

    With ws.Sort
        .SetRange ws.Range(ws.Cells(dataStartRow, 1), ws.Cells(dataEndRow, lastDataCol))
        .Header = xlNo
        .MatchCase = False
        .Orientation = xlTopToBottom
        .SortMethod = xlPinYin
        .Apply
    End With

    ' Update rank column (1, 2, 3...)
    Dim rankCol As Long
    rankCol = 3  ' Column C
    For i = 0 To (dataEndRow - dataStartRow)
        ws.Cells(dataStartRow + i, rankCol).Value = i + 1
    Next i

    ' Refresh alternating rows after sort
    Call Tab4_01_ApplyAlternatingRows

    Application.EnableEvents = True
    Application.ScreenUpdating = True

End Sub

Private Sub Worksheet_Activate()
    '=====================================================================
    ' Refresh formatting when sheet is activated
    '=====================================================================
    On Error Resume Next
    Call Tab4_02_RefreshAllFormatting
End Sub

'========================================
' NOTES:
' - Alternating rows are independent of Tab 2 data
' - Conditional formatting on columns D (Composite) and H/J/L/N (Factor Scores) is preserved
' - Pattern matches Tab 1 exactly: even=white, odd=gray
' - Auto-sorts when weights change (via Worksheet_Calculate)
' - Auto-refreshes formatting after sort
' - Use Tab4_02_RefreshAllFormatting as the main entry point for manual refresh
'========================================


```

### Module: `Sheet2.cls`

- **Stream:** `VBA/Sheet2`
- **File:** `xl/vbaProject.bin`

```vb
Attribute VB_Name = "Sheet2"
Attribute VB_Base = "0{00020820-0000-0000-C000-000000000046}"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = True
Attribute VB_TemplateDerived = False
Attribute VB_Customizable = True
Private Sub Worksheet_Calculate()
      '=====================================================================
      ' Auto-Sort Tab 3 - Alphabetically by Company Name
      '=====================================================================
      ' This code goes in the Sheet3 code window (Tab 3: "3-Data (Complete)")
      '
      ' WHAT IT DOES:
      ' - Automatically sorts all securities alphabetically by Company Name
      ' - Maintains all data integrity across all columns
      ' - Preserves header structure (rows 1-6)
      '
      ' STRUCTURE:
      ' - Rows 1-5: Title/headers
      ' - Row 6: FILTER row
      ' - Row 7+: Data rows
      ' - Column B: Company Name (sort key)
      '=====================================================================

      On Error Resume Next

      ' Only run if this is the active sheet
      If ActiveSheet.Name <> Me.Name Then Exit Sub

      ' Prevent recursive calculation triggers
      Application.EnableEvents = False
      Application.ScreenUpdating = False

      Dim ws As Worksheet
      Set ws = Me

      ' CONFIGURATION
      Dim headerRow As Long
      Dim dataStartRow As Long
      Dim companyNameCol As Long

      ' Tab 3 structure:
      ' Row 5: Headers (Ticker, Company Name, Mkt Val, etc.)
      ' Row 6: FILTER row
      ' Row 7+: Data
      headerRow = 5
      dataStartRow = 7
      companyNameCol = 2  ' Column B = Company Name

      ' Find last row with data (check Ticker column)
      Dim dataEndRow As Long
      dataEndRow = ws.Cells(ws.Rows.Count, 1).End(xlUp).Row  ' Column A = Ticker

      ' Verify we have data to sort
      If dataEndRow < dataStartRow Then
          Application.EnableEvents = True
          Application.ScreenUpdating = True
          Exit Sub
      End If

      ' Find last data column
      Dim lastDataCol As Long
      lastDataCol = ws.Cells(headerRow, ws.Columns.Count).End(xlToLeft).Column

      ' Sort by Company Name (ascending/alphabetical)
      ws.Sort.SortFields.Clear
      ws.Sort.SortFields.Add _
          key:=ws.Range(ws.Cells(dataStartRow, companyNameCol), ws.Cells(dataEndRow, companyNameCol)), _
          SortOn:=xlSortOnValues, _
          Order:=xlAscending, _
          DataOption:=xlSortNormal

      With ws.Sort
          .SetRange ws.Range(ws.Cells(dataStartRow, 1), ws.Cells(dataEndRow, lastDataCol))
          .Header = xlNo
          .MatchCase = False
          .Orientation = xlTopToBottom
          .SortMethod = xlPinYin
          .Apply
      End With

      Application.EnableEvents = True
      Application.ScreenUpdating = True

  End Sub


```

### Module: `Sheet3.cls`

- **Stream:** `VBA/Sheet3`
- **File:** `xl/vbaProject.bin`

```vb
Attribute VB_Name = "Sheet3"
Attribute VB_Base = "0{00020820-0000-0000-C000-000000000046}"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = True
Attribute VB_TemplateDerived = False
Attribute VB_Customizable = True
'========================================
' Tab 3 (3-Factor Data) - COMBINED VBA
'========================================
' HIERARCHICAL ORGANIZATION (Bottom to Top - Operational Order):
'
' USER-FACING MACROS (ordered by execution sequence):
'   1. Tab3_01_ApplyAlternatingRows                - Base layer: Alternating white/gray rows
'   2. Tab3_02_ReapplySystematicEquityHighlighting - Top layer: Green highlighting for Systematic Equity (Column F)
'   3. Tab3_03_ApplySystematicFactorsFormatting    - Top layer: Red "No" formatting (Column N)
'   4. Tab3_04_RefreshAllFormatting                - Master: Calls all in correct order
'
'========================================

Option Explicit

'========================================
' PART 1: USER-FACING MACROS (Operational Order: Bottom to Top)
'========================================

Sub Tab3_01_ApplyAlternatingRows()
    '=====================================================================
    ' STEP 1 (Base Layer): Apply alternating white/gray rows to columns A-F
    ' Column F will have green highlighting applied on top by next step
    '=====================================================================
    Dim ws As Worksheet
    Dim dataStart As Long
    Dim dataEnd As Long
    Dim i As Long
    Dim rowIdx As Long
    Dim col As Long
    Dim cell As Range
    Dim isGreenRow As Boolean

    ' Reference to Tab 3
    Set ws = ThisWorkbook.Sheets("3-Factor Data")

    ' Data starts at row 7 (after Filter row 6)
    dataStart = 7

    ' Find last row with data (Factor Code column C)
    dataEnd = dataStart
    For i = dataStart To 1000
        If ws.Cells(i, 3).Value = "" Then
            dataEnd = i - 1
            Exit For
        End If
    Next i

    ' Define colors
    Const COLOR_WHITE As Long = 16777215        ' RGB(255, 255, 255)
    Const COLOR_LIGHT_GRAY As Long = 15921906   ' RGB(242, 242, 242)
    Const COLOR_GREEN As Long = 13434828        ' RGB(200, 230, 201) - Light green

    ' Apply alternating rows to columns A-F
    For rowIdx = 0 To (dataEnd - dataStart)
        i = dataStart + rowIdx

        ' Check if this row has green highlighting (check column F for existing green)
        isGreenRow = (ws.Cells(i, 6).Interior.Color = COLOR_GREEN)

        ' Determine alternating color (even rows = white, odd rows = gray)
        Dim rowColor As Long
        If rowIdx Mod 2 = 0 Then
            rowColor = COLOR_WHITE
        Else
            rowColor = COLOR_LIGHT_GRAY
        End If

        ' Apply to columns A-F
        For col = 1 To 6
            Set cell = ws.Cells(i, col)

            ' Preserve green highlighting for column F
            If isGreenRow And col = 6 Then
                cell.Interior.Color = COLOR_GREEN
            Else
                ' Apply alternating color
                cell.Interior.Color = rowColor
            End If
        Next col
    Next rowIdx

End Sub

Sub Tab3_02_ReapplySystematicEquityHighlighting()
    '=====================================================================
    ' STEP 2 (Top Layer): Apply green highlighting to "Systematic Equity" rows
    ' Searches column F (Asset Class) and applies green to matching rows
    ' MUST run AFTER alternating rows to sit on top of base formatting
    '=====================================================================
    Dim ws As Worksheet
    Dim dataStart As Long
    Dim dataEnd As Long
    Dim i As Long
    Dim assetClass As String

    Set ws = ThisWorkbook.Sheets("3-Factor Data")

    ' Data starts at row 7
    dataStart = 7

    ' Find last row with data (Factor Code column C)
    dataEnd = dataStart
    For i = dataStart To 1000
        If ws.Cells(i, 3).Value = "" Then
            dataEnd = i - 1
            Exit For
        End If
    Next i

    ' Define colors
    Const COLOR_WHITE As Long = 16777215
    Const COLOR_LIGHT_GRAY As Long = 15921906
    Const COLOR_GREEN As Long = 13434828  ' RGB(200, 230, 201) - Light green

    ' First, clear all green highlighting (reset to alternating colors)
    For i = dataStart To dataEnd
        Dim rowIdx As Long
        rowIdx = i - dataStart

        Dim alternatingColor As Long
        If rowIdx Mod 2 = 0 Then
            alternatingColor = COLOR_WHITE
        Else
            alternatingColor = COLOR_LIGHT_GRAY
        End If

        ' Reset column F to alternating color
        ws.Cells(i, 6).Interior.Color = alternatingColor
    Next i

    ' Apply green highlighting to "Systematic Equity" rows
    For i = dataStart To dataEnd
        ' Get Asset Class value from column F (6)
        assetClass = Trim(UCase(CStr(ws.Cells(i, 6).Value)))

        If assetClass = "SYSTEMATIC EQUITY" Then
            ' Apply green to column F
            ws.Cells(i, 6).Interior.Color = COLOR_GREEN
        End If
    Next i

End Sub

Sub Tab3_03_ApplySystematicFactorsFormatting()
    '=====================================================================
    ' STEP 3: Apply "Systematic Factors" column formatting (Column N)
    ' - Applies red background + dark red text (regular weight) to "No" values
    ' - Matches "Inverse" formatting style from column D (Relationship)
    ' Excel default red: Background #FFC7CE, Text #9C0006, Regular (not bold)
    '=====================================================================
    Dim ws As Worksheet
    Dim dataStart As Long
    Dim dataEnd As Long
    Dim i As Long

    Set ws = ThisWorkbook.Sheets("3-Factor Data")

    ' Define Excel's default red conditional formatting colors (matches "Inverse" in column D)
    Const COLOR_RED_BG As Long = 13551615      ' RGB(255, 199, 206) = #FFC7CE
    Const COLOR_RED_TEXT As Long = 393372     ' RGB(156, 0, 6) = #9C0006
    Const COLOR_BLACK_TEXT As Long = 0         ' RGB(0, 0, 0) = Black

    ' Data starts at row 7 (after Filter row 6)
    dataStart = 7

    ' Find last row with data (Factor Code column A)
    dataEnd = dataStart
    For i = dataStart To 1000
        If ws.Cells(i, 1).Value = "" Then
            dataEnd = i - 1
            Exit For
        End If
    Next i

    ' Apply formatting to all data rows
    For i = dataStart To dataEnd
        Dim cellValue As String
        cellValue = Trim(UCase(CStr(ws.Cells(i, 14).Value)))  ' Column N = 14

        ' Apply formatting based on value (do not modify cell values)
        If cellValue = "NO" Then
            ws.Cells(i, 14).Interior.Color = COLOR_RED_BG
            ws.Cells(i, 14).Font.Color = COLOR_RED_TEXT
            ws.Cells(i, 14).Font.Bold = False  ' Regular weight, not bold
        ElseIf cellValue = "YES" Then
            ' Reset to default (alternating row color will be applied by other functions)
            ws.Cells(i, 14).Font.Color = COLOR_BLACK_TEXT
            ws.Cells(i, 14).Font.Bold = False
        End If
    Next i

End Sub

Sub Tab3_04_RefreshAllFormatting()
    '=====================================================================
    ' STEP 4 (Master Function): Refresh ALL Tab 3 formatting in correct order
    ' Call this after any data changes or sorting
    ' Executes all formatting steps in proper sequence
    '=====================================================================
    Call Tab3_01_ApplyAlternatingRows
    Call Tab3_02_ReapplySystematicEquityHighlighting
    Call Tab3_03_ApplySystematicFactorsFormatting
End Sub

'========================================
' PART 2: AUTOMATIC EVENT HANDLERS
'========================================

Private Sub Worksheet_Change(ByVal Target As Range)
    '=====================================================================
    ' Automatically refresh formatting when column F (Asset Class) changes
    '=====================================================================
    On Error GoTo ErrorHandler

    ' If column F changed, refresh formatting
    If Target.Column = 6 And Target.Cells.Count = 1 Then
        Application.EnableEvents = False
        Call Tab3_04_RefreshAllFormatting
        Application.EnableEvents = True
    End If

    Exit Sub

ErrorHandler:
    Application.EnableEvents = True
    MsgBox "Error " & Err.Number & ": " & Err.Description, vbCritical
End Sub

Private Sub Worksheet_Activate()
    '=====================================================================
    ' Refresh formatting when sheet is activated
    '=====================================================================
    On Error Resume Next
    Call Tab3_04_RefreshAllFormatting
End Sub


```
