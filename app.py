import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Fonction pour générer un KPI
def generate_kpi():
    kpi_value = np.random.randint(100, 1000)
    return kpi_value

# Fonction pour générer un graphique camembert avec Seaborn
def generate_pie_chart(background=False):
    labels = ['Deny', 'Permit']
    sizes = [np.random.randint(20, 80), np.random.randint(20, 80)]
    colors = ['#C70039', '#7FDF70']
    plt.figure(figsize=(6, 6))
    sns.set(style="whitegrid")
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    if not background:
        plt.gca().set_facecolor('none')
    return plt

# Fonction pour générer le top 5 des ips sources
def generate_top_ips():
    ips = [f"192.168.1.{i}" for i in range(1, 6)]
    counts = np.random.randint(10, 100, size=5)
    top_ips_df = pd.DataFrame({'IP Source': ips, 'Nombre de connexions': counts})
    return top_ips_df

# Fonction pour générer un graphique de répartition des ports
def generate_port_distribution(background=False):
    ports = [f"Port {i}" for i in range(1, 6)]
    counts = np.random.randint(10, 100, size=5)
    port_df = pd.DataFrame({'Port': ports, 'Nombre de connexions': counts})
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Port', y='Nombre de connexions', data=port_df, palette='Blues', hue='Port', dodge=False, legend=False)
    plt.xlabel('Ports')
    plt.ylabel('Nombre de connexions')
    plt.title('Répartition des connexions par port')
    if not background:
        plt.gca().set_facecolor('none')
    return plt

def generate_ml_data():
    ip_source = [f"192.168.1.{i}" for i in range(1, 11)]
    ip_destination = [f"10.0.0.{i}" for i in range(1, 11)]
    ports = [f"Port {i}" for i in range(1, 11)]
    access = np.random.choice(['Deny', 'Permit'], size=10)
    rules = [f"Rule {i}" for i in range(1, 11)]
    clusters = np.random.choice(['Dangereux', 'Inoffensif'], size=10)
    ml_data_df = pd.DataFrame({'IP Source': ip_source, 'IP Destination': ip_destination,
                               'Port': ports, 'Accès': access, 'Règle': rules, 'Cluster': clusters})
    return ml_data_df

def dashboard():
    st.title("Dashboard")

    # Filtres de date
    start_date = st.sidebar.date_input("Date de début", value=pd.to_datetime('2024-01-01'))
    end_date = st.sidebar.date_input("Date de fin", value=pd.to_datetime('2024-12-31'))

    # Filtrer par IP destination
    destination_ip = st.sidebar.text_input("Filtrer par IP destination")

    # Afficher le KPI et le graphique camembert sur la même ligne
    col1, col2 = st.columns([2, 3])

    with col1:
        # Afficher le KPI
        kpi_value = generate_kpi()
        st.subheader("Nombre de requêtes")
        st.write(f"La valeur du KPI  : {kpi_value}")

    with col2:
        # Afficher le graphique camembert
        st.subheader("Répartition DENY/Permit")
        pie_chart = generate_pie_chart(background=True)
        st.pyplot(pie_chart)

    # Afficher le top 5 des IP sources
    st.subheader("Top 5 des IP Sources")
    top_ips_df = generate_top_ips()
    st.table(top_ips_df)

    # Afficher la répartition des ports
    st.subheader("Répartition des connexions par port")
    port_distribution = generate_port_distribution(background=True)
    st.pyplot(port_distribution)

def machine_learning():
    st.title("Machine Learning")

    # Générer des données pour l'apprentissage automatique
    ml_data_df = generate_ml_data()

    # Afficher la grande table avec les données d'apprentissage automatique
    # Coloration conditionnelle pour toute la ligne
    def color_row(row):
        if row['Cluster'] == 'Dangereux':
            return ['background-color: orange'] * len(row)
        else:
            return [''] * len(row)

    styled_ml_data_df = ml_data_df.style.apply(color_row, axis=1)
    st.dataframe(styled_ml_data_df, height=600)

def main():
    tabs = ["Dashboard", "Machine Learning"]
    selected_tab = st.sidebar.selectbox("Sélectionnez un onglet", tabs)
    if selected_tab == "Dashboard":
        dashboard()
    elif selected_tab == "Machine Learning":
        machine_learning()

if __name__ == "__main__":
    main()
