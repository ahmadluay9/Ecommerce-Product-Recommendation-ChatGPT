# Use an official Python runtime as a parent image
FROM tiangolo/uvicorn-gunicorn:python3.9

# Make /backend directory
RUN mkdir /backend

# Set the working directory to /backend
WORKDIR /backend

# Copy the current directory contents into the container at /backend
COPY . /backend

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run the FastAPI application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]