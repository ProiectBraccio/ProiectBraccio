# Robot Sortare Litere

Un sistem robotizat pentru sortarea literelor folosind OpenCV, OCR și comunicare serială cu Arduino.

## Descriere

Acest proiect implementează un robot care poate sorta litere în funcție de un cuvânt introdus. Sistemul folosește:
- **Computer Vision** pentru detectarea literelor
- **OCR (Tesseract)** pentru recunoașterea caracterelor
- **Arduino** pentru controlul robotului
- **Tkinter** pentru interfața grafică
- **SQLite** pentru stocarea istoricului

## Cerințe Hardware

- **Raspberry Pi** sau computer cu Linux
- **Arduino** (conectat via USB)
- **Cameră** compatibilă cu `libcamera`
- **Robot** controlat de Arduino pentru manipularea cuburilor cu litere

## Cerințe Software

### Dependințe Python
```bash
pip install opencv-python pytesseract pyserial tkinter numpy
```

### Tesseract OCR
```bash
sudo apt-get install tesseract-ocr
```

### Libcamera (pentru Raspberry Pi)
```bash
sudo apt-get install libcamera-apps
```

## Structura Proiectului

```
PROIECTLITERE/
├── start_robot_system.sh          # Script principal de pornire
├── camera_detection.py      # Detectarea și recunoașterea literelor
├── interface_tkinter.py     # Interfața grafică
├── cuvant.txt              # Fișier temporar cu cuvântul de sortat
└── robot_sortare.db        # Baza de date SQLite
```

## Instalare și Configurare

### 1. Clonarea proiectului
```bash
git clone <repository-url>
cd robot-sortare-litere
```

### 2. Instalarea dependințelor
```bash
# Instalare dependințe Python
pip install -r requirements.txt

# Instalare Tesseract OCR
sudo apt-get update
sudo apt-get install tesseract-ocr

# Pentru Raspberry Pi - instalare libcamera
sudo apt-get install libcamera-apps
```

### 3. Configurarea portului serial
Verificați și ajustați portul Arduino în `camera_detection.py`:
```python
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
```

Pentru a găsi portul corect:
```bash
ls /dev/ttyACM* /dev/ttyUSB*
```

### 4. Permisiuni pentru script
```bash
chmod +x start_robot_system.sh
```

## Utilizare

### Pornirea sistemului
```bash
./start_robot_system.sh
```

### Pași de funcționare:
1. **Porniți sistemul** - Rulați scriptul principal
2. **Introduceți cuvântul** - În interfața Tkinter (2-4 litere unice)
3. **Poziționați cuburile** - Așezați cuburile cu litere în fața camerei
4. **Confirmați detectarea** - Apăsați "Y" când litera este detectată corect
5. **Robotul sortează** - Sistemul va comanda robotului să mute cubul

### Reguli pentru cuvinte:
- **Lungime**: 2-4 litere
- **Caractere**: Doar litere A-Z
- **Unicitate**: Fără litere repetate
- **Exemple valide**: MAC, CAL, MARE, LUNA

## Componente Sistem

### 1. Interface Tkinter (`interface_tkinter.py`)
- Interfață grafică pentru introducerea cuvintelor
- Gestionarea bazei de date SQLite
- Vizualizarea istoricului cuvintelor sortate

### 2. Detectarea Literelor (`camera_detection.py`)
- Captarea video prin `libcamera`
- Procesarea imaginii cu OpenCV
- Recunoașterea OCR cu Tesseract
- Comunicarea cu Arduino

### 3. Script Principal (`start_system.sh`)
- Pornirea automată a tuturor componentelor
- Gestionarea proceselor
- Oprirea sigură a sistemului

## Comunicarea cu Arduino

### Protocol de comunicare:
- **Comandă**: `L<poziție>\n` (ex: `L1\n`, `L2\n`)
- **Răspuns**: `DONE\n` când robotul a terminat mișcarea

### Exemple de comenzi:
```
L1  # Mută cubul în poziția 1
L2  # Mută cubul în poziția 2
L3  # Mută cubul în poziția 3
L4  # Mută cubul în poziția 4
```

## Configurare OCR

### Optimizarea Tesseract:
```python
ocr_config = '--psm 10 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ'
```

### Parametri importanți:
- `--psm 10`: Mod pentru caractere individuale
- `tessedit_char_whitelist`: Restricționează la A-Z

## Baza de Date

### Structura tabelei:
```sql
CREATE TABLE cuvinte_sortate (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cuvant TEXT NOT NULL UNIQUE,
    data_sortare TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Locația bazei de date:
```
~/PROIECTLITERE/robot_sortare.db
```

## Troubleshooting

### Probleme comune:

#### 1. Camera nu funcționează
```bash
# Verificați dacă libcamera este instalat
libcamera-hello

# Testați camera
libcamera-vid -t 5000 --width 640 --height 480
```

#### 2. Portul serial nu funcționează
```bash
# Verificați porturile disponibile
ls /dev/ttyACM* /dev/ttyUSB*

# Verificați permisiunile
sudo usermod -a -G dialout $USER
```

#### 3. OCR nu detectează litere
- Verificați iluminarea
- Ajustați threshold-ul în cod
- Asigurați-vă că literele sunt clare și mari

#### 4. Dependințe lipsă
```bash
# Reinstalați dependințele
pip install --force-reinstall opencv-python pytesseract pyserial
```

## Oprirea sistemului

### Oprire normală:
- Apăsați `Ctrl+C` în terminal
- Toate procesele se vor opri automat

### Oprire forțată:
```bash
pkill -f "python3 interface_tkinter.py"
pkill -f "python3 camera_detection.py"
```

