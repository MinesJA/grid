# Grid

Overview
========
A prototype of a distribtued electrical, smart-grid system which attempts to meet the following requirements:

    1) Supports entities that are producers, consumers, or some combination of the two
    2) Supports entities that have changing rates of production and consumption over time
    3) Has no central orchestrator (is distributed)
    4) Is consistent in it's electricity delivery (minimizes blackouts/brownouts)
    5) Is consistent in it's pricing to consumers

Why?
====
This project was inspired by Gretchen Bakke's excellent book ['The Grid'](https://www.amazon.com/Grid-Fraying-Between-Americans-Energy-ebook/dp/B01DM9Q6CQ) which outlines some of the challenges the electrical grid has with onboarding renewables. In short, the grid was originally designed with a clear distinction between producers and consumers. With the advent of renewables, consumers can also be producers, which disrupts the existing market dynamics. Renewables also introduce the problem of inconsistent power generation (clouds block the sun, the wind dies down, steady streams become raging rivers). The combination of these two qualities makes the requirement of a grid in which consumption equals prdouction at any given moment extremely difficult. But at the heart of it, this seems like a graph-based computer science problem. How do you create a distributed system in which each node can act indepently but for which the sum output of all nodes in the network must meet certain requirements at any given moment (production == consumption).

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