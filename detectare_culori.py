import numpy as np
import cv2
import sys

width = 640
height = 480

# Definim intervalele HSV pentru cele 3 culori
colors = [
    {"name": "Rosu", "lower": [0, 120, 70], "upper": [10, 255, 255]},
    {"name": "Galben", "lower": [20, 100, 100], "upper": [30, 255, 255]},
    {"name": "Albastru", "lower": [100, 150, 50], "upper": [140, 255, 255]}
]

while True:
    # Citim frame-ul YUV de la stdin
    yuv = sys.stdin.buffer.read(width * height * 3 // 2)
    if not yuv or len(yuv) != width * height * 3 // 2:
        continue
    
    yuv = np.frombuffer(yuv, dtype=np.uint8).reshape((height * 3 // 2, width))
    frame = cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR_I420)
    
    # Convertim la HSV pentru detectarea culorilor
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Procesare culoare
    for color in colors:
        # Masca pentru intervalul de culoare
        mask = cv2.inRange(hsv, np.array(color["lower"]), np.array(color["upper"]))
        
        # Eliminare zgomot
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        
        # Gasire contururi
        contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Daca am gasit contururi
        if contours:
            # Cel mai mare contur
            c = max(contours, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            
            if radius > 10:
                cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
                cv2.putText(frame, color["name"], (int(x), int(y)), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    # Afisare rezultat
    cv2.imshow("Detectie culori", frame)
    
    # Iesire cu 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()