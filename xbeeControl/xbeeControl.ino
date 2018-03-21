/*
 *  XBee Control 
 *  Control MY Address = 2
 *  Receiver MY Address = 1
 */

#include <SoftwareSerial.h>

SoftwareSerial XBee(2, 3); // RX, TX

void setup() {
  XBee.begin(57600);
  Serial.begin(9600);

}

void loop() {
  
  // If data comes in from serial monitor, send it out to XBee
  if (Serial.available()) { 
    XBee.write(Serial.read());
  }
  
  // If data comes in from XBee, send it out to serial monitor
  if (XBee.available()) { 
    Serial.write(XBee.read());
   
  }

}
