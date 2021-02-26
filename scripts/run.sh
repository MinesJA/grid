#! /bin/sh

# Take user input of number of nodes I want to start
# Start each node, incrementing 8080 by 1 in each time for port
# Ex. 4 -> 8081, 8082, 8083, 8084
# Output the stdout from each to terminal
# Kill each server if ctrl+c is pressed

echo "Enter the number of nodes you'd like to start"
read usrIn
i=0


# TODO: assert user_input is int
# TODO: Better output handling, colorize different nodes?
# TODO: Better sigint handling

while [ $i -lt $usrIn ]; do
    ((i++))
    echo "Starting Node on: 127.0.0.1:808$i"
    python -m grid.app -a "127.0.0.1" -p "808$i" &
done

wait