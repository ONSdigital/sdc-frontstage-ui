from flask import Flask
import os
import pystache

import typing

app = Flask(__name__)


def render_mustache(template_filename: str, **kwargs):
    template_path = os.path.join('templates', template_filename + '.mustache')
    with app.open_resource(template_path) as f:
        template_str = f.read()
        return pystache.render(template_str, kwargs)
