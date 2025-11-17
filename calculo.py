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

            fig = plt.figure(figsize=(8, 7))
            ax = fig.add_subplot(111, projection='3d')
            ax.plot_surface(X, Y, Z_low, cmap='winter', alpha=0.7)
            ax.plot_surface(X, Y, Z_high, cmap='viridis', alpha=0.7)

            ax.set_xlabel("Eje X")
            ax.set_ylabel("Eje Y")
            ax.set_zlabel("Eje Z")
            ax.set_title("Dominio de Integración Rectangular")
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

            fig = plt.figure(figsize=(8, 7))
            ax = fig.add_subplot(111, projection='3d')
            ax.plot_surface(X, Y, Z_low, cmap='winter', alpha=0.6)
            ax.plot_surface(X, Y, Z_high, cmap='viridis', alpha=0.6)

            ax.set_xlabel("Eje X")
            ax.set_ylabel("Eje Y")
            ax.set_zlabel("Eje Z")
            ax.set_title("Dominio de Integración Cilíndrico")
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

            fig = plt.figure(figsize=(8, 7))
            ax = fig.add_subplot(111, projection='3d')
            ax.plot_surface(X, Y, Z, cmap='magma', alpha=0.8)

            ax.set_xlabel("Eje X")
            ax.set_ylabel("Eje Y")
            ax.set_zlabel("Eje Z")
            ax.set_title("Dominio de Integración Esférico")
            return fig
        except Exception as e:
            print(f"Error al graficar (esférico): {e}")
            return None
