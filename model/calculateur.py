"""
model/calculateur.py
Logique de calcul de la société à 2000 watts.

Facteurs de conversion basés sur le calculateur
http://2000-watt-wohnen.ch/energierechner/
et les données des fiches KWF / HaLege.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


# ─── Constantes société 2000 watts ──────────────────────────────────────────

OBJECTIF_2000W_TOTAL = 2000          # W total par personne
OBJECTIF_LOGEMENT = 420              # W part résidentielle (soll)
MOYENNE_SUISSE = 1300                # W moyenne suisse actuelle (ist)

# Les 3 secteurs : logement (~1/3), mobilité (~1/3), industrie+services (~1/3)
PART_LOGEMENT_PCT = 1 / 3


# ─── Facteurs de conversion en énergie primaire ────────────────────────────
# Sources: 2000-watt-wohnen.ch + données fiches KWF
# Facteurs calibrés pour correspondre aux résultats du calculateur officiel.

# Bois (Stückholz) - énergie renouvelable, facteur primaire très faible
FACTEUR_BOIS_HETRE_KWH_PAR_KG = 4.0    # ~4 kWh/kg pour bois de hêtre sec
FACTEUR_BOIS_SAPIN_KWH_PAR_KG = 4.3    # ~4.3 kWh/kg pour épicéa/sapin
FACTEUR_PRIMAIRE_BOIS = 0.05           # facteur énergie primaire bois (renouvelable)

# Gaz
FACTEUR_PRIMAIRE_GAZ = 1.30            # facteur énergie primaire gaz propane/butane

# Électricité
FACTEUR_PRIMAIRE_ELEC_STANDARD = 2.89  # mix suisse standard
FACTEUR_PRIMAIRE_ELEC_VERTE = 0.14     # éco-courant / solaire

# Heures par année
HEURES_PAR_AN = 8760


class TypeElectricite(Enum):
    STANDARD = "Standard (mix réseau)"
    VERTE = "Éco-courant / Solaire"


class TypeChauffage(Enum):
    BOIS_HETRE = "Bois de hêtre (stères)"
    BOIS_SAPIN = "Bois d'épicéa/sapin (kg)"
    GAZ = "Gaz (propane/butane) en kWh"
    POMPE_CHALEUR = "Pompe à chaleur (kWh élec.)"
    ELECTRIQUE = "Chauffage électrique (kWh)"


@dataclass
class ResultatCalcul:
    """Résultat du calcul 2000 watts."""
    watts_par_personne: float
    watts_foyer: float           # total watts pour l'ensemble du ménage
    energie_primaire_kwh: float
    label: str
    label_court: str
    couleur: str
    atteint_objectif: bool
    pourcentage_objectif: float  # % de l'objectif 420W


def _convertir_chauffage_kwh_primaire(
    type_chauffage: TypeChauffage,
    quantite: float,
) -> float:
    """Convertit la consommation de chauffage en kWh d'énergie primaire."""
    if type_chauffage == TypeChauffage.BOIS_HETRE:
        # quantité en kg
        kwh_utile = quantite * FACTEUR_BOIS_HETRE_KWH_PAR_KG
        return kwh_utile * FACTEUR_PRIMAIRE_BOIS
    elif type_chauffage == TypeChauffage.BOIS_SAPIN:
        kwh_utile = quantite * FACTEUR_BOIS_SAPIN_KWH_PAR_KG
        return kwh_utile * FACTEUR_PRIMAIRE_BOIS
    elif type_chauffage == TypeChauffage.GAZ:
        return quantite * FACTEUR_PRIMAIRE_GAZ
    elif type_chauffage == TypeChauffage.POMPE_CHALEUR:
        # COP moyen ~3, donc kWh élec. * facteur primaire
        return quantite * FACTEUR_PRIMAIRE_ELEC_STANDARD
    elif type_chauffage == TypeChauffage.ELECTRIQUE:
        return quantite * FACTEUR_PRIMAIRE_ELEC_STANDARD
    return 0.0


def _convertir_eau_chaude_kwh_primaire(
    kwh_gaz: float = 0,
    kwh_elec: float = 0,
    type_elec: TypeElectricite = TypeElectricite.STANDARD,
) -> float:
    """Convertit la consommation eau chaude en kWh d'énergie primaire."""
    primaire_gaz = kwh_gaz * FACTEUR_PRIMAIRE_GAZ
    facteur_elec = (
        FACTEUR_PRIMAIRE_ELEC_VERTE
        if type_elec == TypeElectricite.VERTE
        else FACTEUR_PRIMAIRE_ELEC_STANDARD
    )
    primaire_elec = kwh_elec * facteur_elec
    return primaire_gaz + primaire_elec


def _label_energie(watts: float) -> tuple[str, str, str]:
    """Retourne (label, label_court, couleur) selon le niveau."""
    if watts < 420:
        return "Objectif 2000 watts atteint +++", "+++", "#4CAF50"
    elif watts < 700:
        return "Objectif 2000 watts à portée ++", "++", "#8BC34A"
    elif watts < 1000:
        return "Habitat énergétiquement exemplaire +", "+", "#FFC107"
    elif watts < 1300:
        return "Moyenne suisse =", "=", "#FF9800"
    elif watts < 1600:
        return "Consommation supérieure à la moyenne −", "−", "#FF5722"
    elif watts < 1900:
        return "Consommation élevée −−", "−−", "#E91E63"
    else:
        return "Consommation très élevée −−−", "−−−", "#B71C1C"


def calculer_2000_watts(
    nb_occupants: int,
    type_chauffage: TypeChauffage,
    quantite_chauffage: float,
    kwh_eau_chaude_gaz: float,
    kwh_eau_chaude_elec: float,
    kwh_electricite: float,
    type_electricite: TypeElectricite,
) -> ResultatCalcul:
    """
    Calcul principal : convertit les consommations annuelles
    en watts d'énergie primaire par personne.
    """
    # 1. Énergie primaire chauffage
    ep_chauffage = _convertir_chauffage_kwh_primaire(type_chauffage, quantite_chauffage)

    # 2. Énergie primaire eau chaude
    ep_eau_chaude = _convertir_eau_chaude_kwh_primaire(
        kwh_gaz=kwh_eau_chaude_gaz,
        kwh_elec=kwh_eau_chaude_elec,
        type_elec=type_electricite,
    )

    # 3. Énergie primaire électricité
    facteur_elec = (
        FACTEUR_PRIMAIRE_ELEC_VERTE
        if type_electricite == TypeElectricite.VERTE
        else FACTEUR_PRIMAIRE_ELEC_STANDARD
    )
    ep_electricite = kwh_electricite * facteur_elec

    # Total énergie primaire annuelle
    ep_total = ep_chauffage + ep_eau_chaude + ep_electricite

    # Conversion en watts
    # W = kWh/an ÷ 8760 h/an × 1000
    watts_foyer = ep_total / HEURES_PAR_AN * 1000
    watts = watts_foyer / max(nb_occupants, 1)

    label, label_court, couleur = _label_energie(watts)

    return ResultatCalcul(
        watts_par_personne=round(watts),
        watts_foyer=round(watts_foyer),
        energie_primaire_kwh=round(ep_total, 1),
        label=label,
        label_court=label_court,
        couleur=couleur,
        atteint_objectif=watts < OBJECTIF_LOGEMENT,
        pourcentage_objectif=round(watts / OBJECTIF_LOGEMENT * 100, 1),
    )


# ─── Échelle de référence pour l'affichage ─────────────────────────────────

ECHELLE_LABELS = [
    (420, "Objectif 2000W atteint", "+++", "#4CAF50"),
    (700, "Objectif à portée", "++", "#8BC34A"),
    (1000, "Exemplaire", "+", "#FFC107"),
    (1300, "Moyenne Suisse", "=", "#FF9800"),
    (1600, "Supérieur à la moyenne", "−", "#FF5722"),
    (1900, "Élevé", "−−", "#E91E63"),
    (2000, "Très élevé", "−−−", "#B71C1C"),
]
