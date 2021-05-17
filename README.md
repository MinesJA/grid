# Grid

![alt main](https://www.kth.se/polopoly_fs/1.828526.1600720157!/image/MSc-Software-Engineering-of-Distributed-Systems.jpg)

Overview
========
Grid is an attempt to answer the question: 

> What would a decentralized electrical grid look like?

This project was inspired by Gretchen Bakke's excellent book [*The Grid*](https://www.amazon.com/Grid-Fraying-Between-Americans-Energy-ebook/dp/B01DM9Q6CQ) which outlines some of the challenges the electrical grid has with onboarding renewables. In short, the grid was originally designed with a clear distinction between producers and consumers. With the advent of renewables, consumers can also be producers, which disrupts the existing market dynamics. Renewables also introduce the problem of inconsistent power generation (clouds block the sun, the wind dies down, steady streams become raging rivers). 

In essence, the problem can be stated: 

> Centralized players are responsible for ensuring consumption equals prdouction at any given moment without having any control over an increasing share of the power producers.

At the heart of it, this seems like a problem with forcing a centralized system to operate with decentralized players. Grid attempts to establish a purely decentralized system in which players can act indepenently (produce and consume power) but with rules that push them towards a common goal (net power output = 0 at any given time).

Design
======
### Phase I: Establishing the Network
Grid is composed of a series of nodes in an undirected graph, each representing some entity connected to the grid. Each node can theoretically produce and/or consume electricity. In the real world this would cover the full range of possible connected entitites from strict producers (i.e. a power plant) to consumers that also have power generating capabilities (i.e. a house with solar panels) to strict consumers (i.e. a house with no solar panels).

Each node has three main jobs: 

1. Maintain it's own production, consumption, and net output state.  
    * i.e. If a node is producing 5kwH and consuming 10kwH, it should register those values as well as a net of -5kwH.
2. Maintain an undirected relationship to it's siblings.  
    * i.e. If nodeX is added as a sibling to nodeY, then nodeY should also add nodeX as its sibling.
3. Be in sync with all other nodes with regards the net ouput of the system.  
    * i.e. If 3 connected nodes are individually generating a net output state of 5kwH, 10kwH, and -5kwH, respectively, then each node individually should register the total net output of the grid as a whole as 10kwH (5kwH+10kwH-5kwH=10kwH).

Nodes communicate with each other according to the rules of the Actor model. Only a Node can change it's own state and Nodes communicate with each other by sending each other messages which each node processes sequentially.

Setup
=====
Fork and clone the repo
Cd into the repo
Install depenencies:
```
$ pip install --user --requirement ./requirements.txt
```

Run
===
Run a Node by running the following from within the main directory:
```
$ python -m grid.app -s {host address} -p {port} -n {Node Name} -i {Node ID} -t {token}
```

Example:
```
$ python -m grid.app -s "127.0.0.1" -p "8081" -n "A" -i "1" -t "t1"
```

Using
=====
You can run a single instance of Grid but, as it's name suggests, the application is much
more interesting as an actual Grid. To start, lets run 4 instances with their own names and ids. 
To see the messaging between nodes, it's helpful to run an instance per Terminal window like so:

[insert screenshot]

Run the following, one instance per Terminal window:

```
<!-- Start Node A: Terminal 1 -->
$ python -m grid.app -s "127.0.0.1" -p "8081" -n "A" -i "1" -t "t1"

<!-- Start Node B: Terminal 2 -->
$ python -m grid.app -s "127.0.0.1" -p "8082" -n "B" -i "2" -t "t2"

<!-- Start Node C: Terminal 3 -->
$ python -m grid.app -s "127.0.0.1" -p "8083" -n "C" -i "3" -t "t3"

<!-- Start Node D: Terminal 4 -->
$ python -m grid.app -s "127.0.0.1" -p "8084" -n "D" -i "4" -t "t4"
```

Now, let's send some messages. At the moment, Nodes respond to 4 Message Types: 

1. UpdateNet, 
2. SyncGrid, 
3. AddSibling, 
4. UpdateEnergy

We'll focus on AddSibling and UpdateEnergy for now.

Node's start with default production and consumption values of 0. To start, let's update Update Node's A 
and B's production and consumption values. In reality, UpdateEnergy requets would be sent by IoT devices connected to the entities meter and/or energy production equipment (solar panels, etc.), which would register any changes in production and consumption.

```
    <!-- Sending to Node A -->
    curl --location --request GET 'http://127.0.0.1:8081/messaging' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "envType": "Tell",
        "msgType": "UpdateEnergy",
        "msg": {
            "production": 0,
            "consumption": 10
        }
    }'

    <!-- Sending to Node B -->
    curl --location --request GET 'http://127.0.0.1:8082/messaging' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "envType": "Tell",
        "msgType": "UpdateEnergy",
        "msg": {
            "production": 20,
            "consumption": 5
        }
    }' 
```

Note that at this point, both Node's are still a Grid of one each as they are not connected to each other
or any other Node (that's what the AddSibling command is for). That means that their net output is now going to
be -10 for Node A (production 0 - consumption 10 = Net -10) and 15 for Node B (production 20 - consumption 5 = Net 15).

Now let's associate them with each other.

```
    <!-- Tell Node A to add Node B as a sibling -->
    curl --location --request GET 'http://127.0.0.1:8081/messaging' \
    --header 'Content-Type: application/json' \
    --header 'Accept: application/json' \
    --data-raw '{
        "envType": "Tell",
        "msgType": "AddSibling",
        "msg": {
            "siblingName": "B",
            "siblingAddress": "127.0.0.1:8081",
            "siblingId": "2"
        }
    }'
```

You'll notice a couple of things happening. Node A should receive the message and almost immediately sends a Ask message to 
B to add themselves. B receives the Ask, adds A, then responds to A with it's details. A receives the Response and adds B. This back and forth is to ensure that all AddSibling requests result in a bidirectional relationship between the Nodes.

Next, A sends a SyncGrid message. Imagine Node B was already part of a massive Grid full of hundreds of interconnected Nodes. With the addition of A, all Nodes would need to resync their current net values. The SyncGrid message triggers that process. Upon reception of the SyncGrid message, Node's send out their own UpdateNet message, which is responsible for traversing the grid, collecting all the indivdiual net values of each Node and summing them up for that particular Node.

In short, SyncGrid kicks off the UpdateNet process and the UpdateNet process collecs the most up to date net value for the grid as a whole for each Node which sends it out.








```
curl --location --request GET 'http://127.0.0.1:8081/messaging' \
--header 'Content-Type: application/json' \
--header 'Accept: application/json' \
--data-raw '{
    "envType": "Tell",
    "msgType": "AddSibling",
    "msg": {
        "siblingName": "B",
        "siblingAddress": "127.0.0.1:8082",
        "siblingId": "2"
    }
}'
```

```
    headers = {

    }

    curl --location --request GET 'http://127.0.0.1:8082/messaging' \
    --header 'Content-Type: application/json' \
    --header 'Accept: application/json' \
    --header 'Authorization: t1' \
    --header 'Account-ID: t1' \
    --data-raw '{
        "envType": "Tell",
        "msgType": "AddSibling",
        "msg": {
            "siblingName": "D",
            "siblingAddress": "127.0.0.1:8084",
            "siblingId": "4"
        }
    }'
```

