# Step 11 – MSI Narrative Split Kit

This file helps you break the **`01 – Narrative & Intent`** page for **Step 11 – Model & Signal Integration (MSI)**

into smaller child pages in Notion. All content below is taken from your existing Notion export and regrouped

by headings only (no new concepts added).


## A. Parent page – `01 – Narrative & Intent` (new layout)

In Notion, keep `01 – Narrative & Intent` as a short overview and index page. Replace its body with something like:

```markdown
# 01 – Narrative & Intent

This step defines **Model & Signal Integration (MSI)** — the layer of IFNS that consolidates

model outputs and contextual signals into **coherent, conflict-resolved decision proposals**.

Where DIL prepares data, MI produces predictions, and MSA provides structure, MSI is the place

where these views are weighted, combined, and turned into something EI and DRA can act on.


Use this page as a **map** only. The detailed narrative now lives in the child pages below.

## Child pages

1. **MSI – 1. Role in the IFNS Stack**
2. **MSI – 2. Integration Patterns**
3. **MSI – 3. MSI Contracts: From Signals to Proposals**
4. **MSI – 4. Policy-Driven Integration Logic**
5. **MSI – 5. Relationship to SEL and DRA**
6. **MSI – 6. SxE Representation of MSI**

Each child page should appear as a Notion subpage under this one.
```

## B. Child pages (copy each into its own Notion page)


### B.1 `MSI – 1. Role in the IFNS Stack`

```markdown
# MSI – 1. Role in the IFNS Stack

MSI sits between the **Modeling Intelligence** layer and the **Decision & Risk / Execution** layers:

- **Inputs**
  - Model signals from MI (via the Signal API).
  - Structural and regime tags from MSA (STRUCTURE_MTF, REGIME_TAGS).
  - Contextual data (e.g., volatility and liquidity features from DIL).
  - Model metadata from the Model Registry (roles, families, statuses, strengths and weaknesses).

- **Outputs**

  - Consolidated **decision proposals** per symbol/time:
    - Directional view (e.g., long/short/flat),
    - Strength or conviction score,
    - Time horizon or holding period hints,
    - Any auxiliary information (e.g., preferred execution style hints).
  - Additional **diagnostics**:
    - Which models contributed and how,
    - Where disagreements occurred,
    - Indicators of uncertainty.

MSI does not execute trades or enforce risk limits. Instead, it produces a **structured proposal** that DRA evaluates under risk envelopes and that EI turns into concrete execution actions if allowed.

---
```

### B.2 `MSI – 2. Integration Patterns`

```markdown
# MSI – 2. Integration Patterns

MSI supports several core integration patterns, which can be combined and configured:

1. **Weighted Averaging / Voting**
   - Each model outputs a prediction (e.g., probability, expected return).
   - MSI applies model-specific weights (by family, regime, recency of evidence).
   - Produces a single aggregate score or probability.
   - May use:
     - Simple weighted average,
     - Bayesian-style combinations,
     - Ensemble voting (majority, plurality, or threshold-based).

2. **Role-Based Integration**
   - Models are assigned **roles** (e.g., “primary directional”, “confirmation”, “risk filter”, “structure-aware overlay”).
   - MSI uses role logic, such as:
     - Only act when at least one primary model and one confirmation model agree.
     - Use risk models to modulate sizing, not direction.

3. **Regime-Conditioned Integration**

   - Based on MSA regime tags:
     - Different model subsets are active in different regimes.
     - Weights or voting rules change across regimes.
   - This avoids overusing models that are known to perform poorly in specific structural states.

4. **Conflict Detection & Resolution**
   - MSI defines what constitutes a **conflict** (e.g., models disagree strongly on direction).
   - Possible responses:
     - Stand down (no-trade proposal),
     - Reduce conviction/sizing,
     - Escalate to SEL or mark for investigation.

5. **Confidence & Uncertainty Modeling**
   - MSI aggregates model-level uncertainties into a **composite confidence score**.
   - Low confidence reduces allowed risk or suggests no-trade proposals.

These patterns are encoded as **MSI policies** and can be tuned based on performance and risk appetite.

---
```

### B.3 `MSI – 3. MSI Contracts: From Signals to Proposals`

```markdown
# MSI – 3. MSI Contracts: From Signals to Proposals

MSI operates under explicit data contracts.

**Inputs: Model Signal Records**

Each model signal record (from MI) includes at minimum:

- `ts`, `symbol`,
- `model_id`, `model_version`, `model_family`,
- `prediction` (score, probability, expected return),
- `horizon` (time or bars),
- Optional:
  - `confidence` or uncertainty measures,
  - regime or structure hints already encoded by the model.

**Inputs: Context Records**

- Structural tags:
  - `structure_state_short`, `structure_state_medium`, `structure_state_long`,
  - `regime_tag` (e.g., “high-vol-trend”, “low-vol-range”, etc.).

- Context features:
  - Volatility, liquidity summaries,
  - Any relevant DIL features that MSI uses directly.

**Outputs: Decision Proposal Records**

A typical MSI output record contains:

- `ts`, `symbol`,
- `msi_id` or policy version identifier,
- `direction_proposed` (long/short/flat),
- `score` or conviction indicator,
- `effective_horizon`,
- `active_models` (list or summarized representation),
- `disagreement_metric` (how much models differ),
- Optional:
  - `structure_context` (snapshot of relevant structural tags),
  - `policy_flags` (e.g., “reduced_size_due_to_conflict”).

These outputs are the **inputs to DRA**. DRA reads proposals and decides whether they are allowed under current risk envelopes and capital constraints.

---
```

### B.4 `MSI – 4. Policy-Driven Integration Logic`

```markdown
# MSI – 4. Policy-Driven Integration Logic

MSI is governed by **integration policies**, not hardcoded rules.

Examples of policy elements:

- **Model eligibility rules**
  - Only consider models with status `promoted` or `canary` (with additional constraints).
  - Restrict certain models to specific regimes, instruments, or environments.

- **Weighting and aggregation policies**
  - Weight by:
    - Historical performance in similar regimes,
    - Recency of successful evidence,
    - Family role (primary vs. secondary).
  - Cap the influence of any single model to avoid over-concentration.

- **Conflict thresholds**
  - Define thresholds for:
    - Directional disagreement (e.g., probability mass on opposing directions).

    - Confidence mismatch (e.g., high-confidence disagreement vs. low-confidence noise).
  - When exceeded, trigger:
    - No-trade proposals,
    - Reduced-size proposals,
    - Flags to SEL for investigation.

- **Regime transitions**
  - Define how quickly MSI adapts to regime changes:
    - Immediate switch vs. transitional blending.
    - Cooldown periods during structural transitions.

These policies are stored in structured forms (tables/JSON) and surfaced in Admin, so operators can adjust them under governance rules.

---
```

### B.5 `MSI – 5. Relationship to SEL and DRA`

```markdown
# MSI – 5. Relationship to SEL and DRA

MSI interacts closely with **Self-Evaluation & Learning (SEL)** and **Decision & Risk Architecture (DRA)**:

- MSI is the **front-end** integrator:
  - Produces best-effort decision proposals based on current models and policies.

- DRA is the **risk gate**:
  - Takes MSI proposals and decides:
    - Whether they fit within the risk envelope.
    - How much capital to allocate.
    - Whether environment state (kill switch, cooldown) allows execution.

- SEL is the **evaluation and learning loop**:
  - Observes how MSI’s proposals perform over time.
  - Assesses which integration patterns and policies are most effective.
  - Recommends or triggers updates to MSI policies and model weights.

MSI must therefore:

- Emit telemetry that SEL can analyze (e.g., proposals vs. realized outcomes).
- Keep integration behavior **stable and interpretable** over time so that SEL’s inferences are meaningful.

---
```

### B.6 `MSI – 6. SxE Representation of MSI`

```markdown
# MSI – 6. SxE Representation of MSI

MSI is a key part of the system-to-experience story.

- **Mirror**
  - MSI overview dashboards:
    - Which models are currently active and with what weights.
    - How often MSI is proposing trades vs. standing down.
    - Performance of MSI decisions over time (hit rates, TE, risk-adjusted returns).
  - Conflict and uncertainty indicators:
    - Frequency and impact of conflicts between models.
    - Times when MSI chose no-trade due to conflicts.

- **Admin**
  - **MSI Policy Console**:
    - View and edit (under governance) integration policies:
      - Model eligibility rules,
      - Weighting schemes,
      - Conflict thresholds,
      - Regime transition behaviors.
  - **MSI Diagnostics View**:
    - Inspect specific decisions:
      - Which models contributed,
      - How their outputs were combined,
      - Why a particular direction and size were proposed.

MSI’s SxE presence ensures operators can understand how the “collective mind” of the models behaves and can adjust it with traceable changes.

---
```
