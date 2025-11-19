import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

class MathBackend:
    def __init__(self):
        self.x, self.y, self.z = sp.symbols('x y z')
        self.r, self.theta = sp.symbols('r theta')
        self.rho, self.phi = sp.symbols('rho phi')

    def _parse_expression(self, expr_str):
        return sp.sympify(expr_str)

    def solve_triple_integral(self, func_str, limits, mode):
        try:
            if mode == "Rectangulares":
                return self._solve_rectangular(func_str, limits)
            elif mode == "Cilíndricas":
                return self._solve_cylindrical(func_str, limits)
            elif mode == "Esféricas":
                return self._solve_spherical(func_str, limits)
            else:
                return {"error": "Modo no soportado"}
        except Exception as e:
            return {"error": f"Error en el cálculo: {e}"}

    # --- INTEGRALES ---
    def _solve_rectangular(self, func_str, limits):
        f = self._parse_expression(func_str)
        lim_x = [self._parse_expression(l) for l in limits['x']]
        lim_y = [self._parse_expression(l) for l in limits['y']]
        lim_z = [self._parse_expression(l) for l in limits['z']]
        integral = sp.integrate(f, (self.z, lim_z[0], lim_z[1]), (self.y, lim_y[0], lim_y[1]), (self.x, lim_x[0], lim_x[1]))
        proceso = f"∫({lim_x[0]})→({lim_x[1]}) ∫({lim_y[0]})→({lim_y[1]}) ∫({lim_z[0]})→({lim_z[1]}) [{f}] dz dy dx"
        return {
            "proceso": proceso,
            "resultado_simbolico": str(integral),
            "resultado_numerico": f"{integral.evalf():.4f}" if integral.is_number else "N/A"
        }

    def _solve_cylindrical(self, func_str, limits):
        f_rect = self._parse_expression(func_str)
        subs = {self.x: self.r * sp.cos(self.theta), self.y: self.r * sp.sin(self.theta)}
        f_cyl = f_rect.subs(subs)
        f_integrar = f_cyl * self.r

        lim_z = [self._parse_expression(l) for l in limits['z']]
        lim_r = [self._parse_expression(l) for l in limits['r']]
        lim_theta = [self._parse_expression(l) for l in limits['theta']]

        integral = sp.integrate(f_integrar, (self.z, lim_z[0], lim_z[1]), (self.r, lim_r[0], lim_r[1]), (self.theta, lim_theta[0], lim_theta[1]))
        proceso = f"∫({lim_theta[0]})→({lim_theta[1]}) ∫({lim_r[0]})→({lim_r[1]}) ∫({lim_z[0]})→({lim_z[1]}) [{f_cyl}] * r dz dr dθ"
        return {
            "proceso": proceso,
            "resultado_simbolico": str(integral),
            "resultado_numerico": f"{integral.evalf():.4f}" if integral.is_number else "N/A"
        }

    def _solve_spherical(self, func_str, limits):
        f_rect = self._parse_expression(func_str)
        subs = {
            self.x: self.rho * sp.sin(self.phi) * sp.cos(self.theta),
            self.y: self.rho * sp.sin(self.phi) * sp.sin(self.theta),
            self.z: self.rho * sp.cos(self.phi)
        }
        f_sph = f_rect.subs(subs)
        f_integrar = f_sph * self.rho**2 * sp.sin(self.phi)

        lim_rho = [self._parse_expression(l) for l in limits['rho']]
        lim_phi = [self._parse_expression(l) for l in limits['phi']]
        lim_theta = [self._parse_expression(l) for l in limits['theta']]

        integral = sp.integrate(f_integrar, (self.rho, lim_rho[0], lim_rho[1]), (self.phi, lim_phi[0], lim_phi[1]), (self.theta, lim_theta[0], lim_theta[1]))
        proceso = f"∫({lim_theta[0]})→({lim_theta[1]}) ∫({lim_phi[0]})→({lim_phi[1]}) ∫({lim_rho[0]})→({lim_rho[1]}) [{f_sph}] * ρ²sin(φ) dρ dφ dθ"
        return {
            "proceso": proceso,
            "resultado_simbolico": str(integral),
            "resultado_numerico": f"{integral.evalf():.4f}" if integral.is_number else "N/A"
        }

    # --- GRAFICADOS ---
    def plot_rectangular_domain(self, limits):
        try:
            lim_x = [self._parse_expression(l) for l in limits['x']]
            lim_y = [self._parse_expression(l) for l in limits['y']]
            lim_z = [self._parse_expression(l) for l in limits['z']]

            x_inf, x_sup = float(lim_x[0].evalf()), float(lim_x[1].evalf())
            y_inf, y_sup = float(lim_y[0].evalf()), float(lim_y[1].evalf())
            z_inf, z_sup = float(lim_z[0].evalf()), float(lim_z[1].evalf())

            X, Y = np.meshgrid(np.linspace(x_inf, x_sup, 20), np.linspace(y_inf, y_sup, 20))
            Z_low = np.full_like(X, z_inf)
            Z_high = np.full_like(X, z_sup)

            fig = plt.figure(figsize=(12, 9))
            ax = fig.add_subplot(111, projection='3d')
            ax.plot_surface(X, Y, Z_low, cmap='winter', alpha=0.7)
            ax.plot_surface(X, Y, Z_high, cmap='viridis', alpha=0.7)

            ax.set_xlabel("Eje X", fontsize=11)
            ax.set_ylabel("Eje Y", fontsize=11)
            ax.set_zlabel("Eje Z", fontsize=11)
            ax.set_title("Dominio de Integración Rectangular", fontsize=13, fontweight='bold')
            return fig
        except Exception as e:
            print(f"Error al graficar (rectangular): {e}")
            return None

    def plot_cylindrical_domain(self, limits):
        try:
            lim_z = [self._parse_expression(l) for l in limits['z']]
            lim_r = [self._parse_expression(l) for l in limits['r']]
            lim_theta = [self._parse_expression(l) for l in limits['theta']]

            r_inf, r_sup = float(lim_r[0].evalf()), float(lim_r[1].evalf())
            theta_inf, theta_sup = float(lim_theta[0].evalf()), float(lim_theta[1].evalf())

            R, THETA = np.meshgrid(np.linspace(r_inf, r_sup, 40), np.linspace(theta_inf, theta_sup, 40))
            X, Y = R * np.cos(THETA), R * np.sin(THETA)

            z_func_low = sp.lambdify((self.r, self.theta), lim_z[0], 'numpy')
            z_func_high = sp.lambdify((self.r, self.theta), lim_z[1], 'numpy')

            Z_low = z_func_low(R, THETA)
            Z_high = z_func_high(R, THETA)

            # ✅ Si Z es escalar, convertir a matriz
            if np.isscalar(Z_low):
                Z_low = np.full_like(R, float(Z_low))
            if np.isscalar(Z_high):
                Z_high = np.full_like(R, float(Z_high))

            fig = plt.figure(figsize=(12, 9))
            ax = fig.add_subplot(111, projection='3d')
            ax.plot_surface(X, Y, Z_low, cmap='winter', alpha=0.6)
            ax.plot_surface(X, Y, Z_high, cmap='viridis', alpha=0.6)

            ax.set_xlabel("Eje X", fontsize=11)
            ax.set_ylabel("Eje Y", fontsize=11)
            ax.set_zlabel("Eje Z", fontsize=11)
            ax.set_title("Dominio de Integración Cilíndrico", fontsize=13, fontweight='bold')
            return fig
        except Exception as e:
            print(f"Error al graficar (cilíndrico): {e}")
            return None

    def plot_spherical_domain(self, limits):
        try:
            lim_rho = [self._parse_expression(l) for l in limits['rho']]
            lim_phi = [self._parse_expression(l) for l in limits['phi']]
            lim_theta = [self._parse_expression(l) for l in limits['theta']]

            rho_inf, rho_sup = float(lim_rho[0].evalf()), float(lim_rho[1].evalf())
            phi_inf, phi_sup = float(lim_phi[0].evalf()), float(lim_phi[1].evalf())
            theta_inf, theta_sup = float(lim_theta[0].evalf()), float(lim_theta[1].evalf())

            PHI, THETA = np.meshgrid(np.linspace(phi_inf, phi_sup, 40), np.linspace(theta_inf, theta_sup, 40))
            RHO = np.full_like(PHI, rho_sup)

            X = RHO * np.sin(PHI) * np.cos(THETA)
            Y = RHO * np.sin(PHI) * np.sin(THETA)
            Z = RHO * np.cos(PHI)

            fig = plt.figure(figsize=(12, 9))
            ax = fig.add_subplot(111, projection='3d')
            ax.plot_surface(X, Y, Z, cmap='magma', alpha=0.8)

            ax.set_xlabel("Eje X", fontsize=11)
            ax.set_ylabel("Eje Y", fontsize=11)
            ax.set_zlabel("Eje Z", fontsize=11)
            ax.set_title("Dominio de Integración Esférico", fontsize=13, fontweight='bold')
            return fig
        except Exception as e:
            print(f"Error al graficar (esférico): {e}")
            return None

    # --- TEOREMAS ---
    def solve_green_theorem(self, P_str, Q_str, region_limits):
        """
        Resuelve el Teorema de Green:
        ∮_C (P dx + Q dy) = ∬_D (∂Q/∂x - ∂P/∂y) dA
        
        Parámetros:
        - P_str: Componente P del campo vectorial (función de x, y)
        - Q_str: Componente Q del campo vectorial (función de x, y)
        - region_limits: Diccionario con límites de la región D
            {'x': (x_min, x_max), 'y': (y_min, y_max)}
        """
        try:
            P = self._parse_expression(P_str)
            Q = self._parse_expression(Q_str)
            
            # Calcular las derivadas parciales
            dQ_dx = sp.diff(Q, self.x)
            dP_dy = sp.diff(P, self.y)
            
            # Calcular el integrando: ∂Q/∂x - ∂P/∂y
            integrando = dQ_dx - dP_dy
            
            # Obtener límites de la región
            lim_x = [self._parse_expression(l) for l in region_limits['x']]
            lim_y = [self._parse_expression(l) for l in region_limits['y']]
            
            # Calcular la integral doble
            integral = sp.integrate(
                integrando, 
                (self.y, lim_y[0], lim_y[1]), 
                (self.x, lim_x[0], lim_x[1])
            )
            
            # Construir el proceso
            proceso = (
                f"Teorema de Green:\n"
                f"∮_C (P dx + Q dy) = ∬_D (∂Q/∂x - ∂P/∂y) dA\n\n"
                f"Campo vectorial: F = ({P}, {Q})\n"
                f"∂Q/∂x = {dQ_dx}\n"
                f"∂P/∂y = {dP_dy}\n"
                f"Integrando: {integrando}\n\n"
                f"Integral doble:\n"
                f"∫({lim_x[0]})→({lim_x[1]}) ∫({lim_y[0]})→({lim_y[1]}) [{integrando}] dy dx"
            )
            
            return {
                "proceso": proceso,
                "resultado_simbolico": str(integral),
                "resultado_numerico": f"{integral.evalf():.4f}" if integral.is_number else "N/A",
                "integrando": str(integrando),
                "dQ_dx": str(dQ_dx),
                "dP_dy": str(dP_dy)
            }
        except Exception as e:
            return {"error": f"Error en el cálculo del Teorema de Green: {e}"}

    def plot_green_region(self, region_limits):
        """
        Grafica la región D para el Teorema de Green
        """
        try:
            lim_x = [self._parse_expression(l) for l in region_limits['x']]
            lim_y = [self._parse_expression(l) for l in region_limits['y']]

            x_min = float(lim_x[0].evalf())
            x_max = float(lim_x[1].evalf())
            y_min = float(lim_y[0].evalf())
            y_max = float(lim_y[1].evalf())

            fig, ax = plt.subplots(figsize=(10, 8))
            
            # Crear un rectángulo para la región
            rect = plt.Rectangle((x_min, y_min), x_max - x_min, y_max - y_min,
                               fill=True, color='lightblue', alpha=0.5, 
                               edgecolor='darkblue', linewidth=2, label='Región D')
            ax.add_patch(rect)
            
            # Dibujar el borde de la región (curva C)
            x_border = [x_min, x_max, x_max, x_min, x_min]
            y_border = [y_min, y_min, y_max, y_max, y_min]
            ax.plot(x_border, y_border, 'b-', linewidth=2.5, label='Curva C (borde)')
            
            # Configurar ejes
            ax.set_xlim(x_min - 0.5, x_max + 0.5)
            ax.set_ylim(y_min - 0.5, y_max + 0.5)
            ax.set_xlabel("Eje X", fontsize=12)
            ax.set_ylabel("Eje Y", fontsize=12)
            ax.set_title("Región D del Teorema de Green", fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3)
            ax.legend(loc='upper right')
            ax.set_aspect('equal', adjustable='box')
            
            return fig
        except Exception as e:
            print(f"Error al graficar región de Green: {e}")
            return None

    def solve_stokes_theorem(self, P_str, Q_str, R_str, surface_params):
        """
        Resuelve el Teorema de Stokes:
        ∮_C F · dr = ∬_S curl(F) · dS
        
        Para una superficie z = f(x, y) con límites en x e y:
        - P_str, Q_str, R_str: Componentes del campo vectorial F = (P, Q, R)
        - surface_params: Diccionario con:
            'z': función z(x, y) que define la superficie
            'x': límites (x_min, x_max)
            'y': límites (y_min, y_max)
        """
        try:
            # Obtener la función de superficie z = f(x, y)
            z_surface_str = surface_params['z']
            z_surface = self._parse_expression(z_surface_str)
            
            # Sustituir z en las componentes del campo vectorial
            P = self._parse_expression(P_str).subs(self.z, z_surface)
            Q = self._parse_expression(Q_str).subs(self.z, z_surface)
            R = self._parse_expression(R_str).subs(self.z, z_surface)
            
            # Calcular el rotacional: curl(F) = (∂R/∂y - ∂Q/∂z, ∂P/∂z - ∂R/∂x, ∂Q/∂x - ∂P/∂y)
            # Después de sustituir z, las derivadas respecto a z son 0
            dR_dy = sp.diff(R, self.y)
            dQ_dz = sp.Integer(0)  # Después de sustituir z, no hay dependencia explícita
            
            dP_dz = sp.Integer(0)
            dR_dx = sp.diff(R, self.x)
            
            dQ_dx = sp.diff(Q, self.x)
            dP_dy = sp.diff(P, self.y)
            
            curl_x = dR_dy - dQ_dz  # ∂R/∂y - ∂Q/∂z
            curl_y = dP_dz - dR_dx  # ∂P/∂z - ∂R/∂x
            curl_z = dQ_dx - dP_dy  # ∂Q/∂x - ∂P/∂y
            
            # Calcular el vector normal (simplificado para z = f(x,y))
            # Para superficie z = f(x,y), el vector normal hacia arriba es:
            # n = (-∂z/∂x, -∂z/∂y, 1) / sqrt(1 + (∂z/∂x)² + (∂z/∂y)²)
            dz_dx = sp.diff(z_surface, self.x)
            dz_dy = sp.diff(z_surface, self.y)
            
            # Para z = f(x,y), la integral de superficie del rotacional es:
            # ∬ curl(F) · n dS = ∬ [curl_x(-∂z/∂x) + curl_y(-∂z/∂y) + curl_z] dx dy
            
            integrando = curl_x * (-dz_dx) + curl_y * (-dz_dy) + curl_z
            
            # Simplificar el integrando
            integrando = sp.simplify(integrando)
            
            # Obtener límites
            lim_x = [self._parse_expression(l) for l in surface_params['x']]
            lim_y = [self._parse_expression(l) for l in surface_params['y']]
            
            # Calcular la integral doble
            integral = sp.integrate(
                integrando,
                (self.y, lim_y[0], lim_y[1]),
                (self.x, lim_x[0], lim_x[1])
            )
            
            # Construir el proceso
            proceso = (
                f"Teorema de Stokes:\n"
                f"∮_C F · dr = ∬_S curl(F) · dS\n\n"
                f"Campo vectorial: F = ({P_str}, {Q_str}, {R_str})\n"
                f"Superficie: z = {z_surface}\n\n"
                f"Rotacional:\n"
                f"curl(F) = (∂R/∂y - ∂Q/∂z, ∂P/∂z - ∂R/∂x, ∂Q/∂x - ∂P/∂y)\n"
                f"curl(F) = ({curl_x}, {curl_y}, {curl_z})\n\n"
                f"Integrando: {integrando}\n\n"
                f"Integral de superficie:\n"
                f"∫({lim_x[0]})→({lim_x[1]}) ∫({lim_y[0]})→({lim_y[1]}) [{integrando}] dy dx"
            )
            
            return {
                "proceso": proceso,
                "resultado_simbolico": str(integral),
                "resultado_numerico": f"{integral.evalf():.4f}" if integral.is_number else "N/A",
                "integrando": str(integrando),
                "curl": (str(curl_x), str(curl_y), str(curl_z))
            }
        except Exception as e:
            return {"error": f"Error en el cálculo del Teorema de Stokes: {e}"}

    def plot_stokes_surface(self, surface_params):
        """
        Grafica la superficie para el Teorema de Stokes
        """
        try:
            z_surface_str = surface_params['z']
            z_surface = self._parse_expression(z_surface_str)
            
            lim_x = [self._parse_expression(l) for l in surface_params['x']]
            lim_y = [self._parse_expression(l) for l in surface_params['y']]
            
            x_min = float(lim_x[0].evalf())
            x_max = float(lim_x[1].evalf())
            y_min = float(lim_y[0].evalf())
            y_max = float(lim_y[1].evalf())
            
            # Crear malla
            x = np.linspace(x_min, x_max, 30)
            y = np.linspace(y_min, y_max, 30)
            X, Y = np.meshgrid(x, y)
            
            # Evaluar z = f(x, y)
            z_func = sp.lambdify((self.x, self.y), z_surface, 'numpy')
            Z = z_func(X, Y)
            
            fig = plt.figure(figsize=(12, 9))
            ax = fig.add_subplot(111, projection='3d')
            
            # Graficar la superficie
            surf = ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.8, 
                                  edgecolor='black', linewidth=0.3)
            
            # Agregar borde de la superficie (evaluar como arrays)
            x_border = np.array([x_min, x_max, x_max, x_min, x_min])
            y_border = np.array([y_min, y_min, y_max, y_max, y_min])
            z_border = z_func(x_border, y_border)
            ax.plot3D(x_border, y_border, z_border, 'r-', linewidth=2.5, label='Curva C (borde)')
            
            ax.set_xlabel("Eje X", fontsize=11)
            ax.set_ylabel("Eje Y", fontsize=11)
            ax.set_zlabel("Eje Z", fontsize=11)
            ax.set_title("Superficie S del Teorema de Stokes", fontsize=13, fontweight='bold')
            
            fig.colorbar(surf, shrink=0.5, aspect=5)
            
            return fig
        except Exception as e:
            print(f"Error al graficar superficie de Stokes: {e}")
            return None

    def solve_divergence_theorem(self, P_str, Q_str, R_str, volume_limits):
        """
        Resuelve el Teorema de Divergencia:
        ∬_S F · n dS = ∭_V div(F) dV
        
        Para una región rectangular V con límites en x, y, z:
        - P_str, Q_str, R_str: Componentes del campo vectorial F = (P, Q, R)
        - volume_limits: Diccionario con:
            'x': límites (x_min, x_max)
            'y': límites (y_min, y_max)
            'z': límites (z_min, z_max)
        """
        try:
            P = self._parse_expression(P_str)
            Q = self._parse_expression(Q_str)
            R = self._parse_expression(R_str)
            
            # Calcular la divergencia: div(F) = ∂P/∂x + ∂Q/∂y + ∂R/∂z
            dP_dx = sp.diff(P, self.x)
            dQ_dy = sp.diff(Q, self.y)
            dR_dz = sp.diff(R, self.z)
            
            divergence = dP_dx + dQ_dy + dR_dz
            
            # Simplificar la divergencia
            divergence = sp.simplify(divergence)
            
            # Obtener límites
            lim_x = [self._parse_expression(l) for l in volume_limits['x']]
            lim_y = [self._parse_expression(l) for l in volume_limits['y']]
            lim_z = [self._parse_expression(l) for l in volume_limits['z']]
            
            # Calcular la integral triple
            integral = sp.integrate(
                divergence,
                (self.z, lim_z[0], lim_z[1]),
                (self.y, lim_y[0], lim_y[1]),
                (self.x, lim_x[0], lim_x[1])
            )
            
            # Construir el proceso
            proceso = (
                f"Teorema de Divergencia:\n"
                f"∬_S F · n dS = ∭_V div(F) dV\n\n"
                f"Campo vectorial: F = ({P}, {Q}, {R})\n"
                f"Divergencia: div(F) = ∂P/∂x + ∂Q/∂y + ∂R/∂z\n"
                f"∂P/∂x = {dP_dx}\n"
                f"∂Q/∂y = {dQ_dy}\n"
                f"∂R/∂z = {dR_dz}\n"
                f"div(F) = {divergence}\n\n"
                f"Integral triple:\n"
                f"∫({lim_x[0]})→({lim_x[1]}) ∫({lim_y[0]})→({lim_y[1]}) ∫({lim_z[0]})→({lim_z[1]}) [{divergence}] dz dy dx"
            )
            
            return {
                "proceso": proceso,
                "resultado_simbolico": str(integral),
                "resultado_numerico": f"{integral.evalf():.4f}" if integral.is_number else "N/A",
                "divergence": str(divergence),
                "dP_dx": str(dP_dx),
                "dQ_dy": str(dQ_dy),
                "dR_dz": str(dR_dz)
            }
        except Exception as e:
            return {"error": f"Error en el cálculo del Teorema de Divergencia: {e}"}

    def plot_divergence_region(self, volume_limits):
        """
        Grafica la región sólida V para el Teorema de Divergencia
        """
        try:
            lim_x = [self._parse_expression(l) for l in volume_limits['x']]
            lim_y = [self._parse_expression(l) for l in volume_limits['y']]
            lim_z = [self._parse_expression(l) for l in volume_limits['z']]
            
            x_min = float(lim_x[0].evalf())
            x_max = float(lim_x[1].evalf())
            y_min = float(lim_y[0].evalf())
            y_max = float(lim_y[1].evalf())
            z_min = float(lim_z[0].evalf())
            z_max = float(lim_z[1].evalf())
            
            # Crear malla para las caras del cubo
            X, Y = np.meshgrid(np.linspace(x_min, x_max, 20), 
                              np.linspace(y_min, y_max, 20))
            
            fig = plt.figure(figsize=(12, 9))
            ax = fig.add_subplot(111, projection='3d')
            
            # Graficar las 6 caras del cubo
            # Cara inferior (z = z_min)
            ax.plot_surface(X, Y, np.full_like(X, z_min), 
                          color='blue', alpha=0.3, label='Cara z=z_min')
            
            # Cara superior (z = z_max)
            ax.plot_surface(X, Y, np.full_like(X, z_max), 
                          color='green', alpha=0.3, label='Cara z=z_max')
            
            # Caras laterales
            X_z, Z = np.meshgrid(np.linspace(x_min, x_max, 20),
                                np.linspace(z_min, z_max, 20))
            Y_z_min = np.full_like(X_z, y_min)
            Y_z_max = np.full_like(X_z, y_max)
            
            ax.plot_surface(X_z, Y_z_min, Z, color='red', alpha=0.3)
            ax.plot_surface(X_z, Y_z_max, Z, color='orange', alpha=0.3)
            
            Y_y, Z_y = np.meshgrid(np.linspace(y_min, y_max, 20),
                                  np.linspace(z_min, z_max, 20))
            X_y_min = np.full_like(Y_y, x_min)
            X_y_max = np.full_like(Y_y, x_max)
            
            ax.plot_surface(X_y_min, Y_y, Z_y, color='purple', alpha=0.3)
            ax.plot_surface(X_y_max, Y_y, Z_y, color='cyan', alpha=0.3)
            
            # Dibujar bordes más visibles
            # Bordes del cubo
            ax.plot3D([x_min, x_max, x_max, x_min, x_min],
                     [y_min, y_min, y_max, y_max, y_min],
                     [z_min, z_min, z_min, z_min, z_min],
                     'b-', linewidth=2, label='Borde inferior')
            ax.plot3D([x_min, x_max, x_max, x_min, x_min],
                     [y_min, y_min, y_max, y_max, y_min],
                     [z_max, z_max, z_max, z_max, z_max],
                     'g-', linewidth=2, label='Borde superior')
            
            ax.set_xlabel("Eje X", fontsize=11)
            ax.set_ylabel("Eje Y", fontsize=11)
            ax.set_zlabel("Eje Z", fontsize=11)
            ax.set_title("Región V del Teorema de Divergencia", fontsize=13, fontweight='bold')
            
            return fig
        except Exception as e:
            print(f"Error al graficar región de Divergencia: {e}")
            return None