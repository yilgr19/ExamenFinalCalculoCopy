# interfaz.py

import customtkinter as ctk
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# ¡Importante! Importamos la clase del cerebro desde el otro archivo.
from calculo import MathBackend

class TripleIntegralFrame(ctk.CTkFrame):
    def __init__(self, master, math_backend):
        super().__init__(master)
        self.math_backend = math_backend
        self.grid_columnconfigure(0, weight=1)
        self.current_plot_window = None  # Para rastrear ventanas de gráficos

        self.tab_view = ctk.CTkTabview(self, width=400)
        self.tab_view.pack(padx=20, pady=10, fill="both", expand=True)
        self.tab_view.add("Rectangulares")
        self.tab_view.add("Cilíndricas")
        self.tab_view.add("Esféricas")

        self.create_rectangular_tab(self.tab_view.tab("Rectangulares"))
        self.create_cylindrical_tab(self.tab_view.tab("Cilíndricas"))
        self.create_spherical_tab(self.tab_view.tab("Esféricas"))

        self.result_label = ctk.CTkLabel(self, text="Resultado:", font=ctk.CTkFont(size=16, weight="bold"))
        self.result_label.pack(padx=20, pady=(10,0), anchor="w")
        
        self.result_text = ctk.CTkTextbox(self, height=150, activate_scrollbars=True)
        self.result_text.pack(padx=20, pady=10, fill="x", expand=True)
        self.result_text.insert("0.0", "El orden de integración es d(variable interna) d(variable media) d(variable externa).\n"
                                     "Las funciones de límite pueden usar las variables de las integrales más externas.")

    def create_input_fields(self, parent_tab, var_names, func_example):
        entries = {}
        func_frame = ctk.CTkFrame(parent_tab, fg_color="transparent")
        func_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(func_frame, text=f"Función f({', '.join(var_names)}):").pack(side="left")
        entries['func'] = ctk.CTkEntry(func_frame, placeholder_text=f"Ej: {func_example}", width=200)
        entries['func'].pack(side="left", fill="x", expand=True, padx=5)
        
        limits_frame = ctk.CTkFrame(parent_tab)
        limits_frame.pack(fill="x", padx=10, pady=10)
        
        for i, var in enumerate(var_names):
            ctk.CTkLabel(limits_frame, text=f"Límites de {var}:").grid(row=i, column=0, padx=5, pady=5, sticky="w")
            entries[f'{var}_low'] = ctk.CTkEntry(limits_frame, width=80)
            entries[f'{var}_low'].grid(row=i, column=1, padx=5, pady=5)
            ctk.CTkLabel(limits_frame, text="hasta").grid(row=i, column=2, padx=5, pady=5)
            entries[f'{var}_high'] = ctk.CTkEntry(limits_frame, width=80)
            entries[f'{var}_high'].grid(row=i, column=3, padx=5, pady=5)
        
        return entries
    
    def create_rectangular_tab(self, tab):
        self.rect_entries = self.create_input_fields(tab, ['z', 'y', 'x'], "x**2 + y*z")
        self.rect_entries['func'].insert(0, "1")
        self.rect_entries['z_low'].insert(0, "0"); self.rect_entries['z_high'].insert(0, "4-x-2*y")
        self.rect_entries['y_low'].insert(0, "0"); self.rect_entries['y_high'].insert(0, "(4-x)/2")
        self.rect_entries['x_low'].insert(0, "0"); self.rect_entries['x_high'].insert(0, "4")
        button = ctk.CTkButton(tab, text="Calcular Integral Rectangular", command=self.on_calculate)
        button.pack(pady=10)

    def create_cylindrical_tab(self, tab):
        self.cyl_entries = self.create_input_fields(tab, ['z', 'r', 'theta'], "r**2 * sin(theta)")
        self.cyl_entries['func'].insert(0, "r")
        self.cyl_entries['z_low'].insert(0, "0"); self.cyl_entries['z_high'].insert(0, "9-r**2")
        self.cyl_entries['r_low'].insert(0, "0"); self.cyl_entries['r_high'].insert(0, "3")
        self.cyl_entries['theta_low'].insert(0, "0"); self.cyl_entries['theta_high'].insert(0, "2*pi")
        button = ctk.CTkButton(tab, text="Calcular Integral Cilíndrica", command=self.on_calculate)
        button.pack(pady=10)

    def create_spherical_tab(self, tab):
        self.sph_entries = self.create_input_fields(tab, ['rho', 'phi', 'theta'], "rho**2 * cos(phi)")
        self.sph_entries['func'].insert(0, "1")
        self.sph_entries['rho_low'].insert(0, "0"); self.sph_entries['rho_high'].insert(0, "2")
        self.sph_entries['phi_low'].insert(0, "0"); self.sph_entries['phi_high'].insert(0, "pi/3")
        self.sph_entries['theta_low'].insert(0, "0"); self.sph_entries['theta_high'].insert(0, "2*pi")
        button = ctk.CTkButton(tab, text="Calcular Integral Esférica", command=self.on_calculate)
        button.pack(pady=10)

    def on_calculate(self):
        current_tab = self.tab_view.get()
        limits = None
        func_str = ""
        
        if current_tab == "Rectangulares":
            func_str = self.rect_entries['func'].get()
            limits = {'z': (self.rect_entries['z_low'].get(), self.rect_entries['z_high'].get()), 'y': (self.rect_entries['y_low'].get(), self.rect_entries['y_high'].get()), 'x': (self.rect_entries['x_low'].get(), self.rect_entries['x_high'].get())}
        elif current_tab == "Cilíndricas":
            func_str = self.cyl_entries['func'].get()
            limits = {'z': (self.cyl_entries['z_low'].get(), self.cyl_entries['z_high'].get()), 'r': (self.cyl_entries['r_low'].get(), self.cyl_entries['r_high'].get()), 'theta': (self.cyl_entries['theta_low'].get(), self.cyl_entries['theta_high'].get())}
        elif current_tab == "Esféricas":
            func_str = self.sph_entries['func'].get()
            limits = {'rho': (self.sph_entries['rho_low'].get(), self.sph_entries['rho_high'].get()), 'phi': (self.sph_entries['phi_low'].get(), self.sph_entries['phi_high'].get()), 'theta': (self.sph_entries['theta_low'].get(), self.sph_entries['theta_high'].get())}
        else: return

        result = self.math_backend.solve_triple_integral(func_str, limits, current_tab)
        
        self.result_text.delete("0.0", "end")
        if "error" in result:
            self.result_text.insert("0.0", result["error"])
        else:
            display_text = (f"Proceso:\n{result['proceso']}\n\n"
                            f"Resultado Simbólico:\n{result['resultado_simbolico']}\n\n"
                            f"Resultado Numérico:\n{result['resultado_numerico']}")
            self.result_text.insert("0.0", display_text)

            figura = None
            if limits:
                if current_tab == "Rectangulares":
                    figura = self.math_backend.plot_rectangular_domain(limits)
                elif current_tab == "Cilíndricas":
                    figura = self.math_backend.plot_cylindrical_domain(limits)
                elif current_tab == "Esféricas":
                    figura = self.math_backend.plot_spherical_domain(limits)
            
            if figura:
                self.show_plot_window(figura)

    def show_plot_window(self, fig):
        # Cerrar ventana anterior si existe
        if self.current_plot_window and self.current_plot_window.winfo_exists():
            self.current_plot_window.destroy()
        
        plot_window = ctk.CTkToplevel(self)
        plot_window.title("Gráfico del Dominio")
        plot_window.geometry("600x600")
        self.current_plot_window = plot_window
        
        # Manejar el cierre de la ventana
        def on_close():
            plt.close(fig)
            plot_window.destroy()
            self.current_plot_window = None
        
        plot_window.protocol("WM_DELETE_WINDOW", on_close)

        canvas = FigureCanvasTkAgg(fig, master=plot_window)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

class SurfaceIntegralFrame(ctk.CTkFrame):
    def __init__(self, master, math_backend):
        super().__init__(master)
        self.math_backend = math_backend
        self.label = ctk.CTkLabel(self, text="Calculadora de Integrales de Superficie (Punto 2)\n\n(En construcción)", 
                                  font=ctk.CTkFont(size=18))
        self.label.pack(pady=50, padx=20)

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Calculadora de Cálculo Multivariado")
        self.geometry("600x650")
        ctk.set_appearance_mode("dark")
        self.math_backend = MathBackend()

        self.selection_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.selection_frame.pack(pady=10, padx=20, fill="x")
        self.btn_punto1 = ctk.CTkButton(self.selection_frame, text="Punto 1: Integrales Triples", command=self.show_punto1_frame)
        self.btn_punto1.pack(side="left", expand=True, padx=5)
        self.btn_punto2 = ctk.CTkButton(self.selection_frame, text="Punto 2: Integrales de Superficie", command=self.show_punto2_frame)
        self.btn_punto2.pack(side="left", expand=True, padx=5)

        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True, padx=20, pady=10)
        self.punto1_frame = TripleIntegralFrame(self.container, self.math_backend)
        self.punto2_frame = SurfaceIntegralFrame(self.container, self.math_backend)
        self.show_punto1_frame()

    def show_frame(self, frame_to_show):
        self.punto1_frame.pack_forget()
        self.punto2_frame.pack_forget()
        frame_to_show.pack(fill="both", expand=True)

    def show_punto1_frame(self):
        self.show_frame(self.punto1_frame)

    def show_punto2_frame(self):
        self.show_frame(self.punto2_frame)