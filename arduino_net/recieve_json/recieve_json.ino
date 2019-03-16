#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

RF24 radio(7, 8); // CNS, CE


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

const byte read_address[6][6] = { "00001", "00002", "00003", "00004" };
const int read_num = 4;
const byte write_address[6] = "00100";

char roomID[] = "23";
char read_input[6][128] = {  };


void setup() {
  Serial.begin(9600);
  radio.begin();
  radio.openWritingPipe(write_address);
  radio.openReadingPipe(0, read_address[0]);
  
  //radio.openReadingPipe(1, read_address[1]);

  //for(int i = 0; i < read_num; i++)
  //{
  //  radio.openReadingPipe(i, read_address[i]);
  //}
  
  radio.setPALevel(RF24_PA_MIN);
  radio.startListening();
}

void loop() {
  radio.startListening();
  if(radio.available())
  {
    radio.read(read_input[0], 128);
    Serial.print("Recieved: ");
    Serial.println(read_input[0]);
  }
  //delay(1200);
  //radio.stopListening();
  
  //create the json object for current arduino
  //radio.write(&roomID, sizeof(roomID));
  //Serial.print("Sent: ");
  //Serial.println(num++);
  //delay(1000);

}
