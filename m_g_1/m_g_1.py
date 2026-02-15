import numpy as np
import matplotlib.pyplot as plt

# Paramètres constants
TAUX_SERVICE = 1.0
NB_CLIENTS = 1_000_000
NB_REPETS = 3

LAMBDA_LISTE = np.arange(0.1, 1.0, 0.1)

# Simulation M/G/1 (temps de service ~ Gamma)
def simulation_mg1(taux_arrivee, taux_service, n):
    temps_arrivees = np.cumsum(np.random.exponential(1 / taux_arrivee, n))
    # Loi générale : Gamma avec même moyenne que Exp(1/μ) mais distrubution diffrenete (variance diff)
    # Service suivent une loi Gamma (plus générale que l'exponentielle)
    temps_services = np.random.gamma(shape=3, scale=1 / (3 * taux_service), size=n)
    temps_debut = np.zeros(n)
    temps_fin = np.zeros(n)

    for i in range(1, n):
        temps_debut[i] = max(temps_arrivees[i], temps_fin[i - 1])
        temps_fin[i] = temps_debut[i] + temps_services[i]

    attentes = temps_debut - temps_arrivees
    reponses = temps_fin - temps_arrivees

    return reponses.mean(), attentes.mean()

donnees = {
    "lambda": [],
    "temps_reponse": [],
    "temps_attente": [],
    "occupation": []
}

for taux_lambda in LAMBDA_LISTE:
    liste_reponses, liste_attentes = [], []
    for _ in range(NB_REPETS):
        moy_reponse, moy_attente = simulation_mg1(taux_lambda, TAUX_SERVICE, NB_CLIENTS)
        liste_reponses.append(moy_reponse)
        liste_attentes.append(moy_attente)

    donnees["lambda"].append(taux_lambda)
    donnees["temps_reponse"].append(np.mean(liste_reponses))
    donnees["temps_attente"].append(np.mean(liste_attentes))
    donnees["occupation"].append(taux_lambda / TAUX_SERVICE)

plt.figure(figsize=(10, 6), facecolor='black')

plt.plot(donnees["lambda"], donnees["temps_reponse"],
         color='cyan', linestyle='-', marker='o', linewidth=2, label="Temps de réponse moyen")

plt.plot(donnees["lambda"], donnees["temps_attente"],
         color='lime', linestyle='--', marker='s', linewidth=2, label="Temps d'attente moyen")

plt.plot(donnees["lambda"], donnees["occupation"],
         color='orange', linestyle='-.', marker='^', linewidth=2, label="Taux d'occupation (ρ = λ/μ)")

plt.title("📊 Résultats de la simulation M/G/1", fontsize=16, color='white')
plt.xlabel("Taux d'arrivée λ", fontsize=14, color='white')
plt.ylabel("Valeur moyenne", fontsize=14, color='white')
plt.tick_params(colors='white')
plt.grid(True, linestyle=':', color='gray', alpha=0.5)
plt.legend(facecolor='black', edgecolor='white', fontsize=12)
plt.tight_layout()
plt.savefig("simulation_mg1.png", dpi=300, facecolor='black')
plt.show()
