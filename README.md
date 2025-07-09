# ProiectBraccio

# Robot Sortare Litere cu Braț Robotic (Arduino + OCR + Tkinter)

Un sistem robotizat integrat care **recunoaște, sortează și manipulează cuburi cu litere** folosind:
- **Computer Vision + OCR**
- **Arduino Uno R4 WiFi + Braccio**
- **Tkinter GUI**
- **Senzor ultrasonic HC-SR04 + buton multifuncțional**
- **Bază de date SQLite pentru istoric**

---

## Descriere Generală

Sistemul detectează automat litere folosind camera și Tesseract OCR, primește un cuvânt de la utilizator și comandă brațul robotic să sorteze cuburile corespunzătoare literei în poziții dedicate. Confirmarea se face prin apăsarea unui buton fizic, doar dacă senzorul detectează prezența unui cub.

---

## Componente Hardware

- Raspberry Pi / PC cu Linux
- Cameră compatibilă `libcamera`
- Arduino Uno R4 WiFi
- Braț Robotic Braccio (6 servo-motoare)
- Senzor ultrasonic HC-SR04
- Buton multifuncțional
- Fire jumper, breadboard (opțional)

---

## Tehnologii

- **Python 3**: `opencv-python`, `pytesseract`, `tkinter`, `pyserial`, `sqlite3`
- **C++ Arduino**: `Servo.h`, `Braccio.h`, `NewPing.h`
- **OCR**: Tesseract cu whitelist pentru A-Z
- **GUI**: Tkinter
- **Bază de date**: SQLite

---

## Structura Proiectului

```
PROIECTLITERE/
├── start_robot_system.sh       # Script principal de pornire
├── camera_detection.py         # Procesare imagine + OCR + comunicare serială
├── interface_tkinter.py        # Interfață grafică cu SQLite
├── cuvant.txt                  # Fișier temporar cuvânt
├── robot_sortare.db            # Bază de date SQLite
└── robotic_arm_code.ino        # Cod pentru Arduino (Braccio + senzori)
```

---

## Instalare (Software)

### 1. Activare mediu virtual
```bash
source ~/PROIECTLITERE/venv/bin/activate
```

### 2. Instalare pachete Python
```bash
pip install --upgrade pip
pip install opencv-python pytesseract pyserial numpy
```

### 3. Instalare Tesseract OCR
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr tesseract-ocr-ron
```

### 4. Instalare Libcamera (doar pe Raspberry Pi)
```bash
sudo apt-get install libcamera-apps
```

---

## Configurare Arduino

### Codul `robotic_arm_code.ino`:

- Controlează 6 servo-motoare
- Verifică prezența cubului cu HC-SR04
- Așteaptă confirmare prin apăsare de buton
- Primește comenzi seriale de forma `L1`, `L2` etc.

### Fragment cod:
```cpp
if (Serial.available()) {
  String comanda = Serial.readStringUntil('\n');
  if (masoaraDistanta() >= 9 && masoaraDistanta() <= 13) {
    while (digitalRead(BUTTON_PIN) == HIGH); // așteaptă apăsare
    // execută mișcarea conform comenzii
  } else {
    Serial.println("Cubul nu este în poziția corectă!");
  }
}
```

---

## Conexiuni Hardware Arduino

| Componentă        | Pin Arduino                      |
|-------------------|----------------------------------|
| Trigger HC-SR04   | D8                               |
| Echo HC-SR04      | D9                               |
| Buton             | D7                               |
| Servo Motoare     | 11, 10, 9, 6, 5, 3 (implicit Braccio) |

---

## Utilizare

### 1. Activare mediu virtual
```bash
source ~/PROIECTLITERE/venv/bin/activate
```

### 2. Pornire sistem
```bash
./start_robot_system.sh
```

### 3. Flux operare:
1. Introdu un cuvânt (2–4 litere unice, doar A-Z)
2. Așează cuburile în fața camerei
3. Confirmă fiecare literă detectată cu `Y`
4. Apasă butonul fizic pentru fiecare cub
5. Brațul mută cuburile în poziții corespunzătoare (`L1`, `L2`, ...)

---

## Reguli pentru cuvinte

- Doar **A-Z**, litere mari
- **2 – 4 litere**, fără caractere repetate
- Exemplu valid: `LUNA`, `MAC`, `CAL`

---

## Config OCR

```python
ocr_config = '--psm 10 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ'
```

---

## Baza de date (SQLite)

Fișier: `robot_sortare.db`

```sql
CREATE TABLE cuvinte_sortate (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  cuvant TEXT NOT NULL UNIQUE,
  data_sortare TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## Testare Cameră

```bash
libcamera-hello
libcamera-vid -t 5000 --width 640 --height 480
```

---

## Troubleshooting

### Port serial indisponibil:
```bash
ls /dev/ttyACM* /dev/ttyUSB*
sudo usermod -a -G dialout $USER
```

### OCR slab:
- Asigură-te că litera este clară, lumină bună
- Verifică `threshold` și `roi` în `camera_detection.py`

### Dependențe lipsă:
```bash
source ~/PROIECTLITERE/venv/bin/activate
pip install --force-reinstall opencv-python pytesseract pyserial numpy
```

---

## Oprire sistem

### Normal:
- `Ctrl+C` în terminal

### Forțat:
```bash
deactivate
pkill -f "python3 interface_tkinter.py"
pkill -f "python3 camera_detection.py"
```

---

## Comunicare cu Arduino

- Comenzi de forma: `L1\n`, `L2\n`, ... până `L4\n`
- Răspuns Arduino: `DONE\n` după mutarea cubului

---

## Demonstrație

[Vizualizează demo-ul video](https://drive.google.com/file/d/1nT6hrFQWlIjg--yZhD4qCPuB2gSUuGII/view?usp=drive_link)



## Sugestii de îmbunătățire

- Antrenarea unui model pentru recunoaștere litere mai robustă
- Control vocal al comenzilor robotului
- Maparea cu camera a coordonatelor X,Y,Z

## Autori

- Barbu Simina Georgiana - hardware & software
- Lazăr Alexandra-Andreea – hardware & software



