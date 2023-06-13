# Use an official Python runtime as a parent image
FROM python:3.7-buster

# Set the working directory in the container
WORKDIR /s2s

# Add files from your Docker client’s current directory.
ADD . /s2s

# Install OpenCV dependencies
RUN apt-get update && apt-get install -y libglib2.0-0 libsm6 libxext6 libxrender-dev

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Run the command within your image filesystem.
CMD ["python", "evaluate.py"]
