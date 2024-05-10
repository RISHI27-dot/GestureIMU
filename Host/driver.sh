# Using while loop
while true; do
    # Your code here
    filename=Host/txt/input.txt
    sudo hcidump -R > $filename

    echo "Your gesture data has been recorded !!"

    # Prompt user to press Enter to continue
    echo "Press Enter for Gesture Recognition"
    echo " OR "
    echo "Type exit to exit"
    read response

    if [[ -z "$response" ]]; then
        python3 ./Host/parser.py -t
    elif [[ "$response" == "exit" ]]; then
        exit 0
    else
       echo "Reading Gesture..." 
    fi

done
