from dash import Dash, html, dcc, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import string
import random


def render_alert(message, color="info", id=None):
    if id is None:
        id_s = "".join(random.choices(string.ascii_uppercase + string.digits, k=5))
        id = f"loading-output-message-{id_s}"
    return html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Div(
                                [
                                    dbc.Alert(
                                        message,
                                        color=color,
                                    ),
                                ],
                            ),
                        ],
                        width=12,
                    ),
                ],
            ),
        ],
        id=id,
    )


def render_spinner(id=None, color="dark"):
    if id is None:
        id_s = "".join(random.choices(string.ascii_uppercase + string.digits, k=5))
        id = f"loading-output-spinner-{id_s}"
    return html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Div(
                                [
                                    dbc.Spinner(html.Div(id=id), color="dark"),
                                ],
                            ),
                        ],
                        width=12,
                    ),
                ],
            ),
        ],
    )


def render_button(
    title: str = "Submit",
    id=None,
    class_name: str = "me-1",
    color="dark",
    disabled=True,
    active=True,
    n_clicks=0,
):
    if id is None:
        id_s = "".join(random.choices(string.ascii_uppercase + string.digits, k=5))
        id = f"submit_button-{id_s}"
    return html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Div(
                                [
                                    html.Br(),
                                    dbc.Button(
                                        title,
                                        id=id,
                                        color=color,
                                        className=class_name,
                                        disabled=disabled,
                                        active=active,
                                        n_clicks=n_clicks,
                                    ),
                                    html.Br(),
                                    html.Br(),
                                ],
                            ),
                        ],
                        width=12,
                    ),
                ],
            ),
        ],
    )
