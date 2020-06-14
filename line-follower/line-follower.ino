/*
 * Project Name: Line Follower
 * Created By: Sashwat K
 * Created On: 22:49 13 June 2020
*/

// IR Sensor pins
int left = 2;
int right = 5;

// Motor pins
int motorLeftA = 7;
int motorLeftB = 8;
int motorRightA = 11;
int motorRightB = 10;

// Ultrasonic sensor pins
int trig = 4;
int echo = 3;

// Value from Pi
int resultPiPin = 12;

// Functions to move the vehicles
void moveforward();
void moveLeft();
void moveRight();
void moveStop();

// Function to get distance from ultrasonic sensor
int distancefromUS();

void setup() {
  Serial.begin(9600);
  // Initialise IR sensors
  pinMode(left, INPUT);
  pinMode(right, INPUT);

  // Initialise Motor
  pinMode(left, INPUT);
  pinMode(right, INPUT);
  pinMode(left, INPUT);
  pinMode(right, INPUT);

  // Ultrasonic initialisation
  pinMode(trig, OUTPUT);
  pinMode(echo, INPUT);

  // Result from Pi
  pinMode(resultPiPin, INPUT);
  Serial.println("Line follower Initialised");
}

void loop() {
  int leftValue = digitalRead(left);
  int rightValue = digitalRead(right);
  int ultDis = distancefromUS();
  int resultPi = digitalRead(resultPiPin);

  Serial.print("Remarks: ");
  if (ultDis < 8) {
    Serial.println("STOP");
    moveStop();
  } else {
    if (leftValue == rightValue) {
      Serial.println("Go Straight");
      moveforward();
    } else if (leftValue < rightValue) {
      Serial.println("Turn Left");
      moveLeft();
    } else if (leftValue > rightValue){
      Serial.println("Turn Right");
      moveRight();
    }
  }

  if (resultPi == HIGH) {
    Serial.println("Stop request from Pi");
    moveStop();
    delay(2000);    
  }
  
  Serial.println("Sensor Values:-");
  Serial.print("Ultrasonic Sensor Distance: ");Serial.println(ultDis);
  Serial.println("Left \t Right");
  Serial.print(leftValue);Serial.print("\t");Serial.println(rightValue);
}

void moveforward() {
  digitalWrite(motorRightA,HIGH);
  digitalWrite(motorRightB,LOW);
  digitalWrite(motorLeftA,LOW);
  digitalWrite(motorLeftB,HIGH);
}

void moveLeft() {
  digitalWrite(motorRightA,HIGH);
  digitalWrite(motorRightB,LOW);
  digitalWrite(motorLeftA,HIGH);
  digitalWrite(motorLeftB,LOW);
}

void moveRight() {
  digitalWrite(motorRightA,LOW);
  digitalWrite(motorRightB,HIGH);
  digitalWrite(motorLeftA,LOW);
  digitalWrite(motorLeftB,HIGH);
}

void moveStop() {
  digitalWrite(motorRightA,LOW);
  digitalWrite(motorRightB,LOW);
  digitalWrite(motorLeftA,LOW );
  digitalWrite(motorLeftB,LOW);
}

int distancefromUS() {
  long duration;
  digitalWrite(trig, LOW);
  delayMicroseconds(2);
  digitalWrite(trig, HIGH);
  delayMicroseconds(10);
  digitalWrite(trig, LOW);
  duration = pulseIn(echo, HIGH);
  return duration*0.034/2;
}