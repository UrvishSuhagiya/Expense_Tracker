# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app/

# Install system dependencies needed for Django and Tkinter
RUN apt-get update && apt-get install -y \
    libsqlite3-dev \
    tk \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on (default 8000 for Django)
EXPOSE 8000

# Run migrations to prepare the database (you can skip this if you prefer to run it manually)
RUN python manage.py migrate

# Start the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
