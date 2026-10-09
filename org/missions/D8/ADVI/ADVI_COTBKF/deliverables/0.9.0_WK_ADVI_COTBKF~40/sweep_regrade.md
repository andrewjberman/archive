# Commonwealth sweep re-grade (CB-s-1)

The chain valuation -> daily returns -> monthly grade, run twice on the same transactions, price stores and reported returns. BEFORE: cash by CUSIP prefix, no cash legs, sweep trades not special in the flow table. AFTER: the declared sweep list sweeps-v1-20261008.

## The declared sweep list, version sweeps-v1-20261008

| CUSIP | source kind | source (as delivered) | asset type | evidence |
|---|---|---|---|---|
| FDIC66606 | vendor_description | Bank Deposit Sweep Program | Cash | silver transactions Security_Description as delivered; 143,357 rows, types by/dvr/int/sl |
| FDIC66853 | vendor_description | Advisory Retirement Sweep Program | Cash | silver transactions Security_Description as delivered; 80,939 rows, types by/dvr/int/sl |

Cash but not a sweep: CFNCASH (Cash Credit (Debit) Balance)

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

## The single-flow months of the largest class (lo/over 10%), BEFORE and AFTER

The DIFF months (before) of the class `commonwealth_flow_diff_classes` ranks first (lo/over 10%: 249 DIFF months) with exactly one external flow row of the class's type: 106. A DOUBLE-DROP month is one where the account value on the flow day fell by twice the withdrawal (|drop - 2|flow|| <= 1% of |flow| + 0.05, before): 74; a drop of once the withdrawal: 2.

Reading notes: 100 of the 106 single-flow months have a listed-sweep sale of any amount on the flow's day; 59 of the 74 double-drop months pair with a sweep sale of the same amount (within 0.01). Fixed (DIFF before, MATCH after) among the double-drop months: 42.

### The double-drop months, named

| account | month | flow day | withdrawal | value drop / withdrawal | sweep sale that day | before | computed | reported | diff | after | computed | diff |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| acct#f6c79f45 | 2023-08 | 2023-08-14 | 49778.09 | 1.993 | 19333.48 | DIFF | -5.4132 | 3.07 | -8.4832 | DIFF | -1.9287 | -4.9987 |
| acct#b4db1f25 | 2022-03 | 2022-03-09 | 18000.0 | 2.0 | 18000.0 | DIFF | -41.9989 | 0.0 | -41.9989 | UNGRADABLE |  |  |
| acct#b4db1f25 | 2023-03 | 2023-03-20 | 1000.0 | 2.0 | 1000.0 | DIFF | -24.5638 | 0.05 | -24.6138 | UNGRADABLE |  |  |
| acct#93ba00cd | 2017-08 | 2017-08-17 | 80000.0 | 2.0 | 80000.0 | DIFF | -23.6131 | 0.01 | -23.6231 | MATCH | 0.0065 | -0.0035 |
| acct#ef1f3927 | 2019-02 | 2019-02-21 | 20000.0 | 2.0 | 20000.0 | DIFF | -32.5264 | 0.17 | -32.6964 | DIFF | 0.0511 | -0.1189 |
| acct#638a682f | 2016-03 | 2016-03-22 | 18525.77 | 2.0 | 18525.77 | DIFF | -32.4715 | 0.0 | -32.4715 | MATCH | 0.0018 | 0.0018 |
| acct#638a682f | 2016-11 | 2016-11-16 | 8126.12 | 2.0 | 8126.12 | DIFF | 88.0727 | 0.0 | 88.0727 | MATCH | 0.0007 | 0.0007 |
| acct#638a682f | 2017-12 | 2017-12-28 | 3500.0 | 2.0 | 3500.0 | DIFF | -17.4961 | 0.01 | -17.5061 | MATCH | 0.0062 | -0.0038 |
| acct#638a682f | 2018-10 | 2018-10-25 | 3000.0 | 2.0 | 3000.0 | DIFF | 7.7733 | 0.04 | 7.7333 | MATCH | 0.0363 | -0.0037 |
| acct#638a682f | 2019-01 | 2019-01-31 | 4624.48 | 1.999 | 4624.48 | DIFF | -33.0271 | 0.04 | -33.0671 | MATCH | 0.0447 | 0.0047 |
| acct#638a682f | 2020-02 | 2020-02-04 | 11500.0 | 2.0 | 11500.0 | DIFF | -39.0413 | 0.03 | -39.0713 | MATCH | 0.0293 | -0.0007 |
| acct#638a682f | 2020-06 | 2020-06-01 | 3700.0 | 2.0 | 3700.0 | DIFF | 15.3238 | 0.0 | 15.3238 | MATCH | 0.0003 | 0.0003 |
| acct#638a682f | 2020-09 | 2020-09-01 | 3700.0 | 2.0 | 3700.0 | DIFF | 15.3236 | 0.0 | 15.3236 | MATCH | 0.0003 | 0.0003 |
| acct#638a682f | 2020-12 | 2020-12-01 | 3700.0 | 2.0 | 3700.0 | DIFF | -26.7137 | 0.0 | -26.7137 | MATCH | 0.0006 | 0.0006 |
| acct#05dd4a9d | 2023-04 | 2023-04-14 | 455.68 | 2.0 | 455.68 | DIFF | -11.1374 | -0.22 | -10.9174 | DIFF | 0.0651 | 0.2851 |
| acct#05dd4a9d | 2023-05 | 2023-05-15 | 455.68 | 2.0 | 455.68 | DIFF | -14.1216 | 0.07 | -14.1916 | MATCH | 0.0678 | -0.0022 |
| acct#05dd4a9d | 2023-06 | 2023-06-14 | 455.68 | 2.0 | 455.68 | DIFF | -19.7041 | 0.08 | -19.7841 | MATCH | 0.0665 | -0.0135 |
| acct#05dd4a9d | 2023-07 | 2023-07-14 | 455.68 | 2.0 | 455.68 | DIFF | -32.7146 | -0.18 | -32.5346 | DIFF | 0.0779 | 0.2579 |
| acct#2da3289c | 2016-11 | 2016-11-23 | 9000.0 | 2.0 | 9000.0 | DIFF | -11.596 | 0.0 | -11.596 | MATCH | 0.001 | 0.001 |
| acct#2da3289c | 2018-01 | 2018-01-24 | 20000.0 | 2.0 | 20000.0 | DIFF | -23.3664 | 0.02 | -23.3864 | MATCH | 0.0209 | 0.0009 |
| acct#0ef529b4 | 2019-09 | 2019-09-30 | 53555.25 | 2.0 | 53555.25 | DIFF | 328.742 | 0.0 | 328.742 | MATCH | 0.0007 | 0.0007 |
| acct#0ea6ac16 | 2018-01 | 2018-01-05 | 12760.28 | 2.0 | 12760.28 | DIFF | 277.6649 | 0.03 | 277.6349 | MATCH | 0.0264 | -0.0036 |
| acct#0ea6ac16 | 2019-04 | 2019-04-17 | 10000.0 | 2.0 | 10000.0 | DIFF | -36.1136 | 0.11 | -36.2236 | MATCH | 0.1117 | 0.0017 |
| acct#0ea6ac16 | 2019-11 | 2019-11-20 | 3500.0 | 2.0 | 3500.0 | DIFF | -45.5514 | 0.15 | -45.7014 | MATCH | 0.152 | 0.002 |
| acct#0ea6ac16 | 2020-01 | 2020-01-08 | 12760.28 | 2.0 | 12760.28 | DIFF | 918.5319 | 0.07 | 918.4619 | MATCH | 0.0675 | -0.0025 |
| acct#baf557d6 | 2020-05 | 2020-05-01 | 5000.0 | 2.0 | 5000.0 | DIFF | 1099.3439 | 0.0 | 1099.3439 | MATCH | 0.0004 | 0.0004 |
| acct#baf557d6 | 2020-06 | 2020-06-01 | 5000.0 | 2.0 | 5000.0 | DIFF | 1099.2418 | 0.0 | 1099.2418 | MATCH | 0.0002 | 0.0002 |
| acct#baf557d6 | 2020-09 | 2020-09-01 | 5000.0 | 2.0 | 5000.0 | DIFF | 1099.0903 | 0.0 | 1099.0903 | MATCH | 0.0002 | 0.0002 |
| acct#baf557d6 | 2020-12 | 2020-12-01 | 5000.0 | 2.0 | 5000.0 | DIFF | 1098.8381 | 0.0 | 1098.8381 | MATCH | 0.0002 | 0.0002 |
| acct#baf557d6 | 2021-01 | 2021-01-04 | 5000.0 | 2.0 | 5000.0 | DIFF | 1091.2485 | 0.0 | 1091.2485 | MATCH | 0.0008 | 0.0008 |
| acct#baf557d6 | 2022-01 | 2022-01-03 | 5000.0 | 2.0 | 5000.0 | DIFF | 16.5947 | 0.0 | 16.5947 | MATCH | 0.0007 | 0.0007 |
| acct#baf557d6 | 2022-05 | 2022-05-05 | 4000.0 | 2.0 | 4000.0 | DIFF | -17.2447 | 0.0 | -17.2447 | MATCH | 0.0008 | 0.0008 |
| acct#4040a6ea | 2017-10 | 2017-10-03 | 500100.0 | 2.0 | 500100.0 | DIFF | -23.8284 | -0.44 | -23.3884 | DIFF | 0.0046 | 0.4446 |
| acct#c33b5ead | 2017-12 | 2017-12-07 | 6000.0 | 2.0 | 6000.0 | DIFF | -24.0534 | 0.0 | -24.0534 | UNGRADABLE |  |  |
| acct#c33b5ead | 2018-01 | 2018-01-18 | 3000.0 | 2.0 | 3000.0 | DIFF | -24.3459 | -0.32 | -24.0259 | UNGRADABLE |  |  |
| acct#c093546d | 2022-05 | 2022-05-12 | 16000.0 | 2.0 | 16000.0 | DIFF | -14.4658 | 0.0 | -14.4658 | MATCH | 0.001 | 0.001 |
| acct#c093546d | 2024-09 | 2024-09-18 | 2500.0 | 2.0 | 1359.92 | DIFF | -11.8994 | 0.43 | -12.3294 | DIFF | -5.567 | -5.997 |
| acct#c093546d | 2024-11 | 2024-11-15 | 500.0 | 2.0 | 0.0 | DIFF | -13.1909 | 0.4 | -13.5909 | DIFF | -11.924 | -12.324 |
| acct#c093546d | 2024-12 | 2024-12-18 | 1000.0 | 2.0 | 0.0 | DIFF | -36.2257 | 0.48 | -36.7057 | DIFF | -31.7495 | -32.2295 |
| acct#e29efebe | 2025-10 | 2025-10-07 | 218.75 | 2.0 | 218.75 | DIFF | 2.4065 | -0.31 | 2.7165 | DIFF | 0.0021 | 0.3121 |
| acct#e29efebe | 2025-11 | 2025-11-07 | 218.75 | 2.0 | 218.75 | DIFF | 2.4802 | 0.0 | 2.4802 | MATCH | 0.0011 | 0.0011 |
| acct#e29efebe | 2026-01 | 2026-01-07 | 218.75 | 2.0 | 218.75 | DIFF | 2.4119 | -0.3 | 2.7119 | DIFF | 0.0 | 0.3 |
| acct#e29efebe | 2026-02 | 2026-02-06 | 218.75 | 2.0 | 218.75 | DIFF | 2.482 | 0.0 | 2.482 | MATCH | 0.0 | 0.0 |
| acct#e29efebe | 2026-03 | 2026-03-06 | 218.75 | 2.0 | 218.75 | DIFF | 2.482 | 0.0 | 2.482 | MATCH | 0.0 | 0.0 |
| acct#4418ace5 | 2021-05 | 2021-05-20 | 25000.0 | 2.0 | 25000.0 | DIFF | -10.3891 | 0.0 | -10.3891 | MATCH | 0.001 | 0.001 |
| acct#4418ace5 | 2021-07 | 2021-07-14 | 16000.0 | 2.0 | 16000.0 | DIFF | -8.3929 | 0.0 | -8.3929 | MATCH | 0.0009 | 0.0009 |
| acct#4418ace5 | 2021-08 | 2021-08-18 | 14000.0 | 2.0 | 14000.0 | DIFF | -8.8252 | 0.0 | -8.8252 | MATCH | 0.0009 | 0.0009 |
| acct#57e741a5 | 2022-07 | 2022-07-07 | 40000.0 | 2.0 | 40000.0 | DIFF | -39.388 | -0.12 | -39.268 | DIFF | 0.03 | 0.15 |
| acct#57e741a5 | 2024-04 | 2024-04-15 | 38500.0 | 2.0 | 38500.0 | DIFF | -18.3048 | 0.05 | -18.3548 | MATCH | 0.0931 | 0.0431 |
| acct#57e741a5 | 2024-11 | 2024-11-06 | 41630.72 | 2.0 | 17568.66 | DIFF | -32.9578 | 0.45 | -33.4078 | DIFF | -21.9418 | -22.3918 |
| acct#57e741a5 | 2025-01 | 2025-01-15 | 42480.0 | 2.0 | 35002.15 | DIFF | 34.6477 | 0.3 | 34.3477 | DIFF | -9.3798 | -9.6798 |
| acct#57e741a5 | 2025-02 | 2025-02-28 | 5000.0 | 1.991 | 5000.0 | DIFF | -13.0351 | 0.24 | -13.2751 | DIFF | 0.1411 | -0.0989 |
| acct#602ce60b | 2023-07 | 2023-07-03 | 20000.0 | 1.999 | 19975.68 | DIFF | -34.2155 | -0.79 | -33.4255 | DIFF | 0.1546 | 0.9446 |
| acct#921b5169 | 2022-06 | 2022-06-24 | 10000.0 | 2.0 | 10000.0 | DIFF | -25.0707 | 0.01 | -25.0807 | MATCH | 0.0072 | -0.0028 |
| acct#921b5169 | 2022-08 | 2022-08-08 | 9597.98 | 2.0 | 9597.98 | DIFF | -48.2593 | 0.0 | -48.2593 | MATCH | 0.0442 | 0.0442 |
| acct#921b5169 | 2024-03 | 2024-03-26 | 25000.0 | 2.0 | 25000.0 | DIFF | -15.4798 | 0.09 | -15.5698 | MATCH | 0.0852 | -0.0048 |
| acct#921b5169 | 2024-08 | 2024-08-02 | 20000.0 | 2.0 | 20000.0 | DIFF | -17.9535 | 0.07 | -18.0235 | MATCH | 0.0663 | -0.0037 |
| acct#48283de9 | 2025-09 | 2025-09-05 | 20000.0 | 2.0 | 0.0 | DIFF | -16.5193 | 0.35 | -16.8693 | DIFF | -16.3102 | -16.6602 |
| acct#48283de9 | 2025-11 | 2025-11-05 | 20000.0 | 2.0 | 0.0 | DIFF | -24.7968 | 0.32 | -25.1168 | DIFF | -24.3314 | -24.6514 |
| acct#49133b9a | 2024-06 | 2024-06-10 | 15000.0 | 2.0 | 15000.0 | DIFF | -9.1679 | 0.41 | -9.5779 | DIFF | 0.2373 | -0.1727 |
| acct#49133b9a | 2024-07 | 2024-07-10 | 15000.0 | 2.0 | 249.81 | DIFF | -11.3091 | 0.41 | -11.7191 | DIFF | -11.0703 | -11.4803 |
| acct#49133b9a | 2024-08 | 2024-08-12 | 15000.0 | 2.0 | 0.05 | DIFF | -14.6767 | 0.48 | -15.1567 | DIFF | -14.6042 | -15.0842 |
| acct#49133b9a | 2024-09 | 2024-09-10 | 15000.0 | 2.0 | 0.0 | DIFF | -20.964 | 0.46 | -21.424 | DIFF | -20.8173 | -21.2773 |
| acct#9727ac87 | 2023-09 | 2023-09-06 | 1024101.54 | 2.0 | 9428.9 | DIFF | -40.5376 | 0.34 | -40.8776 | DIFF | -40.3072 | -40.6472 |
| acct#9727ac87 | 2024-04 | 2024-04-19 | 200000.0 | 2.0 | 123613.46 | DIFF | -9.8356 | 0.42 | -10.2556 | DIFF | -21.3113 | -21.7313 |
| acct#9727ac87 | 2024-05 | 2024-05-08 | 32001.41 | 2.0 | 32001.41 | DIFF | 10.4182 | 0.43 | 9.9882 | DIFF | 0.277 | -0.153 |
| acct#9727ac87 | 2025-04 | 2025-04-24 | 3298575.0 | 2.0 | 3298575.0 | DIFF | 702.6633 | 0.9 | 701.7633 | DIFF | 0.5011 | -0.3989 |
| D49141618 | 2016-02 | 2016-02-08 | 5386.75 | 2.0 | 5386.75 | DIFF | -20.7179 | 0.0 | -20.7179 | MATCH | 0.0008 | 0.0008 |
| D49141625 | 2020-05 | 2020-05-18 | 2654.97 | 2.0 | 2654.97 | DIFF | 490257.0845 | 0.0 | 490257.0845 | MATCH | -0.0 | -0.0 |
| acct#31c59227 | 2023-10 | 2023-10-04 | 1000.0 | 2.0 | 1000.0 | DIFF | -47.4075 | 0.24 | -47.6475 | DIFF | 0.1482 | -0.0918 |
| acct#31c59227 | 2025-01 | 2025-01-17 | 2000.0 | 2.0 | 2000.0 | DIFF | 300.1402 | 0.14 | 300.0002 | MATCH | 0.105 | -0.035 |
| acct#31c59227 | 2026-02 | 2026-02-17 | 2000.0 | 2.0 | 2000.0 | DIFF | 1448.9517 | 0.0 | 1448.9517 | MATCH | 0.0035 | 0.0035 |
| acct#557ce060 | 2025-11 | 2025-11-07 | 12200.0 | 2.0 | 0.01 | DIFF | 40.6112 | 0.15 | 40.4612 | DIFF | -14.7812 | -14.9312 |
| acct#a82f42db | 2025-01 | 2025-01-22 | 50000.0 | 2.0 | 50000.0 | DIFF | -13.3494 | -0.11 | -13.2394 | DIFF | 69.2014 | 69.3114 |

### The other 32 single-flow months (value did not fall by twice the withdrawal)

| account | month | withdrawal | value drop / withdrawal | sweep sale that day | before | diff | after | diff |
|---|---|---|---|---|---|---|---|---|
| acct#aaeb760c | 2025-07 | 250000.0 | 1.921 | 250000.0 | DIFF | -18.0364 | DIFF | 0.216 |
| acct#f6c79f45 | 2024-12 | 60000.0 | 2.013 | 6199.54 | DIFF | -11.8583 | DIFF | -11.8327 |
| acct#f6c79f45 | 2025-06 | 70000.0 | 1.91 | 7573.83 | DIFF | -17.8208 | DIFF | -16.9151 |
| acct#03836058 | 2023-10 | 3584.43 | 2.16 | 3584.43 | DIFF | -11.8822 | DIFF | -3.5988 |
| acct#03836058 | 2024-10 | 3577.15 | -1.462 | 3577.15 | DIFF | 38.1458 | DIFF | 59.7211 |
| acct#03836058 | 2025-10 | 3297.59 | 2.063 | 3297.59 | DIFF | -11.0245 | DIFF | -0.1449 |
| acct#93ba00cd | 2020-12 | 37081.16 | 2.282 | 47539.94 | DIFF | -35.8811 | MATCH | -0.0061 |
| acct#15327bce | 2017-02 | 1868.58 | 2.111 | 2076.19 | DIFF | -21.5213 | MATCH | 0.0003 |
| acct#baf557d6 | 2019-02 | 5000.0 | 0.507 | 1267.32 | DIFF | -2.5524 | MATCH | 0.0024 |
| acct#baf557d6 | 2019-03 | 5000.0 | 0.507 | 1267.32 | DIFF | -2.6948 | MATCH | -0.0031 |
| acct#baf557d6 | 2019-04 | 5000.0 | 0.507 | 1267.32 | DIFF | -2.8453 | MATCH | -0.0047 |
| acct#baf557d6 | 2019-07 | 5000.0 | 0.507 | 1267.32 | DIFF | -3.4153 | MATCH | -0.0032 |
| acct#baf557d6 | 2019-10 | 5000.0 | 0.507 | 1267.32 | DIFF | -6.3111 | MATCH | -0.0047 |
| acct#baf557d6 | 2020-02 | 5000.0 | 0.304 | 761.05 | DIFF | -7.4237 | MATCH | -0.0003 |
| acct#baf557d6 | 2020-04 | 5000.0 | 0.304 | 761.05 | DIFF | -2.0453 | MATCH | 0.0006 |
| acct#baf557d6 | 2021-02 | 5000.0 | 0.013 | 32.86 | DIFF | -0.3232 | MATCH | 0.0006 |
| acct#baf557d6 | 2021-03 | 5000.0 | 0.013 | 32.86 | DIFF | -0.3253 | MATCH | 0.0006 |
| acct#baf557d6 | 2021-09 | 5000.0 | 0.013 | 32.84 | DIFF | -0.1664 | MATCH | 0.0007 |
| acct#baf557d6 | 2021-10 | 5000.0 | 0.013 | 32.84 | DIFF | -0.1669 | MATCH | 0.0007 |
| acct#baf557d6 | 2021-11 | 5000.0 | 0.013 | 32.84 | DIFF | -0.1675 | MATCH | 0.0007 |
| acct#baf557d6 | 2021-12 | 5000.0 | 0.013 | 32.84 | DIFF | -0.168 | MATCH | 0.0007 |
| acct#f74da374 | 2024-01 | 33300.0 | 0.899 | 33300.0 | DIFF | -8.1651 | DIFF | -8.4676 |
| acct#f74da374 | 2024-03 | 36000.0 | 1.919 | 36000.0 | DIFF | -1.9414 | DIFF | -3.7509 |
| acct#2d4385bf | 2021-02 | 5800.0 | 2.017 | 5800.0 | DIFF | -30.5878 | DIFF | 6.4297 |
| acct#2d4385bf | 2023-05 | 3485.0 | 1.003 | 3485.0 | DIFF | -34.6072 | DIFF | -34.8889 |
| acct#d96c877d | 2026-01 | 155000.0 | 1.824 | 128038.48 | DIFF | -8.1367 | DIFF | -10.3089 |
| acct#0c8de232 | 2023-02 | 40000.0 | 1.761 | 40000.0 | DIFF | -13.9136 | DIFF | -1.7414 |
| acct#921b5169 | 2024-11 | 100000.0 | 0.6 | 30000.0 | DIFF | -42.1743 | MATCH | -0.0209 |
| acct#49133b9a | 2024-10 | 15000.0 | 1.0 | 0.0 | DIFF | -0.1872 | DIFF | -0.1926 |
| acct#557ce060 | 2025-03 | 12000.0 | 1.583 | 2676.16 | DIFF | -22.3408 | DIFF | -22.0191 |
| acct#c0cea213 | 2025-04 | 264824.0 | 1.747 | 53311.8 | DIFF | -33.9573 | DIFF | -33.9071 |
| acct#6834d5a2 | 2025-04 | 75743.0 | 1.983 | 0.69 | DIFF | -23.7505 | DIFF | -23.7474 |

## The whole grade, before and after

- before: MONTHLY-GRADE months=82593 match=1685 diff=1931 ungradable=78977 tolerance_pct=0.05
- after:  MONTHLY-GRADE months=82593 match=2057 diff=1522 ungradable=79014 tolerance_pct=0.05

| verdict | before | after |
|---|---|---|
| MATCH | 1685 | 2057 |
| DIFF | 1931 | 1522 |
| UNGRADABLE | 78977 | 79014 |

Verdict moves (before -> after, months):

- UNGRADABLE -> UNGRADABLE: 78973
- MATCH -> MATCH: 1512
- DIFF -> DIFF: 1357
- DIFF -> MATCH: 543
- MATCH -> DIFF: 163
- DIFF -> UNGRADABLE: 31
- MATCH -> UNGRADABLE: 10
- UNGRADABLE -> DIFF: 2
- UNGRADABLE -> MATCH: 2

## The control: months with no sweep row

A month graded MATCH or DIFF (before or after) of an account with no listed-sweep transaction on or before the month's end: 642 months, 642 with the same verdict and the same computed return (to 1e-09 pct points): control_same=True.

The literal in-month reading (graded months of an account-month with no listed-sweep row IN that month, including months after an earlier sweep trade whose cash leg persists): 919 months, 761 unchanged, 158 moved. Those that moved are accounts whose value now carries the sweep trade's cash leg.

SWEEP-REGRADE sweeps=2 rejected=517 double_drop_months=74 fixed=42 months_before=1685/1931/78977 months_after=2057/1522/79014 control_same=True
