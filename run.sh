#!/bin/sh

# Define the Docker image name
DOCKER_IMAGE="water-jug-riddle"

# Define the Docker run command
DOCKER_RUN_CMD="docker run -u=$(id -u $USER):$(id -g $USER) \
           -e DISPLAY=$DISPLAY \
           -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
           --rm \
           $DOCKER_IMAGE"

# Run the Docker command
$DOCKER_RUN_CMD

# Check the exit code of the command
if [ $? -eq 130 ]; then
    # If exit code is 130, try building the Docker image
    docker build -t $DOCKER_IMAGE .
    
    # Then rerun the Docker command
    $DOCKER_RUN_CMD
fi
