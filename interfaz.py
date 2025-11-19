# interfaz.py

import customtkinter as ctk
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# ¡Importante! Importamos la clase del cerebro desde el otro archivo.
from calculo import MathBackend

class TripleIntegralFrame(ctk.CTkFrame):
    def __init__(self, master, math_backend):
        super().__init__(master, fg_color="#FFFFFF")
        self.math_backend = math_backend
        self.grid_columnconfigure(0, weight=1)
        self.current_plot_window = None  # Para rastrear ventanas de gráficos
        self.current_mode = "Rectangulares"  # Modo actual

        # Contenedor principal con layout de dos columnas optimizado
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(padx=15, pady=(10, 10), fill="both", expand=True)
        
        # Columna izquierda: Selector mejorado con mejor distribución
        left_column = ctk.CTkFrame(main_container, fg_color="transparent", width=200)
        left_column.pack(side="left", fill="y", padx=(0, 10))
        left_column.pack_propagate(False)
        
        # Selector de tipo de coordenadas - diseño mejorado
        selector_frame = ctk.CTkFrame(left_column, fg_color="#E8F5E9", corner_radius=10)
        selector_frame.pack(fill="both", expand=True)
        
        title_label = ctk.CTkLabel(
            selector_frame, text="Sistema de Coordenadas",
            text_color="#2C3E50",
            font=ctk.CTkFont(size=13, weight="bold")
        )
        title_label.pack(pady=(12, 10))
        
        # Botones en layout más espaciado y elegante
        buttons_container = ctk.CTkFrame(selector_frame, fg_color="transparent")
        buttons_container.pack(pady=(0, 12), padx=10, fill="x")
        
        self.btn_rect = ctk.CTkButton(
            buttons_container, text="Rectangulares",
            command=lambda: self.switch_mode("Rectangulares"),
            fg_color="#A8E6CF",
            hover_color="#95D9C4",
            text_color="#2C3E50",
            font=ctk.CTkFont(size=11, weight="bold"),
            corner_radius=8,
            height=36,
            width=180
        )
        self.btn_rect.pack(pady=4, fill="x")
        
        self.btn_cyl = ctk.CTkButton(
            buttons_container, text="Cilíndricas",
            command=lambda: self.switch_mode("Cilíndricas"),
            fg_color="#FFFFFF",
            hover_color="#F5F5F5",
            text_color="#2C3E50",
            font=ctk.CTkFont(size=11, weight="bold"),
            corner_radius=8,
            height=36,
            width=180,
            border_width=1,
            border_color="#A8E6CF"
        )
        self.btn_cyl.pack(pady=4, fill="x")
        
        self.btn_sph = ctk.CTkButton(
            buttons_container, text="Esféricas",
            command=lambda: self.switch_mode("Esféricas"),
            fg_color="#FFFFFF",
            hover_color="#F5F5F5",
            text_color="#2C3E50",
            font=ctk.CTkFont(size=11, weight="bold"),
            corner_radius=8,
            height=36,
            width=180,
            border_width=1,
            border_color="#A8E6CF"
        )
        self.btn_sph.pack(pady=4, fill="x")
        
        # Columna derecha: Contenido (límites y botón) - más espacio
        right_column = ctk.CTkFrame(main_container, fg_color="transparent")
        right_column.pack(side="right", fill="both", expand=True, padx=(8, 0))
        
        # Contenedor para los frames de cada modo - ocupa todo el espacio
        self.content_frame = ctk.CTkFrame(right_column, fg_color="#F8F9FA", corner_radius=8)
        self.content_frame.pack(fill="both", expand=True)
        
        # Crear los frames para cada tipo de coordenada
        self.rect_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.cyl_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.sph_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        
        self.create_rectangular_tab(self.rect_frame)
        self.create_cylindrical_tab(self.cyl_frame)
        self.create_spherical_tab(self.sph_frame)
        
        # Mostrar el frame inicial
        self.switch_mode("Rectangulares")

        # Sección de resultados - optimizada para más espacio
        result_container = ctk.CTkFrame(self, fg_color="#E8F5E9", corner_radius=8)
        result_container.pack(padx=15, pady=(8, 12), fill="both", expand=True)
        
        result_header_frame = ctk.CTkFrame(result_container, fg_color="transparent")
        result_header_frame.pack(padx=12, pady=(10, 6), fill="x")
        
        self.result_label = ctk.CTkLabel(
            result_header_frame, text="📊 Resultado del Cálculo", 
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color="#2C3E50"
        )
        self.result_label.pack(side="left")
        
        self.result_text = ctk.CTkTextbox(
            result_container, activate_scrollbars=True,
            fg_color="#FFFFFF",
            text_color="#2C3E50",
            border_color="#A8E6CF",
            border_width=1,
            corner_radius=6,
            font=ctk.CTkFont(size=11)
        )
        self.result_text.pack(padx=12, pady=(0, 10), fill="both", expand=True)
        self.result_text.insert("0.0", "💡 Nota: El orden de integración es d(variable interna) d(variable media) d(variable externa).\n"
                                     "Las funciones de límite pueden usar las variables de las integrales más externas.")

    def create_input_fields(self, parent_frame, var_names, func_example):
        entries = {}
        
        # Función - más compacta
        func_container = ctk.CTkFrame(
            parent_frame, fg_color="#E8F5E9", corner_radius=8)
        func_container.pack(fill="x", padx=10, pady=(10, 10))
        
        func_label = ctk.CTkLabel(
            func_container, text=f"Función f({', '.join(var_names)}):",
            text_color="#2C3E50",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        func_label.pack(padx=10, pady=(8, 5), anchor="w")
        
        func_entry_frame = ctk.CTkFrame(func_container, fg_color="transparent")
        func_entry_frame.pack(fill="x", padx=10, pady=(0, 8))
        
        entries['func'] = ctk.CTkEntry(
            func_entry_frame, placeholder_text=f"Ej: {func_example}",
            fg_color="#FFFFFF",
            border_color="#A8E6CF",
            border_width=1,
            text_color="#2C3E50",
            font=ctk.CTkFont(size=11),
            corner_radius=6,
            height=32
        )
        entries['func'].pack(fill="x", expand=True)
        
        # Límites - layout optimizado en grid para mejor uso del espacio
        limits_container = ctk.CTkFrame(
            parent_frame, fg_color="#F8F9FA", corner_radius=8)
        limits_container.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        limits_title = ctk.CTkLabel(
            limits_container, text="Límites de Integración",
            text_color="#2C3E50",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        limits_title.pack(padx=10, pady=(8, 8), anchor="w")
        
        limits_frame = ctk.CTkFrame(limits_container, fg_color="transparent")
        limits_frame.pack(fill="both", expand=True, padx=10, pady=(0, 8))
        
        # Layout optimizado: grid para aprovechar mejor el espacio
        for i, var in enumerate(var_names):
            var_label = ctk.CTkLabel(
                limits_frame, text=f"{var}:",
                text_color="#2C3E50",
                font=ctk.CTkFont(size=11, weight="bold"),
                width=50,
                anchor="w"
            )
            var_label.grid(row=i, column=0, padx=(0, 8), pady=4, sticky="w")
            
            entries[f'{var}_low'] = ctk.CTkEntry(
                limits_frame,
                fg_color="#FFFFFF",
                border_color="#A8E6CF",
                border_width=1,
                text_color="#2C3E50",
                font=ctk.CTkFont(size=11),
                corner_radius=6,
                height=28
            )
            entries[f'{var}_low'].grid(row=i, column=1, padx=4, pady=4, sticky="ew")
            
            arrow_label = ctk.CTkLabel(
                limits_frame, text="→",
                text_color="#5A6C7D",
                font=ctk.CTkFont(size=12, weight="bold"),
                width=25
            )
            arrow_label.grid(row=i, column=2, padx=4, pady=4)
            
            entries[f'{var}_high'] = ctk.CTkEntry(
                limits_frame,
                fg_color="#FFFFFF",
                border_color="#A8E6CF",
                border_width=1,
                text_color="#2C3E50",
                font=ctk.CTkFont(size=11),
                corner_radius=6,
                height=28
            )
            entries[f'{var}_high'].grid(row=i, column=3, padx=4, pady=4, sticky="ew")
        
        # Configurar columnas para que se expandan
        limits_frame.grid_columnconfigure(1, weight=1)
        limits_frame.grid_columnconfigure(3, weight=1)
        
        return entries
    
    def create_rectangular_tab(self, frame):
        self.rect_entries = self.create_input_fields(frame, ['z', 'y', 'x'], "x**2 + y*z")
        self.rect_entries['func'].insert(0, "1")
        self.rect_entries['z_low'].insert(0, "0"); self.rect_entries['z_high'].insert(0, "4-x-2*y")
        self.rect_entries['y_low'].insert(0, "0"); self.rect_entries['y_high'].insert(0, "(4-x)/2")
        self.rect_entries['x_low'].insert(0, "0"); self.rect_entries['x_high'].insert(0, "4")
        # Botón más compacto
        button = ctk.CTkButton(
            frame, text="Calcular Integral Rectangular", 
            command=self.on_calculate,
            fg_color="#A8E6CF",
            hover_color="#95D9C4",
            text_color="#2C3E50",
            font=ctk.CTkFont(size=12, weight="bold"),
            corner_radius=8,
            height=36
        )
        button.pack(pady=(8, 10), padx=10, fill="x")

    def create_cylindrical_tab(self, frame):
        self.cyl_entries = self.create_input_fields(frame, ['z', 'r', 'theta'], "r**2 * sin(theta)")
        self.cyl_entries['func'].insert(0, "r")
        self.cyl_entries['z_low'].insert(0, "0"); self.cyl_entries['z_high'].insert(0, "9-r**2")
        self.cyl_entries['r_low'].insert(0, "0"); self.cyl_entries['r_high'].insert(0, "3")
        self.cyl_entries['theta_low'].insert(0, "0"); self.cyl_entries['theta_high'].insert(0, "2*pi")
        button = ctk.CTkButton(
            frame, text="Calcular Integral Cilíndrica", 
            command=self.on_calculate,
            fg_color="#A8E6CF",
            hover_color="#95D9C4",
            text_color="#2C3E50",
            font=ctk.CTkFont(size=12, weight="bold"),
            corner_radius=8,
            height=36
        )
        button.pack(pady=(8, 10), padx=10, fill="x")

    def create_spherical_tab(self, frame):
        self.sph_entries = self.create_input_fields(frame, ['rho', 'phi', 'theta'], "rho**2 * cos(phi)")
        self.sph_entries['func'].insert(0, "1")
        self.sph_entries['rho_low'].insert(0, "0"); self.sph_entries['rho_high'].insert(0, "2")
        self.sph_entries['phi_low'].insert(0, "0"); self.sph_entries['phi_high'].insert(0, "pi/3")
        self.sph_entries['theta_low'].insert(0, "0"); self.sph_entries['theta_high'].insert(0, "2*pi")
        button = ctk.CTkButton(
            frame, text="Calcular Integral Esférica", 
            command=self.on_calculate,
            fg_color="#A8E6CF",
            hover_color="#95D9C4",
            text_color="#2C3E50",
            font=ctk.CTkFont(size=12, weight="bold"),
            corner_radius=8,
            height=36
        )
        button.pack(pady=(8, 10), padx=10, fill="x")

    def switch_mode(self, mode):
        """Cambia entre los diferentes modos de coordenadas"""
        self.current_mode = mode
        
        # Ocultar todos los frames
        self.rect_frame.pack_forget()
        self.cyl_frame.pack_forget()
        self.sph_frame.pack_forget()
        
        # Actualizar estilos de botones
        buttons = {
            "Rectangulares": self.btn_rect,
            "Cilíndricas": self.btn_cyl,
            "Esféricas": self.btn_sph
        }
        
        for name, btn in buttons.items():
            if name == mode:
                btn.configure(
                    fg_color="#A8E6CF",
                    hover_color="#95D9C4",
                    border_width=0
                )
            else:
                btn.configure(
                    fg_color="#FFFFFF",
                    hover_color="#F5F5F5",
                    border_width=1,
                    border_color="#A8E6CF"
                )
        
        # Mostrar el frame correspondiente - sin padding extra
        if mode == "Rectangulares":
            self.rect_frame.pack(fill="both", expand=True, padx=8, pady=8)
        elif mode == "Cilíndricas":
            self.cyl_frame.pack(fill="both", expand=True, padx=8, pady=8)
        elif mode == "Esféricas":
            self.sph_frame.pack(fill="both", expand=True, padx=8, pady=8)

    def on_calculate(self):
        current_tab = self.current_mode
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
            display_text = (f"📐 Proceso:\n{result['proceso']}\n\n"
                            f"🔢 Resultado Simbólico:\n{result['resultado_simbolico']}\n\n"
                            f"📊 Resultado Numérico:\n{result['resultado_numerico']}")
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
        plot_window.configure(fg_color="#F8F9FA")
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
        super().__init__(master, fg_color="#FFFFFF")
        self.math_backend = math_backend
        self.label = ctk.CTkLabel(
            self, text="Calculadora de Integrales de Superficie (Punto 2)\n\n(En construcción)", 
            font=ctk.CTkFont(size=18),
            text_color="#2C3E50"
        )
        self.label.pack(pady=50, padx=20)

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Calculadora de Cálculo Multivariado")
        self.geometry("800x700")
        ctk.set_appearance_mode("light")
        self.configure(fg_color="#F8F9FA")
        self.math_backend = MathBackend()

        # Header superior mejorado con diseño moderno
        header_container = ctk.CTkFrame(self, fg_color="transparent")
        header_container.pack(padx=20, pady=(12, 10), fill="x")
        
        # Título principal
        title_frame = ctk.CTkFrame(header_container, fg_color="transparent")
        title_frame.pack(side="left", fill="y", padx=(0, 15))
        
        main_title = ctk.CTkLabel(
            title_frame, text="Calculadora de Cálculo Multivariado",
            text_color="#2C3E50",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        main_title.pack(anchor="w")
        
        subtitle = ctk.CTkLabel(
            title_frame, text="Integrales Triples y de Superficie",
            text_color="#5A6C7D",
            font=ctk.CTkFont(size=11)
        )
        subtitle.pack(anchor="w", pady=(2, 0))
        
        # Botones de navegación mejorados
        nav_frame = ctk.CTkFrame(header_container, fg_color="#E8F5E9", corner_radius=10)
        nav_frame.pack(side="right", fill="y")
        
        self.btn_punto1 = ctk.CTkButton(
            nav_frame, text="Integrales Triples", 
            command=self.show_punto1_frame,
            fg_color="#A8E6CF",
            hover_color="#95D9C4",
            text_color="#2C3E50",
            font=ctk.CTkFont(size=12, weight="bold"),
            corner_radius=8,
            height=38,
            width=160
        )
        self.btn_punto1.pack(side="left", padx=8, pady=6)
        
        self.btn_punto2 = ctk.CTkButton(
            nav_frame, text="Integrales de Superficie", 
            command=self.show_punto2_frame,
            fg_color="#FFFFFF",
            hover_color="#F5F5F5",
            text_color="#2C3E50",
            font=ctk.CTkFont(size=12, weight="bold"),
            corner_radius=8,
            border_width=1,
            border_color="#A8E6CF",
            height=38,
            width=180
        )
        self.btn_punto2.pack(side="left", padx=(0, 8), pady=6)

        self.container = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=12)
        self.container.pack(fill="both", expand=True, padx=20, pady=(0, 12))
        self.punto1_frame = TripleIntegralFrame(self.container, self.math_backend)
        self.punto2_frame = SurfaceIntegralFrame(self.container, self.math_backend)
        self.show_punto1_frame()

    def show_frame(self, frame_to_show):
        self.punto1_frame.pack_forget()
        self.punto2_frame.pack_forget()
        frame_to_show.pack(fill="both", expand=True)
        
        # Actualizar estilos de botones de navegación
        if frame_to_show == self.punto1_frame:
            self.btn_punto1.configure(
                fg_color="#A8E6CF",
                hover_color="#95D9C4",
                border_width=0
            )
            self.btn_punto2.configure(
                fg_color="#FFFFFF",
                hover_color="#F5F5F5",
                border_width=1,
                border_color="#A8E6CF"
            )
        else:
            self.btn_punto1.configure(
                fg_color="#FFFFFF",
                hover_color="#F5F5F5",
                border_width=1,
                border_color="#A8E6CF"
            )
            self.btn_punto2.configure(
                fg_color="#A8E6CF",
                hover_color="#95D9C4",
                border_width=0
            )

    def show_punto1_frame(self):
        self.show_frame(self.punto1_frame)

    def show_punto2_frame(self):
        self.show_frame(self.punto2_frame)