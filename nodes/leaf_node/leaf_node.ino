#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>
#include "custom_messages.h"

#define CSN_PIN 8
#define CE_PIN 7

#define NODE_ID 2
#define PARENT_NODE_ID 3


RF24 radio(CE_PIN, CSN_PIN);

const byte routing_channel[6] = "86035";
const byte leaf_channel[6] = "59694";

bool motion_detected = false;

bool publish_leaf_msg_flag = false;
byte timer = 0; // number of times through 0.5 second timer

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

void setup() {
  Serial.begin(9600);
  setup_interrupts();

  radio.begin();
  radio.openWritingPipe(leaf_channel); // write proximity when appropriate
  radio.setPALevel(RF24_PA_MIN);
  radio.stopListening();
}

/**
 * interrupt function that occures ~0.5 seconds
 */
ISR(TIMER1_COMPA_vect)
{
  TCNT1 = 34286; // timer duration
  publish_leaf_msg_flag = timer%3 == 0; // every three ticks
  ++timer;
}


void publish_leaf_msg() {
  LeafMsg msg;
  msg.node_id = NODE_ID;
  msg.parent_node_id = PARENT_NODE_ID;
  msg.motion_detected = motion_detected;
  radio.write(&msg, sizeof(LeafMsg));
  publish_leaf_msg_flag = false;
}


void loop(){
  if(publish_leaf_msg_flag) {
    publish_leaf_msg();
    motion_detected = !motion_detected;
  }
  // This is where you'll be sensing motion
}
