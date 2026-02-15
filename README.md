# Modelisation-simulation

Simulation de systèmes **mono-serveur** (jusqu’à **1 000 000 clients**).

## Objectifs
- Simuler des files d’attente mono-serveur
- Étudier l’impact de la **charge** sur les performances du système
- Comparer différents modèles (M/M/1, G/M/1, M/G/1)

## Indicateurs de performance analysés
- **Temps de réponse** (temps passé dans le système)
- **Temps d’attente** (dans la file)
- **Taux d’occupation du serveur** : \( \rho = \lambda / \mu \)

---

## 1) Simulation du système M/M/1
### Description
- Arrivées : loi exponentielle de paramètre **λ**
- Service : loi exponentielle de paramètre **μ**

### Travail Fait
- Faire varier **λ** de **0.1 à 0.9**
- Pour chaque valeur de λ, calculer :
  - Temps de réponse moyen
  - Taux d’occupation du serveur \( \rho = \lambda / \mu \)
  - Temps d’attente moyen dans la file
- Représenter les résultats sous forme de **graphiques**

---

## 2) Simulation du système G/M/1
### Description
- Arrivées : loi **générale** (au choix)
- Service : loi exponentielle (**μ**)

### Travail Fait
- Reprendre la même étude que pour le **M/M/1**
- Comparer les résultats avec ceux du **M/M/1**

---

## 3) Simulation du système M/G/1
### Description
- Arrivées : loi exponentielle (**λ**)
- Service : loi **générale** (au choix)

### Travail Fait
- Étudier les mêmes indicateurs que dans les deux cas précédents :
  - Temps de réponse moyen
  - Taux d’occupation \( \rho \)
  - Temps d’attente moyen
- Comparer les résultats entre les modèles

---
