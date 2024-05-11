#!/bin/bash

# Get input string from user
input_string=$1


# Iterate over each character of the input string
for (( i=0; i<${#input_string}; i++ )); do
    char="${input_string:i:1}"
    test_file_name="test_"
    test_file_name+=$i
    test_file_name+=_
    test_file_name+=$char
    test_file_name+=.csv
    # echo $test_file_name

    r=$((1 + RANDOM % 60))
    random_file_name="$char_$r.csv"
    random_file_name="$char"
    random_file_name+=_
    random_file_name+=$r
    random_file_name+=.csv
    echo "$random_file_name -> $test_file_name"

    cp $random_file_name $test_file_name

done

ls | grep test
