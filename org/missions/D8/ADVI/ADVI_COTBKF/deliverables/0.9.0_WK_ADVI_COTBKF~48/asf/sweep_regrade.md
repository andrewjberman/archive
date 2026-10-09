# Commonwealth sweep re-grade (CB-s-1)

The chain valuation -> daily returns -> monthly grade, run twice on the same transactions, price stores and reported returns. BEFORE: the declared sweep list sweeps-v1-20261008, cash leg method_r25. AFTER: the declared sweep list sweeps-v1-20261008, cash leg method_r26.

## The declared sweep list, version sweeps-v1-20261008

| CUSIP | rule | source kind | source / designation (as delivered) | asset type | evidence |
|---|---|---|---|---|---|
| FDIC66606 | a | vendor_description | Bank Deposit Sweep Program | Cash | silver transactions Security_Description as delivered; 143,357 rows, types by/dvr/int/sl |
| FDIC66853 | a | vendor_description | Advisory Retirement Sweep Program | Cash | silver transactions Security_Description as delivered; 80,939 rows, types by/dvr/int/sl |

Cash but not a sweep: CFNCASH (Cash Credit (Debit) Balance)

Rule (b) candidate 316067107 (Fidelity Government Cash Reserves): **OFF** -- no custodian designation of a core position is citable from data already in the repo or readable by the chain.
  - searched: silver transactions fields (S3 opal-data-assets commonwealth/cottonwood/silver/transactions): Position_Type is CASH on 8,761 of its 8,768 rows but is also CASH on 1,408,059 of the table's 1,416,497 rows for every security (it is the account's cash/margin side, not a core designation); Asset_Type 'Cash Equivalent' is shared by every money-market fund; FundCode CTC1260 is one value; Transaction_Description and Transaction_Note describe the trade ('REDEEMED TO COVER A SETTLED OBLIGATION' is behavior, not a designation)
  - searched: silver positions fields: Position_Type CASH, Account_Status 0 -- no core flag
  - searched: repo: no custodian document or statement line naming it a core position (org/, docs/, data/ searched by CUSIP and by 'core position'); the CTO analysis and the CVO grade call it core on its behavior, which is the census, not a designation

## Rejected candidates (517), by class

- CD (385): certificate of deposit: a dated, rate-bearing security that matures and trades at a price, not a deposit sweep program; stays a priced holding
- MMF (23): money-market fund share: a fund priced by NAV and held as a security, not a bank deposit sweep; stays a priced holding
- CASHMGMT (2): government cash-management fund or service held at the custodian: the description names no bank deposit sweep, so it stays a priced holding until a stated source puts it on the list
- MERGER (52): an equity whose description carries corporate-action wording (cash merger, cash election, cash payout): the security is a stock, not a cash vehicle
- BANKISSUER (32): the issuer's name contains Bank (an equity, note, bond, ETN or fund of or about a bank): a security issued by or about a bank, not a deposit sweep program
- UITCASH (18): unit investment trust: 'Cash' in the name states how the trust distributes (monthly or semi-annual cash), not that the unit is cash
- INSURED (4): municipal trust or fund: 'Insured' states bond insurance on the portfolio, not FDIC deposit insurance
- FUNDNAME (1): equity ETF whose name contains Cash (Pacer U.S. Cash Cows 100): a stock fund, not a cash vehicle

| CUSIP | class | description |
|---|---|---|
| 06048WDB3 | BANKISSUER | Bank of America Corp 2.69000% 08/04/2017 |
| 060505104 | BANKISSUER | Bank of America Corp |
| 060505BD5 | BANKISSUER | Bank of America Corporation 4.75000% 08/15/2013 Global Sb Note  #us060505bd57 |
| 06050WGE9 | BANKISSUER | Bank of Amer Corp MTN 4.00000% 08/15/2034 |
| 06051GEH8 | BANKISSUER | Bank Amer Corp MTN 5.00000% 05/13/2021 |
| 06051GEU9 | BANKISSUER | Bank Amer Corp Sr Ntser L3.300% 01/11/23 B/E Dtd 01/11/13 |
| 06051GFH7 | BANKISSUER | Bank America Corp Fr 4.200% 08/26/2024 |
| 06053FAA7 | BANKISSUER | Bank Amer Corp Srfxd Rt Ser L4.100% 07/24/23 B/E Dtd 07/23/13 |
| 06055JDC0 | BANKISSUER | Bank Amer Corp Me/tra # Trust Unsec |
| 06375MXY6 | BANKISSUER | Bank Montreal 2 Year Autocallable Barrier Contingent Interest Note Linked To INTC 0.00000% 03/05/2026 |
| 063904106 | BANKISSUER | Bank of The Ozarks Com |
| 064058100 | BANKISSUER | Bank of New York Mellon Corp |
| 06406HBM0 | BANKISSUER | Bank of NY Mellon Corp 5. |
| 06417N103 | BANKISSUER | Bank Ozk |
| 06738C828 | BANKISSUER | Barclays Bank PLC ADR Pfd Ser 1 Bond Perpetual 6.27800% |
| 06738JLF9 | BANKISSUER | Barclays Bank PLC MTN 6.00000% 11/04/2025 |
| 06742E711 | BANKISSUER | Barclays Bank PLC iPath S&P 500 Vix Short-Term Futures ETN New 2013 1 For 4 R/s Into Barclays Bank PLC |
| 09661K106 | BANKISSUER | Bank of New York Mellon Emerging Markets Securities Cl A |
| 136069101 | BANKISSUER | Canadian Imperial Bank of Commerce |
| 16950T102 | BANKISSUER | China Merchants Bank Co Limited |
| 31771JLK4 | BANKISSUER | Financing Fed Bank Coupon Strip |
| 40415F101 | BANKISSUER | HDFC Bank Limited |
| 409905106 | BANKISSUER | John Hancock Regional Bank Fund Class A |
| 409905791 | BANKISSUER | John Hancock Regional Bank Fund Class I |
| 45104G104 | BANKISSUER | ICICI Bank Limited |
| 48121CVZ6 | BANKISSUER | JPMorgan Chase Bank Na Note 6.00000% 07/05/2017 Isin #us48121cvz66  #b231mp2 |
| 55261F104 | BANKISSUER | M&t Bank Corp |
| 684000102 | BANKISSUER | Opus Bank Irvine Califcom |
| 69349LAR9 | BANKISSUER | Pnc Bank Na Pittsburgh Pa Medium Term Sub Bk Nts 4.050% 07/26/18 |
| 780097713 | BANKISSUER | Royal Bank Scotland Gpplc Spon ADR Repstgser T Pfd Cpn-7.25%freq Qrtly Perp Mtycall@25 Any W/30 Dnotice Aftr 12/31/12 |
| 780097AM3 | BANKISSUER | Royal Bank Scotland Group PLC Note 4.70000% 07/03/2018 Isin #us780097am39  #3330748 |
| 78010XAD3 | BANKISSUER | Royal Bank Scotland 3.40 |
| 262006836 | CASHMGMT | Pershing Government Cash Management Service Shares |
| PER999676 | CASHMGMT | Bank of New York Pershing Govtcash Management |
| 005594BV7 | CD | Adams Community Bank Adams MA CD 4.30000% 07/02/2027 |
| 02004MB51 | CD | Ally Bank Midvale UT CD 2.45000% 07/30/2015 |
| 02006LS87 | CD | Ally Bank Midvale UT CD 1.45000% 12/10/2018 |
| 02007G3S0 | CD | Ally Bank Sandy UT CD 3.80000% 09/28/2026 |
| 02007G4L4 | CD | Ally Bank Sandy UT CD 4.35000% 02/28/2025 |
| 02007GCN1 | CD | Ally Bank Midvale UT CD 2.70000% 05/11/2020 |
| 02007GCY7 | CD | Ally Bank Midvale UT CD 2.75000% 05/29/2020 |
| 02007GHL0 | CD | Ally Bank Midvale UT CD 2.60000% 02/16/2021 |
| 02007GK69 | CD | Ally Bank Sandy UT CD 4.80000% 03/03/2025 |
| 02007GPU1 | CD | Ally Bank Sandy UT CD 1.40000% 04/21/2023 |
| 02007GQ89 | CD | Ally Bank Sandy UT CD 5.15000% 12/30/2024 |
| 02007GR88 | CD | Ally Bank Sandy UT CD 5.25000% 12/11/2023 |
| 02007GS53 | CD | Ally Bank Sandy UT CD 5.35000% 03/07/2024 |
| 02007GSC8 | CD | Ally Bank Sandy UT CD 2.40000% 12/04/2023 |
| 02007GT52 | CD | Ally Bank Sandy UT CD 5.10000% 03/01/2024 |
| 02007GXB4 | CD | Ally Bank Sandy UT CD 3.00000% 08/04/2023 |
| 02554BDW8 | CD | American Eagle Bank South Elgin CD 4.45000% 02/16/2024 |
| 02587DP28 | CD | American Express C/2.4 Institutional Certificate of Deposit U |
| 02589AAN2 | CD | American Express N/instl Certificate of Deposit Unsec |
| 02589AD66 | CD | American Expressnatl Bank Brokeredintl Certificate of Deposit Programinstl Ctf Dep2.850% 07/06/23 B/E Dtd 07/06/22 |
| 02589AEE8 | CD | American Express N/instl Certificate of Deposit Unsec |
| 029728CG5 | CD | American St Bank Sioux Ctr Ia CD 5.00000% 10/30/2025 |
| 029728CH3 | CD | American St Bank Sioux Ctr Ia CD 5.10000% 04/30/2025 |
| 033537BC4 | CD | Anderson Bros Bank Mullins SC CD 5.10000% 06/09/2025 |
| 033537BE0 | CD | Anderson Bros Bank Mullins SC CD 4.75000% 03/09/2026 |
| 034441AA3 | CD | Andrew Johnson Bank Greeneville CD 5.40000% 06/28/2024 |
| 03727QAB4 | CD | Antwerp Exchange Bank Co OH CD 5.05000% 03/21/2025 |
| 04225AAE8 | CD | Armor Bank Forrest City Ark CD 5.40000% 09/27/2024 |
| 045491TX5 | CD | Associated Bank National Assn Green CD 4.30000% 09/11/2025 |
| 05580A2D5 | CD | Bmw Bank North Amer UT CD 5.00000% 07/10/2023 |
| 05580AMR2 | CD | Bmw Bank North Amer UT CD 2.95000% 05/11/2022 |
| 05580AMZ4 | CD | Bmw Bank North Amer Salt Lake CD 2.75000% 06/15/2020 |
| 05580AN34 | CD | Bmw Bank North Amer UT CD 2.00000% 10/30/2023 |
| 05581W2G9 | CD | BMO Harris Bank National Assn Chicag CD 1.80000% 10/20/2020 |
| 05581WVR3 | CD | BMO Harris Bank National Assn Chicag CD 1.80000% 11/28/2018 |
| 05581WYR0 | CD | BMO Harris Bank National Assn Chicag CD 2.30000% 06/14/2019 |
| 05584CDY9 | CD | Bank of New York Mellon N A/2.2 Institutional Certificate of Deposit U |
| 05584CPQ3 | CD | Bank of New York Mellon N A/instl Certificate of Deposit Unsec |
| 05600XFT2 | CD | BMO Harris Bank National Assn Chicag CD 2.05000% 06/09/2023 |
| 05600XJM3 | CD | BMO Bank National Assn Chicago IL CD 4.15000% 10/30/2023 |
| 05600XJU5 | CD | BMO Bank National Assn Chicago IL CD 4.10000% 11/13/2023 |
| 05600XJW1 | CD | BMO Bank National Assn Chicago IL CD 4.30000% 10/15/2024 |
| 05600XQA1 | CD | BMO Bank National Assn Chicago IL CD 4.80000% 05/09/2025 |
| 05610LDT8 | CD | BMO Bank National Assn Chicago IL CD 5.40000% 11/12/2024 |
| 05610LEB6 | CD | BMO Bank National Assn Chicago IL CD 5.00000% 06/06/2025 |
| 05610LHM9 | CD | BMO Bank National Assn Chicago IL CD 5.25000% 09/23/2024 |
| 05610LHV9 | CD | BMO Bank National Assn Chicago IL CD 4.95000% 04/07/2025 |
| 05610LQK3 | CD | BMO Bank National Assn Chicago IL CD 4.30000% 08/29/2025 |
| 05612LBD3 | CD | Bmw Bank North Amer Salt Lake Ci CD 3.90000% 02/23/2027 |
| 05612LHJ4 | CD | Bmw Bank North Amer Salt Lake Ci CD 3.75000% 11/21/2029 |
| 05612LHS4 | CD | Bmw Bank North Amer Salt Lake Ci CD 3.70000% 01/03/2028 |
| 05612LHU9 | CD | Bmw Bank North Amer Salt Lake Ci CD 3.60000% 07/02/2027 |
| 06051V7W0 | CD | Bank of America Na CD 4.80000% 02/06/2025 |
| 06051VC20 | CD | Bank of America Na CD 2.65000% 08/24/2020 |
| 06051VE85 | CD | Bank Amer Na Charlotte NC CD 2.40000% 02/13/2020 |
| 06051VH90 | CD | Bank Amer Na Charlotte NC CD 2.00000% 04/03/2020 |
| 06051VK39 | CD | Bank Amer Na Charlotte NC CD 1.95000% 08/06/2020 |
| 06051VL95 | CD | Bank Amer Na Charlotte NC CD 1.80000% 09/24/2020 |
| 06051X3R1 | CD | Bank Of America Na Cd 3.75000% 02/25/2027 |
| 06051XDT6 | CD | Bank Of America Na Cd 5.00000% 05/22/2026 |
| 06051XDV1 | CD | Bank of America Na CD 5.15000% 11/24/2025 |
| 06051XDY5 | CD | Bank Of America Na Cd 5.00000% 06/01/2026 |
| 06051XEM0 | CD | Bank of America Na CD 5.20000% 12/15/2025 |
| 06051XER9 | CD | Bank Of America Na Cd 5.05000% 06/22/2026 |
| 06051XET5 | CD | Bank of America Na CD 5.20000% 12/22/2025 |
| 06051XEW8 | CD | Bank Of America Na Cd 5.00000% 06/29/2026 |
| 06051XQC9 | CD | Bank of America Na CD 4.25000% 02/20/2026 |
| 06051XR53 | CD | Bank of America, N.A. CD 3.70000% 11/25/2026 |
| 06051XWK4 | CD | Bank of America Na CD 4.30000% 12/04/2025 |
| 06051XXM9 | CD | Bank Of America Na Cd 4.30000% 06/18/2026 |
| 062163BX7 | CD | Bank Forward Hannaford N D CD 5.20000% 01/14/2025 |
| 06268LAB3 | CD | Bank Houston TX CD 3.00000% 08/04/2023 |
| 06418CBV7 | CD | Bank Ozk Little Rock Ark CD 4.35000% 01/05/2024 |
| 06418CDA1 | CD | Bank Ozk Little Rock Ark CD 4.50000% 02/14/2024 |
| 06418CJZ0 | CD | Bank Ozk Little Rock Ark CD 5.20000% 08/07/2024 |
| 06418CNF9 | CD | Bank Ozk Little Rock Ark CD 5.40000% 10/15/2024 |
| 06418CYX8 | CD | Bank Ozk Little Rock Ark CD 4.90000% 10/15/2024 |
| 06426KCE6 | CD | Bank New Eng Salem NH CD 4.20000% 04/08/2024 |
| 064577GS2 | CD | Bank Rhode Is Providence RI CD 4.25000% 03/09/2026 |
| 065284GL9 | CD | Bank TN Kingsport CD 4.55000% 08/10/2023 |
| 065680KZ2 | CD | Bank West San Francisco CA CD 1.05000% 02/13/2018 |
| 065680NK2 | CD | Bank West San Francisco CA CD 2.15000% 01/02/2019 |
| 065680NN6 | CD | Bank West San Francisco CA CD 2.35000% 07/05/2019 |
| 065680NT3 | CD | Bank West San Francisco CA CD 2.35000% 07/25/2019 |
| 065680NY2 | CD | Bank West San Francisco CA CD 2.30000% 08/08/2019 |
| 065680PD6 | CD | Bank West San Francisco CA CD 2.40000% 07/31/2019 |
| 06610RBY4 | CD | Bankers Bank Madison WI CD 4.00000% 12/29/2023 |
| 06654BHC8 | CD | Bankwell Bank New Canaan CT CD 4.20000% 06/05/2026 |
| 06740KAL1 | CD | Barclays Bank De/3.15 Retail Certificate of Deposit |
| 06740KNA1 | CD | Barclays Bank Delretail Certificate of Deposit 3a2program Book Entryinstl Ctf Dep2.700% 12/19/19 B/E Dtd 12/19/18 |
| 06740KRY5 | CD | Barclays Bank De/retail Certificate of Deposit Unse |
| 06740KSG3 | CD | Barclays Bank De/retail Certificate of Deposit Unse |
| 07279NAM0 | CD | Bayfirst National Bank St Petersburg CD 3.95000% 05/14/2026 |
| 07370T3A9 | CD | Beal Bank Plano TX CD 1.00000% 12/20/2017 |
| 07371A3A9 | CD | Beal Bank Plano TX CD 2.05000% 06/14/2023 |
| 07371BDV0 | CD | Beal Bank Plano TX CD 4.50000% 11/15/2023 |
| 07371BED9 | CD | Beal Bank Plano TX CD 4.60000% 11/22/2023 |
| 07371BGG0 | CD | Beal Bank Plano TX CD 4.40000% 01/03/2024 |
| 07371BGQ8 | CD | Beal Bank Plano TX CD 4.40000% 01/10/2024 |
| 07371BMZ1 | CD | Beal Bank Plano TX CD 5.15000% 11/01/2023 |
| 07371BNC1 | CD | Beal Bank Plano TX CD 5.20000% 12/27/2023 |
| 07371BRE3 | CD | Beal Bank Plano TX CD 5.30000% 04/17/2024 |
| 07371DQZ3 | CD | Beal Bank USA Las Vegas NV CD 4.65000% 02/14/2024 |
| 07371DUZ8 | CD | Beal Bank USA Las Vegas NV CD 5.20000% 08/21/2024 |
| 07815ACR6 | CD | Bell St Bank &tr Fargo N D CD 4.35000% 01/05/2024 |
| 080522AC9 | CD | Belmont Savings Bank SSB CD 4.45000% 11/24/2025 |
| 084601TU7 | CD | Berkshire Bank Pittsfield MA CD 2.25000% 04/15/2020 |
| 108622MX6 | CD | Bridgewater Bank St Louis Pk Min CD 4.35000% 03/20/2026 |
| 108622NM9 | CD | Bridgewater Bank Bloomington MN CD 4.85000% 04/26/2024 |
| 139805BG9 | CD | Capital Bank N A Rockville MD CD 5.30000% 01/23/2024 |
| 139805CS2 | CD | Capital Bank N A Rockville MD CD 3.90000% 05/26/2027 |
| 140420G53 | CD | Capital One Bank (usa) Natural CD 1.40000% 09/28/2020 |
| 140420R44 | CD | Capital One Bank Usanatl Assn Glen Allenva Certificate of Deposit Act/365semi-Annually1.600% 12/09/19 B/E Dtd 12/07/16 |
| 140420TD2 | CD | Capital One Bank USA National Assn 2.00000% 07/08/2019 CD |
| 149159PL3 | CD | Cathay Bank Los Angeles CA Certificate of Deposit 1.60000% 08/30/2021 |
| 150517GQ7 | CD | Cedar Rapids Bank &tr Co IA CD 5.25000% 05/20/2024 |
| 174118AM1 | CD | Citizens Bank New Haven MO CD 2.65000% 01/22/2021 |
| 17669MAW7 | CD | Citizens St Bank Cadott WI CD 5.05000% 08/28/2023 |
| 17669MBK2 | CD | Citizens St Bank Cadott WI CD 5.30000% 02/06/2024 |
| 17801DHY5 | CD | City National Bank FL Miami CD 5.25000% 10/30/2024 |
| 184554BK8 | CD | Clear Fork Bank National Assn Albany CD 4.15000% 03/27/2026 |
| 200339FL8 | CD | Comerica Bank Dallas TX CD 4.95000% 10/17/2024 |
| 2027507F6 | CD | Commonwealth Business Bank Los A CD 5.10000% 12/13/2024 |
| 2027507H2 | CD | Commonwealth Business Bank Los A CD 5.30000% 06/14/2024 |
| 20367GBK4 | CD | Community Comm Bank LA CA CD 4.50000% 06/24/2024 |
| 20376TAA8 | CD | Community National Bank Derby VT CD 1.95000% 01/31/2019 |
| 20415WAN6 | CD | Community West Bank Fresno CA CD 4.25000% 09/17/2025 |
| 20451PUL8 | CD | Compass Bank Birmingham AL CD 2.10000% 05/09/2019 |
| 20784PAN4 | CD | Connection Bank Ft Madison Ia CD 3.45000% 12/22/2023 |
| 20786AEH4 | CD | Connectone Bank Englewood CD 3.20000% 09/21/2023 |
| 21867GBC5 | CD | Core Bank Omaha NE CD 4.20000% 07/29/2025 |
| 220802AV4 | CD | Cortrust Bank Mitchell N A South CD 3.70000% 02/11/2028 |
| 22412VAB3 | CD | Craft Bank Atlanta GA CD 5.15000% 09/29/2023 |
| 22412VAF4 | CD | Craft Bank Atlanta GA CD 5.50000% 09/27/2024 |
| 227563CM3 | CD | Cross Riv Bank Teaneck NJ CD 5.25000% 12/07/2023 |
| 227563CW1 | CD | Cross Riv Bank Teaneck NJ CD 5.25000% 12/23/2024 |
| 227563JM6 | CD | Cross Riv Bank Teaneck NJ CD 4.90000% 09/16/2024 |
| 227563MS9 | CD | Cross Riv Bank Teaneck NJ CD 4.15000% 11/07/2025 |
| 22766AKH7 | CD | Crossfirst Bank Leawood KS CD 4.50000% 01/11/2024 |
| 23062KBV3 | CD | Cumberland Fed Bank Fsb WI CD 2.35000% 07/17/2019 |
| 23062KGH9 | CD | Cumberland Fed Bank Fsb WI CD 5.20000% 05/15/2024 |
| 23322GF77 | CD | Dmb Community Bank Deforest WI CD 4.80000% 10/10/2023 |
| 23322GL47 | CD | Dmb Community Bank Deforest WI CD 5.25000% 04/23/2024 |
| 23322GN94 | CD | Dmb Community Bank Deforest WI CD 5.05000% 08/16/2024 |
| 23322GZE0 | CD | Dmb Community Bank Deforest WI CD 3.20000% 12/08/2023 |
| 23322GZH3 | CD | Dmb Community Bank Deforest WI CD 3.30000% 09/15/2023 |
| 23427AAB0 | CD | Dakota Westn Bank Bowman N D CD 2.40000% 03/13/2020 |
| 251795CF5 | CD | Devon Bank Chicago IL CD 5.00000% 08/09/2023 |
| 254672V70 | CD | Discover Bank CD 1.25000% 06/14/2018 |
| 2546733H7 | CD | Discover Bank CD 5.00000% 09/27/2023 |
| 254673KM7 | CD | Discover Bank CD 1.75000% 01/10/2019 |
| 254673RA6 | CD | Discover Bank CD 2.75000% 07/06/2020 |
| 254673RC2 | CD | Discover Bank CD 3.15000% 07/05/2022 |
| 254673TG1 | CD | Discover Bank CD 2.75000% 09/08/2020 |
| 254676CS6 | CD | Discover Bank CD 4.75000% 11/12/2024 |
| 25660BBY8 | CD | Dogwood State Bank Raleigh NC CD 4.60000% 03/25/2025 |
| 27579TUD0 | CD | East West Bank Pasadena CA CD 3.40000% 06/23/2023 |
| 293404AB5 | CD | Trinity Cap Bank of TX CD 4.20000% 12/26/2025 |
| 29367SJY1 | CD | Enterprise Bank &tr Clayton MO CD 5.05000% 04/11/2024 |
| 296688BM5 | CD | Essex Bank Tappahannock VA CD 2.50000% 01/15/2020 |
| 300185MD4 | CD | Evergreen Bank Group IL CD 5.10000% 12/20/2024 |
| 301074GE4 | CD | Exchange Bank Gibbon NE CD 4.40000% 07/12/2024 |
| 301074HG8 | CD | Exchange Bank Gibbon NE CD 5.40000% 08/16/2024 |
| 30191KAF8 | CD | Fbt Bank &mtg Fordyce Ark CD 5.25000% 08/15/2024 |
| 30257JBT1 | CD | Fnb Bank Inc Romney West VA CD 4.15000% 01/30/2026 |
| 309175DV6 | CD | Farmers Bank Ault Colorado CD 5.20000% 09/23/2024 |
| 31033MBJ5 | CD | Farmers St Bank Calhan Colorado CD 4.55000% 11/28/2023 |
| 312629AA6 | CD | Fayette Savings Bank SSB LA CD 5.05000% 05/13/2024 |
| 316777XG1 | CD | Fifth Third Bank Cincinnati Stn CD 1.15000% 04/16/2021 |
| 316777XV8 | CD | Fifth Third Bank Cincinnati Stn CD 2.95000% 06/30/2023 |
| 316777ZC8 | CD | Fifth Third Bank Cincinnati Stn CD 4.75000% 01/22/2025 |
| 319042GK7 | CD | Htlf Bank Denver Co CD 5.05000% 11/08/2023 |
| 319042GL5 | CD | Htlf Bank Denver Co CD 4.90000% 11/08/2024 |
| 31925YBU5 | CD | First Bank of The Lake CD 4.00000% 04/30/2026 |
| 31925YDG4 | CD | First Bank Of The Lake Cd 3.95000% 02/12/2027 |
| 31944ABU4 | CD | First Cap Bank Laurinburg NC CD 3.70000% 10/20/2023 |
| 31944MCU7 | CD | First Carolina Bank Rocky Mt CD 5.25000% 07/15/2024 |
| 31986HAK1 | CD | First Comm Bank Lewisburg TN CD 3.65000% 08/17/2027 |
| 31987FBN7 | CD | First Community Bank TN Shelbyvill CD 5.25000% 09/20/2024 |
| 31987FCJ5 | CD | First Community Bank TN Shelbyvill CD 4.25000% 03/12/2026 |
| 31987FCP1 | CD | First Community Bank TN Shelbyvill CD 4.15000% 05/05/2026 |
| 32018CAK2 | CD | First Fed Savings Bank Roch CD 5.20000% 03/22/2024 |
| 32021SKB1 | CD | First Financial Bank CD 4.70000% 02/07/2024 |
| 32021SKP0 | CD | First Financial Bank CD 4.75000% 01/23/2025 |
| 32022RZR1 | CD | First Financial Bank USA Dakota Du S CD 4.15000% 12/24/2026 |
| 32026UYW0 | CD | First Foundation Bank Irvine CA CD 4.75000% 05/21/2024 |
| 32050JCH1 | CD | First Heritage Bank Centralia Ka CD 5.00000% 12/06/2024 |
| 321082AB5 | CD | First National Bank Okawville IL CD 2.00000% 02/28/2019 |
| 32110YH99 | CD | First National Bank Amer East Lans CD 4.90000% 11/23/2026 |
| 332135LB6 | CD | First National Bank Omaha NE CD 5.15000% 05/29/2024 |
| 335857EJ3 | CD | First OK Bank Jenks OK CD 3.95000% 09/19/2029 |
| 336460DG2 | CD | First St Bank Dequeen Ark CD 2.10000% 08/31/2023 |
| 33648GCE1 | CD | First St Bank Farnam NE CD 4.60000% 06/05/2023 |
| 33648RBC2 | CD | First St Bank Buxton Nd CD 4.90000% 04/15/2025 |
| 33649EAP2 | CD | First St Bank Russellville Ark CD 4.50000% 07/19/2024 |
| 33732TCB6 | CD | 1st Trust Bank Inc Hazard KY CD 4.20000% 08/05/2025 |
| 337630CA3 | CD | Firstrust Savings Bank PA CD 5.05000% 09/29/2023 |
| 33847GHX3 | CD | Flagstar Bank National Assn Hicksvi CD 5.35000% 07/14/2025 |
| 33847GJH6 | CD | Flagstar Bank National Associa CD 5.20000% 01/27/2026 |
| 33847GLB6 | CD | Flagstar Bank National Associa CD 4.35000% 11/19/2025 |
| 34387AFT1 | CD | Flushing Bank NY CD 4.85000% 05/01/2023 |
| 351593AJ7 | CD | Fox VY Savings Bank Fond Du Lac CD 4.55000% 01/25/2024 |
| 35907XEW3 | CD | Frontier Bank Madison NE CD 3.35000% 09/16/2025 |
| 38143ABN4 | CD | Goldman Sachs Bank USA NY CD 2.05000% 11/16/2016 |
| 38147JUT7 | CD | Goldman Sachs Bank USA NY CD 1.90000% 03/05/2019 |
| 38148JXP1 | CD | Goldman Sachs Bank USA CD 2.55000% 07/08/2021 |
| 38148JXX4 | CD | Goldman Sachs Bank USA NY CD 1.15000% 07/10/2017 |
| 38148P4Z7 | CD | Goldman Sachs Bank USA CD 2.85000% 02/14/2022 |
| 38148PJ73 | CD | Goldman Sachs Bank USA CD 2.90000% 05/10/2021 |
| 38148PN29 | CD | Goldman Sachs Bank USA CD 3.00000% 06/01/2021 |
| 38148PYP6 | CD | Goldman Sachs Bank USA NY CD 2.10000% 08/28/2019 |
| 38149M5S8 | CD | Goldman Sachs Bank USA CD 1.90000% 10/27/2023 |
| 38149M6E8 | CD | Goldman Sachs Bank USA CD 1.65000% 05/04/2023 |
| 38149MAP8 | CD | Goldman Sachs Bank USA CD 2.45000% 05/28/2021 |
| 38149MBA0 | CD | Goldman Sachs Bank Usanew York Ctf Dep2.450% 06/07/21 B/E Dtd 06/05/19 |
| 38150V5J4 | CD | Goldman Sachs Bank USA CD 3.85000% 09/02/2026 |
| 38150V5M7 | CD | Goldman Sachs Bank USA CD 3.80000% 09/02/2027 |
| 38150V6Q7 | CD | Goldman Sachs Bank USA CD 3.70000% 09/23/2026 |
| 38150VAX7 | CD | Goldman Sachs Bank USA CD 2.05000% 05/25/2023 |
| 38150VBB4 | CD | Goldman Sachs Bank USA CD 2.10000% 06/01/2023 |
| 38150VBU2 | CD | Goldman Sachs Bank USA CD 2.10000% 06/08/2023 |
| 38150VFE4 | CD | Goldman Sachs Bank USA CD 5.00000% 09/29/2023 |
| 38150VHG7 | CD | Goldman Sachs Bank USA CD 5.00000% 05/14/2024 |
| 38150VND7 | CD | Goldman Sachs Bank USA CD 5.45000% 10/09/2024 |
| 38150VNJ4 | CD | Goldman Sachs Bank USA CD 5.40000% 01/17/2024 |
| 38150VPE3 | CD | Goldman Sachs Bank USA CD 5.45000% 11/05/2024 |
| 38150VPY9 | CD | Goldman Sachs Bank USA CD 5.20000% 12/03/2024 |
| 38150VQH5 | CD | Goldman Sachs Bank USA CD 5.10000% 12/11/2024 |
| 38150VQN2 | CD | Goldman Sachs Bank USA CD 5.10000% 12/17/2024 |
| 38150VTF6 | CD | Goldman Sachs Bank USA CD 5.20000% 07/30/2024 |
| 38150VTV1 | CD | Goldman Sachs Bank USA CD 5.25000% 11/14/2024 |
| 38150VUY3 | CD | Goldman Sachs Bank USA CD 5.30000% 06/11/2025 |
| 38150VUZ0 | CD | Goldman Sachs Bank USA CD 5.05000% 06/11/2026 |
| 38150VV55 | CD | Goldman Sachs Bank USA CD 3.75000% 04/15/2026 |
| 38150VXD6 | CD | Goldman Sachs Bank USA CD 4.55000% 02/27/2025 |
| 38151PCW9 | CD | Goldman Sachs Bank USA CD 3.70000% 11/26/2027 |
| 38151PET4 | CD | Goldman Sachs Bank USA CD 3.60000% 06/30/2027 |
| 38151PFA4 | CD | Goldman Sachs Bank USA CD 3.70000% 01/06/2028 |
| 38151PLX7 | CD | Goldman Sachs Bank USA CD 3.95000% 04/17/2028 |
| 381573AL8 | CD | Goldwater Bank N A CD 5.10000% 08/09/2023 |
| 381573AQ7 | CD | Goldwater Bank N A CD 5.05000% 04/25/2025 |
| 40963QAK9 | CD | Keb Hana Bank of New York Agency CD 4.80000% 12/27/2024 |
| 429882FY4 | CD | Highland Bank St Michael MN CD 4.65000% 02/09/2024 |
| 434207AA4 | CD | Hodge Bank &tr Co LA CD 3.50000% 09/30/2027 |
| 44914ABQ2 | CD | Hyperion Bank Philadelphia PA CD 4.90000% 06/27/2025 |
| 45340KGH6 | CD | Independence Bank KY CD 5.25000% 01/22/2024 |
| 45340KGZ6 | CD | Independence Bank KY CD 5.00000% 09/13/2024 |
| 46091MAE4 | CD | Investar Bank National Assn Baton Ro CD 5.00000% 03/08/2024 |
| 46657VTB6 | CD | JPMorgan Chase Bank N A CD 4.50000% 12/31/2027 |
| 46659CHT0 | CD | JPMorgan Chase Bank N A CD 4.00000% 09/30/2030 |
| 48123YPB6 | CD | JPMorgan Chase Bank Na 0.00000% 09/26/2016 CD Flt |
| 48128FCD2 | CD | JPMorgan Chase Bank CD 3.25000% 05/31/2023 |
| 490846AH5 | CD | Kentland Bank IN CD 3.60000% 07/30/2027 |
| 49306SRF5 | CD | Key Bank National Assn OH 0.45000% 02/27/2015 CD |
| 52470QCE2 | CD | Legacy Bank &tr Co Rogersville CD 4.05000% 10/15/2024 |
| 531045AJ1 | CD | Liberty National Bank In Paris TX CD 5.20000% 11/12/2024 |
| 53957NAA9 | CD | Locality Bank Ft Lauderdale FL CD 5.50000% 03/28/2024 |
| 53957NAE1 | CD | Locality Bank Ft Lauderdale FL CD 5.40000% 10/28/2024 |
| 54066QAF7 | CD | Logan County Bank Scranton Ark CD 4.05000% 10/05/2023 |
| 54889MAD6 | CD | Loyal Trust Bank Johns Creek GA CD 5.00000% 03/26/2025 |
| 554479EG6 | CD | Machias Savings Bank ME CD 4.10000% 02/09/2026 |
| 554479EJ0 | CD | Machias Savings Bank ME CD 4.60000% 02/09/2024 |
| 554479FC4 | CD | Machias Savings Bank ME CD 4.20000% 11/02/2028 |
| 559582AV3 | CD | Magnolia Bank Inc KY CD 5.50000% 07/18/2024 |
| 56065GBV9 | CD | Mainstreet Bank Fairfax VA CD 4.20000% 12/19/2025 |
| 57116ATT5 | CD | Marlin Business Bank Salt Lake CD 1.60000% 08/26/2021 |
| 58321JCG1 | CD | Meadows Bank Las Vegas NV CD 1.80000% 08/28/2020 |
| 58321JDP0 | CD | Meadows Bank Las Vegas NV CD 5.40000% 03/18/2024 |
| 59013KWN2 | CD | Merrick Bank South Jordan UT CD 5.30000% 08/30/2024 |
| 60425SKR9 | CD | Minnwest Bank Redwood Falls MN CD 5.20000% 01/05/2026 |
| 61768E3Z4 | CD | Morgan Stanley Private Bank National CD 4.90000% 05/24/2027 |
| 624786CR8 | CD | Mufg Union Bank Na San Fran CA CD 2.30000% 06/19/2019 |
| 624786FR5 | CD | Mufg Union Bank Na San Fran CA CD 2.40000% 05/13/2020 |
| 62835LAH7 | CD | Mutual Savings Bank Franklin IN CD 5.20000% 05/13/2024 |
| 63518VAA2 | CD | National Cap Bank WA D C CD 4.15000% 05/29/2026 |
| 63969ACD4 | CD | Nebraska St Bank &tr Broken Bow CD 1.95000% 02/21/2022 |
| 64016YAH6 | CD | Neighborhood National Bank El Cajon CD 4.25000% 12/09/2025 |
| 654062MJ4 | CD | Nicolet National Bank Green Bay WI CD 3.85000% 11/01/2027 |
| 67118MAH2 | CD | Old MO Bank Springfield CD 4.85000% 05/15/2025 |
| 680061HS0 | CD | Old National Bank Evansville IN CD 1.95000% 05/26/2023 |
| 682325DT9 | CD | One Community Bank OR WI CD 5.50000% 12/30/2024 |
| 682325DY8 | CD | One Community Bank OR WI CD 5.00000% 08/29/2025 |
| 68371GDG4 | CD | Open Bank Los Angeles CA CD 4.45000% 02/24/2025 |
| 69355NBZ7 | CD | PNC Bank National Association CD 4.50000% 12/28/2023 |
| 69355NCX1 | CD | PNC Bank National Association CD 5.25000% 06/28/2024 |
| 69355NEF8 | CD | PNC Bank National Association CD 5.45000% 10/17/2024 |
| 69355NER2 | CD | PNC Bank National Association CD 5.40000% 11/15/2024 |
| 693963AB6 | CD | Pacific Alliance Bank Rosemead CD 4.20000% 10/14/2025 |
| 69506YVP1 | CD | Pacific Westn Bank Beverly Hills CD 4.60000% 01/11/2024 |
| 70337MHP6 | CD | Patriot Bank N A CD 4.50000% 08/03/2026 |
| 71019PBV5 | CD | Peoples Bank Middle TN CD 4.50000% 08/16/2023 |
| 71104AAT0 | CD | Peoples Exchange Bank Winchester CD 4.00000% 01/21/2026 |
| 712498CL6 | CD | Peoples St Bank Prairie Du Chien CD 5.05000% 03/13/2025 |
| 712515KX2 | CD | Peoples St Bank Wausau WI CD 4.20000% 02/06/2026 |
| 720121AJ1 | CD | Piedmont Bank Norcross GA CD 5.45000% 04/19/2024 |
| 72345SHR5 | CD | Pinnacle Bank Nashville TN CD 2.45000% 11/14/2019 |
| 72345SKW0 | CD | Pinnacle Bank Nashville TN CD 2.20000% 08/28/2023 |
| 72346RBL5 | CD | Pinnacle Bank Elberton GA CD 5.35000% 08/23/2024 |
| 72347BAF3 | CD | Pinnacle Bank Inc Vanceburg KY CD 2.30000% 08/30/2019 |
| 726547BE1 | CD | Plains St Bank TX CD 2.50000% 02/28/2020 |
| 726547CC4 | CD | Plains St Bank TX CD 4.90000% 04/15/2024 |
| 726547CD2 | CD | Plains St Bank TX CD 5.00000% 02/18/2025 |
| 726547CG5 | CD | Plains St Bank TX CD 5.10000% 10/27/2025 |
| 726547CS9 | CD | Plains St Bank TX CD 3.90000% 01/19/2027 |
| 732770BS0 | CD | Pony Express Bank Missouri CD 2.10000% 08/31/2023 |
| 74349KDX5 | CD | Prospect Bank (illinois) CD 5.20000% 05/29/2025 |
| 743837DV5 | CD | Provident Bank Amesbury MA CD 2.30000% 08/26/2019 |
| 75524KPW8 | CD | Citizens Bank Na Providence RI CD 4.60000% 06/26/2023 |
| 75524KPY4 | CD | Citizens Bank Na Providence RI CD 4.55000% 10/18/2023 |
| 75524KQD9 | CD | Citizens Bank Na Providence RI CD 4.70000% 02/15/2024 |
| 75524KQF4 | CD | Citizens Bank Na Providence RI CD 5.10000% 12/15/2023 |
| 75524KRE6 | CD | Citizens Bank Na Providence RI CD 5.40000% 05/15/2024 |
| 768825BF7 | CD | Riverside Bank Sparkman Ar CD 4.25000% 01/17/2024 |
| 78658Q5J8 | CD | Safra National Bank Newyork Certificate of Deposit Programbook Entry 3/A2instl Ctf Dep2.550% 01/16/20 B/E Dtd 01/17/19 |
| 78658Q5M1 | CD | Safra National Bank of New York Institutional CD 2.55000% 01/30/2020 |
| 78658Q7A5 | CD | Safra National Bank of New York Institutional CD 2.00000% 07/30/2020 |
| 78658RBR1 | CD | Safra National Bank N/instl Certificate of Deposit Unsec |
| 78658RKQ3 | CD | Safra National Bank N/instl Certificate of Deposit Unsec |
| 78658RKZ3 | CD | Safra National Bank N/instl Certificate of Deposit Unsec |
| 78658RNA5 | CD | Safra National Bank N/instl Certificate of Deposit Unsec |
| 78658RPP0 | CD | Safra National Bank N/instl Certificate of Deposit Unsec |
| 7954503X1 | CD | Sallie Mae Bank Murray UT CD 1.90000% 08/23/2021 |
| 795450P66 | CD | Sallie Mae Bank Murray UT CD 3.20000% 05/09/2023 |
| 795450T47 | CD | Sallie Mae Bank Murray UT CD 3.30000% 07/03/2023 |
| 80280JWV9 | CD | Santander Bank National Assn CD 5.30000% 09/16/2024 |
| 80280JWY3 | CD | Santander Bank National Assn CD 5.00000% 11/21/2024 |
| 80280JXV8 | CD | Santander Bank National Assn CD 5.35000% 06/18/2025 |
| 814661AC8 | CD | Security National Bank Omaha NE CD 4.00000% 01/15/2026 |
| 81501JAC6 | CD | Security St Bank Warroad MN CD 4.50000% 12/20/2024 |
| 82669LLJ0 | CD | Signature Bank of Arkansas CD 4.20000% 11/26/2025 |
| 82869ABP9 | CD | Simmons Bank Pinebluff Ark Ctf Dep2.100% 12/30/22 B/E Dtd 06/30/22 |
| 82869AFN0 | CD | Simmons Bank Pine Bluff Ark CD 5.10000% 03/27/2025 |
| 82869AHR9 | CD | Simmons Bank Pine Bluff Ark CD 4.30000% 04/25/2025 |
| 84287PGL0 | CD | Southern First Bank N A Greenvil CD 1.65000% 02/28/2023 |
| 84287PHX3 | CD | Southern First Bank N A Greenvil CD 5.35000% 02/23/2024 |
| 851791AW3 | CD | Springs VY Bank &tr Co CD 2.40000% 10/05/2020 |
| 856188CA3 | CD | State Bank Fenton MI CD 4.95000% 06/30/2025 |
| 856487AN3 | CD | State Bank Reeseville WI CD 2.40000% 04/12/2021 |
| 856528EM2 | CD | State Bank TX Dallas CD 5.05000% 03/19/2024 |
| 856528EP5 | CD | State Bank TX Dallas CD 5.05000% 03/28/2024 |
| 856528ER1 | CD | State Bank TX Dallas CD 5.15000% 02/28/2025 |
| 856528ES9 | CD | State Bank TX Dallas CD 5.00000% 08/29/2025 |
| 857894ZR3 | CD | Stearns Bank Na St Cloud MN CD 2.45000% 05/28/2021 |
| 868221AB8 | CD | Superior National Bank Hancock MI CD 4.55000% 04/15/2024 |
| 87164DMG2 | CD | Synovus Bank Columbus GA CD 2.45000% 02/13/2020 |
| 87164DVS6 | CD | Synovus Bank Columbus GA CD 5.00000% 06/10/2024 |
| 87164YYU2 | CD | Synchrony Bank Re/retail Certificate of Deposit Unse |
| 87220LCD4 | CD | Tbk Bank SSB Inst/instl Certificate of Deposit Unsec |
| 87220LDL5 | CD | Tbk Bank SSB Inst/instl Certificate of Deposit Unsec |
| 872308GB1 | CD | Tcm Bank National Assoc Tampa Fl CD 5.20000% 08/23/2024 |
| 88269ACU0 | CD | Texas Sec Bank Dallas TX CD 4.30000% 05/26/2028 |
| 89155MBZ9 | CD | Touchmark National Bank Norcross GA CD 5.10000% 10/05/2023 |
| 89235MSR3 | CD | Toyota Financial Savings Bank Hend NV CD 4.00000% 08/06/2027 |
| 89388CJX7 | CD | Transportation Alliance Bank Inc CD 4.10000% 06/15/2026 |
| 89580DAZ5 | CD | Triad Business Bank CD 5.30000% 12/30/2024 |
| 89580DBB7 | CD | Triad Business Bank CD 5.30000% 10/17/2025 |
| 89678LGJ0 | CD | Triumph Bank Germantown TN CD 2.50000% 07/15/2020 |
| 90344LEE5 | CD | Usny Bank Geneva NY CD 2.55000% 12/30/2019 |
| 90354KCB2 | CD | U.S. Bank National Ass/instl Certificate of Deposit Unsec |
| 90355GAX4 | CD | UBS Bank USA Salt Lake City Ut CD 4.50000% 02/03/2025 |
| 90355GHN9 | CD | UBS Bank USA National Assn CD 5.15000% 11/09/2026 |
| 90355GHZ2 | CD | UBS Bank USA Salt Lake City Ut CD 4.95000% 12/01/2025 |
| 90421MDK6 | CD | Umpqua Bank Roseburg OR CD 1.80000% 03/23/2020 |
| 908398AB6 | CD | Union St Bank Ark City Kansas CD 5.45000% 07/15/2024 |
| 909557KU3 | CD | United Bankers Bank Bloomington CD 4.90000% 02/04/2026 |
| 909557LB4 | CD | United Bankers Bank Bloomington CD 5.00000% 03/30/2026 |
| 909557LE8 | CD | United Bankers Bank Bloomington CD 3.90000% 09/11/2026 |
| 90983WCD1 | CD | United Community Bank Chatham IL CD 4.00000% 01/29/2027 |
| 91134CCJ8 | CD | United Prairie Bank MTN Lake MN CD 4.05000% 07/07/2023 |
| 919853GY1 | CD | Valley National Bank Passaic NJ CD 3.55000% 09/21/2023 |
| 919853KU4 | CD | Valley National Bank Passaic NJ CD 5.30000% 06/05/2024 |
| 923450BD1 | CD | Veritex Community Bank Na Dallas TX CD 2.35000% 09/19/2019 |
| 923450DD9 | CD | Veritex Community Bank Na Dallas TX CD 4.70000% 11/24/2023 |
| 92834ABU9 | CD | Vision Bank St Louis Pk MN CD 5.30000% 11/14/2025 |
| 928784EN3 | CD | Volunteer St Bank TN CD 2.15000% 05/16/2019 |
| 929356AE3 | CD | Winona National &svgs Bank MN CD 4.70000% 07/07/2023 |
| 938828DZ0 | CD | Washington Fed Bank Seattle CD 5.30000% 06/18/2025 |
| 949763SE7 | CD | Wells Fargo Bank National Assn CD 2.80000% 07/13/2020 |
| 95763PRB9 | CD | Western Alliance Bank Phoenix CD 5.40000% 03/13/2024 |
| 95763PTL5 | CD | Western Alliance Bank Phoenix CD 5.25000% 12/01/2025 |
| 95763PVS7 | CD | Western Alliance Bank Phoenix CD 4.20000% 05/27/2026 |
| 95763PXR7 | CD | Western Alliance Bank Phoenix CD 4.15000% 11/30/2026 |
| 96153WAK8 | CD | Weststar Bank El Paso TX CD 4.70000% 04/25/2025 |
| 96153WAU6 | CD | Weststar Bank El Paso TX CD 4.00000% 10/24/2025 |
| 98970LPN7 | CD | Zions Bancorpor/instl Certificate of Deposit Unsec |
| 69374H881 | FUNDNAME | Pacer U.S. Cash Cows 100 ETF |
| 09250G102 | INSURED | BlackRock Insured Municipal Income T |
| 09254T100 | INSURED | BlackRock MuniYield Fl Insured Fund |
| 458083490 | INSURED | Insured Municipals Income Trust Unit Ser 79 Monthly |
| 46132P108 | INSURED | Invesco Insured Municipal Income Trust |
| 00507V109 | MERGER | Activision Blizzard Inc Com *cash Merger At $ 95.00* |
| 009CVR036 | MERGER | Akouos Inc Shares *cash Payout At $ 1.00* |
| 02916P103 | MERGER | American Railcar Inds Inc Com *cash Merger At $70.00 Per Share* |
| 032359309 | MERGER | Amtrust Financial Services Inc Com *cash Merger At $14.75 Per Share* |
| 03753U106 | MERGER | Apellis Pharmaceuticals Inc Com Exchanged For CUSIP 037cvr016 & Cash Merger At $41.00 |
| 05370A108 | MERGER | Avidity Biosciences Inc Com Cash Merger At $72.00 |
| 118230101 | MERGER | Buckeye Partners LP Unit Limited Participation **cash Merger At $41.50 Per Share** |
| 12508E101 | MERGER | Cdk Global Inc Com  *cash Merger At $ 54.87* |
| 126349109 | MERGER | CSG Systems International Inc Cash Merger At $80.7 |
| 12673P105 | MERGER | CA Inc Com *cash Merger At $44.50 Per Share* |
| 128246105 | MERGER | Calavo Growers Inc Exchanged For 0.979 Shares of CUSIP 60510v108 & Cash Merger At $14.85 |
| 148806102 | MERGER | Catalent Inc Com *cash Merger At $ 63.50* |
| 16150R104 | MERGER | Chase Corp Com *cash Merger At $ 127.50* |
| 177376100 | MERGER | Citrix System Inc Com *cash Merger At $ 104.00* |
| 209034107 | MERGER | Consolidated Communications Holdings Inc *cash Merger At $ 4.70* |
| 212015101 | MERGER | Continental Resources Inc Com *cash Merger At $ 74.28* |
| 22282E102 | MERGER | Covanta Holding Corporation Com Stock Usd0.10 *cash Merger At 20.25* |
| 22304C100 | MERGER | Covetrus Inc Com *cash Merger At $ 21.00* |
| 291641108 | MERGER | Empire Dist Elec Co *cash Merger At $34.00 Per Share* |
| 30063P105 | MERGER | Exact Sciences Corp Cash Merger At $ 105.00 |
| 344849104 | MERGER | Foot Locker Inc Com  *cash Merger At $24.00* |
| 419879101 | MERGER | Hawaiian Holdings Inc Com  *cash Merger At $18.00* |
| 431571108 | MERGER | Hillenbrand Inc Cash Merger At $32 |
| 456CSH014 | MERGER | Infinera Corp Com Merger Election From CUSIP 45667g103 Cash Election |
| 487836108 | MERGER | Kellanova Com Cash Merger At $83.5 |
| 49271M100 | MERGER | Keurig Green MTN Inc *cash Merger At $92.00 Per Share* |
| 552676108 | MERGER | Mdc Holdings Inc *cash Merger At $ 63.00* |
| 61166W101 | MERGER | Monsanto Co Com  *cash Merger At $128.00 Per Share* |
| 655664100 | MERGER | Nordstrom Inc Com NPV *cash Merger At $24.25* |
| 740189105 | MERGER | Precision Castparts Corp *cash Merger At $235 Per Share* |
| 748356102 | MERGER | Questar Corp Com *cash Merger At $25.00 Per Share* |
| 758766109 | MERGER | Regal Entertainment Group Com  Cl A *cash Merger At $23.00 Per Share* |
| 80283M101 | MERGER | Santander Consumer USA Holdings I Com *cash Merger At $ 41.5* |
| 806882106 | MERGER | Radius Recycling Inc Cl A *cash Merger At $30.00 Per Share* |
| 82028K200 | MERGER | Shaw Communications Inc Cl B Conv Isin #ca82028k2002  #2801836 *cash Merger At $ 29.87591536* |
| 82489T104 | MERGER | Shockwave Medical Inc *cash Merger At $335.00* |
| 838518108 | MERGER | South Jersey Industries *cash Merger At $ 36.00* |
| 848637104 | MERGER | Splunk Inc Com  *cash Merger At $157.00* |
| 872375100 | MERGER | Teco Energy Inc **cash Merger At $27.55 Per Share** |
| 87265H109 | MERGER | Tri Pointe Homes Inc Com Cash Merger At $47.0 |
| 87901J105 | MERGER | Tegna Inc Com Cash Merger At $22.00 Per Share |
| 87968A104 | MERGER | Tellurian Inc New Com *cash Merger At $1.00 Per Share* |
| 912909108 | MERGER | United States Steel Corp *cash Merger At $55.0* |
| 92240M108 | MERGER | Vector Group Limited *cash Merger At $15.00 Per Share* |
| 923454102 | MERGER | Veritiv Corp Com *cash Merger At $ 170.00* |
| 928563402 | MERGER | Vmware Inc Com Stock  Cl A *cash Merger At $ 142.50* |
| 966837106 | MERGER | Whole Foods Market Inc Com Stock NPV *cash Merger At $42.00 Per Share* |
| 969CSH980 | MERGER | Williams Cos Inc Cash Election Fm 969457100 |
| 98416J118 | MERGER | Xerium Technologies Inc Com  *cash Merger At $13.50 Per Share* |
| 98936J101 | MERGER | Zendesk Inc Com  *cash Merger At $ 77.50* |
| 98983V106 | MERGER | Zuora Inc Com Cl A *cash Merger At $10.00 Per Share* |
| G2554F113 | MERGER | Covidien PLC  Isin #ie00b68sqd29  #b68sqd2 *exchanged For 0.956 Shares of CUSIP G5960l103 & Cash |
| 009999875 | MMF | Treasury Money Market Cl A |
| 009999877 | MMF | Treasury Securities Money Market Fund |
| 02630U107 | MMF | American Funds U.S. Government Money Market Fund Cl A |
| 02630U602 | MMF | American Funds US Government Money Market Cl 529-A |
| 02630U875 | MMF | American Funds U.S. Government Money Market Cl 529-F-1 |
| 09248U213 | MMF | BlackRock Liquidity Funds FedFund Premier Shares |
| 316067107 | MMF | Fidelity Government Cash Reserves |
| 31607A877 | MMF | Fimm Money Market Prime Resources Port Cl I |
| 316175108 | MMF | Fidelity Money Market Government Portfolio Cl I |
| 316175207 | MMF | FIMM Money Market Portfolio Cl I |
| 31617H102 | MMF | Fidelity Government Money Market |
| 31617H201 | MMF | Fidelity Money Market |
| 31617H508 | MMF | Fidelity Govt Money Market Capital Reserves Cl |
| 31617H805 | MMF | Fidelity Money Market Premium Class |
| 372497404 | MMF | Gsf Gold Sachs VIT Government Money Market Fund Serv |
| 52470R847 | MMF | Western Asset Government Reserves Cl A |
| 60934N682 | MMF | Federated Hermes U.S. Treasury Cash Reserves Fund Cl I |
| 650914203 | MMF | Prime Fund Capital Reserves Cl |
| 922906201 | MMF | Vanguard Cash Reserv Federal Money Market Invtr |
| 922906300 | MMF | Vanguard Fed Reserve Money Market Investor Cl |
| 922906508 | MMF | Vanguard Cash Reserv Fed Money Market Admiral |
| 922907506 | MMF | Vanguard Municipal Money Market Inv |
| 949917371 | MMF | Wells Fgo Avtg Money Mkt-Inv |
| 30271S404 | UITCASH | First Trust Unit 3982 Multi Sector Income Portfolio Ser 12 Monthly Cash |
| 30278Q203 | UITCASH | First Trust Unit 3201 Defensive Equity Portfolio Ser 17 Semi Annual Cash |
| 30279H400 | UITCASH | First Trust Unit 3355 Natural Gas Portfolio Ser 13 Semi Annual Cash |
| 30280X253 | UITCASH | First Trust Unit 3879 Preferred Income Portfolio Ser 58 Monthly Cash |
| 30280Y657 | UITCASH | First Trust Unit 3940 Target VIP 1q 13 Term 4/9/14 Semi Annual Cash |
| 30282W600 | UITCASH | FT Unit 4593 60/40 Strategic Allocation Port 1q 14 Term 04/16/15 Monthly Cash |
| 30284T605 | UITCASH | FT Unit 5008 Defensive Equity Portfolio Ser 29 Semi Annual Cash |
| 30285G388 | UITCASH | FT Unit 5153 Health Care Select Port Ser 35 Semi Annual Cash |
| 30285G735 | UITCASH | FT Unit 5164 Defensive Equity Portfolio Ser 30 Semi Annual Cash |
| 30286B156 | UITCASH | FT Unit 5378 60/40 Strategic Allocation Port 2q 15 Term 7/15/16 Monthly Cash |
| 30288G559 | UITCASH | FT Unit 5968 60/40 Strategic Allocation Port 2q 16 Term 7/17/17 Monthly Cash |
| 30289A205 | UITCASH | FT Unit 6083 Defensive Equity Portfolio Ser 37 Semi-Annual Cash |
| 40166C265 | UITCASH | Guggenheim Defined Portfolios Unit 897 Zacks Income Advantage Strategy Port Ser 17 Monthly Cash |
| 40166G100 | UITCASH | Guggenheim Defined Portfolios Unit 967 Zacks Income Advantage Strategy Port Ser 19 Monthly Cash |
| 40167Q743 | UITCASH | Guggenheim Defined Portfolios Unit 863 Zacks Income Advantage Strategy Portfolio Ser 16 Monthly Cash |
| 40168B406 | UITCASH | Guggenheim Defined Portfolios Unit 1064 U.S. Low Volatility Strategy Port Ser 4 Monthly Cash |
| 40168C388 | UITCASH | Guggenheim Defined Portfolios Unit 1030 Zacks Income Advantage Strategy Port Ser 21 Monthly Cash |
| 40168J300 | UITCASH | Guggenheim Defined Portfolios Unit 1102 Zacks Income Advantage Strategy Port Ser 23 Monthly Cash |

## The census: CUSIPs of the silver transactions whose prefix, description or asset type suggests cash or a sweep

Flagged by prefix FDIC/CASH/SWEEP, a description word (SWEEP, DEPOSIT, FDIC, INSURED, MONEY MARKET, CASH, LIQUIDITY, BANK, RESERVE) or Asset_Type Cash. Distinct flagged CUSIPs: 520.

By status: SWEEP=2, CASH_BALANCE=1, REJECTED=517, UNACCOUNTED=0

| CUSIP | description (most common) | asset type | rows | accounts | flagged by | status |
|---|---|---|---|---|---|---|
| FDIC66606 | Bank Deposit Sweep Program | Cash | 143357 | 708 | asset_type:Cash,description:BANK,description:DEPOSIT,description:SWEEP,prefix:FDIC | SWEEP |
| CFNCASH | Cash Credit (Debit) Balance | Cash | 93833 | 1514 | asset_type:Cash,description:CASH | CASH_BALANCE |
| FDIC66853 | Advisory Retirement Sweep Program | Cash | 80939 | 391 | asset_type:Cash,description:SWEEP,prefix:FDIC | SWEEP |

The rejected candidates (517) are listed with their descriptions and reasons below.

## Behavior census (list only; informs, decides nothing)

Per CUSIP over the silver transactions: accounts holding it, rows, first date, share of its rows on an account-day on which the account also traded another CUSIP, dividend rows (dv/dvr) and the distinct months carrying one.

| CUSIP | role | accounts | rows | first date | same-day paired % | dv+dvr rows | dividend months | months active |
|---|---|---|---|---|---|---|---|---|
| FDIC66606 | listed (a) | 708 | 143357 | 2013-06-27 | 74.5 | 30708 | 152 | 157 |
| FDIC66853 | listed (a) | 391 | 80939 | 2018-02-28 | 78.1 | 21632 | 99 | 101 |
| 316067107 | rule (b) candidate, OFF | 232 | 8768 | 2023-03-17 | 91.1 | 6702 | 40 | 40 |
| 009999875 | MMF, off | 3 | 3 | 2013-12-31 | 33.3 | 3 | 1 | 1 |
| 009999877 | MMF, off | 1 | 3 | 2015-10-30 | 0.0 | 3 | 3 | 3 |
| 02630U107 | MMF, off | 1 | 2 | 2014-02-03 | 50.0 | 0 | 0 | 1 |
| 02630U602 | MMF, off | 2 | 7 | 2020-04-30 | 100.0 | 0 | 0 | 3 |
| 02630U875 | MMF, off | 1 | 2 | 2020-08-31 | 100.0 | 0 | 0 | 2 |
| 09248U213 | MMF, off | 1 | 13 | 2025-11-26 | 23.1 | 11 | 6 | 6 |
| 31607A877 | MMF, off | 48 | 1178 | 2019-02-07 | 96.3 | 955 | 19 | 19 |
| 316175108 | MMF, off | 36 | 1088 | 2023-03-17 | 85.3 | 702 | 40 | 40 |
| 316175207 | MMF, off | 1 | 119 | 2022-12-22 | 99.2 | 86 | 43 | 43 |
| 31617H102 | MMF, off | 1 | 285 | 2022-07-13 | 89.5 | 95 | 47 | 48 |
| 31617H201 | MMF, off | 14 | 103 | 2022-12-07 | 100.0 | 61 | 4 | 4 |
| 31617H508 | MMF, off | 25 | 8895 | 2016-01-22 | 80.5 | 2919 | 125 | 126 |
| 31617H805 | MMF, off | 1 | 6 | 2017-11-15 | 100.0 | 4 | 2 | 2 |
| 372497404 | MMF, off | 1 | 2 | 2026-01-28 | 50.0 | 0 | 0 | 2 |
| 52470R847 | MMF, off | 1 | 2 | 2020-06-08 | 100.0 | 0 | 0 | 1 |
| 60934N682 | MMF, off | 1 | 5 | 2024-09-24 | 100.0 | 3 | 2 | 2 |
| 650914203 | MMF, off | 1 | 2 | 2013-06-27 | 100.0 | 0 | 0 | 2 |
| 922906201 | MMF, off | 25 | 648 | 2018-07-18 | 89.5 | 525 | 32 | 33 |
| 922906300 | MMF, off | 2 | 7 | 2018-08-07 | 100.0 | 2 | 2 | 2 |
| 922906508 | MMF, off | 2 | 46 | 2021-03-05 | 93.5 | 10 | 6 | 7 |
| 922907506 | MMF, off | 1 | 3 | 2024-12-11 | 100.0 | 1 | 1 | 1 |
| 949917371 | MMF, off | 1 | 2 | 2014-12-12 | 50.0 | 0 | 0 | 2 |

## The single-flow months of the largest class (lo/over 10%), BEFORE and AFTER

The DIFF months (before) of the class `commonwealth_flow_diff_classes` ranks first (lo/over 10%: 57 DIFF months) with exactly one external flow row of the class's type: 11. A DOUBLE-DROP month is one where the account value on the flow day fell by twice the withdrawal (|drop - 2|flow|| <= 1% of |flow| + 0.05, before): 0; a drop of once the withdrawal: 4.

Reading notes: 11 of the 11 single-flow months have a listed-sweep sale of any amount on the flow's day; 0 of the 0 double-drop months pair with a sweep sale of the same amount (within 0.01). Fixed (DIFF before, MATCH after) among the double-drop months: 0.

### The double-drop months, named

| account | month | flow day | withdrawal | value drop / withdrawal | sweep sale that day | before | computed | reported | diff | after | computed | diff |
|---|---|---|---|---|---|---|---|---|---|---|---|---|

### The other 11 single-flow months (value did not fall by twice the withdrawal)

| account | month | withdrawal | value drop / withdrawal | sweep sale that day | before | diff | after | diff |
|---|---|---|---|---|---|---|---|---|
| acct#f74da374 | 2024-01 | 33300.0 | 0.902 | 33300.0 | DIFF | 2.5691 | DIFF | 2.5691 |
| acct#f74da374 | 2024-03 | 36000.0 | 0.919 | 36000.0 | DIFF | -3.016 | DIFF | -3.016 |
| acct#2d4385bf | 2021-02 | 5800.0 | 1.017 | 5800.0 | DIFF | 6.7385 | DIFF | 6.7385 |
| acct#2d4385bf | 2023-05 | 3485.0 | 1.003 | 3485.0 | DIFF | 0.0601 | DIFF | 0.0601 |
| acct#f0b52456 | 2022-11 | 20000.0 | 0.984 | 20000.0 | DIFF | 2.2108 | DIFF | 2.2108 |
| acct#f0b52456 | 2023-05 | 20000.0 | 0.99 | 20000.0 | DIFF | -6.2534 | DIFF | -6.2534 |
| acct#1f02bee1 | 2023-02 | 28574.88 | 1.0 | 28574.88 | DIFF | 5.9962 | DIFF | 5.9962 |
| D49143349 | 2022-12 | 75000.0 | 0.999 | 75000.0 | DIFF | 1.8833 | DIFF | 1.8833 |
| D49151054 | 2021-08 | 8055.0 | 0.992 | 8055.0 | DIFF | 9.7228 | DIFF | 9.7228 |
| acct#c0cea213 | 2025-04 | 264824.0 | 0.943 | 53311.8 | DIFF | 0.1692 | DIFF | 0.1692 |
| acct#6834d5a2 | 2025-04 | 75743.0 | 0.983 | 0.69 | DIFF | 0.551 | DIFF | 0.551 |

## The whole grade, before and after

- before: MONTHLY-GRADE months=82593 match=3098 diff=886 ungradable=78609 tolerance_pct=0.05
- after:  MONTHLY-GRADE months=82593 match=3098 diff=886 ungradable=78609 tolerance_pct=0.05

| verdict | before | after |
|---|---|---|
| MATCH | 3098 | 3098 |
| DIFF | 886 | 886 |
| UNGRADABLE | 78609 | 78609 |

Verdict moves (before -> after, months):

- UNGRADABLE -> UNGRADABLE: 78609
- MATCH -> MATCH: 3098
- DIFF -> DIFF: 886

### Months that moved MATCH -> DIFF between the arms, each named: 0 (never forced)

| account | month | BEFORE computed | AFTER computed | reported | AFTER diff |
|---|---|---|---|---|---|

## The round-19 MATCH -> DIFF months (mover_classes.parquet), with their result in this re-grade

163 months (account-months graded MATCH with no list and DIFF with sweeps-v1), each classed by its account's holdings (commonwealth_mover_classes: core = holds 316067107, other_mmf = holds another rejected MMF, neither). This re-grade: BEFORE = sweeps-v1-20261008, cash leg method_r25, AFTER = sweeps-v1-20261008, cash leg method_r26. Counted per class by the AFTER verdict:

| class | months | after MATCH | after DIFF | after UNGRADABLE | after ABSENT |
|---|---|---|---|---|---|
| core | 16 | 13 | 3 | 0 | 0 |
| other_mmf | 0 | 0 | 0 | 0 | 0 |
| neither | 147 | 125 | 22 | 0 | 0 |

| account | month | class | reported | round-19 no-list | round-19 v1 | before (sweeps-v1-20261008, cash leg method_r25) | after (sweeps-v1-20261008, cash leg method_r26) | after computed | after diff |
|---|---|---|---|---|---|---|---|---|---|
| acct#f6c79f45 | 2024-06 | core | -0.88 | -0.8874 | 1.2105 | DIFF | DIFF | -0.8239 | 0.0561 |
| acct#9727ac87 | 2024-07 | core | -0.08 | -0.0415 | -0.0234 | MATCH | MATCH | -0.0798 | 0.0002 |
| D49143350 | 2023-11 | core | -4.59 | -4.6175 | -5.3344 | DIFF | DIFF | -3.4367 | 1.1533 |
| D49143350 | 2026-02 | core | 2.05 | 2.0179 | -16.069 | DIFF | DIFF | 2.4881 | 0.4381 |
| acct#557ce060 | 2026-01 | core | 0.02 | 0.0118 | 0.0988 | MATCH | MATCH | 0.0233 | 0.0033 |
| acct#c0cea213 | 2024-10 | core | -0.0 | 0.0329 | 0.1609 | MATCH | MATCH | 0.0468 | 0.0468 |
| acct#7f62f16f | 2025-02 | core | 0.06 | 0.0995 | 0.1518 | MATCH | MATCH | 0.0645 | 0.0045 |
| acct#61ebda90 | 2025-04 | core | 0.09 | 0.0436 | 95.1114 | MATCH | MATCH | 0.0872 | -0.0028 |
| acct#ce1f487c | 2025-04 | core | 0.09 | 0.0436 | 95.1114 | MATCH | MATCH | 0.0872 | -0.0028 |
| acct#16bf540c | 2025-04 | core | 0.09 | 0.0436 | 95.1114 | MATCH | MATCH | 0.0872 | -0.0028 |
| acct#177b7e48 | 2025-04 | core | 0.09 | 0.0436 | 95.1114 | MATCH | MATCH | 0.0872 | -0.0028 |
| acct#aed810ab | 2025-04 | core | 0.09 | 0.0436 | 95.1116 | MATCH | MATCH | 0.0872 | -0.0028 |
| acct#781a748b | 2025-04 | core | 0.09 | 0.0436 | 95.1114 | MATCH | MATCH | 0.0872 | -0.0028 |
| acct#1b22f63a | 2025-04 | core | 0.09 | 0.0436 | 95.1114 | MATCH | MATCH | 0.0872 | -0.0028 |
| acct#744c9c00 | 2025-06 | core | 0.15 | 0.1042 | 99.2457 | MATCH | MATCH | 0.1533 | 0.0033 |
| acct#5fd6a5d4 | 2026-05 | core | 0.03 | 0.0283 | 0.265 | MATCH | MATCH | 0.0284 | -0.0016 |
| acct#aaeb760c | 2021-10 | neither | 5.51 | 5.4855 | 6.0313 | DIFF | DIFF | 5.3811 | -0.1289 |
| acct#aaeb760c | 2022-03 | neither | 4.82 | 4.7791 | 5.0603 | DIFF | DIFF | 4.6996 | -0.1204 |
| acct#aaeb760c | 2022-08 | neither | -1.06 | -1.0435 | -1.3538 | MATCH | MATCH | -1.027 | 0.033 |
| acct#aaeb760c | 2023-12 | neither | 1.56 | 1.5886 | 1.6144 | MATCH | MATCH | 1.5676 | 0.0076 |
| acct#aaeb760c | 2025-03 | neither | -7.16 | -7.1874 | -7.4127 | MATCH | MATCH | -7.1115 | 0.0485 |
| acct#b4db1f25 | 2020-01 | neither | 0.02 | 0.0169 | 0.0835 | MATCH | MATCH | 0.0212 | 0.0012 |
| acct#b4db1f25 | 2020-02 | neither | 0.02 | 0.0158 | 0.0781 | MATCH | MATCH | 0.0199 | -0.0001 |
| acct#b4db1f25 | 2020-11 | neither | 0.08 | 0.0654 | 0.0034 | MATCH | MATCH | 0.0808 | 0.0008 |
| acct#03836058 | 2022-04 | neither | -1.41 | -1.3963 | -2.7833 | DIFF | DIFF | -1.1928 | 0.2172 |
| acct#eea1157e | 2021-05 | neither | 0.76 | 0.7731 | 1.3492 | DIFF | DIFF | 1.1828 | 0.4228 |
| acct#eea1157e | 2022-12 | neither | -0.04 | 0.0072 | -0.5123 | MATCH | MATCH | 0.0099 | 0.0499 |
| acct#eea1157e | 2023-07 | neither | -0.02 | -0.0182 | 0.0314 | MATCH | MATCH | -0.025 | -0.005 |
| acct#eea1157e | 2024-09 | neither | 0.13 | 0.1142 | -0.3309 | MATCH | MATCH | 0.153 | 0.023 |
| acct#eea1157e | 2025-08 | neither | 1.22 | 1.2591 | 1.974 | DIFF | DIFF | 1.6857 | 0.4657 |
| acct#1c3da532 | 2017-08 | neither | 0.0 | 0.0039 | 0.0503 | MATCH | MATCH | 0.0042 | 0.0042 |
| acct#1c3da532 | 2017-10 | neither | 0.0 | 0.0039 | 0.0502 | MATCH | MATCH | 0.0042 | 0.0042 |
| acct#1c3da532 | 2017-12 | neither | 0.0 | 0.0039 | 0.0502 | MATCH | MATCH | 0.0042 | 0.0042 |
| acct#1c3da532 | 2018-01 | neither | 0.01 | 0.0112 | 0.1447 | MATCH | MATCH | 0.0122 | 0.0022 |
| acct#1c3da532 | 2018-02 | neither | 0.01 | 0.0106 | 0.1363 | MATCH | MATCH | 0.0115 | 0.0015 |
| acct#1c3da532 | 2018-03 | neither | 0.01 | 0.013 | 0.1669 | MATCH | MATCH | 0.0141 | 0.0041 |
| acct#5aa91f68 | 2017-07 | neither | 0.0 | 0.002 | 0.093 | MATCH | MATCH | 0.002 | 0.002 |
| acct#5aa91f68 | 2017-08 | neither | 0.0 | 0.0042 | 0.1956 | MATCH | MATCH | 0.0042 | 0.0042 |
| acct#5aa91f68 | 2017-09 | neither | 0.0 | 0.0039 | 0.1854 | MATCH | MATCH | 0.004 | 0.004 |
| acct#5aa91f68 | 2017-10 | neither | 0.0 | 0.0042 | 0.1948 | MATCH | MATCH | 0.0042 | 0.0042 |
| acct#5aa91f68 | 2017-12 | neither | 0.0 | 0.0041 | 0.1892 | MATCH | MATCH | 0.0042 | 0.0042 |
| acct#5aa91f68 | 2018-01 | neither | 0.01 | 0.0119 | 0.5521 | MATCH | MATCH | 0.0121 | 0.0021 |
| acct#5aa91f68 | 2018-02 | neither | 0.01 | 0.0112 | 0.5201 | MATCH | MATCH | 0.0115 | 0.0015 |
| acct#5aa91f68 | 2018-03 | neither | 0.01 | 0.0137 | 0.6324 | MATCH | MATCH | 0.014 | 0.004 |
| acct#5aa91f68 | 2018-04 | neither | 0.02 | 0.0201 | 0.9189 | MATCH | MATCH | 0.0205 | 0.0005 |
| acct#5aa91f68 | 2018-05 | neither | 0.02 | 0.0207 | 0.9388 | MATCH | MATCH | 0.0212 | 0.0012 |
| acct#5aa91f68 | 2018-06 | neither | 0.02 | 0.0201 | 0.902 | MATCH | MATCH | 0.0205 | 0.0005 |
| acct#04ebe1d1 | 2021-04 | neither | -3.41 | -3.4508 | -3.4979 | DIFF | DIFF | -3.5078 | -0.0978 |
| acct#04ebe1d1 | 2021-06 | neither | -4.82 | -4.8644 | -4.9327 | DIFF | DIFF | -4.9435 | -0.1235 |
| acct#04ebe1d1 | 2021-10 | neither | -1.39 | -1.4342 | -1.4564 | DIFF | DIFF | -1.4589 | -0.0689 |
| acct#04ebe1d1 | 2024-05 | neither | 0.67 | 0.6758 | 0.6079 | MATCH | MATCH | 0.6889 | 0.0189 |
| acct#015306a0 | 2023-04 | neither | 1.23 | 1.2331 | 1.1523 | DIFF | DIFF | 1.1702 | -0.0598 |
| acct#fa488a0b | 2021-04 | neither | 2.21 | 2.2439 | 2.2794 | DIFF | DIFF | 2.3118 | 0.1018 |
| acct#fa488a0b | 2021-08 | neither | 1.0 | 1.0456 | 1.0615 | DIFF | DIFF | 1.076 | 0.076 |
| acct#fa488a0b | 2021-10 | neither | 2.52 | 2.5402 | 2.5791 | DIFF | DIFF | 2.6146 | 0.0946 |
| acct#fa488a0b | 2023-04 | neither | 1.0 | 1.0012 | 1.1639 | MATCH | MATCH | 1.0304 | 0.0304 |
| acct#fa488a0b | 2023-07 | neither | 2.9 | 2.9077 | 3.0773 | DIFF | DIFF | 2.9899 | 0.0899 |
| acct#fa488a0b | 2024-01 | neither | -0.95 | -0.9005 | -1.1563 | MATCH | MATCH | -0.9242 | 0.0258 |
| acct#21515eb6 | 2025-04 | neither | 0.53 | 0.5019 | 0.8003 | MATCH | MATCH | 0.5019 | -0.0281 |
| acct#21515eb6 | 2025-05 | neither | 8.21 | 8.2042 | 8.2754 | MATCH | MATCH | 8.2042 | -0.0058 |
| acct#2d4385bf | 2022-03 | neither | 4.92 | 4.9078 | 4.9714 | DIFF | DIFF | 5.0504 | 0.1304 |
| acct#2d4385bf | 2023-04 | neither | -1.04 | -1.0474 | -1.1362 | MATCH | MATCH | -1.068 | -0.028 |
| acct#ab0c6781 | 2018-01 | neither | 0.18 | 0.1777 | 0.5903 | MATCH | MATCH | 0.1814 | 0.0014 |
| acct#ab0c6781 | 2018-02 | neither | 0.01 | 0.0113 | 0.5544 | MATCH | MATCH | 0.0115 | 0.0015 |
| acct#ab0c6781 | 2018-03 | neither | 0.01 | 0.0138 | 0.6766 | MATCH | MATCH | 0.0141 | 0.0041 |
| acct#92164e0d | 2017-03 | neither | -0.09 | -0.0454 | 0.0008 | MATCH | MATCH | -0.0908 | -0.0008 |
| acct#ebb31a1c | 2017-03 | neither | -0.09 | -0.0465 | 0.0008 | MATCH | MATCH | -0.0929 | -0.0029 |
| acct#dfa7a25c | 2017-06 | neither | -0.1 | -0.051 | 0.0008 | MATCH | MATCH | -0.102 | -0.002 |
| acct#4040a6ea | 2017-09 | neither | -0.07 | -0.0372 | 0.0041 | MATCH | MATCH | -0.0743 | -0.0043 |
| acct#0e2c97b9 | 2018-07 | neither | -0.08 | -0.0404 | 0.0476 | MATCH | MATCH | -0.0808 | -0.0008 |
| acct#de79caf1 | 2018-07 | neither | -0.08 | -0.0404 | 0.0476 | MATCH | MATCH | -0.0808 | -0.0008 |
| acct#25880078 | 2021-07 | neither | -0.04 | -0.0173 | -0.7036 | DIFF | DIFF | -0.1154 | -0.0754 |
| acct#25880078 | 2022-01 | neither | -9.71 | -9.669 | -9.3296 | DIFF | DIFF | -9.8401 | -0.1301 |
| acct#25880078 | 2023-04 | neither | 0.65 | 0.6165 | 0.9938 | DIFF | DIFF | 0.5451 | -0.1049 |
| acct#8680d8f4 | 2018-06 | neither | -0.08 | -0.0406 | 0.044 | MATCH | MATCH | -0.0813 | -0.0013 |
| acct#e29efebe | 2020-10 | neither | -4.06 | -4.0428 | -3.7118 | MATCH | MATCH | -4.07 | -0.01 |
| acct#e29efebe | 2020-12 | neither | 4.15 | 4.1387 | 3.8748 | MATCH | MATCH | 4.1661 | 0.0161 |
| acct#e29efebe | 2021-01 | neither | 3.93 | 3.8931 | 4.262 | MATCH | MATCH | 3.9179 | -0.0121 |
| acct#e29efebe | 2021-03 | neither | 1.7 | 1.6982 | 1.45 | MATCH | MATCH | 1.7085 | 0.0085 |
| acct#e29efebe | 2021-09 | neither | -6.42 | -6.3785 | -6.5812 | MATCH | MATCH | -6.4083 | 0.0117 |
| acct#e29efebe | 2021-12 | neither | 1.91 | 1.913 | 1.7259 | MATCH | MATCH | 1.9212 | 0.0112 |
| acct#e29efebe | 2022-03 | neither | 3.37 | 3.3653 | 3.1712 | MATCH | MATCH | 3.381 | 0.011 |
| acct#e29efebe | 2022-06 | neither | -5.26 | -5.2245 | -5.5037 | MATCH | MATCH | -5.2513 | 0.0087 |
| acct#e29efebe | 2022-12 | neither | -5.66 | -5.6204 | -5.9713 | MATCH | MATCH | -5.6507 | 0.0093 |
| acct#e29efebe | 2023-04 | neither | 6.46 | 6.4297 | 6.5457 | MATCH | MATCH | 6.4603 | 0.0003 |
| acct#e29efebe | 2023-12 | neither | -0.55 | -0.5243 | -0.7259 | MATCH | MATCH | -0.546 | 0.004 |
| acct#e29efebe | 2024-02 | neither | 3.97 | 4.0017 | 4.0695 | DIFF | DIFF | 4.1591 | 0.1891 |
| acct#e29efebe | 2024-12 | neither | -0.26 | -0.2414 | -0.431 | MATCH | MATCH | -0.2583 | 0.0017 |
| acct#79d02c2c | 2023-05 | neither | 0.1 | 0.1307 | 0.0043 | MATCH | MATCH | 0.1418 | 0.0418 |
| acct#79d02c2c | 2024-07 | neither | 1.94 | 1.9751 | 1.8241 | DIFF | DIFF | 2.1112 | 0.1712 |
| acct#79d02c2c | 2024-11 | neither | 5.35 | 5.3014 | 5.5761 | DIFF | DIFF | 5.4413 | 0.0913 |
| acct#79d02c2c | 2025-01 | neither | 2.21 | 2.1652 | 2.4415 | MATCH | MATCH | 2.2206 | 0.0106 |
| acct#4a890dd1 | 2023-05 | neither | 0.11 | 0.1379 | 0.0153 | MATCH | MATCH | 0.1493 | 0.0393 |
| acct#4a890dd1 | 2024-07 | neither | 1.94 | 1.9836 | 1.8256 | DIFF | DIFF | 2.1159 | 0.1759 |
| acct#4a890dd1 | 2025-01 | neither | 2.23 | 2.1802 | 2.4546 | MATCH | MATCH | 2.2339 | 0.0039 |
| acct#4a890dd1 | 2025-05 | neither | 4.83 | 4.8549 | 5.0695 | DIFF | DIFF | 4.9152 | 0.0852 |
| acct#3b89d062 | 2022-07 | neither | -0.08 | -0.0493 | 0.0319 | MATCH | MATCH | -0.0821 | -0.0021 |
| acct#3b89d062 | 2022-10 | neither | -0.07 | -0.0518 | 0.0829 | MATCH | MATCH | -0.0729 | -0.0029 |
| acct#3b89d062 | 2022-11 | neither | 0.03 | 0.0247 | 0.0848 | MATCH | MATCH | 0.0348 | 0.0048 |
| acct#3b89d062 | 2022-12 | neither | 0.06 | 0.0452 | 0.1552 | MATCH | MATCH | 0.0637 | 0.0037 |
| acct#3b89d062 | 2023-01 | neither | -0.04 | -0.0259 | 0.1549 | MATCH | MATCH | -0.0364 | 0.0036 |
| acct#3b89d062 | 2023-02 | neither | 0.06 | 0.0409 | 0.1398 | MATCH | MATCH | 0.0575 | -0.0025 |
| acct#6acbfb93 | 2021-06 | neither | -0.09 | -0.0468 | 0.0008 | MATCH | MATCH | -0.0936 | -0.0036 |
| acct#921b5169 | 2022-04 | neither | -0.06 | -0.0299 | 0.0007 | MATCH | MATCH | -0.0609 | -0.0009 |
| acct#921b5169 | 2022-07 | neither | -0.05 | -0.0241 | 0.0118 | MATCH | MATCH | -0.05 | 0.0 |
| acct#921b5169 | 2023-04 | neither | -0.0 | -0.0002 | 0.0611 | MATCH | MATCH | -0.0004 | -0.0004 |
| acct#921b5169 | 2023-07 | neither | 0.0 | 0.0006 | 0.0631 | MATCH | MATCH | 0.0013 | 0.0013 |
| acct#921b5169 | 2023-10 | neither | -0.0 | -0.0011 | 0.063 | MATCH | MATCH | -0.0022 | -0.0022 |
| acct#921b5169 | 2024-01 | neither | -0.0 | -0.0002 | 0.0628 | MATCH | MATCH | -0.0004 | -0.0004 |
| acct#921b5169 | 2024-04 | neither | -0.01 | -0.0051 | 0.0605 | MATCH | MATCH | -0.0103 | -0.0003 |
| acct#921b5169 | 2024-07 | neither | -0.01 | -0.0052 | 0.0624 | MATCH | MATCH | -0.0103 | -0.0003 |
| acct#921b5169 | 2024-10 | neither | -0.01 | -0.0059 | 0.0618 | MATCH | MATCH | -0.0117 | -0.0017 |
| acct#921b5169 | 2025-01 | neither | -0.04 | -0.0178 | 0.0359 | MATCH | MATCH | -0.0359 | 0.0041 |
| acct#921b5169 | 2025-04 | neither | -0.06 | -0.0294 | 0.0172 | MATCH | MATCH | -0.0593 | 0.0007 |
| acct#3345c43a | 2023-01 | neither | -0.06 | -0.029 | 0.1934 | MATCH | MATCH | -0.058 | 0.002 |
| acct#3345c43a | 2023-04 | neither | -0.06 | -0.028 | 0.1797 | MATCH | MATCH | -0.056 | 0.004 |
| acct#3345c43a | 2023-07 | neither | -0.07 | -0.0366 | 0.1546 | MATCH | MATCH | -0.0731 | -0.0031 |
| acct#3345c43a | 2023-10 | neither | -0.09 | -0.0428 | 0.1575 | MATCH | MATCH | -0.0854 | 0.0046 |
| acct#1f02bee1 | 2022-10 | neither | 11.87 | 11.8922 | 11.5015 | MATCH | MATCH | 11.8922 | 0.0222 |
| acct#1f02bee1 | 2022-11 | neither | 18.29 | 18.2894 | 18.3535 | MATCH | MATCH | 18.2894 | -0.0006 |
| acct#16f4eae3 | 2025-01 | neither | 0.92 | 0.9233 | 1.3343 | MATCH | MATCH | 0.9333 | 0.0133 |
| acct#16f4eae3 | 2026-01 | neither | 1.68 | 1.6752 | 2.1165 | MATCH | MATCH | 1.6914 | 0.0114 |
| acct#0f2d2c45 | 2024-01 | neither | -0.3 | -0.2815 | 0.0268 | MATCH | MATCH | -0.2854 | 0.0146 |
| acct#cce589ab | 2024-01 | neither | -0.3 | -0.2804 | 0.028 | MATCH | MATCH | -0.2843 | 0.0157 |
| acct#cce589ab | 2024-02 | neither | 4.32 | 4.2779 | 4.813 | MATCH | MATCH | 4.3367 | 0.0167 |
| acct#cce589ab | 2024-04 | neither | -3.96 | -3.9239 | -4.0511 | MATCH | MATCH | -3.974 | -0.014 |
| acct#cce589ab | 2024-08 | neither | 1.79 | 1.7636 | 1.9586 | MATCH | MATCH | 1.7854 | -0.0046 |
| acct#cce589ab | 2024-10 | neither | -1.6 | -1.5618 | -1.4023 | MATCH | MATCH | -1.5803 | 0.0197 |
| acct#cce589ab | 2024-11 | neither | 5.25 | 5.213 | 5.7813 | MATCH | MATCH | 5.2837 | 0.0337 |
| acct#cce589ab | 2025-01 | neither | 2.52 | 2.481 | 3.0843 | MATCH | MATCH | 2.5101 | -0.0099 |
| acct#cce589ab | 2025-02 | neither | -1.55 | -1.5551 | -1.7189 | MATCH | MATCH | -1.5729 | -0.0229 |
| acct#cce589ab | 2025-04 | neither | -0.05 | -0.0504 | 0.2743 | MATCH | MATCH | -0.051 | -0.001 |
| acct#cce589ab | 2025-07 | neither | 1.24 | 1.2346 | 1.6808 | MATCH | MATCH | 1.2482 | 0.0082 |
| acct#cce589ab | 2025-08 | neither | 2.52 | 2.4854 | 2.7275 | MATCH | MATCH | 2.5124 | -0.0076 |
| acct#cce589ab | 2025-10 | neither | 1.44 | 1.4272 | 1.8756 | MATCH | MATCH | 1.4418 | 0.0018 |
| acct#cce589ab | 2026-01 | neither | 1.76 | 1.738 | 2.218 | MATCH | MATCH | 1.7554 | -0.0046 |
| D49141608 | 2019-02 | neither | 0.04 | 0.0412 | 2.2299 | MATCH | MATCH | 0.0419 | 0.0019 |
| D49141608 | 2019-03 | neither | 0.05 | 0.0457 | 2.4237 | MATCH | MATCH | 0.0466 | -0.0034 |
| D49141608 | 2019-04 | neither | 0.05 | 0.0443 | 2.2953 | MATCH | MATCH | 0.0452 | -0.0048 |
| D49141608 | 2019-05 | neither | 0.05 | 0.0457 | 2.3132 | MATCH | MATCH | 0.0465 | -0.0035 |
| D49141608 | 2019-06 | neither | 0.05 | 0.0443 | 2.1931 | MATCH | MATCH | 0.0451 | -0.0049 |
| D49141608 | 2019-07 | neither | 0.05 | 0.0456 | 2.2124 | MATCH | MATCH | 0.0465 | -0.0035 |
| D49141608 | 2019-08 | neither | 0.04 | 0.0374 | 1.7749 | MATCH | MATCH | 0.0381 | -0.0019 |
| D49141608 | 2019-09 | neither | 0.03 | 0.0315 | 1.4675 | MATCH | MATCH | 0.0321 | 0.0021 |
| D49141714 | 2019-02 | neither | 0.04 | 0.0416 | 3.3111 | MATCH | MATCH | 0.0421 | 0.0021 |
| acct#a011b5f7 | 2025-04 | neither | 0.41 | 0.4142 | 0.3581 | MATCH | MATCH | 0.4142 | 0.0042 |
| acct#a011b5f7 | 2025-10 | neither | 0.64 | 0.6038 | 1.0099 | MATCH | MATCH | 0.6039 | -0.0361 |
| acct#a011b5f7 | 2026-01 | neither | 1.56 | 1.5626 | 1.934 | MATCH | MATCH | 1.5628 | 0.0028 |
| acct#cf292cea | 2024-07 | neither | -7.76 | -7.7261 | -8.3764 | MATCH | MATCH | -7.7261 | 0.0339 |
| acct#cf292cea | 2024-08 | neither | 4.62 | 4.6488 | 4.6829 | MATCH | MATCH | 4.6488 | 0.0288 |
| acct#cf292cea | 2024-10 | neither | -9.03 | -8.9903 | -9.7576 | MATCH | MATCH | -8.9903 | 0.0397 |
| acct#65b3b3ea | 2024-12 | neither | -8.02 | -7.9838 | -8.8079 | MATCH | MATCH | -7.9838 | 0.0362 |
| acct#65b3b3ea | 2025-03 | neither | 7.66 | 7.684 | 6.8268 | MATCH | MATCH | 7.684 | 0.024 |
| acct#65b3b3ea | 2025-04 | neither | -11.06 | -11.0556 | -11.1826 | MATCH | MATCH | -11.0556 | 0.0044 |
| acct#65b3b3ea | 2025-06 | neither | 6.23 | 6.2553 | 5.3767 | MATCH | MATCH | 6.2553 | 0.0253 |
| acct#65b3b3ea | 2025-07 | neither | 3.42 | 3.4191 | 3.5626 | MATCH | MATCH | 3.4191 | -0.0009 |
| acct#65b3b3ea | 2025-09 | neither | -0.47 | -0.4562 | -1.3469 | MATCH | MATCH | -0.4562 | 0.0138 |
| acct#65b3b3ea | 2025-10 | neither | 1.33 | 1.3311 | 1.4283 | MATCH | MATCH | 1.3311 | 0.0011 |
| acct#65b3b3ea | 2025-12 | neither | 4.56 | 4.5619 | 3.813 | MATCH | MATCH | 4.5619 | 0.0019 |
| acct#65b3b3ea | 2026-01 | neither | 16.79 | 16.7871 | 17.4998 | MATCH | MATCH | 16.7871 | -0.0029 |
| acct#65b3b3ea | 2026-03 | neither | 11.58 | 11.5754 | 11.2522 | MATCH | MATCH | 11.5754 | -0.0046 |
| acct#65b3b3ea | 2026-04 | neither | -8.79 | -8.7931 | -9.0353 | MATCH | MATCH | -8.7931 | -0.0031 |
| acct#ed5f47fe | 2026-01 | neither | 2.76 | 2.7564 | 3.0739 | MATCH | MATCH | 2.7603 | 0.0003 |

## The 163 round-19 movers under three verdicts (no list / sweeps-v1 unrepaired / repaired)

Read from mover_classes.parquet (causes from mover_causes.parquet). The verdict under the round-19 no-list arm and under sweeps-v1 unrepaired is the monthly grade's rule applied to the persisted computed return (tolerance 0.05); the BEFORE and AFTER columns are this re-grade's own arms (BEFORE = sweeps-v1-20261008, cash leg method_r25, AFTER = sweeps-v1-20261008, cash leg method_r26).

- movers: 163; MATCH under no list: 163; DIFF under sweeps-v1 unrepaired: 163
- this re-grade's BEFORE arm gives the unrepaired verdict on 25 of 163 movers
- back to MATCH in the AFTER arm: 138 of 163
- `neither` cause `other:sweep_trade_day`: 68 of 75 back to MATCH
- `neither` cause `sweep_balance`: 57 of 72 back to MATCH
- `neither` movers back to MATCH: 125 of 147; `core` movers back to MATCH: 13 of 16

| account | month | class | cause | reported | no list | v1 unrepaired | BEFORE arm | AFTER arm | AFTER computed | AFTER diff |
|---|---|---|---|---|---|---|---|---|---|---|
| acct#f6c79f45 | 2024-06 | core | other:sweep_trade_day | -0.88 | MATCH | DIFF | DIFF | DIFF | -0.8239 | 0.0561 |
| acct#9727ac87 | 2024-07 | core | other:sweep_trade_day | -0.08 | MATCH | DIFF | MATCH | MATCH | -0.0798 | 0.0002 |
| D49143350 | 2026-02 | core | other:sweep_trade_day | 2.05 | MATCH | DIFF | DIFF | DIFF | 2.4881 | 0.4381 |
| acct#557ce060 | 2026-01 | core | other:sweep_trade_day | 0.02 | MATCH | DIFF | MATCH | MATCH | 0.0233 | 0.0033 |
| acct#c0cea213 | 2024-10 | core | other:sweep_trade_day | -0.0 | MATCH | DIFF | MATCH | MATCH | 0.0468 | 0.0468 |
| acct#7f62f16f | 2025-02 | core | other:sweep_trade_day | 0.06 | MATCH | DIFF | MATCH | MATCH | 0.0645 | 0.0045 |
| acct#61ebda90 | 2025-04 | core | other:sweep_trade_day | 0.09 | MATCH | DIFF | MATCH | MATCH | 0.0872 | -0.0028 |
| acct#ce1f487c | 2025-04 | core | other:sweep_trade_day | 0.09 | MATCH | DIFF | MATCH | MATCH | 0.0872 | -0.0028 |
| acct#16bf540c | 2025-04 | core | other:sweep_trade_day | 0.09 | MATCH | DIFF | MATCH | MATCH | 0.0872 | -0.0028 |
| acct#177b7e48 | 2025-04 | core | other:sweep_trade_day | 0.09 | MATCH | DIFF | MATCH | MATCH | 0.0872 | -0.0028 |
| acct#aed810ab | 2025-04 | core | other:sweep_trade_day | 0.09 | MATCH | DIFF | MATCH | MATCH | 0.0872 | -0.0028 |
| acct#781a748b | 2025-04 | core | other:sweep_trade_day | 0.09 | MATCH | DIFF | MATCH | MATCH | 0.0872 | -0.0028 |
| acct#1b22f63a | 2025-04 | core | other:sweep_trade_day | 0.09 | MATCH | DIFF | MATCH | MATCH | 0.0872 | -0.0028 |
| acct#744c9c00 | 2025-06 | core | other:sweep_trade_day | 0.15 | MATCH | DIFF | MATCH | MATCH | 0.1533 | 0.0033 |
| acct#5fd6a5d4 | 2026-05 | core | other:sweep_trade_day | 0.03 | MATCH | DIFF | MATCH | MATCH | 0.0284 | -0.0016 |
| D49143350 | 2023-11 | core | sweep_balance | -4.59 | MATCH | DIFF | DIFF | DIFF | -3.4367 | 1.1533 |
| acct#aaeb760c | 2022-08 | neither | other:sweep_trade_day | -1.06 | MATCH | DIFF | MATCH | MATCH | -1.027 | 0.033 |
| acct#aaeb760c | 2025-03 | neither | other:sweep_trade_day | -7.16 | MATCH | DIFF | MATCH | MATCH | -7.1115 | 0.0485 |
| acct#b4db1f25 | 2020-11 | neither | other:sweep_trade_day | 0.08 | MATCH | DIFF | MATCH | MATCH | 0.0808 | 0.0008 |
| acct#eea1157e | 2022-12 | neither | other:sweep_trade_day | -0.04 | MATCH | DIFF | MATCH | MATCH | 0.0099 | 0.0499 |
| acct#eea1157e | 2023-07 | neither | other:sweep_trade_day | -0.02 | MATCH | DIFF | MATCH | MATCH | -0.025 | -0.005 |
| acct#eea1157e | 2024-09 | neither | other:sweep_trade_day | 0.13 | MATCH | DIFF | MATCH | MATCH | 0.153 | 0.023 |
| acct#04ebe1d1 | 2024-05 | neither | other:sweep_trade_day | 0.67 | MATCH | DIFF | MATCH | MATCH | 0.6889 | 0.0189 |
| acct#015306a0 | 2023-04 | neither | other:sweep_trade_day | 1.23 | MATCH | DIFF | DIFF | DIFF | 1.1702 | -0.0598 |
| acct#fa488a0b | 2023-04 | neither | other:sweep_trade_day | 1.0 | MATCH | DIFF | MATCH | MATCH | 1.0304 | 0.0304 |
| acct#fa488a0b | 2023-07 | neither | other:sweep_trade_day | 2.9 | MATCH | DIFF | DIFF | DIFF | 2.9899 | 0.0899 |
| acct#fa488a0b | 2024-01 | neither | other:sweep_trade_day | -0.95 | MATCH | DIFF | MATCH | MATCH | -0.9242 | 0.0258 |
| acct#21515eb6 | 2025-04 | neither | other:sweep_trade_day | 0.53 | MATCH | DIFF | MATCH | MATCH | 0.5019 | -0.0281 |
| acct#2d4385bf | 2023-04 | neither | other:sweep_trade_day | -1.04 | MATCH | DIFF | MATCH | MATCH | -1.068 | -0.028 |
| acct#92164e0d | 2017-03 | neither | other:sweep_trade_day | -0.09 | MATCH | DIFF | MATCH | MATCH | -0.0908 | -0.0008 |
| acct#ebb31a1c | 2017-03 | neither | other:sweep_trade_day | -0.09 | MATCH | DIFF | MATCH | MATCH | -0.0929 | -0.0029 |
| acct#dfa7a25c | 2017-06 | neither | other:sweep_trade_day | -0.1 | MATCH | DIFF | MATCH | MATCH | -0.102 | -0.002 |
| acct#4040a6ea | 2017-09 | neither | other:sweep_trade_day | -0.07 | MATCH | DIFF | MATCH | MATCH | -0.0743 | -0.0043 |
| acct#0e2c97b9 | 2018-07 | neither | other:sweep_trade_day | -0.08 | MATCH | DIFF | MATCH | MATCH | -0.0808 | -0.0008 |
| acct#de79caf1 | 2018-07 | neither | other:sweep_trade_day | -0.08 | MATCH | DIFF | MATCH | MATCH | -0.0808 | -0.0008 |
| acct#25880078 | 2021-07 | neither | other:sweep_trade_day | -0.04 | MATCH | DIFF | DIFF | DIFF | -0.1154 | -0.0754 |
| acct#25880078 | 2022-01 | neither | other:sweep_trade_day | -9.71 | MATCH | DIFF | DIFF | DIFF | -9.8401 | -0.1301 |
| acct#25880078 | 2023-04 | neither | other:sweep_trade_day | 0.65 | MATCH | DIFF | DIFF | DIFF | 0.5451 | -0.1049 |
| acct#8680d8f4 | 2018-06 | neither | other:sweep_trade_day | -0.08 | MATCH | DIFF | MATCH | MATCH | -0.0813 | -0.0013 |
| acct#e29efebe | 2020-10 | neither | other:sweep_trade_day | -4.06 | MATCH | DIFF | MATCH | MATCH | -4.07 | -0.01 |
| acct#e29efebe | 2020-12 | neither | other:sweep_trade_day | 4.15 | MATCH | DIFF | MATCH | MATCH | 4.1661 | 0.0161 |
| acct#e29efebe | 2021-01 | neither | other:sweep_trade_day | 3.93 | MATCH | DIFF | MATCH | MATCH | 3.9179 | -0.0121 |
| acct#e29efebe | 2021-03 | neither | other:sweep_trade_day | 1.7 | MATCH | DIFF | MATCH | MATCH | 1.7085 | 0.0085 |
| acct#e29efebe | 2021-09 | neither | other:sweep_trade_day | -6.42 | MATCH | DIFF | MATCH | MATCH | -6.4083 | 0.0117 |
| acct#e29efebe | 2021-12 | neither | other:sweep_trade_day | 1.91 | MATCH | DIFF | MATCH | MATCH | 1.9212 | 0.0112 |
| acct#e29efebe | 2022-03 | neither | other:sweep_trade_day | 3.37 | MATCH | DIFF | MATCH | MATCH | 3.381 | 0.011 |
| acct#e29efebe | 2022-06 | neither | other:sweep_trade_day | -5.26 | MATCH | DIFF | MATCH | MATCH | -5.2513 | 0.0087 |
| acct#e29efebe | 2022-12 | neither | other:sweep_trade_day | -5.66 | MATCH | DIFF | MATCH | MATCH | -5.6507 | 0.0093 |
| acct#e29efebe | 2023-12 | neither | other:sweep_trade_day | -0.55 | MATCH | DIFF | MATCH | MATCH | -0.546 | 0.004 |
| acct#e29efebe | 2024-12 | neither | other:sweep_trade_day | -0.26 | MATCH | DIFF | MATCH | MATCH | -0.2583 | 0.0017 |
| acct#79d02c2c | 2024-07 | neither | other:sweep_trade_day | 1.94 | MATCH | DIFF | DIFF | DIFF | 2.1112 | 0.1712 |
| acct#4a890dd1 | 2024-07 | neither | other:sweep_trade_day | 1.94 | MATCH | DIFF | DIFF | DIFF | 2.1159 | 0.1759 |
| acct#3b89d062 | 2022-07 | neither | other:sweep_trade_day | -0.08 | MATCH | DIFF | MATCH | MATCH | -0.0821 | -0.0021 |
| acct#3b89d062 | 2022-10 | neither | other:sweep_trade_day | -0.07 | MATCH | DIFF | MATCH | MATCH | -0.0729 | -0.0029 |
| acct#6acbfb93 | 2021-06 | neither | other:sweep_trade_day | -0.09 | MATCH | DIFF | MATCH | MATCH | -0.0936 | -0.0036 |
| acct#921b5169 | 2022-04 | neither | other:sweep_trade_day | -0.06 | MATCH | DIFF | MATCH | MATCH | -0.0609 | -0.0009 |
| acct#921b5169 | 2022-07 | neither | other:sweep_trade_day | -0.05 | MATCH | DIFF | MATCH | MATCH | -0.05 | 0.0 |
| acct#921b5169 | 2023-04 | neither | other:sweep_trade_day | -0.0 | MATCH | DIFF | MATCH | MATCH | -0.0004 | -0.0004 |
| acct#921b5169 | 2023-10 | neither | other:sweep_trade_day | -0.0 | MATCH | DIFF | MATCH | MATCH | -0.0022 | -0.0022 |
| acct#921b5169 | 2024-01 | neither | other:sweep_trade_day | -0.0 | MATCH | DIFF | MATCH | MATCH | -0.0004 | -0.0004 |
| acct#921b5169 | 2024-04 | neither | other:sweep_trade_day | -0.01 | MATCH | DIFF | MATCH | MATCH | -0.0103 | -0.0003 |
| acct#921b5169 | 2024-07 | neither | other:sweep_trade_day | -0.01 | MATCH | DIFF | MATCH | MATCH | -0.0103 | -0.0003 |
| acct#921b5169 | 2024-10 | neither | other:sweep_trade_day | -0.01 | MATCH | DIFF | MATCH | MATCH | -0.0117 | -0.0017 |
| acct#921b5169 | 2025-01 | neither | other:sweep_trade_day | -0.04 | MATCH | DIFF | MATCH | MATCH | -0.0359 | 0.0041 |
| acct#921b5169 | 2025-04 | neither | other:sweep_trade_day | -0.06 | MATCH | DIFF | MATCH | MATCH | -0.0593 | 0.0007 |
| acct#3345c43a | 2023-01 | neither | other:sweep_trade_day | -0.06 | MATCH | DIFF | MATCH | MATCH | -0.058 | 0.002 |
| acct#3345c43a | 2023-04 | neither | other:sweep_trade_day | -0.06 | MATCH | DIFF | MATCH | MATCH | -0.056 | 0.004 |
| acct#3345c43a | 2023-07 | neither | other:sweep_trade_day | -0.07 | MATCH | DIFF | MATCH | MATCH | -0.0731 | -0.0031 |
| acct#3345c43a | 2023-10 | neither | other:sweep_trade_day | -0.09 | MATCH | DIFF | MATCH | MATCH | -0.0854 | 0.0046 |
| acct#1f02bee1 | 2022-10 | neither | other:sweep_trade_day | 11.87 | MATCH | DIFF | MATCH | MATCH | 11.8922 | 0.0222 |
| acct#16f4eae3 | 2025-01 | neither | other:sweep_trade_day | 0.92 | MATCH | DIFF | MATCH | MATCH | 0.9333 | 0.0133 |
| acct#16f4eae3 | 2026-01 | neither | other:sweep_trade_day | 1.68 | MATCH | DIFF | MATCH | MATCH | 1.6914 | 0.0114 |
| acct#0f2d2c45 | 2024-01 | neither | other:sweep_trade_day | -0.3 | MATCH | DIFF | MATCH | MATCH | -0.2854 | 0.0146 |
| acct#cce589ab | 2024-01 | neither | other:sweep_trade_day | -0.3 | MATCH | DIFF | MATCH | MATCH | -0.2843 | 0.0157 |
| acct#cce589ab | 2024-10 | neither | other:sweep_trade_day | -1.6 | MATCH | DIFF | MATCH | MATCH | -1.5803 | 0.0197 |
| acct#cce589ab | 2025-04 | neither | other:sweep_trade_day | -0.05 | MATCH | DIFF | MATCH | MATCH | -0.051 | -0.001 |
| acct#cce589ab | 2025-07 | neither | other:sweep_trade_day | 1.24 | MATCH | DIFF | MATCH | MATCH | 1.2482 | 0.0082 |
| acct#cce589ab | 2025-10 | neither | other:sweep_trade_day | 1.44 | MATCH | DIFF | MATCH | MATCH | 1.4418 | 0.0018 |
| acct#cce589ab | 2026-01 | neither | other:sweep_trade_day | 1.76 | MATCH | DIFF | MATCH | MATCH | 1.7554 | -0.0046 |
| acct#a011b5f7 | 2025-04 | neither | other:sweep_trade_day | 0.41 | MATCH | DIFF | MATCH | MATCH | 0.4142 | 0.0042 |
| acct#a011b5f7 | 2025-10 | neither | other:sweep_trade_day | 0.64 | MATCH | DIFF | MATCH | MATCH | 0.6039 | -0.0361 |
| acct#a011b5f7 | 2026-01 | neither | other:sweep_trade_day | 1.56 | MATCH | DIFF | MATCH | MATCH | 1.5628 | 0.0028 |
| acct#cf292cea | 2024-07 | neither | other:sweep_trade_day | -7.76 | MATCH | DIFF | MATCH | MATCH | -7.7261 | 0.0339 |
| acct#cf292cea | 2024-10 | neither | other:sweep_trade_day | -9.03 | MATCH | DIFF | MATCH | MATCH | -8.9903 | 0.0397 |
| acct#65b3b3ea | 2024-12 | neither | other:sweep_trade_day | -8.02 | MATCH | DIFF | MATCH | MATCH | -7.9838 | 0.0362 |
| acct#65b3b3ea | 2025-03 | neither | other:sweep_trade_day | 7.66 | MATCH | DIFF | MATCH | MATCH | 7.684 | 0.024 |
| acct#65b3b3ea | 2025-06 | neither | other:sweep_trade_day | 6.23 | MATCH | DIFF | MATCH | MATCH | 6.2553 | 0.0253 |
| acct#65b3b3ea | 2025-09 | neither | other:sweep_trade_day | -0.47 | MATCH | DIFF | MATCH | MATCH | -0.4562 | 0.0138 |
| acct#65b3b3ea | 2025-12 | neither | other:sweep_trade_day | 4.56 | MATCH | DIFF | MATCH | MATCH | 4.5619 | 0.0019 |
| acct#65b3b3ea | 2026-03 | neither | other:sweep_trade_day | 11.58 | MATCH | DIFF | MATCH | MATCH | 11.5754 | -0.0046 |
| acct#ed5f47fe | 2026-01 | neither | other:sweep_trade_day | 2.76 | MATCH | DIFF | MATCH | MATCH | 2.7603 | 0.0003 |
| acct#aaeb760c | 2021-10 | neither | sweep_balance | 5.51 | MATCH | DIFF | DIFF | DIFF | 5.3811 | -0.1289 |
| acct#aaeb760c | 2022-03 | neither | sweep_balance | 4.82 | MATCH | DIFF | DIFF | DIFF | 4.6996 | -0.1204 |
| acct#aaeb760c | 2023-12 | neither | sweep_balance | 1.56 | MATCH | DIFF | MATCH | MATCH | 1.5676 | 0.0076 |
| acct#b4db1f25 | 2020-01 | neither | sweep_balance | 0.02 | MATCH | DIFF | MATCH | MATCH | 0.0212 | 0.0012 |
| acct#b4db1f25 | 2020-02 | neither | sweep_balance | 0.02 | MATCH | DIFF | MATCH | MATCH | 0.0199 | -0.0001 |
| acct#03836058 | 2022-04 | neither | sweep_balance | -1.41 | MATCH | DIFF | DIFF | DIFF | -1.1928 | 0.2172 |
| acct#eea1157e | 2021-05 | neither | sweep_balance | 0.76 | MATCH | DIFF | DIFF | DIFF | 1.1828 | 0.4228 |
| acct#eea1157e | 2025-08 | neither | sweep_balance | 1.22 | MATCH | DIFF | DIFF | DIFF | 1.6857 | 0.4657 |
| acct#1c3da532 | 2017-08 | neither | sweep_balance | 0.0 | MATCH | DIFF | MATCH | MATCH | 0.0042 | 0.0042 |
| acct#1c3da532 | 2017-10 | neither | sweep_balance | 0.0 | MATCH | DIFF | MATCH | MATCH | 0.0042 | 0.0042 |
| acct#1c3da532 | 2017-12 | neither | sweep_balance | 0.0 | MATCH | DIFF | MATCH | MATCH | 0.0042 | 0.0042 |
| acct#1c3da532 | 2018-01 | neither | sweep_balance | 0.01 | MATCH | DIFF | MATCH | MATCH | 0.0122 | 0.0022 |
| acct#1c3da532 | 2018-02 | neither | sweep_balance | 0.01 | MATCH | DIFF | MATCH | MATCH | 0.0115 | 0.0015 |
| acct#1c3da532 | 2018-03 | neither | sweep_balance | 0.01 | MATCH | DIFF | MATCH | MATCH | 0.0141 | 0.0041 |
| acct#5aa91f68 | 2017-07 | neither | sweep_balance | 0.0 | MATCH | DIFF | MATCH | MATCH | 0.002 | 0.002 |
| acct#5aa91f68 | 2017-08 | neither | sweep_balance | 0.0 | MATCH | DIFF | MATCH | MATCH | 0.0042 | 0.0042 |
| acct#5aa91f68 | 2017-09 | neither | sweep_balance | 0.0 | MATCH | DIFF | MATCH | MATCH | 0.004 | 0.004 |
| acct#5aa91f68 | 2017-10 | neither | sweep_balance | 0.0 | MATCH | DIFF | MATCH | MATCH | 0.0042 | 0.0042 |
| acct#5aa91f68 | 2017-12 | neither | sweep_balance | 0.0 | MATCH | DIFF | MATCH | MATCH | 0.0042 | 0.0042 |
| acct#5aa91f68 | 2018-01 | neither | sweep_balance | 0.01 | MATCH | DIFF | MATCH | MATCH | 0.0121 | 0.0021 |
| acct#5aa91f68 | 2018-02 | neither | sweep_balance | 0.01 | MATCH | DIFF | MATCH | MATCH | 0.0115 | 0.0015 |
| acct#5aa91f68 | 2018-03 | neither | sweep_balance | 0.01 | MATCH | DIFF | MATCH | MATCH | 0.014 | 0.004 |
| acct#5aa91f68 | 2018-04 | neither | sweep_balance | 0.02 | MATCH | DIFF | MATCH | MATCH | 0.0205 | 0.0005 |
| acct#5aa91f68 | 2018-05 | neither | sweep_balance | 0.02 | MATCH | DIFF | MATCH | MATCH | 0.0212 | 0.0012 |
| acct#5aa91f68 | 2018-06 | neither | sweep_balance | 0.02 | MATCH | DIFF | MATCH | MATCH | 0.0205 | 0.0005 |
| acct#04ebe1d1 | 2021-04 | neither | sweep_balance | -3.41 | MATCH | DIFF | DIFF | DIFF | -3.5078 | -0.0978 |
| acct#04ebe1d1 | 2021-06 | neither | sweep_balance | -4.82 | MATCH | DIFF | DIFF | DIFF | -4.9435 | -0.1235 |
| acct#04ebe1d1 | 2021-10 | neither | sweep_balance | -1.39 | MATCH | DIFF | DIFF | DIFF | -1.4589 | -0.0689 |
| acct#fa488a0b | 2021-04 | neither | sweep_balance | 2.21 | MATCH | DIFF | DIFF | DIFF | 2.3118 | 0.1018 |
| acct#fa488a0b | 2021-08 | neither | sweep_balance | 1.0 | MATCH | DIFF | DIFF | DIFF | 1.076 | 0.076 |
| acct#fa488a0b | 2021-10 | neither | sweep_balance | 2.52 | MATCH | DIFF | DIFF | DIFF | 2.6146 | 0.0946 |
| acct#21515eb6 | 2025-05 | neither | sweep_balance | 8.21 | MATCH | DIFF | MATCH | MATCH | 8.2042 | -0.0058 |
| acct#2d4385bf | 2022-03 | neither | sweep_balance | 4.92 | MATCH | DIFF | DIFF | DIFF | 5.0504 | 0.1304 |
| acct#ab0c6781 | 2018-01 | neither | sweep_balance | 0.18 | MATCH | DIFF | MATCH | MATCH | 0.1814 | 0.0014 |
| acct#ab0c6781 | 2018-02 | neither | sweep_balance | 0.01 | MATCH | DIFF | MATCH | MATCH | 0.0115 | 0.0015 |
| acct#ab0c6781 | 2018-03 | neither | sweep_balance | 0.01 | MATCH | DIFF | MATCH | MATCH | 0.0141 | 0.0041 |
| acct#e29efebe | 2023-04 | neither | sweep_balance | 6.46 | MATCH | DIFF | MATCH | MATCH | 6.4603 | 0.0003 |
| acct#e29efebe | 2024-02 | neither | sweep_balance | 3.97 | MATCH | DIFF | DIFF | DIFF | 4.1591 | 0.1891 |
| acct#79d02c2c | 2023-05 | neither | sweep_balance | 0.1 | MATCH | DIFF | MATCH | MATCH | 0.1418 | 0.0418 |
| acct#79d02c2c | 2024-11 | neither | sweep_balance | 5.35 | MATCH | DIFF | DIFF | DIFF | 5.4413 | 0.0913 |
| acct#79d02c2c | 2025-01 | neither | sweep_balance | 2.21 | MATCH | DIFF | MATCH | MATCH | 2.2206 | 0.0106 |
| acct#4a890dd1 | 2023-05 | neither | sweep_balance | 0.11 | MATCH | DIFF | MATCH | MATCH | 0.1493 | 0.0393 |
| acct#4a890dd1 | 2025-01 | neither | sweep_balance | 2.23 | MATCH | DIFF | MATCH | MATCH | 2.2339 | 0.0039 |
| acct#4a890dd1 | 2025-05 | neither | sweep_balance | 4.83 | MATCH | DIFF | DIFF | DIFF | 4.9152 | 0.0852 |
| acct#3b89d062 | 2022-11 | neither | sweep_balance | 0.03 | MATCH | DIFF | MATCH | MATCH | 0.0348 | 0.0048 |
| acct#3b89d062 | 2022-12 | neither | sweep_balance | 0.06 | MATCH | DIFF | MATCH | MATCH | 0.0637 | 0.0037 |
| acct#3b89d062 | 2023-01 | neither | sweep_balance | -0.04 | MATCH | DIFF | MATCH | MATCH | -0.0364 | 0.0036 |
| acct#3b89d062 | 2023-02 | neither | sweep_balance | 0.06 | MATCH | DIFF | MATCH | MATCH | 0.0575 | -0.0025 |
| acct#921b5169 | 2023-07 | neither | sweep_balance | 0.0 | MATCH | DIFF | MATCH | MATCH | 0.0013 | 0.0013 |
| acct#1f02bee1 | 2022-11 | neither | sweep_balance | 18.29 | MATCH | DIFF | MATCH | MATCH | 18.2894 | -0.0006 |
| acct#cce589ab | 2024-02 | neither | sweep_balance | 4.32 | MATCH | DIFF | MATCH | MATCH | 4.3367 | 0.0167 |
| acct#cce589ab | 2024-04 | neither | sweep_balance | -3.96 | MATCH | DIFF | MATCH | MATCH | -3.974 | -0.014 |
| acct#cce589ab | 2024-08 | neither | sweep_balance | 1.79 | MATCH | DIFF | MATCH | MATCH | 1.7854 | -0.0046 |
| acct#cce589ab | 2024-11 | neither | sweep_balance | 5.25 | MATCH | DIFF | MATCH | MATCH | 5.2837 | 0.0337 |
| acct#cce589ab | 2025-01 | neither | sweep_balance | 2.52 | MATCH | DIFF | MATCH | MATCH | 2.5101 | -0.0099 |
| acct#cce589ab | 2025-02 | neither | sweep_balance | -1.55 | MATCH | DIFF | MATCH | MATCH | -1.5729 | -0.0229 |
| acct#cce589ab | 2025-08 | neither | sweep_balance | 2.52 | MATCH | DIFF | MATCH | MATCH | 2.5124 | -0.0076 |
| D49141608 | 2019-02 | neither | sweep_balance | 0.04 | MATCH | DIFF | MATCH | MATCH | 0.0419 | 0.0019 |
| D49141608 | 2019-03 | neither | sweep_balance | 0.05 | MATCH | DIFF | MATCH | MATCH | 0.0466 | -0.0034 |
| D49141608 | 2019-04 | neither | sweep_balance | 0.05 | MATCH | DIFF | MATCH | MATCH | 0.0452 | -0.0048 |
| D49141608 | 2019-05 | neither | sweep_balance | 0.05 | MATCH | DIFF | MATCH | MATCH | 0.0465 | -0.0035 |
| D49141608 | 2019-06 | neither | sweep_balance | 0.05 | MATCH | DIFF | MATCH | MATCH | 0.0451 | -0.0049 |
| D49141608 | 2019-07 | neither | sweep_balance | 0.05 | MATCH | DIFF | MATCH | MATCH | 0.0465 | -0.0035 |
| D49141608 | 2019-08 | neither | sweep_balance | 0.04 | MATCH | DIFF | MATCH | MATCH | 0.0381 | -0.0019 |
| D49141608 | 2019-09 | neither | sweep_balance | 0.03 | MATCH | DIFF | MATCH | MATCH | 0.0321 | 0.0021 |
| D49141714 | 2019-02 | neither | sweep_balance | 0.04 | MATCH | DIFF | MATCH | MATCH | 0.0421 | 0.0021 |
| acct#cf292cea | 2024-08 | neither | sweep_balance | 4.62 | MATCH | DIFF | MATCH | MATCH | 4.6488 | 0.0288 |
| acct#65b3b3ea | 2025-04 | neither | sweep_balance | -11.06 | MATCH | DIFF | MATCH | MATCH | -11.0556 | 0.0044 |
| acct#65b3b3ea | 2025-07 | neither | sweep_balance | 3.42 | MATCH | DIFF | MATCH | MATCH | 3.4191 | -0.0009 |
| acct#65b3b3ea | 2025-10 | neither | sweep_balance | 1.33 | MATCH | DIFF | MATCH | MATCH | 1.3311 | 0.0011 |
| acct#65b3b3ea | 2026-01 | neither | sweep_balance | 16.79 | MATCH | DIFF | MATCH | MATCH | 16.7871 | -0.0029 |
| acct#65b3b3ea | 2026-04 | neither | sweep_balance | -8.79 | MATCH | DIFF | MATCH | MATCH | -8.7931 | -0.0031 |

### Movers left not MATCH in the AFTER arm, each named: 25 (DIFF 25; other 0) (never forced)

| account | month | class | cause | AFTER verdict | computed | reported |
|---|---|---|---|---|---|---|
| acct#f6c79f45 | 2024-06 | core | other:sweep_trade_day | DIFF | -0.8239 | -0.88 |
| D49143350 | 2026-02 | core | other:sweep_trade_day | DIFF | 2.4881 | 2.05 |
| D49143350 | 2023-11 | core | sweep_balance | DIFF | -3.4367 | -4.59 |
| acct#015306a0 | 2023-04 | neither | other:sweep_trade_day | DIFF | 1.1702 | 1.23 |
| acct#fa488a0b | 2023-07 | neither | other:sweep_trade_day | DIFF | 2.9899 | 2.9 |
| acct#25880078 | 2021-07 | neither | other:sweep_trade_day | DIFF | -0.1154 | -0.04 |
| acct#25880078 | 2022-01 | neither | other:sweep_trade_day | DIFF | -9.8401 | -9.71 |
| acct#25880078 | 2023-04 | neither | other:sweep_trade_day | DIFF | 0.5451 | 0.65 |
| acct#79d02c2c | 2024-07 | neither | other:sweep_trade_day | DIFF | 2.1112 | 1.94 |
| acct#4a890dd1 | 2024-07 | neither | other:sweep_trade_day | DIFF | 2.1159 | 1.94 |
| acct#aaeb760c | 2021-10 | neither | sweep_balance | DIFF | 5.3811 | 5.51 |
| acct#aaeb760c | 2022-03 | neither | sweep_balance | DIFF | 4.6996 | 4.82 |
| acct#03836058 | 2022-04 | neither | sweep_balance | DIFF | -1.1928 | -1.41 |
| acct#eea1157e | 2021-05 | neither | sweep_balance | DIFF | 1.1828 | 0.76 |
| acct#eea1157e | 2025-08 | neither | sweep_balance | DIFF | 1.6857 | 1.22 |
| acct#04ebe1d1 | 2021-04 | neither | sweep_balance | DIFF | -3.5078 | -3.41 |
| acct#04ebe1d1 | 2021-06 | neither | sweep_balance | DIFF | -4.9435 | -4.82 |
| acct#04ebe1d1 | 2021-10 | neither | sweep_balance | DIFF | -1.4589 | -1.39 |
| acct#fa488a0b | 2021-04 | neither | sweep_balance | DIFF | 2.3118 | 2.21 |
| acct#fa488a0b | 2021-08 | neither | sweep_balance | DIFF | 1.076 | 1.0 |
| acct#fa488a0b | 2021-10 | neither | sweep_balance | DIFF | 2.6146 | 2.52 |
| acct#2d4385bf | 2022-03 | neither | sweep_balance | DIFF | 5.0504 | 4.92 |
| acct#e29efebe | 2024-02 | neither | sweep_balance | DIFF | 4.1591 | 3.97 |
| acct#79d02c2c | 2024-11 | neither | sweep_balance | DIFF | 5.4413 | 5.35 |
| acct#4a890dd1 | 2025-05 | neither | sweep_balance | DIFF | 4.9152 | 4.83 |


## Round 22's 23 regressions (MATCH under r19, DIFF under repaired), classed, and their result in this re-grade

Read from 0.9.0_WK_ADVI_COTBKF~43 (r19 -> repaired). Each is classed by what the conditional rule does to its credit days (first class that applies): `double_credit` = a credit day dropped by (b), a credit-signed CFNCASH row of the same account-day equals the sale proceeds within 0.01; `vendor_cfncash_leg_of_sweep_sale` = a day dropped by (c), a CFNCASH row of any type equals a same-day listed-sweep sale; `unvalued_funding_sale` = a day blanked by (a'), a sold security was not held and priced the trading day before (the day's return is blank, the month UNGRADABLE); `other:<name>` = none of these. Counts: other:credit_kept_by_every_condition=1, unvalued_funding_sale=9, vendor_cfncash_leg_of_sweep_sale=13; total 23.

Under this arm: 23 of 23 are MATCH, 0 are not.

| account | month | class | now | computed | reported | credit days up to the month (day, credited, kept, CFNCASH rows that day, reason dropped or cut) |
|---|---|---|---|---|---|---|
| acct#c42b98c0 | 2025-05 | unvalued_funding_sale | MATCH | 0.3188 | 0.32 | 2017-08-04 25000.0 dropped [none] {unvalued_funding_sale_25000.0} / 2024-03-07 90000.0 dropped [none] {unvalued_funding_sale_90000.0} / 2025-04-07 100000.0 dropped [none] {unvalued_funding_sale_100000.0} |
| acct#c42b98c0 | 2025-06 | unvalued_funding_sale | MATCH | 0.307 | 0.31 | 2017-08-04 25000.0 dropped [none] {unvalued_funding_sale_25000.0} / 2024-03-07 90000.0 dropped [none] {unvalued_funding_sale_90000.0} / 2025-04-07 100000.0 dropped [none] {unvalued_funding_sale_100000.0} |
| acct#c42b98c0 | 2025-07 | unvalued_funding_sale | MATCH | 0.3187 | 0.32 | 2017-08-04 25000.0 dropped [none] {unvalued_funding_sale_25000.0} / 2024-03-07 90000.0 dropped [none] {unvalued_funding_sale_90000.0} / 2025-04-07 100000.0 dropped [none] {unvalued_funding_sale_100000.0} |
| acct#c42b98c0 | 2025-08 | unvalued_funding_sale | MATCH | 0.3182 | 0.32 | 2017-08-04 25000.0 dropped [none] {unvalued_funding_sale_25000.0} / 2024-03-07 90000.0 dropped [none] {unvalued_funding_sale_90000.0} / 2025-04-07 100000.0 dropped [none] {unvalued_funding_sale_100000.0} |
| acct#c42b98c0 | 2025-09 | unvalued_funding_sale | MATCH | 0.3008 | 0.3 | 2017-08-04 25000.0 dropped [none] {unvalued_funding_sale_25000.0} / 2024-03-07 90000.0 dropped [none] {unvalued_funding_sale_90000.0} / 2025-04-07 100000.0 dropped [none] {unvalued_funding_sale_100000.0} |
| acct#c42b98c0 | 2025-10 | unvalued_funding_sale | MATCH | 0.3016 | 0.3 | 2017-08-04 25000.0 dropped [none] {unvalued_funding_sale_25000.0} / 2024-03-07 90000.0 dropped [none] {unvalued_funding_sale_90000.0} / 2025-04-07 100000.0 dropped [none] {unvalued_funding_sale_100000.0} |
| acct#05dd4a9d | 2023-05 | vendor_cfncash_leg_of_sweep_sale | MATCH | 0.074 | 0.07 | 2021-07-16 13000.0 dropped [lo 12788.22] {vendor_leg_of_sweep_sale} / 2021-07-20 10000.0 dropped [lo 10000.0] {vendor_leg_of_sweep_sale} / 2022-07-18 9678.95 dropped [lo 7034.39] {vendor_leg_of_sweep_sale} |
| acct#05dd4a9d | 2023-06 | vendor_cfncash_leg_of_sweep_sale | MATCH | 0.076 | 0.08 | 2021-07-16 13000.0 dropped [lo 12788.22] {vendor_leg_of_sweep_sale} / 2021-07-20 10000.0 dropped [lo 10000.0] {vendor_leg_of_sweep_sale} / 2022-07-18 9678.95 dropped [lo 7034.39] {vendor_leg_of_sweep_sale} |
| acct#05dd4a9d | 2023-08 | vendor_cfncash_leg_of_sweep_sale | MATCH | 0.0608 | 0.06 | 2021-07-16 13000.0 dropped [lo 12788.22] {vendor_leg_of_sweep_sale} / 2021-07-20 10000.0 dropped [lo 10000.0] {vendor_leg_of_sweep_sale} / 2022-07-18 9678.95 dropped [lo 7034.39] {vendor_leg_of_sweep_sale} |
| acct#05dd4a9d | 2023-09 | vendor_cfncash_leg_of_sweep_sale | MATCH | 0.0608 | 0.06 | 2021-07-16 13000.0 dropped [lo 12788.22] {vendor_leg_of_sweep_sale} / 2021-07-20 10000.0 dropped [lo 10000.0] {vendor_leg_of_sweep_sale} / 2022-07-18 9678.95 dropped [lo 7034.39] {vendor_leg_of_sweep_sale} |
| acct#05dd4a9d | 2023-11 | vendor_cfncash_leg_of_sweep_sale | MATCH | 0.0609 | 0.06 | 2021-07-16 13000.0 dropped [lo 12788.22] {vendor_leg_of_sweep_sale} / 2021-07-20 10000.0 dropped [lo 10000.0] {vendor_leg_of_sweep_sale} / 2022-07-18 9678.95 dropped [lo 7034.39] {vendor_leg_of_sweep_sale} |
| acct#05dd4a9d | 2023-12 | vendor_cfncash_leg_of_sweep_sale | MATCH | 0.0609 | 0.06 | 2021-07-16 13000.0 dropped [lo 12788.22] {vendor_leg_of_sweep_sale} / 2021-07-20 10000.0 dropped [lo 10000.0] {vendor_leg_of_sweep_sale} / 2022-07-18 9678.95 dropped [lo 7034.39] {vendor_leg_of_sweep_sale} |
| acct#05dd4a9d | 2024-02 | vendor_cfncash_leg_of_sweep_sale | MATCH | 0.0581 | 0.06 | 2021-07-16 13000.0 dropped [lo 12788.22] {vendor_leg_of_sweep_sale} / 2021-07-20 10000.0 dropped [lo 10000.0] {vendor_leg_of_sweep_sale} / 2022-07-18 9678.95 dropped [lo 7034.39] {vendor_leg_of_sweep_sale} |
| acct#05dd4a9d | 2024-03 | vendor_cfncash_leg_of_sweep_sale | MATCH | 0.0609 | 0.06 | 2021-07-16 13000.0 dropped [lo 12788.22] {vendor_leg_of_sweep_sale} / 2021-07-20 10000.0 dropped [lo 10000.0] {vendor_leg_of_sweep_sale} / 2022-07-18 9678.95 dropped [lo 7034.39] {vendor_leg_of_sweep_sale} |
| acct#05dd4a9d | 2024-05 | vendor_cfncash_leg_of_sweep_sale | MATCH | 0.061 | 0.06 | 2021-07-16 13000.0 dropped [lo 12788.22] {vendor_leg_of_sweep_sale} / 2021-07-20 10000.0 dropped [lo 10000.0] {vendor_leg_of_sweep_sale} / 2022-07-18 9678.95 dropped [lo 7034.39] {vendor_leg_of_sweep_sale} |
| acct#05dd4a9d | 2024-06 | vendor_cfncash_leg_of_sweep_sale | MATCH | 0.0581 | 0.06 | 2021-07-16 13000.0 dropped [lo 12788.22] {vendor_leg_of_sweep_sale} / 2021-07-20 10000.0 dropped [lo 10000.0] {vendor_leg_of_sweep_sale} / 2022-07-18 9678.95 dropped [lo 7034.39] {vendor_leg_of_sweep_sale} |
| acct#05dd4a9d | 2024-08 | vendor_cfncash_leg_of_sweep_sale | MATCH | 0.0611 | 0.06 | 2021-07-16 13000.0 dropped [lo 12788.22] {vendor_leg_of_sweep_sale} / 2021-07-20 10000.0 dropped [lo 10000.0] {vendor_leg_of_sweep_sale} / 2022-07-18 9678.95 dropped [lo 7034.39] {vendor_leg_of_sweep_sale} |
| acct#05dd4a9d | 2024-09 | vendor_cfncash_leg_of_sweep_sale | MATCH | 0.061 | 0.06 | 2021-07-16 13000.0 dropped [lo 12788.22] {vendor_leg_of_sweep_sale} / 2021-07-20 10000.0 dropped [lo 10000.0] {vendor_leg_of_sweep_sale} / 2022-07-18 9678.95 dropped [lo 7034.39] {vendor_leg_of_sweep_sale} |
| acct#05dd4a9d | 2024-11 | vendor_cfncash_leg_of_sweep_sale | MATCH | 0.0582 | 0.06 | 2021-07-16 13000.0 dropped [lo 12788.22] {vendor_leg_of_sweep_sale} / 2021-07-20 10000.0 dropped [lo 10000.0] {vendor_leg_of_sweep_sale} / 2022-07-18 9678.95 dropped [lo 7034.39] {vendor_leg_of_sweep_sale} |
| acct#c093546d | 2023-10 | unvalued_funding_sale | MATCH | 0.0669 | 0.07 | 2019-03-19 20000.0 dropped [none] {unvalued_funding_sale_20000.0} / 2019-07-08 6000.0 dropped [none] {unvalued_funding_sale_6000.0} / 2020-03-13 25000.0 dropped [none] {unvalued_funding_sale_25000.0} / 2020-08-13 70627.31 dropped [none] {unvalued_funding_sale_70627.31} |
| acct#57e741a5 | 2025-07 | other:credit_kept_by_every_condition | MATCH | 0.1182 | 0.12 | 2025-03-28 4871.6 kept [none] / 2025-04-29 4711.88 kept [none] / 2025-05-28 1514.07 kept [none] / 2025-06-27 778.15 kept [none] |
| acct#99b947c2 | 2025-01 | unvalued_funding_sale | MATCH | 0.2212 | 0.22 | 2023-09-28 75000.0 dropped [none] {unvalued_funding_sale_75000.0} / 2024-04-18 78000.0 dropped [none] {unvalued_funding_sale_78000.0} / 2024-10-10 80000.0 dropped [none] {unvalued_funding_sale_80000.0} |
| acct#62a9544e | 2025-01 | unvalued_funding_sale | MATCH | 0.2212 | 0.22 | 2023-09-28 75000.0 dropped [none] {unvalued_funding_sale_75000.0} / 2024-04-18 78000.0 dropped [none] {unvalued_funding_sale_78000.0} / 2024-10-10 80000.0 dropped [none] {unvalued_funding_sale_80000.0} |

### Round 22's 25 recovered movers (round-19 movers MATCH under repaired): still MATCH under this arm: 25 of 25

Lost: none

By new verdict: MATCH=25, DIFF=0, UNGRADABLE=0, ABSENT=0

| account | month | new verdict |
|---|---|---|
| acct#5aa91f68 | 2017-07 | MATCH |
| acct#5aa91f68 | 2017-08 | MATCH |
| acct#5aa91f68 | 2017-09 | MATCH |
| acct#5aa91f68 | 2017-10 | MATCH |
| acct#5aa91f68 | 2017-12 | MATCH |
| acct#5aa91f68 | 2018-01 | MATCH |
| acct#5aa91f68 | 2018-02 | MATCH |
| acct#5aa91f68 | 2018-03 | MATCH |
| acct#5aa91f68 | 2018-04 | MATCH |
| acct#5aa91f68 | 2018-05 | MATCH |
| acct#5aa91f68 | 2018-06 | MATCH |
| acct#ab0c6781 | 2018-01 | MATCH |
| acct#cce589ab | 2024-02 | MATCH |
| acct#cce589ab | 2024-08 | MATCH |
| acct#cce589ab | 2025-02 | MATCH |
| acct#cce589ab | 2025-08 | MATCH |
| D49141608 | 2019-02 | MATCH |
| D49141608 | 2019-03 | MATCH |
| D49141608 | 2019-04 | MATCH |
| D49141608 | 2019-05 | MATCH |
| D49141608 | 2019-06 | MATCH |
| D49141608 | 2019-07 | MATCH |
| D49141608 | 2019-08 | MATCH |
| D49141608 | 2019-09 | MATCH |
| D49141714 | 2019-02 | MATCH |


## The method, row type by row type (commonwealth_sweeps.CASH_POSTINGS / CFN_POSTINGS, commonwealth_flows.METHOD_*)

Source of the treatment: the CRO's table (RESEARCH_20261008_COMMONWEALTH_TWR_METHOD.md); the cash posting is the one the 2026-06-23 snapshot confirms. A type the table does not name keeps the default flow table. Of the 31 such types, 9 are fees, charges or taxes and are flagged UNLISTED CHARGE/TAX (ASF, bcf, cbf, fco, stp, term, ftax, stax, frntax); the rest are trades, cancels, corporate actions and in-kind moves. Under `method_r26` the nine carry the sourced treatment of the round-25 source table below; only ASF still has none.

| type | rows: security / CFNCASH / sweep | cash posting (security line) | cash posting (CFNCASH line) | return treatment |
|---|---|---|---|---|
| 12b1 | 0 / 1466 / 0 |  | Amount as delivered | income, inside the return |
| ASF | 0 / 6 / 0 |  | Amount as delivered | INTERNAL, inside the return (round 25: NO SOURCE: the description is 'ASF' and names no fee; its notes (a quarterly-period 'Fee Reversal' and 'Returned Payment') do not say whether it is an advisory fee (a drag) or another charge (a flow); stays INTERNAL) |
| BYX | 1 / 0 / 0 | +1 x abs(Amount) |  | not a fee, charge or income row the table covers: default kept (INTERNAL) |
| CAE | 7 / 0 / 0 | none (moves securities, not cash) |  | not a fee, charge or income row the table covers: default kept (INTERNAL) |
| CAF | 478 / 0 / 0 | none (moves securities, not cash) |  | not a fee, charge or income row the table covers: default kept (INTERNAL) |
| DVRX | 611 / 0 / 0 | + Amount |  | not a fee, charge or income row the table covers: default kept (INTERNAL) |
| DVX | 273 / 0 / 0 | - Amount |  | not a fee, charge or income row the table covers: default kept (INTERNAL) |
| INTX | 1 / 0 / 0 | - Amount |  | not a fee, charge or income row the table covers: default kept (INTERNAL) |
| LICASU | 17 / 0 / 0 | none (moves securities, not cash) |  | not a fee, charge or income row the table covers: default kept (INTERNAL) |
| LISU | 157 / 0 / 0 | none (moves securities, not cash) |  | EXTERNAL FLOW (default table, +1 x abs(Amount)) |
| LIX | 0 / 1 / 0 |  | -1 x abs(Amount) | EXTERNAL FLOW (default table, -1 x abs(Amount)) |
| LOX | 0 / 9 / 0 |  | +1 x abs(Amount) | EXTERNAL FLOW (default table, +1 x abs(Amount)) |
| ManAltF | 0 / 1012 / 0 |  | Amount as delivered | EXTERNAL FLOW = Amount as delivered |
| ManAltT | 0 / 1012 / 0 |  | none (fee owed here, paid elsewhere) | DRAG inside the return, not a flow; numerator takes the Amount (cash not debited) |
| ManCheck | 0 / 124 / 0 |  | none (fee owed here, paid elsewhere) | DRAG inside the return, not a flow; numerator takes the Amount (cash not debited) |
| QA | 383 / 0 / 0 | none (moves securities, not cash) |  | not a fee, charge or income row the table covers: default kept (INTERNAL) |
| TRCISU | 59 / 0 / 0 | none (moves securities, not cash) |  | EXTERNAL FLOW (default table, +1 x abs(Amount)) |
| TRFIR | 1107 / 0 / 0 | none (moves securities, not cash) |  | EXTERNAL FLOW (default table, +1 x abs(Amount)) |
| ac | 230 / 0 / 0 | + Amount |  | not a fee, charge or income row the table covers: default kept (INTERNAL) |
| acca | 195 / 0 / 0 | none (moves securities, not cash) |  | not a fee, charge or income row the table covers: default kept (INTERNAL) |
| accal | 178 / 0 / 0 | none (moves securities, not cash) |  | not a fee, charge or income row the table covers: default kept (INTERNAL) |
| bcf | 0 / 2 / 0 |  | Amount as delivered | EXTERNAL FLOW = Amount as delivered (round 25: DESCRIPTION 'Bounced Check Fee' (flat 15.00) + CRO: every charge other than an advisory fee is a withdrawal) |
| by | 105730 / 0 / 73159 | -1 x abs(Amount); sweep line: none (internal move inside the one cash position) |  | not a fee, charge or income row the table covers: default kept (INTERNAL) |
| cbf | 0 / 39 / 0 |  | Amount as delivered | EXTERNAL FLOW = Amount as delivered (round 25: DESCRIPTION 'Checkbook Fee' (flat 5.00 each) + CRO: every charge other than an advisory fee is a withdrawal) |
| ci | 15659 / 0 / 0 | none (contribution and purchase cancel) |  | EXTERNAL FLOW (the CRO's table names ci a flow code; the default table has it INTERNAL), +1 x abs(Amount) |
| cs | 24 / 0 / 0 | -1 x abs(Amount) |  | not a fee, charge or income row the table covers: default kept (INTERNAL) |
| csltfee | 0 / 164 / 0 |  | Amount as delivered | EXTERNAL FLOW = Amount as delivered |
| dv | 410839 / 8086 / 0 | + Amount | Amount as delivered | income, inside the return |
| dvlt | 23451 / 0 / 0 | + Amount |  | income, inside the return |
| dvr | 309330 / 0 / 52340 | - Amount; sweep line: none (internal move inside the one cash position) |  | income, inside the return |
| dvst | 9678 / 0 / 0 | + Amount |  | income, inside the return |
| fch | 0 / 2301 / 0 |  | Amount as delivered | EXTERNAL FLOW = Amount as delivered |
| fco | 0 / 57 / 0 |  | Amount as delivered | EXTERNAL FLOW = Amount as delivered (round 25: DESCRIPTION 'IRA Close Expenses', the same description family as fch 'IRA Maintenance Expenses' and fee 'IRA Expense', which the CRO's table makes external flows) |
| fee | 0 / 281 / 0 |  | Amount as delivered | EXTERNAL FLOW = Amount as delivered |
| frntax | 1086 / 1173 / 0 | + Amount | Amount as delivered | INTERNAL, inside the return (round 25: PAIRING: each security-line row sits on a same-security same-day dv and is a round fraction of it (25 percent, 15 percent): tax withheld at source out of the holding's own income, so the income is net of it, inside the return) |
| ftax | 14 / 4198 / 0 | + Amount | Amount as delivered | EXTERNAL FLOW = Amount as delivered where a CFNCASH row rides a same-day CFNCASH lo, else INTERNAL (round 25: PAIRING: a CFNCASH row on the same account and day as a CFNCASH withdrawal (lo): the withdrawal is gross = lo + withholding, and the withholding is a fixed share of that gross) |
| genmain | 0 / 872 / 0 |  | Amount as delivered | EXTERNAL FLOW = Amount as delivered |
| ileu | 267 / 0 / 0 | + Amount |  | not a fee, charge or income row the table covers: default kept (INTERNAL) |
| int | 10432 / 136 / 53186 | + Amount; sweep line: income, +Amount | Amount as delivered | income, inside the return |
| leu | 515 / 0 / 0 | +1 x abs(Amount) |  | not a fee, charge or income row the table covers: default kept (INTERNAL) |
| li | 41809 / 19335 / 0 | none (moves securities, not cash) | +1 x abs(Amount) | EXTERNAL FLOW (default table, +1 x abs(Amount)) |
| lica | 9226 / 0 / 0 | none (moves securities, not cash) |  | not a fee, charge or income row the table covers: default kept (INTERNAL) |
| licar | 28464 / 0 / 0 | none (moves securities, not cash) |  | not a fee, charge or income row the table covers: default kept (INTERNAL) |
| lo | 19016 / 30673 / 0 | none (moves securities, not cash) | -1 x abs(Amount) | EXTERNAL FLOW (default table, -1 x abs(Amount)) |
| loca | 1966 / 0 / 0 | none (moves securities, not cash) |  | not a fee, charge or income row the table covers: default kept (INTERNAL) |
| man | 0 / 19753 / 0 |  | Amount as delivered | DRAG inside the return, not a flow |
| misc | 1216 / 320 / 0 | + Amount | Amount as delivered | EXTERNAL FLOW = Amount as delivered |
| pcf | 0 / 96 / 0 |  | Amount as delivered | EXTERNAL FLOW = Amount as delivered |
| pyd | 497 / 0 / 0 | +1 x abs(Amount) |  | not a fee, charge or income row the table covers: default kept (INTERNAL) |
| roy | 889 / 0 / 0 | + Amount |  | not a fee, charge or income row the table covers: default kept (INTERNAL) |
| si | 6 / 0 / 0 | none (moves securities, not cash) |  | EXTERNAL FLOW (default table, -1 x abs(Amount)) |
| sl | 102284 / 0 / 45611 | +1 x abs(Amount); sweep line: none (internal move inside the one cash position) |  | not a fee, charge or income row the table covers: default kept (INTERNAL) |
| so | 3 / 0 / 0 | none (moves securities, not cash) |  | EXTERNAL FLOW (default table, +1 x abs(Amount)) |
| ss | 26 / 0 / 0 | +1 x abs(Amount) |  | not a fee, charge or income row the table covers: default kept (INTERNAL) |
| stax | 0 / 112 / 0 |  | Amount as delivered | EXTERNAL FLOW = Amount as delivered where a CFNCASH row rides a same-day CFNCASH lo, else INTERNAL (round 25: PAIRING: the same as ftax (a CFNCASH row on the same account and day as a CFNCASH lo)) |
| stp | 0 / 4 / 0 |  | Amount as delivered | EXTERNAL FLOW = Amount as delivered (round 25: DESCRIPTION 'Stop Payment Expense' (flat 10.00) + CRO: every charge other than an advisory fee is a withdrawal) |
| term | 0 / 5 / 0 |  | Amount as delivered | EXTERNAL FLOW = Amount as delivered (round 25: DESCRIPTION 'Termination Fee' (flat 100.00) + CRO: every charge other than an advisory fee is a withdrawal) |
| trci | 111 / 0 / 0 | none (moves securities, not cash) |  | EXTERNAL FLOW (default table, +1 x abs(Amount)) |
| trco | 147 / 0 / 0 | none (moves securities, not cash) |  | EXTERNAL FLOW (default table, -1 x abs(Amount)) |
| trfi | 1375 / 1298 / 0 | none (moves securities, not cash) | +1 x abs(Amount) | EXTERNAL FLOW (default table, +1 x abs(Amount)) |
| trfo | 611 / 1298 / 0 | none (moves securities, not cash) | -1 x abs(Amount) | EXTERNAL FLOW (default table, -1 x abs(Amount)) |

## The round-25 source table: a treatment for each unlisted row type, with its stated source (decided before the run)

Sources: DESCRIPTION = the delivered file's own Transaction_Description of the type (silver transactions); PAIRING = how the rows sit in the delivery; CRO = RESEARCH_20261008_COMMONWEALTH_TWR_METHOD.md section 1 ("'NetofFees' means net of advisory fees only, and every other charge is a withdrawal"). A type with no source stays INTERNAL and says so. The treatment is `method_r25`, layered on `method` (the cash ledger is the same, only the return's treatment of these rows differs).

| type | delivered description | rows (CFNCASH / security) | accounts | treatment | source | measured on the delivery |
|---|---|---|---|---|---|---|
| ASF | ASF | 6 / 0 | 1 | INTERNAL (inside the return) | NO SOURCE: the description is 'ASF' and names no fee; its notes (a quarterly-period 'Fee Reversal' and 'Returned Payment') do not say whether it is an advisory fee (a drag) or another charge (a flow); stays INTERNAL | 6 rows; the description names no fee |
| bcf | Bounced Check Fee | 2 / 0 | 1 | EXTERNAL FLOW = Amount as delivered | DESCRIPTION 'Bounced Check Fee' (flat 15.00) + CRO: every charge other than an advisory fee is a withdrawal | |Amount| 15.0 x 2 |
| cbf | Checkbook Fee | 39 / 0 | 20 | EXTERNAL FLOW = Amount as delivered | DESCRIPTION 'Checkbook Fee' (flat 5.00 each) + CRO: every charge other than an advisory fee is a withdrawal | |Amount| 5.0 x 39 |
| fco | IRA Close Expenses | 57 / 0 | 54 | EXTERNAL FLOW = Amount as delivered | DESCRIPTION 'IRA Close Expenses', the same description family as fch 'IRA Maintenance Expenses' and fee 'IRA Expense', which the CRO's table makes external flows | |Amount| 125.0 x 47, 95.0 x 9, 47.62 x 1 |
| frntax | Foreign Tax | 1173 / 1086 | 158 | INTERNAL (inside the return) | PAIRING: each security-line row sits on a same-security same-day dv and is a round fraction of it (25 percent, 15 percent): tax withheld at source out of the holding's own income, so the income is net of it, inside the return | 1086 of 1086 security-line rows sit on a same-security same-day dv; share of that dividend: 0.25 x 697, 0.15 x 163, 0.21 x 58, 0.5 x 22 |
| ftax | Federal Tax Withholding | 4198 / 14 | 201 | EXTERNAL FLOW = Amount as delivered when the CFNCASH row rides a same-day CFNCASH lo; otherwise INTERNAL | PAIRING: a CFNCASH row on the same account and day as a CFNCASH withdrawal (lo): the withdrawal is gross = lo + withholding, and the withholding is a fixed share of that gross | 4056 of 4212 rows ride a same-day lo (4044 account-days); withheld share of lo + withholding: 0.15 x 1042, 0.1 x 921, 0.2 x 868, 0.25 x 532 |
| stax | State Tax Withholding | 112 / 0 | 9 | EXTERNAL FLOW = Amount as delivered when the CFNCASH row rides a same-day CFNCASH lo; otherwise INTERNAL | PAIRING: the same as ftax (a CFNCASH row on the same account and day as a CFNCASH lo) | 107 of 112 rows ride a same-day lo (107 account-days); withheld share of lo + withholding: 0.02 x 44, 0.06 x 40, 0.13 x 7, 0.1 x 4 |
| stp | Stop Payment Expense | 4 / 0 | 3 | EXTERNAL FLOW = Amount as delivered | DESCRIPTION 'Stop Payment Expense' (flat 10.00) + CRO: every charge other than an advisory fee is a withdrawal | |Amount| 10.0 x 4 |
| term | Termination Fee | 5 / 0 | 4 | EXTERNAL FLOW = Amount as delivered | DESCRIPTION 'Termination Fee' (flat 100.00) + CRO: every charge other than an advisory fee is a withdrawal | |Amount| 100.0 x 5 |


## Round 26: ASF's state

State NO-SOURCE, treatment internal (commonwealth_asf_source.py decides it from the delivery before any grade). ASF rows in the delivery: 6 (flows.ASF_ROWS says 6). `method_r26` is `method_r25` plus that treatment: ASF stays internal, so the two rules are equal and any difference between the arms is a defect.

## Round 24's 35 MATCH -> DIFF months that hold an unlisted type, under this arm

The 35 of round 24's 98 regressions (MATCH under `conditional`, DIFF under `method`; 0.9.0_WK_ADVI_COTBKF~46/month_grades_after.parquet) whose rows include one of the nine types. Each is MATCH under this arm or carries its unlisted rows and the treatment each got.

| account | month | unlisted rows (type x n: treatment) | reported | `method` computed | now computed | now | result |
|---|---|---|---|---|---|---|---|
| acct#93ba00cd | 2020-12 | ftax x 1: flow (rides a same-day lo) | 0.02 | -15.4624 | 0.0201 | MATCH | MATCH |
| acct#15327bce | 2017-01 | ftax x 1: flow (rides a same-day lo) | 0.0 | -0.4536 | 0.0008 | MATCH | MATCH |
| acct#15327bce | 2017-02 | ftax x 1: flow (rides a same-day lo) | 0.0 | -4.3138 | 0.0004 | MATCH | MATCH |
| acct#47bd9af5 | 2016-03 | ftax x 1: flow (rides a same-day lo) | 0.0 | -0.1616 | 0.0008 | MATCH | MATCH |
| acct#47bd9af5 | 2016-04 | ftax x 2: flow (rides a same-day lo) | 0.0 | -0.3277 | 0.0008 | MATCH | MATCH |
| acct#47bd9af5 | 2016-06 | ftax x 1: flow (rides a same-day lo) | 0.0 | -0.1656 | 0.0008 | MATCH | MATCH |
| acct#47bd9af5 | 2016-07 | ftax x 1: flow (rides a same-day lo) | 0.0 | -0.167 | 0.0008 | MATCH | MATCH |
| acct#47bd9af5 | 2016-08 | ftax x 1: flow (rides a same-day lo) | 0.0 | -0.1684 | 0.0008 | MATCH | MATCH |
| acct#47bd9af5 | 2016-09 | ftax x 2: flow (rides a same-day lo) | 0.0 | -0.3417 | 0.0008 | MATCH | MATCH |
| acct#47bd9af5 | 2016-11 | ftax x 1: flow (rides a same-day lo) | 0.0 | -0.1728 | 0.0008 | MATCH | MATCH |
| acct#47bd9af5 | 2016-12 | ftax x 1: flow (rides a same-day lo) | 0.0 | -0.1743 | 0.0008 | MATCH | MATCH |
| acct#47bd9af5 | 2017-01 | ftax x 1: flow (rides a same-day lo) | 0.0 | -0.1728 | 0.0008 | MATCH | MATCH |
| acct#47bd9af5 | 2017-02 | ftax x 1: flow (rides a same-day lo) | 0.0 | -0.1744 | 0.0008 | MATCH | MATCH |
| acct#47bd9af5 | 2017-03 | ftax x 2: flow (rides a same-day lo) | 0.0 | -0.3538 | 0.0008 | MATCH | MATCH |
| acct#47bd9af5 | 2017-05 | ftax x 1: flow (rides a same-day lo) | 0.0 | -0.179 | 0.0008 | MATCH | MATCH |
| acct#47bd9af5 | 2017-06 | ftax x 2: flow (rides a same-day lo) | 0.0 | -0.3635 | 0.0008 | MATCH | MATCH |
| acct#47bd9af5 | 2017-08 | ftax x 1: flow (rides a same-day lo) | 0.0 | -0.1806 | 0.0042 | MATCH | MATCH |
| acct#47bd9af5 | 2017-09 | ftax x 2: flow (rides a same-day lo) | 0.0 | -0.3704 | 0.0041 | MATCH | MATCH |
| acct#47bd9af5 | 2017-11 | ftax x 1: flow (rides a same-day lo) | 0.0 | -0.186 | 0.0041 | MATCH | MATCH |
| acct#47bd9af5 | 2017-12 | ftax x 1: flow (rides a same-day lo) | 0.0 | -0.1878 | 0.0042 | MATCH | MATCH |
| acct#47bd9af5 | 2018-01 | ftax x 1: flow (rides a same-day lo) | 0.01 | -0.171 | 0.0122 | MATCH | MATCH |
| acct#47bd9af5 | 2018-02 | ftax x 1: flow (rides a same-day lo) | 0.01 | -0.1734 | 0.0115 | MATCH | MATCH |
| acct#47bd9af5 | 2018-03 | ftax x 2: flow (rides a same-day lo) | 0.01 | -0.3604 | 0.0141 | MATCH | MATCH |
| acct#655e1810 | 2016-05 | cbf x 1: flow (sourced charge) | 0.0 | -0.0578 | 0.0008 | MATCH | MATCH |
| acct#655e1810 | 2016-09 | cbf x 1: flow (sourced charge) | 0.0 | -0.2446 | 0.0025 | MATCH | MATCH |
| acct#655e1810 | 2017-03 | stp x 1: flow (sourced charge) | 0.0 | -0.0911 | 0.001 | MATCH | MATCH |
| acct#655e1810 | 2018-06 | cbf x 1: flow (sourced charge) | 0.02 | -0.0557 | 0.0215 | MATCH | MATCH |
| acct#248f2de0 | 2022-05 | fco x 1: flow (sourced charge) | 0.0 | -2.0825 | 0.0008 | MATCH | MATCH |
| acct#9d0bbc8f | 2023-09 | ftax x 1: flow (rides a same-day lo); stax x 1: flow (rides a same-day lo) | 0.07 | -1.6944 | 0.0651 | MATCH | MATCH |
| cv18643456 | 2014-01 | ftax x 1: flow (rides a same-day lo) | 0.0 | -5.9733 | 0.0017 | MATCH | MATCH |
| cv18643456 | 2014-02 | ftax x 1: flow (rides a same-day lo) | 0.0 | -9.9287 | 0.0017 | MATCH | MATCH |
| cv18643456 | 2015-09 | ftax x 1: flow (rides a same-day lo) | 0.0 | -14.9997 | 0.0003 | MATCH | MATCH |
| cv18643456 | 2015-10 | ftax x 1: flow (rides a same-day lo) | 0.0 | -14.9996 | 0.0003 | MATCH | MATCH |
| cv18643456 | 2015-11 | ftax x 1: flow (rides a same-day lo) | 0.0 | -14.9996 | 0.0003 | MATCH | MATCH |
| cv18643456 | 2015-12 | ftax x 2: flow (rides a same-day lo) | 0.0 | -3750038.4541 | 0.0001 | MATCH | MATCH |

MATCH under this arm: 35 of 35.

### Every other month whose computed return moved between the arms: 0

| account | month | unlisted rows held | `method` | now | reported |
|---|---|---|---|---|---|

Control months (no listed position) that differ between the arms: 0, of which 0 are among the 35 above. They differ because the new treatment applies to a CFNCASH row whether or not the account holds a listed sweep.

## The ledger against the 2026-06-23 positions snapshot (the one cash fact in the delivery)

The ledger of every posting of an account (sweep + CFNCASH, one cash position) against that account's sweep and CFNCASH positions on the snapshot: 40 accounts hold one; equal within 0.01: 40.

### What the 0 MATCH -> DIFF months hold (measured, nothing adopted from it)

- months holding a row of an UNLISTED CHARGE/TAX type (the table does not name it; default kept): 0 (none)
- months holding a dividend row (dv, dvlt or dvst, dated by its pay date): 0
- months holding neither: 0
- accounts: 0; the largest: 

### Every MATCH -> DIFF month with ONE named cause: 0 (traced from the month's own rows, nothing forced, no treatment changed)

Rule, stated before the counts: a month holding a row of a type the CRO's table does not name is `unlisted_type:<type>`. Any other month's daily returns are compared between the arms: a day on which the arms' account values differ by a changed amount is a step day named by the posting type(s) that equal that amount to the cent; a day on which the arms' external flows differ is a flow day; every other day differs by the level carried from earlier steps. The bucket carrying the largest sum of |return difference| names the month; `unexplained:` names a month where none could be read. A carried level is split by the category of the steps that built it (dividend_row, fee_row, charge_row, trade_cash, mixed_rows) and named by the category with the largest net (netted, since a sale's credit and a later purchase's debit cancel), with the type under a fee, charge or dividend category. `pre_first_valued_day` is the amount the arms already differ by on the account's first valued day: every posting made while the account was unvalued, which the arms' cash rules post differently; it is not split by row type because the conditional arm's cash by type is not recorded. `cash_leg_difference` is a step that no set of that day's postings equals to the cent.

Counts per cause (sum 0): 

| account | month | computed before | computed after | reported | cause | trace |
|---|---|---|---|---|---|---|

## The 163 round-19 movers re-counted by verdict (round 24)

AFTER verdict of the 163: MATCH 138, DIFF 25, UNGRADABLE 0, ABSENT 0.


## Round 22's 25 recovered months under this arm, each MATCH or named with its traced cause

| account | month | verdict | computed | reported | diff | cause |
|---|---|---|---|---|---|---|
| acct#5aa91f68 | 2017-07 | MATCH | 0.002 | 0.0 | 0.002 | MATCH |
| acct#5aa91f68 | 2017-08 | MATCH | 0.0042 | 0.0 | 0.0042 | MATCH |
| acct#5aa91f68 | 2017-09 | MATCH | 0.004 | 0.0 | 0.004 | MATCH |
| acct#5aa91f68 | 2017-10 | MATCH | 0.0042 | 0.0 | 0.0042 | MATCH |
| acct#5aa91f68 | 2017-12 | MATCH | 0.0042 | 0.0 | 0.0042 | MATCH |
| acct#5aa91f68 | 2018-01 | MATCH | 0.0121 | 0.01 | 0.0021 | MATCH |
| acct#5aa91f68 | 2018-02 | MATCH | 0.0115 | 0.01 | 0.0015 | MATCH |
| acct#5aa91f68 | 2018-03 | MATCH | 0.014 | 0.01 | 0.004 | MATCH |
| acct#5aa91f68 | 2018-04 | MATCH | 0.0205 | 0.02 | 0.0005 | MATCH |
| acct#5aa91f68 | 2018-05 | MATCH | 0.0212 | 0.02 | 0.0012 | MATCH |
| acct#5aa91f68 | 2018-06 | MATCH | 0.0205 | 0.02 | 0.0005 | MATCH |
| acct#ab0c6781 | 2018-01 | MATCH | 0.1814 | 0.18 | 0.0014 | MATCH |
| acct#cce589ab | 2024-02 | MATCH | 4.3367 | 4.32 | 0.0167 | MATCH |
| acct#cce589ab | 2024-08 | MATCH | 1.7854 | 1.79 | -0.0046 | MATCH |
| acct#cce589ab | 2025-02 | MATCH | -1.5729 | -1.55 | -0.0229 | MATCH |
| acct#cce589ab | 2025-08 | MATCH | 2.5124 | 2.52 | -0.0076 | MATCH |
| D49141608 | 2019-02 | MATCH | 0.0419 | 0.04 | 0.0019 | MATCH |
| D49141608 | 2019-03 | MATCH | 0.0466 | 0.05 | -0.0034 | MATCH |
| D49141608 | 2019-04 | MATCH | 0.0452 | 0.05 | -0.0048 | MATCH |
| D49141608 | 2019-05 | MATCH | 0.0465 | 0.05 | -0.0035 | MATCH |
| D49141608 | 2019-06 | MATCH | 0.0451 | 0.05 | -0.0049 | MATCH |
| D49141608 | 2019-07 | MATCH | 0.0465 | 0.05 | -0.0035 | MATCH |
| D49141608 | 2019-08 | MATCH | 0.0381 | 0.04 | -0.0019 | MATCH |
| D49141608 | 2019-09 | MATCH | 0.0321 | 0.03 | 0.0021 | MATCH |
| D49141714 | 2019-02 | MATCH | 0.0421 | 0.04 | 0.0021 | MATCH |


## Cross-month dividends graded BOTH ways: NOT GRADED, no ex-date source

The pay arm is the file's own dating (every dividend row carries ONE date, the pay date). The ex arm needs each dividend's ex-date, and no store the chain reads holds one: the price stores carry date, security and price only (opal-data-cot silver/prices/canonical_prices.parquet: date, asset_name, ticker, price, source), and the Yahoo dividend series the price backfill pulls is not among the stores read. So the months holding a cross-month dividend cannot even be named (a cross-month dividend is one whose ex-date and pay date fall in different months), and none is guessed from a price move. The mechanism is built and tested (--dividend-date ex --ex-dates <cusip, pay_date, ex_date>; commonwealth_sweeps.method_cash_rows); run with a source it prints this section's table with the swing per month and in total. Neither date is adopted: the default stays pay, as delivered.

## The YEAR-CHAIN control

Rule, stated before the counts: an account-year is in the control when Commonwealth reports its Year row (Jan 1 .. Dec 31, TWR net) and all 12 of its Month rows and the 12 months chained (prod(1 + m/100) - 1) agree with the Year row within 0.1 pct points (Commonwealth's year row chains its month rows; the CRO measured 4,050 of 4,054). For each such account-year in which Opal computed all 12 months, Opal's chained months must agree with Opal's own year chain (the product of the account's daily returns over the year) within the same 0.1. year_chain_same is True when every such account-year does and at least one exists.

- account-years with a full Year row and 12 reported months: 4054; of which Commonwealth's year row chains its months: 4050
- of those, account-years in which Opal computed all 12 months: 103; Opal's chained months agree with Opal's own year chain: 103; worst deviation 3.98e-13 pct points
- year_chain_same=True


## The control: months with no listed position

A month graded MATCH or DIFF (before or after) of an account with no listed-sweep (or listed core-position) transaction on or before the month's end (a CUSIP listed in either arm counts): 566 months, 566 with the same verdict and the same computed return (to 1e-09 pct points): control_same=True.

The literal in-month reading (graded months of an account-month with no listed-sweep row IN that month, including months after an earlier sweep trade whose cash leg persists): 955 months, 955 unchanged, 0 moved. Those that moved are accounts whose value now carries the sweep trade's cash leg.

SWEEP-REGRADE sweeps=2 rejected=517 double_drop_months=0 fixed=0 months_before=3098/886/78609 months_after=3098/886/78609 control_same=True regressions=0 movers_back=138 year_chain_same=True r22_named=25/25 dividend_both=NA
