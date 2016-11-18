from flask import Flask, Response, jsonify
from os.path import join
from pystache import Renderer
from typing import Dict

import typing

app = Flask(__name__)


def render_mustache(template_filename: str, **kwargs) -> Response:
    templates_dir = 'templates'
    template_path = join(templates_dir, template_filename + '.mustache')
    with app.open_resource(template_path) as f:
        template_str = f.read()
        renderer = Renderer(search_dirs=[templates_dir])
        return renderer.render(template_str, **kwargs)


def json_response(data: Dict, status_code: int=200) -> Response:
    response = jsonify(data)
    response.status_code = status_code
    return response
