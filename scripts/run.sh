#! /bin/sh

# Take user input of number of nodes I want to start
# Start each node, incrementing 8080 by 1 in each time for port
# Ex. 4 -> 8081, 8082, 8083, 8084
# Output the stdout from each to terminal
# Kill each server if ctrl+c is pressed

# echo "Enter the number of nodes you'd like to start"
# read usrIn

nodes=4
i=0


# TODO: assert user_input is int
# TODO: Better output handling, colorize different nodes?
# TODO: Better sigint handling

arrVar1=()
arrVar2=()

# parser.add_argument('--name', '-n')
# parser.add_argument('--token', '-t')
# parser.add_argument('--address', '-a')
# parser.add_argument('--port', '-p', type=int)
python -m grid.app -s "127.0.0.1" -p "8080" -n "A" -t "t1" # NodeA
python -m grid.app -s "127.0.0.1" -p "8081" -n "B" -t "t2" # NodeA
python -m grid.app -s "127.0.0.1" -p "8082" -n "C" -t "t3" # NodeA
python -m grid.app -s "127.0.0.1" -p "8083" -n "D" -t "t4" # NodeA




curl -X PUT -d arg=val -d arg2=val2 127.0.0.1:8080
curl -X PUT -H "Content-Type: application/json" -d '{"nodes": [{  }}' "YOUR_URI"
  -d '{"name" :1, "url_name": "example" }}' \


  {'address': self.address, 'port': self.port}

'nodes': [{'address': self.address, 'port': self.port}]


{"nodes": [
	{"address": "127.0.0.1", "port": "8081"},
	{"address": "127.0.0.1", "port": "8083"}
	]
} #NodeA siblings

{"nodes": [
	{"address": "127.0.0.1", "port": "8080"},
	{"address": "127.0.0.1", "port": "8082"}
	]
} #NodeB siblings

{"nodes": [
	{"address": "127.0.0.1", "port": "8081"},
	{"address": "127.0.0.1", "port": "8083"}
	]
} #NodeC siblings

{"nodes": [
	{"address": "127.0.0.1", "port": "8082"},
	{"address": "127.0.0.1", "port": "8080"}
	]
} #NodeD siblings



# while [ $i -lt $usrIn ]; do
#     ((i++))
#     echo "Starting Node on: 127.0.0.1:808$i"
#     python -m grid.app -a "127.0.0.1" -p "808$i" &
#     arrVar+=("808$i")
# done






wait

2
"524764c8-787e-11eb-a30d-8c85906e1539"

3
"524678ec-787e-11eb-a22d-8c85906e1539"