"""
model/data.py
Données des micromaisons extraites des fiches d'information HaLege / KWF.
Chaque entrée représente un type d'habitat avec ses caractéristiques
physiques, matériaux, approvisionnement énergétique et résultat 2000-Watt.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class Materiau:
    composant: str          # Étage, Mur, Toit, Fenêtres
    description: str
    valeur_u: float         # W/m²·K
    unite: str = "W/m²·K"


@dataclass
class ApprovisionnementEnergie:
    chauffage: str
    eau_chaude: str
    autres_energies: str
    consommation_electricite_kwh: float
    detail_electricite: str
    part_solaire: str
    couverture_solaire_pct: float  # 0-100


@dataclass
class DonneesEnergie:
    bois_hetre_kg: float = 0.0
    bois_sapin_kg: float = 0.0
    gaz_propane_kwh: float = 0.0
    gaz_butane_kwh: float = 0.0
    electricite_solaire_kwh: float = 0.0
    electricite_reseau_kwh: float = 0.0


@dataclass
class Micromaison:
    id: str
    nom: str
    sous_titre: str
    description: str
    icone: str  # emoji

    # Données clé
    surface_habitable_m2: float
    surface_sol_m2: float
    dimensions: str
    poids_tonnes: float
    occupants: str
    nb_occupants_calcul: int  # pour le calcul 2000W
    mobilite: str

    # Matériaux
    materiaux: list[Materiau] = field(default_factory=list)

    # Énergie
    approvisionnement: Optional[ApprovisionnementEnergie] = None
    donnees_energie: Optional[DonneesEnergie] = None

    # Résultat 2000-Watt
    consommation_watts: float = 0.0
    comparaison: str = ""  # ex: "un demi-réfrigérateur"

    # Année de construction
    annee: int = 0


# ─── Base de données des habitats ──────────────────────────────────────────

MICROMAISONS: list[Micromaison] = [
    Micromaison(
        id="mini_maison",
        nom="La Mini Maison",
        sous_titre="Habitat léger",
        description=(
            "Éco-mini maison construite en 2012 selon des principes stricts "
            "de biologie de la construction. Matériaux naturels, faible "
            "consommation d'énergie grise, air intérieur sain. "
            "Complètement autonome en électricité avec toilette sèche."
        ),
        icone="🏡",
        surface_habitable_m2=35,
        surface_sol_m2=51,
        dimensions="3,6 × 12 m + module technique 2,5 × 3 m",
        poids_tonnes=19,
        occupants="1-2 occupants + 1 invité",
        nb_occupants_calcul=1,
        mobilite="Grue + chargeur surbaissé, véhicule d'escorte requis",
        materiaux=[
            Materiau("Sol", "Panneau fibres bois tendre 20 cm, plancher 3 couches, bois massif", 0.16),
            Materiau("Mur", "Fibre souple + panneaux 3 couches, intérieur argile", 0.17),
            Materiau("Toit", "Panneaux fibres 3 couches souples, écologie extensive 60 mm", 0.15),
            Materiau("Fenêtres", "Métal et bois de chêne, triple vitrage", 0.60),
        ],
        approvisionnement=ApprovisionnementEnergie(
            chauffage="Poêle à bois, env. 1,5 stère de hêtre/an",
            eau_chaude="Pompe à chaleur air-eau",
            autres_energies="~11 kg gaz propane (cuisine + eau chaude grand froid)",
            consommation_electricite_kwh=430,
            detail_electricite="Réfrigérateur, pompe à chaleur, ventilation, appareils portables, éclairage",
            part_solaire="Modules PV ~18 m², monocristallins, batterie plomb",
            couverture_solaire_pct=100,
        ),
        donnees_energie=DonneesEnergie(
            bois_hetre_kg=1125,
            gaz_propane_kwh=141.57,
            electricite_solaire_kwh=430,
        ),
        consommation_watts=53,
        comparaison="un demi-réfrigérateur",
        annee=2012,
    ),

    Micromaison(
        id="tiny_house",
        nom="Tiny House",
        sous_titre="Habitat léger",
        description=(
            "Tiny house créée en 2018 par le collectif Winzig. "
            "Dispose d'un permis de conduire, adaptée aux autoroutes. "
            "Ossature bois avec système solaire et isolation performante. "
            "Permis de construire obtenu à Zurich au printemps 2020."
        ),
        icone="🏠",
        surface_habitable_m2=13,
        surface_sol_m2=17,
        dimensions="6,5 × 2,55 m",
        poids_tonnes=3.2,
        occupants="2 personnes",
        nb_occupants_calcul=2,
        mobilite="Remorque catégorie BE (voiture puissante)",
        materiaux=[
            Materiau("Sol", "Plots bois, isolation PU 12 cm, contreplaqué + OSB, sol caoutchouc", 0.17),
            Materiau("Mur", "Poteaux bois, isolation PU 12 cm, contreplaqué bouleau, façade membrane ventilée", 0.18),
            Materiau("Toit", "Poutres bois, isolation PU 12 cm, polycarbonate résistant grêle, contreplaqué bouleau", 0.19),
            Materiau("Fenêtres", "Bois triple vitrage, gaz argon", 0.55),
        ],
        approvisionnement=ApprovisionnementEnergie(
            chauffage="130 L gaz propane/an",
            eau_chaude="Gaz / énergie solaire",
            autres_energies="-",
            consommation_electricite_kwh=180,
            detail_electricite="Réfrigérateur, appareils mobiles, domotique, ventilateur, WLAN, HiFi",
            part_solaire="Modules PV ~4 m², flexibles, batterie lithium moyenne",
            couverture_solaire_pct=100,
        ),
        donnees_energie=DonneesEnergie(
            gaz_propane_kwh=846.59,
            electricite_solaire_kwh=180,
        ),
        consommation_watts=65,
        comparaison="un ordinateur portable en continu",
        annee=2018,
    ),

    Micromaison(
        id="yourte",
        nom="Yourte",
        sous_titre="Habitat léger",
        description=(
            "Modification de la yourte traditionnelle mongole, "
            "située dans l'Entlebuch. Construite principalement "
            "à partir de matières premières renouvelables, "
            "équipée de panneaux solaires. Eau à la ferme voisine."
        ),
        icone="⛺",
        surface_habitable_m2=28,
        surface_sol_m2=28,
        dimensions="Diamètre extérieur 6 m",
        poids_tonnes=1.5,
        occupants="1 personne (espace pour 4)",
        nb_occupants_calcul=1,
        mobilite="Démontable en 1-3 jours par 3 personnes, remorque 3,5 t",
        materiaux=[
            Materiau("Sol", "Contreplaqué, laine de mouton 10 cm, plancher épicéa", 0.40),
            Materiau("Mur", "Tapis laine 3 cm entre draps bio-fibre + feuille anti-pluie", 4.10),
            Materiau("Plafond", "Comme les murs", 3.50),
            Materiau("Fenêtres", "Porte vitrée + fenêtre + dôme plastique 1,5 m", 1.50),
        ],
        approvisionnement=ApprovisionnementEnergie(
            chauffage="Poêle à bois, ~4 stères/an (~3 000 kg hêtre)",
            eau_chaude="Chauffée sur poêle à bois en hiver + sanitaires partagés à 50 m",
            autres_energies="5,5 kg gaz butane/an (cuisine)",
            consommation_electricite_kwh=100,
            detail_electricite="Ordinateur, lampe bureau, 2 LED, station recharge 12V",
            part_solaire="Modules PV ~1 m², monocristallins, petite batterie plomb",
            couverture_solaire_pct=50,
        ),
        donnees_energie=DonneesEnergie(
            bois_hetre_kg=3000,
            gaz_butane_kwh=69.85,
            electricite_solaire_kwh=50,
            electricite_reseau_kwh=50,
        ),
        consommation_watts=109,
        comparaison="un téléviseur ordinaire en continu",
        annee=2015,
    ),

    Micromaison(
        id="roulotte",
        nom="Roulotte",
        sous_titre="Habitat léger",
        description=(
            "Espace de vie reconstruit sur un chariot de cirque "
            "des années 80. Conservation maximale des ressources, "
            "base d'origine conservée, reste construit par le propriétaire. "
            "Située dans la vallée d'Embrach."
        ),
        icone="🚐",
        surface_habitable_m2=17,
        surface_sol_m2=21,
        dimensions="2,5 × 8,2 m",
        poids_tonnes=5,
        occupants="1 personne + 1-2 invités",
        nb_occupants_calcul=1,
        mobilite="Facile à déplacer (ex: tracteur)",
        materiaux=[
            Materiau("Sol", "Bois tendre, XPS 12 cm, tapis antibruit, parquet chêne", 0.21),
            Materiau("Mur", "Laine de bois 8 cm entre panneaux bois tendre, lambris ventilé", 0.85),
            Materiau("Toit", "Laine de roche 6 cm entre panneaux bois tendre", 0.53),
            Materiau("Fenêtres", "Bois triple vitrage", 0.70),
        ],
        approvisionnement=ApprovisionnementEnergie(
            chauffage="Poêle à bois + poêle électrique (absences), ~6 stères sapin/an",
            eau_chaude="Chaudière électrique",
            autres_energies="-",
            consommation_electricite_kwh=1450,
            detail_electricite="Chaudière, réfrigérateur, éclairage, données climat, routeur, chauffage eau",
            part_solaire="Aucun",
            couverture_solaire_pct=0,
        ),
        donnees_energie=DonneesEnergie(
            bois_sapin_kg=3300,
            electricite_reseau_kwh=1450,
        ),
        consommation_watts=522,
        comparaison="un PC bureau + console de jeu en continu",
        annee=1980,
    ),

    Micromaison(
        id="appartement",
        nom="Appartement témoin 2020",
        sous_titre="Suisse 2020",
        description=(
            "Appartement modèle de niveau moyen supérieur, construit en 2020. "
            "Isolation extérieure 20 cm, structure béton. "
            "Pompe à chaleur géothermique, capteurs solaires, "
            "système de ventilation de confort."
        ),
        icone="🏢",
        surface_habitable_m2=45,
        surface_sol_m2=53,
        dimensions="Part prorata de 180 m² (2×1 pers. + 1×2 pers.)",
        poids_tonnes=45,
        occupants="1 personne + 1 lit invité",
        nb_occupants_calcul=1,
        mobilite="Non mobile",
        materiaux=[
            Materiau("Sol", "Isolation XPS 14 cm, béton 25 cm, béton dur 3 cm", 0.23),
            Materiau("Mur", "Laine de roche 20 cm compacte, enduit minéral ext., silicate int.", 0.17),
            Materiau("Toit", "Toit plat végétalisé 10 cm substrat + PIR 10,5 cm, béton", 0.20),
            Materiau("Fenêtres", "Bois-métal triple vitrage", 0.50),
        ],
        approvisionnement=ApprovisionnementEnergie(
            chauffage="Chauffage sol via pompe à chaleur géothermique",
            eau_chaude="Pompe à chaleur + énergie solaire",
            autres_energies="-",
            consommation_electricite_kwh=2000,
            detail_electricite="Réfrigérateur, cuisinière, TV+PS, éclairage, aspirateur, fer, ventilation, domotique, WLAN",
            part_solaire="Capteurs solaires sur toiture",
            couverture_solaire_pct=70,
        ),
        donnees_energie=DonneesEnergie(
            electricite_solaire_kwh=1400,
            electricite_reseau_kwh=600,
        ),
        consommation_watts=302,
        comparaison="deux PC moyens à pleine charge",
        annee=2020,
    ),
]


def get_micromaison_by_id(habitat_id: str) -> Optional[Micromaison]:
    """Retourne une micromaison par son identifiant."""
    for m in MICROMAISONS:
        if m.id == habitat_id:
            return m
    return None


def get_all_ids() -> list[str]:
    """Retourne la liste des identifiants."""
    return [m.id for m in MICROMAISONS]


def get_all_noms() -> list[str]:
    """Retourne la liste des noms."""
    return [m.nom for m in MICROMAISONS]


# ─── Presets calculateur (valeurs d'entrée du site 2000-watt-wohnen.ch) ────

PRESETS_CALCULATEUR: dict[str, dict] = {
    "mini_maison": {
        "nb_occupants": 1,
        "type_chauffage": "Bois de hêtre (kg)",
        "quantite_chauffage": 1125.0,
        "kwh_eau_chaude_gaz": 142.0,
        "kwh_eau_chaude_elec": 0.0,
        "kwh_electricite": 430.0,
        "type_elec": "Éco-courant / Solaire",
    },
    "tiny_house": {
        "nb_occupants": 2,
        "type_chauffage": "Gaz (propane/butane) en kWh",
        "quantite_chauffage": 847.0,
        "kwh_eau_chaude_gaz": 0.0,
        "kwh_eau_chaude_elec": 0.0,
        "kwh_electricite": 180.0,
        "type_elec": "Éco-courant / Solaire",
    },
    "yourte": {
        "nb_occupants": 1,
        "type_chauffage": "Bois de hêtre (kg)",
        "quantite_chauffage": 3000.0,
        "kwh_eau_chaude_gaz": 70.0,
        "kwh_eau_chaude_elec": 0.0,
        "kwh_electricite": 50.0,
        "type_elec": "Standard (mix réseau)",
    },
    "roulotte": {
        "nb_occupants": 1,
        "type_chauffage": "Bois d'épicéa/sapin (kg)",
        "quantite_chauffage": 3300.0,
        "kwh_eau_chaude_gaz": 0.0,
        "kwh_eau_chaude_elec": 0.0,
        "kwh_electricite": 1450.0,
        "type_elec": "Standard (mix réseau)",
    },
    "appartement": {
        "nb_occupants": 1,
        "type_chauffage": "Pompe à chaleur (kWh élec.)",
        "quantite_chauffage": 1200.0,
        "kwh_eau_chaude_gaz": 0.0,
        "kwh_eau_chaude_elec": 400.0,
        "kwh_electricite": 2000.0,
        "type_elec": "Standard (mix réseau)",
    },
}
