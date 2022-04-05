from datetime import datetime, timedelta
from dash import Dash, html, dcc, dash_table
from flask_login import current_user
import flask
from flask import redirect, current_app, session, has_app_context, url_for
from dash import dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
import uuid
import os
import pickle
import random
import string

from airflow.www.app import csrf

def save_object(obj, session_id, name):
    os.makedirs("dir_store", exist_ok=True)
    file = "dir_store/{}_{}".format(session_id, name)
    pickle.dump(obj, open(file, "wb"))


def load_object(session_id, name):
    file = "dir_store/{}_{}".format(session_id, name)
    obj = pickle.load(open(file, "rb"))
    os.remove(file)
    return obj


def clean_dir_store():
    if os.path.isdir("dir_store"):
        file_list = pd.Series("dir_store/" + i for i in os.listdir("dir_store"))
        mt = file_list.apply(
            lambda x: datetime.fromtimestamp(os.path.getmtime(x))
        ).astype(str)
        for i in file_list[mt < str(datetime.now() - timedelta(hours=3))]:
            os.remove(i)


def build_pathname_params(url_base):
    pathname_params = dict()
    pathname_params["url_base_pathname"] = None
    pathname_params["routes_pathname_prefix"] = None
    pathname_params["requests_pathname_prefix"] = None
    if os.environ.get("SCRIPT_NAME", False):
        # if running under a proxy such as nginx or shinyproxy, you need to add the fullpathname to the requests
        full_hosting_url = f"{os.environ.get('SCRIPT_NAME').rstrip('/')}{url_base}"
        pathname_params["routes_pathname_prefix"] = url_base
        pathname_params["requests_pathname_prefix"] = full_hosting_url
    else:
        pathname_params["url_base_pathname"] = url_base
    return pathname_params


def apply_layout_with_auth(app, layout, appbuilder):
    def build_navbar():
        return dbc.NavbarSimple(
            children=[
                dbc.NavItem(
                    dbc.NavLink(
                        "Home",
                        href=url_for("Airflow.index"),
                        external_link=True,
                        target="_blank",
                    )
                ),
                dbc.NavItem(
                    dbc.NavLink(
                        "Help",
                        href="https://dabbleofdevopshelp.zendesk.com/",
                        target="_blank",
                        external_link=True,
                    )
                ),
            ],
            brand="BioAnalyze",
            brand_href=url_for("Airflow.index"),
            color="primary",
            dark=True,
        )

    def serve_layout():
        if current_user and current_user.is_authenticated:
            session_id = str(uuid.uuid4())
            clean_dir_store()
            return html.Div(
                [
                    html.Div(session_id, id="session_id", style={"display": "none"}),
                    dcc.Location(id="url", refresh=False),
                    dbc.Container(
                        [
                            build_navbar(),
                        ],
                        fluid=True,
                        className="dbc",
                    ),
                    layout,
                ]
            )
        if has_app_context():
            return dcc.Location(pathname=appbuilder.get_url_for_login, id="")
        return None

    app.config.suppress_callback_exceptions = True
    app.layout = serve_layout
    # https://github.com/plotly/dash/issues/308#issuecomment-412653680
    csrf._exempt_views.add("dash.dash.dispatch")


def render_data_table(title, id=None, data=[], columns=[], hidden_columns=[], row_selectable="single"):
    # Setting row_selectable and row_deletable with empty data results in an error
    if id is None:
        id_s = "".join(random.choices(string.ascii_uppercase + string.digits, k=5))
        id = f"aws_conn_dt-{id_s}"
    elif "_dt" not in id:
        id = f"{id}_dt"

    if len(data) and len(columns):
        row_selectable =row_selectable
        row_deletable = True
    else:
        row_selectable = None
        row_deletable = False
    return dbc.Row(
        [
            dbc.Col(
                [
                    html.H5(title),
                    # dbc.Table.from_dataframe(var_df, striped=True, bordered=True, hover=True),
                    dash_table.DataTable(
                        id=id,
                        data=data,
                        columns=columns,
                        hidden_columns=hidden_columns,
                        editable=True,
                        filter_action="native",
                        sort_action="native",
                        sort_mode="multi",
                        column_selectable="single",
                        row_selectable=row_selectable,
                        row_deletable=row_deletable,
                        selected_columns=[],
                        selected_rows=[],
                        page_action="native",
                        page_current=0,
                        page_size=10,
                        css=[{"selector": ".show-hide", "rule": "display: none"}],
                        style_table={"overflowX": "auto"},
                        style_cell={
                            "height": "auto",
                            # all three widths are needed
                            "minWidth": "180px",
                            "width": "180px",
                            "maxWidth": "180px",
                            "whiteSpace": "normal",
                        },
                    ),
                ],
                width=12,
            )
        ],
        id=id,
    )
