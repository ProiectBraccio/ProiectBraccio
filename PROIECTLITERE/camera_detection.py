import cv2
import numpy as np
import pytesseract
import time
import sys
import serial
import tkinter as tk
from tkinter import simpledialog, messagebox
import subprocess
import os

# === CONFIGURARE SERIALA ===
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
ser.flush()

# === CITIRE CUVANT ===
with open("cuvant.txt", "r") as f:
    cuvant = f.read().strip().upper()
print(f"Cuvantul de sortat este: {cuvant}")

# === CONFIGURARE OCR ===
last_detected = ""
last_time = 0
ocr_config = '--psm 10 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ'

# === VARIABILE PENTRU SINCRONIZARE ===
waiting_for_reset = False
reset_start_time = 0
RESET_DELAY = 3  # 3 secunde pauza pentru reset camera

# === VARIABILE PENTRU OPRIRE AUTOMATA ===
litere_asezate = 0
total_litere = len(cuvant)

# === GUI PENTRU CONFIRMARE ===
root = tk.Tk()
root.withdraw()

def confirma_litera(litera):
    raspuns = simpledialog.askstring("Confirmare", f"Este litera '{litera}' corecta? (Y/N)")
    if raspuns:
        return raspuns.strip().upper() == "Y"
    return False

def restart_camera_feed():
    try:
        print("Restartez feed-ul camerei...")
        sys.stdin.close()
        sys.stdin = open('/dev/stdin', 'rb')
        time.sleep(1)
        print("Feed-ul camerei a fost resetat!")
        return True
    except:
        print("Nu am putut restarta feed-ul camerei.")
        return False

def opreste_program():
    print("=" * 50)
    print("PROGRAM TERMINAT!")
    print(f"Robotul a asortat cu succes cuvantul: {cuvant}")
    print(f"Toate {total_litere} litere au fost asezate!")
    print("=" * 50)
    cv2.destroyAllWindows()
    ser.close()
    root.destroy()
    print("Programul se va inchide in 3 secunde...")
    time.sleep(3)
    sys.exit(0)

def read_mjpeg_frames():
    buffer = b""
    SOI = b'\xff\xd8'
    EOI = b'\xff\xd9'
    
    while True:
        chunk = sys.stdin.buffer.read(4096)
        if not chunk:
            break
        buffer += chunk
        
        while True:
            start = buffer.find(SOI)
            end = buffer.find(EOI)
            if start != -1 and end != -1 and end > start:
                jpg = buffer[start:end+2]
                buffer = buffer[end+2:]
                frame = cv2.imdecode(np.frombuffer(jpg, np.uint8), cv2.IMREAD_COLOR)
                if frame is not None:
                    yield frame
            else:
                break

def gaseste_pozitie(litera):
    # Returneaza pozitia literei in cuvantul cu litere distincte
    if litera in cuvant:
        return cuvant.index(litera) + 1
    return None

# === LOOP PRINCIPAL ===
for frame in read_mjpeg_frames():
    current_time = time.time()
    
    if waiting_for_reset:
        if current_time - reset_start_time < RESET_DELAY:
            cv2.putText(frame, "Astept resetare camera...", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.putText(frame, f"Timp ramas: {RESET_DELAY - int(current_time - reset_start_time)}s", (10, 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.imshow("Recunoastere Litere A-Z", frame)
            cv2.waitKey(1)
            continue
        else:
            waiting_for_reset = False
            print("Camera resetata. Continuam detectarea...")
            for _ in range(5):
                try:
                    chunk = sys.stdin.buffer.read(1024)
                    if len(chunk) == 0:
                        break
                except:
                    break
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 130, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    detected_letter = ""
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if w > 60 and h > 60:
            roi = thresh[y:y+h, x:x+w]
            roi = cv2.resize(roi, (100, 100))
            text = pytesseract.image_to_string(roi, config=ocr_config).strip().upper()
            if text.isalpha() and len(text) == 1:
                detected_letter = text
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                break
    
    if detected_letter:
        cv2.putText(frame, f"Litera: {detected_letter}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        if detected_letter != last_detected or current_time - last_time > 1:
            last_detected = detected_letter
            last_time = current_time
            print(f"Detectat: {detected_letter}")
            
            if confirma_litera(detected_letter):
                if detected_letter in cuvant:
                    pozitie = gaseste_pozitie(detected_letter)
                    if pozitie:
                        comanda = f"L{pozitie}\n"
                        print(f"Trimit catre Arduino: {comanda.strip()}")
                        ser.write(comanda.encode())
                        
                        while True:
                            if ser.in_waiting > 0:
                                raspuns = ser.readline().decode().strip()
                                print(f"Raspuns de la Arduino: {raspuns}")
                                if raspuns == "DONE":
                                    litere_asezate += 1
                                    print(f"Litera {detected_letter} asezata! Progres: {litere_asezate}/{total_litere}")
                                    if litere_asezate >= total_litere:
                                        print("TOATE LITERELE AU FOST ASEZATE!")
                                        print("Astept ca robotul sa revina in pozitia initiala...")
                                        time.sleep(2)
                                        opreste_program()
                                    break
                        
                        waiting_for_reset = True
                        reset_start_time = current_time
                        print("Astept resetarea camerei pentru sincronizare...")
                        
                        print("Golesc buffer-ul camerei...")
                        buffer_cleared = False
                        clear_attempts = 0
                        
                        while not buffer_cleared and clear_attempts < 50:
                            try:
                                data = sys.stdin.buffer.read(8192)
                                if len(data) == 0:
                                    buffer_cleared = True
                                    print("Buffer golit complet!")
                                clear_attempts += 1
                                time.sleep(0.1)
                            except:
                                buffer_cleared = True
                                break
                        
                        continue
                    else:
                        print(f"Litera {detected_letter} a fost deja asezata!")
                else:
                    messagebox.showerror("Eroare", f"Litera {detected_letter} nu se afla in cuvantul {cuvant}")
                    print(f"EROARE: Litera {detected_letter} nu se afla in cuvantul {cuvant}")
            else:
                print("Detectare respinsa.")
    else:
        cv2.putText(frame, "Astept litera...", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    
    cv2.imshow("Recunoastere Litere A-Z", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()