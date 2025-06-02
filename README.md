# ProiectBraccio

# Proiect Raspberry Pi + Braț Robotic + Detecție litere

Acesta este un proiect care combină controlul unui brat robotic cu procesare de imagine în timp real pe un Raspberry Pi. Proiectul integrează senzoristică, detecție de litere și control hardware. Are ca scop realizarea unui rebus format dintr-un cuvânt unde brațul să așeze corespunzător literele
## Module ale proiectului

- braț-robotic : cod și logică pentru controlul celor 6 servo-motoare ale bratului robotic Braccio
- raspberry-pi: integrarea camerei și comunicarea serială cu Arduino
- detecție-litere: detectarea literelor de pe cuburi din fluxuri video YUV folosind OpenCV
- senzor ultrasonic : măsurare distanță cu senzor HC-SR04 (ultrasunete)
- buton : activare ciclu de ridicare a cuburilor

## Tehnologii folosite

- Python 3
- OpenCV
- NumPy
- Raspberry Pi
- Arduino IDE- programare servomotoare robot
- Servo-motoare, senzori, butoane (ultrasonic, cameră etc.)

## Cum pornești proiectul

1. Clonează repository-ul:
   ```bash
   git clone https://github.com/lazaralexandra29/ProiectBraccio
   cd ProiectBraccio
   ```

2. Instalează dependențele:
   ```bash
   pip install numpy opencv-python
   ```

3. Alege ce parte din proiect vrei să rulezi:

### Detectare culori (cu OpenCV)
   ```bash
   python detectare_culori.py
   ```
   *Asigură-te că scriptul primește input video în format YUV (I420) prin stdin – de exemplu:*
   ```bash
   ffmpeg -i video.mp4 -f rawvideo -pix_fmt yuv420p - | python detectare_culori.py
   ```

### Control braț robotic
   ```bash
   
   ```

### Senzor ultrasonic (HC-SR04)
   ```bash
   
   ```

---

## Demo

Va urma

## Sugestii de îmbunătățire

- Control wireless (Bluetooth/WiFi) pentru braț robotic
- Detecție forme/obstacole cu YOLO sau MediaPipe
- Interfață grafică pentru control de pe PC
- Maparea cu camera a coordonatelor X,Y,Z

## Autori

- Barbu Simina Georgiana - hardware & software
- Lazăr Alexandra-Andreea – hardware & software



