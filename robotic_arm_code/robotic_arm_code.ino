#include <Braccio.h>
#include <Servo.h>

//servo-uri
Servo base, shoulder, elbow, wrist_ver, wrist_rot, gripper;

//pini hardware
#define BUTTON_PIN 2
#define TRIG_PIN 7
#define ECHO_PIN 8

//pozitii de baza pentru plasare
#define POZITIE1 65
#define POZITIE2 85
#define POZITIE3 105
#define POZITIE4 125

#define GRIPPER_DESCHIS 10
#define GRIPPER_INCHIS 73

#define DELAY_POZITIE_INITIALA 1000

//variabile pentru comanda seriala
String comandaPrimita = "";
bool comandaDisponibila = false;

void setup() {
  Serial.begin(9600);
  Braccio.begin();

  pinMode(BUTTON_PIN, INPUT_PULLUP);
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);

  //pozitia initiala
  Braccio.ServoMovement(20, 0, 45, 180, 0, 90, GRIPPER_DESCHIS);
  delay(DELAY_POZITIE_INITIALA);
  Serial.println("Robotul este in pozitia initiala.");
}

void loop() {
  asteaptaComanda();

  if (comandaDisponibila) {
    int poz = getPozitieDinComanda();
    if (poz != -1) {
      if (verificaSiPreiaCub()) {
        plasareCub(poz);
        revenireInitiala();
        Serial.println("Comanda executata cu succes!");
        Serial.println("DONE");
        Serial.flush();  //trimite semnal complet la Python
      }
    } else {
      Serial.println("Comanda invalida: " + comandaPrimita);
    }

    //resetare comanda
    comandaPrimita = "";
    comandaDisponibila = false;
  }
}

// ====================== FUNCTII UTILE ======================

void asteaptaComanda() {
  Serial.println("Astept comanda de la Python...");
  while (true) {
    if (Serial.available() > 0) {
      comandaPrimita = Serial.readStringUntil('\n');
      comandaPrimita.trim();
      if (comandaPrimita.length() > 0) {
        comandaDisponibila = true;
        Serial.println("Comanda primita: " + comandaPrimita);
        break;
      }
    }
    delay(10);
  }

  Serial.println("Apasa butonul pentru a executa comanda...");

  //buton eliberat inainte de apasare
  while (digitalRead(BUTTON_PIN) == LOW) {
    delay(10);
  }

  //asteapta apasare valida
  while (digitalRead(BUTTON_PIN) == HIGH) {
    delay(10);
  }

  delay(100);  // debounce suplimentar
  while (digitalRead(BUTTON_PIN) == LOW) {
    delay(10);
  }

  delay(100);
}

int getPozitieDinComanda() {
  if (comandaPrimita == "L1") return POZITIE1;
  if (comandaPrimita == "L2") return POZITIE2;
  if (comandaPrimita == "L3") return POZITIE3;
  if (comandaPrimita == "L4") return POZITIE4;
  return -1;
}

void revenireInitiala() {
  Braccio.ServoMovement(20, 0, 90, 180, 0, 90, GRIPPER_DESCHIS);
  Braccio.ServoMovement(20, 0, 45, 180, 0, 90, GRIPPER_DESCHIS);
  delay(DELAY_POZITIE_INITIALA);
}

// ====================== DETECTIE CUB ======================

long masoaraDistanta() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  long durata = pulseIn(ECHO_PIN, HIGH, 30000);  //timeout 30ms
  if (durata == 0) return -1;
  return durata * 0.034 / 2;  //conversie în cm
}

bool verificaSiPreiaCub() {
  long d = masoaraDistanta();
  Serial.print("Distanta: ");
  Serial.println(d);
  if (d != -1 && d >= 9 && d <= 13) {
    preluareCub();
    return true;
  } else {
    Serial.println("Cubul nu este in zona.");
    return false;
  }
}

// ====================== MISCARI BRAT ======================

void preluareCub() {
  Braccio.ServoMovement(20, 180, 80, 0, 90, 90, GRIPPER_DESCHIS);  // coborare
  Braccio.ServoMovement(20, 180, 45, 0, 135, 90, GRIPPER_DESCHIS); // apropie
  Braccio.ServoMovement(20, 180, 45, 0, 135, 90, GRIPPER_INCHIS);  // prinde
  delay(500);
}

void plasareCub(int pozitieBaza) {
  Braccio.ServoMovement(20, pozitieBaza, 70, 60, 100, 90, GRIPPER_INCHIS); //ridica la inaltime mica
  Braccio.ServoMovement(20, pozitieBaza, 45, 0, 100, 100, GRIPPER_INCHIS); //coboara 
  Braccio.ServoMovement(20, pozitieBaza, 45, 0, 120, 110, GRIPPER_DESCHIS); //lasa cubul
  delay(500);
  Braccio.ServoMovement(20, pozitieBaza, 90, 0, 90, 110, GRIPPER_DESCHIS); //revenire
}