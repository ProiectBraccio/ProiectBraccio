#define TRIG_PIN 32
#define ECHO_PIN 34

void setup() {
  Serial.begin(9600);
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
}

void loop() {
  long durata, distanta;

  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);

  // Trimit un impuls de 10 microsecunde pe TRIG
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  // Măsurare durată ecou
  durata = pulseIn(ECHO_PIN, HIGH, 30000); // timeout 30ms

  // Conversie în centimetri
  distanta = durata * 0.034 / 2;

  if (durata == 0) {
    Serial.println("Nicio măsurătoare validă!");
  } else {
    Serial.print("Distanta: ");
    Serial.print(distanta);
    Serial.println(" cm");
  }

  delay(2000); // Măsoară la fiecare 2 secunde
}
