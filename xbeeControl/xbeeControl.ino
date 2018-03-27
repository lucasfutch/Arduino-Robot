/*
 *  XBee Control 
 *  Control MY Address = 2
 *  Receiver MY Address = 1
 *  
 */

#include <SoftwareSerial.h>
#include <Wire.h>

const char startOfNumberDelimiter = '<';
const char endOfNumberDelimiter   = '>';

SoftwareSerial XBee(2, 3); // RX, TX

void setup() {
  XBee.begin(57600);
  delay(10);
  Serial.begin(9600);
}



void processNumber (const long n) {
  Serial.println (n);
}  


  
void processInput () {
  static long receivedNumber = 0;
  static boolean negative = false;

  byte c = Serial.read ();

  switch (c)
    {
    
    case endOfNumberDelimiter:  
      if (negative) 
        processNumber (- receivedNumber); 
      else
        processNumber (receivedNumber); 
  
    // fall through to start a new number
    case startOfNumberDelimiter: 
      receivedNumber = 0; 
      negative = false;
      break;
      
    case '0' ... '9': 
      receivedNumber *= 10;
      receivedNumber += c - '0';
      break;
      
    case '-':
      negative = true;
      break;
      
    } // end of switch  
  }  // end of processInput
  

void loop() {

  // If data comes in from serial monitor, send it out to XBee
  if (Serial.available()) { 
    processInput();
    XBee.write(Serial.read());
  }
  
  // If data comes in from XBee, send it out to serial monitor
  if (XBee.available()) { 
    Serial.write(XBee.read());
   
  }

}
