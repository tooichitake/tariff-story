# Stakeholder Persona & User Stories

_Project: The Tariff Tax — Who Pays?_
_Assessment: AT3 — The Data Narrative Studio (Part 3, UTS 2026)_

---

## Primary Stakeholder Persona

### "President of the United States" — The Reluctant Decider

| Attribute | Value |
|---|---|
| Role | President of the United States (2025–) |
| Decision horizon | 90 days (Section 122 expires 2026-07-24) |
| Daily consumption | ~6 hours of briefings; scans, rarely reads |
| Data literacy | High for politics, moderate for economics; trusts visuals over tables |
| Reading style | **Headline-first**, then verdict, then evidence if needed |
| Attention floor | Must understand thesis in **≤30 seconds** or closes the tab |
| Success metric | Make a defensible decision by July 24 that can be communicated to voters and markets simultaneously |

### Context — What's on their desk right now

- Tariffs raised **$364B/yr** in customs revenue — the most aggressive tariff schedule in a century.
- Supreme Court struck down the IEEPA authority (2026-02-20); Section 122 is the current legal vehicle.
- Fed calls the inflation shock **"a one-time price level shift"** — not sustained inflation.
- Manufacturing employment is down ~97K since Jan 2025 (BLS MANEMP: 12,673K → 12,576K through Feb 2026) despite $1T+ in reshoring announcements.
- **The political math**: the bottom income decile is losing 1.14% of income; the top decile 0.36%. The policy is regressive — and voters know it.

### Pain Points

1. Every advisor pitches either "kill the tariffs" (economists) or "extend them" (political base). Nobody presents **the distributional truth** side-by-side with the revenue truth.
2. Dashboards either bury the headline in 30 charts or oversimplify to "big number go up/down."
3. **Trust deficit**: any briefing that looks partisan is ignored. Data must feel like the Fed or CBO wrote it, not a lobby group.

### Why This Audience Justifies the Narrative Arc

Chose **What → So What → What Next** (classic executive efficiency arc) because:
- The President is not a data scientist — they want the thesis, the stakes, and the decision in that order.
- The arc ends with prescription, not exploration (Martini Glass would hand them a sandbox they won't use).
- Not Detective — we don't have an "anomaly" to uncover; the facts are public.
- Not Sparkline — we need emotional gradient across 4 acts, not a single gap.

### MDSI Persona Framework (OCEAN anchor for the team)

| Trait | Score for the stakeholder | Implication for our design |
|---|---|---|
| Openness | Low–Medium | Avoid novel chart types; use bar, line, map — not sankey or radial |
| Conscientiousness | High | Every claim must be cited; no unsourced rhetoric |
| Extraversion | High | Narrative language, direct address ("Mr. President"), rhetorical questions work |
| Agreeableness | Low | Will dismiss empathy without evidence; pair every heart-string beat with a number |
| Neuroticism | High (under pressure) | Urgency cues welcome (countdown), panic cues counterproductive (avoid flashing red) |

---

## User Stories

Each story follows: `As <role>, I want <capability>, so that <benefit>.`
Plus **Acceptance Criteria** (how we verify it works) and **Definition of Done** (when the story is closeable).

---

### US-1 — Grasp the scale in under 30 seconds

> _As the President, I want to see how big the tariff shift is at a glance, so that I can decide whether to keep reading._

**Acceptance Criteria:**
- Hook visible above the fold on a 1440×900 viewport shows **one dominant number** (tariff revenue or rate) with a one-sentence subtitle.
- Act I tariff timeline shows the 2024→2026 arc with ≥3 annotated turning points.
- A non-expert reader can answer "did tariffs go up or down, by roughly how much?" within 30 seconds.

**Definition of Done:**
- Hook loads in < 3s on a cold cache.
- Pair-test with one non-economist reader confirms they can state the thesis after scrolling to the end of Act I.

---

### US-2 — Understand who actually pays

> _As the President, I want to see the distributional burden by income group, so that I can judge the fairness of the current policy._

**Acceptance Criteria:**
- A single chart shows all 10 income deciles' income loss (%) side-by-side.
- The chart's declarative title states the punch-line ("3.2x more for the poorest").
- A scenario toggle lets me compare Current Policy vs. IEEPA Upheld.
- A secondary view toggle switches % → USD cost per household.
- Hovering reveals the product categories driving each decile's loss.

**Definition of Done:**
- Chart matches viz3_who_pays.csv data exactly; no hardcoded figures.
- Bottom/top ratio computed dynamically (not hardcoded as 3.2x).
- Supporting visuals reinforce the ratio without duplicating the bar chart: the Act II income pyramid (Census HINC-06) shows where the bill lands in the distribution; the Act IV Scenario × Decile heatmap shows that the regressive gap holds across every policy scenario. (A 100-person pictogram lived in Act II in an earlier iteration — it was re-purposed into the Act IV heatmap to avoid telling the same story twice.)

---

### US-3 — Audit the trade-offs honestly

> _As the President, I want to see what the tariffs bought alongside what they cost, so that I can't be accused of one-sided advice._

**Acceptance Criteria:**
- Act III opens with a **Promise vs. Reality** scorecard listing ≥4 promises (revenue, deficit, jobs, leverage) with each row's actual outcome and verdict color.
- Gains (revenue up 4.4x, negotiating leverage, reshoring announcements) appear with the same visual weight as losses (manufacturing jobs, import collapse).
- Supporting charts are reachable via expander — they don't flood the primary view.

**Definition of Done:**
- No bullet point is a bare claim; each links to either a viz column or a cited source.
- The Fed's "one-time price shift" framing (the post-August-2025 replacement for the earlier "transitory" language) is named explicitly in the Act II intro and addressed, not ignored: "Even if the Fed is right that this is a one-time price shift, the bill is still regressive."

---

### US-4 — Explore "what if" without reading the appendix

> _As the President, I want to drag a slider to see the consequences of raising or lowering the tariff rate, so that I can evaluate options quickly._

**Acceptance Criteria:**
- Slider covers the realistic range (0% – 25% effective).
- Moving the slider updates all 10 decile burden bars in real-time (< 200ms).
- The slider's current position is shown relative to the 5 discrete policy scenarios (let expire / 10% extension / 15% extension / targeted S232 / IEEPA restore).

**Definition of Done:**
- No page reload.
- Edge cases (0%, 25%) produce sane values (no negative burdens, no NaN).

---

### US-5 — Drill into any specific event

> _As the President, I want to click any key event (Liberation Day, Geneva talks, SCOTUS ruling) and see how the economy responded around that date, so that I can sanity-check whether a single event drove the outcome._

**Acceptance Criteria:**
- Sidebar event dropdown lists all ~31 events with dates.
- Selecting an event:
  1. Highlights the event date on every time-series chart with a subtle vertical band.
  2. **Filters** time-series charts to a ±N-day window around that date.
  3. Filters the Act II price-impact chart to only categories materially affected by the event (via `affected_categories` column).
  4. Displays a **sidebar narrative block** with a real event photo (for the 6 priority events) and a one-paragraph summary.

**Definition of Done:**
- Selecting "None" restores full-range views.
- The narrative block shows source attribution for the photo.

---

### US-6 — Trust the data

> _As the President, I want to see where every number came from, so that I can defend the briefing in a press conference tomorrow._

**Acceptance Criteria:**
- Each viz file has a `source` column or a footer citation.
- README Credits section lists every dataset with provenance and every image with license + author.
- No narrative claim (e.g. "$50B in reshoring announced") appears without either a `source_url` in key_events.csv or being removed from the app.

**Definition of Done:**
- Every dataset listed in `Instructions.md` "Dataset Inventory" (27+ rows) has a traceable `File Location` and `Source` column — provenance lives there, not inside every joined CSV (only `viz1_tariff_market_fear.csv` and `viz7_whatif.csv` carry inline `source` columns; the rest inherit provenance from their input files in `data/raw/`).
- Key events carry inline `source_url` in `data/reference/key_events.csv`; the sidebar event card renders the attribution link.
- External reviewer can trace any on-screen number to a dataset path in under 2 minutes via the Instructions Dataset Inventory.

---

## Out-of-Scope for This Iteration

- **Voter-facing version** — the framing ("Mr. President") is stakeholder-specific. A public-facing cut would re-skin with second-person language and would trade some editorial polish for accessibility on mobile.
- **Continuous data refresh** — all CSVs are static snapshots through Feb 2026. A live pipeline (FRED API + scheduled re-joins) is out-of-scope but noted in the README reproduce section.
- **Policy recommendation engine** — the app surfaces trade-offs; it does not prescribe a rate. That is deliberately the President's decision, not the analyst's.
