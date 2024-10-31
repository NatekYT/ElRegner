import tkinter as tk
from tkinter import messagebox

class ResistanceCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Resistans Kalkulator")

        # Input for Total Voltage
        self.voltage_label = tk.Label(root, text="Inngangsspenning (V):")
        self.voltage_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.voltage_entry = tk.Entry(root, width=30)
        self.voltage_entry.grid(row=0, column=1, padx=10, pady=5)

        # Series Section
        self.series_label = tk.Label(root, text="Serie (R1, R2, ...):")
        self.series_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.series_entry = tk.Entry(root, width=30)
        self.series_entry.grid(row=1, column=1, padx=10, pady=5)
        self.series_result = tk.Label(root, text="Resultat:")
        self.series_result.grid(row=1, column=2, padx=10, pady=5, sticky="w")
        self.series_calc_button = tk.Button(root, text="Beregn", command=self.calculate_series)
        self.series_calc_button.grid(row=1, column=3, padx=5, pady=5)

        # Parallel Section
        self.parallel_label = tk.Label(root, text="Parallell (R1, R2, ...):")
        self.parallel_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.parallel_entry = tk.Entry(root, width=30)
        self.parallel_entry.grid(row=2, column=1, padx=10, pady=5)
        self.parallel_result = tk.Label(root, text="Resultat:")
        self.parallel_result.grid(row=2, column=2, padx=10, pady=5, sticky="w")
        self.parallel_calc_button = tk.Button(root, text="Beregn", command=self.calculate_parallel)
        self.parallel_calc_button.grid(row=2, column=3, padx=5, pady=5)

        # Series-Parallel Section
        self.series_parallel_label = tk.Label(root, text="Serie-Parallell (eks: R1 (R2, R3))")
        self.series_parallel_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.series_parallel_entry = tk.Entry(root, width=30)
        self.series_parallel_entry.grid(row=3, column=1, padx=10, pady=5)
        self.series_parallel_result = tk.Label(root, text="Resultat:")
        self.series_parallel_result.grid(row=3, column=2, padx=10, pady=5, sticky="w")
        self.series_parallel_calc_button = tk.Button(root, text="Beregn", command=self.calculate_series_parallel)
        self.series_parallel_calc_button.grid(row=3, column=3, padx=5, pady=5)

        # Explanation Label for Series-Parallel
        self.explanation_label = tk.Label(root, text="Eks: R1 (R2, R3) betyr serie R1 med parallell R2 og R3", fg="gray")
        self.explanation_label.grid(row=4, column=1, padx=10, pady=5, sticky="w")

        # Copy and Clear Buttons
        self.copy_button = tk.Button(root, text="Kopier Resultat", command=self.copy_result)
        self.copy_button.grid(row=5, column=1, padx=5, pady=10, sticky="e")
        self.clear_button = tk.Button(root, text="Slett Alle", command=self.clear_all)
        self.clear_button.grid(row=5, column=2, padx=5, pady=10, sticky="w")

    def calculate_series(self):
        try:
            resistors = list(map(float, self.series_entry.get().split(',')))
            total_resistance = sum(resistors)
            total_voltage = float(self.voltage_entry.get())
            total_current = total_voltage / total_resistance

            # Beregning av spenning over hver motstand i serie
            voltages = [total_current * r for r in resistors]
            voltage_text = " | ".join(f"R{i+1}: {v:.2f} V" for i, v in enumerate(voltages))
            self.series_result.config(text=f"Resultat: {total_resistance} Ω, I = {total_current:.2f} A\nSpenning: {voltage_text}")

        except ValueError:
            messagebox.showerror("Feil", "Skriv inn gyldige motstands- og spenningsverdier separert med komma.")
    
    def calculate_parallel(self):
        try:
            resistors = list(map(float, self.parallel_entry.get().split(',')))
            total_voltage = float(self.voltage_entry.get())
            total_resistance = 1 / sum(1 / r for r in resistors)
            total_current = total_voltage / total_resistance

            # Beregning av strøm gjennom hver motstand i parallell
            currents = [total_voltage / r for r in resistors]
            current_text = " | ".join(f"R{i+1}: {c:.2f} A" for i, c in enumerate(currents))
            self.parallel_result.config(text=f"Resultat: {total_resistance:.2f} Ω, I_total = {total_current:.2f} A\nStrøm: {current_text}")

        except ValueError:
            messagebox.showerror("Feil", "Skriv inn gyldige motstands- og spenningsverdier separert med komma.")
        except ZeroDivisionError:
            messagebox.showerror("Feil", "Motstand kan ikke være null.")

    def calculate_series_parallel(self):
        try:
            input_str = self.series_parallel_entry.get()
            total_resistance, formula = self.parse_series_parallel(input_str)
            self.series_parallel_result.config(text=f"Resultat: {total_resistance:.2f} Ω ({formula})")
        except ValueError:
            messagebox.showerror("Feil", "Ugyldig format for serie-parallell.")

    def parse_series_parallel(self, input_str):
        input_str = input_str.replace("(", " ( ").replace(")", " ) ").replace(",", " ")
        tokens = input_str.split()

        stack, parallel_stack = [], []
        formula_stack, parallel_formula_stack = [], []
        is_parallel = False
        for token in tokens:
            if token == '(':
                is_parallel = True
                parallel_stack.append([])
                parallel_formula_stack.append([])
            elif token == ')':
                is_parallel = False
                last_parallel = parallel_stack.pop()
                last_formula = parallel_formula_stack.pop()
                parallel_resistance = 1 / sum(1 / float(r) for r in last_parallel)
                parallel_formula = "1 / (" + " + ".join(f"1/{r}" for r in last_formula) + ")"
                if parallel_stack:
                    parallel_stack[-1].append(parallel_resistance)
                    parallel_formula_stack[-1].append(parallel_formula)
                else:
                    stack.append(parallel_resistance)
                    formula_stack.append(parallel_formula)
            elif is_parallel:
                parallel_stack[-1].append(float(token))
                parallel_formula_stack[-1].append(token)
            else:
                stack.append(float(token))
                formula_stack.append(token)
        
        total_formula = " + ".join(formula_stack)
        return sum(stack), total_formula

    def copy_result(self):
        result_text = (f"Serie: {self.series_result.cget('text')}\n"
                       f"Parallell: {self.parallel_result.cget('text')}\n"
                       f"Serie-Parallell: {self.series_parallel_result.cget('text')}")
        self.root.clipboard_clear()
        self.root.clipboard_append(result_text)
        messagebox.showinfo("Kopiert", "Resultater kopiert til utklippstavlen.")
        
    def clear_all(self):
        self.voltage_entry.delete(0, tk.END)
        self.series_entry.delete(0, tk.END)
        self.parallel_entry.delete(0, tk.END)
        self.series_parallel_entry.delete(0, tk.END)
        self.series_result.config(text="Resultat:")
        self.parallel_result.config(text="Resultat:")
        self.series_parallel_result.config(text="Resultat:")

root = tk.Tk()
app = ResistanceCalculator(root)
root.mainloop()
