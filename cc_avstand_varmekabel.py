import tkinter as tk
from tkinter import ttk

# Funksjon for å beregne CC-avstand
def beregn_cc_avstand():
    try:
        rom_areal = float(rom_areal_inn.get())
        effekt_per_m2 = float(effekt_per_m2_inn.get())
        kabel_effekt = float(kabel_effekt_inn.get())
        
        cc_avstand = (kabel_effekt / effekt_per_m2) / rom_areal
        resultat.set(f"Anbefalt CC-avstand: {cc_avstand:.2f} cm")
    except ValueError:
        resultat.set("Skriv inn gyldige verdier.")

def main():
    # GUI-oppsett for CC-avstand beregning
    root = tk.Tk()
    root.title("CC-avstand Beregning for Varmekabel")

    # Input felt for rom areal
    ttk.Label(root, text="Rom areal (m²):").grid(column=0, row=0, padx=10, pady=5)
    rom_areal_inn = tk.Entry(root)
    rom_areal_inn.grid(column=1, row=0, padx=10, pady=5)

    # Input felt for ønsket effekt per m²
    ttk.Label(root, text="Effekt per m² (W/m²):").grid(column=0, row=1, padx=10, pady=5)
    effekt_per_m2_inn = tk.Entry(root)
    effekt_per_m2_inn.grid(column=1, row=1, padx=10, pady=5)

    # Input felt for kabelens effekt
    ttk.Label(root, text="Kabel effekt (W):").grid(column=0, row=2, padx=10, pady=5)
    kabel_effekt_inn = tk.Entry(root)
    kabel_effekt_inn.grid(column=1, row=2, padx=10, pady=5)

    # Resultatfelt
    resultat = tk.StringVar()
    ttk.Label(root, textvariable=resultat).grid(column=0, row=3, columnspan=2, padx=10, pady=5)

    # Knapp for å beregne CC-avstand
    beregn_knapp = ttk.Button(root, text="Beregn", command=beregn_cc_avstand)
    beregn_knapp.grid(column=0, row=4, columnspan=2, padx=10, pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
