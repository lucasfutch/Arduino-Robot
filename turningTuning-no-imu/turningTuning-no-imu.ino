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

int Left_Speed_Hold = 0;
int Right_Speed_Hold = 0;

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

    // initialize serial communication
    Serial.begin(57600);

    MOTOR_GO_RIGHT

}

void setSpeed(){
    analogWrite(ENB,Left_Speed_Hold);
    analogWrite(ENA,Right_Speed_Hold);
}

void loop() {
    
    if (Serial.available() > 0) {

      char inChar = Serial.read();
      
      if ((int)inChar == 1){
        // turn right
        MOTOR_GO_RIGHT
      }
      else if ((int)inChar == 2){
        // turn left
        MOTOR_GO_LEFT
      }
      
      else{
        int turnSpeed = (int)inChar;
        Left_Speed_Hold = turnSpeed;
        Right_Speed_Hold = turnSpeed;
        setSpeed();
      }

    }
    
}

