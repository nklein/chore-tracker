# CHORE-TRACKER

## Overview

This is a Python application that runs on a Raspberry Pi using a STEMMA-QT I2C interface to four arcade buttons.
The application can be configured to allow each button to have a different chores schedule.
When it is time for a button (owner) to do chores, the button will flash.
After 45 minutes of flashing, the button will flash faster.
If the button is pressed while flashing, it will become solid on indicating that chores are underway.
If the button is pressed while solid on, it will turn off reflecting that chores are complete.

## Installation

To install the application, ensure that the `INSTALL_DIR` is set appropriately in the `Makefile`.
Then, run:

    make install

This will copy the application to the specified directory and start it using `systemd`.

You can edit the `${INSTALL_DIR}/etc/config.json` appropriately so that the `syslog` logging reflects the button owners.
After editing the configuration file, you can restart the app using `systemd`:

    systemctl restart chore-tracker.service

## Creating a development environment

The application requires Python 3.
It also requires the python packages listed in the `requirements.txt` file.

You should set up a Python virtual enviroment to use when testing the application:

    python -m venv python-venv

With that created, you can install a local copy of the required packages:

    . python-venv/bin/activate
	pip3 install --no-cache-dir -r requirements.txt

After that, you can run the application manually.

    cd app
    python main.py

Unless your `etc/config.json` specifies `"sim_mode": true`, you should stop the `systemd` service before running.

    systemctl stop chore-tracker.service
