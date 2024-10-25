import tkinter as tk
from tkinter import ttk

# Funksjon for å beregne CC-avstand (vises inne i en ramme)
def start_cc_avstand_varmekabel(parent_frame):
    ttk.Label(parent_frame, text="CC-avstand Beregning for Varmekabel").pack(pady=10)

    # Input felt for rom areal
    rom_areal_frame = tk.Frame(parent_frame)
    rom_areal_frame.pack(pady=5)
    ttk.Label(rom_areal_frame, text="Rom areal (m²):").grid(row=0, column=0, padx=5)
    rom_areal_inn = tk.Entry(rom_areal_frame)
    rom_areal_inn.grid(row=0, column=1, padx=5)

    # Input felt for kabel lengde
    kabel_lengde_frame = tk.Frame(parent_frame)
    kabel_lengde_frame.pack(pady=5)
    ttk.Label(kabel_lengde_frame, text="Kabelens lengde (m):").grid(row=1, column=0, padx=5)
    kabel_lengde_inn = tk.Entry(kabel_lengde_frame)
    kabel_lengde_inn.grid(row=1, column=1, padx=5)

    # Resultatfelt
    resultat = tk.StringVar()
    ttk.Label(parent_frame, textvariable=resultat).pack(pady=5)

    # Funksjon for å beregne CC-avstand
    def beregn_cc_avstand():
        try:
            rom_areal = float(rom_areal_inn.get())
            kabel_lengde = float(kabel_lengde_inn.get())
            cc_avstand = (rom_areal * 100) / kabel_lengde
            resultat.set(f"Anbefalt CC-avstand: {cc_avstand:.2f} cm")
        except ValueError:
            resultat.set("Skriv inn gyldige verdier.")

    # Knapp for å beregne CC-avstand
    beregn_knapp = ttk.Button(parent_frame, text="Beregn", command=beregn_cc_avstand)
    beregn_knapp.pack(pady=10)
