# ============================================
# Ejercicios de Distribución Normal con Python
# ============================================

from scipy.stats import norm

# ------------------------------------------------------
# Funciones auxiliares
# ------------------------------------------------------
def prob_between(mu, sigma, a, b):
    """Probabilidad de que X ~ N(mu, sigma^2) esté entre a y b."""
    return norm.cdf(b, loc=mu, scale=sigma) - norm.cdf(a, loc=mu, scale=sigma)

def prob_greater(mu, sigma, x):
    """Probabilidad de que X > x."""
    return 1 - norm.cdf(x, loc=mu, scale=sigma)

def prob_less(mu, sigma, x):
    """Probabilidad de que X < x."""
    return norm.cdf(x, loc=mu, scale=sigma)


# ------------------------------------------------------
# 1) Temperaturas en junio
# ------------------------------------------------------
mu1 = 23.0      # media
sigma1 = 5.0    # desviación típica
a1, b1 = 21.0, 27.0

prob_21_27 = prob_between(mu1, sigma1, a1, b1)
dias_mes = 30
dias_esperados_21_27 = prob_21_27 * dias_mes

print("1) Temperaturas en junio (μ=23, σ=5):")
print(f"   Probabilidad entre {a1}º y {b1}º: {prob_21_27:.6f}")
print(f"   Días esperados en el mes: {dias_esperados_21_27:.3f} días\n")


# ------------------------------------------------------
# 2) Pesos de estudiantes
# ------------------------------------------------------
n_students = 500
mu2 = 70.0
sigma2 = 3.0

# a) Entre 60 y 75 kg
p_60_75 = prob_between(mu2, sigma2, 60, 75)
count_60_75 = p_60_75 * n_students

# b) Más de 90 kg
p_more_90 = prob_greater(mu2, sigma2, 90)
count_more_90 = p_more_90 * n_students

# c) Menos de 64 kg
p_less_64 = prob_less(mu2, sigma2, 64)
count_less_64 = p_less_64 * n_students

print("2) Pesos (n=500, μ=70, σ=3):")
print(f"   Entre 60 kg y 75 kg → Prob = {p_60_75:.6f} → {count_60_75:.1f} estudiantes")
print(f"   Más de 90 kg        → Prob = {p_more_90:.6e} → {count_more_90:.6f} estudiantes")
print(f"   Menos de 64 kg      → Prob = {p_less_64:.6f} → {count_less_64:.1f} estudiantes\n")


# ------------------------------------------------------
# 3) Percentiles de Z ~ N(0,1)
# ------------------------------------------------------
percentiles = [0.25, 0.5, 0.95, 0.99]
z_values = {p: norm.ppf(p) for p in percentiles}

print("3) Percentiles de Z ~ N(0,1):")
for p, z in z_values.items():
    print(f"   Percentil {int(p*100)} (p={p}): z = {z:.6f}")
