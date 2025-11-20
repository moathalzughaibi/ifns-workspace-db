# Step 13 – SEL Narrative Split Kit

This file helps you break the long **`01 – Narrative & Intent`** page for **Step 13 – Self‑Evaluation & Learning (SEL)**

into smaller child pages in Notion. All content below is taken from your existing Notion export and regrouped

by headings only (no new concepts added).


## A. Parent page – `01 – Narrative & Intent` (new layout)

In Notion, keep `01 – Narrative & Intent` as a short overview and index page. Replace its body with something like:

```markdown
# 01 – Narrative & Intent

This step defines **Self‑Evaluation & Learning (SEL)** — the meta‑layer that helps IFNS learn from its own

history. SEL turns backtest results, paper runs, live telemetry, incidents, and operator feedback into structured

decisions about what to retrain, promote, roll back, or retire.


Use this page as a **map** only. The detailed narrative now lives in the child pages below.

## Child pages

1. **SEL – 1. Role in the IFNS Stack**
2. **SEL – 2. The Continuous Learning Loop**
3. **SEL – 3. Evidence, Metrics, and Learning Artifacts**
4. **SEL – 4. Retraining, Refresh, and Experiment Cycles**
5. **SEL – 5. Learning‑Driven Promotions, Rollbacks, and Policy Updates**
6. **SEL – 6. SxE Representation of SEL**

Each child page should appear as a Notion subpage under this one.
```

## B. Child pages (copy each into its own Notion page)


### B.1 `SEL – 1. Role in the IFNS Stack`

```markdown
# SEL – 1. Role in the IFNS Stack

SEL sits above all other layers as the **meta‑observer and planner**:

- **Inputs**
  - Backtest metrics and diagnostics (from Stage 4).
  - Paper‑run and live‑run KPIs and telemetry (from Stages 6 and 7).
  - Execution metrics (slippage, TE, fill quality).

  - Risk metrics (envelope usage, breaches, kill switch and cooldown events).
  - Incident logs, reasoning reports, and operator feedback.

- **Outputs**
  - **Learning decisions and recommendations**, such as:
    - Retrain or refresh specific models or families.
    - Change MSI weighting or conflict rules.
    - Adjust risk envelopes or gate thresholds.
    - Refine DIL feature frameworks or labeling policies.
  - **Promotion and rollback proposals** for models and strategies.
  - **Roadmaps and review schedules** (e.g., quarterly re‑evaluations of specific components).

SEL does not directly execute trades or change policies; instead, it **produces structured recommendations and tasks** that flow into DRA and Admin workflows for approval and implementation.

---
```

### B.2 `SEL – 2. The Continuous Learning Loop`

```markdown
# SEL – 2. The Continuous Learning Loop

SEL operates as a continuous loop from data to decision to outcome to learning:

1. **Plan**
   - Define what we expect from models, strategies, and policies:
     - Target KPIs (e.g., Sharpe, hit rate, TE, slippage bands).
     - Risk and envelope expectations.
     - Operational constraints (incident rates, execution failure tolerances).

2. **Observe**
   - Collect evidence from:
     - Backtests,
     - Paper sessions,
     - Live sessions,
     - Incidents and runbook executions.
   - Consolidate this evidence into **performance dashboards and datasets**.

3. **Diagnose**
   - Identify:
     - Under‑performing models, strategies, or integration rules.

     - Regimes where performance is systematically weaker or stronger.
     - Sources of incidents and operational friction.
   - Use both quantitative analysis and narrative reasoning.

4. **Decide**
   - Formulate **recommendations**:
     - Retraining specific models with updated data ranges or features.
     - Changing MSI policies (weights, eligibility, conflict thresholds).
     - Adjusting DRA envelopes or promotion/rollback criteria.
     - Refining feature frameworks or labeling policies in DIL.

5. **Act**
   - Convert recommendations into:
     - Approved changes in Admin (model promotions/retirements, policy updates).
     - Scheduled retraining jobs and experiments.
     - Updates to documentation and SxE surfaces.

6. **Review**
   - Evaluate the impact of changes:
     - Did performance improve?
     - Did risk behavior improve or degrade?
     - Are incidents less frequent or better handled?

This loop ensures IFNS evolves **deliberately and evidence‑first**, not haphazardly.

---
```

### B.3 `SEL – 3. Evidence, Metrics, and Learning Artifacts`

```markdown
# SEL – 3. Evidence, Metrics, and Learning Artifacts

SEL relies on a well‑defined set of **learning artifacts** and metrics, built from telemetry and registries:

- **Performance Evidence**
  - Backtest metrics by strategy, regime, and period.
  - Paper‑run and live‑run KPIs (Sharpe, TE, drawdowns, hit rates, slippage, etc.).
  - Per‑model and per‑MSI‑policy performance breakdowns.

- **Risk & Incident Evidence**
  - Envelope usage and breach statistics.

  - Kill switch and cooldown activations and their causes.
  - Incident frequency, types, and resolution quality.

- **Execution Evidence**
  - Slippage and TE distributions vs. targets.
  - Rejection rates and reasons.
  - Execution anomalies correlated with structure, regime, or policy changes.

- **Learning Datasets**
  - Aggregations of telemetry into **learning tables**, for example:
    - `Model_Performance_By_Regime`,
    - `Strategy_Performance_By_Structure`,
    - `Execution_Quality_By_Route`,
    - `Risk_Breaches_By_Envelope_And_Condition`.

These artifacts are stored in structured tables/JSON and are accessible to both automated analysis and human reviewers.

---
```

### B.4 `SEL – 4. Retraining, Refresh, and Experiment Cycles`

```markdown
# SEL – 4. Retraining, Refresh, and Experiment Cycles

SEL orchestrates **retraining and refresh cycles** for models and policies.

Key elements:

- **Retraining Schedules**
  - Baseline schedules (e.g., monthly, quarterly) for model retraining.
  - Event‑driven retraining (e.g., after a regime shift or significant performance change).

- **Retraining Specs**
  - Which datasets to use (time ranges, markets, regimes).
  - What label and feature versions to apply.
  - Whether to:
    - Maintain architecture,
    - Tune hyperparameters,
    - Experiment with new architectures.

- **Experiment Coordination**
  - SEL uses the **Experiment Log** and **Model Registry** to:
    - Track which retraining and new model experiments are in flight.
    - Ensure results are compared against baselines and prior versions.

  - Recommendations are made based on:
    - Statistically robust improvements,
    - Operational side‑effects (e.g., more complex models vs. marginal performance gains).

- **Refresh vs. Replace**
  - SEL distinguishes between:
    - Simple **refreshes** (retrain same model family on more recent data),
    - **Replacements** (new architectures, new families),
    - **Retirements** (models that should no longer be used).

SEL ensures that retraining is not an uncontrolled, constant churn; instead, it is a **planned, governed process**.

---
```

### B.5 `SEL – 5. Learning‑Driven Promotions, Rollbacks, and Policy Updates`

```markdown
# SEL – 5. Learning‑Driven Promotions, Rollbacks, and Policy Updates

SEL feeds **promotion, rollback, and policy update proposals** into DRA and Admin workflows:

- **Promotions**
  - SEL aggregates evidence for candidate models and strategies:
    - Backtests,
    - Paper runs,
    - Live canary performance,
    - Execution and risk behavior.
  - Produces a **Promotion Dossier**:
    - Summary metrics vs. baselines,
    - Regime‑specific strengths and weaknesses,
    - Risk and incident profile.
  - DRA then applies gate logic to decide whether to promote.

- **Rollbacks**
  - SEL monitors ongoing performance:
    - Detects degradation, instability, or structural mismatch.
    - Correlates issues with:
      - Recent changes,
      - Regime shifts,
      - Data quality issues.
  - Issues **Rollback Recommendations** when evidence shows persistent or dangerous under‑performance.

- **Policy Updates**

  - Based on SEL analysis, recommendations may include:
    - Tightening or relaxing risk envelopes.
    - Updating MSI integration policies.
    - Adjusting execution policies (routes, pacing, slippage limits).
  - These proposals are structured and sent to Admin for review and approval.

This keeps change management **anchored in SEL’s evidence**, while ensuring final authority remains with DRA and governed Admin workflows.

---
```

### B.6 `SEL – 6. SxE Representation of SEL`

```markdown
# SEL – 6. SxE Representation of SEL

SEL is surfaced in SxE as both **analytics** and **governance tooling**:

- **Mirror**
  - Learning dashboards:
    - Long‑horizon performance curves for models and strategies.
    - Before‑and‑after comparisons for major changes (e.g., model promotions, policy updates).
  - Health indicators:
    - Areas where IFNS is over/under‑performing expectations.
    - Regimes or structures where reliability is low.

- **Admin**
  - **Learning & Review Console**
    - Scheduled review agendas (e.g., monthly model reviews, quarterly risk reviews).
    - Lists of recommendations from SEL:
      - Pending promotions or rollbacks.
      - Suggested policy adjustments.
  - **Dossiers & Evidence**
    - Access to Promotion Dossiers, Rollback Reports, and Learning Notes.
    - Links to underlying metrics, charts, and telemetry tables.

SEL’s SxE presence ensures that learning is **visible, planned, and traceable**, not buried in code or scattered notebooks.

---
```