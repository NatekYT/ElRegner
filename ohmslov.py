import tkinter as tk
from tkinter import messagebox

def calculate():
    try:
        u = float(entry_u.get()) if entry_u.get() else None
        i = float(entry_i.get()) if entry_i.get() else None
        r = float(entry_r.get()) if entry_r.get() else None
        p = float(entry_p.get()) if entry_p.get() else None

        result_text = ""
        
        if u is not None and i is not None:
            r = u / i
            p = u * i
            result_text = f"R = U / I = {u} / {i} = {r} ohm\n"
            result_text += f"P = U * I = {u} * {i} = {p} watt"
        elif u is not None and r is not None:
            i = u / r
            p = (u ** 2) / r
            result_text = f"I = U / R = {u} / {r} = {i} ampere\n"
            result_text += f"P = U² / R = ({u}²) / {r} = {p} watt"
        elif u is not None and p is not None:
            i = p / u
            r = (u ** 2) / p
            result_text = f"I = P / U = {p} / {u} = {i} ampere\n"
            result_text += f"R = U² / P = ({u}²) / {p} = {r} ohm"
        elif i is not None and r is not None:
            u = i * r
            p = (i ** 2) * r
            result_text = f"U = I * R = {i} * {r} = {u} volt\n"
            result_text += f"P = I² * R = ({i}²) * {r} = {p} watt"
        elif i is not None and p is not None:
            u = p / i
            r = p / (i ** 2)
            result_text = f"U = P / I = {p} / {i} = {u} volt\n"
            result_text += f"R = P / I² = {p} / ({i}²) = {r} ohm"
        elif r is not None and p is not None:
            i = (p / r) ** 0.5
            u = i * r
            result_text = f"I = √(P / R) = √({p} / {r}) = {i} ampere\n"
            result_text += f"U = I * R = {i} * {r} = {u} volt"
        else:
            messagebox.showerror("Feil", "Vennligst fyll inn to verdier.")
            return

        result_label.config(text=result_text)

    except ValueError:
        messagebox.showerror("Feil", "Ugyldig input! Vennligst fyll inn gyldige tall.")

def copy_result():
    root.clipboard_clear()
    root.clipboard_append(result_label.cget("text"))
    messagebox.showinfo("Kopiert", "Resultatet er kopiert til utklippstavlen.")

def clear_fields():
    entry_u.delete(0, tk.END)
    entry_i.delete(0, tk.END)
    entry_r.delete(0, tk.END)
    entry_p.delete(0, tk.END)
    result_label.config(text="")

root = tk.Tk()
root.title("Ohms Lov Kalkulator")

# Inputfelt
tk.Label(root, text="U (volt):").grid(row=0, column=0, sticky="e")
entry_u = tk.Entry(root)
entry_u.grid(row=0, column=1)

tk.Label(root, text="I (ampere):").grid(row=1, column=0, sticky="e")
entry_i = tk.Entry(root)
entry_i.grid(row=1, column=1)

tk.Label(root, text="R (ohm):").grid(row=2, column=0, sticky="e")
entry_r = tk.Entry(root)
entry_r.grid(row=2, column=1)

tk.Label(root, text="P (watt):").grid(row=3, column=0, sticky="e")
entry_p = tk.Entry(root)
entry_p.grid(row=3, column=1)

# Beregningsknapp
calculate_button = tk.Button(root, text="Beregn", command=calculate)
calculate_button.grid(row=4, column=0, columnspan=2)

# Resultatvisning
result_label = tk.Label(root, text="", justify="left")
result_label.grid(row=5, column=0, columnspan=2)

# Kopieringsknapp
copy_button = tk.Button(root, text="Kopier resultat", command=copy_result)
copy_button.grid(row=6, column=0, columnspan=2)

# Slett-knapp
clear_button = tk.Button(root, text="Slett alt", command=clear_fields)
clear_button.grid(row=7, column=0, columnspan=2)

root.mainloop()
