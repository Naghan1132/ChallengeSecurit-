import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Charger les données
@st.cache_data
def load_data(file_path):
    return pd.read_csv(file_path, sep=';')

# Titre de l'application
st.title("Analyse des logs Iptables")

# Afficher les premières lignes des données
st.write("Les premières lignes des données :")
df = load_data("logs_iptables.csv")
st.write(df.head())

# 1. Analyse descriptive des flux rejetés et autorisés par protocoles (TCP, UDP) avec filtrage par plages de ports
st.subheader("Analyse des flux par protocoles et plages de ports")
selected_protocol = st.selectbox("Sélectionner un protocole :", df['Protocole'].unique())
min_port = st.slider("Port minimum :", min_value=0, max_value=65535, value=0)
max_port = st.slider("Port maximum :", min_value=0, max_value=65535, value=65535)

filtered_df = df[(df['Protocole'] == selected_protocol) & (df['Port de destination'].between(min_port, max_port))]
st.write(filtered_df)

# 2. Parcours des données via l'utilisation de renderDataTable
st.subheader("Parcours des données via renderDataTable")
st.dataframe(filtered_df)

# 3. Visualisation interactive des données
st.subheader("Visualisation interactive des données")
source_ip_counts = df['Source IP'].value_counts()
selected_ip = st.selectbox("Sélectionner une adresse IP source :", source_ip_counts.index)
filtered_destinations = df[df['Source IP'] == selected_ip]
destination_counts = filtered_destinations['Destination IP'].value_counts()

plt.figure(figsize=(10, 6))
sns.barplot(x=destination_counts.index, y=destination_counts.values)
plt.xlabel('Adresse IP de destination')
plt.ylabel('Nombre d\'occurrences')
plt.title('Occurrence des adresses IP de destination')
plt.xticks(rotation=45)
st.pyplot()

# 4. Statistiques relatives
st.subheader("Statistiques relatives")
top_source_ips = source_ip_counts.head(5)
st.write("TOP 5 des IP sources les plus émettrices :")
st.write(top_source_ips)

top_ports = df[df['Action'] == 'Permit']['Port de destination'].value_counts().head(10)
st.write("TOP 10 des ports inférieurs à 1024 avec un accès autorisé :")
st.write(top_ports)

invalid_ips = df[~df['Source IP'].str.startswith('192.168')]
st.write("Accès des adresses non inclues dans le plan d'adressage de l'Université :")
st.write(invalid_ips)
