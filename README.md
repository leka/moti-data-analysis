# Moti Data Analysis

A simple Python tool to plot data sent by a Moti device (via BT or USB)

## Format

The data must be under this format:

    A, 12345
    M, 1, 0, 1, 0
    L 0, 255, 0, 255
    S, 25.0, 32.0, -20.0, 70.0, -20.0, 10.0

It represents:

* A, XXXXX is the time (in ms) at which the data has been sent
* M, RD, RS, LD, LS are the motor-relative data, right wheel direction,
right wheel speed, left wheel direction, left wheel speed
* L, I, R, G, B are the data relatives to LEDS, I is the LED indicator
(0 for the HEART), R, G and B are the intensities of Red, Green and Blue
* S, AX, AY, AZ, GY, GP, GR reperents the data concerning sensors, AX, AY
and AZ are the accelerometer values and GY, GP, GR the gyroscope values.

## Install

It is recommended to use a Python [virtualenv](http://virtualenv.readthedocs.org/en/latest/),
but it is up to you.

Then, just perform:

    pip install -r requirements.txt
    python data-analysis.py MOTI_DATA_FILE

The plotted data will then appear in the `plot/` directory.
