import tkinter as tk
from tkinter import ttk
from kabeldimensjonering import start_kabeldimensjonering
from cc_avstand_varmekabel import start_cc_avstand_varmekabel
from resistans import start_resistans
from ohmslov import start_ohmslov
import socket
import requests
import sys


PC_name = socket.gethostname()
print(PC_name)

license_keys = requests.get("https://raw.githubusercontent.com/NatekYT/ElRegner/refs/heads/main/LC").text
print(license_keys)

if PC_name in license_keys:
    print("True")
else:
    print("False")
    
    # Oppretter hovedvinduet
    root = tk.Tk()
    root.title("Elregner lisens ikke aktivert")
    root.geometry("400x200")  # Setter størrelse på vinduet

    # Legger til en etikett med teksten "Test"
    label = tk.Label(root, text=f"Lisens ikke aktivert. Send melding til natsed13@outlook.com eller kontakt Natan for å kjøpe lisens.                                                 Oppgi denne koden til Natan for å aktivere lisens. Kode: {PC_name}", wraplength=350)
    label.pack(pady=20)

    # Definerer funksjonen som avslutter programmet
    def avslutt():
        root.destroy()

    # Legger til en knapp med teksten "OK" som kaller avslutt-funksjonen
    ok_button = tk.Button(root, text="OK", command=avslutt)
    ok_button.pack()

    # Starter hovedløkken til Tkinter
    root.mainloop()
    sys.exit()      # Stopper programmet helt



# Hovedvindu oppsett
def main_window():
    root = tk.Tk()
    root.title("Elektro Beregningsprogram")
    root.geometry("600x800")

    # Funksjon for å bytte mellom funksjoner
    def vis_kabeldimensjonering():
        clear_frame()
        start_kabeldimensjonering(frame)

    def vis_cc_avstand():
        clear_frame()
        start_cc_avstand_varmekabel(frame)
    
    def vis_resistans():
        clear_frame()
        start_resistans(frame)

    def vis_ohmslov():
        clear_frame()
        start_ohmslov(frame)

    # Slett nåværende innhold i rammen
    def clear_frame():
        for widget in frame.winfo_children():
            widget.destroy()

    # Lage en meny
    menubar = tk.Menu(root)
    root.config(menu=menubar)

    # Legg til "Funksjoner" i menyen
    funksjoner_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Funksjoner", menu=funksjoner_menu)

    # Menyvalg for "Kabeldimensjonering" og "CC-avstand"
    funksjoner_menu.add_command(label="Kabeldimensjonering", command=vis_kabeldimensjonering)
    funksjoner_menu.add_command(label="CC-avstand for varmekabel", command=vis_cc_avstand)
    funksjoner_menu.add_command(label="Beregning av motstander", command=vis_resistans)
    funksjoner_menu.add_command(label="Ohms Lov", command=vis_ohmslov)

    # Ramme for å vise forskjellige funksjoner i hovedvinduet
    global frame
    frame = tk.Frame(root)
    frame.pack(fill="both", expand=True)

    root.mainloop()

# This line should be at the same indentation level as `main_window`
if __name__ == "__main__":
    main_window()
