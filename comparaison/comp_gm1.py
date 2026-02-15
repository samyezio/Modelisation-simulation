import numpy as np
import matplotlib.pyplot as plt

# Paramètres généraux
MU = 1.0  # Taux de service
NUM_CUSTOMERS = 1_000_000
REPEATS = 3
LAMBDA_VALUES = np.arange(0.1, 1.0, 0.1)

# Fonction de simulation générique pour les files mono-serveur
def simulate(arrival_gen, service_gen, n):
    arrival_times = np.cumsum(arrival_gen(n))
    service_times = service_gen(n)
    start_times = np.zeros(n)
    end_times = np.zeros(n)

    for i in range(1, n):
        start_times[i] = max(arrival_times[i], end_times[i-1])
        end_times[i] = start_times[i] + service_times[i]

    wait_times = start_times - arrival_times
    response_times = end_times - arrival_times

    return response_times.mean(), wait_times.mean()

results_gm1 = {"lambda": [], "response_time": [], "wait_time": [], "rho": []}

for lmbda in LAMBDA_VALUES:
    responses = []
    waits = []
    for _ in range(REPEATS):
        resp, wait = simulate(
            arrival_gen=lambda n: np.random.gamma(shape=2, scale=1/(2*lmbda), size=n),
            service_gen=lambda n: np.random.exponential(1/MU, n),
            n=NUM_CUSTOMERS
        )
        responses.append(resp)
        waits.append(wait)
    results_gm1["lambda"].append(lmbda)
    results_gm1["response_time"].append(np.mean(responses))
    results_gm1["wait_time"].append(np.mean(waits))
    results_gm1["rho"].append(lmbda / MU)
    
results_gm1_det = {"lambda": [], "response_time": [], "wait_time": [], "rho": []}

for lmbda in LAMBDA_VALUES:
    responses = []
    waits = []
    for _ in range(REPEATS):
        resp, wait = simulate(
            arrival_gen=lambda n: np.full(n, 1/lmbda),
            service_gen=lambda n: np.random.exponential(1/MU, n),
            n=NUM_CUSTOMERS
        )
        responses.append(resp)
        waits.append(wait)
    results_gm1_det["lambda"].append(lmbda)
    results_gm1_det["response_time"].append(np.mean(responses))
    results_gm1_det["wait_time"].append(np.mean(waits))
    results_gm1_det["rho"].append(lmbda / MU)    
    
def plot_results(results, title_prefix):
     plt.plot(results["lambda"], results["response_time"],
             color='cyan', linewidth=2, label=f"{title_prefix} - Temps de réponse")
    
     plt.plot(results["lambda"], results["wait_time"],
             color='lime', linewidth=2,label=f"{title_prefix} - Temps d'attente")
    
     plt.plot(results["lambda"], results["rho"],
             color='orange', linewidth=2, label=f"{title_prefix} - Taux d'occupations")

plt.figure(figsize=(12, 8), facecolor='black')
plot_results(results_gm1, "G/M/1")
plot_results(results_gm1_det, "G/M/1_det ")
plt.title("📊 Comparaison des modèles G/M/1 et G/M/1_det", fontsize=16, color='white')
plt.xlabel("Taux d'arrivée λ", fontsize=14, color='white')
plt.ylabel("Valeur moyenne", fontsize=14, color='white')    
plt.tick_params(colors='white')
plt.grid(True, linestyle=':', color='gray', alpha=0.5)    
plt.legend(facecolor='black', edgecolor='white', fontsize=12)
plt.tight_layout()    
plt.savefig("comp_gm1.png", dpi=300, facecolor='black')
plt.show()     