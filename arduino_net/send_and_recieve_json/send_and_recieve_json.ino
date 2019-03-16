#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>
#include <ArduinoJson.h>

RF24 radio(7, 8);  

//  radio :  Arduino
// ===================
//   V+   :  3.3V
//   GND  :  GND
//   CSN  :  Pin 8 
//   CE   :  Pin 7
//   MOSI :  Pin 11
//   SCK  :  Pin 13
//   MISO :  Pin 12
//   IRQ  :  No Connection

const byte read_address[6][6] = { "00001", "00002", "00003" };
const int read_num = 3;
const byte write_address[6] = "00100";
int input_num = 0;
char input_json[6][150];
int num = 1;

const size_t capacity = JSON_OBJECT_SIZE(4);
DynamicJsonDocument doc(capacity);

int noisePin = 5;
int motionPin = 6;

// const uint8_t* json = "{\"roomID\":23,\"occupied\":1}";
char this_json[150];

void setup() {
    Serial.begin(9600);
    
    pinMode(noisePin, INPUT);
    pinMode(motionPin, INPUT);
    
    radio.begin();
    radio.openWritingPipe(write_address);
    radio.openReadingPipe(0, read_address[0]);
    radio.setPALevel(RF24_PA_MIN);
    //DynamicJsonDocument doc_in(capacity);

    doc["roomID"] = 56;
    doc["occupied"] = 0;
    doc["noise"] = 0;
    doc["motion"] = 0;
}

void loop() {
  delay(50);
  radio.startListening();
  if(radio.available())
  {
    input_num = 0;
    while(radio.available())
    {
      radio.read(input_json[input_num++], 150);
      if(input_num >= read_num) break;
    }
  }

  delay(50);
  radio.stopListening();
  // write info for current arduino
  // write info for other arduinos
  doc["noise"] = digitalRead(noisePin);
  doc["motion"] = digitalRead(motionPin);
  
  serializeJson(doc, this_json);
  Serial.println("====Self====");
  radio.write(this_json, strlen(this_json));
  Serial.println(this_json);

  Serial.println("===inputs====");
  for(int t = 0; t < read_num; t++)
  {
    radio.write(input_json[t], strlen(input_json[t]));
    Serial.println(input_json[t]);
  }
  
}
