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

```bash
aws --endpoint-url=http://localhost:4566 lambda create-function --function-name ExchangeRatesFunction --runtime python3.8 --role arn:aws:iam::000000000000:role/lambda-role --handler lambda_function.lambda_handler --zip-file fileb://lambda_function.zip
```
```
curl http://localhost:4566/restapis/<restApiId>/dev/_user_request_/rates


