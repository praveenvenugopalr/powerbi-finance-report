# Power BI Finance Report

Power BI project (PBIP/TMDL format) connecting to Snowflake data marts. Contains the semantic model definition for the Finance Report dashboard.

Part of the [Consolidated dbt Docs](https://github.com/praveenvenugopalr/consolidated-dbt-docs) multi-project documentation pipeline.

## Structure

```
FinanceReport.SemanticModel/definition/
  ├── tables/                   → TMDL table definitions (columns, measures, partitions)
  │   ├── DM_CUSTOMER_360.tmdl
  │   ├── DM_ACCOUNT_SUMMARY.tmdl
  │   ├── DM_TRANSACTION_DAILY.tmdl
  │   ├── DM_LIQUIDITY_POSITION.tmdl
  │   └── DM_CREDIT_EXPOSURE.tmdl
  └── relationships.tmdl        → Foreign key relationships between tables
scripts/
  └── export_metadata.py        → Parses TMDL and exports pbi_metadata.json
```

## How It Works

The TMDL files contain Snowflake connection info in their `partition` blocks:
```
partition 'dm_customer_360' = m
  source =
    Snowflake.Databases("account.snowflakecomputing.com", "WAREHOUSE")
    {[Name="FINANCE_MART"]}[Data]
    {[Name="RETAIL_BANKING"]}[Data]
    {[Name="DM_CUSTOMER_360"]}[Data]
```

The `scripts/export_metadata.py` script parses these to produce `pbi_metadata.json`, which the consolidated-dbt-docs repo uses to inject Power BI exposures into the unified lineage DAG.

## CI/CD

On push to `main`, GitHub Actions:
1. Parses TMDL files and exports `pbi_metadata.json`
2. Uploads the JSON as an artifact
3. Triggers the consolidated-dbt-docs repo to rebuild the unified site

### Required Secret

| Secret | Purpose |
|--------|---------|
| `DOCS_DISPATCH_TOKEN` | PAT with `contents:read` + `actions:read` on the consolidated-dbt-docs repo |

See the [consolidated-dbt-docs README](https://github.com/praveenvenugopalr/consolidated-dbt-docs#quick-start-fork--configure) for full setup instructions.

## Customizing

To connect your own Power BI report:
1. Save your Power BI file as PBIP format (File → Save As → Power BI Project)
2. Replace the contents of `FinanceReport.SemanticModel/` with your exported model
3. Update `scripts/export_metadata.py` if your directory structure differs
