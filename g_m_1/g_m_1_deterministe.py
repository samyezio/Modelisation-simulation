import numpy as np
import matplotlib.pyplot as plt

TAUX_SERVICE = 1.0
NB_CLIENTS = 1_000_000
NB_REPETITIONS = 3
TAUX_ARRIVEE = np.arange(0.1, 1.0, 0.1)

def simuler_gm1(taux, mu, n):
    TEMPS_ENTREES = np.full(n, 1 / taux)
    TEMPS_ARRIVEE = np.cumsum(TEMPS_ENTREES)
    TEMPS_SERVICE = np.random.exponential(1 / mu, n)

    TEMPS_DEBUT = np.zeros(n)
    TEMPS_FIN = np.zeros(n)

    for i in range(1, n):
        TEMPS_DEBUT[i] = max(TEMPS_ARRIVEE[i], TEMPS_FIN[i - 1])
        TEMPS_FIN[i] = TEMPS_DEBUT[i] + TEMPS_SERVICE[i]

    ATTENTES = TEMPS_DEBUT - TEMPS_ARRIVEE
    REPONSES = TEMPS_FIN - TEMPS_ARRIVEE

    return REPONSES.mean(), ATTENTES.mean()

GM1_RESULTATS = {"lambda": [], "response_time": [], "wait_time": [], "rho": []}

for TAUX in TAUX_ARRIVEE:
    REPONSES, ATTENTES = [], []
    for _ in range(NB_REPETITIONS):
        R, W = simuler_gm1(TAUX, TAUX_SERVICE, NB_CLIENTS)
        REPONSES.append(R)
        ATTENTES.append(W)

    GM1_RESULTATS["lambda"].append(TAUX)
    GM1_RESULTATS["response_time"].append(np.mean(REPONSES))
    GM1_RESULTATS["wait_time"].append(np.mean(ATTENTES))
    GM1_RESULTATS["rho"].append(TAUX / TAUX_SERVICE)

plt.figure(figsize=(10, 6), facecolor='black')

plt.plot(GM1_RESULTATS["lambda"], GM1_RESULTATS["response_time"],
         color='cyan', linestyle='-', marker='o', linewidth=2, label="M/G/1 - Temps de réponse")

plt.plot(GM1_RESULTATS["lambda"], GM1_RESULTATS["wait_time"],
         color='lime', linestyle='--', marker='s', linewidth=2, label="M/G/1 - Temps d'attente")

plt.plot(GM1_RESULTATS["lambda"], GM1_RESULTATS["rho"],
         color='orange', linestyle='-.', marker='^', linewidth=2, label="Taux d'occupation (ρ = λ/μ)")

plt.title("📊 Résultats de la simulation G/M/1 deterministe", fontsize=16, color='white')
plt.xlabel("Taux d'arrivée λ", fontsize=14, color='white')
plt.ylabel("Valeur moyenne", fontsize=14, color='white')
plt.tick_params(colors='white')
plt.grid(True, linestyle=':', color='gray', alpha=0.5)
plt.legend(facecolor='black', edgecolor='white', fontsize=12)
plt.tight_layout()
plt.savefig("simulation_gm1_deterministe.png", dpi=300, facecolor='black')
plt.show()
