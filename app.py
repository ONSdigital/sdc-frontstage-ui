from flask import Flask
import os
import typing

from utils import render_mustache


app = Flask(__name__)


@app.route('/my-surveys', methods=['GET'])
def my_surveys():
    surveys = [
        {
            'ru_name':   'Treacherous Trees',
            'ru_ref':    '239592852',
            'survey':    'Annual Purchases Survey',
            'period':    '2015-08',
            'status':    'not_started',
            'return_by': '2015-07-31',
        },
        {
            'ru_name':   'Treacherous Trees',
            'ru_ref':    '239592852',
            'survey':    'Financial Institutions Register Survey',
            'period':    '2015-08',
            'status':    'not_started',
            'return_by': '2015-07-31',
        },
        {
            'ru_name':   'Tesco',
            'ru_ref':    '032759874',
            'survey':    'Monthly Wages and Salaries Survey',
            'period':    '2015-08',
            'status':    'not_started',
            'return_by': '2015-07-31',
        },
    ]
    return render_mustache('my-surveys', surveys=surveys)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
