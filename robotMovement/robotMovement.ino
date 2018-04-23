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

bool dataStart, dataEnd;
int dataCount = 0;
bool movingLeft, movingRight, movingForward;

#define MOTOR_GO_FORWARD  { digitalWrite(INPUT1,LOW);digitalWrite(INPUT2,HIGH);digitalWrite(INPUT3,LOW);digitalWrite(INPUT4,HIGH);}
#define MOTOR_GO_BACK    {   digitalWrite(INPUT1,HIGH);digitalWrite(INPUT2,LOW);digitalWrite(INPUT3,HIGH);digitalWrite(INPUT4,LOW);}
#define MOTOR_GO_RIGHT    {digitalWrite(INPUT1,HIGH);digitalWrite(INPUT2,LOW);digitalWrite(INPUT3,LOW);digitalWrite(INPUT4,HIGH);}
#define MOTOR_GO_LEFT   {digitalWrite(INPUT1,LOW);digitalWrite(INPUT2,HIGH);digitalWrite(INPUT3,HIGH);digitalWrite(INPUT4,LOW);}
#define MOTOR_GO_STOP   {digitalWrite(INPUT1,LOW);digitalWrite(INPUT2,LOW);digitalWrite(INPUT3,LOW);digitalWrite(INPUT4,LOW);}


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


        if ((int)inChar == 0) {
            MOTOR_GO_STOP
        }
        // turn right
        else if ((int)inChar == 1){
            movingRight = true;
        
        }

        // turn left
        else if ((int)inChar == 2){
            movingLeft = true;
        }
  
        // move forward
        else if ((int)inChar == 3) {
  
            movingForward = true;
          
        }
  
        // start expect two bytes
        else if ((int)inChar == 4) {
            dataCount = 0;
            dataStart = true;
        }
  
        // end expect two bytes
        else if (((int)inChar == 5) && (dataCount == 2)) {
          setSpeed();
          MOTOR_GO_BACK
          movingForward = false;
          
        }

        // set the speed
        else {
          
            if (movingLeft ) {
                int turnSpeed = (int)inChar;
                Left_Speed_Hold = turnSpeed;
                Right_Speed_Hold = turnSpeed;
                movingLeft = false;
                setSpeed();
                MOTOR_GO_LEFT
            }
            else if (movingRight) {
                int turnSpeed = (int)inChar;
                Left_Speed_Hold = turnSpeed;
                Right_Speed_Hold = turnSpeed;
                movingRight = false;
                setSpeed();
                MOTOR_GO_RIGHT
            }

            // expecting two bytes to set forward speed
            else if (movingForward && dataStart) {
                int turnSpeed = (int)inChar;
                dataCount += 1;

                // first byte in
                if (dataCount == 1) {
                    Left_Speed_Hold = turnSpeed;
                }

                // second byte in
                // change dataStart to know it has received both
                else if (dataCount == 2) {
                    Right_Speed_Hold = turnSpeed;
                    dataStart = false;
                    
                }
            }

            // somethign went wrong -> reset everything and wait for new command
            else {
                dataStart = false;
                dataEnd = false;
                movingForward = false;
                movingLeft = false;
                movingRight = false;
            }
        }
      }   
}

