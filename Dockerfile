# Base image
FROM python:3.9-slim

# working directory in the container
WORKDIR /app

# Copy current directory to /app
COPY . /app

# Install requirements
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 outside this container
EXPOSE 8080

# Define environment variable
ENV FLASK_APP=weatherapi.py

# Run app.py when the container launches
CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]
