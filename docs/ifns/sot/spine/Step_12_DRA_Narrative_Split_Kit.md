# Step 12 – DRA Narrative Split Kit

This file helps you break the long **`01 – Narrative & Intent`** page for **Step 12 – Decision & Risk Architecture (DRA)**

into smaller child pages in Notion. All content below is taken from your existing Notion export and regrouped

by headings only (no new concepts added).


## A. Parent page – `01 – Narrative & Intent` (new layout)

In Notion, keep `01 – Narrative & Intent` as a short overview and index page. Replace its body with something like:

```markdown
# 01 – Narrative & Intent

This step defines **Decision & Risk Architecture (DRA)** — the control layer that decides **how much risk** IFNS is

allowed to take, **when**, and **under which conditions**. DRA turns modeled intent and execution capabilities into

capital allocation, envelopes, gates, and explicit incident responses.


Use this page as a **map** only. The detailed narrative now lives in the child pages below.

## Child pages

1. **DRA – 1. Role in the IFNS Stack**
2. **DRA – 2. Risk Envelopes and Limits**
3. **DRA – 3. Decision Tables and Gates**
4. **DRA – 4. Kill Switches, Cooldowns, and Incident Handling**
5. **DRA – 5. Promotion, Rollback, and Capital Scaling**
6. **DRA – 6. SxE Representation of DRA**

Each child page should appear as a Notion subpage under this one.
```

## B. Child pages (copy each into its own Notion page)


### B.1 `DRA – 1. Role in the IFNS Stack`

```markdown
# DRA – 1. Role in the IFNS Stack

DRA sits between MSI and EI, and above environmental controls (offline/paper/live):

- **Inputs**

  - Decision proposals from MSI (direction, conviction, horizon, contributing models, conflict metrics).
  - Structural and regime context from MSA.
  - Risk metrics and envelopes:
    - Per-strategy, per-instrument, and global limits.
    - Volatility, drawdown, and tail risk bounds.
  - Capital allocation plans (how much capital is assigned to each strategy/environment).
  - System state:
    - Kill switch status,
    - Cooldowns,
    - Incident states.

- **Outputs**
  - **Trade authorization decisions**:
    - Allowed/not allowed,
    - Maximum size / exposure,
    - Any additional constraints.
  - **Environment control decisions**:
    - Whether certain lanes are open (e.g., live_canary, live_promoted),
    - Whether to reduce or zero-out exposures.
  - **Promotion and rollback decisions** for models and strategies.
  - **Incident triggers** when risk rules are violated.

DRA is where policy meets reality: it encodes *how much risk we are willing to take* when IFNS wants to act.

---
```

### B.2 `DRA – 2. Risk Envelopes and Limits`

```markdown
# DRA – 2. Risk Envelopes and Limits

At the core of DRA are **risk envelopes** — structured definitions of acceptable risk across multiple dimensions:

- **Per-strategy envelopes**
  - Max position size per instrument or group.
  - Max leverage or notional exposure.
  - Max daily/weekly loss and drawdown thresholds.
  - Volatility- or regime-dependent caps (e.g., lower caps in high-vol regimes).

- **Per-portfolio / global envelopes**

  - Aggregate exposure limits by sector, country, or asset class.
  - Correlation or concentration limits (e.g., maximum weight in any single cluster).
  - Global drawdown or VaR-like thresholds.

- **Environment-specific envelopes**
  - Stricter limits in `paper` and `live_canary` lanes.
  - Gradual relaxation as evidence accumulates and promotions occur.

Risk envelopes are defined in structured tables/JSON (e.g., `risk_envelope.json`) and are consumed by DRA decision tables in real time.

DRA ensures that **no decision proposal is approved** unless it fits within all relevant envelopes.

---
```

### B.3 `DRA – 3. Decision Tables and Gates`

```markdown
# DRA – 3. Decision Tables and Gates

DRA uses a system of **decision tables** and **gates** to turn inputs into decisions:

1. **Eligibility Gate**
   - Checks:
     - Is this strategy enabled in the current environment?
     - Are models behind the proposal in allowed statuses (e.g., `promoted`, `canary`)?
     - Are there any active incidents that block this lane?

2. **Risk Envelope Gate**
   - Evaluates:
     - New proposed position vs. envelope limits.
     - Impact on drawdown and exposure.
     - Whether volatility, liquidity, and structural conditions meet minimum criteria.

3. **Capital Allocation Gate**
   - Applies capital allocation plans:
     - Maximum capital share per strategy, environment, and lane.
     - Budget usage (how much of allocated capital is already in use).

4. **Control State Gate**
   - Considers:
     - Kill switch state (global or strategy-specific).

     - Cooldown state (recent breach or incident requiring rest).
     - Manual overrides where explicit operator decisions are in place.

5. **Final Decision & Instruction**
   - Produces:
     - `decision = ALLOW | REDUCE | DENY`.
     - Approved size range and constraints (e.g., “allow up to X units”, “no new exposure, only risk reductions”).
     - Any flags to be attached to the execution request.

These gates are encoded as structured **DRA decision tables** that can be visualized and edited in Admin (under governance), rather than opaque code branches.

---
```

### B.4 `DRA – 4. Kill Switches, Cooldowns, and Incident Handling`

```markdown
# DRA – 4. Kill Switches, Cooldowns, and Incident Handling

DRA defines how IFNS responds when risk envelopes are breached or when abnormal behavior is detected:

- **Kill Switches**
  - Global kill switch:
    - Stops all new trading in live environments, optionally unwinds risk.
  - Strategy-level kill switches:
    - Block new trades or scaling in specific strategies or universes.
  - Trigger conditions can include:
    - Exceeding drawdown thresholds,
    - Serious execution anomalies,
    - Data integrity incidents,
    - Manual operator activation.

- **Cooldowns**
  - Time-based or condition-based **rest periods** after:
    - Risk breaches,
    - Large losses,
    - Regime or structural shocks.
  - During cooldowns:
    - No new risk is added,
    - Positions may be reduced,
    - System collects further evidence before reactivation.

- **Incident Handling**

  - DRA integrates with the **incident taxonomy and runbooks**:
    - When a risk rule is violated, DRA emits an incident.
    - Incidents trigger a predefined runbook (e.g., stop certain lanes, notify operators, require approval to resume).
  - Outcome of incidents (resolved, escalated, root cause identified) is recorded and fed into SEL.

These mechanisms ensure IFNS is **capable of saying no** and can move into safe states quickly, with a clear audit trail.

---
```

### B.5 `DRA – 5. Promotion, Rollback, and Capital Scaling`

```markdown
# DRA – 5. Promotion, Rollback, and Capital Scaling

DRA also governs **non-instantaneous decisions** such as promotions, rollbacks, and capital scaling:

- **Promotion Gates**
  - Define criteria for moving:
    - From `offline` to `paper`,
    - From `paper` to `live_canary`,
    - From `live_canary` to `live_promoted`.
  - Criteria include:
    - Backtest metrics and robustness indicators,
    - Paper-run KPIs (e.g., TE, slippage, incident-free performance),
    - Live canary performance where applicable.
  - Promotions are **decisions in their own right**, subject to approvals and logging.

- **Rollback Gates**
  - Define conditions under which:
    - Models or strategies must be downgraded (e.g., `promoted` → `canary` → `baseline`),
    - Lanes must be closed (e.g., suspend live_canary).
  - May be triggered by:
    - Performance deterioration,
    - Excessive incidents,
    - Changes in market structure or data quality.

- **Capital Scaling Rules**

  - Govern how capital allocations can increase or decrease over time:
    - Stepwise increases after sustained good performance,
    - Automatic reductions after drawdown or incident patterns.
  - Capital scaling is always **conditional on risk envelopes** and environment state.

All promotions, rollbacks, and capital scaling changes must be:

- Expressed in structured DRA policies,
- Logged in the **Change Log**,
- Visible in SxE for later review.

---
```

### B.6 `DRA – 6. SxE Representation of DRA`

```markdown
# DRA – 6. SxE Representation of DRA

DRA is highly visible in both Mirror and Admin:

- **Mirror**
  - Risk posture overview:
    - Current envelope usage (per strategy and globally),
    - Current environment states (which lanes open/closed),
    - Active kill switches and cooldowns.
  - Breach and incident views:
    - Timeline of risk breaches and responses,
    - Impact on positions and performance.

- **Admin**
  - **Risk Envelope Console**
    - View and manage risk envelopes and limits.
    - See current vs. allowed risk by strategy and portfolio.
  - **Decision & Gate Console**
    - Visualize DRA decision tables.
    - Inspect how a specific decision was reached (which gates passed/failed).
  - **Promotion & Capital Scaling Console**
    - Track promotions, rollbacks, and capital changes.
    - Initiate requests and approvals with attached evidence.

These SxE surfaces help operators understand not only **what** DRA decided, but **why**.

---
```