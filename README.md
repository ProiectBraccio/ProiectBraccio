# BratRobotic-Arduino

# Proiect Braț Robotic + Arduino Uno R4 WiFi + Detecție cuburi + Buton

Acesta este un proiect care controlează un **braț robotic Braccio** folosind un **Arduino Uno R4 WiFi**. Integrează un **senzor ultrasonic HC-SR04**, un **buton multifuncțional** și logica de control pentru 6 **servo-motoare**. Scopul este detecția obiectelor și manipularea automată sau la comandă prin apăsarea butonului.

## Module ale proiectului

- control-brat : cod și logică pentru controlul celor 6 servo-motoare ale brațului robotic Braccio
- senzor-ultrasonic : măsurare distanță cu senzorul HC-SR04 pentru detectarea obiectelor
- buton-multifunctional : declanșarea acțiunilor brațului prin apăsare scurtă/lungă sau dublu-click
- main.ino : scriptul principal care leagă toate modulele și controlează fluxul de operare

## Componente folosite

- Arduino UNO R4 WiFi  
- Braț Robotic Braccio (6 x Servo-motoare)  
- HC-SR04 - senzor ultrasonic pentru măsurare distanță  
- Buton digital (cu 5 moduri de interacțiune)  
- Fire jumper, breadboard (opțional)  

## Tehnologii folosite

- Arduino IDE (C/C++)
- Servo.h - control servo-motoare
- NewPing.h - măsurare distanță cu HC-SR04
- Cod personalizat pentru interpretarea stărilor butonului

## ⚙️ Etape principale din cod

### 🔧 1. Inițializarea sistemului

```cpp
void setup() {
  Serial.begin(9600);
  Braccio.begin();
  Braccio.ServoMovement(20, 0, 45, 180, 0, 90, 73); // Poziția inițială cu gripper deschis
  pinMode(BUTTON_PIN, INPUT_PULLUP);
}
```

### 📩 2. Citirea comenzii seriale

```cpp
if (Serial.available()) {
  comanda = Serial.readStringUntil('\n');
  Serial.println("Comanda primită: " + comanda);
}
```
### ⏳ 3. Așteptarea confirmării prin buton

```cpp
Serial.println("Apasa butonul pentru a executa comanda...");
while (digitalRead(BUTTON_PIN) == HIGH);  // Așteaptă apăsare
delay(200); // Debounce
```
### 📏 4. Verificarea prezenței cubului cu senzor ultrasonic

```cpp
int distanta = masoaraDistanta();  // apel funcție din senzor.ino
if (distanta < 9 || distanta > 13) {
  Serial.println("Cubul nu este în poziția corectă!");
  return;
}
```
## 🔌 Conexiuni hardware

| Componentă        | Pin Arduino                      |
|-------------------|----------------------------------|
| Trigger HC-SR04   | 8                                |
| Echo HC-SR04      | 9                                |
| Buton             | 7                                |
| Servo Motoare     | 11, 10, 9, 6, 5, 3 (implicit Braccio) |
