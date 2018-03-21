/*
 * Arduino Robot Control
 * Motor movement defined
 * Speed can be changed
 * 
 */

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
    

void setup()
{
    pinMode(ENA,OUTPUT); 
    pinMode(ENB,OUTPUT); 
    pinMode(INPUT1,OUTPUT); 
    pinMode(INPUT2,OUTPUT); 
    pinMode(INPUT3,OUTPUT); 
    pinMode(INPUT4,OUTPUT); 

    Serial.begin(57600);
}

void setSpeed(){
    analogWrite(ENB,Left_Speed_Hold);
    analogWrite(ENA,Right_Speed_Hold);
}


void loop()
  {  
    while(1)
    {

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

        delay(500);
        
      }      
      
    }  
    
  }

