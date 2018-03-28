/*
 * Arduino Robot Control
 * Motor movement defined
 * Speed can be changed
 * 
 */

#include "GY_85.h"
#include <Wire.h>

GY_85 GY85;

int ENA = 5;
int ENB = 6;
int INPUT2 = 7;
int INPUT1 = 8;
int INPUT3 = 12;
int INPUT4 = 13;

int Left_Speed_Hold;
int Right_Speed_Hold;

#define MOTOR_GO_FORWARD  { digitalWrite(INPUT1,LOW);digitalWrite(INPUT2,HIGH);digitalWrite(INPUT3,LOW);digitalWrite(INPUT4,HIGH);}                        
#define MOTOR_GO_BACK    {   digitalWrite(INPUT1,HIGH);digitalWrite(INPUT2,LOW);digitalWrite(INPUT3,HIGH);digitalWrite(INPUT4,LOW);}    //车体前进
#define MOTOR_GO_RIGHT    {digitalWrite(INPUT1,HIGH);digitalWrite(INPUT2,LOW);digitalWrite(INPUT3,LOW);digitalWrite(INPUT4,HIGH);}    //车体前进
#define MOTOR_GO_LEFT   {digitalWrite(INPUT1,LOW);digitalWrite(INPUT2,HIGH);digitalWrite(INPUT3,HIGH);digitalWrite(INPUT4,LOW);}    //车体前进
#define MOTOR_GO_STOP   {digitalWrite(INPUT1,LOW);digitalWrite(INPUT2,LOW);digitalWrite(INPUT3,LOW);digitalWrite(INPUT4,LOW);}    //车体前进

const char startOfNumberDelimiter = '<';
const char endOfNumberDelimiter   = '>';

void setup()
{
    pinMode(ENA,OUTPUT); 
    pinMode(ENB,OUTPUT); 
    pinMode(INPUT1,OUTPUT); 
    pinMode(INPUT2,OUTPUT); 
    pinMode(INPUT3,OUTPUT); 
    pinMode(INPUT4,OUTPUT); 

    Serial.begin(57600);

    
//
//  //------ ACCELEROMETER SETUP --------//
//
//  // DATA_FORMAT Register
//  // Set range for g resolution
//  // 2, 4, 8, 16 are the possible ranges
//  Wire.beginTransmission(ACC);
//  Wire.write(0x31);
//  Wire.write(0x01);
//  Wire.endTransmission();
//
//  // Power Control Register
//  // Set the measure bit to 1 to init measuring mode
//  Wire.beginTransmission(ACC);
//  Wire.write(0x2D);
//  Wire.write(0x08);
//  Wire.endTransmission();
//
//  //------ MAGNETOMETER SETUP --------//
//  
//  // Mode Register
//  // Set as continuous-measurement mode
//  Wire.beginTransmission(MAG);
//  Wire.write(0x02);
//  Wire.write(0x00);
//  Wire.endTransmission();
//
//  //------ GYROSCOPE SETUP -----------//
//
//  // Power Management
//  // Set clock source as internal oscillator
//  Wire.beginTransmission(GYRO);
//  Wire.write(0x3E);
//  Wire.write(0x00);
//  Wire.endTransmission();
//
//  // Sample Rate Divider 
//  // 125 Hz
//  Wire.beginTransmission(GYRO);
//  Wire.write(0x15);
//  Wire.write(0x07);
//  Wire.endTransmission();
//
//  // DLPF, Full Scale
//  // Set at +/- 2000 degrees/sec, 1kHz sample rate, 5Hz low pass filter bandwidth
//  Wire.beginTransmission(GYRO);
//  Wire.write(0x16);
//  Wire.write(0x1E);
//  Wire.endTransmission();
//
//  // Interrupt Configuration
//  // Set to disable read of all raw data
////  Wire.beginTransmission(MAG);
////  Wire.write(0x17);
////  Wire.write(0x00);
////  Wire.endTransmission();
////  

//  delay(10);

}


void setSpeed(){
    analogWrite(ENB,Left_Speed_Hold);
    analogWrite(ENA,Right_Speed_Hold);
}


void loop() {  
    while(1) {

      int ax = GY85.accelerometer_x( GY85.readFromAccelerometer() );
      int ay = GY85.accelerometer_y( GY85.readFromAccelerometer() );
      int az = GY85.accelerometer_z( GY85.readFromAccelerometer() );
        
      int cx = GY85.compass_x( GY85.readFromCompass() );
      int cy = GY85.compass_y( GY85.readFromCompass() );
      int cz = GY85.compass_z( GY85.readFromCompass() );
    
      float gx = GY85.gyro_x( GY85.readGyro() );
      float gy = GY85.gyro_y( GY85.readGyro() );
      float gz = GY85.gyro_z( GY85.readGyro() );
      float gt = GY85.temp  ( GY85.readGyro() );
    
      Serial.println ("Starting ...");
      Serial.print (startOfNumberDelimiter);    
      Serial.print (ax);    // send the number
      Serial.print (endOfNumberDelimiter);  
      Serial.println ();

      if (Serial.available() > 0) {

        char inChar = Serial.read();
        Serial.write(inChar);

        if(inChar == 'w') {
         
          Left_Speed_Hold = 200;
          Right_Speed_Hold = 200;
          setSpeed();
          MOTOR_GO_FORWARD;
          delay(500);
          MOTOR_GO_STOP;
        }

        else if(inChar == 'a') {
          Left_Speed_Hold = 100;
          Right_Speed_Hold = 200;
          setSpeed();
          MOTOR_GO_LEFT;
          delay(500);
          MOTOR_GO_STOP;
        }

        else if(inChar == 's') {
          Left_Speed_Hold = 200;
          Right_Speed_Hold = 200;
          setSpeed();
          MOTOR_GO_BACK;
          delay(500);
          MOTOR_GO_STOP;
        }

        else if(inChar == 'd') {
          Left_Speed_Hold = 200;
          Right_Speed_Hold = 100;
          setSpeed();
          MOTOR_GO_RIGHT;
          delay(500);
          MOTOR_GO_STOP;

        }

        else {
          delay(500);
          MOTOR_GO_STOP;
        }

        delay(10);
        
      }      
      
    }  
    
  }

