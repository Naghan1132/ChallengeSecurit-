import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Fonction pour l'onglet Accueil
def accueil():
    st.title("Application de Cybersécurité")
    st.write("""
        Bienvenue sur notre application de cybersécurité. Cette application vous permet d'analyser et de visualiser des données de sécurité informatique.
        """)

# Fonction pour l'onglet Dashboard
def dashboard():
    st.title("Dashboard")
    st.write("Voici quelques graphiques et indicateurs :")

    # Exemple de graphique à barres
    st.subheader("Graphique à barres")
    data = pd.DataFrame({
        'Catégorie': ['A', 'B', 'C', 'D'],
        'Valeurs': [20, 30, 40, 50]
    })
    st.bar_chart(data.set_index('Catégorie'))

    # Exemple de graphique linéaire
    st.subheader("Graphique linéaire")
    np.random.seed(0)
    df = pd.DataFrame(np.random.randn(10, 2), columns=['A', 'B'])
    st.line_chart(df)

    # Exemple de tableau
    st.subheader("Tableau de données")
    st.write(data)

# Fonction pour l'onglet Machine Learning
def machine_learning():
    st.title("Machine Learning")
    st.write("""
        Dans cet onglet, vous pourriez mettre en œuvre votre code de détection d'adresses IP malveillantes en utilisant des algorithmes de machine learning.
        """)

def main():
    st.sidebar.title("Navigation")
    pages = ["Accueil", "Dashboard", "Machine Learning"]
    selection = st.sidebar.radio("Aller à", pages)

    if selection == "Accueil":
        accueil()
    elif selection == "Dashboard":
        dashboard()
    elif selection == "Machine Learning":
        machine_learning()

if __name__ == "__main__":
    main()
