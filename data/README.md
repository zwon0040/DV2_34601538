# Data for "Malaysia's health spending: who pays and what it buys"

Every file here is either an original CSV from an open-data site (kept as published) or a table copied from an official PDF.
For the PDF tables, every column was checked against the table's own published "Total" row.
Chart ids (c1, m1 and so on) match `index.html` and `js/specs/`.

## Files

### From the Ministry of Health (MOH) National Health Accounts report
Source: [Malaysia National Health Accounts: Health Expenditure Report 2011–2024](https://www.moh.gov.my/images/04-penerbitan/laporan-mnha/MNHA%20National%20Health%20Accounts%20Health%20Expenditure%20Report%202011-2024.pdf). All money is in **RM million**.

| File | Report table | What is in it | Used by |
|---|---|---|---|
| `mnha_national_2011_2024.csv` | 4.1, 4.2, 5.1d, 8.1 | One row per year: total spending (as spent and in 2024 prices), % of GDP, per person, population, public and private split | c1 line chart, c8 waterfall, top KPI cards |
| `mnha_financing_sources_2011_2024.csv` | 5.1b, 5.1c | Who paid: 15 sources by 14 years, in RM and % of total. `payer_group` collapses them into five groups | c2 waffle, c3 slope chart |
| `mnha_functions_2011_2024.csv` | 7.1b, 7.1c | What the money bought: 11 services, with a plain-English label for each | c4 streamgraph |
| `mnha_providers_2011_2024.csv` | 6.1b, 6.1c | Where it was spent (hospitals, clinics, pharmacies and so on), total and public. Private = total minus public | c5 bump chart, c11 Marimekko |
| `mnha_oop_providers_2011_2024.csv` | 9.2c | Families' own money, by the type of private provider they paid | c6 dumbbell chart |
| `mnha_state_2024.csv` | 4.3 | 2024 spending and population by state. `state` uses data.gov.my names so it joins with the other files | m1 Dorling cartogram |

Blank cells mean "n/a" in the report (for example rehabilitative care 2013–2021).

### From the MOH Annual Reports
| File | Source | What is in it | Used by |
|---|---|---|---|
| `moh_programme_budget_2020_2025.csv` | [MOH Annual Reports](https://www.moh.gov.my/en/publications-and-reports/infographics-reports-statistics/annual-report) 2020 to 2025, Finance chapter, "Allocation and Expenditure of Operating Budget by Programme" | Operating budget allocated and spent per programme, in RM (not million). `group` keeps the stable programmes and puts the changing ones in "Other" | c7 bullet chart (2025), c10 programme-share chart (2020 vs 2025) |

### From data.gov.my and OpenDOSM (licence CC BY 4.0)
| File | Source | What is in it | Used by |
|---|---|---|---|
| `budget_allocation_moh.csv` | [data.gov.my federal_budget_moh](https://data.gov.my/data-catalogue/federal_budget_moh) | MOH budget 2015–2024 in RM: `de` is the development budget, `oe` the operating budget, split into salaries (`oe_10000`), services and supplies (`oe_20000`), assets (`oe_30000`), fixed payments (`oe_40000`) and other (`oe_50000`) | c9 budget-type lines |
| `hospital_beds_state.csv` | [data.gov.my hospital_beds](https://data.gov.my/data-catalogue/hospital_beds) | State-level rows only (district rows dropped), 2015–2022 | m2 symbol map |
| `healthcare_staff.csv` | [data.gov.my healthcare_staff](https://data.gov.my/data-catalogue/healthcare_staff) | Public-sector doctors, nurses, community nurses and dentists by state, 2014–2022 | m3 staff map |
| `population_state_2022.csv` | [OpenDOSM population_state](https://open.dosm.gov.my/data-catalogue/population_state) | 2022 population by state, **in thousands** | m2 (beds per 10,000 people) |

### International comparison (World Bank, from the WHO Global Health Expenditure Database; CC BY 4.0)
| File | What is in it | Used by |
|---|---|---|
| `asean_health_spending_2000_2023.csv` | 11 ASEAN countries, 2000–2023: government health spending as a % of all government spending, and related indicators | m4 ASEAN map |

### Map files (`geo/`)
| File | What it is | Join key |
|---|---|---|
| `malaysia_states.topojson` | State boundaries, Natural Earth 1:10m Admin 1, simplified. Object name `states` | `properties.state` matches `state` in the data files |
| `asean_countries.topojson` | South-East Asia country boundaries, Natural Earth 1:50m Admin 0, simplified. Object name `countries` | `properties.iso3` matches `iso3` in the ASEAN CSV |
| `malaysia_state_label_points.csv` | Longitude and latitude per state, for symbols and labels | `state` |
| `malaysia_dorling_positions.csv` | Circle positions for the Dorling cartogram, made by `tools/build_dorling_positions.py` | `state` |

## Things to know about the data

1. **State spending is counted where the hospital is, not where patients live** (report section 4.3). Kuala Lumpur and Putrajaya look high because people from nearby states use their hospitals. The m1 caption says so.
2. **"hospital_non_moh" beds are other government hospitals** (university and military), not private hospitals. Private beds are not in the dataset, so m2 is labelled "public hospital beds".
3. **Staff figures for 2020 look broken for several states** (for example Perak nurses drop, then Perlis jumps). The staff map therefore compares only 2014 and 2022.
4. **MOH programme names change between years.** In 2021 some hospital support costs moved to the development budget, so 2021 operating figures are lower. c10 groups small programmes and says so in its caption.
5. **Two different "totals" exist.** The National Health Accounts total includes buildings and training. The World Bank "current health expenditure" leaves those out. The World Bank file is used only to compare countries (m4); everything about Malaysia comes from the National Health Accounts.
6. `population_state_2022.csv` is 2022 only, to match the 2022 bed counts. The 2024 per-person figures use the population column in `mnha_state_2024.csv`.

## How the CSV files were made

- `tools/build_mnha.py` and `tools/build_moh_programmes.py` hold the values copied from the PDFs, plus the checks (each column adds up to the published total; per person = total ÷ population).
  Run them with `python3` to rebuild the CSVs.
- `tools/build_dorling_positions.py` builds the cartogram circle positions.
- The open-data CSVs and the TopoJSON files are not made by scripts in this repo; they are downloaded and simplified once.
