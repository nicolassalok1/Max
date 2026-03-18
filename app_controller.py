"""
controller/app_controller.py
Contrôleur principal de l'application.
Orchestre les interactions entre le modèle (données + calcul)
et la vue (composants Streamlit).
"""

from __future__ import annotations

import streamlit as st

from model.data import get_micromaison_by_id, MICROMAISONS, PRESETS_CALCULATEUR
from model.calculateur import (
    calculer_2000_watts,
    TypeChauffage,
    TypeElectricite,
    ResultatCalcul,
)
from vue.composants import (
    render_hero,
    render_tabs,
    render_selecteur_habitat,
    render_fiche_habitat,
    render_presets,
    render_calculateur_form,
    render_resultat_calcul,
    render_comparatif,
    render_footer,
)
from vue.theme import inject_css


# ─── Mapping formulaire → enum ──────────────────────────────────────────────

_MAP_CHAUFFAGE = {
    "Bois de hêtre (kg)": TypeChauffage.BOIS_HETRE,
    "Bois d'épicéa/sapin (kg)": TypeChauffage.BOIS_SAPIN,
    "Gaz (propane/butane) en kWh": TypeChauffage.GAZ,
    "Pompe à chaleur (kWh élec.)": TypeChauffage.POMPE_CHALEUR,
    "Chauffage électrique (kWh)": TypeChauffage.ELECTRIQUE,
}

_MAP_ELEC = {
    "Éco-courant / Solaire": TypeElectricite.VERTE,
    "Standard (mix réseau)": TypeElectricite.STANDARD,
}


class AppController:
    """Contrôleur principal qui pilote le flux de l'application."""

    def __init__(self):
        self._init_session_state()

    def _init_session_state(self):
        """Initialise l'état de session Streamlit."""
        if "habitat_selectionne" not in st.session_state:
            st.session_state.habitat_selectionne = MICROMAISONS[0].id
        if "resultat_calcul" not in st.session_state:
            st.session_state.resultat_calcul = None
        if "preset_values" not in st.session_state:
            st.session_state.preset_values = {}

    def run(self):
        """Point d'entrée principal — exécute le cycle complet MVC."""
        # 1. Thème
        inject_css()

        # 2. Header
        render_hero()

        # 3. Onglets
        tab_fiches, tab_calcul, tab_comparatif = render_tabs()

        # 4. Contenu
        with tab_fiches:
            self._handle_fiches()

        with tab_calcul:
            self._handle_calculateur()

        with tab_comparatif:
            self._handle_comparatif()

        # 5. Footer
        render_footer()

    # ─── Handlers par section ───────────────────────────────────────────

    def _handle_fiches(self):
        """Gère l'onglet Fiches habitats."""
        habitat_id = render_selecteur_habitat()
        st.session_state.habitat_selectionne = habitat_id

        micromaison = get_micromaison_by_id(habitat_id)
        if micromaison:
            render_fiche_habitat(micromaison)

    def _handle_calculateur(self):
        """Gère l'onglet Calculateur 2000W avec presets."""

        # Presets : charger les valeurs d'un habitat existant
        preset_id = render_presets()
        if preset_id and preset_id in PRESETS_CALCULATEUR:
            st.session_state.preset_values = PRESETS_CALCULATEUR[preset_id].copy()
            st.rerun()

        st.markdown("---")

        # Formulaire
        form_data = render_calculateur_form()

        # Bouton calcul
        col_btn, col_reset = st.columns([3, 1])
        with col_btn:
            calc_clicked = st.button(
                "⚡  Calculer l'énergie primaire",
                use_container_width=True,
                type="primary",
            )
        with col_reset:
            if st.button("🔄 Reset", use_container_width=True):
                st.session_state.preset_values = {}
                st.session_state.resultat_calcul = None
                st.rerun()

        if calc_clicked:
            resultat = self._calculer(form_data)
            st.session_state.resultat_calcul = resultat

        # Résultat
        if st.session_state.resultat_calcul:
            st.markdown("")
            render_resultat_calcul(st.session_state.resultat_calcul)

    def _handle_comparatif(self):
        """Gère l'onglet Comparatif."""
        render_comparatif()

    # ─── Logique métier ─────────────────────────────────────────────────

    def _calculer(self, form_data: dict) -> ResultatCalcul:
        """Convertit les données du formulaire et appelle le modèle de calcul."""
        type_chauffage = _MAP_CHAUFFAGE.get(
            form_data["type_chauffage"], TypeChauffage.BOIS_HETRE
        )
        type_elec = _MAP_ELEC.get(
            form_data["type_elec"], TypeElectricite.VERTE
        )

        return calculer_2000_watts(
            nb_occupants=form_data["nb_occupants"],
            type_chauffage=type_chauffage,
            quantite_chauffage=form_data["quantite_chauffage"],
            kwh_eau_chaude_gaz=form_data["kwh_eau_chaude_gaz"],
            kwh_eau_chaude_elec=form_data["kwh_eau_chaude_elec"],
            kwh_electricite=form_data["kwh_electricite"],
            type_electricite=type_elec,
        )
