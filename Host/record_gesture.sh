#!/bin/bash

gesture=$1

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
