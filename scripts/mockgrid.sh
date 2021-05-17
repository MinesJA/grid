#! /bin/sh

gnome-terminal -e python -m grid.app -s "127.0.0.1" -p "8083" -n "C" -i "3" -t "t3"


open -a Terminal.app scriptfile



curl -X GET -d arg=val -d arg2=val2 127.0.0.1:8080
curl -X PUT -H "Content-Type: application/json" -d '{"nodes": [{  }}' "YOUR_URI"
  -d '{"name" :1, "url_name": "example" }}' \


  curl -X GET https://127.0.0.1:8081 \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: {token}' \
  -H 'Account-ID: {account-id}' \
  -d '{
        "envType": "Tell",
        "msgType": "AddSibling",
        "msg": {
            "siblingName": "D",
            "siblingAddress": "127.0.0.1:8084",
            "siblingId": "4"
        }
    }'

    nodes=4
    i=0

    while [ $i -lt $usrIn ]; do
        ((i++))
        echo "Starting Node on: 127.0.0.1:808$i"
        python -m grid.app -a "127.0.0.1" -p "808$i" &
        arrVar+=("808$i")
    done






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


