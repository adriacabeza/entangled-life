# Use the latest Python image as the base image
FROM python:latest

# Add the current directory (where the Dockerfile resides) to the "/srv/game" directory inside the container
ADD . /srv/game

# Set the working directory to "/srv/game" inside the container
WORKDIR /srv/game

# Upgrade pip to the latest version
RUN pip3 install --upgrade pip

# Install the Python dependencies listed in the "requirements.lock" file
RUN pip3 install -r requirements.lock
