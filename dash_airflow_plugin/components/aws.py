import dash_react_json_schema_form
from aws_utils_airflow_plugin import list_connections, S3Hook
import s3fs
from dash import Dash, html, dcc, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
from typing import List, Any, Dict
from pprint import pprint

from dash_airflow_plugin.components.alerts import render_alert
from dash_airflow_plugin.components.data_table import render_data_table, dash_data_table_columns


def render_aws_conns_dt(
    dt_id: str = "aws_conns_dt", row_selectable: str = "multiple"
) -> dbc.Row:
    conns = list_connections()
    if len(conns):
        conns_records = []
        for conn in conns:
            conns_records.append({"conn_id": conn["conn_id"]})

        conns_df = pd.DataFrame.from_records(conns_records)
        return (
            render_data_table(
                title="Choose one or more AWS Connections",
                id=dt_id,
                data=conns_df.to_dict("records"),
                columns=dash_data_table_columns(conns_df),
                row_selectable="multiple",
                hidden_columns=[],
            ),
        )
    else:
        render_alert(
            "No AWS connections found. Please enter some using the Airflow Connections page.",
            color="danger",
        )


def render_s3_buckets_dt(
    aws_conn_ids: List[str] = [],
    dt_id: str = "buckets_list",
    row_selectable="multiple",
) -> dbc.Row:
    buckets = []
    for aws_conn_id in aws_conn_ids:
        try:
            s3_hook = S3Hook(aws_conn_id)
            s3_client = s3_hook.get_client()
            response = s3_client.list_buckets()
            for bucket in response["Buckets"]:
                buckets.append(
                    {
                        "bucket": bucket["Name"],
                        "creation_date": bucket["CreationDate"],
                        "aws_conn_id": aws_conn_id,
                    }
                )
        except Exception as e:
            print("Nope")

    buckets_df = pd.DataFrame.from_records(buckets)
    buckets_df.sort_values(by=['creation_date', 'bucket'], inplace=True, ascending=False)
    return render_data_table(
        title="Choose one or more S3 Buckets",
        id=dt_id,
        data=buckets_df.to_dict("records"),
        columns=dash_data_table_columns(buckets_df),
        row_selectable=row_selectable,
        hidden_columns=[],
    )


def render_s3_bucket_objects_dt(
    buckets_data: List[Any],
    paths: str,
    dt_id: str = "buckets_objects_list",
    max_depth=1000,
    glob=False,
    title="",
    row_selectable="multiple",
) -> dbc.Row:
    all_files = []
    if isinstance(paths, str):
        paths = paths.split(",")
    for data in buckets_data:
        aws_conn_id = data["aws_conn_id"]
        bucket = data["bucket"]
        s3_hook = S3Hook(aws_conn_id)
        s3_session = s3_hook.get_session()
        s3_client = s3_hook.get_client()
        credentials = s3_hook.get_credentials()
        fs = s3fs.S3FileSystem(
            key=credentials.access_key, secret=credentials.secret_key
        )
        for path in paths:
            if glob:
                files = fs.glob(
                    f"s3://{bucket}/{path}", recursive=True, max_depth=max_depth
                )
            else:
                files = fs.find(
                    f"s3://{bucket}/{path}", recursive=True, max_depth=max_depth
                )
            for file in files:
                file = file.replace(f"{bucket}/", "")
                all_files.append(
                    {"bucket": bucket, "aws_conn_id": aws_conn_id, "file": file}
                )
    buckets_files_df = pd.DataFrame.from_records(all_files)
    return render_data_table(
        title=title,
        id=dt_id,
        data=buckets_files_df.to_dict("records"),
        columns=dash_data_table_columns(buckets_files_df),
        row_selectable=row_selectable,
        hidden_columns=[],
    )
