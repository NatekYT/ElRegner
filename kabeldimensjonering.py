import tkinter as tk
from tkinter import ttk

# Funksjon for kabeldimensjonering (vises inne i en ramme)
def start_kabeldimensjonering(parent_frame):
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
            fasevalg = fase_valg.get()  # Hent valg for 2 eller 3 faser


            # Valg av materiale
            materiale = kabel_type.get()

            # Beregner korrigeringsfaktor for nærføring
            korr_nærføring = beregn_korrigeringsfaktor(antall_kabler)

            # Velger tabell for materialet og forlegningsmetode
            strømkapasitet = strømkapasitet_tabell[materiale][forlegning]

            # Temperaturkorreksjonstabell
            temperatur_korreksjon = {
                "PVC": [1.22, 1.17, 1.12, 1.06, 1.00, 0.94, 0.87, 0.79, 0.71, 0.61, 0.50],
                "PEX/EPR": [1.15, 1.12, 1.08, 1.04, 1.00, 0.96, 0.91, 0.87, 0.82, 0.76, 0.71, 0.65, 0.58, 0.50, 0.41]
            }

            # Velg temperaturkorreksjonstabell etter isolasjonstype
            isolasjonstype = "PVC" if materiale == "Kobber" else "PEX/EPR"
            temperatur_korreksjon_verdi = temperatur_korreksjon[isolasjonstype][temperatur // 7]

           
                

            # Finn riktig tverrsnitt basert på korrigert strømkapasitet
            riktig_tverrsnitt = next((tverrsnitt for tverrsnitt, kapasitet in zip(tverrsnitt_liste, strømkapasitet)
                                     if kapasitet * korr_nærføring * temperatur_korreksjon_verdi >= strøm), None)

            if riktig_tverrsnitt is None:
                hoved_resultat.configure(state="normal")
                hoved_resultat.delete(1.0, tk.END)
                hoved_resultat.insert(tk.END, "Ingen passende kabel funnet.")
                hoved_resultat.configure(state="disabled")
                return

            # Merkestrøm til vernet
            merkestrøm_vernet = strøm * 1.25  # Eksempel på å sette merkestrøm til vern med faktor 1.25

            # Beregner RL og spenningsfall
            ρ = resistans[materiale]
            fasefaktor = 2 if fasevalg == "2" else 3**0.5
            RL = (ρ * lengde * fasefaktor) / riktig_tverrsnitt
            spenningsfall = RL * strøm
            spenningsfall_prosent = (spenningsfall / start_spenning) * 100
            u_stikk = start_spenning - spenningsfall

            # Kort resultat
            hoved_resultat.configure(state="normal")
            hoved_resultat.delete(1.0, tk.END)
            
            # Skjekk at isolasjonen tåler temperatur
            if (isolasjonstype == "PVC" and temperatur > 70 ) or (isolasjonstype == "PEX/EPR" and temperatur > 80):
                hoved_resultat.insert(tk.END,
                                      "For høy temperatur. Velg lavere temperatur"
                                      ) 
            else:
                hoved_resultat.insert(tk.END,
                                   f"Kabeltverrsnitt: {riktig_tverrsnitt}mm²\n"
                                   f"Vernstørrelse: {merkestrøm_vernet:.1f}A\n"
                                   f"Spenningsfall: {spenningsfall:.1f}V ({spenningsfall_prosent:.1f}%)\n"
                                  f"Isolasjonstype: {isolasjonstype}"
                                   )
                hoved_resultat.configure(state="disabled")

            # Detaljert utregning for "Mer info"
            detaljert_resultat.configure(state="normal")
            detaljert_resultat.delete(1.0, tk.END)
            detaljert_resultat.insert(tk.END,
                                     f"Krav 1: IB < IN < IZ\n"
                                     f"IB = {strøm}A\n"
                                     f"IN = {merkestrøm_vernet:.1f}A\n"
                                     f"\nForlegningsmetode {forlegning}\n"
                                     f"Iz min = IN / (KT * KN) => {merkestrøm_vernet:.1f}A / ({temperatur_korreksjon_verdi} * {korr_nærføring}) = {merkestrøm_vernet / (temperatur_korreksjon_verdi * korr_nærføring):.1f}A\n"
                                     f"\nIz korr = Iz avlest * KN * KT => {strømkapasitet[tverrsnitt_liste.index(riktig_tverrsnitt)]}A * {temperatur_korreksjon_verdi} * {korr_nærføring} = {strømkapasitet[tverrsnitt_liste.index(riktig_tverrsnitt)] * 0.75 * korr_nærføring:.1f}A\n"
                                     f"\nVern = {merkestrøm_vernet:.1f}A, kabel = {riktig_tverrsnitt}mm²\n"
                                     f"Krav 2: Spenningsfall ΔU% <= maxspenningsfall:\n"
                                     f"ρ * lengde * √3 / A => {ρ}Ω * {lengde}m * √3 / {riktig_tverrsnitt}mm² = {spenningsfall:.1f}V\n"
                                     f"ΔU% = {spenningsfall_prosent:.1f}% \n"
                                     f"Spenningsfall til stikk: {u_stikk:.1f}V"
                                     )
            detaljert_resultat.configure(state="disabled")

        except ValueError:
            hoved_resultat.configure(state="normal")
            hoved_resultat.delete(1.0, tk.END)
            hoved_resultat.insert(tk.END, "Vennligst fyll inn alle feltene riktig.")
            hoved_resultat.configure(state="disabled")
    # Funksjon for å vise detaljert resultat når "Mer info" trykkes
    def vis_detaljert_info():
        detaljert_resultat.grid(row=13, column=0, columnspan=2, pady=10)
        detaljert_resultat.configure(state="disabled")

    # Kopier-funksjon for detaljert resultat
    def kopier_detaljert_info():
        parent_frame.clipboard_clear()
        parent_frame.clipboard_append(detaljert_resultat.get("1.0", tk.END))

    # Inndata for dimensjoneringskriterier
    ttk.Label(parent_frame, text="Strøm (A):").grid(row=1, column=0, sticky="w")
    strøm_inn = ttk.Entry(parent_frame)
    strøm_inn.grid(row=1, column=1, padx=10)

    ttk.Label(parent_frame, text="Lengde (m):").grid(row=2, column=0, sticky="w")
    lengde_inn = ttk.Entry(parent_frame)
    lengde_inn.grid(row=2, column=1, padx=10)

    ttk.Label(parent_frame, text="Spenning (V):").grid(row=3, column=0, sticky="w")
    spenning_inn = ttk.Entry(parent_frame)
    spenning_inn.grid(row=3, column=1, padx=10)

    ttk.Label(parent_frame, text="Temperatur (°C):").grid(row=4, column=0, sticky="w")
    temp_inn = ttk.Entry(parent_frame)
    temp_inn.grid(row=4, column=1, padx=10)

    ttk.Label(parent_frame, text="Antall kabler for nærføring:").grid(row=5, column=0, sticky="w")
    nærføring_inn = ttk.Entry(parent_frame)
    nærføring_inn.grid(row=5, column=1, padx=10)

    ttk.Label(parent_frame, text="Max spenningsfall (%):").grid(row=6, column=0, sticky="w")
    spenningsfall_inn = ttk.Entry(parent_frame)
    spenningsfall_inn.grid(row=6, column=1, padx=10)

    # Materiale og forlegning metode valg
    ttk.Label(parent_frame, text="Kabeltype:").grid(row=7, column=0, sticky="w")
    kabel_type = ttk.Combobox(parent_frame, values=["Kobber", "Aluminium"])
    kabel_type.grid(row=7, column=1, padx=10)
    kabel_type.current(0)

    ttk.Label(parent_frame, text="Forlegningsmetode:").grid(row=8, column=0, sticky="w")
    forlegning_metode = ttk.Combobox(parent_frame, values=["A1", "A2", "B1", "B2", "C", "D1", "D2"])
    forlegning_metode.grid(row=8, column=1, padx=10)
    forlegning_metode.current(0)

    # Fasevalg: 2 eller 3-fase
    ttk.Label(parent_frame, text="Velg fase (2/3-tråds kabel):").grid(row=9, column=0, sticky="w")
    fase_valg = ttk.Combobox(parent_frame, values=["2", "3"])
    fase_valg.grid(row=9, column=1, padx=10)
    fase_valg.current(0)

    # Resultatvisning i en read-only tekst widget
    hoved_resultat = tk.Text(parent_frame, wrap="word", height=5, width=50)
    hoved_resultat.grid(row=11, column=0, columnspan=2, pady=10)
    hoved_resultat.configure(state="disabled")

    # Detaljert resultatvisning (for "Mer info") i en større read-only tekst widget
    detaljert_resultat = tk.Text(parent_frame, wrap="word", height=15, width=70)  # Justert størrelse

    # Knapp for å vise detaljert info
    mer_info_knapp = ttk.Button(parent_frame, text="Mer info", command=vis_detaljert_info)
    mer_info_knapp.grid(row=12, column=0, pady=5)

    # Knapp for å kopiere detaljert info
    kopier_knapp = ttk.Button(parent_frame, text="Kopier", command=kopier_detaljert_info)
    kopier_knapp.grid(row=12, column=1, pady=5)

    # Beregn-knapp
    beregn_knapp = ttk.Button(parent_frame, text="Beregn", command=dimensjoner_kabel)
    beregn_knapp.grid(row=10, column=0, columnspan=2, pady=10)
