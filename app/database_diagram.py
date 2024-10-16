import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import tempfile

# Funkce pro načtení cizích klíčů
def load_relationships(engine, schema):
    query = f"""
    SELECT
        fk.name AS foreign_key,
        tp.name AS parent_table,
        tr.name AS referenced_table,
        cp.name AS parent_column,
        cr.name AS referenced_column
    FROM
        sys.foreign_keys AS fk
    INNER JOIN
        sys.foreign_key_columns AS fkc ON fk.object_id = fkc.constraint_object_id
    INNER JOIN
        sys.tables AS tp ON fk.parent_object_id = tp.object_id
    INNER JOIN
        sys.columns AS cp ON tp.object_id = cp.object_id AND fkc.parent_column_id = cp.column_id
    INNER JOIN
        sys.tables AS tr ON fk.referenced_object_id = tr.object_id
    INNER JOIN
        sys.columns AS cr ON tr.object_id = cr.object_id AND fkc.referenced_column_id = cr.column_id
    WHERE
        SCHEMA_NAME(tp.schema_id) = '{schema}'
    """
    return pd.read_sql(query, engine)

# Funkce pro generování databázového diagramu
# Funkce pro generování databázového diagramu s lepším rozložením
def generate_diagram(engine, schema):
    relationships = load_relationships(engine, schema)

    if relationships.empty:
        st.warning("Nebyly nalezeny žádné vztahy mezi tabulkami.")
        return

    # Vytvoření grafu pomocí NetworkX
    graph = nx.DiGraph()
    for _, row in relationships.iterrows():
        graph.add_edge(f"{row['parent_table']} ({row['parent_column']})", 
                       f"{row['referenced_table']} ({row['referenced_column']})", 
                       label=row['foreign_key'])

    # Optimalizované pozice a vykreslení grafu
    plt.figure(figsize=(15, 10))  # Zvětšená velikost obrázku
    pos = nx.spring_layout(graph, k=0.8, seed=42)  # Lepší rozložení uzlů

    nx.draw(graph, pos, with_labels=True, node_color="skyblue", node_size=4000, 
            edge_color="gray", font_size=12, font_weight="bold", arrowsize=20)
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=nx.get_edge_attributes(graph, 'label'))

    # Uložení diagramu do dočasného souboru
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
        plt.savefig(tmpfile.name)
        st.image(tmpfile.name)

    # Výpis vztahů pod diagramem
    st.write("### Vztahy mezi tabulkami")
    st.dataframe(relationships)


# Stránka s databázovým diagramem
def database_diagram_page():
    st.title("Databázový diagram tabulek a sloupců")

    # Načtení připojení k databázi z session state
    engine = st.session_state.get('engine')

    if not engine:
        st.error("Není dostupné připojení k databázi.")
        return

    # Výběr databáze a schématu
    selected_database = st.selectbox("Vyberte databázi", ["master", "Eshop", "DalšíDatabáze"])  # Zde může být dynamicky načítaná databáze
    selected_schema = st.selectbox("Vyberte schéma", ["dbo", "Production", "Sales"])  # Zde může být dynamicky načítané schéma

    if st.button("Vygenerovat diagram"):
        try:
            generate_diagram(engine, selected_schema)
        except Exception as e:
            st.error(f"Chyba při generování diagramu: {e}")
