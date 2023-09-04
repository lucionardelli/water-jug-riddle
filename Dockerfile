# Use the official Python image as the base image
FROM python:3.11

# Set the working directory inside the container
WORKDIR /app


COPY requirements.txt /app
RUN pip install -r /app/requirements.txt

# Copy the current solution into the container at /app
COPY src/ /app/src

# Run the application
CMD ["python", "src/main.py"]
