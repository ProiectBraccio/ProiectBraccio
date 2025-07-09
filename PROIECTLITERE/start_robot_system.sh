#!/bin/bash

echo "===== SISTEM ROBOT SORTARE LITERE ====="
echo "Verificarea si activarea mediului virtual..."

# Creeaza folderul PROIECTLITERE daca nu exista
if [ ! -d "$HOME/PROIECTLITERE" ]; then
    echo "Creez folderul PROIECTLITERE..."
    mkdir -p "$HOME/PROIECTLITERE"
fi

# Verifica daca mediul virtual exista
if [ ! -d "$HOME/PROIECTLITERE/venv" ]; then
    echo "Mediul virtual nu exista. Il creez..."
    python3 -m venv "$HOME/PROIECTLITERE/venv"
    
    if [ $? -eq 0 ]; then
        echo "Mediu virtual creat cu succes in $HOME/PROIECTLITERE/venv"
    else
        echo "EROARE: Nu am putut crea mediul virtual!"
        exit 1
    fi
fi

# Activeaza mediul virtual
echo "Activez mediul virtual..."
source "$HOME/PROIECTLITERE/venv/bin/activate"

if [ $? -eq 0 ]; then
    echo "Mediu virtual activat cu succes!"
    echo "Python utilizat: $(which python3)"
else
    echo "EROARE: Nu am putut activa mediul virtual!"
    exit 1
fi

# Verifica si instaleaza dependintele daca este necesar
echo "Verific dependintele Python..."
python3 -c "import cv2, pytesseract, serial, tkinter, numpy" 2>/dev/null

if [ $? -ne 0 ]; then
    echo "Instalez dependintele lipsa..."
    pip install --upgrade pip
    pip install opencv-python pytesseract pyserial numpy
    
    if [ $? -eq 0 ]; then
        echo "Dependinte instalate cu succes!"
    else
        echo "EROARE: Nu am putut instala dependintele!"
        echo "Va rugam sa rulati manual: pip install opencv-python pytesseract pyserial numpy"
        exit 1
    fi
else
    echo "Toate dependintele sunt instalate!"
fi

cleanup() {
    echo "Oprire sistem..."
    kill $INTERFACE_PID 2>/dev/null
    deactivate 2>/dev/null  # Dezactiveaza mediul virtual
    exit 0
}

trap cleanup SIGINT

echo "Pornirea componentelor..."
echo "1. Pornesc interfata Tkinter..."
python3 interface_tkinter.py &
INTERFACE_PID=$!

echo ""
echo "===== SISTEM PORNIT ====="
echo "- Interfata Tkinter: PID $INTERFACE_PID"
echo "- Mediu virtual: ACTIV"
echo "- Locatie venv: $HOME/PROIECTLITERE/venv"
echo ""
echo "INSTRUCTIUNI:"
echo "1. Introdu cuvantul in interfata Tkinter (ex: MAC)"
echo "2. Aseaza cuburile in fata camerei"
echo "3. Apasa butonul pe Arduino cand vezi litera detectata"
echo "4. Robotul va muta cubul"
echo ""
echo "Pentru oprire: Ctrl+C"
echo ""

wait $INTERFACE_PID

echo "Sistem oprit."
deactivate 2>/dev/null  # Dezactiveaza mediul virtual la iesire
