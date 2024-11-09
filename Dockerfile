# Use the official Python image from Docker Hub
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project to the container
COPY . /app/

# Expose the port the app will run on (default for FastAPI/Flask is 8080)
EXPOSE 8080

# Define the entrypoint for your container to run the app
CMD ["python", "main.py"]