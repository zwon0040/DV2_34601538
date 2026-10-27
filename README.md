# Malaysia's health spending: who pays and what it buys

FIT3179 Data Visualisation 2, by Wong Zi Cheng (student ID 34601538), October 2026.

A single scrolling page about Malaysia's health spending, built with Vega-Lite 5.21 (Vega 5.30, vega-embed 6.26).
Live page: https://zwon0040.github.io/DV2_34601538/

## The story

The page is written for an average Malaysian adult and follows the money in five parts.
Each part asks one question, answers it in one bold sentence, and backs it with one or more charts.

| Part | Question | Charts |
|---|---|---|
| 1 The bill keeps growing | Is Malaysia spending more on health? | c1, c8 |
| 2 Who pays the bill? | Whose money pays for health care? | c2, c3 |
| 3 What does the money buy? | What is the money spent on, and where? | c4, c5, c11, c6 |
| 4 The government's own priorities | Does the Ministry spend what it plans, and have its priorities changed? | c7, c9, c10 |
| 5 Does the money reach every state? | Is spending, bed and staff supply even across states? How does Malaysia compare in ASEAN? | m1, m2, m3, m4 |

The page ends with three takeaways: care keeps costing more, the government's share is shrinking, and families fill the gap.

## Charts

| id | file | idiom | what it shows |
|---|---|---|---|
| c1 | c1_per_person | line chart | spending per person, 2011 to 2024 |
| c8 | c8_waterfall_real_spending | waterfall chart | yearly change in total spending, 2011 to 2024 |
| c2 | c2_waffle_payers | waffle chart | who paid in 2024 (1 square is about RM1 billion) |
| c3 | c3_slope_shares | slope chart | each payer's share, 2011 vs 2024 |
| c4 | c4_stream_functions | streamgraph | spending by service, 2011 to 2024 |
| c5 | c5_bump_providers | bump chart | rank of where the money is spent |
| c11 | c11_marimekko_providers | Marimekko chart | provider size and public vs private payer, 2024 |
| c6 | c6_dumbbell_oop | dumbbell chart | what families paid at private providers, 2011 vs 2024 |
| c7 | c7_bullet_programmes | bullet chart | Ministry budget vs money spent by programme, 2025 |
| c9 | c9_budget_types | line chart | Ministry budget by type, 2015 to 2024 |
| c10 | c10_programme_shift | diverging bar chart | change in each programme's share of the budget, 2020 to 2025 |
| m1 | m1_state_spending | Dorling cartogram | spending per person (colour) and population (circle area) by state, 2024 |
| m2 | m2_beds_symbols | graduated symbol map | public hospital beds (size) and beds per 10,000 people (colour), 2022 |
| m3 | m3_staff_map | choropleth + linked line chart | change in public health staff by state, 2014 to 2022 |
| m4 | m4_asean_priority | choropleth + year slider + linked line chart | health's share of government spending in ASEAN, 2000 to 2023 |

## Interaction

- **Legends are clickable** (c2, c4, c8, c10, c11, m1, m2, m3, m4): click a colour to highlight it and fade the rest.
- **Click a state** on any of the three state maps (m1, m2, m3) to highlight it on all three. A white label shows its numbers. Click again to clear.
- **Hover** a line on the bump chart (c5) or a state on the staff map (m3) to highlight it.
- **Year slider** on the ASEAN map (m4) changes the year shown; a vertical line follows it on the line chart below.
- **Tooltips** on every chart give exact values.

## Design

- **Colours:** warm cream page (`#F4F3EC`), pale sage chart cards (`#E2EAD8`) and olive crosses on the story line (`#3F5D2C`).
  Each Part has one muted earthy colour for its title block and the line above its callouts:
  olive `#3B4D2F`, clay `#6B4A3A`, olive-gold `#5E5430`, slate teal `#2F4A47`, taupe `#4B3E36`.
- **Type:** Archivo (titles and big numbers), Plus Jakarta Sans (small labels), Source Sans 3 (body text and charts). All sans-serif, left-aligned, at most about ten words a line.
- **Layout:** text on the left with a thin "story spine" line and a cross at each text block, the chart in a card on the right.
  Top KPI cards and the closing takeaways sit in the same sage cards.
- **Data colours (one meaning each, on every chart):**

| Colour | Meaning |
|---|---|
| Blue `#3A5FCD` | total health spending, and "share increased" on c10 |
| Dark green `#007A5E` | Ministry of Health and government money |
| Light green `#3DB58F` | other government bodies |
| Orange `#E69F00` | families paying out of pocket |
| Pink `#C065A6` | private insurance |
| Plum `#7D3C6E` | employers and others |
| Earth tones (sand to chocolate, rust, navy) | services in the streamgraph only |
| Greys | context, and "share decreased" on c10 |

## Run it

The page loads its data with `fetch`, so it must be served over HTTP. Double-clicking `index.html` shows empty charts.

- **VS Code:** install "Live Server", right-click `index.html`, choose "Open with Live Server".
- **Python:** run `python -m http.server` in this folder, then open http://localhost:8000.
- **GitHub Pages:** push this folder to a repo, then Settings, Pages, Deploy from branch (main, root).

## Folder layout

```
index.html            story text, chart titles, captions and sources (one <div id="..."> per chart)
css/style.css         all colours, type and layout (design tokens at the top)
js/main.js            shared chart theme, list of charts, linked state selection
js/specs/*.vl.json    one Vega-Lite spec per chart (open any in the Vega Editor)
data/*.csv            data files (see data/README.md for sources)
geo/*.topojson        map boundaries from Natural Earth
geo/*.csv             label points and Dorling cartogram positions
tools/*.py            scripts that build the data and the cartogram positions
```

## Where the data and maps come from

- **Ministry of Health tables** (`mnha_*.csv`, `moh_programme_budget_2020_2025.csv`): the numbers were copied from tables in official PDF reports
  (National Health Accounts report 2011 to 2024; MOH Annual Reports 2020 to 2025) into `tools/build_mnha.py` and `tools/build_moh_programmes.py`.
  The scripts check that every column adds up to the total the report publishes, then write the CSV files.
  Run `python tools/build_mnha.py` to rebuild the National Health Accounts CSVs. It also writes a spare `mnha_oop_functions_2011_2024.csv`, which the page does not use.
- **Open government data** (`budget_allocation_moh.csv`, `hospital_beds_state.csv`, `healthcare_staff.csv`, `population_state_2022.csv`): downloaded from data.gov.my and OpenDOSM and kept as published.
- **ASEAN comparison** (`asean_health_spending_2000_2023.csv`): World Bank indicator from the World Health Organization's health expenditure database.
- **Map shapes** (`geo/malaysia_states.topojson`, `geo/asean_countries.topojson`): Natural Earth boundaries, simplified and saved as TopoJSON so the files are small.
  The join key is the `state` property (Malaysia) or `iso3` (ASEAN).
- **Dorling cartogram** (`geo/malaysia_dorling_positions.csv`): made by `python tools/build_dorling_positions.py .`.
  Circles start near each state's real position, are pulled together with their neighbours, then pushed apart until none overlap.

## Notes on the data

- State spending is counted where the hospital is, not where patients live, so Kuala Lumpur and Putrajaya look high.
- Hospital beds are public-sector only; private hospitals are not in the dataset.
- Staff figures for 2020 look disrupted for several states and are marked on the staff chart.
- Ministry programme names changed between years, and in 2021 some hospital costs moved to the development budget.
  The programme-share chart (c10) groups the small programmes and says so in its caption.

## Sources and AI use

Full source list is in the footer of `index.html` and in `data/README.md`.
AI use: Claude (Anthropic) helped collect data, draft code, write and check text, review layout and colour choices, and compare the page with the assignment rubric. All figures come from the sources listed.
