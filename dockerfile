# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy only the necessary files (e.g., your application files and requirements)
COPY . .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the Flask app will run on
EXPOSE 6000

# Define the command to run the Flask app
CMD ["flask", "--app", "api.api", "run", "--host=0.0.0.0", "--port=6000"]
