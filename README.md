# Where does your health ringgit go? (v2.1 story spine)

FIT3179 Data Visualisation 2 draft by Zi Cheng Wong (October 2026).
A single scrolling page about Malaysia's health spending, built with Vega-Lite 5.

## v2.1 layout

As v2.0, plus: text always on the left with a thin "story spine" line and nodes linking the text blocks, a tick from each text block to its chart, neutral charcoal chapter bands, no pull quote, and pharmacies recoloured rust to match medicines.

## v2.0 layout

Same charts and data as v1. Changes: coloured chapter band per Part (colour = that Part's main attribute), one full-width hero chart per Part (c1, c4, c9, m1), text-beside-chart rows for the other charts, and a pull quote in Part 2. Hero charts were widened to fit (see each spec's `width`).

## Run it

The page loads its data with `fetch`, so it must be served over HTTP. Opening `index.html` by double-clicking will show empty charts.

- **VS Code:** install the "Live Server" extension, right-click `index.html`, then choose "Open with Live Server".
- **Python:** run `python -m http.server` in this folder, then open http://localhost:8000.
- **GitHub Pages:** push this folder to a repo, then go to Settings → Pages → Deploy from branch (main, root).

## Folder layout

```
index.html          story text, chart titles, sources (one <div id="..."> per chart)
css/style.css       all colours, type and layout (section 1 holds the design tokens)
js/main.js          shared chart theme + list of charts to load
js/specs/*.vl.json  one Vega-Lite spec per chart (open any of them in the Vega Editor)
data/*.csv          data files (see the data README for sources)
geo/*.topojson      map boundaries from Natural Earth
```

## Charts

| id | file | idiom |
|---|---|---|
| c1 | c1_per_person | line chart (as spent vs after inflation) |
| c2 | c2_waffle_payers | waffle chart (1 square ≈ RM1 billion) |
| c3 | c3_slope_shares | slope chart (2011 vs 2024) |
| c4 | c4_stream_functions | 100% stacked area (share of spending by service) |
| c5 | c5_bump_providers | bump chart (rank over time) |
| c6 | c6_dumbbell_oop | dumbbell chart (2011 vs 2024) |
| c7 | c7_bullet_programmes | bullet chart (budget vs spent) |
| c8 | c8_waterfall_real_spending | waterfall (total spending, 2019 → 2024, with the 2022 fall) |
| c11 | c11_marimekko_providers | Marimekko (where money was spent × public vs private payer, 2024) |
| c9 | c9_budget_types | indexed line chart (2015 = 100) |
| m1 | m1_state_spending | choropleth map + linked bar chart |
| m2 | m2_beds_symbols | proportional symbol map |
| m3 | m3_staff_map | choropleth + linked indexed line chart |
| m4 | m4_asean_priority | choropleth with year slider + linked line chart |

## Colour key (same meaning on every chart)

| Colour | Meaning |
|---|---|
| Blue `#3A5FCD` | total health spending (all payers) |
| Dark green `#007A5E` | Ministry of Health / government money |
| Light green `#3DB58F` | other government bodies |
| Orange `#E69F00` | households paying out of pocket |
| Pink `#C065A6` | private insurance |
| Plum `#7D3C6E` | employers and others |
| Earth tones (sand → chocolate, rust, navy) | services in the streamgraph only (sand = background services; chocolate = buildings, rust = medicines, navy = prevention) |
| Greys | context, totals, data notes |

## Sources

See the footer of `index.html` and the data README. AI use: Claude (Anthropic) helped collect data, draft code and check grammar.
