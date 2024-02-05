FROM python:3.9

# Make /frontend directory
RUN mkdir /frontend

# Set the working directory to /frontend
WORKDIR /frontend

# Copy the current directory contents into the container at /frontend
COPY . /frontend

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8501 available to the world outside this container
EXPOSE 8501

# Run the Streamlit application
CMD ["streamlit", "run", "app.py"]