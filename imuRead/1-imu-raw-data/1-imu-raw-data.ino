/*
   MPU6050_raw.ino : example of reading raw IMU data from MPU6050 using Teensy 3.X or Teensy LC

   This file is part of MPU6050.

   MPU6050 is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.
   Hackflight is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.
   You should have received a copy of the GNU General Public License
   along with Hackflight.  If not, see <http://www.gnu.org/licenses/>.
 */

#include "MPU6050.h"
#define ACCELEROMETER_SENSITIVITY 16,384 
#define GYROSCOPE_SENSITIVITY 131

unsigned long newTime;

MPU6050 imu;
int16_t ax, ay, az, gx, gy, gz;

void setup()
{
    Serial.begin(9600);

    Wire.begin();
    imu.writeByte(0x6B, 0x00);
    imu.writeByte(0x1A, 0x03);
    imu.writeByte(0x38, 0x00);
    imu.writeByte(0x1B, 0x70);
    imu.writeByte(0x1C, 0x70);
    

    //pinMode(2, INPUT);
    //attachInterrupt(2, readImu, RISING);
    pinMode(13, OUTPUT);
    digitalWrite(13, LOW);
    newTime = millis();

    

}

void readImu(void){

  imu.getMotion6Counts(&ax, &ay, &az, &gx, &gy, &gz);

}

void loop()
{  
  if  ((millis()-newTime) > 5){
    newTime = millis();
    readImu();
    Serial.print(ax);
    Serial.print(" ");
    Serial.print(gx);
    Serial.print(" ");
    
    /*
    Serial.print(ay);
    Serial.print(" ");
    Serial.print(gy);
    Serial.print(" ");
    Serial.print(az);
    Serial.print(" ");
    Serial.print(gz);
    Serial.print(" ");
     */
     
    Serial.println();
    digitalWrite(13, !digitalRead(13));
  }
}





