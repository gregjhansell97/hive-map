#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>
#include "custom_messages.h"

#define CSN_PIN 8
#define CE_PIN 7

#define MSG_BUFFER_SIZE 5
#define MAX_NEIGHBORS 10
#define NODE_ID 1

struct Neighbor {
  Neighbor():
      node_id(-1),
      distance(0),
      msg_buffer{0, 0, 0, 0, 0}{}
  uint32_t node_id; // the node id of the neighbor
  byte distance; // distance away from neighbor
  byte msg_buffer[MSG_BUFFER_SIZE]; // ring buffer of most recently recieved messages
};

RF24 radio(CE_PIN, CSN_PIN);

const byte routing_channel[6] = "86035";
const byte leaf_channel[6] = "59694";

Neighbor neighbors[MAX_NEIGHBORS];
byte neighbors_count = 0;

byte timer = 0; // number of times through 0.5 second timer
bool publish_proximity_flag = false; // sends a proximity message out when true

/**
 * sets the timer to send out distance status
 */
void setup_interrupts() {
  noInterrupts(); // disable interrupts
  // set up timer interput phase
  TCCR1A = 0;
  TCCR1B = 0;
  TCNT1 = 0;
  OCR1A = 31250; // compare match register (16MHz/256/2Hz)

  TCCR1B |= (1 << WGM12); // CTC mode

  TCCR1B |= (1 << CS12); // 256 prescaler
  
  TIMSK1 |= (1 << OCIE1A); // enable timer compare interrupt

  interrupts(); // re-endable interrupts
}

/**
 * sets the neighbor list to starting values (not guaranteed with lists)
 */
void setup_neighbors() {
  for(uint32_t i = 0; i < MAX_NEIGHBORS; ++i) {
    neighbors[i].node_id = -1; //max value reserved for unkown nodes
    neighbors[i].distance = 0;
    for(byte j = 0; j < MSG_BUFFER_SIZE; ++j) {
      neighbors[i].msg_buffer[j] = 0;
    }
  }
}

void setup() {
  Serial.begin(9600);
  setup_interrupts();
  setup_neighbors();

  radio.begin();
  radio.openWritingPipe(routing_channel); // write proximity when appropriate
  radio.openReadingPipe(0, routing_channel); // listens on routing channel
  radio.setPALevel(RF24_PA_MIN);
  radio.startListening();
}

/**
 * interrupt function that occures ~0.5 seconds
 */
ISR(TIMER1_COMPA_vect)
{
  TCNT1 = 34286; // timer duration
  publish_proximity_flag = timer%3 == 0; // every three ticks
  ++timer;
}

/**
 * sends a message out about the nodes proximity to a computer proxy
 */
void publish_proximity() {
  ProximityMsg msg;
  msg.distance = 0; // its a computer proxy so it's zero away from next level
  msg.node_id = NODE_ID;
  radio.stopListening(); // have to stop listening to write
  radio.write(&msg, sizeof(msg));
  radio.startListening(); // remember to start listening
  publish_proximity_flag = false; // resets flag (if true)
}

/**
 * retrives a neighbor instance from the neighbor table with a given node_id
 * 
 * Args:
 *   node_id(uint32_t): node_id of neighbor being retrieved
 * 
 * Returns:
 *   (Neighbor*): address to neighbor with node_id, NULL if not found
 */
Neighbor* get_neighbor(uint32_t node_id) {
  if(node_id >= 0 && node_id < MAX_NEIGHBORS) {
    Neighbor* nbr = neighbors + node_id;
    nbr->node_id = node_id;
    return nbr;
  }
  return NULL;
}

/**
 * handles a leaf message
 * 
 * Args:
 *     raw_msg(void*) the message recieved over radio
 */
void handle_leaf_msg(void* raw_msg) {
  return; // the computer proxy doesn't do anything for leaf messages
}

/**
 * handles a routing message. It updates a neighbor in the neighbor table with a new ring buffer and writes the message serially
 * 
 * Args:
 *   raw_msg(void*): the message recieved over radio
 */
void handle_routing_msg(void* raw_msg) {
  RoutingMsg* msg = (RoutingMsg*)raw_msg;
  Neighbor* nbr = get_neighbor(msg->node_id);

  if(nbr == NULL) return;

  // adds message to ring buffer or discards it
  byte first_zero = 0;
  bool first_zero_found = false;
  for(byte i = 0; i < MSG_BUFFER_SIZE; ++i) {
    if(!first_zero_found && nbr->msg_buffer[i] == 0) {
      first_zero = i;
      first_zero_found = true;
    }

    //discards message if in ring buffer
    if(msg->msg_number == nbr->msg_buffer[i]) return;
  }
  nbr->msg_buffer[first_zero] = msg->msg_number;
  first_zero = (first_zero + 1)%MSG_BUFFER_SIZE;
  nbr->msg_buffer[first_zero] = 0;

  //THIS PART IS DISTINCTION BETWEEN COMPUTER PROXY AND ROUTING NODE
  //COMPUTER PROXY WRITES MESSAGE SERIALLY WHILE ROUTING NODE SENDS IT
  //OUT IF IT HAS ANYONE CLOSER THAT IS LISTENING
  Serial.println("Routing Message Recieved");
  Serial.print("  node_id: ");
  Serial.println(msg->node_id);
  Serial.print("  is_occupied: ");
  Serial.println(msg->is_occupied);
  Serial.print("  message number: ");
  Serial.println(msg->msg_number);
}

/**
 * handles a proximity message. It updates the neighbor table with a new distance away from the next level
 * 
 * Args:
 *   raw_msg(void*): the message recieved over radio
 */
void handle_proximity_msg(void* raw_msg) {
  ProximityMsg* msg = (ProximityMsg*)raw_msg;
  Neighbor*nbr = get_neighbor(msg->node_id);

  if(nbr == NULL) return;
  nbr->distance = msg->distance; 
}

void loop(){
  if(publish_proximity_flag) {
    publish_proximity();
    //print_neighbor_table();
  }
  if(radio.available()) {
    Msg raw_msg;
    radio.read(&raw_msg, sizeof(raw_msg));
    switch(raw_msg.type) {
      case LEAF_MSG:
        handle_leaf_msg(&raw_msg);
        break;
      case ROUTING_MSG:
        handle_routing_msg(&raw_msg);
        break;
      case PROXIMITY_MSG:
        handle_proximity_msg(&raw_msg);
        break;
    }
  }
}


// DEBUGGING FUNCTIONS
void print_neighbor_table() {
  Serial.println("Neighbors: ");
  for(uint32_t  i = 0; i < MAX_NEIGHBORS; ++i) {
    if(neighbors[i].node_id == i) {
      Serial.print("  ");
      Serial.print(neighbors[i].node_id);
      Serial.println(": ");
      Serial.print("    distance: ");
      Serial.println(neighbors[i].distance);
      Serial.print("    ring buffer:");
      for(byte j = 0; j < MSG_BUFFER_SIZE; ++j) {
        Serial.print(" ");
        Serial.print(neighbors[i].msg_buffer[j]); 
      }
      Serial.print("\n");
    }
  }
}
