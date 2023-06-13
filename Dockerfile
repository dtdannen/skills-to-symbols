# Use an official Python runtime as a parent image
FROM python:3.7-buster

# Set the working directory in the container
WORKDIR /app

# Add files from your Docker client’s current directory.
ADD . /app

# Install OpenCV and Pygame dependencies
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libsdl-image1.2-dev \
    libsdl-mixer1.2-dev \
    libsdl-ttf2.0-dev \
    libsdl1.2-dev \
    libsmpeg-dev \
    python-numpy \
    subversion \
    libportmidi-dev \
    ffmpeg \
    libswscale-dev \
    libavformat-dev \
    libavcodec-dev \
    libblas-dev \
    liblapack-dev

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Run the command within your image filesystem.
CMD ["python", "build_treasure_game.py"]
