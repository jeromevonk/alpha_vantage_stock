#-------------------------------------------------------------------------------
# Name:        Alpha_vantage stock test
# Author:      Jerome Vergueiro Vonk
# Created:     10/07/2018
#-------------------------------------------------------------------------------
import requests

#-------------------------------------------------------------------------------
# Helper function
#-------------------------------------------------------------------------------
def equityValue(stock):
    try:
        r = requests.post(AWS, json = stock)
        print(r.status_code)
        print(r.text)

    except requests.exceptions.RequestException as e:
        print(e)

#-------------------------------------------------------------------------------
# Hosted locally
#-------------------------------------------------------------------------------
AWS  = 'https://9mj1a85khj.execute-api.sa-east-1.amazonaws.com/v1/'

#-------------------------------------------------------------------------------
# Valid cases
#-------------------------------------------------------------------------------

# a) Near date
print("Valid data: near date")
input = {"AtivoNome": "GOOGL", "DataPreco": "2018-07-04" }
equityValue(input)

# b) Date far in the past
print("Valid data: date far in the past")
input = {"AtivoNome": "GOOGL", "DataPreco": "2011-01-05" }
equityValue(input)

#-------------------------------------------------------------------------------
# Invalid cases
#-------------------------------------------------------------------------------
# c) Invalid stock symbol
print("Invalid data: invalid stock symbol")
input = {"AtivoNome": "GOOGLE", "DataPreco": "2018-07-04" }
equityValue(input)

# d) Wrong date format
print("Invalid data: wrong date format")
input = {"AtivoNome": "GOOGL", "DataPreco": "07/07/2018" }
equityValue(input)

# e) Date in the future
print("Invalid data: date in the future")
input = {"AtivoNome": "GOOGL", "DataPreco": "2045-07-04"}
equityValue(input)

# f) Date too far in the past
print("Invalid data: date too far in the past")
input = {"AtivoNome": "GOOGL", "DataPreco": "1501-07-04"}
equityValue(input)

# g) Missing stock symbol
print("Invalid data: missing stock symbol")
input = {"DataPreco": "2018-07-04"}
equityValue(input)

# h) Missing date
print("Invalid data: missing date")
input = {"AtivoNome": "GOOGL" }
equityValue(input)