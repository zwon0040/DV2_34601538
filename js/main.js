// main.js: loads every chart into the page.
// Font names are quoted ("'Source Sans 3'") because a family name with a digit
// is invalid in a CSS font string unless quoted; Vega would then mis-measure labels.
// One shared theme keeps fonts, sizes and greys identical across all charts,
// so each spec file only describes its data and encodings.

const theme = {
  background: "#FBE9EA",
  font: "'Source Sans 3', sans-serif",
  padding: 4,
  view: { stroke: null },
  axis: {
    labelFont: "'Source Sans 3', sans-serif",
    labelFontSize: 13,
    labelColor: "#3E4C59",
    titleFont: "'Source Sans 3', sans-serif",
    titleFontSize: 12,
    titleFontWeight: 600,
    titleColor: "#52606D",
    domainColor: "#CBD2D9",
    tickColor: "#CBD2D9",
    gridColor: "#D9C6C4"
  },
  legend: {
    labelFont: "'Source Sans 3', sans-serif",
    labelFontSize: 13,
    labelColor: "#3E4C59",
    titleFont: "'Source Sans 3', sans-serif",
    titleFontSize: 12,
    titleFontWeight: 600,
    titleColor: "#3E4C59"
  },
  header: { labelFont: "'Source Sans 3', sans-serif", titleFont: "'Source Sans 3', sans-serif" },
  text: { font: "'Source Sans 3', sans-serif" },
  title: { font: "'Plus Jakarta Sans', sans-serif", anchor: "start", color: "#1F2933" }
};

// [element id, spec file]
const charts = [
  ["#c1", "js/specs/c1_per_person.vl.json"],
  ["#c2", "js/specs/c2_waffle_payers.vl.json"],
  ["#c3", "js/specs/c3_slope_shares.vl.json"],
  ["#c4", "js/specs/c4_stream_functions.vl.json"],
  ["#c5", "js/specs/c5_bump_providers.vl.json"],
  ["#c11", "js/specs/c11_marimekko_providers.vl.json"],
  ["#c6", "js/specs/c6_dumbbell_oop.vl.json"],
  ["#c7", "js/specs/c7_bullet_programmes.vl.json"],
  ["#c8", "js/specs/c8_waterfall_real_spending.vl.json"],
  ["#c9", "js/specs/c9_budget_types.vl.json"],
  ["#m1", "js/specs/m1_state_spending.vl.json"],
  ["#m2", "js/specs/m2_beds_symbols.vl.json"],
  ["#m3", "js/specs/m3_staff_map.vl.json"],
  ["#m4", "js/specs/m4_asean_priority.vl.json"]
];

// The three Malaysia maps share one "focus state". Clicking a state on any of them
// outlines that state on all three (and highlights its line in the staff chart).
// Clicking the same state again, or empty space, clears it.
const linkedMaps = ["#m1", "#m2", "#m3"];
const linkedViews = [];
let focusState = null;

function stateOf(item) {
  const d = item && item.datum;
  if (!d) return null;
  return d.state || (d.properties && d.properties.state) || null;
}

function setFocus(state) {
  focusState = state;
  for (const view of linkedViews) view.signal("focus_state", state).runAsync();
}

// Wait for the web fonts first, so Vega measures label widths with the real font.
document.fonts.ready.then(() => {
  for (const [id, spec] of charts) {
    vegaEmbed(id, spec, { actions: false, renderer: "svg", config: theme })
      .then((result) => {
        // Let the chart grow to fill its card on wide screens, up to 30% larger than designed,
        // so text inside charts never gets oversized. The SVG keeps its viewBox, so it scales evenly.
        const svg = document.querySelector(id + " svg");
        if (svg) {
          svg.style.maxWidth = Math.round(svg.width.baseVal.value * 1.3) + "px";
          svg.style.width = "100%";
        }
        if (!linkedMaps.includes(id)) return;
        linkedViews.push(result.view);
        result.view.addEventListener("click", (event, item) => {
          const state = stateOf(item);
          setFocus(state && state !== focusState && state !== "Malaysia" ? state : null);
        });
      })
      .catch((error) => console.error(id, error));
  }
});
