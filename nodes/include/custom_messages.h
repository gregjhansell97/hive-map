
#ifndef CUSTOM_STRUCTURES_H
#define CUSTOM_STRUCTURES_H

#define LEAF_MSG 1
#define ROUTING_MSG 2
#define PROXIMITY_MSG 3

/**
 * Generic message of same sized length as the other messages
 */
struct Msg {
  Msg():
    type(LEAF_MSG),
    buff{0, 0, 0, 0, 0, 0, 0}{}
  byte type; // type of message (used to cast message)
  byte buff[7]; // excess bytes (likely to be cased to another message
};

/**
   Leaf nodes message regarding motion detected
*/
struct LeafMsg {
  LeafMsg():
    type(LEAF_MSG),
    node_id(-1),
    parent_node_id(-1),
    motion_detected(false),
    buff{0} {}
  byte type; // the type of message
  byte node_id; // id of the leaf node
  uint32_t parent_node_id; // the id of the routing node that listens for sensor data
  bool motion_detected; // true if motion was detected, false otherwise
  byte buff[1]; // excess bytes (all messages a standard size)
};

/**
   Message sent to other routing nodes (and computer proxy) when occupancy is detected in a room
*/
struct RoutingMsg {
  RoutingMsg():
    type(ROUTING_MSG),
    node_id(-1),
    is_occupied(false),
    msg_number(0),
    distance(-1){}

  byte type; // the type of message
  uint32_t node_id; // the id of the routing node
  bool is_occupied; // true if room is occupied, false otherwise
  byte msg_number; // used to keep track of messages to prevents echos
  byte distance; // how are message is from next level
};

/**
   Message sent to perform bellman ford shortest path algorithm
*/
struct ProximityMsg {
  ProximityMsg():
    type(PROXIMITY_MSG),
    node_id(-1),
    distance(0),
    buff{0, 0} {}

  byte type; // the type of message
  uint32_t node_id; // the id of routing node
  byte distance; // the distance to a next level node
  byte buff[2]; // excess bytes (all messages a standard size)
};


#endif
