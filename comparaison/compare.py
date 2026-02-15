import numpy as np
import matplotlib.pyplot as plt

# Paramètres généraux
TAUX_SERVICE = 1.0  # Taux de service
NB_CLIENTS = 1_000_000
NB_REPETS = 3
LAMBDA_LISTE = np.arange(0.1, 1.0, 0.1)

# Fonction de simulation générique pour les files mono-serveur
def simulate(arrival_gen, service_gen, n):
    temps_arrivees = np.cumsum(arrival_gen(n))
    temps_services = service_gen(n)
    temps_debut = np.zeros(n)
    temps_fin = np.zeros(n)

    for i in range(1, n):
        temps_debut[i] = max(temps_arrivees[i], temps_fin[i-1])
        temps_fin[i] = temps_debut[i] + temps_services[i]

    attentes = temps_debut - temps_arrivees
    reponses = temps_fin - temps_arrivees

    return reponses.mean(), attentes.mean()

# Simulation de M/M/1
resultats_mm1 = {"lambda": [], "temps_reponse": [], "temps_attente": [], "rho": []}

for taux_lambda in LAMBDA_LISTE:
    liste_reponses = []
    liste_attentes = []
    for _ in range(NB_REPETS):
        moy_reponse, moy_attente = simulate(
            arrival_gen=lambda n: np.random.exponential(1 / taux_lambda, n),
            service_gen=lambda n: np.random.exponential(1 / TAUX_SERVICE, n),
            n=NB_CLIENTS
        )
        liste_reponses.append(moy_reponse)
        liste_attentes.append(moy_attente)
    resultats_mm1["lambda"].append(taux_lambda)
    resultats_mm1["temps_reponse"].append(np.mean(liste_reponses))
    resultats_mm1["temps_attente"].append(np.mean(liste_attentes))
    resultats_mm1["rho"].append(taux_lambda / TAUX_SERVICE)

# Simulation de G/M/1 (arrivées gamma)
resultats_gm1 = {"lambda": [], "temps_reponse": [], "temps_attente": [], "rho": []}

for taux_lambda in LAMBDA_LISTE:
    liste_reponses = []
    liste_attentes = []
    for _ in range(NB_REPETS):
        moy_reponse, moy_attente = simulate(
            arrival_gen=lambda n: np.random.gamma(shape=2, scale=1 / (2 * taux_lambda), size=n),
            service_gen=lambda n: np.random.exponential(1 / TAUX_SERVICE, n),
            n=NB_CLIENTS
        )
        liste_reponses.append(moy_reponse)
        liste_attentes.append(moy_attente)
    resultats_gm1["lambda"].append(taux_lambda)
    resultats_gm1["temps_reponse"].append(np.mean(liste_reponses))
    resultats_gm1["temps_attente"].append(np.mean(liste_attentes))
    resultats_gm1["rho"].append(taux_lambda / TAUX_SERVICE)

# Simulation de M/G/1 (services gamma)
resultats_mg1 = {"lambda": [], "temps_reponse": [], "temps_attente": [], "rho": []}

for taux_lambda in LAMBDA_LISTE:
    liste_reponses = []
    liste_attentes = []
    for _ in range(NB_REPETS):
        moy_reponse, moy_attente = simulate(
            arrival_gen=lambda n: np.random.exponential(1 / taux_lambda, n),
            service_gen=lambda n: np.random.gamma(shape=2, scale=1 / (2 * TAUX_SERVICE), size=n),
            n=NB_CLIENTS
        )
        liste_reponses.append(moy_reponse)
        liste_attentes.append(moy_attente)
    resultats_mg1["lambda"].append(taux_lambda)
    resultats_mg1["temps_reponse"].append(np.mean(liste_reponses))
    resultats_mg1["temps_attente"].append(np.mean(liste_attentes))
    resultats_mg1["rho"].append(taux_lambda / TAUX_SERVICE)

# Fonction de tracé des résultats
def tracer(resultats, titre):
    plt.plot(resultats["lambda"], resultats["temps_reponse"],
             linewidth=2, label=f"{titre} - Temps de réponse")
    
    plt.plot(resultats["lambda"], resultats["temps_attente"],
             linewidth=2, label=f"{titre} - Temps d'attente")
    
    plt.plot(resultats["lambda"], resultats["rho"],
             linewidth=2, label=f"{titre} - Taux d'occupation")

plt.figure(figsize=(12, 8), facecolor='black')
tracer(resultats_mm1, "M/M/1")
tracer(resultats_gm1, "G/M/1")
tracer(resultats_mg1, "M/G/1")
plt.title("📊 Comparaison des modèles M/M/1, G/M/1 et M/G/1", fontsize=16, color='white')
plt.xlabel("Taux d'arrivée λ", fontsize=14, color='white')
plt.ylabel("Valeur moyenne", fontsize=14, color='white')
plt.tick_params(colors='white')
plt.grid(True, linestyle=':', color='gray', alpha=0.5)
plt.legend(facecolor='black', edgecolor='white', fontsize=12)
plt.tight_layout()
plt.savefig("comparaison.png", dpi=300, facecolor='black')
plt.show()
