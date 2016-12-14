from flask import Flask, Response, abort, flash, get_flashed_messages, redirect, request, session, url_for
from functools import wraps
import os
from typing import Callable, Tuple
import typing

from utils import json_response, render_mustache

import requests

app = Flask(__name__)

PORT = int(os.environ.get('PORT', 5002))
LOGIN_ROOT_URL                  = os.getenv('LOGIN_ROOT_URL',                  'http://localhost:5009')
ORGANISATION_ROOT_URL           = os.getenv('ORGANISATION_ROOT_URL',           'http://localhost:5010')
QUESTIONNAIRE_RESPONSE_ROOT_URL = os.getenv('QUESTIONNAIRE_RESPONSE_ROOT_URL', 'http://localhost:5006')


@app.errorhandler(401)
def unauthorised(e: Exception) -> Response:
    body = "The server couldn't verify that you are authorised to access the URL requested."
    return render_mustache('error', title='401 - Unauthorised', body=body)


def login_required(func: Callable) -> Callable:
    """Decorator used to prevent access to endpoints by unauthorised users"""
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not session.get('login_token'):
            abort(401)
        return func(*args, **kwargs)
    return decorated_view


def get_login_token_and_data(email_address: str, password: str) -> Tuple[str, str]:
    # call sdc-login-user - which returns a token to be used in subsequent call
    # test data: 'florence.nightingale@example.com', 'password'
    response = requests.post(LOGIN_ROOT_URL + '/login', json={"email": email_address, "password": password},
                             headers={"Content-type": "application/json"})
    return response.json().get('token'), response.json().get('data')


def get_organisations_token_and_data(login_token: str) -> Tuple[str, str]:
    # call sdc-organisations - which returns a token to be used in subsequent call
    response = requests.get(ORGANISATION_ROOT_URL + '/reporting_units', headers={'token': login_token})
    return response.json().get('token'), response.json().get('data')


def get_questionnaires_token_and_data(organisation_token: str, reporting_unit_ref: str) -> Tuple[str, str]:
    # call sdc-questionnaires - which returns the surveys
    url = '{}/questionnaires/{}'.format(QUESTIONNAIRE_RESPONSE_ROOT_URL, reporting_unit_ref)
    response = requests.get(url, headers={'token': organisation_token})
    return response.json().get('token'), response.json().get('data')


@app.route('/', methods=['GET'])
def bounce() -> Response:
    return redirect("/login")


@app.route('/login', methods=['GET'])
def get_login_endpoint() -> Response:
    user_name = session.get('data', {}).get('name')
    messages = get_flashed_messages()
    return render_mustache('login', user_name=user_name, messages=messages)


@app.route('/login', methods=['POST'])
def post_login_endpoint() -> Response:
    email_address = request.form.get('email_address')
    password = request.form.get('password')

    # the front stage sequence is:
    #   1. log the user in and get a login taken
    #   2. use the login token to get the user's organisations and get an organisation token
    #   3. use the organisation token to get the user's surveys / questionnaires

    login_token, login_data = get_login_token_and_data(email_address, password)
    if login_token:
        session['login_token'] = login_token
        session['data'] = login_data
        organisation_token, organisation_data = get_organisations_token_and_data(login_token)
        if organisation_token:
            session['organisation_token'] = organisation_token
            session['data'] = organisation_data
            return redirect(url_for('get_my_surveys_endpoint'))

    flash('Invalid email address/password combination')
    return redirect(url_for('get_login_endpoint'))


@app.route('/logout')
def logout_page() -> Response:
    session.clear()
    return redirect(url_for('get_login_endpoint'))


@app.route('/my-surveys', methods=['GET'])
@login_required
def get_my_surveys_endpoint() -> Response:
    # display the surveys
    organisation_token = session.get('organisation_token')
    #organisation_token = request.headers.get('token')
    reporting_unit_ref = session.get('data', {}).get('reporting_units', [{}])[0].get('organisation', {}).get('reference')
    _, data = get_questionnaires_token_and_data(organisation_token, reporting_unit_ref)
    surveys = data.get('surveys') or []
    user_name = session.get('data', {}).get('name')
    return render_mustache('my-surveys', surveys=surveys, user_name=user_name)


# quick hack to serve the CSS file
@app.route('/dist/site.min.css', methods=['GET'])
def css_endpoint() -> Response:
    filename = 'dist/site.min.css'
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), filename)
    with open(path, 'r') as f:
        return Response(f.read(), mimetype='text/css')


if __name__ == '__main__':
    app.config['SECRET_KEY'] = 'ITSASECRET'
    app.run(debug=True, host='0.0.0.0', port=PORT)
