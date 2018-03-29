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
bool movingLeft, movingRight, movignForward;

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

        // turn right
        if ((int)inChar == 1){
            movingRight = true;
        
            MOTOR_GO_RIGHT
        }

        // turn left
        else if ((int)inChar == 2){
            movingLeft = true;
            MOTOR_GO_LEFT
        }
  
        // move forward
        else if ((int(inChar == 3) {
  
            movingForward = true;
          
        }
  
        // start expect two bytes
        else if ((int(inChar == 4) {
  
            dataStart = true;
        }
  
        // end expect two bytes
        else if ((int(inChar == 5) {
  
            dataEnd = true;
        }

        // set the speed
        else {
          
            if (movingLeft) {
                int turnSpeed = (int)inChar;
                Left_Speed_Hold = turnSpeed;
                Right_Speed_Hold = 0;
                movingLeft = false;
                setSpeed()
            }
            else if (movingRight) {
                int turnSpeed = (int)inChar;
                Left_Speed_Hold = turnSpeed;
                Right_Speed_Hold = 0;
                movingRight = false;
                setSpeed()
            }

            // expecting two bytes to set forward speed
            else if (movingForward && dataStart) {
                int turnSpeed = (int)inChar;
                dataCount = 0;
    
                dataCount += 1;

                // first byte in
                if (dataCount == 1) {
                    Left_Speed_Hold = turnSpeed;
                }

                // second byte in
                // change dataStart to know it has received both
                else if (dataCount == 2) {
                    Right_Speed_Hold = turnSpeed;
                    dataCount = 0;
                    dataStart = false;
                    
                }
            }

            // two triggers: dataEnd received and dataStart flipped when second byte received
            else if (movingForward && dataEnd && !dataStart) {
                setSpeed();
                movingForward = false;
                dataEnd = false;
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
        
        
//        else{
//            int turnSpeed = (int)inChar;
//            Left_Speed_Hold = turnSpeed;
//            Right_Speed_Hold = turnSpeed;
//            setSpeed();
//        }
  
      }
    
}

