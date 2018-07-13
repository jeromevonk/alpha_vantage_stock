import json
from botocore.vendored import requests
from datetime import datetime, timedelta

# Required keys
REQUIRED = ['AtivoNome', 'DataPreco']

# Alpha Vantage API
API_TOKEN = "OPVSB0L3RACDA2ZO"
FUNCTION = "TIME_SERIES_DAILY_ADJUSTED"

def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))

    for parameter in REQUIRED:
        if not parameter in event:
            return 'Missing required parameter: {}'.format(parameter)

    stock  = event['AtivoNome']
    date   = event['DataPreco']

    # Convert to datetime object
    try:
        dt = datetime.strptime(date, ("%Y-%m-%d"))
    except:
        return { 'Error message:' : 'Invalid date format, should be YYYY-MM-DD' }

    result, bRet = getStockValue(stock, dt)

    return { 'AtivoNome': stock, 'DataPreco': date, "Preco": result }


def getStockValue(stock, dt):
    '''Get stock value from Alpha Vantage API '''
    to_return = ""
    bRet = True
    _size = 'compact'
    
    # The date requested can't be in the future
    if ( datetime.now() < dt ):
        return "Data requested is in the future", False

    # Do we need the 'compact' or the 'full' outputsize?
    # The 'compact' one has the lastest 100 data points, which probably means more than 100 days.
    delta = datetime.now() - dt

    # To be on the safe side, ask for the full data when it's more the 100 days diff from today
    if delta > timedelta(days=100):
        _size = 'full'

    # Make the request
    try:
        r = requests.get("https://www.alphavantage.co/query?function={}&symbol={}&outputsize={}&apikey={}&datatype=json".format(FUNCTION, stock, _size, API_TOKEN))

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
                dt -= timedelta(days=1)
                date = dt.strftime("%Y-%m-%d")

            # Get data as a float, than format it as a string with 8 decimal places
            fValue = float(data[date]['4. close'])
            to_return = "{:.8f}".format(fValue)

    except:
        to_return = "No data for this stock"
        bRet = False

    return to_return, bRet