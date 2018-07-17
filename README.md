# alpha_vantage_stock
Small service to get data from [alpha vantage API](https://www.alphavantage.co/documentation/).

Try it [here](https://jeromevonk.github.io/other/test_lambda.html).

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

The stock price returned as "Preco" is obtained as follows:

1. A call to the Alpha Vantage API with the function *TIME_SERIES_DAILY_ADJUSTED* is made;
2. The stock value for that desired date is obtained from the "4.close" key. If the desired date is not present on the retrieved data, the day before is considered;
3. The stock value is formatted with 8 decimal places.


## AWS Lambda

- lamba.py : source code for the lambda
- StockAPI-v1-swagger-postman.json : exported stage for use with [Postman](https://www.getpostman.com/)
- test_lambda.py : test cases with python
- test_lambda.html: simple front-end test ([TRY IT HERE](https://jeromevonk.github.io/other/test_lambda.html))

How to use: make a POST request to 'https://9mj1a85khj.execute-api.sa-east-1.amazonaws.com/v1/'

## Localhost - a flask service (for initial development)

- server.py : flask server code
- test.py : test cases with python
- templates/index.html: simple front-end test

*How to use*: make a POST request to 'http://localhost:5000/stock'