#include <Servo.h>

#define CAMERA_SERVO_PORT 7
#define JOINT_PORT 8
#define EFFECTOR_PORT 9
#define LEFT_WHEEL_PORT 10
#define RIGHT_WHEEL_PORT 11
#define SERIAL_BAUD_RATE 9600

Servo effector;
Servo joint;

Servo leftWheel;
Servo rightWheel;

int incomingByte = 0;
int leftSpeed = 70;                   // VELOCIDADE PADRAO DA RODA ESQUERDA - 70
int rightSpeed = 107;                 // VELOCIDADE PADRAO DA RODA DIREITA - 107
int turnRightSpeed = rightSpeed - 4;  // VELOCIDADE DA RODA DIREITA EM CURVAS PARA A DIREITA - 103
int turnLeftSpeed = leftSpeed + 5;    // VELOCIDADE DA RODA ESQUERDA EM CURVAS PARA A ESQUERDA - 75
int pos;


void setup() {
  Serial.begin(SERIAL_BAUD_RATE);

  attachMotors();
  effector.attach(EFFECTOR_PORT);
  joint.attach(JOINT_PORT);

  jointInitialConfiguration();
  delay(1000);
}

void loop() {  

  if (Serial.available() > 0) {
    incomingByte = Serial.read();
    Serial.print("Byte received from Raspberry: ");
    Serial.println(incomingByte);
  }

  switch(incomingByte) {
  case 82: //RIGHT
    turnRight();
    break;

  case 76: //LEFT
    turnLeft();
    break;

  case 70: //FRONT
    goFront();
    break;

  case 66: //BACK
    goBack();
    break;

  case 67: //CATCH
    catchBall();
    break;

  case 83: //SOLTA - DROP
    dropBall();
    break;
  }

}

void jointInitialConfiguration() {
  joint.write(40);
  effector.write(170);
  delay(5);
}

void attachMotors() {
  rightWheel.attach(RIGHT_WHEEL_PORT);
  leftWheel.attach(LEFT_WHEEL_PORT);
}

void stopMotors() {
  rightWheel.detach();
  leftWheel.detach();
}

void goFront() {
  attachMotors();
  rightWheel.write(rightSpeed);
  leftWheel.write(leftSpeed);
  delay(5);
}

void goBack() {
  attachMotors();
  rightWheel.write(leftSpeed);
  leftWheel.write(rightSpeed);
  delay(5);
}

void turnRight() {
  attachMotors();
  rightWheel.write(turnRightSpeed);
  leftWheel.write(leftSpeed);
  delay(5);
}

void turnLeft() {
  attachMotors();
  rightWheel.write(rightSpeed);
  leftWheel.write(turnLeftSpeed);
  delay(5);
}

void catchBall() {
  openEffector();
  jointDown();
  closeEffector();
  jointUp();
  delay(100);
  incomingByte = 1;
}

void dropBall() {
  goFront();
  delay(150);
  stopMotors();
  for(pos = 60; pos < 90; pos += 1) {
    joint.write(pos);
    delay(10);
  }
  openEffector();
  incomingByte = 1;
}

void openEffector() {
  for (pos = 170; pos > 20; pos -= 1) {
    effector.write(pos);
    delay(10);
  }
}

void closeEffector() {
  for (pos = 20; pos < 176; pos += 1) {
    effector.write(pos);
    delay(10);
  }
  delay(100);
}

void jointUp() {
  for (pos = 137 ; pos > 70; pos -= 1) {
    joint.write(pos);
    delay(10);
  }
}

void jointDown() {
  for (pos = 60; pos < 130; pos += 1) {
    joint.write(pos);
    delay(10);
  }
}

