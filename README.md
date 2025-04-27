# 📊 Portfolio Crisis Analysis

Projet Python réalisé dans le cadre du certificat "Python for Finance".

---

## 🎯 Objectif du projet

Analyser et comparer trois stratégies de portefeuilles sur données réelles (2013–2024) :

- **Equal Weighted** (poids constants)
- **Rolling Max Sharpe** (optimisation du ratio de Sharpe tous les 6 mois)
- **Rolling Min Variance** (minimisation de la variance tous les 6 mois)

Avec un focus particulier sur :
- La performance globale
- La performance pendant la crise du COVID (mars à décembre 2020) pour voir quel portefeuille est plus robuste pendant les crises

---

## 📚 Méthodologie

### 🔹 Données
- Source : Yahoo Finance via `yfinance`
- Actions : 9 grandes entreprises américaines (ex: AAPL, MSFT, NVDA, etc.)
- Fréquence : journalière
- Période : 01/01/2013 au 01/01/2024

### 🔹 Traitement
- Calcul des **log-returns**.
- Suppression des valeurs manquantes.

### 🔹 Backtests Rolling
- **Window size** : 3 ans (756 jours)
- **Test size** : 6 mois (126 jours)
- **Step size** : 6 mois (126 jours)

➡️ À chaque itération :
1. Estimation des poids sur 3 ans de données historiques.
2. Application de ces poids pendant les 6 mois suivants.
3. Avancement de 6 mois.

---

## 🧱 Organisation du code

### 📂 `function/`
- `data_loader.py` : chargement des données.
- `data_analyzer.py` : calcul des returns, corrélations, et graphiques.
- `portfolio.py` : création des portefeuilles Equal, Max Sharpe et Min Variance.
- `backtest.py` : simulation rolling des stratégies.
- `performance_analyzer.py` : comparaison des performances (Sharpe, Volatility, Drawdown).
- `report.py` : sauvegarde des graphiques.

### 📂 `output/`
- Dossier contenant tous les graphiques générés automatiquement (.png).

### 📄 `main.py`
- Script principal orchestrant toutes les étapes : importation, analyse, backtests, et reporting.

---
## 📈 Commentaire sur les résultats

La stratégie **Equal Weighted** est celle qui a offert la meilleure performance globale sur la période 2013–2024 (**+418%**), avec un **Sharpe Ratio élevé de 1.00**, tirant parti du marché haussier.  
La stratégie **Max Sharpe** obtient une performance inférieure (**+182%**), mais montre une bonne capacité à **gérer le risque** pendant la crise du COVID (**Sharpe Ratio de 0.84** contre **0.71** pour Equal Weighted).  
La stratégie **Min Variance** protège efficacement contre la volatilité, mais au prix d’une **forte sous-performance** globale (**+66%**).

Pendant la crise COVID, **Max Sharpe** devient la stratégie la plus adaptée avec le meilleur compromis rendement/risque, tandis que **Equal Weighted** reste robuste et **Min Variance** reste défensif mais peu rentable.

### ✅ Conclusion
- **Equal Weighted** est très efficace sur un horizon long terme.
- **Max Sharpe** surperforme en période de crise.
- **Min Variance** réduit la volatilité mais sacrifie beaucoup de rendement.
