#include <Braccio.h>
#include <Servo.h>

// Servo-uri
Servo base;
Servo shoulder;
Servo elbow;
Servo wrist_ver;
Servo wrist_rot;
Servo gripper;

// Buton
#define BUTTON_PIN 30

// Poziții cutii
#define CUTIE_ROSIE 0
#define CUTIE_GALBENA 90
#define CUTIE_ALBASTRU 135

// Stare gripper
#define GRIPPER_DESCHIS 10
#define GRIPPER_INCHIS 73

// Timpi
#define DELAY_POZITIE_INITIALA 1000

void setup() {
  Serial.begin(9600);
  Braccio.begin();
  pinMode(BUTTON_PIN, INPUT_PULLUP);

  // Poziție FIXĂ la pornire sau upload
  Braccio.ServoMovement(20, 0, 45, 180, 0, 90, GRIPPER_DESCHIS);
  delay(DELAY_POZITIE_INITIALA);
  Serial.println("Robotul este în poziția fixă inițială. Aștept buton...");
}

// Revenire în poziția fixă inițială
void revenireInitiala() {
  Braccio.ServoMovement(20, 0, 90, 180, 0, 90, GRIPPER_DESCHIS);
  Braccio.ServoMovement(20, 0, 45, 180, 0, 90, GRIPPER_DESCHIS);
  
  delay(DELAY_POZITIE_INITIALA);
}

void asteaptaButon() {
  Serial.println("Apasă butonul pentru a continua...");
  while(digitalRead(BUTTON_PIN) == HIGH) { delay(10); }
  delay(300);
  while(digitalRead(BUTTON_PIN) == LOW) { delay(10); }
}

void loop() {
  // 1. Cub galben
  asteaptaButon();
  preluareCub();
  plasareCub(CUTIE_GALBENA);
  revenireInitiala();

  // 2. Cub roșu
  asteaptaButon();
  preluareCub();
  plasareCub(CUTIE_ROSIE);
  revenireInitiala();

  // 3. Cub albastru
  asteaptaButon();
  preluareCub();
  plasareCub(CUTIE_ALBASTRU);
  revenireInitiala();

  // Reset ciclu
  Serial.println("Ciclu complet! Apasă buton pentru reset...");
  while(true) {
    if(digitalRead(BUTTON_PIN) == LOW) {
      delay(300);
      while(digitalRead(BUTTON_PIN) == LOW) { delay(10); }
      break;
    }
    delay(100);
  }
}

void preluareCub() {
  // Ridicare cub
  Braccio.ServoMovement(20, 180, 90, 0, 90, 90, GRIPPER_DESCHIS);
  Braccio.ServoMovement(20, 180, 45, 0, 135, 90, GRIPPER_DESCHIS);
  Braccio.ServoMovement(20, 180, 45, 0, 135, 90, GRIPPER_INCHIS);
  delay(500);
}

void plasareCub(int pozitieBaza) {
  // Plasare cub
  Braccio.ServoMovement(20, pozitieBaza, 90, 0, 90, 90, GRIPPER_INCHIS);
  Braccio.ServoMovement(20, pozitieBaza, 75, 0, 120, 90, GRIPPER_INCHIS);
  Braccio.ServoMovement(20, pozitieBaza, 75, 0, 120, 90, GRIPPER_DESCHIS);
  delay(500);
  Braccio.ServoMovement(20, pozitieBaza, 90, 0, 90, 90, GRIPPER_DESCHIS);
}