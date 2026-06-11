"""
Exports parsed Power BI metadata to a JSON artifact for consumption
by the consolidated-dbt-docs repo.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from parse_pbi import parse_pbi_project

def export_metadata():
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    project = parse_pbi_project(repo_root)

    output = {
        "report_name": project["report_name"],
        "tables": [],
        "relationships": [],
    }

    for table in project["tables"]:
        sf_fqn = ""
        if table.snowflake_database and table.snowflake_schema and table.snowflake_table:
            sf_fqn = f"{table.snowflake_database}.{table.snowflake_schema}.{table.snowflake_table}"
        output["tables"].append({
            "name": table.name,
            "source_fqn": sf_fqn,
            "mode": table.mode,
            "measures": [
                {"name": m.name, "expression": m.expression, "format_string": m.format_string, "description": m.description}
                for m in table.measures
            ],
            "columns": [
                {"name": c.name, "data_type": c.data_type, "description": c.description, "summarize_by": c.summarize_by}
                for c in table.columns
            ],
        })

    for rel in project["relationships"]:
        output["relationships"].append({
            "name": rel.name,
            "from_table": rel.from_table,
            "from_column": rel.from_column,
            "to_table": rel.to_table,
            "to_column": rel.to_column,
        })

    os.makedirs("artifacts", exist_ok=True)
    with open("artifacts/pbi_metadata.json", "w") as f:
        json.dump(output, f, indent=2)

    print(f"Exported: {len(output['tables'])} tables, {len(output['relationships'])} relationships")
    print(f"Output: artifacts/pbi_metadata.json")

if __name__ == "__main__":
    export_metadata()
