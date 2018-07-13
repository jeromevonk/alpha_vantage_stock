from flask import Flask, jsonify, abort, request, make_response, url_for, render_template

import json
import sys
import traceback


import time
import requests
from datetime import datetime, timedelta

# ----------------------------------------------------------------------------------
# Initialization
# ----------------------------------------------------------------------------------
app = Flask(__name__, static_url_path = "")

REQUIRED = ['AtivoNome', 'DataPreco']
# ----------------------------------------------------------------------------------
# Error Handlers
# ----------------------------------------------------------------------------------
@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

# ----------------------------------------------------------------------------------
# Index page
# ----------------------------------------------------------------------------------
@app.route("/")
def start_page():
    ''' Shows the index page '''
    return render_template('index.html')

# ----------------------------------------------------------------------------------
# Get Stock Value
# ----------------------------------------------------------------------------------
@app.route('/stock', methods = ['POST'])
def stock():
    ''' Handle request'''
    if not request.json:
        abort(400)

    for parameter in REQUIRED:
        if not parameter in request.json:
            return jsonify({'error' : 'Missing required parameter: {}'.format(parameter) } ), 400
            
    stock = request.json['AtivoNome']
    date   = request.json['DataPreco']
    
    # Convert to datetime object
    try:
        dt = datetime.strptime(date, ("%Y-%m-%d"))
    except:
        return jsonify({ 'Error message:' : 'Invalid date format, should be YYYY-MM-DD' }), 400

    result, bRet = getStockValue(stock, dt)
    
    if False == bRet:
        return jsonify( { 'AtivoNome': stock, 'DataPreco': date,'Preco': result } ), 400
    
    return jsonify( { 'AtivoNome': stock, 'DataPreco': date,'Preco': result } )

# ----------------------------------------------------------------------------------
# Auxiliar functions
# ----------------------------------------------------------------------------------
def getStockValue(stock, dt):
    '''Get stock value from Alpha Vantage API '''
    to_return = ""
    bRet = True
    _size = 'compact'
    
    if ( datetime.now() < dt ):
        print("Date requested is in the future")
        return "Data requested is in the future", False
        
    # Do we need the 'compact' or the 'full' outputsize?
    # The 'compact' one has the lastest 100 data points, which probably means more than 100 days.
    delta = datetime.now() - dt
    
    # To be on the safe side, ask for the full data when it's more the 100 days diff from today
    if delta > timedelta(days=100):
        print("Delta is {}, requesting full output".format(delta))
        _size = 'full' 
   
    # Make the request
    try:
        start_time = time.monotonic()
        r = requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={}&outputsize={}&apikey=OPVSB0L3RACDA2ZO&datatype=json".format(stock, _size))
        elapsed_time = time.monotonic() - start_time
        print("get_daily took {}s".format(elapsed_time))
        
        # Get the data and metadata
        json_data = json.loads(r.text)

        meta_data = json_data["Meta Data"]
        data      = json_data["Time Series (Daily)"]
        
        # Convert date back to string
        date = dt.strftime("%Y-%m-%d")
        
        # Sorting can be time-consuming, but should not be significant 
        # compared to getting the data over the network
        last_data_point = sorted(data, key=lambda  kv: kv[1])[-1]
        
        # Is there data for this date?
        if ( dt < datetime.strptime(last_data_point, ("%Y-%m-%d")) ):
            to_return = "Data for this date does not exist. Last data point is {}".format(last_data_point)
        else:
            while date not in data:
                print("No data for date {}".format(date)) 
                dt -= timedelta(days=1)
                date = dt.strftime("%Y-%m-%d")
            
            # Get data as a float, than format it as a string with 8 decimal places
            fValue = float(data[date]['4. close'])
            to_return = "{:.8f}".format(fValue)
      
    except:
        to_return = "No data for this stock"
        bRet = False
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback)

    return to_return, bRet
    
# ----------------------------------------------------------------------------------
# Initialize application (don't run app here)
# ----------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug = True)