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
def generate_pie_chart(data,ip=None,background=False):
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

def dashboard(data):
    st.title("Dashboard")

    # Filtres de date (si votre dataframe contient une colonne de date)
    start_date = st.sidebar.date_input("Date de début", value=pd.to_datetime('2024-01-01'))
    end_date = st.sidebar.date_input("Date de fin", value=pd.to_datetime('2024-12-31'))

    # Filtrer par IP destination
    destination_ip = st.sidebar.text_input("Filtrer par IP destination")

    # Afficher le KPI et le graphique camembert sur la même ligne
    col1, col2 = st.columns([2, 3])

    with col1:
        # Afficher le KPI
        st.subheader("Nombre de requêtes")
        kpi_value = generate_kpi(data)
        st.write(f"La valeur du KPI : {kpi_value}")

    with col2:
        # Afficher le graphique camembert
        st.subheader("Répartition DENY/Permit")
        pie_chart = generate_pie_chart(data, background=True)
        st.pyplot(pie_chart)

    # Afficher le top 5 des IP sources
    st.subheader("Top 5 des IP Sources")
    top_ips_df = generate_top_ips(data)
    st.table(top_ips_df)

    # Afficher la répartition des ports
    st.subheader("Répartition des connexions par port")
    port_distribution = generate_port_distribution(data, background=True)
    st.pyplot(port_distribution)




def machine_learning(data):
    import seaborn as sns
    import matplotlib.pyplot as plt
    st.title("Machine Learning")

    # Générer des données pour l'apprentissage automatique
    ml_data_df = generate_ml(data)
    print(ml_data_df)

    # Afficher un échantillon des données d'apprentissage automatique
    st.subheader("Échantillon des données d'apprentissage automatique")
    st.dataframe(ml_data_df.sample(15), height=600)

    # Créer le nuage de points avec Seaborn
    plt.figure(figsize=(10, 8))
    
    # Sélection des colonnes pertinentes pour le graphique
    x = ml_data_df['SPT']
    x = x.head(10000)
    y = ml_data_df['Rule']
    y = y.head(10000)
    clusters = ml_data_df['Cluster']
    clusters = clusters.head(10000)
    
    # Utilisation de Seaborn pour le nuage de points avec coloration en fonction des clusters
    sns.scatterplot(x=x, y=y, hue=clusters, palette='viridis', alpha=0.5)
    
    # Ajout de labels et titre
    plt.xlabel('SPT')
    plt.ylabel('Règle')
    plt.title('Nuage de points avec clusters des individus')
    
    plt.legend(title='Cluster')
    
    # Affichage du graphique avec Streamlit
    st.pyplot(plt.gcf())


def generate_ml(data): 
    from sklearn.cluster import KMeans
    from sklearn.preprocessing import StandardScaler

    # Générer des données pour l'apprentissage automatique
    ml_data = data.copy()  # Copie des données pour éviter de modifier les données originales

    features = data[['SPT']]

    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)
    print(scaled_features)

    kmeans = KMeans(n_clusters=2, random_state=42)  # Spécifiez le nombre de clusters souhaité
    kmeans.fit(scaled_features)
    
    cluster_labels = kmeans.labels_

    data['Cluster'] = cluster_labels

    return data
    
    
    # # Séparation des caractéristiques et de la cible
    # X = ml_data.drop(columns=['Status'])  # Caractéristiques (variables indépendantes)
    # y = ml_data['Status']  # Cible (variable dépendante)

    # # Diviser les données en ensembles d'entraînement et de test (80% d'entraînement, 20% de test)
    # from sklearn.model_selection import train_test_split
    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


    # # Entraîner un modèle de machine learning (par exemple, une régression logistique)
    # from sklearn.linear_model import LogisticRegression
    # model = LogisticRegression()
    # model.fit(X_train, y_train)

    # # Évaluer la performance du modèle
    # accuracy = model.score(X_test, y_test)
    # st.write(f"Précision du modèle : {accuracy}")

    # # Retourner les données utilisées pour l'entraînement et l'évaluation
    # return {
    #     'X_train': X_train,
    #     'X_test': X_test,
    #     'y_train': y_train,
    #     'y_test': y_test,
    #     'model': model
    # }

    
def main():
    data = pd.read_csv("C:/Users/nagrimault/Downloads/final_proto_2.csv")  # Charger vos données à partir du fichier CSV

    tabs = ["Dashboard", "Machine Learning"]
    selected_tab = st.sidebar.selectbox("Sélectionnez un onglet", tabs)
    if selected_tab == "Dashboard":
        dashboard(data)
    elif selected_tab == "Machine Learning":
        machine_learning(data)

if __name__ == "__main__":
    main()
