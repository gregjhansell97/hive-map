#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>
#include <ArduinoJson.h>

#define ROOM_ID 23
#define NUM_INPUTS 0

const byte write_address[6] = "00001";
const byte read_address[6][6] = { "00001", "00003", "00004" };


int noise[100];
int motion[100];
int sample = 0;

float av_noise = 0.0;
float av_motion = 0.0;

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

int input_num = 0;
char input_json[3][32];
int num = 1;

const size_t capacity = JSON_OBJECT_SIZE(4);
DynamicJsonDocument doc(capacity);

int noisePin = 5;
int motionPin = 6;

char this_json[32];

void setup() {
    Serial.begin(9600);
    
    pinMode(noisePin, INPUT);
    pinMode(motionPin, INPUT);
    for(int r = 0; r < 100; r++)
    {
      noise[r] = 0;
      motion[r] = 0;
    }
    
    radio.begin();
    radio.openWritingPipe(write_address);
    radio.openReadingPipe(0, read_address[0]);
    radio.setPALevel(RF24_PA_MIN);
    //DynamicJsonDocument doc_in(capacity);

    doc["r"] = ROOM_ID;
    doc["c"] = 0;
    doc["n"] = 0;
}

void loop() {
  delay(100);
  radio.startListening();
  if(radio.available())
  {
    input_num = 0;
    while(radio.available())
    {
      radio.read(input_json[input_num++], 32);
      if(input_num >= NUM_INPUTS) break;
    }
  }

  //delay(10);
  radio.stopListening();
  // write info for current arduino
  // write info for other arduinos
  for(int e = 0; e < 100; e++)
  {
    noise[sample%100] = digitalRead(noisePin);
    if(noise[sample%100] > 0) break;
    delay(1);
  }
  //noise[sample%100] = digitalRead(noisePin);
  motion[sample++%100] = digitalRead(motionPin);
  av_noise = 0.0;
  av_motion = 0.0;
  for(int t = 0; t < 100; t++)
  {
    av_noise = av_noise + noise[t];
    av_motion = av_motion + motion[t];
  }
  doc["n"] = av_noise;
  if(av_motion >= 10)
  {
    doc["c"] = 1;
  }
  else
  {
    if(av_noise >= 50)
    {
      doc["c"] = 1;
    }
    else
    {
      doc["c"] = 0;
    }
  }
  
  serializeJson(doc, this_json);
  radio.write(this_json, strlen(this_json));
  Serial.println(this_json);

  for(int t = 0; t < NUM_INPUTS; t++)
  {
    if(input_json[t] != "\0")
    {
      radio.write(input_json[t], strlen(input_json[t]));
      Serial.println(input_json[t]);
    }
  }
  
}
