# alpha_vantage_stock
Small service to get data from alpha vantage API

Example input:

```json
{
	"AtivoNome": "GOOGL",
	"DataPreco": "2018-07-04"
}
```

Example format:

```json
{
	"AtivoNome": "GOOGL",
	"DataPreco": "2018-07-04",
	"Preco": "1116.28000000"
}
```

## Localhost - a flask service (for initial development)

- server.py : flask server code
- test.py : test cases
- templates/index.html: simple front-end test

*How to use*: make a POST request to 'http://localhost:5000/stock'

## AWS Lambda

- lamba.py : source code for the lambda
- StockAPI-v1-swagger-postman.json : exported stage for use with [Postman](https://www.getpostman.com/)
- test_lambda.py : test cases

*How to use*: make a POST request to 'https://9mj1a85khj.execute-api.sa-east-1.amazonaws.com".