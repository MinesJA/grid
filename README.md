# Grid
A prototype of a distribtued, electric smart-grid using the [Actor Model](https://en.wikipedia.org/wiki/Actor_model) as a basis for how nodes interact with each other. A node represents an entity, connected to the grid, that can either produce or consume energy or both (a house with or without a solar panel, a business, a power plant, etc.). Any one node should know exactly how much energy it is both producing and/or consuming, as well as the net energy of the grid as whole. Nodes should not know the specific consumption or production values of any other nodes in the grid.

Run a Mock Grid
===============
Fork and clone the repo

Run the scripts/run.sh script to run 4 sample nodes, connected to each other:


Get the current net energy from any of the nodes like so: 
`/energy`
Send a message increasing the consumption of to any node like so:
`PUT /energy`
Now get the net energy from a different node and notice the net has been updated to match the increase in consumption:
`GET /energy`

Design
======
Grid is composed of a series of nodes in an undirected graph, each representing some entity connected to the grid. Each node can theoretically produce and consume electricity. In the real world this would cover the full range of possible connected entitites from residential or commercial buildings with solar panels (producer and consumer) to residential or commercial without any means of producing electricity (strict consumer) to power plants (strict producer).

Each node has three main jobs: 

    1) Maintain it's own production and consumption state. i.e. If a node is producing 5kwH and consuming 10kwH, it should register a consumption of 5 and production of 10.
    2) Be in sync with all other nodes with regards the net ouput of the system. i.e. If 3 connected nodes are outputting a net total of 10kwH and the first node increases it's consumption by 2kwH, then the new net output of the Grid will be 10kwH-8kwH and each node should recalculate their net energy to reflect this.
    3) Maintain an undirected relationship to it's siblings. ie. If nodeX is added as a sibling to nodeY, then nodeY should also add nodeX as its sibling.

Grid is written in Python 3. At the heart of Grid is a Node object which runs it's own [Gunicorn]('https://github.com/benoitc/gunicorn') server with requests being handled using the [Falcon Web framework]('https://github.com/falconry/falcon'). Theoretically, nodes could be run on something as simple as a RaspberryPi, which would register changes from the production and consumption values of it's meter. All nodes expose a GET '/nodes' route availible for adding sibling nodes which serves as the main entry point for joining the network. The only thing required is the address and port of the route. Once added, nodes will automatically attempt to stay in sync when changes to any individual node is registered.

Why?
====
This project was inspired by Gretchen Bakke's excellent book ['The Grid'](https://www.amazon.com/Grid-Fraying-Between-Americans-Energy-ebook/dp/B01DM9Q6CQ) which outlines some of the challenges the electrical grid has with onboarding renewables. In short, the grid was originally designed with a clear distinction between producers and consumers. With the advent of renewables, consumers can also be producers, which disrupts the existing market dynamics. Renewables also introduce the problem of inconsistent power generation (clouds block the sun, the wind dies down, steady streams become raging rivers). The combination of these two qualities makes the requirement of a grid in which consumption equals prdouction at any given moment extremely difficult. But at the heart of it, this seems like a graph-based computer science problem. How do you create a distributed system in which each node can act indepently but for which the sum output of all nodes in the network must meet certain requirements at any given moment (production == consumption). In creating a network of nodes that can stay distributed yet in-sync, this project serves as the first step towards attempting to solve some of the other more difficult challenges of modernizing the grid.

Design
======
Grid is composed of a series of nodes in an undirected graph, each representing some entity connected to the grid. Each node can theoretically produce and consume electricity. In the real world this would cover the full range of possible connected entitites from residential or commercial buildings with solar panels (producer and consumer) to residential or commercial without any means of producing electricity (strict consumer) to power plants (strict producer).

Each node has three main jobs: 

    1) Maintain it's own production and consumption state. ie. If a node is producing 5kwH and consuming 10kwH, it should register those values.
    2) Be in sync with all other nodes with regards the net ouput of the system. ie. If 3 connected nodes are outputting a net total of 10kwH, each node individually should register that net.
    3) Maintain an undirected relationship to it's siblings. ie. If nodeX is added as a sibling to nodeY, then nodeY should also add nodeX as its sibling.

Technical Design
================
At the heart of Grid is a Node object which runs it's own [Gunicorn]() server with requests being handled using the [Falcon]() REST framework. Theoretically, nodes could be run on something as simple as a RaspberryPi, which would register changes from the production and consumption values of it's meter. All nodes expose a GET '/nodes' route availible for adding sibling nodes which serves as the main entry point for joining the network. The only thing required is the address and port of the route. Once added, nodes will automatically attempt to stay in sync when changes to any individual node is registered.

Setup
=====
Fork and clone the repo

Run the scripts/run.sh script to run 4 sample nodes


Run
===



Contributing
============
