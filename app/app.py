import numpy as np
from flask import Flask, request, render_template
from sales_forecasting.app.helper import run_model
import pickle

app = Flask(__name__)



@app.route('/', methods=['POST', 'GET'])
def predict():
    if request.method == "POST":
        store_ID = int(request.get_json()['store_ID'])
        day_of_week = int(request.get_json()['day_of_week'])
        date = request.get_json()['date']
        nb_customers_on_day = int(request.get_json()['nb_customers_on_day'])
        open = int(request.get_json()['open'])
        state_holiday = int(request.get_json()['state_holiday'])
        school_holiday = int(request.get_json()['school_holiday'])

        parameters_dict = {
            'store_ID': store_ID,
            'day_of_week': day_of_week,
            'date': date,
            'nb_customers_on_day': nb_customers_on_day,
            'open': open,
            'state_holiday': state_holiday,
            'school_holiday': school_holiday
        }

        output = run_model(parameters_dict)[0]

        return {'prediction_text':output}
    else:
        return {"status": "alive"}


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)