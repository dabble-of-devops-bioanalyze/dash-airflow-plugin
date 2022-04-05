from datetime import datetime, timedelta
from flask_login import current_user
import flask
from flask import redirect, current_app, session, has_app_context, url_for
from dash import (
    dcc,
    html,
    Dash,
)
from dash.dash import _default_index, _validate, _get_paths, _flask_compress_version
from dash._configs import get_combined_config, pathname_configs
import dash_bootstrap_components as dbc
from pkg_resources import get_distribution, parse_version
import collections
import pandas as pd
import uuid
import os
import pickle

from dash.resources import Scripts, Css
from dash._utils import (
    AttributeDict,
    format_tag,
    generate_hash,
    inputs_to_dict,
    inputs_to_vals,
    interpolate_str,
    patch_collections_abc,
    split_callback_id,
    to_json,
)
import os
import sys
import collections
import importlib
from importlib.machinery import ModuleSpec
import pkgutil
import threading
import re
import logging
import time
import mimetypes
import hashlib
import base64
from urllib.parse import urlparse

import flask
from flask_compress import Compress
from werkzeug.debug.tbtools import get_current_traceback
from pkg_resources import get_distribution, parse_version
from dash import dcc
from dash import html
from dash import dash_table

"""
Dash looks for a flask.Flask object, but we are passing in a werkzeug.local.LocalProxy

This is a very verbose hack that just lets us use the flask context with the current_app to add dash apps
"""


class CustomDash(Dash):
    def __init__(
        self,
        name=None,
        server=True,
        assets_folder="assets",
        assets_url_path="assets",
        assets_ignore="",
        assets_external_path=None,
        eager_loading=False,
        include_assets_files=True,
        url_base_pathname=None,
        requests_pathname_prefix=None,
        routes_pathname_prefix=None,
        serve_locally=True,
        compress=None,
        meta_tags=None,
        index_string=_default_index,
        external_scripts=None,
        external_stylesheets=None,
        suppress_callback_exceptions=None,
        prevent_initial_callbacks=False,
        show_undo_redo=False,
        extra_hot_reload_paths=None,
        plugins=None,
        title="Dash",
        update_title="Updating...",
        long_callback_manager=None,
        **obsolete,
    ):
        super().__init__(
            name=name,
            server=False,
            assets_folder=assets_folder,
            assets_url_path=assets_url_path,
            assets_ignore=assets_ignore,
            assets_external_path=assets_external_path,
            eager_loading=eager_loading,
            include_assets_files=include_assets_files,
            url_base_pathname=url_base_pathname,
            requests_pathname_prefix=requests_pathname_prefix,
            routes_pathname_prefix=routes_pathname_prefix,
            serve_locally=serve_locally,
            compress=compress,
            meta_tags=meta_tags,
            index_string=index_string,
            external_scripts=external_scripts,
            external_stylesheets=external_stylesheets,
            suppress_callback_exceptions=suppress_callback_exceptions,
            prevent_initial_callbacks=prevent_initial_callbacks,
            show_undo_redo=show_undo_redo,
            extra_hot_reload_paths=extra_hot_reload_paths,
            plugins=plugins,
            title=title,
            update_title=update_title,
            long_callback_manager=long_callback_manager,
            **obsolete,
        )

        self.server = server
        if name is None:
            try:
                name = getattr(server, "name", "__main__")
            except Exception as e:
                logging.warn(e)

        if (
            self.server is not None
            and not hasattr(self.server.config, "COMPRESS_ALGORITHM")
            and _flask_compress_version >= parse_version("1.6.0")
        ):
            # flask-compress==1.6.0 changed default to ['br', 'gzip']
            # and non-overridable default compression with Brotli is
            # causing performance issues
            self.server.config["COMPRESS_ALGORITHM"] = ["gzip"]

        if self.server is not None:
            self.init_app()
