import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Funksjon for å starte resistansberegningen inne i en gitt ramme
def start_resistans(parent_frame):
    ttk.Label(parent_frame, text="Resistans Kalkulator").pack(pady=10)

    class ResistanceCalculator:
        def __init__(self, frame):
            # Bruker parent_frame i stedet for et nytt rotvindu
            self.frame = frame

            # Input for Total Voltage
            self.voltage_label = tk.Label(frame, text="Inngangsspenning (V):")
            self.voltage_label.pack(padx=10, pady=5, anchor="w")
            self.voltage_entry = tk.Entry(frame, width=30)
            self.voltage_entry.pack(padx=10, pady=5)

            # Serie Seksjon
            self.series_label = tk.Label(frame, text="Serie (R1, R2, ...):")
            self.series_label.pack(padx=10, pady=5, anchor="w")
            self.series_entry = tk.Entry(frame, width=30)
            self.series_entry.pack(padx=10, pady=5)
            self.series_result = tk.Label(frame, text="Resultat:")
            self.series_result.pack(padx=10, pady=5, anchor="w")
            self.series_calc_button = tk.Button(frame, text="Beregn", command=self.calculate_series)
            self.series_calc_button.pack(padx=5, pady=5)

            # Parallell Seksjon
            self.parallel_label = tk.Label(frame, text="Parallell (R1, R2, ...):")
            self.parallel_label.pack(padx=10, pady=5, anchor="w")
            self.parallel_entry = tk.Entry(frame, width=30)
            self.parallel_entry.pack(padx=10, pady=5)
            self.parallel_result = tk.Label(frame, text="Resultat:")
            self.parallel_result.pack(padx=10, pady=5, anchor="w")
            self.parallel_calc_button = tk.Button(frame, text="Beregn", command=self.calculate_parallel)
            self.parallel_calc_button.pack(padx=5, pady=5)

            # Serie-Parallell Seksjon
            self.series_parallel_label = tk.Label(frame, text="Serie-Parallell (eks: R1 (R2, R3))")
            self.series_parallel_label.pack(padx=10, pady=5, anchor="w")
            self.series_parallel_entry = tk.Entry(frame, width=30)
            self.series_parallel_entry.pack(padx=10, pady=5)
            self.series_parallel_result = tk.Label(frame, text="Resultat:")
            self.series_parallel_result.pack(padx=10, pady=5, anchor="w")
            self.series_parallel_calc_button = tk.Button(frame, text="Beregn", command=self.calculate_series_parallel)
            self.series_parallel_calc_button.pack(padx=5, pady=5)

            # Forklaringsetikett for Serie-Parallell
            self.explanation_label = tk.Label(frame, text="Eks: R1 (R2, R3) betyr serie R1 med parallell R2 og R3", fg="gray")
            self.explanation_label.pack(padx=10, pady=5, anchor="w")

            # Kopier og Slett-knapper
            self.copy_button = tk.Button(frame, text="Kopier Resultat", command=self.copy_result)
            self.copy_button.pack(side="left", padx=5, pady=10)
            self.clear_button = tk.Button(frame, text="Slett Alle", command=self.clear_all)
            self.clear_button.pack(side="left", padx=5, pady=10)

        # Beregning av serie-motstander
        def calculate_series(self):
            try:
                resistors = list(map(float, self.series_entry.get().split(',')))
                total_resistance = sum(resistors)
                total_voltage = float(self.voltage_entry.get())
                total_current = total_voltage / total_resistance

                # Spenning over hver motstand i serie
                voltages = [total_current * r for r in resistors]
                voltage_text = " | ".join(f"R{i+1}: {v:.2f} V" for i, v in enumerate(voltages))
                self.series_result.config(text=f"Resultat: {total_resistance} Ω, I = {total_current:.2f} A\nSpenning: {voltage_text}")

            except ValueError:
                messagebox.showerror("Feil", "Skriv inn gyldige motstands- og spenningsverdier separert med komma.")

        # Beregning av parallell-motstander
        def calculate_parallel(self):
            try:
                resistors = list(map(float, self.parallel_entry.get().split(',')))
                total_voltage = float(self.voltage_entry.get())
                total_resistance = 1 / sum(1 / r for r in resistors)
                total_current = total_voltage / total_resistance

                # Strøm gjennom hver motstand i parallell
                currents = [total_voltage / r for r in resistors]
                current_text = " | ".join(f"R{i+1}: {c:.2f} A" for i, c in enumerate(currents))
                self.parallel_result.config(text=f"Resultat: {total_resistance:.2f} Ω, I_total = {total_current:.2f} A\nStrøm: {current_text}")

            except ValueError:
                messagebox.showerror("Feil", "Skriv inn gyldige motstands- og spenningsverdier separert med komma.")
            except ZeroDivisionError:
                messagebox.showerror("Feil", "Motstand kan ikke være null.")

        # Beregning av serie-parallell motstander
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

        # Kopier resultatet til utklippstavlen
        def copy_result(self):
            result_text = (f"Serie: {self.series_result.cget('text')}\n"
                           f"Parallell: {self.parallel_result.cget('text')}\n"
                           f"Serie-Parallell: {self.series_parallel_result.cget('text')}")
            self.frame.clipboard_clear()
            self.frame.clipboard_append(result_text)
            messagebox.showinfo("Kopiert", "Resultater kopiert til utklippstavlen.")

        # Slett alle inndata og resultater
        def clear_all(self):
            self.voltage_entry.delete(0, tk.END)
            self.series_entry.delete(0, tk.END)
            self.parallel_entry.delete(0, tk.END)
            self.series_parallel_entry.delete(0, tk.END)
            self.series_result.config(text="Resultat:")
            self.parallel_result.config(text="Resultat:")
            self.series_parallel_result.config(text="Resultat:")

    # Initialiser applikasjonen direkte med parent_frame
    app = ResistanceCalculator(parent_frame)
