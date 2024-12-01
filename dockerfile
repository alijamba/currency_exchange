# Use an official Python runtime as a parent image
FROM public.ecr.aws/lambda/python:3.12

# Set the working directory in the container
WORKDIR /var/task

# Copy the current directory contents into the container
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Command to run the Lambda function
CMD ["lambda_function.lambda_handler"]
