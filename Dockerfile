# Use an official Ubuntu 18.04 base image
FROM ubuntu:18.04

# Install Python 3.7, pip, and Node.js
RUN apt-get update && apt-get install -y \
    software-properties-common \
    curl \
    && add-apt-repository ppa:deadsnakes/ppa \
    && curl -sL https://deb.nodesource.com/setup_14.x | bash - \
    && apt-get update && apt-get install -y \
    python3.7 \
    python3-pip \
    python3.7-dev \
    git \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgl1-mesa-glx \
    nodejs \
    && apt-get clean

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install Python dependencies
RUN pip3 install --upgrade pip
RUN pip3 install numpy
RUN pip3 install opencv-python
RUN pip3 install tensorflow==2.5.0
RUN pip3 install mediapipe flask flask-cors

# Install Node.js dependencies and build the React app
RUN cd frontend && npm install && npm run build

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV NAME OpencvMediaPipeFlask

# Copy the React build to a folder served by Flask
# Assume your Flask app is set up to serve files from the 'build' directory
RUN cp -r client/* static/

# Run app.py when the container launches
CMD ["python3.7", "run.py"]
