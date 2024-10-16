import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import MaxNLocator

def styled_histplot(df, selected_column):
    # Vytvoření stylizovaného grafu distribuce
    fig, ax = plt.subplots()
    
    # Upravený histogram s jemnější mřížkou
    sns.histplot(df[selected_column], bins=30, ax=ax, kde=True, color='dodgerblue', edgecolor='black')
    
    # Upravení názvu os a titulků s bílou barvou
    ax.set_title(f"Distribuce {selected_column}", fontsize=16, color='white')
    ax.set_xlabel(selected_column, fontsize=14, color='white')
    ax.set_ylabel('Počet', fontsize=14, color='white')
    
    # Jemnější mřížka a nastavení průhlednosti
    ax.grid(True, linestyle='--', alpha=0.3)  # Změna na 0.3 pro jemnější vzhled
    
    # Nastavení pozadí grafu
    ax.set_facecolor("#222222")  # Tmavé pozadí
    
    # Barva os (čísla na osách)
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    
    # Maximální hodnoty na ose x jako celé číslo
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    
    # Nastavení barev pozadí kolem grafu
    fig.patch.set_facecolor('#222222')  # Celý graf má tmavé pozadí
    
    return fig
