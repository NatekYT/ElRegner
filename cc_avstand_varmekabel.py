import tkinter as tk
from tkinter import ttk

# Funksjon for å beregne CC-avstand basert på den nye formelen
def beregn_cc_avstand():
    try:
        rom_areal = float(rom_areal_inn.get())
        kabel_lengde = float(kabel_lengde_inn.get())
        
        # Beregning av CC-avstand
        cc_avstand = (rom_areal * 100) / kabel_lengde
        resultat.set(f"Anbefalt CC-avstand: {cc_avstand:.2f} cm")
    except ValueError:
        resultat.set("Skriv inn gyldige verdier.")

def main():
    # GUI-oppsett for CC-avstand beregning
    root = tk.Tk()
    root.title("CC-avstand Beregning for Varmekabel")

    # Input felt for rom areal
    ttk.Label(root, text="Rom areal (m²):").grid(column=0, row=0, padx=10, pady=5)
    global rom_areal_inn
    rom_areal_inn = tk.Entry(root)
    rom_areal_inn.grid(column=1, row=0, padx=10, pady=5)

    # Input felt for kabel lengde
    ttk.Label(root, text="Kabelens lengde (m):").grid(column=0, row=1, padx=10, pady=5)
    global kabel_lengde_inn
    kabel_lengde_inn = tk.Entry(root)
    kabel_lengde_inn.grid(column=1, row=1, padx=10, pady=5)

    # Resultatfelt
    global resultat
    resultat = tk.StringVar()
    ttk.Label(root, textvariable=resultat).grid(column=0, row=2, columnspan=2, padx=10, pady=5)

    # Knapp for å beregne CC-avstand
    beregn_knapp = ttk.Button(root, text="Beregn", command=beregn_cc_avstand)
    beregn_knapp.grid(column=0, row=3, columnspan=2, padx=10, pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
