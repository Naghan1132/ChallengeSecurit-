import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Fonction pour générer un KPI
def generate_kpi(data):
    kpi_value = data['Status'].count()  # Compter le nombre de requêtes
    return kpi_value

# Fonction pour générer un graphique camembert avec Seaborn
def generate_pie_chart(data, background=False):
    deny_count = data[data['Status'] == 'DENY']['Status'].count()
    permit_count = data[data['Status'] == 'PERMIT']['Status'].count()
    labels = ['Deny', 'Permit']
    sizes = [deny_count, permit_count]
    colors = ['#C70039', '#7FDF70']
    plt.figure(figsize=(6, 6))
    sns.set(style="whitegrid")
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    if not background:
        plt.gca().set_facecolor('none')
    return plt

# Fonction pour générer le top 5 des ips sources
def generate_top_ips(data):
    top_ips = data['SRC'].value_counts().head(5).reset_index()
    top_ips.columns = ['IP Source', 'Nombre de connexions']
    return top_ips

# Fonction pour générer un graphique de répartition des ports
def generate_port_distribution(data, background=False):
    port_counts = data['SPT'].value_counts().head(5).reset_index()
    port_counts.columns = ['Port', 'Nombre de connexions']
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Port', y='Nombre de connexions', data=port_counts, palette='Blues', hue='Port', dodge=False, legend=False)
    plt.xlabel('Ports')
    plt.ylabel('Nombre de connexions')
    plt.title('Répartition des connexions par port')
    if not background:
        plt.gca().set_facecolor('none')
    return plt

def generate_month_distribution(data, background=False):
    month_counts = data['Mois'].value_counts().reset_index()
    month_counts.columns = ['Mois', 'Nombre d\'événements']
    
    # Liste des mois dans l'ordre désiré
    month_order = ['Jan', 'Fev', 'Mar', 'Avr', 'Mai', 'Juin', 'Juil', 'Aou', 'Sep', 'Oct', 'Nov', 'Dec']
    
    # Créer un DataFrame pour tous les mois avec une fréquence de 0
    all_months = pd.DataFrame({'Mois': month_order})
    month_counts = pd.merge(all_months, month_counts, on='Mois', how='left')
    month_counts['Nombre d\'événements'] = month_counts['Nombre d\'événements'].fillna(0)
    
    # Trier par ordre des mois
    #month_counts = month_counts.sort_values(by='Mois', key=lambda x: month_order.index(x))
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Mois', y='Nombre d\'événements', data=month_counts, palette='Blues')
    plt.xlabel('Mois')
    plt.ylabel('Nombre d\'événements')
    plt.title('Répartition des événements par mois')
    if not background:
        plt.gca().set_facecolor('none')
    return plt


# Fonction pour générer un graphique de répartition des événements par jour
def generate_day_distribution(data, background=False):
    day_counts = data['Jour'].value_counts().reset_index()
    day_counts.columns = ['Jour', 'Nombre d\'événements']
    day_order = ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim']
    #day_counts = day_counts.sort_values(by='Jour', key=lambda x: day_order.index(x))
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Jour', y='Nombre d\'événements', data=day_counts, palette='Blues')
    plt.xlabel('Jour')
    plt.ylabel('Nombre d\'événements')
    plt.title('Répartition des événements par jour')
    if not background:
        plt.gca().set_facecolor('none')
    return plt

# Fonction pour générer un graphique de répartition des événements par heure
def generate_hour_distribution(data, background=False):
    data['Heure'] = pd.to_datetime(data['Heure'])
    data['Heure'] = data['Heure'].dt.hour
    hour_counts = data['Heure'].value_counts().reset_index()
    hour_counts.columns = ['Heure', 'Nombre d\'événements']
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Heure', y='Nombre d\'événements', data=hour_counts, palette='Blues')
    plt.xlabel('Heure')
    plt.ylabel('Nombre d\'événements')
    plt.title('Répartition des événements par heure de la journée')
    if not background:
        plt.gca().set_facecolor('none')
    return plt

def dashboard(data):
    st.title("Dashboard")

    # Filtrer par plage de dates
    start_date = st.sidebar.date_input("Date de début", pd.to_datetime(data['Time_Stamp']).min())
    end_date = st.sidebar.date_input("Date de fin", pd.to_datetime(data['Time_Stamp']).max())

    # Convert 'Time_Stamp' column to datetime
    data['Time_Stamp'] = pd.to_datetime(data['Time_Stamp'])

    # Filtrer les données en fonction de la plage de dates sélectionnée
    filtered_data = data[(data['Time_Stamp'] >= pd.Timestamp(start_date)) & (data['Time_Stamp'] <= pd.Timestamp(end_date))]

    # Afficher le KPI et le graphique camembert sur la même ligne
    col1, col2 = st.columns([2, 3])

    with col1:
        # Afficher le KPI
        st.subheader("Nombre de requêtes")
        kpi_value = generate_kpi(filtered_data)
        st.write(f"La valeur du KPI : {kpi_value}")

    with col2:
        # Afficher le graphique camembert
        st.subheader("Répartition DENY/Permit")
        pie_chart = generate_pie_chart(filtered_data, background=True)
        st.pyplot(pie_chart)

    # Afficher le top 5 des IP sources
    st.subheader("Top 5 des IP Sources")
    top_ips_df = generate_top_ips(filtered_data)
    st.table(top_ips_df)

    # Afficher la répartition des ports
    st.subheader("Répartition des connexions par port")
    port_distribution = generate_port_distribution(filtered_data, background=True)
    st.pyplot(port_distribution)

    # Afficher la répartition des événements par mois
    st.subheader("Répartition des événements par mois")
    month_distribution = generate_month_distribution(filtered_data, background=True)
    st.pyplot(month_distribution)

    # Afficher la répartition des événements par jour
    st.subheader("Répartition des événements par jour")
    day_distribution = generate_day_distribution(filtered_data, background=True)
    st.pyplot(day_distribution)

    # Afficher la répartition des événements par heure
    st.subheader("Répartition des événements par heure de la journée")
    hour_distribution = generate_hour_distribution(filtered_data, background=True)
    st.pyplot(hour_distribution)
# Assurez-vous de mettre à jour la fonction main() également
def machine_learning():
    st.title("Machine Learning")

    # Générer des données pour l'apprentissage automati que
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
    data = pd.read_csv("final_proto_TS.csv")  # Charger vos données à partir du fichier CSV
    pages = {
        "Dashboard": dashboard,
        "Machine Learning": machine_learning
    }
    selected_page = st.sidebar.radio("Sélectionnez une page", list(pages.keys()))
    pages[selected_page](data)

if __name__ == "__main__":
    main()


