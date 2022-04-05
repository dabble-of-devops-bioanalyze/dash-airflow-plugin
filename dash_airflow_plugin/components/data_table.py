from dash import Dash, html, dcc, dash_table
import dash_bootstrap_components as dbc
import pandas as pd


def dash_data_table_columns(
    df: pd.DataFrame, deletable=False, selectable=False, overrides: dict = {}
):
    columns = []
    for i in df.columns:
        if i in overrides:
            columns.append(
                {
                    {
                        "name": i,
                        "id": i,
                        "deletable": overrides.get("deletable", deletable),
                        "selectable": overrides.get("selectable", selectable),
                    }
                }
            )
        else:
            columns.append(
                {"name": i, "id": i, "deletable": deletable, "selectable": selectable}
            )
    return columns


def render_data_table(
    title,
    id,
    data=[],
    columns=[],
    hidden_columns=[],
    row_selectable="single",
    row_deletable=True,
):
    # Setting row_selectable and row_deletable with empty data results in an error
    if len(data) and len(columns):
        row_selectable = row_selectable
        row_deletable = row_deletable
    else:
        row_selectable = None
        row_deletable = False
    return html.Div(
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H5(title),
                        # dbc.Table.from_dataframe(var_df, striped=True, bordered=True, hover=True),
                        dash_table.DataTable(
                            id=f"{id}_dt",
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
        ),
    )
