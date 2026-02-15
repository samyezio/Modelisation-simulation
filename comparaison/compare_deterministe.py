import numpy as np
import matplotlib.pyplot as plt

TAUX_SERVICE = 1.0
NB_CLIENTS = 1_000_000
NB_REPETITIONS = 3
TAUX_ARRIVEE = np.arange(0.1, 1.0, 0.1)

def simuler(entree_gen, service_gen, n):
    ARRIVEES = np.cumsum(entree_gen(n))
    SERVICES = service_gen(n)
    DEBUTS = np.zeros(n)
    FINS = np.zeros(n)

    for i in range(1, n):
        DEBUTS[i] = max(ARRIVEES[i], FINS[i - 1])
        FINS[i] = DEBUTS[i] + SERVICES[i]

    ATTENTES = DEBUTS - ARRIVEES
    REPONSES = FINS - ARRIVEES

    return REPONSES.mean(), ATTENTES.mean()

MM1_RESULTATS = {"lambda": [], "response_time": [], "wait_time": [], "rho": []}

for TAUX in TAUX_ARRIVEE:
    REPONSES, ATTENTES = [], []
    for _ in range(NB_REPETITIONS):
        R, W = simuler(
            entree_gen=lambda n: np.random.exponential(1 / TAUX, n),
            service_gen=lambda n: np.random.exponential(1 / TAUX_SERVICE, n),
            n=NB_CLIENTS
        )
        REPONSES.append(R)
        ATTENTES.append(W)
    MM1_RESULTATS["lambda"].append(TAUX)
    MM1_RESULTATS["response_time"].append(np.mean(REPONSES))
    MM1_RESULTATS["wait_time"].append(np.mean(ATTENTES))
    MM1_RESULTATS["rho"].append(TAUX / TAUX_SERVICE)

GM1_RESULTATS = {"lambda": [], "response_time": [], "wait_time": [], "rho": []}

for TAUX in TAUX_ARRIVEE:
    REPONSES, ATTENTES = [], []
    for _ in range(NB_REPETITIONS):
        R, W = simuler(
            entree_gen=lambda n: np.full(n, 1 / TAUX),
            service_gen=lambda n: np.random.exponential(1 / TAUX_SERVICE, n),
            n=NB_CLIENTS
        )
        REPONSES.append(R)
        ATTENTES.append(W)
    GM1_RESULTATS["lambda"].append(TAUX)
    GM1_RESULTATS["response_time"].append(np.mean(REPONSES))
    GM1_RESULTATS["wait_time"].append(np.mean(ATTENTES))
    GM1_RESULTATS["rho"].append(TAUX / TAUX_SERVICE)

MG1_RESULTATS = {"lambda": [], "response_time": [], "wait_time": [], "rho": []}

for TAUX in TAUX_ARRIVEE:
    REPONSES, ATTENTES = [], []
    for _ in range(NB_REPETITIONS):
        R, W = simuler(
            entree_gen=lambda n: np.random.exponential(1 / TAUX, n),
            service_gen=lambda n: np.full(n, 1 / TAUX_SERVICE),
            n=NB_CLIENTS
        )
        REPONSES.append(R)
        ATTENTES.append(W)
    MG1_RESULTATS["lambda"].append(TAUX)
    MG1_RESULTATS["response_time"].append(np.mean(REPONSES))
    MG1_RESULTATS["wait_time"].append(np.mean(ATTENTES))
    MG1_RESULTATS["rho"].append(TAUX / TAUX_SERVICE)

def tracer(resultats, prefixe):
    plt.plot(resultats["lambda"], resultats["response_time"],
              linewidth=2, label=f"{prefixe} - Temps de réponse")
    plt.plot(resultats["lambda"], resultats["wait_time"],
              linewidth=2, label=f"{prefixe} - Temps d'attente")
    plt.plot(resultats["lambda"], resultats["rho"],
              linewidth=2, label=f"{prefixe} - Taux d'occupations")

plt.figure(figsize=(12, 8), facecolor='black')
tracer(MM1_RESULTATS, "M/M/1")
tracer(GM1_RESULTATS, "G/M/1_det ")
tracer(MG1_RESULTATS, "M/G/1_det ")
plt.title("📊 Comparaison des modèles M/M/1, G/M/1_det et M/G/1_det", fontsize=16, color='white')
plt.xlabel("Taux d'arrivée λ", fontsize=14, color='white')
plt.ylabel("Valeur moyenne", fontsize=14, color='white')
plt.tick_params(colors='white')
plt.grid(True, linestyle=':', color='gray', alpha=0.5)
plt.legend(facecolor='black', edgecolor='white', fontsize=12)
plt.tight_layout()
plt.savefig("comparaison_det.png", dpi=300, facecolor='black')
plt.show()
