# Using while loop
# while true; do

    # Propmt
    echo "Reading gestured data from ble"

    # Your code here
    filename=txt/input.txt
    sudo hcidump -R > $filename
    
    cat $filename

    echo "Your gesture data has been recorded !!"

    # Prompt user to press Enter to continue
    echo "Press Enter for Gesture Recognition"
    read response

    if [[ -z "$response" ]]; then
        # Generate the corresponding csv file
        python3 parser.py -d input
        python3 parser.py -t
    else
       echo "Reading Gesture..."
    fi

# done
