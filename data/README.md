# DV2 data pack – Malaysia health expenditure

Downloaded and checked on 9 Oct 2026. Every file is either the original CSV (byte-for-byte, checked with SHA-256) or a table copied from an official PDF, with every column checked against the table's own published "Total" row.

Put `data/` and `geo/` into your GitHub repo as they are. Total size is under 1 MB.

## Files

### From the MOH National Health Accounts report (main source)
Source: [MNHA Health Expenditure Report 2011–2024](https://www.moh.gov.my/images/04-penerbitan/laporan-mnha/MNHA%20National%20Health%20Accounts%20Health%20Expenditure%20Report%202011-2024.pdf), Ministry of Health Malaysia. All money in **RM million**.

| File | Report table | What's in it | Use for |
|---|---|---|---|
| `mnha_national_2011_2024.csv` | T4.1, T4.2, T5.1d, T8.1 | One row per year: total spending (nominal and inflation-adjusted to 2024 prices), % of GDP, per person (nominal and adjusted), population, public vs private split, MOH share | C1, hero numbers, C3 |
| `mnha_financing_sources_2011_2024.csv` | T5.1b, T5.1c | Who paid, 15 sources × 14 years, RM and % of total. `payer_group` collapses them to 5 groups (MOH, out of pocket, private insurance, other public, other private) | C2 waffle, C3 slope |
| `mnha_functions_2011_2024.csv` | T7.1b, T7.1c, T5.2.4b | What the money paid for (11 functions), total and public-only. `plain_label` = plain-English name | C4 stream, C5 heatmap |
| `mnha_providers_2011_2024.csv` | T6.1b, T6.1c, T5.2.3b | Where it was spent (hospitals, clinics, pharmacies…), total and public-only (private = total − public) | C6 bump, C7 Marimekko |
| `mnha_oop_providers_2011_2024.csv` | T9.2c | Households' own money by where they paid (private hospitals, clinics, pharmacies…) | C8 treemap |
| `mnha_oop_functions_2011_2024.csv` | T9.3a | Households' own money by service (outpatient, inpatient, medicines…) | C8 alternative |
| `mnha_state_2024.csv` | T4.3 | 2024 spending and population per state. `state` uses data.gov.my names so it joins with the other files | M1, M3 |

Blank cells = "n/a" in the report (rehabilitative care 2013–2021; "<1" in 2012).

### From the MOH Annual Reports
| File | Source | What's in it | Use for |
|---|---|---|---|
| `moh_programme_budget_2020_2025.csv` | [MOH Annual Reports](https://www.moh.gov.my/en/publications-and-reports/infographics-reports-statistics/annual-report) 2020–2025, Finance chapter table "Allocation and Expenditure of Operating Budget by Programme" | Operating budget **allocated vs actually spent** per programme, in RM (not million). `group` keeps the 7 stable programmes and lumps the changing ones into "Other" | C9 bullet, C10 waterfall |

### From data.gov.my / OpenDOSM (licence CC BY 4.0)
| File | Source | What's in it | Use for |
|---|---|---|---|
| `mnha.csv` | [data.moh.gov.my/data-catalogue/mnha](https://data.moh.gov.my/data-catalogue/mnha) | Total / current spending, public / private, 2013–2022, **in RM** (not million) | Cross-check only |
| `budget_allocation_moh.csv` | [data.gov.my/data-catalogue/federal_budget_moh](https://data.gov.my/data-catalogue/federal_budget_moh) | MOH budget 2015–2024 in RM: `de` development, `oe` operating; `oe_10000` emoluments (salaries), `oe_20000` services & supplies, `oe_30000` assets, `oe_40000` fixed payments, `oe_50000` other | C11 |
| `hospital_beds_state.csv` | [data.gov.my/data-catalogue/hospital_beds](https://data.gov.my/data-catalogue/hospital_beds) | State-level rows only (district rows dropped), 2015–2022 | M2, M4 |
| `healthcare_staff.csv` | [data.gov.my/data-catalogue/healthcare_staff](https://data.gov.my/data-catalogue/healthcare_staff) | Public-sector doctors, nurses, dentists by state, 2014–2022 | M3 |
| `population_state.csv` | [open.dosm.gov.my/data-catalogue/population_state](https://open.dosm.gov.my/data-catalogue/population_state) | Population **in thousands**, all ages/sexes/ethnicities, 2020–2023 | per-person rates |

### International comparison (World Bank, from WHO's Global Health Expenditure Database; CC BY 4.0)
| File | What's in it | Use for |
|---|---|---|
| `asean_health_spending_2000_2023.csv` | 11 ASEAN countries × 2000–2023: government health spending as % of all government spending (`SH.XPD.GHED.GE.ZS`), current health spending % of GDP, out-of-pocket % of current spending, spending per person in USD. Rounded to 2 decimals | M5 |

### Map boundaries (`geo/`, from [Natural Earth](https://www.naturalearthdata.com/), public domain)
| File | TopoJSON object (`feature` in Vega-Lite) | Join key |
|---|---|---|
| `malaysia_states.topojson` (150 KB, from 1:10m Admin 1) | `states` | `properties.state` matches the `state` column in the data.gov.my files and `mnha_state_2024.csv` |
| `asean_countries.topojson` (210 KB, from 1:50m Admin 0, South-Eastern Asia incl. Timor-Leste) | `countries` | `properties.iso3` matches `iso3` in the ASEAN CSV |
| `malaysia_state_label_points.csv` | — | longitude/latitude per state, for proportional circles (M2) and labels |

Made the same way as the Week 8 studio's mapshaper steps (filter → simplify → export TopoJSON), using the TopoJSON libraries in Node.

## Things to know before you chart (found while checking)

1. **State spending is counted where the hospital is, not where patients live** (report section 4.3). So Kuala Lumpur (≈RM6,450 per person) and Putrajaya (≈RM8,280) look huge because people from nearby states use their hospitals. Say this on M1, or it looks like an error.
2. **"hospital_non_moh" beds are other *government* hospitals** (university and military), **not private hospitals**. Private beds aren't in this dataset, so call M2 "public-sector hospital beds".
3. **Healthcare staff 2020 looks broken for several states** (e.g. Perak nurses drop to 981, then Perlis jumps to 9,465). Use 2022 (or 2021) for M3 and skip 2020. Putrajaya's doctor count includes MOH headquarters staff, so consider leaving it out of per-person comparisons, or flag it.
4. **MOH programme names change between years.** 2021 operating figures are lower partly because hospital support services were moved to the development budget (Annual Report 2021 note). Compare the 7 stable programmes; keep "Other" separate.
5. **Two different "totals" exist.** The MNHA report (TEH, includes buildings and training) gives 4.65% of GDP for 2024. The WHO / World Bank "current health expenditure" leaves those out (≈3.96% for Malaysia in 2023). Use the World Bank file only to compare countries, and the MNHA files for everything about Malaysia.
6. `mnha.csv` from data.gov.my is an older version of the national accounts (e.g. 2015: RM50.26 bn vs RM50.07 bn in the 2024 report). Use the report-based files and mention the newer edition.
7. `population_state.csv` stops at 2023. For 2024 per-person values use the population column in `mnha_state_2024.csv` (same DOSM source).

## How the PDF tables were extracted
`scripts/build_mnha.py` and `scripts/build_moh_programmes.py` hold the values copied from the PDFs, plus the checks (each column sums to the published total; per-person = total ÷ population; constant = nominal ÷ deflator). Run them with `python3` to regenerate the CSVs.
