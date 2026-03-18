"""
vue/composants.py
Composants d'affichage Streamlit pour l'application Micromaisons.
Chaque fonction rend un élément visuel autonome.
"""

from __future__ import annotations

import streamlit as st
import pandas as pd

from model.data import Micromaison, MICROMAISONS, PRESETS_CALCULATEUR
from model.calculateur import (
    ResultatCalcul,
    OBJECTIF_LOGEMENT,
    MOYENNE_SUISSE,
    ECHELLE_LABELS,
)


# ═══════════════════════════════════════════════════════════════════════════
#  HERO HEADER
# ═══════════════════════════════════════════════════════════════════════════

def render_hero():
    """En-tête principal de l'application."""
    st.html("""
    <div class="hero-header">
        <div class="hero-badge">🌿 Société à 2000 watts · HaLege Suisse</div>
        <h1>Efficacité Énergétique<br>des Micromaisons</h1>
        <p>
            Comparez la consommation énergétique de différentes formes d'habitat léger
            et calculez votre propre bilan selon le concept de la société à 2000 watts.
        </p>
    </div>
    """)


# ═══════════════════════════════════════════════════════════════════════════
#  NAVIGATION
# ═══════════════════════════════════════════════════════════════════════════

def render_tabs():
    """Onglets de navigation principaux."""
    return st.tabs([
        "📋  Fiches habitats",
        "🔢  Calculateur 2000W",
        "📊  Comparatif",
    ])


# ═══════════════════════════════════════════════════════════════════════════
#  ONGLET 1 — FICHES HABITATS
# ═══════════════════════════════════════════════════════════════════════════

def render_selecteur_habitat() -> str:
    """Sélecteur de type d'habitat. Retourne l'id sélectionné."""
    ids = [m.id for m in MICROMAISONS]
    labels = [f"{m.icone}  {m.nom}" for m in MICROMAISONS]

    current_id = st.session_state.get("habitat_selectionne", ids[0])
    default_label = labels[ids.index(current_id)] if current_id in ids else labels[0]

    choix_label = st.pills(
        "Choisir un habitat",
        options=labels,
        default=default_label,
        label_visibility="collapsed",
        key="selecteur_habitat",
    )
    if choix_label is None:
        choix_label = default_label
    return ids[labels.index(choix_label)]


def render_fiche_habitat(m: Micromaison):
    """Affiche la fiche complète d'un habitat."""

    # ── Titre + Description
    st.html(f"""
    <div class="card">
        <div class="card-header">
            <div class="card-icon">{m.icone}</div>
            <div>
                <p class="card-subtitle">{m.sous_titre} · {m.annee}</p>
                <h3 class="card-title">{m.nom}</h3>
            </div>
        </div>
        <p style="color: var(--text-muted); font-size: 0.92rem; line-height: 1.6; margin: 0;">
            {m.description}
        </p>
    </div>
    """)

    # ── Résultat Watt + Données clé
    col_watt, col_info = st.columns([1, 1.5])

    with col_watt:
        _render_watt_card(m.consommation_watts, m.comparaison)

    with col_info:
        _render_donnees_cle(m)

    # ── Matériaux + Énergie
    col_mat, col_nrj = st.columns(2)

    with col_mat:
        _render_materiaux(m)

    with col_nrj:
        _render_approvisionnement(m)


def _render_watt_card(watts: float, comparaison: str):
    couleur = _couleur_watts(watts)
    st.html(f"""
    <div class="card" style="text-align:center;">
        <div class="watt-display">
            <p class="watt-number" style="color: {couleur};">{int(watts)}</p>
            <p class="watt-unit">Watts par personne</p>
            <span class="watt-label">≈ {comparaison}</span>
        </div>
        {_render_gauge_html(watts)}
    </div>
    """)


def _render_donnees_cle(m: Micromaison):
    rows = [
        ("Surface habitable", f"{m.surface_habitable_m2} m²"),
        ("Surface au sol", f"{m.surface_sol_m2} m²"),
        ("Dimensions", m.dimensions),
        ("Poids", f"{m.poids_tonnes} t"),
        ("Occupants", m.occupants),
        ("Mobilité", m.mobilite),
    ]
    rows_html = ""
    for label, value in rows:
        rows_html += f"""
        <div class="data-row">
            <span class="data-label">{label}</span>
            <span class="data-value" style="max-width:60%; text-align:right;">{value}</span>
        </div>"""

    st.html(f"""
    <div class="card">
        <h4 style="font-family: 'DM Serif Display', serif; margin: 0 0 1rem 0; font-size: 1.1rem;">
            Données clé
        </h4>
        {rows_html}
    </div>
    """)


def _render_materiaux(m: Micromaison):
    mat_rows = ""
    for mat in m.materiaux:
        mat_rows += f"""
        <div style="padding: 0.5rem 0; border-bottom: 1px solid var(--border);">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span class="data-label" style="font-weight:500;">{mat.composant}</span>
                <span class="mat-badge">U = {mat.valeur_u} {mat.unite}</span>
            </div>
            <p style="font-size:0.78rem; color:var(--text-light); margin:0.2rem 0 0 0; line-height:1.4;">
                {mat.description}
            </p>
        </div>"""

    st.html(f"""
    <div class="card">
        <h4 style="font-family: 'DM Serif Display', serif; margin: 0 0 0.8rem 0; font-size: 1.1rem;">
            🧱 Matériaux principaux
        </h4>
        {mat_rows}
    </div>
    """)


def _render_approvisionnement(m: Micromaison):
    if not m.approvisionnement:
        return
    a = m.approvisionnement

    if a.couverture_solaire_pct >= 70:
        sol_color, sol_bg = "#4CAF50", "rgba(76,175,80,0.1)"
    elif a.couverture_solaire_pct >= 40:
        sol_color, sol_bg = "#FFC107", "rgba(255,193,7,0.1)"
    else:
        sol_color, sol_bg = "#FF5722", "rgba(255,87,34,0.1)"

    st.html(f"""
    <div class="card">
        <h4 style="font-family: 'DM Serif Display', serif; margin: 0 0 0.8rem 0; font-size: 1.1rem;">
            ⚡ Approvisionnement en énergie
        </h4>
        <div class="data-row">
            <span class="data-label">🔥 Chauffage</span>
            <span class="data-value" style="max-width:55%; text-align:right; font-size:0.82rem;">
                {a.chauffage}
            </span>
        </div>
        <div class="data-row">
            <span class="data-label">💧 Eau chaude</span>
            <span class="data-value" style="max-width:55%; text-align:right; font-size:0.82rem;">
                {a.eau_chaude}
            </span>
        </div>
        <div class="data-row">
            <span class="data-label">⚡ Électricité</span>
            <span class="data-value">{int(a.consommation_electricite_kwh)} kWh/an</span>
        </div>
        <div class="data-row">
            <span class="data-label">🔋 Détail</span>
            <span class="data-value" style="max-width:60%; text-align:right; font-size:0.78rem; color:var(--text-muted);">
                {a.detail_electricite}
            </span>
        </div>
        <div style="margin-top:0.8rem; padding:0.7rem 1rem; background:{sol_bg}; border-radius:8px;
                    display:flex; justify-content:space-between; align-items:center;">
            <span style="font-size:0.88rem;">☀️ Couverture solaire</span>
            <span style="font-weight:700; color:{sol_color}; font-size:1.1rem;">
                {int(a.couverture_solaire_pct)}%
            </span>
        </div>
    </div>
    """)


# ═══════════════════════════════════════════════════════════════════════════
#  ONGLET 2 — CALCULATEUR
# ═══════════════════════════════════════════════════════════════════════════

def render_presets() -> str | None:
    """Boutons de chargement des presets. Retourne l'id si cliqué."""
    st.html("""
    <p style="font-size:0.88rem; color:var(--text-muted); margin-bottom:0.5rem;">
        ⚡ Charger les valeurs d'un habitat existant :
    </p>
    """)

    cols = st.columns(len(MICROMAISONS))
    for i, m in enumerate(MICROMAISONS):
        with cols[i]:
            if st.button(
                f"{m.icone} {m.nom.split()[0]}",
                key=f"preset_{m.id}",
                width='stretch',
            ):
                return m.id
    return None


def render_calculateur_form() -> dict:
    """Formulaire du calculateur 2000W. Retourne les valeurs saisies."""

    st.html("""
    <div class="card" style="border-left: 4px solid var(--primary);">
        <h4 style="font-family: 'DM Serif Display', serif; margin: 0 0 0.3rem 0;">
            Calculateur Énergie Primaire
        </h4>
        <p style="color: var(--text-muted); font-size: 0.88rem; margin: 0;">
            Saisissez vos consommations annuelles pour obtenir votre note d'efficacité
            énergétique résidentielle et la consommation de votre ménage par personne.
        </p>
    </div>
    """)

    # Preset values from session_state
    p = st.session_state.get("preset_values", {})

    chauffage_options = [
        "Bois de hêtre (kg)",
        "Bois d'épicéa/sapin (kg)",
        "Gaz (propane/butane) en kWh",
        "Pompe à chaleur (kWh élec.)",
        "Chauffage électrique (kWh)",
    ]
    chauffage_idx = 0
    if p.get("type_chauffage") in chauffage_options:
        chauffage_idx = chauffage_options.index(p["type_chauffage"])

    elec_options = ["Éco-courant / Solaire", "Standard (mix réseau)"]
    elec_idx = 0
    if p.get("type_elec") in elec_options:
        elec_idx = elec_options.index(p["type_elec"])

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("##### 👥 Logement")
        nb_occupants = st.number_input(
            "👤 Habitants du ménage",
            min_value=1, max_value=10,
            value=p.get("nb_occupants", 1),
            step=1,
            key="calc_nb_occ",
        )
        type_chauffage = st.selectbox(
            "🔥 Type de chauffage",
            options=chauffage_options,
            index=chauffage_idx,
            key="calc_type_chauffage",
        )
        quantite_chauffage = st.number_input(
            "📏 Quantité chauffage/an",
            min_value=0.0, max_value=50000.0,
            value=float(p.get("quantite_chauffage", 1125.0)),
            step=50.0,
            help="En kg pour le bois, en kWh pour gaz/électricité",
            key="calc_qte_chauffage",
        )

    with col2:
        st.markdown("##### 💧 Eau chaude & Électricité")
        kwh_eau_chaude_gaz = st.number_input(
            "Eau chaude — gaz (kWh/an)",
            min_value=0.0, max_value=10000.0,
            value=float(p.get("kwh_eau_chaude_gaz", 142.0)),
            step=10.0,
            key="calc_ec_gaz",
        )
        kwh_eau_chaude_elec = st.number_input(
            "Eau chaude — élec. (kWh/an)",
            min_value=0.0, max_value=10000.0,
            value=float(p.get("kwh_eau_chaude_elec", 0.0)),
            step=10.0,
            key="calc_ec_elec",
        )
        kwh_electricite = st.number_input(
            "⚡ Électricité ménage (kWh/an)",
            min_value=0.0, max_value=50000.0,
            value=float(p.get("kwh_electricite", 430.0)),
            step=50.0,
            key="calc_elec",
        )

    type_elec = st.radio(
        "☀️ Type d'électricité",
        options=elec_options,
        index=elec_idx,
        horizontal=True,
        key="calc_type_elec",
    )

    return {
        "nb_occupants": nb_occupants,
        "type_chauffage": type_chauffage,
        "quantite_chauffage": quantite_chauffage,
        "kwh_eau_chaude_gaz": kwh_eau_chaude_gaz,
        "kwh_eau_chaude_elec": kwh_eau_chaude_elec,
        "kwh_electricite": kwh_electricite,
        "type_elec": type_elec,
    }


def render_resultat_calcul(resultat: ResultatCalcul):
    """Affiche le résultat du calcul 2000W."""

    col_res, col_echelle = st.columns([1, 1])

    with col_res:
        st.html(f"""
        <div class="card" style="border-top: 4px solid {resultat.couleur};">
            <p style="font-size: 0.78rem; font-weight: 600; letter-spacing: 0.08em;
                      color: var(--text-light); text-transform: uppercase; margin: 0 0 0.8rem 0;">
                Note de l'habitation
            </p>
            <div style="display: flex; align-items: center; justify-content: center;
                        gap: 0.8rem; margin-bottom: 0.8rem;">
                <span style="font-family: 'DM Serif Display', serif; font-size: 2.8rem;
                             font-weight: 400; color: {resultat.couleur}; line-height: 1;">
                    {resultat.label_court}
                </span>
                <span style="font-size: 0.88rem; color: var(--text-muted); max-width: 180px;
                             line-height: 1.4;">
                    {resultat.label}
                </span>
            </div>
            <div style="display: flex; gap: 1rem; margin-bottom: 0.5rem;">
                <div style="flex: 1; background: {resultat.couleur}18; border-radius: 10px;
                            padding: 0.9rem; text-align: center;">
                    <p style="font-size: 0.75rem; color: var(--text-muted); margin: 0 0 0.3rem 0;">
                        Par personne
                    </p>
                    <p style="font-family: 'DM Serif Display', serif; font-size: 2rem;
                              color: {resultat.couleur}; margin: 0; line-height: 1;">
                        {resultat.watts_par_personne}
                    </p>
                    <p style="font-size: 0.75rem; color: var(--text-muted); margin: 0.2rem 0 0 0;">
                        W / personne
                    </p>
                </div>
                <div style="flex: 1; background: rgba(139,168,52,0.06); border-radius: 10px;
                            padding: 0.9rem; text-align: center;">
                    <p style="font-size: 0.75rem; color: var(--text-muted); margin: 0 0 0.3rem 0;">
                        Total ménage
                    </p>
                    <p style="font-family: 'DM Serif Display', serif; font-size: 2rem;
                              color: var(--text-main); margin: 0; line-height: 1;">
                        {resultat.watts_foyer}
                    </p>
                    <p style="font-size: 0.75rem; color: var(--text-muted); margin: 0.2rem 0 0 0;">
                        W total
                    </p>
                </div>
            </div>
            {_render_gauge_html(resultat.watts_par_personne)}
            <p style="text-align:center; font-size:0.82rem; color:var(--text-light); margin-top:0.5rem;">
                Énergie primaire totale : {resultat.energie_primaire_kwh:,.0f} kWh/an
            </p>
        </div>
        """)

    with col_echelle:
        _render_echelle(resultat)


def _render_echelle(resultat: ResultatCalcul):
    """Échelle de référence 2000 watts."""
    rows_html = ""
    prev_seuil = 0
    for seuil, label, note, couleur in ECHELLE_LABELS:
        actif = prev_seuil <= resultat.watts_par_personne < seuil
        if seuil == 420 and resultat.watts_par_personne < 420:
            actif = True

        bg = f"{couleur}18" if actif else "transparent"
        fw = "700" if actif else "400"
        indicator = " ◀" if actif else ""

        rows_html += f"""
        <div class="data-row" style="background:{bg}; padding: 0.5rem 0.8rem; border-radius: 6px; margin: 2px 0;">
            <span class="data-label" style="font-weight:{fw};">
                <span style="color:{couleur}; font-weight:700; min-width:35px; display:inline-block;">{note}</span>
                {label}
            </span>
            <span class="data-value">
                {'<' if seuil < 2000 else '>'} {seuil} W{indicator}
            </span>
        </div>"""
        prev_seuil = seuil

    st.html(f"""
    <div class="card">
        <h4 style="font-family: 'DM Serif Display', serif; margin: 0 0 1rem 0; font-size: 1rem;">
            Échelle de référence
        </h4>
        {rows_html}
        <p style="font-size:0.75rem; color:var(--text-light); margin-top:0.8rem; line-height:1.5;">
            La société à 2000 W répartit la consommation mondiale équitablement.
            L'objectif résidentiel est de <strong>420 W/personne</strong>, soit ~1/3 du budget total.
        </p>
    </div>
    """)


# ═══════════════════════════════════════════════════════════════════════════
#  ONGLET 3 — COMPARATIF
# ═══════════════════════════════════════════════════════════════════════════

def render_comparatif():
    """Affiche le comparatif complet de tous les habitats."""

    st.html("""
    <div class="card" style="border-left: 4px solid var(--primary);">
        <h4 style="font-family: 'DM Serif Display', serif; margin: 0 0 0.3rem 0;">
            Comparatif des habitats
        </h4>
        <p style="color: var(--text-muted); font-size: 0.88rem; margin: 0;">
            Vue d'ensemble de l'efficacité énergétique selon la société à 2000 watts.
        </p>
    </div>
    """)

    # Barres de comparaison
    max_watts = max(m.consommation_watts for m in MICROMAISONS)
    bar_max = max(max_watts, 600)

    for m in MICROMAISONS:
        pct = min(m.consommation_watts / bar_max * 100, 100)
        couleur = _couleur_watts(m.consommation_watts)
        objectif_pct = OBJECTIF_LOGEMENT / bar_max * 100
        check = "✅" if m.consommation_watts <= OBJECTIF_LOGEMENT else ""

        st.html(f"""
        <div class="card" style="padding: 1rem 1.2rem;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem;">
                <div style="display:flex; align-items:center; gap:0.6rem;">
                    <span style="font-size:1.5rem;">{m.icone}</span>
                    <div>
                        <span style="font-weight:600; font-size:0.95rem;">{m.nom}</span>
                        <span style="font-size:0.78rem; color:var(--text-light); margin-left:0.4rem;">
                            {m.surface_habitable_m2} m²
                        </span>
                    </div>
                </div>
                <div style="text-align:right;">
                    <span style="font-weight:700; color:{couleur}; font-size:1.3rem;">
                        {int(m.consommation_watts)} W
                    </span>
                    <span style="font-size:0.85rem; margin-left:0.3rem;">{check}</span>
                </div>
            </div>
            <div style="width:100%; height:12px; background:#f0f0ec; border-radius:6px; overflow:hidden; position:relative;">
                <div style="width:{pct}%; height:100%; background:{couleur}; border-radius:6px;
                     transition: width 0.6s ease;"></div>
                <div style="position:absolute; left:{objectif_pct}%; top:0; width:2px; height:100%;
                     background:rgba(0,0,0,0.3);"></div>
            </div>
            <div style="display:flex; justify-content:space-between; margin-top:0.35rem;
                        font-size:0.73rem; color:var(--text-light);">
                <span>{m.occupants} · {m.mobilite.split(',')[0].split('.')[0]}</span>
                <span>Solaire : {int(m.approvisionnement.couverture_solaire_pct) if m.approvisionnement else 0}%</span>
            </div>
        </div>
        """)

    # Graphique natif Streamlit
    st.html('<div class="section-title">Consommation par habitat</div>')

    df_chart = pd.DataFrame({
        "Habitat": [m.nom for m in MICROMAISONS],
        "Watts/personne": [m.consommation_watts for m in MICROMAISONS],
    }).set_index("Habitat")

    st.bar_chart(df_chart, color="#8BA834", horizontal=True)

    # Tableau récapitulatif
    st.html('<div class="section-title">Résumé approvisionnement</div>')

    tableau_data = []
    for m in MICROMAISONS:
        if m.donnees_energie:
            d = m.donnees_energie
            tableau_data.append({
                "Habitat": f"{m.icone} {m.nom}",
                "Bois hêtre (kg)": d.bois_hetre_kg,
                "Bois sapin (kg)": d.bois_sapin_kg,
                "Gaz propane (kWh)": d.gaz_propane_kwh,
                "Gaz butane (kWh)": d.gaz_butane_kwh,
                "Élec. solaire (kWh)": d.electricite_solaire_kwh,
                "Élec. réseau (kWh)": d.electricite_reseau_kwh,
                "Résultat (W/pers.)": m.consommation_watts,
            })

    df = pd.DataFrame(tableau_data)
    st.dataframe(
        df,
        width='stretch',
        hide_index=True,
        column_config={
            "Résultat (W/pers.)": st.column_config.ProgressColumn(
                "Résultat (W/pers.)",
                format="%d W",
                min_value=0,
                max_value=600,
            ),
        },
    )

    # Explication
    st.html("""
    <div class="card" style="background: rgba(139, 168, 52, 0.04); border-color: rgba(139, 168, 52, 0.2);">
        <h4 style="font-family: 'DM Serif Display', serif; margin: 0 0 0.5rem 0; font-size: 1rem; color: var(--primary-dark);">
            Qu'est-ce que la société à 2000 watts ?
        </h4>
        <p style="font-size: 0.88rem; color: var(--text-muted); line-height: 1.65; margin: 0;">
            Le concept prend la consommation mondiale réelle d'énergie (2010) et la répartit
            équitablement entre tous les habitants de la terre. Si l'on réduit simultanément la part
            fossile, le mode de vie actuel peut être maintenu écologiquement. Les trois secteurs
            — logement, mobilité, industrie & services — représentent chacun environ 1/3 des 2000 W.
            La valeur cible pour le logement est de <strong>420 watts par personne</strong>.
        </p>
    </div>
    """)


# ═══════════════════════════════════════════════════════════════════════════
#  FOOTER
# ═══════════════════════════════════════════════════════════════════════════

def render_footer():
    """Pied de page."""
    st.html("""
    <div class="footer">
        <p>
            Données : <a href="https://www.habitat-leger.ch" target="_blank">habitat-leger.ch</a>
            · Association HaLege Suisse · Verein Kleinwohnformen Schweiz
        </p>
        <p>
            "Fact Sheets Kleinwohnformen", Juillet 2020 · Traduction 2022 HaLege
        </p>
    </div>
    """)


# ═══════════════════════════════════════════════════════════════════════════
#  HELPERS
# ═══════════════════════════════════════════════════════════════════════════

def _couleur_watts(watts: float) -> str:
    if watts < 420:
        return "#4CAF50"
    elif watts < 700:
        return "#8BC34A"
    elif watts < 1000:
        return "#FFC107"
    elif watts < 1300:
        return "#FF9800"
    elif watts < 1600:
        return "#FF5722"
    else:
        return "#E53935"


def _render_gauge_html(watts: float) -> str:
    pct = min(watts / 2000 * 100, 100)
    objectif_pct = OBJECTIF_LOGEMENT / 2000 * 100

    return f"""
    <div class="gauge-container">
        <div class="gauge-bar">
            <div class="gauge-marker" style="left: {pct}%;" data-label="{int(watts)} W"></div>
            <div style="position:absolute; left:{objectif_pct}%; top:-4px; width:2px; height:22px;
                 background:rgba(0,0,0,0.3); border-radius:1px;"
                 title="Objectif 420W"></div>
        </div>
        <div class="gauge-labels">
            <span>0 W</span>
            <span>420 W<br><small style="color:var(--primary);">objectif</small></span>
            <span>1000 W</span>
            <span>2000 W</span>
        </div>
    </div>
    """
