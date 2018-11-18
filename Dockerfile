# Start with a base image
FROM python:3.6-alpine

# Install required compilers
RUN apk add --update curl gcc g++

# Install Python dependencies
COPY requirements.txt /
RUN pip install -r requirements.txt

# Copy source code into container
COPY src/ /app
WORKDIR /app

# Run Python script
CMD python drive_ynab_data.py
