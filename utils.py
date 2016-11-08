from flask import Flask, Response, jsonify
import os
import pystache
from typing import Dict

import typing

app = Flask(__name__)


def render_mustache(template_filename: str, **kwargs) -> Response:
    template_path = os.path.join('templates', template_filename + '.mustache')
    with app.open_resource(template_path) as f:
        template_str = f.read()
        return pystache.render(template_str, kwargs)


def json_response(data: Dict, status_code: int=200) -> Response:
    response = jsonify(data)
    response.status_code = status_code
    return response
