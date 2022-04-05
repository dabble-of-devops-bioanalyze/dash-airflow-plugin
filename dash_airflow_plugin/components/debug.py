import dash
import json
from dash import Dash, html, dcc, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
from datetime import datetime
import string
import random


def render_ctx(id=None):
    if id is None:
        id_s = "".join(random.choices(string.ascii_uppercase + string.digits, k=5))
        id = f"debug-{id_s}"
    ctx = dash.callback_context
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    ctx_msg = json.dumps(
        {
            "states": ctx.states,
            "triggered": ctx.triggered,
            # "inputs": ctx.inputs,
            "dt": dt_string,
            "id": id,
        },
        indent=2,
    )
    return html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [html.Pre(ctx_msg)],
                        width=12,
                    ),
                ],
            ),
        ],
        id=id,
    )


def render_data(id="debug", data={}):

    ctx_msg = json.dumps(
        data,
        indent=2,
    )
    return html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [html.Pre(ctx_msg)],
                        width=12,
                    ),
                ],
            ),
        ],
        id=id,
    )

