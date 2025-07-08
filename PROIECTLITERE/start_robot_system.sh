#!/bin/bash

echo "===== SISTEM ROBOT SORTARE LITERE ====="
echo "Pornirea componentelor..."

if [ ! -d "$HOME/PROIECTLITERE" ]; then
    echo "Creez folderul PROIECTLITERE..."
    mkdir -p "$HOME/PROIECTLITERE"
fi

cleanup() {
    echo "Oprire sistem..."
    kill $INTERFACE_PID 2>/dev/null
    exit 0
}

trap cleanup SIGINT

echo "1. Pornesc interfata Tkinter..."
python3 interface_tkinter.py &
INTERFACE_PID=$!

echo ""
echo "===== SISTEM PORNIT ====="
echo "- Interfata Tkinter: PID $INTERFACE_PID"
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
