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
### Phase I: Establishing the NetWork
Grid is composed of a series of nodes in an undirected graph, each representing some entity connected to the grid. Each node can theoretically produce and/or consume electricity. In the real world this would cover the full range of possible connected entitites from strict producers (i.e. a power plant) to consumers that also have power generating capabilities (i.e. a house with solar panels) to strict consumers (i.e. a house with no solar panels).

Each node has three main jobs: 

1. Maintain it's own production, consumption, and net output state.  
    * i.e. If a node is producing 5kwH and consuming 10kwH, it should register those values as well as a net of -5kwH.
2. Maintain an undirected relationship to it's siblings.  
    * i.e. If nodeX is added as a sibling to nodeY, then nodeY should also add nodeX as its sibling.
3. Be in sync with all other nodes with regards the net ouput of the system.  
    * i.e. If 3 connected nodes are individually generating a net output state of 5kwH, 10kwH, and -5kwH, respectively, then each node individually should register the total net output of the grid as a whole as 10kwH (5kwH+10kwH-5kwH=10kwH).

Nodes communicate with each other according to the Actor model. Only a Node can change it's own state and Nodes communicate with each other by sending each other messages which each node processes sequentially.

Setup
=====
Fork and clone the repo

Run
===
Run the scripts/run.sh script to run 4 sample nodes