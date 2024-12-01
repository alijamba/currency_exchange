# Currency Exchange Tracking Application (LocalStack Version)

## Setup

### Requirements
- Docker
- LocalStack
- AWS CLI
- Python 3.x
- Git

### Steps to Deploy Locally

1. **Run LocalStack**:

   ```bash
   docker run --rm -it -e DOCKER_HOST=unix:///var/run/docker.sock -p 4566:4566 -p 4510-4559:4510-4559 localstack/localstack
```bach
aws configure set aws_access_key_id test
```
```
aws configure set aws_secret_access_key test
```
```
aws configure set region us-east-1
```
```
zip -r lambda_function.zip lambda_function.py
```
create the Lambda function in LocalStack using the AWS CLI
```bash
aws --endpoint-url=http://localhost:4566 lambda create-function --function-name ExchangeRatesFunction --runtime python3.12 --role arn:aws:iam::000000000000:role/lambda-role --handler lambda_function.lambda_handler --zip-file fileb://lambda_function.zip
```
Create an API Gateway REST AP
```
aws --endpoint-url=http://localhost:4566 apigateway create-rest-api \
    --name "CurrencyExchangeAPI"
```
Get Root Resource ID
```
aws --endpoint-url=http://localhost:4566 apigateway get-resources \
    --rest-api-id <restApiId>
```
Create /rates Resource
```
aws --endpoint-url=http://localhost:4566 apigateway create-resource \
    --rest-api-id <restApiId> \
    --parent-id <rootResourceId> \
    --path-part rates

```
Create a GET method for the /rates resource:
```
aws --endpoint-url=http://localhost:4566 apigateway put-method \
    --rest-api-id <restApiId> \
    --resource-id <resourceId> \
    --http-method GET \
    --authorization-type NONE
```
Integrate Lambda with GET Method
```
aws --endpoint-url=http://localhost:4566 apigateway put-integration \
    --rest-api-id <restApiId> \
    --resource-id <resourceId> \
    --http-method GET \
    --integration-http-method POST \
    --type AWS_PROXY \
    --uri arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/arn:aws:lambda:us-east-1:000000000000:function:ExchangeRatesFunction/invocations
```
Grant API Gateway Permission to Invoke Lambda
```
aws --endpoint-url=http://localhost:4566 lambda add-permission \
    --function-name ExchangeRatesFunction \
    --principal apigateway.amazonaws.com \
    --statement-id some-unique-id \
    --action lambda:InvokeFunction
```
Deploy the API
```
aws --endpoint-url=http://localhost:4566 apigateway create-deployment \
    --rest-api-id <restApiId> \
    --stage-name dev
```
test
```
curl http://localhost:4566/restapis/<restApiId>/dev/_user_request_/rates


