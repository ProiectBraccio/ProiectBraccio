import tkinter as tk
from tkinter import messagebox, Toplevel, Scrollbar
import threading
import subprocess
import os
import sqlite3

# Folder si cale fixa pentru baza de date si fisierul cuvant.txt
BASE_FOLDER = os.path.expanduser('~/PROIECTLITERE')
DB_PATH = os.path.join(BASE_FOLDER, 'robot_sortare.db')
CUVANT_FILE = os.path.join(BASE_FOLDER, 'cuvant.txt')

# Creeaza folderul daca nu exista
os.makedirs(BASE_FOLDER, exist_ok=True)

# Initializare baza de date cu tabela pentru cuvinte
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS cuvinte_sortate (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cuvant TEXT NOT NULL UNIQUE,
            data_sortare TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Porneste scriptul care acceseaza camera si proceseaza imaginea
def porneste_camera():
    subprocess.run("libcamera-vid -t 0 --width 640 --height 480 --framerate 10 --codec mjpeg -o - | python3 camera_detection.py", shell=True)

# Trimite cuvantul introdus catre robot
def trimite_cuvant():
    cuvant = entry.get().strip().upper()
    
    # Validari: lungime, doar litere, fara repetitii
    if not (2 <= len(cuvant) <= 4):
        messagebox.showwarning("Eroare", "Cuvantul trebuie sa aiba intre 2 si 4 litere!")
        return
    if not cuvant.isalpha():
        messagebox.showwarning("Eroare", "Doar litere sunt permise!")
        return
    if len(set(cuvant)) != len(cuvant):
        messagebox.showwarning("Eroare", "Literele nu pot fi repetate!")
        return

    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('INSERT INTO cuvinte_sortate (cuvant) VALUES (?)', (cuvant,))
        conn.commit()
        conn.close()

        # Scrie cuvantul intr-un fisier care va fi citit de scriptul de procesare video
        with open(CUVANT_FILE, 'w') as f:
            f.write(cuvant)

        messagebox.showinfo("Succes", f"Robotul va sorta: {cuvant}")
        entry.delete(0, tk.END)

        # Porneste camera intr-un thread separat pentru a nu bloca interfata
        threading.Thread(target=porneste_camera, daemon=True).start()

    except sqlite3.IntegrityError:
        messagebox.showwarning("Eroare", "Cuvantul a fost deja sortat!")

# Afiseaza lista cuvintelor sortate intr-o fereastra noua
def afiseaza_lista():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT id, cuvant, data_sortare FROM cuvinte_sortate ORDER BY data_sortare DESC')
    rezultate = c.fetchall()
    conn.close()

    fereastra = Toplevel(root)
    fereastra.title("Cuvinte sortate")
    fereastra.geometry("600x400")

    scrollbar = Scrollbar(fereastra)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    lista = tk.Listbox(fereastra, width=50, height=15, yscrollcommand=scrollbar.set, selectmode=tk.SINGLE)
    lista.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    scrollbar.config(command=lista.yview)

    id_list = []
    for id_, cuv, data in rezultate:
        lista.insert(tk.END, f"{cuv} - {data}")
        id_list.append(id_)

    # Sterge cuvantul selectat din lista si din baza de date
    def sterge_selectat():
        try:
            selection = lista.curselection()
            if not selection:
                messagebox.showwarning("Atentie", "Selecteaza un cuvant din lista!")
                return
            index = selection[0]
            id_sters = id_list[index]
            cuvant_sters = rezultate[index][1]

            confirmare = messagebox.askyesno(
                "Confirma stergerea",
                f"Esti sigur ca vrei sa stergi cuvantul '{cuvant_sters}'?"
            )
            if confirmare:
                conn = sqlite3.connect(DB_PATH)
                c = conn.cursor()
                c.execute('DELETE FROM cuvinte_sortate WHERE id = ?', (id_sters,))
                conn.commit()
                conn.close()

                lista.delete(index)
                id_list.pop(index)
                messagebox.showinfo("Succes", "Cuvant sters cu succes!")
        except Exception as e:
            messagebox.showerror("Eroare", f"A aparut o eroare: {str(e)}")

    frame_butoane = tk.Frame(fereastra)
    frame_butoane.pack(pady=10)

    btn_sterge = tk.Button(
        frame_butoane,
        text="Sterge cuvantul selectat",
        command=sterge_selectat,
        bg="orange",
        fg="white"
    )
    btn_sterge.pack(side=tk.LEFT, padx=5)

# Sterge toate cuvintele din baza si fisierul cuvant.txt
def sterge_toate_cuvintele():
    if messagebox.askyesno("Confirma", "Stergi TOATE cuvintele din baza de date?"):
        try:
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute('DELETE FROM cuvinte_sortate')
            conn.commit()
            conn.close()

            if os.path.exists(CUVANT_FILE):
                os.remove(CUVANT_FILE)

            entry.delete(0, tk.END)
            messagebox.showinfo("Succes", "Toate cuvintele au fost sterse!")
        except Exception as e:
            messagebox.showerror("Eroare", f"Eroare la stergere: {str(e)}")

# Interfata grafica principala
root = tk.Tk()
root.title("Robot Sortare Litere - Versiunea Combinata")
root.geometry("500x550")
root.resizable(True, True)

title_label = tk.Label(root, text="ROBOT SORTARE LITERE", 
                      font=("Arial", 16, "bold"), fg="blue")
title_label.pack(pady=15)

instruction_label = tk.Label(root, text="Introdu un cuvant (2-4 litere unice)", 
                            font=("Arial", 12))
instruction_label.pack(pady=5)

entry = tk.Entry(root, font=("Arial", 16), justify="center", width=20)
entry.pack(pady=15)

frame_principal = tk.Frame(root)
frame_principal.pack(pady=10)

btn_trimite = tk.Button(frame_principal, text="Trimite la Robot", 
                       font=("Arial", 12), bg="green", fg="white", 
                       command=trimite_cuvant, width=25, height=2)
btn_trimite.pack(pady=8)

btn_vezi = tk.Button(frame_principal, text="Vezi Cuvinte Sortate", 
                    font=("Arial", 12), bg="blue", fg="white", 
                    command=afiseaza_lista, width=25, height=2)
btn_vezi.pack(pady=8)

separator = tk.Frame(root, height=2, bg="gray")
separator.pack(fill=tk.X, padx=20, pady=15)

frame_stergere = tk.Frame(root)
frame_stergere.pack(pady=10)

btn_sterge_tot = tk.Button(frame_stergere, text="Sterge Tot", 
                          font=("Arial", 12, "bold"), bg="red", fg="white", 
                          command=sterge_toate_cuvintele, width=25, height=2)
btn_sterge_tot.pack(pady=8)

info_frame = tk.Frame(root)
info_frame.pack(pady=15)

info_label = tk.Label(info_frame, text="Tip: Literele trebuie sa fie unice (A-Z)", 
                     font=("Arial", 10), fg="gray")
info_label.pack()

usage_label = tk.Label(info_frame, text="Exemple valide: mac, lac, mare, cal", 
                      font=("Arial", 9), fg="darkgreen")
usage_label.pack(pady=5)

# Configurari pentru scalare
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Focus automat pe input si trimitere cu Enter
entry.focus()
entry.bind('<Return>', lambda event: trimite_cuvant())

# Porneste aplicatia
root.mainloop()
