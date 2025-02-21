from flask import Flask,request
import flask
import threading
import os
import sys
import json
import pytz
ist = pytz.timezone('Asia/Kolkata')
from datetime import datetime
import pandas as pd
import numpy as np
from calclulate_price import calculate_dynamic_beer_price
import google.generativeai as genai

key=os.getenv('GEMINI_KEY')
genai.configure(api_key=key)
# for m in genai.list_models():
#     if 'generateContent' in m.supported_generation_methods:
#         print(m.name)


########## FLASK CODE BEGINS ##########

app = Flask(__name__)
# from flask_cors import CORS
# CORS(app)

@app.route('/ping', methods=['GET'])
def ping():
    return flask.Response(response='Successful Ping')

@app.after_request
def add_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'  # Adjust as needed
    return response
 

@app.route('/invocations', methods=['POST'])
def query_generation():
    start = datetime.now(ist)
    current_timestamp_start = start.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

    beer_data = request.get_json()
    if not beer_data.get('BaseSellingPrice', None) or beer_data.get('BaseSellingPrice', None) < 0:
        answer=json.dumps({"error":"Base Selling Price is missing"})
        return flask.Response(response=answer, status=403, mimetype='application/json')


    
    try:
        
        predicted_price=calculate_dynamic_beer_price(beer_data)
        schema=f""" You are a FAQ chatbot which takes base selling price and predicted price of a beer based on several factors provided in context.
        Use the context provided {beer_data}, the predicted price is {predicted_price} .
        1. You need to provide the reasoning of % price change in base price and predicted price on factors mentioned above.
        2. Use html format strictly
        Create a 4 bullet pointed short and concise answer for above. Use facts only, do not hallucinate.

        Directly provide the answer, do not say i can help with you that, start with heading like Reasoning behind this Price Prediction.
        """
        
        model=genai.GenerativeModel('gemini-2.0-flash')
        response=model.generate_content(schema)
    
        reasoning=response.text
        print(reasoning)
        answer=json.dumps({"predicted_price":float(predicted_price),"reasoning":reasoning})
    except Exception as e:
        errors = {'Errors':e}
        print(errors)
        answer="Error"
    
    
    return flask.Response(response=answer, status=200, mimetype='application/json')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 8080, threaded = True)
