## Architecture

```mermaid
flowchart TD
    A["Input<br/>CSV / JSON / Parquet / XLSX"] --> B["Ingestion & Standardization Layer<br/>(format detection, schema extraction)"]

    B -->|canonical form| C[("Canonical Parquet Layer<br/>Standard Internal Representation")]
    B -->|preserved evidence| C2[("Input Evidence / Metadata<br/>original characteristics, casting outcomes,<br/>rejected values, transformation log")]

    DC["Dataset Contract<br/>YAML / JSON"] --> CM["Configuration Manager<br/>parse + validate config"]

    CM --> CVQ{"Structural / Type / Value /<br/>Enum / Cross-field / Rule-ref /<br/>Cycle checks pass?"}

    CVQ -->|No| CE["Configuration Error<br/>(rejected before Spark execution)"]
    CVQ -->|Yes| VC["ValidationConfig"]

    RREG["Rule Registry<br/>(20-25 rule catalogue)"] --> DEP

    VC --> DEP["Dependency Graph +<br/>Applicability Evaluation"]
    C --> DEP
    C2 --> DEP

    DEP --> EP["Execution Planner<br/>(groups eligible rules by strategy,<br/>respects dependency order)"]

    EP --> M["Metadata Rules<br/>(no scan - df.schema)"]
    EP --> AG["Aggregate Rules<br/>(one agg())"]
    EP --> COL["Column Expression Rules<br/>(one select())"]
    EP --> GB["GroupBy Rules<br/>(one groupBy())"]
    EP --> J["Join Rules<br/>(FK / lookup)"]
    EP --> H["History Rules"]

    H --> HMP["History Metrics Provider<br/>(detect first run, hide storage)"]

    HMP <--> BMR[("Batch Metrics Repository<br/>one fingerprint per batch")]

    HMP --> HB["Computed Historical Baseline<br/>(mean/median/stddev/percentiles,<br/>computed on demand)"]

    HB --> H

    EHx["Exception Handler<br/>(system/software errors only:<br/>Spark failure, storage outage, calc bugs)"] -.governs.-> EP

    M --> RC["Result Collector"]
    AG --> RC
    COL --> RC
    GB --> RC
    J --> RC
    H --> RC

    RC --> RL["RuleResult[]<br/>Identity / Execution / Validation /<br/>Applied Config / Diagnostics"]

    RL --> AE["Aggregation Engine<br/>count outcomes, count critical failures,<br/>compute quality_score, build summary"]

    AE --> VS["ValidationSummary<br/>quality_score, critical_failures,<br/>soft_failures, errored_rules"]

    VS --> DE["Decision Engine<br/>(policy only, never inspects rules)"]

    DE --> DO["Decision Object<br/>status, decision_reason, quality_score, timestamp"]

    DO -->|PASS| PS[("Pass Storage<br/>TableName_batchID.parquet")]
    DO -->|QUARANTINE / SYSTEM_ERROR| QS[("Quarantine Storage<br/>TableName_batchID.parquet")]

    PS --> VMR[("Validation Metadata /<br/>Batch History Repository")]
    QS --> VMR

    PS -.fingerprint.-> BMR
    QS -.fingerprint.-> BMR

    VMR --> RPT["Validation Reports"]
    VMR --> TR["Historical Trend"]
    VMR --> DASH["Streamlit Dashboard"]
