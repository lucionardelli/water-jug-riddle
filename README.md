# Water Jug Riddle

## Overview

Build an application that solves the Water Jug Riddle for dynamic inputs (X, Y, Z). The
simulation should have a UI to display state changes for each state for each jug (Empty, Full, or
Partially Full).

You have an X-gallon and a Y-gallon jug that you can fill from a lake. (Assume lake has unlimited
amount of water.) By using only an X-gallon and Y-gallon jug (no third jug), measure Z gallons of
water.

The jugs do not have markings to measure smaller quantities.

## Goals

1. Measure Z gallons of water in the most efficient way.
2. Build a UI where a user can enter any input for X, Y, Z and see the solution.
3. If no solution, display “No Solution”.

## Limitations

* No partial measurement. Each jug can be empty or full.
* Actions allowed: Fill, Empty, Transfer.
* Use one of the following programming languages: Scala, Java, Nodejs, Go, Python, C, C++, Kotlin.

## How to run

The application runs dockerized and it has a GUI implemented using tkinter. This means that running
the container is not straightforward.

First of all, as usual, we need to create the image:

```sh
$ docker build -t water-jug-riddle .
```

Now, to run the Water Jug Riddle program, we need to give access to our display to Docker:

```sh
$ docker run -u $(id -u $USER):$(id -g $USER) \
           -e DISPLAY=$DISPLAY \
           -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
           --rm \
           water-jug-riddle
```

- `-u` is used to set the name of the user,
- `-e` to set the display,
- `-v` creates a volume in X11-unix to provide display,
- `--rm` to automatically remove the container after usage.

In order to ease this process, a helper script is also provided. The script basically
runs the container, if it fails, it tries to build the image and then tries once more.

Using this script, we can just run:

```sh
$ ./run.sh
```
