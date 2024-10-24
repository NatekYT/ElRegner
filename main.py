import tkinter as tk
from tkinter import ttk
import subprocess

def start_kabeldimensjonering():
    subprocess.run(["python", "kabeldimensjonering.py"])

def start_cc_avstand_varmekabel():
    subprocess.run(["python", "cc_avstand_varmekabel.py"])

# GUI-oppsett
root = tk.Tk()
root.title("Elektriske Beregninger")

# Legg til knapper for de forskjellige funksjonene
ttk.Label(root, text="Velg funksjon:").pack(pady=10)

ttk.Button(root, text="Kabeldimensjonering", command=start_kabeldimensjonering).pack(pady=10)
ttk.Button(root, text="CC Avstand for Varmekabel", command=start_cc_avstand_varmekabel).pack(pady=10)

# Start GUI
root.mainloop()
