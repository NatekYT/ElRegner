import tkinter as tk
from tkinter import messagebox

def beregn_kondensator():
    try:
        # Hent verdier fra input-feltene
        C = float(entry_capacitance.get())
        V = float(entry_voltage.get())
        dV_dt = float(entry_dv_dt.get())

        # Beregning av ladning (Q) og strøm (I)
        Q = C * V
        I = C * dV_dt

        # Lag formelstrengen for ladning (Q) og strøm (I)
        formel_charge = f"Q = C * V = {C} F * {V} V = {Q:.6f} C"
        formel_current = f"I = C * (dV/dt) = {C} F * {dV_dt} V/s = {I:.6f} A"

        # Oppdater resultatetiketter med formel og utregning
        label_result_charge.config(text=f"Ladning (Q): {formel_charge}")
        label_result_current.config(text=f"Strøm (I): {formel_current}")
    except ValueError:
        messagebox.showerror("Inputfeil", "Vennligst skriv inn gyldige numeriske verdier.")

# Opprett hovedvinduet
root = tk.Tk()
root.title("Kondensatorberegning")
root.geometry("450x400")

# Kapasitans-input
label_capacitance = tk.Label(root, text="Kapasitans (C) i farad (F):")
label_capacitance.pack(pady=5)
entry_capacitance = tk.Entry(root)
entry_capacitance.pack(pady=5)

# Spenning-input
label_voltage = tk.Label(root, text="Spenning (V) i volt (V):")
label_voltage.pack(pady=5)
entry_voltage = tk.Entry(root)
entry_voltage.pack(pady=5)

# Endring i spenning over tid
label_dv_dt = tk.Label(root, text="Endring i spenning over tid (dV/dt) i V/s:")
label_dv_dt.pack(pady=5)
entry_dv_dt = tk.Entry(root)
entry_dv_dt.pack(pady=5)

# Beregn-knapp
button_calculate = tk.Button(root, text="Beregn", command=beregn_kondensator)
button_calculate.pack(pady=10)

# Resultat-etiketter
label_result_charge = tk.Label(root, text="Ladning (Q): ")
label_result_charge.pack(pady=5)

label_result_current = tk.Label(root, text="Strøm (I): ")
label_result_current.pack(pady=5)

# Start GUI-hovedløkka
root.mainloop()
