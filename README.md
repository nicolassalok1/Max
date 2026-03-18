# 🏡 Micromaisons — Efficacité Énergétique

Application Streamlit pour visualiser et calculer l'efficacité énergétique des micromaisons selon le concept de la **société à 2000 watts**.

Basé sur les fiches d'information de [HaLege Suisse](https://www.habitat-leger.ch) et du [Verein Kleinwohnformen Schweiz](https://www.kleinwohnformen.ch).

## Architecture MVC

```
├── app.py                  # Point d'entrée Streamlit
├── model/                  # Données et logique métier
│   ├── data.py            # Modèles de données des habitats
│   └── calculateur.py     # Logique de calcul 2000 watts
├── vue/                    # Composants d'affichage
│   ├── theme.py           # CSS personnalisé
│   └── composants.py      # Composants UI Streamlit
├── controller/             # Orchestration
│   └── app_controller.py  # Contrôleur principal
├── .streamlit/
│   └── config.toml        # Configuration Streamlit
└── requirements.txt
```

## Installation

```bash
pip install -r requirements.txt
```

## Lancement

```bash
streamlit run app.py
```

## Fonctionnalités

- **Fiches habitats** : consultation détaillée de 5 types d'habitat (Mini Maison, Tiny House, Yourte, Roulotte, Appartement témoin)
- **Calculateur 2000W** : estimation de l'énergie primaire par personne à partir de 3 données
- **Comparatif** : vue d'ensemble avec barres de progression et tableau récapitulatif

## Sources

- Données : *Fact Sheets Kleinwohnformen*, Juillet 2020
- Traduction 2022 : Association HaLege Suisse
- Calculateur : [2000-watt-wohnen.ch/energierechner](http://2000-watt-wohnen.ch/energierechner/)
