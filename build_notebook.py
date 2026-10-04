import nbformat as nbf

nb = nbf.v4.new_notebook()
C = []
md = lambda s: C.append(nbf.v4.new_markdown_cell(s.strip()))
code = lambda s: C.append(nbf.v4.new_code_cell(s.strip()))

md(r"""
# Deflexión de la luz por un objeto masivo: métrica de Schwarzschild

**Relatividad General — Presentación 1, Tema 1: Tests de la Relatividad General**

Objetivo: calcular cuánto se desvía un rayo de luz que pasa cerca de un objeto masivo, usando la métrica de Schwarzschild, y comparar el resultado analítico con una integración numérica exacta y con las observaciones.

**Contenido**
1. La métrica de Schwarzschild y las geodésicas nulas
2. Ecuación de la órbita de un fotón
3. Solución perturbativa y ángulo de deflexión $\hat\alpha = 4GM/(c^2 b)$
4. Verificación simbólica (SymPy)
5. Integración numérica exacta y comparación
6. Trayectorias de la luz
7. El caso del Sol y verificación experimental
8. Más allá del régimen débil: esfera de fotones
9. Conclusiones y referencias
""")

md(r"""
## 1. Métrica de Schwarzschild y geodésicas nulas

Para el exterior de una masa $M$ esférica y estática, con signatura $(-,+,+,+)$:

$$ds^2 = -\left(1-\frac{r_s}{r}\right)c^2dt^2 + \left(1-\frac{r_s}{r}\right)^{-1}dr^2 + r^2\left(d\theta^2+\sin^2\theta\,d\varphi^2\right),\qquad r_s=\frac{2GM}{c^2}.$$

La luz sigue **geodésicas nulas** ($ds^2=0$). Por la simetría esférica la órbita queda en un plano, y tomamos $\theta=\pi/2$. Con parámetro afín $\lambda$, la métrica no depende de $t$ ni de $\varphi$, así que hay dos cantidades conservadas:

$$E = \left(1-\frac{r_s}{r}\right)c^2\dot t,\qquad L = r^2\dot\varphi .$$

El cociente $b = cL/E$ es el **parámetro de impacto**: la distancia a la que pasaría el rayo del centro si no hubiera deflexión (lejos de la masa, donde el espaciotiempo es plano).
""")

md(r"""
## 2. Ecuación de la órbita

Imponiendo $ds^2=0$ y sustituyendo $\dot t$ y $\dot\varphi$:

$$\dot r^2 = \frac{E^2}{c^2} - \left(1-\frac{r_s}{r}\right)\frac{L^2}{r^2}.$$

Dividiendo por $\dot\varphi^2 = L^2/r^4$ y definiendo $u=1/r$:

$$\left(\frac{du}{d\varphi}\right)^2 = \frac{1}{b^2} - u^2 + r_s\,u^3 .$$

Derivando respecto de $\varphi$:

$$\boxed{\frac{d^2u}{d\varphi^2} + u = \frac{3}{2}\,r_s\,u^2 = \frac{3GM}{c^2}u^2}$$

Sin el término de la derecha (espacio plano) la solución es una recta: $u_0=\sin\varphi/b$. El término $\tfrac32 r_s u^2$ es la corrección relativista y es pequeño si $r_s \ll b$.
""")

md(r"""
## 3. Solución perturbativa

Sea $\varepsilon = r_s/b \ll 1$. Escribimos $u = u_0 + u_1$ con $u_0=\sin\varphi/b$. A primer orden:

$$u_1'' + u_1 = \frac{3 r_s}{2}\,\frac{\sin^2\varphi}{b^2} = \frac{3r_s}{4b^2}\left(1-\cos 2\varphi\right).$$

Una solución particular es $u_1 = \dfrac{r_s}{4b^2}\left(3+\cos 2\varphi\right)=\dfrac{r_s}{2b^2}\left(1+\cos^2\varphi\right)$ (se verifica en la sección 4), de modo que

$$u(\varphi) = \frac{\sin\varphi}{b} + \frac{r_s}{2b^2}\left(1+\cos^2\varphi\right).$$

**Ángulo de deflexión.** El rayo viene del infinito ($u=0$) en $\varphi=-\delta_1$ y se va al infinito en $\varphi=\pi+\delta_2$. Con $\delta$ pequeño, $\sin\varphi\approx\mp\delta$ y $\cos^2\varphi\approx1$, entonces

$$0 = \mp\frac{\delta}{b} + \frac{r_s}{b^2}\quad\Rightarrow\quad \delta_1=\delta_2=\frac{r_s}{b}.$$

La dirección total cambia en $\hat\alpha=\delta_1+\delta_2$:

$$\boxed{\hat\alpha = \frac{2r_s}{b} = \frac{4GM}{c^2 b}}$$

(con $r_s = 2GM/c^2$). Es **el doble** del valor newtoniano ($2GM/c^2b$, tratando la luz como partícula de velocidad $c$). El factor extra viene de la curvatura espacial: la parte espacial de la métrica contribuye tanto como la dilatación temporal.
""")

md(r"""
## 4. Verificación simbólica con SymPy

Comprobamos que $u_1$ resuelve la ecuación perturbada y que el ángulo de salida da $\hat\alpha = 2r_s/b$.
""")

code(r"""
import sympy as sp

phi, b, rs = sp.symbols('varphi b r_s', positive=True)

u0 = sp.sin(phi)/b
u1 = rs/(2*b**2) * (1 + sp.cos(phi)**2)

# u1'' + u1 - (3/2) rs u0^2 debe ser 0
residuo = sp.simplify(sp.diff(u1, phi, 2) + u1 - sp.Rational(3, 2)*rs*u0**2)
print("Residuo de la ecuación perturbada:", residuo)

# ángulo de salida: resolver u(pi + d) = 0 a primer orden en d
d = sp.symbols('delta')
u = u0 + u1
eq = sp.series(u.subs(phi, sp.pi + d), d, 0, 2).removeO()
delta_sol = sp.solve(eq, d)[0]
print("delta =", delta_sol, "  ->  alpha = 2*delta =", sp.simplify(2*delta_sol))
""")

md(r"""
## 5. Integración numérica exacta

Sin aproximar, a partir de $(du/d\varphi)^2 = b^{-2}-u^2+r_s u^3$, el rayo llega a una distancia mínima $r_0=1/u_0$, donde $u_0$ es la menor raíz positiva de $b^{-2}-u^2+r_su^3=0$. Entonces

$$\Delta\varphi = 2\int_0^{u_0}\frac{du}{\sqrt{b^{-2}-u^2+r_s u^3}},\qquad \hat\alpha_{\rm exacto}=\Delta\varphi-\pi .$$

Trabajamos en unidades $GM/c^2 = 1$ (así $r_s=2$ y las longitudes se miden en $GM/c^2$).
""")

code(r"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad, solve_ivp

plt.rcParams.update({"figure.dpi": 110, "axes.grid": True, "grid.alpha": .3})

def alpha_exacto(b, M=1.0):
    # deflexión exacta (rad) para parámetro de impacto b, en unidades G=c=1
    rs = 2*M
    # b^-2 - u^2 + rs u^3 = 0 ; menor raíz positiva real
    raices = np.roots([rs, -1, 0, 1/b**2])
    u0 = min(r.real for r in raices if abs(r.imag) < 1e-12 and r.real > 0)
    # P(u) = (u0-u) * Q(u),  Q(u) = -(rs u^2 + (rs u0 - 1) u + (rs u0^2 - u0))
    B = rs*u0 - 1
    Cc = B*u0
    Q = lambda u: -(rs*u**2 + B*u + Cc)
    integral, _ = quad(lambda u: 1/np.sqrt(Q(u)), 0, u0, weight='alg', wvar=(0, -0.5))
    return 2*integral - np.pi

alpha_1 = lambda b, M=1.0: 4*M/b   # primer orden

for b in [1e3, 1e2, 30, 10, 6]:
    ex, a1 = alpha_exacto(b), alpha_1(b)
    print(f"b = {b:7.1f} GM/c²   exacto = {ex:.6f} rad   4GM/c²b = {a1:.6f} rad   error relativo = {abs(ex-a1)/ex:.2%}")
""")

code(r"""
b_c = 3*np.sqrt(3)   # parámetro de impacto crítico (sección 8)
b_vals = np.logspace(np.log10(b_c*1.02), 3, 200)
ex = np.array([alpha_exacto(b) for b in b_vals])
a1 = alpha_1(b_vals)

fig, ax = plt.subplots(1, 2, figsize=(11, 4))
ax[0].loglog(b_vals, ex, label="exacto (numérico)")
ax[0].loglog(b_vals, a1, "--", label=r"$4GM/c^2b$")
ax[0].loglog(b_vals, a1/2, ":", label=r"newtoniano $2GM/c^2b$")
ax[0].set(xlabel=r"$b \;[GM/c^2]$", ylabel=r"$\hat\alpha$ [rad]", title="Ángulo de deflexión")
ax[0].legend()

ax[1].semilogx(b_vals, (a1-ex)/ex*100)
ax[1].set(xlabel=r"$b \;[GM/c^2]$", ylabel="error de primer orden [%]", title="Error de la aproximación débil")
plt.tight_layout(); plt.show()
""")

md(r"""
La fórmula de primer orden coincide con la solución exacta para $b\gg GM/c^2$ (el error relativo decrece como $\sim 1/b$). Al acercarse $b$ a $b_c\approx5.2\,GM/c^2$ la deflexión diverge (sección 8). El siguiente orden del desarrollo es $\hat\alpha = \frac{4GM}{c^2b} + \frac{15\pi}{4}\left(\frac{GM}{c^2b}\right)^2+\dots$, que podemos comprobar:
""")

code(r"""
b = 200.0
a2 = 4/b + 15*np.pi/4/b**2
print(f"exacto: {alpha_exacto(b):.8f}   1er orden: {4/b:.8f}   2º orden: {a2:.8f}")
""")

md(r"""
## 6. Trayectorias de la luz

Integramos directamente $u''+u=3Mu^2$ (con $G=c=1$, $M=1$) para varios parámetros de impacto. La condición inicial es $u(0)=0$, $u'(0)=1/b$ (rayo que llega desde $\varphi=0$, lejos de la masa) y se integra hasta que $u$ vuelve a cero. Comparamos con la línea recta (sin gravedad).
""")

code(r"""
def trayectoria(b, M=1.0):
    f = lambda p, y: [y[1], -y[0] + 3*M*y[0]**2]
    ev = lambda p, y: y[0]
    ev.terminal, ev.direction = True, -1
    sol = solve_ivp(f, [0, 4*np.pi], [0, 1/b], events=ev, rtol=1e-11, atol=1e-13,
                    dense_output=True)
    p = np.linspace(0.02, sol.t[-1] - 0.02, 4000)
    u = sol.sol(p)[0]
    r = 1/u
    return r*np.cos(p), r*np.sin(p)

fig, ax = plt.subplots(figsize=(7, 5))
for b in [7, 10, 15, 25]:
    x, y = trayectoria(b)
    ax.plot(x, y, label=f"b = {b} GM/c²")
ax.add_patch(plt.Circle((0, 0), 2, color="k"))   # r_s = 2GM/c²
ax.set(xlim=(-60, 60), ylim=(-5, 40), aspect="equal", xlabel=r"$x\;[GM/c^2]$", ylabel=r"$y\;[GM/c^2]$",
       title="Rayos de luz desviados por una masa (círculo negro: $r_s$)")
ax.legend(); plt.show()
""")

md(r"""
## 7. El Sol y las observaciones

Para un rayo que **roza** el limbo solar, $b=R_\odot$:
""")

code(r"""
G, c = 6.67430e-11, 2.99792458e8
M_sun, R_sun = 1.98847e30, 6.957e8
rad2arcsec = 180/np.pi*3600

alpha_sol = 4*G*M_sun/(c**2*R_sun)
print(f"GM/c² (Sol)       = {G*M_sun/c**2:.1f} m")
print(f"r_s / R_sol       = {2*G*M_sun/c**2/R_sun:.2e}   (régimen de campo débil)")
print(f"Deflexión RG      = {alpha_sol:.3e} rad = {alpha_sol*rad2arcsec:.4f} segundos de arco")
print(f"Deflexión newton. = {alpha_sol/2*rad2arcsec:.4f} segundos de arco")

# Verificación con la integral exacta (unidades GM/c²)
b_sol = R_sun/(G*M_sun/c**2)
print(f"Deflexión exacta  = {alpha_exacto(b_sol)*rad2arcsec:.4f} segundos de arco")
""")

code(r"""
# Deflexión en función de la distancia al centro del Sol (en radios solares)
b_Rsun = np.linspace(1, 20, 200)
a = 4*G*M_sun/(c**2*b_Rsun*R_sun)*rad2arcsec

fig, ax = plt.subplots(figsize=(6.5, 4))
ax.plot(b_Rsun, a, label="RG: $4GM/c^2b$")
ax.plot(b_Rsun, a/2, "--", label="Newton: $2GM/c^2b$")
ax.errorbar([1.0], [1.98], yerr=[0.16], fmt="o", capsize=3, label="Eddington 1919 (Sobral) 1.98 ± 0.16″")
ax.errorbar([1.0], [1.61], yerr=[0.40], fmt="s", capsize=3, label="Eddington 1919 (Príncipe) 1.61 ± 0.40″")
ax.set(xlabel=r"$b\;[R_\odot]$", ylabel="deflexión [″]", title="Deflexión de la luz estelar por el Sol")
ax.legend(fontsize=8); plt.show()
""")

md(r"""
### Verificación experimental

| Experimento | Resultado | Cociente con RG |
|---|---|---|
| Eddington, eclipse de 1919 (Sobral) | $1.98\pm0.16''$ | ≈ 1.13 |
| Eddington, eclipse de 1919 (Príncipe) | $1.61\pm0.40''$ | ≈ 0.92 |
| Interferometría radio (VLBI) | acuerdo a < 0.1 % | ≈ 1.000 |

Los datos de 1919 descartaron el valor newtoniano (0.87″) y favorecieron el de Einstein (1.75″). Las medidas modernas por radio (VLBI) confirman el factor 2 con gran precisión. Las cifras son valores de referencia de la literatura; conviene verificar la fuente primaria antes de exponer.

Parametrizado en el formalismo PPN, $\hat\alpha = \tfrac{1+\gamma}{2}\cdot\tfrac{4GM}{c^2b}$: la observación fija $\gamma = 1$ (RG) con gran precisión. El valor newtoniano correspondería a $\gamma=0$.
""")

md(r"""
## 8. Más allá del campo débil: esfera de fotones

Para $b$ comparable a $r_s$, el rayo puede dar vueltas alrededor de la masa. En $r=3GM/c^2$ hay una órbita circular inestable (**esfera de fotones**). El parámetro de impacto crítico es

$$b_c = \frac{3\sqrt3\,GM}{c^2}\approx 5.196\,\frac{GM}{c^2}.$$

Para $b<b_c$ la luz es capturada; para $b\to b_c^+$ el ángulo de deflexión diverge logarítmicamente.
""")

code(r"""
print("b crítico =", b_c, "GM/c²")
for eps in [1e-1, 1e-2, 1e-4, 1e-6]:
    bb = b_c*(1+eps)
    al = alpha_exacto(bb)
    print(f"b = b_c(1+{eps:g}):  alpha = {al:.3f} rad = {al/(2*np.pi):.2f} vueltas")

bs = b_c*(1 + np.logspace(-8, -1, 100))
al = np.array([alpha_exacto(x) for x in bs])
plt.figure(figsize=(6, 4))
plt.semilogx(bs/b_c - 1, al)
plt.xlabel(r"$b/b_c-1$"); plt.ylabel(r"$\hat\alpha$ [rad]")
plt.title("Divergencia de la deflexión cerca de la esfera de fotones"); plt.show()
""")

md(r"""
## 9. Conclusiones

- La luz sigue geodésicas nulas; en Schwarzschild satisfacen $u''+u=3GMu^2/c^2$.
- A primer orden, la deflexión es $\hat\alpha = 4GM/(c^2b)$, **el doble** de la predicción newtoniana.
- Para el Sol, $\hat\alpha_\odot\approx1.75''$; las observaciones (eclipse de 1919 y, con mucha más precisión, VLBI) confirman la RG.
- La integral exacta muestra que la aproximación débil es excelente para $b\gg GM/c^2$ y que la deflexión diverge en $b_c=3\sqrt3\,GM/c^2$.

### Referencias
- Bert Janssen, *Teoría de la Relatividad General*, Universidad de Granada (2013).
- Sean Carroll, *Spacetime and Geometry*, Addison Wesley (2004).
- David Tong, *Lectures on General Relativity*, <http://www.damtp.cam.ac.uk/user/tong/gr.html>.
- F. W. Dyson, A. S. Eddington, C. Davidson, *Phil. Trans. R. Soc. A* **220**, 291 (1920).
""")

nb.cells = C
nb.metadata["kernelspec"] = {"display_name": "Python 3", "language": "python", "name": "python3"}
nbf.write(nb, "deflexion_luz_schwarzschild.ipynb")
