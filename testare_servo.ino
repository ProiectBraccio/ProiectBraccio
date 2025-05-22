//testare motoare brat

#include <Braccio.h>
#include <Servo.h>


Servo base;
Servo shoulder;
Servo elbow;
Servo wrist_rot;
Servo wrist_ver;
Servo gripper;


void setup() {  
  //Initialization functions and set up the initial position for Braccio
  //All the servo motors will be positioned in the "safety" position:
  //Base (M1):90 degrees
  //Shoulder (M2): 45 degrees
  //Elbow (M3): 180 degrees
  //Wrist vertical (M4): 180 degrees
  //Wrist rotation (M5): 90 degrees
  //gripper (M6): 10 degrees
  Braccio.begin();
}

void loop() {

  //M1
  Braccio.ServoMovement(20, 0, 90, 90, 90, 90, 35);
  Braccio.ServoMovement(20, 180, 90, 90, 90, 90, 35);
  Braccio.ServoMovement(20, 90, 90, 90, 90, 90, 35);
  delay(2000);
  //M2
  Braccio.ServoMovement(20, 90, 0, 90, 90, 90, 35);
  Braccio.ServoMovement(20, 90, 180, 90, 90, 90, 35);
  Braccio.ServoMovement(20, 90, 90, 90, 90, 90, 35);
  delay(2000);
  //M3
  Braccio.ServoMovement(20, 90, 90, 0, 90, 90, 35);
  Braccio.ServoMovement(20, 90, 90, 180, 90, 90, 35);
  Braccio.ServoMovement(20, 90, 90, 90, 90, 90, 35);
  delay(2000);
  //M4
  Braccio.ServoMovement(20, 90, 90, 90, 0, 90, 35);
  Braccio.ServoMovement(20, 90, 90, 90, 180, 90, 35);
  Braccio.ServoMovement(20, 90, 90, 90, 180, 90, 35);
  delay(2000);
  //M5
  Braccio.ServoMovement(20, 90, 90, 90, 90, 0, 35);
  Braccio.ServoMovement(20, 90, 90, 90, 90, 180, 35);
  Braccio.ServoMovement(20, 90, 90, 90, 90, 90, 35);
  delay(2000);
  //M6

  Braccio.ServoMovement(20, 90, 90, 90, 90, 90, 10);
  Braccio.ServoMovement(20, 90, 90, 90, 90, 90, 73);

  // Oprire permanentă
  while (true);
}
