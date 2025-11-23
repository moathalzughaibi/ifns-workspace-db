# Step 10 – MSA Narrative Split Kit

This file helps you break the **`01 – Narrative & Intent`** page for **Step 10 – Market Structural Awareness (MSA)**

into smaller child pages in Notion. All content below is taken from your existing Notion export and regrouped

by headings only (no new concepts added).


## A. Parent page – `01 – Narrative & Intent` (new layout)

In Notion, keep `01 – Narrative & Intent` as a short overview and index page. Replace its body with something like:

```markdown
# 01 – Narrative & Intent

This step defines **Market Structural Awareness (MSA)** — the layer of IFNS that cares about the

shape, regimes, and *context* of the market, not just immediate price moves. It provides a shared

structural language (swings, trends, regimes) that DIL, MI, EI, DRA, and SEL can all rely on.


Use this page as a **map** only. The detailed narrative now lives in the child pages below.

## Child pages

1. **MSA – 1. Role in the IFNS Stack**
2. **MSA – 2. Structural Ontology: Swings, Trends, and Regimes**
3. **MSA – 3. STRUCTURE_MTF and Derived Feature Frameworks**
4. **MSA – 4. Structure-Aware Modeling and MSI**
5. **MSA – 5. Structural Constraints for Risk and Execution**
6. **MSA – 6. SxE Representation of MSA**

Each child page should appear as a Notion subpage under this one.
```

## B. Child pages (copy each into its own Notion page)


### B.1 `MSA – 1. Role in the IFNS Stack`

```markdown
# MSA – 1. Role in the IFNS Stack

MSA bridges the gap between **raw price action** and **strategic decision-making**:

- It consumes:
  - Canonical bars and derived structure features (from DIL’s STRUCTURE_MTF, TREND_MTF, VOL_LIQ frameworks).
  - Historical context for swing points, regimes, and volatility states.

- It produces:

  - **Structural tags** at each point in time (e.g., “HHHL uptrend”, “range-bound”, “breakdown from range”).
  - **Regime labels** (e.g., trending vs. mean-reverting, high-vol vs. low-vol, stable vs. structurally stressed).
  - Optional **structure-aware signals** (e.g., “pullback within uptrend”, “failed breakout”).

MSA’s outputs influence:

- How MI models are trained and interpreted (e.g., regime-conditioned models).
- How MSI integrates multiple models and signals (e.g., preferring certain models in certain regimes).
- How DRA and EI behave (e.g., tightening risk or execution constraints in structurally stressed conditions).

MSA ensures that IFNS does not treat all time periods as interchangeable — the system is aware of *where* in the structural map it is operating.

---
```

### B.2 `MSA – 2. Structural Ontology: Swings, Trends, and Regimes`

```markdown
# MSA – 2. Structural Ontology: Swings, Trends, and Regimes

MSA uses a clear structural ontology so that all components talk about structure in the same language.

Key elements:

1. **Swing Points**
   - **Major swing highs/lows** – large, structurally significant turning points.
   - **Primary swing highs/lows** – intermediate-level swings within major trends.
   - **Minor swing highs/lows** – local fluctuations within primary swings.

2. **Trend States**
   - Higher highs / higher lows (**HHHL**) – canonical uptrend.
   - Lower highs / lower lows (**LHLL**) – canonical downtrend.
   - Higher highs / lower lows or similar mixed patterns – **transition or range** states.

3. **Regime Labels**

   - **Trend vs. Range**:
     - Trending (strong directional bias).
     - Range-bound (oscillating within a defined band).
   - **Volatility**:
     - High-vol regime.
     - Low-vol regime.
   - **Liquidity**:
     - Deep/liquid vs. thin/fragile.
   - **Structural stress**:
     - Breakout/breakdown zones, structural gaps, halted or fragmented trading.

4. **Multi-Timeframe Context**
   - Each instrument can have separate but related structure labels at:
     - Short-term (e.g., intraday),
     - Medium-term (e.g., swing),
     - Long-term (e.g., positional).

The ontology is encoded in **STRUCTURE_MTF** and **REGIME_TAGS** feature frameworks, allowing models and policies to reason over structure in a consistent way.

---
```

### B.3 `MSA – 3. STRUCTURE_MTF and Derived Feature Frameworks`

```markdown
# MSA – 3. STRUCTURE_MTF and Derived Feature Frameworks

MSA is built on DIL’s **STRUCTURE_MTF** and related frameworks, which translate raw prices into structured features and labels.

Key components:

- **STRUCTURE_MTF**
  - Identifies swing highs/lows at multiple timeframes.
  - Computes trend state tags (HHHL, LHLL, range, transition).
  - Tracks distance to key structural levels (previous major high/low, breakout levels).

- **REGIME_TAGS**
  - Combines STRUCTURE_MTF, TREND_MTF, and VOL_LIQ to classify regimes (e.g., “high-vol uptrend”, “low-vol range”).

- **STRUCTURE_EVENTS**
  - Optional event stream describing:
    - Breakouts above previous highs,
    - Breakdowns below previous lows,
    - Tests and failures of significant levels.

These frameworks are used by:

- MI (structure-aware models),
- MSI (structure-informed integration and gating),
- DRA (structure-aware risk and allocation),
- SxE (visualizations of structural state for operators).

---
```

### B.4 `MSA – 4. Structure-Aware Modeling and MSI`

```markdown
# MSA – 4. Structure-Aware Modeling and MSI

MSA has two modes of interaction with MI and MSI:

1. **Conditioning**
   - Models are trained and evaluated **conditional on structure**:
     - Separate models per regime (e.g., trending vs. range).
     - Models that learn regime-specific behaviors (e.g., signals only active in pullbacks within trends).
   - Model performance is tracked by regime in backtests and live telemetry.

2. **Gating & Weighting**
   - MSI uses structural tags as **gating variables**:
     - Certain signals only allowed in specific structural states.
     - Model weights adjusted based on regime (e.g., giving more weight to certain models in high-vol regimes).
   - Structural states can trigger changes in:
     - Position sizing guidelines,
     - Allowed leverage or exposure,
     - Execution style (e.g., more cautious in fragile structures).

MSA thus ensures that the **same signal is not interpreted the same way** in completely different structural contexts.

---
```

### B.5 `MSA – 5. Structural Constraints for Risk and Execution`

```markdown
# MSA – 5. Structural Constraints for Risk and Execution

Market structure is also a **risk and execution constraint**, not just a modeling input.

Examples of structural constraints:

- **Structural No-Trade Zones**
  - Avoid or reduce activity:

    - Immediately after major breakouts/breakdowns until structure stabilizes.
    - In extremely illiquid or structurally stressed regimes.

- **Position Management Rules**
  - Tighten stops or reduce position sizes when:
    - Volatility spikes above a threshold within a given structure.
    - The market transitions from trend to range or vice versa.

- **Time-of-Structure Constraints**
  - Adjust behavior around key structural events:
    - Pre-/post-earnings or macro events tied to structural resets.
    - Opening and closing auction regimes with structural gaps.

These constraints are encoded in DRA and execution policies, but **MSA provides the structural signals** that drive them.

---
```

### B.6 `MSA – 6. SxE Representation of MSA`

```markdown
# MSA – 6. SxE Representation of MSA

MSA has a strong visual and analytical presence in SxE surfaces:

- **Mirror**
  - Structural overview panels:
    - Current regime and trend state per instrument/universe.
    - Distribution of capital and risk exposure by regime.
  - Structural event timelines:
    - Major breakouts/breakdowns, regime shifts, and their impact on performance.
  - “Structure vs. performance” views:
    - How strategies behave in different regimes.

- **Admin**
  - Structural settings and thresholds:
    - Parameters for swing detection (lookback windows, sensitivity).
    - Regime definition thresholds (trend strength, volatility bands).
  - Structural constraint policies:
    - No-trade zones,
    - Structural risk adjustment rules,
    - Regime-based exposure caps.

  - Audit history for changes to structural definitions or thresholds.

MSA’s SxE representation ensures that operators can **see, adjust, and trust** the way structure is defined and used in IFNS.

---
```
