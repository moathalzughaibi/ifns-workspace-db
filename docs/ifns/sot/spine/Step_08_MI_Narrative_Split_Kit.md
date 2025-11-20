# Step 08 – MI Narrative Split Kit

This file helps you break the long **`01 – Narrative & Intent`** page for **Step 08 – Modeling Intelligence (MI)**

into smaller child pages in Notion. All content below is taken from your existing Notion export and regrouped

by headings only (no new concepts added).


## A. Parent page – `01 – Narrative & Intent` (new layout)

In Notion, keep `01 – Narrative & Intent` as a short overview and index page. Replace its body with something like:

```markdown
# 01 – Narrative & Intent

This step defines **Modeling Intelligence (MI)** — the cognitive heart of IFNS.

MI is responsible for turning the rich representations produced by DIL into actionable signals, 
scores, and decisions, governed by clear contracts and promotion rules.


Use this page as a **map** only. The detailed narrative now lives in the child pages below.

## Child pages

1. **MI – 1. Role in the IFNS Stack**
2. **MI – 2. Model Families and Roles**
3. **MI – 3. Model Registry**
4. **MI – 4. Training & Evaluation Pipelines**
5. **MI – 5. Calibration, Constraints, and Robustness**
6. **MI – 6. SxE Representation of MI**
7. **MI – 7. Promotion Path and Lifecycle**

Each child page should appear as a Notion subpage under this one.
```

## B. Child pages (copy each into its own Notion page)


### B.1 `MI – 1. Role in the IFNS Stack`

```markdown
# MI – 1. Role in the IFNS Stack

MI sits between DIL and EI:

- **Upstream / Inputs**
  - Feature frameworks and labels from DIL (e.g., TREND_MTF, CANDLE_SHAPE, STRUCTURE_MTF, VOL_LIQ).
  - Training and evaluation datasets defined in DIL’s dataset schemas.
  - Regime and structural tags (from MSA) that can be used as model inputs or segmentation keys.

- **Downstream / Outputs**
  - Predictions and scores (e.g., directional probabilities, expected returns, risk-adjusted scores).
  - Uncertainty estimates or confidence scores.

  - Regime or structure-aware signals (e.g., strategy recommendations conditioned on MSA context).
  - Artifacts and metrics that feed Backtesting & Evaluation (Stage 4) and SEL.

MI’s primary responsibilities:

- Define **model families** and their roles.
- Provide **reproducible training pipelines**.
- Maintain a **Model Registry** with robust metadata and statuses.
- Enforce **evaluation and calibration standards** before models can influence execution.
```

### B.2 `MI – 2. Model Families and Roles`

```markdown
# MI – 2. Model Families and Roles

IFNS organizes models into **families** based on their purpose and behavior. Examples include:

1. **Alpha / Directional Models**
   - Predict direction or return over a horizon (e.g., probability of upward move in the next H bars).
   - Drive primary trade entry and position sizing decisions.

2. **Structure & Regime Models**
   - Infer market regimes (trending vs. mean-reverting, high vs. low volatility).
   - Interpret STRUCTURE_MTF features to classify structural states (e.g., breakout, consolidation, topping).

3. **Risk & Volatility Models**
   - Forecast volatility, drawdown risk, or tail risk.
   - Feed into risk envelopes and position limits.

4. **Execution Cost / Slippage Models**
   - Estimate expected slippage, market impact, and execution quality.
   - Influence routing decisions and time-slicing strategies.

5. **Auxiliary / Diagnostic Models**
   - Detect anomalies in data, model behavior, or environment conditions.
   - Support SEL and incident detection.

Each model family is defined by:

- **Input feature sets** (which feature frameworks and versions).
- **Label definitions** (what future outcome is predicted).
- **Intended role** (alpha, risk, structure, etc.).
- **Acceptable algorithms** (e.g., tree-based, linear, neural, hybrid).
- **Evaluation metrics** that matter for that role (e.g., directional accuracy, calibration error, drawdown profile).

Model families provide **templates** that individual models (with specific hyperparameters, training periods, and feature subsets) can instantiate.
```

### B.3 `MI – 3. Model Registry`

```markdown
# MI – 3. Model Registry

The **Model Registry** is the authoritative catalog of all models in IFNS. It is a structured registry rather than a folder of arbitrary files.

Each model entry includes at least:

- **Model ID and name**
- **Family and role** (e.g., Alpha_MTF_V1, Volatility_Forecast_V2)
- **Version** (semantic versioning where applicable)
- **Input dataset(s)** (dataset IDs from DIL)
- **Feature frameworks and versions**
- **Label definition(s)**
- **Training period(s) and universe**
- **Training configuration**
  - Algorithm type,
  - Hyperparameters,
  - Regularization/constraints.
- **Evaluation metrics**
  - On training, validation, and test sets.
- **Calibration metrics**
  - For probabilistic models (e.g., Brier score, calibration curves).
- **Status**
  - `draft`, `candidate`, `baseline`, `canary`, `promoted`, `deprecated`.
- **Operational deployment info**
  - Where and how it is used (offline, paper, live),

  - Associated gates and risk envelopes.

The Model Registry is the **single source of truth** for “what models exist, what they do, and whether they are allowed to influence decisions”.
```

### B.4 `MI – 4. Training & Evaluation Pipelines`

```markdown
# MI – 4. Training & Evaluation Pipelines

MI defines **standardized training pipelines** that take DIL datasets and produce models plus metrics.

Key properties:

- **Reproducible**
  - Training jobs are fully specified (config, code version, data snapshot).
  - Jobs can be re-run to confirm results.

- **Config-driven**
  - Training specifications live in structured configs (e.g., `Model_Training_Spec` tables).
  - Hyperparameter ranges, seeds, and stopping criteria are defined explicitly.

- **Metrics-rich**
  - Metrics include:
    - Predictive performance (e.g., AUC, accuracy, log loss),
    - Risk-related measures (e.g., drawdown of strategy prototypes),
    - Stability metrics (e.g., performance consistency across folds),
    - Calibration quality (for probabilistic outputs).

- **Evaluation-first**
  - Models are not merely “trained”; they are evaluated via:
    - Cross-validation or rolling windows,
    - Out-of-sample segments,
    - Scenario-based stress testing.

Results of each training run are:

- Logged to an **Experiments or Training Runs table**,
- Linked back to the Model Registry entry,
- Used as evidence for promotion decisions in SEL.
```

### B.5 `MI – 5. Calibration, Constraints, and Robustness`

```markdown
# MI – 5. Calibration, Constraints, and Robustness

MI places strong emphasis on **calibration and robustness**, not just raw predictive strength.

- **Calibration**
  - For probabilistic outputs, predicted probabilities must align with realized frequencies.
  - Calibration plots and metrics are stored and surfaced to SxE.

- **Constraints**
  - Models should adhere to constraints appropriate for their role, such as:
    - Monotonic constraints for certain risk features,
    - Bounds on position recommendations,
    - Limits on sensitivity to specific inputs (where required).

- **Robustness**
  - Models should be stress-tested on:
    - Different regimes (e.g., high vs. low volatility),
    - Crash-like scenarios,
    - Thinner liquidity conditions.
  - Robustness metrics are captured and used in promotion decisions.

Calibration and robustness information must be **inspectable** in Admin and Mirror, so that operators understand not just “how strong” a model is, but **where it might break**.
```

### B.6 `MI – 6. SxE Representation of MI`

```markdown
# MI – 6. SxE Representation of MI

MI is deeply integrated into SxE:

- **Mirror**
  - Provides model-level views:
    - Active and inactive models by family and status,
    - Key performance metrics,
    - Model health and drift indicators.
  - Presents aggregated views:
    - How much of current strategy behavior is driven by each model or family,
    - Which models are under review or in canary mode.

- **Admin**
  - Provides:
    - Read/write access (under governance) to:

      - Model Registry entries (excluding immutable audit fields),
      - Model statuses (promotion/demotion actions via approved workflows).
    - Workflows for:
      - Approving a model to enter canary or promoted status,
      - Deprecating outdated models,
      - Attaching evidence (backtests, paper runs, incidents) to decisions.

- **Telemetry & Registries**
  - Training runs, experiments, and model promotions/rollbacks generate events that are:
    - Stored in telemetry streams,
    - Linked to Model Registry entries,
    - Visible in incident and change logs.

MI is **not invisible**: it has a clear presence in the operator experience, and its lifecycle is part of the governance story.
```

### B.7 `MI – 7. Promotion Path and Lifecycle`

```markdown
# MI – 7. Promotion Path and Lifecycle

Models in IFNS follow a **controlled lifecycle**:

1. **Draft**
   - Newly trained models, under research.
   - Not allowed to influence paper or live decisions.

2. **Candidate**
   - Models that meet minimal performance standards in backtests and validation.
   - Eligible for deeper evaluation and scenario testing.

3. **Baseline**
   - Reference models used for comparison.
   - Provide a floor of acceptable performance (e.g., simple benchmarks).

4. **Canary**
   - Models deployed in **paper** or **limited-live** contexts with small capital and strict monitoring.
   - Subject to tight KPIs and fast rollback rules.

5. **Promoted**
   - Models with sufficient evidence across backtests, paper, and live canary phases.

   - Can drive a meaningful portion of production behavior.

6. **Deprecated**
   - Models retired from active use, but preserved for audit and historical analysis.

SEL and DRA use this lifecycle to decide:

- Which models can provide signals to EI and MSI.
- How much weight to give each model.
- When to trigger retraining or demotion.

---
```