# IFNS SoT – Missing / Non-Referenced Assets Report (v0.1)

Generated: 2025-11-19

This report compares the contents of the `autopilot-notion-ops` repo snapshot

against the current SoT split kits available in this workspace.



For each file in the repo (limited to `.md`, `.csv`, `.json`, `.yaml`, `.yml`, `.ndjson`),

we check whether its **basename** appears anywhere inside the SoT kit markdown files

currently present under `/mnt/data`.



**Interpretation:**

- `referenced_in_SoT_kits` means: the file name is mentioned at least once in one of the kits

  (for example, `QC_Weekly_Telemetry_V1.md` is referenced in the QC Weekly Spec Kit).

- `not_referenced_in_SoT_kits` means: there is no direct textual mention of this file name in the kits;

  it may or may not already be conceptually covered, but there is no explicit reference.



- Total repo doc-like files scanned: **156**

- Referenced in SoT kits: **4**

- Not referenced in SoT kits: **152**


---

## 1. Summary by category (not referenced)

- **infra_workflow**: 13 files
- **other**: 27 files
- **integration_config**: 4 files
- **notion_db_export**: 6 files
- **notion_page_export**: 1 files
- **sample_data**: 2 files
- **ifns_docs**: 71 files
- **ifns_sync_artifact**: 28 files

---

## 2. Detailed list – not referenced in SoT kits


### ifns_docs

- `autopilot-notion-ops/docs/ifns/Conceptual_Framework.md`
- `autopilot-notion-ops/docs/ifns/Dashboard_Analytics.md`
- `autopilot-notion-ops/docs/ifns/IFNS_UI_Drafts_and_Working_Notes_v2.md`
- `autopilot-notion-ops/docs/ifns/IFNS_UI_Master_Summary_v2.md`
- `autopilot-notion-ops/docs/ifns/IFNS_UI_Steps_Index_v2.md`
- `autopilot-notion-ops/docs/ifns/Operational_Framework.md`
- `autopilot-notion-ops/docs/ifns/Reference_Library.md`
- `autopilot-notion-ops/docs/ifns/Step_01_Preface_Integration.md`
- `autopilot-notion-ops/docs/ifns/Step_02_Executive_Summary.md`
- `autopilot-notion-ops/docs/ifns/Step_03_Visionary_Technical_Overview.md`
- `autopilot-notion-ops/docs/ifns/Step_04_Preface_Timeline.md`
- `autopilot-notion-ops/docs/ifns/Step_05_Introduction_Operational_Genesis.md`
- `autopilot-notion-ops/docs/ifns/Step_06_System_Architecture.md`
- `autopilot-notion-ops/docs/ifns/Step_07_Data_Intelligence_Layer_DIL.md`
- `autopilot-notion-ops/docs/ifns/Step_08_Modeling_Intelligence_MI.md`
- `autopilot-notion-ops/docs/ifns/Step_09_Execution_Intelligence_EI.md`
- `autopilot-notion-ops/docs/ifns/Step_10_Market_Structural_Awareness_MSA.md`
- `autopilot-notion-ops/docs/ifns/Step_11_Model_and_Signal_Integration_MSI.md`
- `autopilot-notion-ops/docs/ifns/Step_12_Decision_and_Risk_Architecture_DRA.md`
- `autopilot-notion-ops/docs/ifns/Step_13_Self_Evaluation_and_Learning_SEL.md`
- `autopilot-notion-ops/docs/ifns/Step_14_Advanced_Awareness_and_Quantum_Cognition.md`
- `autopilot-notion-ops/docs/ifns/Wireframe.md`
- `autopilot-notion-ops/docs/ifns/crosswalks/Repo_Inventory_and_Git-Notion_Crosswalk_autopilot-notion-ops_2025_11_19.md`
- `autopilot-notion-ops/docs/ifns/handover/Phase_0_Autopilot_Hub_Inventory.md`
- `autopilot-notion-ops/docs/ifns/handover/Phase_1_IFNS_14-Step_Spine_and_Hub_Structure.md`
- `autopilot-notion-ops/docs/ifns/handover/Phase_2_Attach_UI_Master_V2_to_14-Step_Spine.md`
- `autopilot-notion-ops/docs/ifns/handover/Phase_3_Telemetry_QC_Runtime_and_Calendar_Wiring.md`
- `autopilot-notion-ops/docs/ifns/handover/Phase_4_Catalog_and_Feature_Universe_Surfaces.md`
- `autopilot-notion-ops/docs/ifns/handover/Phase_5_Living_SoT_Rules_and_V1_Crosswalk.md`
- `autopilot-notion-ops/docs/ifns/indicators/CI_Guard.md`
- `autopilot-notion-ops/docs/ifns/indicators/Feature_Family_and_Pytest_Starter.md`
- `autopilot-notion-ops/docs/ifns/indicators/Feature_Policy_Matrix.md`
- `autopilot-notion-ops/docs/ifns/indicators/IO_Utilities_and_Synthetic_Inputs.md`
- `autopilot-notion-ops/docs/ifns/indicators/Indicators_Feature_Schema_Phase5.md`
- `autopilot-notion-ops/docs/ifns/indicators/Indicators_Implementation_Templates_Phase6.md`
- `autopilot-notion-ops/docs/ifns/indicators/Indicators_L1_Catalog_Phase3.md`
- `autopilot-notion-ops/docs/ifns/indicators/Indicators_L2L3_Catalog_Phase4.md`
- `autopilot-notion-ops/docs/ifns/indicators/Indicators_ML_Integration_Phase7.md`
- `autopilot-notion-ops/docs/ifns/indicators/Indicators_Master_Index_Phases_1_to_7.md`
- `autopilot-notion-ops/docs/ifns/indicators/Indicators_Taxonomy_Phase1.md`
- `autopilot-notion-ops/docs/ifns/indicators/Indicators_Universe_Phase2.md`
- `autopilot-notion-ops/docs/ifns/indicators/Manifest_Diff_Tool.md`
- `autopilot-notion-ops/docs/ifns/indicators/Manifests_with_Family_and_Linter.md`
- `autopilot-notion-ops/docs/ifns/indicators/QC_Weekly_ETL_Clip_Integration.md`
- `autopilot-notion-ops/docs/ifns/indicators/QC_Weekly_ETL_Skeleton.md`
- `autopilot-notion-ops/docs/ifns/indicators/Soft_Clipping_and_Calendars.md`
- `autopilot-notion-ops/docs/ifns/indicators/Unit_Test_Scaffolds.md`
- `autopilot-notion-ops/docs/ifns/indicators/checklists/Phase1_Taxonomy_Governance.md`
- `autopilot-notion-ops/docs/ifns/indicators/checklists/Phase2_Indicator_Universe.md`
- `autopilot-notion-ops/docs/ifns/indicators/checklists/Phase3_L1_Catalog.md`
- `autopilot-notion-ops/docs/ifns/indicators/checklists/Phase4_L2L3_Frameworks.md`
- `autopilot-notion-ops/docs/ifns/indicators/checklists/Phase5_Feature_Output_Digitization.md`
- `autopilot-notion-ops/docs/ifns/indicators/checklists/Phase6_Implementation_Runtime.md`
- `autopilot-notion-ops/docs/ifns/indicators/checklists/Phase7_ML_Integration_Operations.md`
- `autopilot-notion-ops/docs/ifns/saved_views/CalendarGaps2025_views.md`
- `autopilot-notion-ops/docs/ifns/saved_views/CatalogL1_views.md`
- `autopilot-notion-ops/docs/ifns/saved_views/CatalogL2L3_views.md`
- `autopilot-notion-ops/docs/ifns/saved_views/FamilyMap_views.md`
- `autopilot-notion-ops/docs/ifns/saved_views/FeatureSchemaH1_views.md`
- `autopilot-notion-ops/docs/ifns/saved_views/FeatureSchemaV1_views.md`
- `autopilot-notion-ops/docs/ifns/saved_views/PolicyMatrix_views.md`
- `autopilot-notion-ops/docs/ifns/saved_views/QCWeekly_views.md`
- `autopilot-notion-ops/docs/ifns/saved_views/UniverseP2_views.md`
- `autopilot-notion-ops/docs/ifns/stages/Stage_00_Document_Overview.md`
- `autopilot-notion-ops/docs/ifns/stages/Stage_01_Foundations_and_Architecture.md`
- `autopilot-notion-ops/docs/ifns/stages/Stage_02_Data_and_Feature_Pipeline.md`
- `autopilot-notion-ops/docs/ifns/stages/Stage_03_Modeling_and_Training.md`
- `autopilot-notion-ops/docs/ifns/stages/Stage_04_Backtesting_and_Evaluation.md`
- `autopilot-notion-ops/docs/ifns/stages/Stage_05_Risk_Execution_and_SxE_Link.md`
- `autopilot-notion-ops/docs/ifns/stages/Stage_06_Paper_Trading.md`
- `autopilot-notion-ops/docs/ifns/stages/Stage_07_Live_Trading_and_Operations.md`

### ifns_sync_artifact

- `autopilot-notion-ops/sync/ifns/Backtest_Results_Table.csv`
- `autopilot-notion-ops/sync/ifns/Execution_API_Log.csv`
- `autopilot-notion-ops/sync/ifns/Experiment_Logs.csv`
- `autopilot-notion-ops/sync/ifns/Model_Registry.csv`
- `autopilot-notion-ops/sync/ifns/Portfolio_Matrix.csv`
- `autopilot-notion-ops/sync/ifns/RiskAPI_Alerts.csv`
- `autopilot-notion-ops/sync/ifns/System_Layers_Tracker.csv`
- `autopilot-notion-ops/sync/ifns/calendar_gaps_2025.json`
- `autopilot-notion-ops/sync/ifns/clip_events_schema_v1.json`
- `autopilot-notion-ops/sync/ifns/examples/clip_events_sample.ndjson`
- `autopilot-notion-ops/sync/ifns/examples/feature_view_D1_demo.csv`
- `autopilot-notion-ops/sync/ifns/examples/feature_view_H1_demo.csv`
- `autopilot-notion-ops/sync/ifns/examples/indicator_feature_schema_d1_demo.csv`
- `autopilot-notion-ops/sync/ifns/examples/indicator_feature_schema_h1_demo.csv`
- `autopilot-notion-ops/sync/ifns/examples/training_manifest_D1_demo.json`
- `autopilot-notion-ops/sync/ifns/examples/training_manifest_H1_demo.json`
- `autopilot-notion-ops/sync/ifns/feature_family_map.csv`
- `autopilot-notion-ops/sync/ifns/feature_policy_matrix.csv`
- `autopilot-notion-ops/sync/ifns/indicator_feature_schema_h1_v1_with_family.csv`
- `autopilot-notion-ops/sync/ifns/indicator_feature_schema_v1_with_family.csv`
- `autopilot-notion-ops/sync/ifns/indicators_catalog_L1_phase3.csv`
- `autopilot-notion-ops/sync/ifns/indicators_catalog_L2L3_phase4.csv`
- `autopilot-notion-ops/sync/ifns/indicators_universe_catalog_phase2.csv`
- `autopilot-notion-ops/sync/ifns/lint_report.csv`
- `autopilot-notion-ops/sync/ifns/lint_report.json`
- `autopilot-notion-ops/sync/ifns/test_assertions_manifest.json`
- `autopilot-notion-ops/sync/ifns/training_manifest_D1_v1_1.json`
- `autopilot-notion-ops/sync/ifns/training_manifest_H1_v1_0.json`

### infra_workflow

- `autopilot-notion-ops/.github/workflows/ci_ifns_guard.yml`
- `autopilot-notion-ops/.github/workflows/ifns-sync.yml`
- `autopilot-notion-ops/.github/workflows/ifns-test-incident.yml`
- `autopilot-notion-ops/.github/workflows/ifns-verify.yml`
- `autopilot-notion-ops/.github/workflows/notion-backup.yml`
- `autopilot-notion-ops/.github/workflows/notion-commands.yml`
- `autopilot-notion-ops/.github/workflows/notion-export.yml`
- `autopilot-notion-ops/.github/workflows/notion-integration-layer.yml`
- `autopilot-notion-ops/.github/workflows/notion-list.yml`
- `autopilot-notion-ops/.github/workflows/notion-quick-add.yml`
- `autopilot-notion-ops/.github/workflows/notion-seed.yml`
- `autopilot-notion-ops/.github/workflows/notion-sync.yml`
- `autopilot-notion-ops/.github/workflows/ops-command-runner.yml`

### integration_config

- `autopilot-notion-ops/IFNS_Notion_DB_Buildout_V2/config/ifns_v2_db_map.json`
- `autopilot-notion-ops/config/Integration Setup.json`
- `autopilot-notion-ops/config/ifns-mappings.json`
- `autopilot-notion-ops/config/incident-webhook.json`

### notion_db_export

- `autopilot-notion-ops/content/databases/Autopilot_Architecture_Notes.csv`
- `autopilot-notion-ops/content/databases/Autopilot_Decisions_Log.csv`
- `autopilot-notion-ops/content/databases/Autopilot_Experiments_Log.csv`
- `autopilot-notion-ops/content/databases/Autopilot_Glossary.csv`
- `autopilot-notion-ops/content/databases/Autopilot_Tasks_Backlog.csv`
- `autopilot-notion-ops/content/databases/Autopilot_Variables_Config.csv`

### notion_page_export

- `autopilot-notion-ops/content/pages/README.md`

### other

- `autopilot-notion-ops/.vscode/settings.json`
- `autopilot-notion-ops/IFNS_Indicators_Quickstart_v0_18.md`
- `autopilot-notion-ops/README.md`
- `autopilot-notion-ops/README_Moath_Local.md`
- `autopilot-notion-ops/docs/IFNS_Notion_Page_Index.md`
- `autopilot-notion-ops/docs/IFNS_Troubleshooting_Log.md`
- `autopilot-notion-ops/docs/IFNS_UI_Master_Notion_Snapshot.md`
- `autopilot-notion-ops/etl/qc_weekly_etl_config.yaml`
- `autopilot-notion-ops/logs/ifns_notions_tree_2025-11-18.csv`
- `autopilot-notion-ops/meta_index/IFNS_Indicators_Packs_Index_v0_18.csv`
- `autopilot-notion-ops/meta_index/IFNS_Indicators_Packs_Index_v0_18.json`
- `autopilot-notion-ops/meta_index/README_Merge_Order.md`
- `autopilot-notion-ops/runtime_templates/RUN_IFNS_FEATUREVIEW_D1_ARCX_IWM_V1_1.yaml`
- `autopilot-notion-ops/runtime_templates/RUN_IFNS_FEATUREVIEW_D1_ARCX_SPY_V1_1.yaml`
- `autopilot-notion-ops/runtime_templates/RUN_IFNS_FEATUREVIEW_D1_XNAS_MSFT_V1_1.yaml`
- `autopilot-notion-ops/runtime_templates/RUN_IFNS_FEATUREVIEW_D1_XNYS_AAPL_V1_1.yaml`
- `autopilot-notion-ops/runtime_templates/RUN_IFNS_FEATUREVIEW_H1_ARCX_IWM_V1_1.yaml`
- `autopilot-notion-ops/runtime_templates/RUN_IFNS_FEATUREVIEW_H1_ARCX_SPY_V1_1.yaml`
- `autopilot-notion-ops/runtime_templates/RUN_IFNS_FEATUREVIEW_H1_XNAS_AAPL_V1_1.yaml`
- `autopilot-notion-ops/runtime_templates/RUN_IFNS_FEATUREVIEW_H1_XNAS_MSFT_V1_1.yaml`
- `autopilot-notion-ops/schemas/databases.yml`
- `autopilot-notion-ops/tests/fixtures/test_ATR14_PCT_D1_fixture.csv`
- `autopilot-notion-ops/tests/fixtures/test_BOLL_Z20x2_D1_fixture.csv`
- `autopilot-notion-ops/tests/fixtures/test_CTX_PRICE_LOCATION_BIN_H1_fixture.csv`
- `autopilot-notion-ops/tests/fixtures/test_RET_1H_H1_fixture.csv`
- `autopilot-notion-ops/tests/fixtures/test_RSI14_D1_fixture.csv`
- `autopilot-notion-ops/‎.github/workflows/notion-integration-layer.yml`

### sample_data

- `autopilot-notion-ops/data/d1_arcx_spy_demo.csv`
- `autopilot-notion-ops/data/h1_xnas_msft_demo.csv`
