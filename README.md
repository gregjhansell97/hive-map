# Hive-Map

Communication Agnostic Distributed Pub-Sub Network

## Description

**Hive-map provides a framework to facilitate message publishing to user defined 
locations.**

A **location** is an abstract point that information can be published to.
A **destination** publishes information to a targeted location. Both location 
and destination instances use **sockets** to communicate with other instances 
across a network. The system is event driven: the event is the delivery of information to 
a location.

![ ](docs/diagrams/node_interaction_01.png)

In the diagram above, each node has a location instance *L* or a 
destination instance *D*. The network is the connections between 
the nodes. The green-node's destination instance cannot directly publish
information to the blue-node's location instance. If the green-node's 
destination instance publishes information then the yellow-node's 
destination instance will pass that information along so that it can
be delivered to the blue-node's location instance. 

**Destinations with matching target locations work together to get their messages
to that location.**

The developer defines the means of communication with sockets and the available
locations. Hive-map delivers published information from destinations to locations.

## Goal

A framework to perform distributed routing of published information from
destinations to locations.

## Components

### Location
A location is an abstract point that information can be published to. A location has
subscribers; these subscribers receive information that is published
to the location. A location is identified by a unique identifier.
If there exists two location instances with the same unique identifier then
any particular publish will likely be delivered to only one of the location
instances.

### Destination
A destination represents an interest in a location. A destination can publish
information to the location of interest. Destinations with the same location interest 
will help get the published information to the location.

### Socket
Locations and destinations use sockets to communicate with one another across a network.
The actual communication implementation is developer defined and follows the
language-specific interface.

## Examples

### Library Occupancy Detection

The goal of library occupancy detection is to get occupancy information from 
rooms in the library to a database. The only location in the system is
the *occupancy database*.  Each room is an independent node that can collect
occupancy information. Every room node has a destination of the 
*occupany database* that they publish occupancy information to. The location and
destinations use radio-communication sockets to get published information from each
destination to the *occupancy database* location.


## Libraries

[Python3 (up-to-date)](https://github.com/gregjhansell97/hive-map-python-3/)

[Embedded Cpp (not-up-to-date)](https://github.com/gregjhansell97/hive-map-cpp/)  
  
