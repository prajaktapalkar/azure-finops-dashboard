import azure.functions as func
import logging
import json
import os
from datetime import datetime

from azure.identity import DefaultAzureCredential
from azure.mgmt.costmanagement import CostManagementClient
from azure.mgmt.costmanagement.models import (
    QueryDefinition, QueryTimePeriod,
    QueryDataset, QueryAggregation,
    QueryGrouping, TimeframeType
)
from azure.storage.blob import BlobServiceClient

app = func.FunctionApp()

@app.timer_trigger(schedule="0 0 8 * * *", arg_name="myTimer", run_on_startup=False)
def CostExporter(myTimer: func.TimerRequest) -> None:

    SUBSCRIPTION_ID = os.environ["SUBSCRIPTION_ID"]
    STORAGE_CONN_STR = os.environ["STORAGE_CONNECTION_STRING"]
    CONTAINER_NAME = "cost-exports"

    logging.info("Cost Exporter triggered at %s", datetime.utcnow())

    credential = DefaultAzureCredential()
    client = CostManagementClient(credential, SUBSCRIPTION_ID)

    today = datetime.utcnow().date()
    start = today.replace(day=1)

    scope = f"/subscriptions/{SUBSCRIPTION_ID}"

    query = QueryDefinition(
        type="ActualCost",
        timeframe=TimeframeType.CUSTOM,
        time_period=QueryTimePeriod(
            from_property=datetime(start.year, start.month, start.day),
            to=datetime(today.year, today.month, today.day)
        ),
        dataset=QueryDataset(
            granularity="Daily",
            aggregation={
                "totalCost": QueryAggregation(
                    name="Cost", function="Sum"
                )
            },
            grouping=[
                QueryGrouping(type="Dimension", name="ServiceName"),
                QueryGrouping(type="Dimension", name="ResourceGroup")
            ]
        )
    )

    result = client.query.usage(scope=scope, parameters=query)

    rows = []
    for row in result.rows:
        rows.append({
            "date": str(today),
            "cost_usd": round(float(row[0]), 4),
            "currency": "USD",
            "service_name": row[3] if len(row) > 3 else "Unknown",
            "resource_group": row[4] if len(row) > 4 else "Unknown",
            "export_timestamp": datetime.utcnow().isoformat()
        })

    blob_client = BlobServiceClient.from_connection_string(STORAGE_CONN_STR)
    container = blob_client.get_container_client(CONTAINER_NAME)

    try:
        container.create_container()
    except Exception:
        pass

    blob_name = f"cost-data-{today.strftime('%Y-%m-%d')}.json"
    container.upload_blob(
        name=blob_name,
        data=json.dumps(rows, indent=2),
        overwrite=True
    )

    logging.info("Exported %d rows to blob: %s", len(rows), blob_name)