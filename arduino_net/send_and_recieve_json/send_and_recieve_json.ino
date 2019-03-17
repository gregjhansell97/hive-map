#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>
#include <ArduinoJson.h>

// the 3 static parameters that must be set for each different arduino node
#define ROOM_ID 3  // unique ID for each arduino/room
#define NUM_INPUTS 2 // number of input radio signals to read from
const uint64_t write_address = 0xB3B4B5B6CDLL; // radio address to write data to

// possible list of addresses to read from
const uint64_t read_address[] = {0x7878787878LL, 0xB3B4B5B6F1LL, 0xB3B4B5B6CDLL};
//                                chan 1 -> 3     chan 2 -> 3     chan 3 -> ??
int noise[100];
int motion[100];
int sample = 0;
float av_noise = 0.0;
float av_motion = 0.0;
bool usingButton = false;

RF24 radio(7, 8);  // creates radio instance

// PINOUT
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
char input_json[NUM_INPUTS][32];// array to hold jsons read from other 
int num = 1;

const size_t capacity = JSON_OBJECT_SIZE(4);
DynamicJsonDocument doc(capacity);

int noisePin = 5;// digital input pin for noise detection
int motionPin = 6;// digital input pin for motion detection

char this_json[32];// array to hold json of current arduino

void setup() {
    Serial.begin(9600);

    // set up input pins
    pinMode(noisePin, INPUT);
    pinMode(motionPin, INPUT);
    for(int r = 0; r < 100; r++)
    {
      noise[r] = 0;
      motion[r] = 0;
    }

    //additional pins to provide 5V and GND
    pinMode(3, OUTPUT);
    pinMode(4, OUTPUT);
    digitalWrite(3, HIGH);
    digitalWrite(4, LOW);
    
    
    radio.begin();
    radio.openWritingPipe(write_address);// open pipe for sending data
    for(int u = 0; u < NUM_INPUTS; u++)
    {
      // opens pipes for reading data from multiple radios
      radio.openReadingPipe(u, read_address[u]);
    }
    radio.setPALevel(RF24_PA_MIN);

    doc["r"] = ROOM_ID;
    doc["c"] = 0;
    doc["n"] = 0;
}

void loop() {
  byte pipeNum = 0;
  radio.startListening();
  delay(100);
  if(radio.available(&pipeNum))
  {
      radio.read(input_json[pipeNum], 32);
  }

  radio.stopListening();
  for(int e = 0; e < 100; e++)
  {
    noise[sample%100] = digitalRead(noisePin);
    if(noise[sample%100] > 0)
    {
      delay(100 - e);
      break;
    }
    delay(1);
  }
  motion[sample++%100] = digitalRead(motionPin);
  av_noise = 0.0;
  av_motion = 0.0;
  for(int t = 0; t < 100; t++)
  {
    av_noise = av_noise + noise[t];
    av_motion = av_motion + motion[t];
  }
  if(av_noise < 10)
  {
    doc["n"] = 1; // room is quiet
  }
  else
  {
    doc["n"] = 0; // room is not quiet
  }
  if(av_motion >= 15)
  {
    doc["c"] = 1;// occupied (motion detected)
  }
  else
  {
    if(av_noise >= 30)              
    {
      doc["c"] = 1;// occupied (no motion, but noise levels high)
    }
    else
    {
      doc["c"] = 0;// unoccupied (no motion or noise)
    }
  }
  if(ROOM_ID == 2 && digitalRead(motionPin))// accounts for arduino with button sensor
  {
    doc["c"] = 0;
  }
  else if (ROOM_ID == 2)
  {
    doc["c"] = 1;
  }
  serializeJson(doc, this_json);
  radio.write(this_json, strlen(this_json));// writes json of current arduino
  Serial.println(this_json);

  for(int t = 0; t < NUM_INPUTS; t++)
  {
      radio.write(input_json[t], strlen(input_json[t]));// writes jsons of input arduinos
      Serial.println(input_json[t]);
  }
  
  
}
