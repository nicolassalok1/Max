"""
app.py
Point d'entrée de l'application Streamlit.
Architecture MVC :
    model/       → Données et logique métier
    vue/         → Composants d'affichage Streamlit
    controller/  → Orchestration du flux applicatif
"""

import streamlit as st
from controller.app_controller import AppController


def main():
    st.set_page_config(
        page_title="Micromaisons — Efficacité Énergétique",
        page_icon="🏡",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
    controller = AppController()
    controller.run()


if __name__ == "__main__":
    main()
