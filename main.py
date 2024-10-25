import tkinter as tk
from tkinter import ttk
from kabeldimensjonering import start_kabeldimensjonering
from cc_avstand_varmekabel import start_cc_avstand_varmekabel

# Hovedvindu oppsett
def main_window():
    root = tk.Tk()
    root.title("Elektro Beregningsprogram")
    root.geometry("400x500")

    # Funksjon for å bytte mellom funksjoner
    def vis_kabeldimensjonering():
        clear_frame()
        start_kabeldimensjonering(frame)

    def vis_cc_avstand():
        clear_frame()
        start_cc_avstand_varmekabel(frame)

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

    # Ramme for å vise forskjellige funksjoner i hovedvinduet
    global frame
    frame = tk.Frame(root)
    frame.pack(fill="both", expand=True)

    root.mainloop()

# This line should be at the same indentation level as `main_window`
if __name__ == "__main__":
    main_window()
