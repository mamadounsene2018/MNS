# African Stock Market Financial Analysis

Une application complète d'analyse financière des sociétés cotées en bourse en Afrique.

## 📊 Description

Cette application permet d'analyser les sociétés cotées sur les principales bourses africaines, incluant:

- **JSE** (Johannesburg Stock Exchange) - Afrique du Sud
- **NSE** (Nigerian Stock Exchange) - Nigeria  
- **NSE** (Nairobi Securities Exchange) - Kenya
- **BRVM** (Bourse Régionale des Valeurs Mobilières) - Afrique de l'Ouest
- **CSE** (Casablanca Stock Exchange) - Maroc
- **EGX** (Egyptian Exchange) - Égypte

## ✨ Fonctionnalités

### 1. Récupération de Données
- Téléchargement de données historiques pour les actions africaines
- Informations détaillées sur les entreprises
- États financiers (bilan, compte de résultat, flux de trésorerie)
- Vue d'ensemble du marché africain

### 2. Analyse Financière
- **Ratios de rentabilité**: ROE, ROA, marge bénéficiaire
- **Ratios de liquidité**: ratio de liquidité générale, ratio de liquidité immédiate
- **Ratios d'endettement**: ratio d'endettement, couverture des intérêts
- **Ratios de valorisation**: P/E, P/B, rendement du dividende
- **Croissance**: croissance des bénéfices et du chiffre d'affaires

### 3. Analyse Technique
- Moyennes mobiles (SMA, EMA)
- Indicateurs de momentum (RSI, MACD)
- Bandes de Bollinger
- Identification des tendances
- Niveaux de support et de résistance

### 4. Visualisation
- Graphiques de prix historiques
- Graphiques en chandeliers
- Moyennes mobiles
- Distribution des rendements
- Matrices de corrélation
- Indicateurs techniques (RSI, MACD)
- Comparaison de performances

## 🚀 Installation

### Prérequis
- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### Installation des dépendances

```bash
pip install -r requirements.txt
```

Les dépendances principales incluent:
- pandas: manipulation de données
- numpy: calculs numériques
- yfinance: récupération de données financières
- matplotlib & seaborn: visualisation
- requests & beautifulsoup4: scraping web

## 📖 Utilisation

### Exemple 1: Analyse de base d'une action

```python
from african_stock_analysis import StockDataFetcher, FinancialRatios, TrendAnalyzer

# Initialiser le récupérateur de données
fetcher = StockDataFetcher()

# Récupérer les données pour MTN Group (Afrique du Sud)
stock_data = fetcher.get_stock_data('MTN.JO', period='1y')
stock_info = fetcher.get_stock_info('MTN.JO')

# Analyser les ratios financiers
ratios = FinancialRatios(stock_info)
print(ratios.get_valuation_summary())

# Analyser la tendance
analyzer = TrendAnalyzer(stock_data)
print(analyzer.get_analysis_summary())
```

### Exemple 2: Analyse comparative

```python
from african_stock_analysis import StockDataFetcher, ChartGenerator

fetcher = StockDataFetcher()

# Récupérer des données pour plusieurs actions
stocks = {
    'MTN Group': 'MTN.JO',
    'Safaricom': 'SCOM.NR',
    'Vodacom': 'VOD.JO'
}

stocks_data = fetcher.get_multiple_stocks(list(stocks.values()), period='6mo')

# Créer un graphique comparatif
chart_gen = ChartGenerator()
chart_gen.plot_comparative_performance(stocks_data, title="Comparaison Télécom Afrique")
```

### Exemple 3: Vue d'ensemble du marché

```python
from african_stock_analysis import StockDataFetcher

fetcher = StockDataFetcher()

# Obtenir la liste des actions africaines disponibles
stocks = fetcher.list_available_stocks()
for name, symbol in stocks.items():
    print(f"{name}: {symbol}")

# Vue d'ensemble du marché
overview = fetcher.get_african_market_overview()
print(overview)
```

## 📁 Structure du Projet

```
MNS/
├── src/
│   └── african_stock_analysis/
│       ├── __init__.py
│       ├── data/
│       │   ├── __init__.py
│       │   └── stock_data.py          # Récupération de données
│       ├── analysis/
│       │   ├── __init__.py
│       │   ├── financial_ratios.py    # Calcul de ratios
│       │   └── trend_analysis.py      # Analyse technique
│       ├── visualization/
│       │   ├── __init__.py
│       │   └── charts.py              # Génération de graphiques
│       └── utils/
│           ├── __init__.py
│           └── helpers.py             # Fonctions utilitaires
├── examples/
│   ├── example_1_basic_analysis.py
│   ├── example_2_comparative_analysis.py
│   └── example_3_market_overview.py
├── requirements.txt
├── .gitignore
└── README.md
```

## 🎯 Exemples d'Utilisation

Le dossier `examples/` contient des exemples complets:

1. **example_1_basic_analysis.py**: Analyse de base d'une action
2. **example_2_comparative_analysis.py**: Comparaison de plusieurs actions
3. **example_3_market_overview.py**: Vue d'ensemble du marché

Pour exécuter un exemple:

```bash
python examples/example_1_basic_analysis.py
```

## 📈 Actions Pré-configurées

L'application inclut des symboles boursiers pour les principales entreprises africaines:

### Afrique du Sud (JSE)
- Naspers (NPN.JO)
- MTN Group (MTN.JO)
- Sasol (SOL.JO)
- Standard Bank (SBK.JO)
- Shoprite (SHP.JO)
- Anglo American (AGL.JO)
- FirstRand (FSR.JO)
- Vodacom (VOD.JO)

### Nigeria (NSE)
- Dangote Cement (DANGCEM.LG)
- Guaranty Trust Bank (GUARANTY.LG)
- Zenith Bank (ZENITHBANK.LG)

### Kenya (NSE)
- Safaricom (SCOM.NR)
- Equity Bank (EQBNK.NR)

### Égypte (EGX)
- Commercial International Bank (COMI.CA)

### Maroc (CSE)
- Attijariwafa Bank (ATW.CS)

## 🛠️ API Reference

### StockDataFetcher
```python
# Récupérer des données historiques
get_stock_data(symbol, period='1y', interval='1d')

# Obtenir des informations sur l'action
get_stock_info(symbol)

# Récupérer les états financiers
get_financial_statements(symbol)

# Vue d'ensemble du marché
get_african_market_overview()
```

### FinancialRatios
```python
# Ratios de valorisation
get_pe_ratio()
get_pb_ratio()

# Ratios de rentabilité
get_roe()
get_roa()
get_profit_margin()

# Ratios de liquidité
get_current_ratio()
get_quick_ratio()

# Obtenir tous les ratios
get_all_ratios()
```

### TrendAnalyzer
```python
# Moyennes mobiles
calculate_sma(period=20)
calculate_ema(period=20)

# Indicateurs
calculate_rsi(period=14)
calculate_macd()
calculate_bollinger_bands()

# Analyse
identify_trend()
get_momentum_score()
get_analysis_summary()
```

### ChartGenerator
```python
# Graphiques de prix
plot_price_history(stock_data)
plot_candlestick(stock_data)

# Analyse technique
plot_moving_averages(stock_data, periods=[20, 50, 200])
plot_rsi(stock_data, rsi_values)

# Comparaisons
plot_comparative_performance(stocks_data)
plot_correlation_matrix(stocks_data)
```

## 🔍 Notes Importantes

- Les données sont récupérées via Yahoo Finance, qui peut avoir des limitations pour certaines bourses africaines
- Certains symboles boursiers peuvent ne pas être disponibles ou à jour
- Les connexions Internet sont requises pour récupérer les données
- Les graphiques nécessitent un environnement avec affichage graphique

## 📝 Contribution

Les contributions sont les bienvenues! N'hésitez pas à:
- Signaler des bugs
- Suggérer de nouvelles fonctionnalités
- Ajouter de nouvelles actions africaines
- Améliorer la documentation

## 📄 Licence

Ce projet est sous licence open source.

## 👥 Auteur

MNS - Application d'analyse financière pour les marchés boursiers africains

---

**Note**: Cette application est à des fins éducatives et d'information uniquement. Elle ne constitue pas un conseil en investissement.
