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
        self.grid_rowconfigure(0, weight=1)   # Sección superior compacta
        self.grid_rowconfigure(1, weight=4)   # Dar mucho más peso a la sección de resultados
        self.current_plot_window = None  # Para rastrear ventanas de gráficos (ya no se usa)
        self.current_mode = "Rectangulares"  # Modo actual
        self.current_plot_canvas = None  # Canvas de matplotlib integrado

        # Contenedor principal con layout de dos columnas optimizado - más compacto
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.grid(row=0, column=0, sticky="nsew", padx=15, pady=(6, 4))
        
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
        title_label.pack(pady=(8, 6))
        
        # Botones en layout más compacto
        buttons_container = ctk.CTkFrame(selector_frame, fg_color="transparent")
        buttons_container.pack(pady=(0, 8), padx=10, fill="x")
        
        self.btn_rect = ctk.CTkButton(
            buttons_container, text="Rectangulares",
            command=lambda: self.switch_mode("Rectangulares"),
            fg_color="#A8E6CF",
            hover_color="#95D9C4",
            text_color="#2C3E50",
            font=ctk.CTkFont(size=11, weight="bold"),
            corner_radius=8,
            height=32,
            width=180
        )
        self.btn_rect.pack(pady=2, fill="x")
        
        self.btn_cyl = ctk.CTkButton(
            buttons_container, text="Cilíndricas",
            command=lambda: self.switch_mode("Cilíndricas"),
            fg_color="#FFFFFF",
            hover_color="#F5F5F5",
            text_color="#2C3E50",
            font=ctk.CTkFont(size=11, weight="bold"),
            corner_radius=8,
            height=32,
            width=180,
            border_width=1,
            border_color="#A8E6CF"
        )
        self.btn_cyl.pack(pady=2, fill="x")
        
        self.btn_sph = ctk.CTkButton(
            buttons_container, text="Esféricas",
            command=lambda: self.switch_mode("Esféricas"),
            fg_color="#FFFFFF",
            hover_color="#F5F5F5",
            text_color="#2C3E50",
            font=ctk.CTkFont(size=11, weight="bold"),
            corner_radius=8,
            height=32,
            width=180,
            border_width=1,
            border_color="#A8E6CF"
        )
        self.btn_sph.pack(pady=2, fill="x")
        
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

        # Sección de resultados - usando pestañas para mejor organización
        # Dar más prioridad a esta sección con menos padding superior
        result_container = ctk.CTkFrame(self, fg_color="#E8F5E9", corner_radius=8)
        result_container.grid(row=1, column=0, sticky="nsew", padx=15, pady=(2, 12))
        
        result_header_frame = ctk.CTkFrame(result_container, fg_color="transparent")
        result_header_frame.pack(padx=12, pady=(8, 4), fill="x")
        
        self.result_label = ctk.CTkLabel(
            result_header_frame, text="📊 Resultado del Cálculo", 
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color="#2C3E50"
        )
        self.result_label.pack(side="left")
        
        # Usar pestañas para separar resultados y gráfica
        self.result_tabview = ctk.CTkTabview(
            result_container,
            fg_color="#FFFFFF",
            corner_radius=8,
            segmented_button_fg_color="#E8F5E9",
            segmented_button_selected_color="#A8E6CF",
            segmented_button_unselected_color="#FFFFFF",
            segmented_button_selected_hover_color="#95D9C4",
            segmented_button_unselected_hover_color="#F0F0F0"
        )
        self.result_tabview.pack(padx=12, pady=(0, 8), fill="both", expand=True)
        
        # Pestaña de resultados textuales
        self.text_tab = self.result_tabview.add("📝 Resultados")
        self.text_tab.grid_columnconfigure(0, weight=1)
        self.text_tab.grid_rowconfigure(0, weight=1)
        
        self.result_text = ctk.CTkTextbox(
            self.text_tab, activate_scrollbars=True,
            fg_color="#FFFFFF",
            text_color="#2C3E50",
            border_color="#A8E6CF",
            border_width=1,
            corner_radius=6,
            font=ctk.CTkFont(size=11)
        )
        self.result_text.grid(row=0, column=0, sticky="nsew", padx=8, pady=8)

        
        # Pestaña de gráfica
        self.plot_tab = self.result_tabview.add("📈 Gráfico")
        self.plot_tab.grid_columnconfigure(0, weight=1)
        self.plot_tab.grid_rowconfigure(0, weight=1)
        
        # Frame para la gráfica
        plot_frame = ctk.CTkFrame(self.plot_tab, fg_color="#FFFFFF", corner_radius=6)
        plot_frame.grid(row=0, column=0, sticky="nsew", padx=8, pady=8)
        plot_frame.grid_columnconfigure(0, weight=1)
        plot_frame.grid_rowconfigure(1, weight=1)
        
        plot_label = ctk.CTkLabel(
            plot_frame, text="📈 Gráfico del Dominio",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#2C3E50"
        )
        plot_label.grid(row=0, column=0, pady=(8, 4))
        
        # Canvas para matplotlib - inicialmente vacío, más grande
        self.plot_canvas = None
        self.plot_widget_frame = ctk.CTkFrame(plot_frame, fg_color="transparent")
        self.plot_widget_frame.grid(row=1, column=0, sticky="nsew", padx=8, pady=(0, 8))
        self.plot_widget_frame.grid_columnconfigure(0, weight=1)
        self.plot_widget_frame.grid_rowconfigure(0, weight=1)
        
        # Configurar colores de texto después de agregar todas las pestañas
        def configure_tab_text():
            try:
                # Acceder a los botones segmentados y cambiar el color del texto
                for button in self.result_tabview._segmented_button._buttons_dict.values():
                    button.configure(text_color="#2C3E50")
            except:
                try:
                    # Método alternativo: acceder directamente a los botones
                    for i in range(len(self.result_tabview._segmented_button._buttons_list)):
                        btn = self.result_tabview._segmented_button._buttons_list[i]
                        btn.configure(text_color="#2C3E50")
                except:
                    pass
        
        # Ejecutar después de que el widget se haya renderizado
        self.master.after(100, configure_tab_text)

    def create_input_fields(self, parent_frame, var_names, func_example):
        entries = {}
        
        # Función - más compacta
        func_container = ctk.CTkFrame(
            parent_frame, fg_color="#E8F5E9", corner_radius=8)
        func_container.pack(fill="x", padx=10, pady=(6, 6))
        
        func_label = ctk.CTkLabel(
            func_container, text=f"Función f({', '.join(var_names)}):",
            text_color="#2C3E50",
            font=ctk.CTkFont(size=11, weight="bold")
        )
        func_label.pack(padx=10, pady=(6, 4), anchor="w")
        
        func_entry_frame = ctk.CTkFrame(func_container, fg_color="transparent")
        func_entry_frame.pack(fill="x", padx=10, pady=(0, 6))
        
        entries['func'] = ctk.CTkEntry(
            func_entry_frame, placeholder_text=f"Ej: {func_example}",
            fg_color="#FFFFFF",
            border_color="#A8E6CF",
            border_width=1,
            text_color="#2C3E50",
            font=ctk.CTkFont(size=11),
            corner_radius=6,
            height=28
        )
        entries['func'].pack(fill="x", expand=True)
        
        # Límites - layout optimizado en grid para mejor uso del espacio - más compacto
        limits_container = ctk.CTkFrame(
            parent_frame, fg_color="#F8F9FA", corner_radius=8)
        limits_container.pack(fill="both", expand=True, padx=10, pady=(0, 6))
        
        limits_title = ctk.CTkLabel(
            limits_container, text="Límites de Integración",
            text_color="#2C3E50",
            font=ctk.CTkFont(size=11, weight="bold")
        )
        limits_title.pack(padx=10, pady=(6, 6), anchor="w")
        
        limits_frame = ctk.CTkFrame(limits_container, fg_color="transparent")
        limits_frame.pack(fill="both", expand=True, padx=10, pady=(0, 6))
        
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
                height=26
            )
            entries[f'{var}_low'].grid(row=i, column=1, padx=4, pady=2, sticky="ew")
            
            arrow_label = ctk.CTkLabel(
                limits_frame, text="→",
                text_color="#5A6C7D",
                font=ctk.CTkFont(size=11, weight="bold"),
                width=20
            )
            arrow_label.grid(row=i, column=2, padx=2, pady=2)
            
            entries[f'{var}_high'] = ctk.CTkEntry(
                limits_frame,
                fg_color="#FFFFFF",
                border_color="#A8E6CF",
                border_width=1,
                text_color="#2C3E50",
                font=ctk.CTkFont(size=11),
                corner_radius=6,
                height=26
            )
            entries[f'{var}_high'].grid(row=i, column=3, padx=4, pady=2, sticky="ew")
        
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
        button.pack(pady=(4, 6), padx=10, fill="x")

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
        button.pack(pady=(4, 6), padx=10, fill="x")

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
        button.pack(pady=(4, 6), padx=10, fill="x")

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
        
        # Mostrar el frame correspondiente - más compacto
        if mode == "Rectangulares":
            self.rect_frame.pack(fill="both", expand=True, padx=8, pady=4)
        elif mode == "Cilíndricas":
            self.cyl_frame.pack(fill="both", expand=True, padx=8, pady=4)
        elif mode == "Esféricas":
            self.sph_frame.pack(fill="both", expand=True, padx=8, pady=4)

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
        # Limpiar canvas anterior si existe
        if self.current_plot_canvas:
            self.current_plot_canvas.get_tk_widget().destroy()
            plt.close(self.current_plot_canvas.figure)
            self.current_plot_canvas = None
        
        # Cambiar a la pestaña de gráfico automáticamente
        self.result_tabview.set("📈 Gráfico")
        
        # Crear nuevo canvas en el frame de la interfaz
        self.current_plot_canvas = FigureCanvasTkAgg(fig, master=self.plot_widget_frame)
        self.current_plot_canvas.draw()
        self.current_plot_canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

class SurfaceIntegralFrame(ctk.CTkFrame):
    def __init__(self, master, math_backend):
        super().__init__(master, fg_color="#FFFFFF")
        self.math_backend = math_backend
        self.current_plot_window = None
        self.current_plot_canvas = None  # Canvas de matplotlib integrado
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)   # Sección superior compacta
        self.grid_rowconfigure(1, weight=4)   # Dar mucho más peso a la sección de resultados
        
        # Contenedor principal - más compacto
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.grid(row=0, column=0, sticky="nsew", padx=15, pady=(6, 4))
        
        # Selector de teoremas - más compacto
        theorems_frame = ctk.CTkFrame(main_container, fg_color="#E8F5E9", corner_radius=10)
        theorems_frame.pack(pady=(0, 8), fill="x")
        
        title_label = ctk.CTkLabel(
            theorems_frame, text="Teoremas de Cálculo Vectorial",
            text_color="#2C3E50",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        title_label.pack(pady=(8, 6))
        
        buttons_container = ctk.CTkFrame(theorems_frame, fg_color="transparent")
        buttons_container.pack(pady=(0, 8), padx=10, fill="x")
        
        self.btn_green = ctk.CTkButton(
            buttons_container, text="Teorema de Green",
            command=lambda: self.switch_theorem("Green"),
            fg_color="#A8E6CF",
            hover_color="#95D9C4",
            text_color="#2C3E50",
            font=ctk.CTkFont(size=11, weight="bold"),
            corner_radius=8,
            height=32
        )
        self.btn_green.pack(side="left", expand=True, padx=4, pady=2)
        
        self.btn_stokes = ctk.CTkButton(
            buttons_container, text="Teorema de Stokes",
            command=lambda: self.switch_theorem("Stokes"),
            fg_color="#FFFFFF",
            hover_color="#F5F5F5",
            text_color="#2C3E50",
            font=ctk.CTkFont(size=11, weight="bold"),
            corner_radius=8,
            height=32,
            border_width=1,
            border_color="#A8E6CF"
        )
        self.btn_stokes.pack(side="left", expand=True, padx=4, pady=2)
        
        self.btn_divergence = ctk.CTkButton(
            buttons_container, text="Teorema de Divergencia",
            command=lambda: self.switch_theorem("Divergence"),
            fg_color="#FFFFFF",
            hover_color="#F5F5F5",
            text_color="#2C3E50",
            font=ctk.CTkFont(size=11, weight="bold"),
            corner_radius=8,
            height=32,
            border_width=1,
            border_color="#A8E6CF"
        )
        self.btn_divergence.pack(side="left", expand=True, padx=4, pady=2)
        
        # Contenedor para los frames de cada teorema
        self.content_frame = ctk.CTkFrame(main_container, fg_color="#F8F9FA", corner_radius=8)
        self.content_frame.pack(fill="both", expand=True, pady=(0, 6))
        
        # Crear frames para cada teorema
        self.green_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.stokes_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.divergence_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        
        self.create_green_frame(self.green_frame)
        self.create_stokes_frame(self.stokes_frame)
        self.create_divergence_frame(self.divergence_frame)
        
        # Mostrar el frame inicial
        self.current_theorem = "Green"
        self.switch_theorem("Green")
        
        # Sección de resultados - usando pestañas como en TripleIntegralFrame
        result_container = ctk.CTkFrame(self, fg_color="#E8F5E9", corner_radius=8)
        result_container.grid(row=1, column=0, sticky="nsew", padx=15, pady=(2, 12))
        
        result_header_frame = ctk.CTkFrame(result_container, fg_color="transparent")
        result_header_frame.pack(padx=12, pady=(8, 4), fill="x")
        
        self.result_label = ctk.CTkLabel(
            result_header_frame, text="📊 Resultado del Cálculo",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color="#2C3E50"
        )
        self.result_label.pack(side="left")
        
        # Usar pestañas para separar resultados y gráfica
        self.result_tabview = ctk.CTkTabview(
            result_container,
            fg_color="#FFFFFF",
            corner_radius=8,
            segmented_button_fg_color="#E8F5E9",
            segmented_button_selected_color="#A8E6CF",
            segmented_button_unselected_color="#FFFFFF",
            segmented_button_selected_hover_color="#95D9C4",
            segmented_button_unselected_hover_color="#F0F0F0"
        )
        self.result_tabview.pack(padx=12, pady=(0, 8), fill="both", expand=True)
        
        # Configurar colores de texto después de crear el tabview
        def configure_tab_text():
            try:
                # Acceder a los botones segmentados y cambiar el color del texto
                for button in self.result_tabview._segmented_button._buttons_dict.values():
                    button.configure(text_color="#2C3E50")
            except:
                try:
                    # Método alternativo: acceder directamente a los botones
                    for i in range(len(self.result_tabview._segmented_button._buttons_list)):
                        btn = self.result_tabview._segmented_button._buttons_list[i]
                        btn.configure(text_color="#2C3E50")
                except:
                    pass
        
        # Ejecutar después de que el widget se haya renderizado
        self.after(100, configure_tab_text)
        
        # Pestaña de resultados textuales
        self.text_tab = self.result_tabview.add("📝 Resultados")
        self.text_tab.grid_columnconfigure(0, weight=1)
        self.text_tab.grid_rowconfigure(0, weight=1)
        
        self.result_text = ctk.CTkTextbox(
            self.text_tab, activate_scrollbars=True,
            fg_color="#FFFFFF",
            text_color="#2C3E50",
            border_color="#A8E6CF",
            border_width=1,
            corner_radius=6,
            font=ctk.CTkFont(size=11)
        )
        self.result_text.grid(row=0, column=0, sticky="nsew", padx=8, pady=8)
        self.result_text.insert("1.0", "Selecciona un teorema y completa los campos para calcular.")
        
        # Pestaña de gráfica
        self.plot_tab = self.result_tabview.add("📈 Gráfico")
        self.plot_tab.grid_columnconfigure(0, weight=1)
        self.plot_tab.grid_rowconfigure(0, weight=1)
        
        # Frame para la gráfica
        plot_frame = ctk.CTkFrame(self.plot_tab, fg_color="#FFFFFF", corner_radius=6)
        plot_frame.grid(row=0, column=0, sticky="nsew", padx=8, pady=8)
        plot_frame.grid_columnconfigure(0, weight=1)
        plot_frame.grid_rowconfigure(1, weight=1)
        
        plot_label = ctk.CTkLabel(
            plot_frame, text="📈 Gráfico de la Región",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#2C3E50"
        )
        plot_label.grid(row=0, column=0, pady=(8, 4))
        
        # Canvas para matplotlib
        self.plot_widget_frame = ctk.CTkFrame(plot_frame, fg_color="transparent")
        self.plot_widget_frame.grid(row=1, column=0, sticky="nsew", padx=8, pady=(0, 8))
        self.plot_widget_frame.grid_columnconfigure(0, weight=1)
        self.plot_widget_frame.grid_rowconfigure(0, weight=1)
        
        # Configurar colores de texto después de agregar todas las pestañas
        def configure_tab_text():
            try:
                # Acceder a los botones segmentados y cambiar el color del texto
                for button in self.result_tabview._segmented_button._buttons_dict.values():
                    button.configure(text_color="#2C3E50")
            except:
                try:
                    # Método alternativo: acceder directamente a los botones
                    for i in range(len(self.result_tabview._segmented_button._buttons_list)):
                        btn = self.result_tabview._segmented_button._buttons_list[i]
                        btn.configure(text_color="#2C3E50")
                except:
                    pass
        
        # Ejecutar después de que el widget se haya renderizado
        self.master.after(100, configure_tab_text)
    
    def switch_theorem(self, theorem):
        """Cambia entre los diferentes teoremas"""
        self.current_theorem = theorem
        
        # Ocultar todos los frames
        self.green_frame.pack_forget()
        self.stokes_frame.pack_forget()
        self.divergence_frame.pack_forget()
        
        # Actualizar estilos de botones
        buttons = {
            "Green": self.btn_green,
            "Stokes": self.btn_stokes,
            "Divergence": self.btn_divergence
        }
        
        for name, btn in buttons.items():
            if name == theorem:
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
        
        # Mostrar el frame correspondiente - más compacto
        if theorem == "Green":
            self.green_frame.pack(fill="both", expand=True, padx=8, pady=4)
        elif theorem == "Stokes":
            self.stokes_frame.pack(fill="both", expand=True, padx=8, pady=4)
        elif theorem == "Divergence":
            self.divergence_frame.pack(fill="both", expand=True, padx=8, pady=4)
    
    def create_green_frame(self, frame):
        """Crea la interfaz para el Teorema de Green - Layout horizontal"""
        # Información del teorema - más compacto
        info_frame = ctk.CTkFrame(frame, fg_color="#E8F5E9", corner_radius=8)
        info_frame.pack(fill="x", padx=10, pady=(0, 6))
        
        info_label = ctk.CTkLabel(
            info_frame,
            text="Teorema de Green: ∮_C (P dx + Q dy) = ∬_D (∂Q/∂x - ∂P/∂y) dA",
            text_color="#2C3E50",
            font=ctk.CTkFont(size=9, weight="bold"),
            wraplength=600
        )
        info_label.pack(padx=10, pady=4)
        
        # Contenedor principal horizontal para aprovechar espacio
        main_green_container = ctk.CTkFrame(frame, fg_color="transparent")
        main_green_container.pack(fill="both", expand=True, padx=10, pady=(0, 6))
        
        # Lado izquierdo: Campo Vectorial
        left_green = ctk.CTkFrame(main_green_container, fg_color="#F8F9FA", corner_radius=8)
        left_green.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        vector_title = ctk.CTkLabel(
            left_green, text="Campo Vectorial F = (P, Q)",
            text_color="#2C3E50",
            font=ctk.CTkFont(size=10, weight="bold")
        )
        vector_title.pack(padx=8, pady=(6, 4), anchor="w")
        
        # Componente P
        p_frame = ctk.CTkFrame(left_green, fg_color="transparent")
        p_frame.pack(fill="x", padx=8, pady=3)
        ctk.CTkLabel(p_frame, text="P:", text_color="#2C3E50",
                    font=ctk.CTkFont(size=10, weight="bold"), width=35).pack(side="left", padx=(0, 6))
        self.green_P_entry = ctk.CTkEntry(p_frame, placeholder_text="x**2 + y",
            fg_color="#FFFFFF", border_color="#A8E6CF", border_width=1,
            text_color="#2C3E50", font=ctk.CTkFont(size=10), corner_radius=6, height=26)
        self.green_P_entry.pack(side="left", fill="x", expand=True)
        self.green_P_entry.insert(0, "x**2 - y**2")
        
        # Componente Q
        q_frame = ctk.CTkFrame(left_green, fg_color="transparent")
        q_frame.pack(fill="x", padx=8, pady=(3, 6))
        ctk.CTkLabel(q_frame, text="Q:", text_color="#2C3E50",
                    font=ctk.CTkFont(size=10, weight="bold"), width=35).pack(side="left", padx=(0, 6))
        self.green_Q_entry = ctk.CTkEntry(q_frame, placeholder_text="2*x*y",
            fg_color="#FFFFFF", border_color="#A8E6CF", border_width=1,
            text_color="#2C3E50", font=ctk.CTkFont(size=10), corner_radius=6, height=26)
        self.green_Q_entry.pack(side="left", fill="x", expand=True)
        self.green_Q_entry.insert(0, "2*x*y")
        
        # Lado derecho: Región D
        right_green = ctk.CTkFrame(main_green_container, fg_color="#E8F5E9", corner_radius=8)
        right_green.pack(side="right", fill="both", expand=True, padx=(5, 0))
        
        region_title = ctk.CTkLabel(
            right_green, text="Región D (Límites)",
            text_color="#2C3E50",
            font=ctk.CTkFont(size=10, weight="bold")
        )
        region_title.pack(padx=8, pady=(6, 4), anchor="w")
        
        limits_frame = ctk.CTkFrame(right_green, fg_color="transparent")
        limits_frame.pack(fill="both", expand=True, padx=8, pady=(0, 6))
        
        # Límites de x - en una línea compacta
        x_row = ctk.CTkFrame(limits_frame, fg_color="transparent")
        x_row.pack(fill="x", pady=2)
        ctk.CTkLabel(x_row, text="x:", text_color="#2C3E50",
                    font=ctk.CTkFont(size=9, weight="bold"), width=25).pack(side="left", padx=(0, 4))
        self.green_x_min = ctk.CTkEntry(x_row, fg_color="#FFFFFF",
            border_color="#A8E6CF", border_width=1, text_color="#2C3E50",
            font=ctk.CTkFont(size=9), corner_radius=5, height=24)
        self.green_x_min.pack(side="left", padx=2, fill="x", expand=True)
        self.green_x_min.insert(0, "0")
        ctk.CTkLabel(x_row, text="→", text_color="#5A6C7D",
                    font=ctk.CTkFont(size=9), width=12).pack(side="left", padx=1)
        self.green_x_max = ctk.CTkEntry(x_row, fg_color="#FFFFFF",
            border_color="#A8E6CF", border_width=1, text_color="#2C3E50",
            font=ctk.CTkFont(size=9), corner_radius=5, height=24)
        self.green_x_max.pack(side="left", padx=2, fill="x", expand=True)
        self.green_x_max.insert(0, "1")
        
        # Límites de y - en una línea compacta
        y_row = ctk.CTkFrame(limits_frame, fg_color="transparent")
        y_row.pack(fill="x", pady=2)
        ctk.CTkLabel(y_row, text="y:", text_color="#2C3E50",
                    font=ctk.CTkFont(size=9, weight="bold"), width=25).pack(side="left", padx=(0, 4))
        self.green_y_min = ctk.CTkEntry(y_row, fg_color="#FFFFFF",
            border_color="#A8E6CF", border_width=1, text_color="#2C3E50",
            font=ctk.CTkFont(size=9), corner_radius=5, height=24)
        self.green_y_min.pack(side="left", padx=2, fill="x", expand=True)
        self.green_y_min.insert(0, "0")
        ctk.CTkLabel(y_row, text="→", text_color="#5A6C7D",
                    font=ctk.CTkFont(size=9), width=12).pack(side="left", padx=1)
        self.green_y_max = ctk.CTkEntry(y_row, fg_color="#FFFFFF",
            border_color="#A8E6CF", border_width=1, text_color="#2C3E50",
            font=ctk.CTkFont(size=9), corner_radius=5, height=24)
        self.green_y_max.pack(side="left", padx=2, fill="x", expand=True)
        self.green_y_max.insert(0, "1")
        
        # Botón calcular - compacto
        calc_button = ctk.CTkButton(
            frame, text="Calcular con Teorema de Green",
            command=self.calculate_green,
            fg_color="#A8E6CF",
            hover_color="#95D9C4",
            text_color="#2C3E50",
            font=ctk.CTkFont(size=11, weight="bold"),
            corner_radius=8,
            height=34
        )
        calc_button.pack(pady=(4, 6), padx=10, fill="x")
    
    def create_stokes_frame(self, frame):
        """Crea la interfaz para el Teorema de Stokes - Layout compacto"""
        # Información del teorema - muy compacta
        info_frame = ctk.CTkFrame(frame, fg_color="#E8F5E9", corner_radius=8)
        info_frame.pack(fill="x", padx=10, pady=(0, 6))
        
        info_label = ctk.CTkLabel(
            info_frame,
            text="Teorema de Stokes: ∮_C F · dr = ∬_S curl(F) · dS",
            text_color="#2C3E50",
            font=ctk.CTkFont(size=9, weight="bold"),
            wraplength=600
        )
        info_label.pack(padx=10, pady=4)
        
        # Contenedor principal horizontal para aprovechar espacio
        main_stokes_container = ctk.CTkFrame(frame, fg_color="transparent")
        main_stokes_container.pack(fill="both", expand=True, padx=10, pady=(0, 6))
        
        # Lado izquierdo: Campo Vectorial
        left_stokes = ctk.CTkFrame(main_stokes_container, fg_color="#F8F9FA", corner_radius=8)
        left_stokes.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        vector_title = ctk.CTkLabel(
            left_stokes, text="Campo Vectorial F = (P, Q, R)",
            text_color="#2C3E50",
            font=ctk.CTkFont(size=10, weight="bold")
        )
        vector_title.pack(padx=8, pady=(6, 4), anchor="w")
        
        # Componente P
        p_frame = ctk.CTkFrame(left_stokes, fg_color="transparent")
        p_frame.pack(fill="x", padx=8, pady=3)
        ctk.CTkLabel(p_frame, text="P:", text_color="#2C3E50",
                    font=ctk.CTkFont(size=10, weight="bold"), width=35).pack(side="left", padx=(0, 6))
        self.stokes_P_entry = ctk.CTkEntry(p_frame, placeholder_text="y",
            fg_color="#FFFFFF", border_color="#A8E6CF", border_width=1,
            text_color="#2C3E50", font=ctk.CTkFont(size=10), corner_radius=6, height=26)
        self.stokes_P_entry.pack(side="left", fill="x", expand=True)
        self.stokes_P_entry.insert(0, "y")
        
        # Componente Q
        q_frame = ctk.CTkFrame(left_stokes, fg_color="transparent")
        q_frame.pack(fill="x", padx=8, pady=3)
        ctk.CTkLabel(q_frame, text="Q:", text_color="#2C3E50",
                    font=ctk.CTkFont(size=10, weight="bold"), width=35).pack(side="left", padx=(0, 6))
        self.stokes_Q_entry = ctk.CTkEntry(q_frame, placeholder_text="z",
            fg_color="#FFFFFF", border_color="#A8E6CF", border_width=1,
            text_color="#2C3E50", font=ctk.CTkFont(size=10), corner_radius=6, height=26)
        self.stokes_Q_entry.pack(side="left", fill="x", expand=True)
        self.stokes_Q_entry.insert(0, "z")
        
        # Componente R
        r_frame = ctk.CTkFrame(left_stokes, fg_color="transparent")
        r_frame.pack(fill="x", padx=8, pady=(3, 6))
        ctk.CTkLabel(r_frame, text="R:", text_color="#2C3E50",
                    font=ctk.CTkFont(size=10, weight="bold"), width=35).pack(side="left", padx=(0, 6))
        self.stokes_R_entry = ctk.CTkEntry(r_frame, placeholder_text="x",
            fg_color="#FFFFFF", border_color="#A8E6CF", border_width=1,
            text_color="#2C3E50", font=ctk.CTkFont(size=10), corner_radius=6, height=26)
        self.stokes_R_entry.pack(side="left", fill="x", expand=True)
        self.stokes_R_entry.insert(0, "x")
        
        # Lado derecho: Superficie y Región lado a lado (dos columnas)
        right_stokes = ctk.CTkFrame(main_stokes_container, fg_color="transparent")
        right_stokes.pack(side="right", fill="both", expand=True, padx=(5, 0))
        
        # Superficie - arriba
        surface_frame = ctk.CTkFrame(right_stokes, fg_color="#E8F5E9", corner_radius=8)
        surface_frame.pack(fill="x", pady=(0, 5))
        
        surface_title = ctk.CTkLabel(
            surface_frame, text="Superficie: z(x,y)",
            text_color="#2C3E50",
            font=ctk.CTkFont(size=10, weight="bold")
        )
        surface_title.pack(padx=8, pady=(5, 3), anchor="w")
        
        z_frame = ctk.CTkFrame(surface_frame, fg_color="transparent")
        z_frame.pack(fill="x", padx=8, pady=(0, 5))
        self.stokes_z_entry = ctk.CTkEntry(z_frame, placeholder_text="x + y",
            fg_color="#FFFFFF", border_color="#A8E6CF", border_width=1,
            text_color="#2C3E50", font=ctk.CTkFont(size=10), corner_radius=6, height=26)
        self.stokes_z_entry.pack(fill="x")
        self.stokes_z_entry.insert(0, "x + y")
        
        # Región de proyección - abajo
        region_frame = ctk.CTkFrame(right_stokes, fg_color="#E8F5E9", corner_radius=8)
        region_frame.pack(fill="x")
        
        region_title = ctk.CTkLabel(
            region_frame, text="Límites xy",
            text_color="#2C3E50",
            font=ctk.CTkFont(size=10, weight="bold")
        )
        region_title.pack(padx=8, pady=(5, 3), anchor="w")
        
        limits_container = ctk.CTkFrame(region_frame, fg_color="transparent")
        limits_container.pack(fill="x", padx=8, pady=(0, 5))
        
        # Límites de x - en una línea compacta
        x_row = ctk.CTkFrame(limits_container, fg_color="transparent")
        x_row.pack(fill="x", pady=1)
        ctk.CTkLabel(x_row, text="x:", text_color="#2C3E50",
                    font=ctk.CTkFont(size=9, weight="bold"), width=25).pack(side="left", padx=(0, 4))
        self.stokes_x_min = ctk.CTkEntry(x_row, fg_color="#FFFFFF",
            border_color="#A8E6CF", border_width=1, text_color="#2C3E50",
            font=ctk.CTkFont(size=9), corner_radius=5, height=24)
        self.stokes_x_min.pack(side="left", padx=2, fill="x", expand=True)
        self.stokes_x_min.insert(0, "0")
        ctk.CTkLabel(x_row, text="→", text_color="#5A6C7D",
                    font=ctk.CTkFont(size=9), width=12).pack(side="left", padx=1)
        self.stokes_x_max = ctk.CTkEntry(x_row, fg_color="#FFFFFF",
            border_color="#A8E6CF", border_width=1, text_color="#2C3E50",
            font=ctk.CTkFont(size=9), corner_radius=5, height=24)
        self.stokes_x_max.pack(side="left", padx=2, fill="x", expand=True)
        self.stokes_x_max.insert(0, "1")
        
        # Límites de y - en una línea compacta
        y_row = ctk.CTkFrame(limits_container, fg_color="transparent")
        y_row.pack(fill="x", pady=1)
        ctk.CTkLabel(y_row, text="y:", text_color="#2C3E50",
                    font=ctk.CTkFont(size=9, weight="bold"), width=25).pack(side="left", padx=(0, 4))
        self.stokes_y_min = ctk.CTkEntry(y_row, fg_color="#FFFFFF",
            border_color="#A8E6CF", border_width=1, text_color="#2C3E50",
            font=ctk.CTkFont(size=9), corner_radius=5, height=24)
        self.stokes_y_min.pack(side="left", padx=2, fill="x", expand=True)
        self.stokes_y_min.insert(0, "0")
        ctk.CTkLabel(y_row, text="→", text_color="#5A6C7D",
                    font=ctk.CTkFont(size=9), width=12).pack(side="left", padx=1)
        self.stokes_y_max = ctk.CTkEntry(y_row, fg_color="#FFFFFF",
            border_color="#A8E6CF", border_width=1, text_color="#2C3E50",
            font=ctk.CTkFont(size=9), corner_radius=5, height=24)
        self.stokes_y_max.pack(side="left", padx=2, fill="x", expand=True)
        self.stokes_y_max.insert(0, "1")
        
        # Botón calcular - compacto
        calc_button = ctk.CTkButton(
            frame, text="Calcular con Teorema de Stokes",
            command=self.calculate_stokes,
            fg_color="#A8E6CF",
            hover_color="#95D9C4",
            text_color="#2C3E50",
            font=ctk.CTkFont(size=11, weight="bold"),
            corner_radius=8,
            height=34
        )
        calc_button.pack(pady=(4, 6), padx=10, fill="x")
    
    def create_divergence_frame(self, frame):
        """Crea la interfaz para el Teorema de Divergencia - Layout compacto"""
        # Información del teorema - muy compacta
        info_frame = ctk.CTkFrame(frame, fg_color="#E8F5E9", corner_radius=8)
        info_frame.pack(fill="x", padx=10, pady=(0, 6))
        
        info_label = ctk.CTkLabel(
            info_frame,
            text="Teorema de Divergencia: ∬_S F · n dS = ∭_V div(F) dV",
            text_color="#2C3E50",
            font=ctk.CTkFont(size=9, weight="bold"),
            wraplength=600
        )
        info_label.pack(padx=10, pady=4)
        
        # Contenedor principal horizontal para aprovechar espacio
        main_div_container = ctk.CTkFrame(frame, fg_color="transparent")
        main_div_container.pack(fill="both", expand=True, padx=10, pady=(0, 6))
        
        # Lado izquierdo: Campo Vectorial
        left_div = ctk.CTkFrame(main_div_container, fg_color="#F8F9FA", corner_radius=8)
        left_div.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        vector_title = ctk.CTkLabel(
            left_div, text="Campo Vectorial F = (P, Q, R)",
            text_color="#2C3E50",
            font=ctk.CTkFont(size=10, weight="bold")
        )
        vector_title.pack(padx=8, pady=(6, 4), anchor="w")
        
        # Componente P
        p_frame = ctk.CTkFrame(left_div, fg_color="transparent")
        p_frame.pack(fill="x", padx=8, pady=3)
        ctk.CTkLabel(p_frame, text="P:", text_color="#2C3E50",
                    font=ctk.CTkFont(size=10, weight="bold"), width=35).pack(side="left", padx=(0, 6))
        self.div_P_entry = ctk.CTkEntry(p_frame, placeholder_text="x",
            fg_color="#FFFFFF", border_color="#A8E6CF", border_width=1,
            text_color="#2C3E50", font=ctk.CTkFont(size=10), corner_radius=6, height=26)
        self.div_P_entry.pack(side="left", fill="x", expand=True)
        self.div_P_entry.insert(0, "x")
        
        # Componente Q
        q_frame = ctk.CTkFrame(left_div, fg_color="transparent")
        q_frame.pack(fill="x", padx=8, pady=3)
        ctk.CTkLabel(q_frame, text="Q:", text_color="#2C3E50",
                    font=ctk.CTkFont(size=10, weight="bold"), width=35).pack(side="left", padx=(0, 6))
        self.div_Q_entry = ctk.CTkEntry(q_frame, placeholder_text="y",
            fg_color="#FFFFFF", border_color="#A8E6CF", border_width=1,
            text_color="#2C3E50", font=ctk.CTkFont(size=10), corner_radius=6, height=26)
        self.div_Q_entry.pack(side="left", fill="x", expand=True)
        self.div_Q_entry.insert(0, "y")
        
        # Componente R
        r_frame = ctk.CTkFrame(left_div, fg_color="transparent")
        r_frame.pack(fill="x", padx=8, pady=(3, 6))
        ctk.CTkLabel(r_frame, text="R:", text_color="#2C3E50",
                    font=ctk.CTkFont(size=10, weight="bold"), width=35).pack(side="left", padx=(0, 6))
        self.div_R_entry = ctk.CTkEntry(r_frame, placeholder_text="z",
            fg_color="#FFFFFF", border_color="#A8E6CF", border_width=1,
            text_color="#2C3E50", font=ctk.CTkFont(size=10), corner_radius=6, height=26)
        self.div_R_entry.pack(side="left", fill="x", expand=True)
        self.div_R_entry.insert(0, "z")
        
        # Lado derecho: Límites de la región V
        right_div = ctk.CTkFrame(main_div_container, fg_color="#E8F5E9", corner_radius=8)
        right_div.pack(side="right", fill="both", expand=True, padx=(5, 0))
        
        limits_title = ctk.CTkLabel(
            right_div, text="Límites de la Región V",
            text_color="#2C3E50",
            font=ctk.CTkFont(size=10, weight="bold")
        )
        limits_title.pack(padx=8, pady=(6, 4), anchor="w")
        
        limits_container = ctk.CTkFrame(right_div, fg_color="transparent")
        limits_container.pack(fill="both", expand=True, padx=8, pady=(0, 6))
        
        # Límites de x - en una línea compacta
        x_row = ctk.CTkFrame(limits_container, fg_color="transparent")
        x_row.pack(fill="x", pady=2)
        ctk.CTkLabel(x_row, text="x:", text_color="#2C3E50",
                    font=ctk.CTkFont(size=9, weight="bold"), width=25).pack(side="left", padx=(0, 4))
        self.div_x_min = ctk.CTkEntry(x_row, fg_color="#FFFFFF",
            border_color="#A8E6CF", border_width=1, text_color="#2C3E50",
            font=ctk.CTkFont(size=9), corner_radius=5, height=24)
        self.div_x_min.pack(side="left", padx=2, fill="x", expand=True)
        self.div_x_min.insert(0, "0")
        ctk.CTkLabel(x_row, text="→", text_color="#5A6C7D",
                    font=ctk.CTkFont(size=9), width=12).pack(side="left", padx=1)
        self.div_x_max = ctk.CTkEntry(x_row, fg_color="#FFFFFF",
            border_color="#A8E6CF", border_width=1, text_color="#2C3E50",
            font=ctk.CTkFont(size=9), corner_radius=5, height=24)
        self.div_x_max.pack(side="left", padx=2, fill="x", expand=True)
        self.div_x_max.insert(0, "1")
        
        # Límites de y - en una línea compacta
        y_row = ctk.CTkFrame(limits_container, fg_color="transparent")
        y_row.pack(fill="x", pady=2)
        ctk.CTkLabel(y_row, text="y:", text_color="#2C3E50",
                    font=ctk.CTkFont(size=9, weight="bold"), width=25).pack(side="left", padx=(0, 4))
        self.div_y_min = ctk.CTkEntry(y_row, fg_color="#FFFFFF",
            border_color="#A8E6CF", border_width=1, text_color="#2C3E50",
            font=ctk.CTkFont(size=9), corner_radius=5, height=24)
        self.div_y_min.pack(side="left", padx=2, fill="x", expand=True)
        self.div_y_min.insert(0, "0")
        ctk.CTkLabel(y_row, text="→", text_color="#5A6C7D",
                    font=ctk.CTkFont(size=9), width=12).pack(side="left", padx=1)
        self.div_y_max = ctk.CTkEntry(y_row, fg_color="#FFFFFF",
            border_color="#A8E6CF", border_width=1, text_color="#2C3E50",
            font=ctk.CTkFont(size=9), corner_radius=5, height=24)
        self.div_y_max.pack(side="left", padx=2, fill="x", expand=True)
        self.div_y_max.insert(0, "1")
        
        # Límites de z - en una línea compacta
        z_row = ctk.CTkFrame(limits_container, fg_color="transparent")
        z_row.pack(fill="x", pady=2)
        ctk.CTkLabel(z_row, text="z:", text_color="#2C3E50",
                    font=ctk.CTkFont(size=9, weight="bold"), width=25).pack(side="left", padx=(0, 4))
        self.div_z_min = ctk.CTkEntry(z_row, fg_color="#FFFFFF",
            border_color="#A8E6CF", border_width=1, text_color="#2C3E50",
            font=ctk.CTkFont(size=9), corner_radius=5, height=24)
        self.div_z_min.pack(side="left", padx=2, fill="x", expand=True)
        self.div_z_min.insert(0, "0")
        ctk.CTkLabel(z_row, text="→", text_color="#5A6C7D",
                    font=ctk.CTkFont(size=9), width=12).pack(side="left", padx=1)
        self.div_z_max = ctk.CTkEntry(z_row, fg_color="#FFFFFF",
            border_color="#A8E6CF", border_width=1, text_color="#2C3E50",
            font=ctk.CTkFont(size=9), corner_radius=5, height=24)
        self.div_z_max.pack(side="left", padx=2, fill="x", expand=True)
        self.div_z_max.insert(0, "1")
        
        # Botón calcular - compacto
        calc_button = ctk.CTkButton(
            frame, text="Calcular con Teorema de Divergencia",
            command=self.calculate_divergence,
            fg_color="#A8E6CF",
            hover_color="#95D9C4",
            text_color="#2C3E50",
            font=ctk.CTkFont(size=11, weight="bold"),
            corner_radius=8,
            height=34
        )
        calc_button.pack(pady=(4, 6), padx=10, fill="x")
    
    def calculate_green(self):
        """Calcula usando el Teorema de Green"""
        try:
            # Obtener valores de los campos de entrada
            P_str = self.green_P_entry.get().strip()
            Q_str = self.green_Q_entry.get().strip()
            
            # Verificar que los campos no estén vacíos
            if not P_str or not Q_str:
                self.result_text.delete("1.0", "end")
                self.result_text.insert("1.0", "❌ Error: Por favor ingresa valores para P(x,y) y Q(x,y)")
                return
            
            # Obtener límites de la región
            x_min = self.green_x_min.get().strip()
            x_max = self.green_x_max.get().strip()
            y_min = self.green_y_min.get().strip()
            y_max = self.green_y_max.get().strip()
            
            if not all([x_min, x_max, y_min, y_max]):
                self.result_text.delete("1.0", "end")
                self.result_text.insert("1.0", "❌ Error: Por favor completa todos los límites de integración")
                return
            
            region_limits = {
                'x': (x_min, x_max),
                'y': (y_min, y_max)
            }
            
            # Calcular el resultado
            result = self.math_backend.solve_green_theorem(P_str, Q_str, region_limits)
            
            # Mostrar el resultado
            self.result_text.delete("1.0", "end")
            if "error" in result:
                self.result_text.insert("1.0", f"❌ {result['error']}")
            else:
                display_text = (
                    f"{result['proceso']}\n\n"
                    f"🔢 Resultado Simbólico:\n{result['resultado_simbolico']}\n\n"
                    f"📊 Resultado Numérico:\n{result['resultado_numerico']}"
                )
                self.result_text.insert("1.0", display_text)
                
                # Graficar la región
                figura = self.math_backend.plot_green_region(region_limits)
                if figura:
                    self.show_plot_green(figura)
        except Exception as e:
            import traceback
            error_msg = f"❌ Error inesperado:\n{str(e)}\n\n{traceback.format_exc()}"
            self.result_text.delete("1.0", "end")
            self.result_text.insert("1.0", error_msg)
    
    def show_plot_green(self, fig):
        """Muestra la gráfica de la región de Green en la interfaz"""
        # Limpiar canvas anterior si existe
        if self.current_plot_canvas:
            self.current_plot_canvas.get_tk_widget().destroy()
            plt.close(self.current_plot_canvas.figure)
            self.current_plot_canvas = None
        
        # Cambiar a la pestaña de gráfico automáticamente
        self.result_tabview.set("📈 Gráfico")
        
        # Crear nuevo canvas en el frame de la interfaz
        self.current_plot_canvas = FigureCanvasTkAgg(fig, master=self.plot_widget_frame)
        self.current_plot_canvas.draw()
        self.current_plot_canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")
    
    def calculate_stokes(self):
        """Calcula usando el Teorema de Stokes"""
        try:
            # Obtener valores de los campos de entrada
            P_str = self.stokes_P_entry.get().strip()
            Q_str = self.stokes_Q_entry.get().strip()
            R_str = self.stokes_R_entry.get().strip()
            z_str = self.stokes_z_entry.get().strip()
            
            # Verificar que los campos no estén vacíos
            if not all([P_str, Q_str, R_str, z_str]):
                self.result_text.delete("1.0", "end")
                self.result_text.insert("1.0", "❌ Error: Por favor completa todos los campos")
                return
            
            # Obtener límites
            x_min = self.stokes_x_min.get().strip()
            x_max = self.stokes_x_max.get().strip()
            y_min = self.stokes_y_min.get().strip()
            y_max = self.stokes_y_max.get().strip()
            
            if not all([x_min, x_max, y_min, y_max]):
                self.result_text.delete("1.0", "end")
                self.result_text.insert("1.0", "❌ Error: Por favor completa todos los límites")
                return
            
            surface_params = {
                'z': z_str,
                'x': (x_min, x_max),
                'y': (y_min, y_max)
            }
            
            # Calcular el resultado
            result = self.math_backend.solve_stokes_theorem(P_str, Q_str, R_str, surface_params)
            
            # Mostrar el resultado
            self.result_text.delete("1.0", "end")
            if "error" in result:
                self.result_text.insert("1.0", f"❌ {result['error']}")
            else:
                display_text = (
                    f"{result['proceso']}\n\n"
                    f"🔢 Resultado Simbólico:\n{result['resultado_simbolico']}\n\n"
                    f"📊 Resultado Numérico:\n{result['resultado_numerico']}"
                )
                self.result_text.insert("1.0", display_text)
                
                # Graficar la superficie
                figura = self.math_backend.plot_stokes_surface(surface_params)
                if figura:
                    self.show_plot_stokes(figura)
        except Exception as e:
            import traceback
            error_msg = f"❌ Error inesperado:\n{str(e)}\n\n{traceback.format_exc()}"
            self.result_text.delete("1.0", "end")
            self.result_text.insert("1.0", error_msg)
    
    def show_plot_stokes(self, fig):
        """Muestra la gráfica de la superficie de Stokes en la interfaz"""
        # Limpiar canvas anterior si existe
        if self.current_plot_canvas:
            self.current_plot_canvas.get_tk_widget().destroy()
            plt.close(self.current_plot_canvas.figure)
            self.current_plot_canvas = None
        
        # Cambiar a la pestaña de gráfico automáticamente
        self.result_tabview.set("📈 Gráfico")
        
        # Crear nuevo canvas en el frame de la interfaz
        self.current_plot_canvas = FigureCanvasTkAgg(fig, master=self.plot_widget_frame)
        self.current_plot_canvas.draw()
        self.current_plot_canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")
    
    def calculate_divergence(self):
        """Calcula usando el Teorema de Divergencia"""
        try:
            # Obtener valores de los campos de entrada
            P_str = self.div_P_entry.get().strip()
            Q_str = self.div_Q_entry.get().strip()
            R_str = self.div_R_entry.get().strip()
            
            # Verificar que los campos no estén vacíos
            if not all([P_str, Q_str, R_str]):
                self.result_text.delete("1.0", "end")
                self.result_text.insert("1.0", "❌ Error: Por favor completa todos los campos")
                return
            
            # Obtener límites
            x_min = self.div_x_min.get().strip()
            x_max = self.div_x_max.get().strip()
            y_min = self.div_y_min.get().strip()
            y_max = self.div_y_max.get().strip()
            z_min = self.div_z_min.get().strip()
            z_max = self.div_z_max.get().strip()
            
            if not all([x_min, x_max, y_min, y_max, z_min, z_max]):
                self.result_text.delete("1.0", "end")
                self.result_text.insert("1.0", "❌ Error: Por favor completa todos los límites")
                return
            
            volume_limits = {
                'x': (x_min, x_max),
                'y': (y_min, y_max),
                'z': (z_min, z_max)
            }
            
            # Calcular el resultado
            result = self.math_backend.solve_divergence_theorem(P_str, Q_str, R_str, volume_limits)
            
            # Mostrar el resultado
            self.result_text.delete("1.0", "end")
            if "error" in result:
                self.result_text.insert("1.0", f"❌ {result['error']}")
            else:
                display_text = (
                    f"{result['proceso']}\n\n"
                    f"🔢 Resultado Simbólico:\n{result['resultado_simbolico']}\n\n"
                    f"📊 Resultado Numérico:\n{result['resultado_numerico']}"
                )
                self.result_text.insert("1.0", display_text)
                
                # Graficar la región
                figura = self.math_backend.plot_divergence_region(volume_limits)
                if figura:
                    self.show_plot_divergence(figura)
        except Exception as e:
            import traceback
            error_msg = f"❌ Error inesperado:\n{str(e)}\n\n{traceback.format_exc()}"
            self.result_text.delete("1.0", "end")
            self.result_text.insert("1.0", error_msg)
    
    def show_plot_divergence(self, fig):
        """Muestra la gráfica de la región de Divergencia en la interfaz"""
        # Limpiar canvas anterior si existe
        if self.current_plot_canvas:
            self.current_plot_canvas.get_tk_widget().destroy()
            plt.close(self.current_plot_canvas.figure)
            self.current_plot_canvas = None
        
        # Cambiar a la pestaña de gráfico automáticamente
        self.result_tabview.set("📈 Gráfico")
        
        # Crear nuevo canvas en el frame de la interfaz
        self.current_plot_canvas = FigureCanvasTkAgg(fig, master=self.plot_widget_frame)
        self.current_plot_canvas.draw()
        self.current_plot_canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Calculadora de Cálculo Multivariado")
        self.geometry("1200x850")
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