#!/bin/bash

sleep 5

CONTROLLER_MAC="C8:48:05:85:32:93"

while true; do
    echo "Attempting to connect to controller..."
    bluetoothctl connect $CONTROLLER_MAC

    if bluetoothctl info $CONTROLLER_MAC | grep -q "Connected: yes"; then
        echo "Controller connected successfully!"
        exit 0
    fi

    echo "Controller not found, retrying in 3 seconds..."
    sleep 3
done
