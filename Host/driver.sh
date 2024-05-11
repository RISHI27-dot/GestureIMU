# Using while loop
# while true; do

    # Propmt
    echo "Reading gestured data from ble"

    # Your code here
    filename=txt/input.txt
    sudo hcidump -R > $filename
    
    # cat $filename

    # echo "Your gesture data has been recorded !!"

    # # Prompt user to press Enter to continue
    # echo "Press Enter for Gesture Recognition"
    # read response

    # if [[ -z "$response" ]]; then
        # Generate the corresponding csv file
    python3 demo.py -d input
    python3 demo.py -t
    # else
    #    echo "Reading Gesture..."
    # fi
    rm txt/input.txt
    rm csv/input_0.csv

# done
