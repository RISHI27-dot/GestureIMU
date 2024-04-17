#!/bin/bash

gesture=$1

# Check if the txt directory exists
if [ ! -d "txt" ]; then
    echo "txt directory does not exist, creating it"
    mkdir "txt"
fi

# Check if the csv directory exists
if [ ! -d "csv" ]; then
    echo "csv directory does not exist, creating it"
    mkdir "csv"
fi

if [ -z $gesture]
then
    echo "Please provide a gesture among -> 0 2 9"
else
    filename=txt/$gesture".txt"
    echo "Recording data for gesture '$gesture' in $filename"
    sudo hcidump -R > $filename
fi

# TODO : Try to run this in parallel to make visually appleaing.
# while true; do echo -n ". "; sleep 1; done
