import tkinter as tk
from tkinter import ttk

# Tabell fra NEK 400 for strømkapasitet (forenklet) basert på forlegningsmetode og tverrsnitt
strømkapasitet_tabell = {
    "Kobber": {
        "A1": [13.5, 18, 24, 31, 42, 52, 68, 89, 108, 136, 165, 196, 245, 286, 328],
        "A2": [13, 17.5, 23, 29, 39, 48, 63, 83, 99, 125, 150, 182, 223, 261, 298],
        "B1": [15.5, 21, 28, 36, 49, 60, 77, 99, 134, 171, 207, 239, 262, 346, 394],
        "B2": [15, 20, 27, 34, 46, 58, 75, 96, 118, 149, 179, 209, 255, 297, 339],
        "C": [17.5, 24, 32, 41, 57, 68, 89, 119, 144, 184, 223, 259, 299, 403, 464],
        "D1": [18, 24, 32, 41, 56, 64, 82, 106, 116, 192, 223, 243, 278, 320, 359],
        "D2": [19, 24, 33, 41, 57, 70, 92, 110, 130, 162, 193, 220, 246, 278, 359],
    },
    "Aluminium": {
        "A1": [14, 18.5, 24, 31, 42, 53, 70, 89, 99, 125, 150, 186, 223, 232, 305],
        "A2": [13.5, 17.5, 23, 30, 40, 50, 67, 83, 118, 161, 207, 236, 262, 297, 394],
        "B1": [16.5, 22, 28, 39, 53, 70, 89, 110, 134, 171, 207, 232, 262, 299, 464],
        "B2": [15.5, 21, 27, 34, 46, 58, 75, 96, 144, 149, 179, 192, 243, 262, 305],
        "C": [18.5, 25, 32, 39, 56, 70, 92, 110, 144, 223, 162, 179, 207, 243, 262],
        "D1": [18, 23, 30, 41, 56, 64, 80, 106, 136, 161, 196, 207, 232, 243, 346],
        "D2": [19, 24, 31, 39, 56, 69, 89, 110, 134, 148, 186, 196, 207, 262, 305],
    }
}

# Spesifikk resistans (ohm * mm² / meter)
resistans = {
    "Kobber": 0.0175,
    "Aluminium": 0.0282
}

# Funksjon for å beregne korrigeringsfaktor for nærføring
def beregn_korrigeringsfaktor(antall_kabler):
    if antall_kabler == 1:
        return 1.0
    elif 2 <= antall_kabler <= 3:
        return 0.9
    elif 4 <= antall_kabler <= 6:
        return 0.8
    elif 7 <= antall_kabler <= 9:
        return 0.7
    else:
        return 0.5

# Funksjon for å dimensjonere kabel, vern og beregne spenningsfall
def dimensjoner_kabel():
    try:
        strøm = float(strøm_inn.get())
        lengde = float(lengde_inn.get())
        start_spenning = float(spenning_inn.get())
        temperatur = int(temp_inn.get())
        antall_kabler = int(nærføring_inn.get())
        max_spenningsfall = float(spenningsfall_inn.get())
        forlegning = forlegning_metode.get()
        tverrsnitt_liste = [1.5, 2.5, 4, 6, 10, 16, 25, 35, 50, 70, 95, 120, 150, 185, 240]

        # Valg av materiale
        materiale = kabel_type.get()

        # Beregner korrigeringsfaktor for nærføring
        korr_nærføring = beregn_korrigeringsfaktor(antall_kabler)

        # Velger tabell for materialet og forlegningsmetode
        strømkapasitet = strømkapasitet_tabell[materiale][forlegning]

        # Finn riktig tverrsnitt basert på korrigert strømkapasitet
        riktig_tverrsnitt = next((tverrsnitt for tverrsnitt, kapasitet in zip(tverrsnitt_liste, strømkapasitet)
                                  if kapasitet * korr_nærføring >= strøm), None)

        if riktig_tverrsnitt is None:
            resultat.set("Ingen passende kabel funnet.")
            return

        # Bruker angitt karakteristikk for vern
        karakteristikk = karakteristikk_vern.get()

        # Merkestrøm til vernet
        merkestrøm_vernet = strøm * 1.25  # Eksempel på å sette merkestrøm til vern med faktor 1.25

        # Iterasjon for spenningsfall basert på maksimalt tillatt spenningsfall
        while True:
            ρ = resistans[materiale]
            spenningsfall = (strøm * lengde * ρ) / riktig_tverrsnitt
            spenningsfall_prosent = (spenningsfall / start_spenning) * 100
            
            # Sjekk om spenningsfallet er under eller likt maksimalt tillatt spenningsfall
            if spenningsfall_prosent <= max_spenningsfall:
                break

            # Hvis spenningsfallet er over tillatt grense, øk tverrsnittet til neste tilgjengelige verdi
            next_index = tverrsnitt_liste.index(riktig_tverrsnitt) + 1
            if next_index < len(tverrsnitt_liste):
                riktig_tverrsnitt = tverrsnitt_liste[next_index]
            else:
                resultat.set(f"Ingen passende kabel funnet som gir spenningsfall under {max_spenningsfall}%.")
                return

        resultat.set(f"Riktig kabeltverrsnitt: {riktig_tverrsnitt} mm²\n"
                     f"Merkestrøm til vern: {merkestrøm_vernet:.1f} A\n"
                     f"Karakteristikk for vern: {karakteristikk}\n"
                     f"Spenningsfall: {spenningsfall:.2f} V\n"
                     f"Spenningsfall (%): {spenningsfall_prosent:.2f}%")
    except ValueError:
        resultat.set("Skriv inn gyldige verdier.")

# GUI-oppsett
root = tk.Tk()
root.title("Kabel- og Vernedimensjonering")

# Input felt for strøm
ttk.Label(root, text="Strøm (A):").grid(column=0, row=0, padx=10, pady=5)
strøm_inn = tk.Entry(root)
strøm_inn.grid(column=1, row=0, padx=10, pady=5)

# Input felt for lengde
ttk.Label(root, text="Lengde (m):").grid(column=0, row=1, padx=10, pady=5)
lengde_inn = tk.Entry(root)
lengde_inn.grid(column=1, row=1, padx=10, pady=5)

# Input felt for startspenning
ttk.Label(root, text="Startspenning (V):").grid(column=0, row=2, padx=10, pady=5)
spenning_inn = tk.Entry(root)
spenning_inn.grid(column=1, row=2, padx=10, pady=5)

# Input felt for maksimalt spenningsfall
ttk.Label(root, text="Maksimalt Spenningsfall (%):").grid(column=0, row=3, padx=10, pady=5)
spenningsfall_inn = tk.Entry(root)
spenningsfall_inn.grid(column=1, row=3, padx=10, pady=5)

# Input felt for temperatur
ttk.Label(root, text="Omgivelsestemperatur (°C):").grid(column=0, row=4, padx=10, pady=5)
temp_inn = tk.Entry(root)
temp_inn.grid(column=1, row=4, padx=10, pady=5)

# Input felt for nærføring
ttk.Label(root, text="Antall kabler i nærføring:").grid(column=0, row=5, padx=10, pady=5)
nærføring_inn = tk.Entry(root)
nærføring_inn.grid(column=1, row=5, padx=10, pady=5)

# Valg for forlegningsmetode
ttk.Label(root, text="Forlegningsmetode:").grid(column=0, row=6, padx=10, pady=5)
forlegning_metode = ttk.Combobox(root, values=["A1", "A2", "B1", "B2", "C", "D1", "D2"])
forlegning_metode.grid(column=1, row=6, padx=10, pady=5)
forlegning_metode.current(0)

# Valg for kabelmateriale (kobber eller aluminium)
ttk.Label(root, text="Kabelmateriale:").grid(column=0, row=7, padx=10, pady=5)
kabel_type = ttk.Combobox(root, values=["Kobber", "Aluminium"])
kabel_type.grid(column=1, row=7, padx=10, pady=5)
kabel_type.current(0)

# Valg for karakteristikk til vern (B, C, D)
ttk.Label(root, text="Karakteristikk for vern:").grid(column=0, row=8, padx=10, pady=5)
karakteristikk_vern = ttk.Combobox(root, values=["B", "C", "D"])
karakteristikk_vern.grid(column=1, row=8, padx=10, pady=5)
karakteristikk_vern.current(0)

# Resultatfelt
resultat = tk.StringVar()
ttk.Label(root, textvariable=resultat).grid(column=0, row=10, columnspan=2, padx=10, pady=5)

# Knapp for å beregne
beregn_knapp = ttk.Button(root, text="Beregn", command=dimensjoner_kabel)
beregn_knapp.grid(column=0, row=9, columnspan=2, padx=10, pady=10)

root.mainloop()
