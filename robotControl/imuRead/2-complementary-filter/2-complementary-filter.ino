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
#define dt 0.005
#define ACCELEROMETER_SENSITIVITY 16,384 
#define GYROSCOPE_SENSITIVITY 131

unsigned long newTime;

MPU6050 imu;
int16_t ax, ay, az, gx, gy, gz;
float pitch = 0;
float roll = 0;
float accPitch = 0;
float accRoll = 0;
float gyrPitch = 0;
float gyrRoll = 0;

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

void ComplementaryFilter(short accData[3], short gyrData[3], float * roll, float * accRoll, float * gyrRoll)
{
    
    // http://www.pieter-jan.com/node/11
    
    
        
   
    // Integrate the gyroscope data -> int(angularSpeed) = angle
    *roll -= ((float)gyrData[1] / GYROSCOPE_SENSITIVITY) * dt;    // Angle around the Y-axis
    *gyrRoll -= ((float)gyrData[1] / GYROSCOPE_SENSITIVITY) * dt;    // Angle around the Y-axis
    
    // Compensate for drift with accelerometer data if !bullshit
    // Sensitivity = -2 to 2 G at 16Bit -> 2G = 32768 && 0.5G = 8192
    int forceMagnitudeApprox = abs(accData[0]) + abs(accData[1]) + abs(accData[2]);
    if (forceMagnitudeApprox > 8192 && forceMagnitudeApprox < 32768)
    {
        // Turning around the Y axis results in a vector on the X-axis
        *accRoll = atan2f((float)accData[0], (float)accData[2]) * 180 / M_PI;
        *roll = *roll * 0.70 + *accRoll * 0.30;

    }
    
} 

void loop()
{  
  if  ((millis()-newTime) > 5){
    newTime = millis();
    
    readImu();
    short accData[3] = {ax, ay, az};
    short gyrData[3] = {gx, gy, gz};
    ComplementaryFilter(accData, gyrData, &roll, &accRoll, &gyrRoll);
    Serial.print(roll);
    Serial.print(" ");
    Serial.print(accRoll);
    //Serial.print(" ");
    //Serial.print(gyrRoll);
    Serial.println();
    
    digitalWrite(13, !digitalRead(13));
  }
}





