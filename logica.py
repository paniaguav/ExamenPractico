import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import base64
import json
from io import BytesIO

COLOR_BARRAS = '#c21414'
COLOR_POLIGONO = '#c21414'
COLOR_ACUMULADA = '#c21414'

def get_base64_image():
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('utf-8')

df = pd.read_csv('datos_examen.csv')
df['velocidad'] = df['velocidad'].fillna(df['velocidad'].mean())

variables_numericas = ['peso', 'altura', 'velocidad']
IMGS = {}

baseDatos = {
    "peso": {"media": "9.78", "mediana": "10.30", "moda": "11.00"},
    "altura": {"media": "68.62", "mediana": "70.00", "moda": "75.00"},
    "velocidad": {"media": "25.10", "mediana": "21.80", "moda": "10.30"},
    "color": {"media": "N/A", "mediana": "N/A", "moda": "Verde"}
}

for var in variables_numericas:
    counts, bins = np.histogram(df[var], bins=6)
    centros = 0.5 * (bins[:-1] + bins[1:])
    etiquetas = [f"[{bins[i]:.1f} - {bins[i+1]:.1f})" for i in range(len(bins)-1)]
    
    plt.figure(figsize=(6,4))
    plt.bar(etiquetas, counts, color=COLOR_BARRAS, edgecolor='white')
    plt.title(f'Frecuencias Absolutas - {var.capitalize()}')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    IMGS[f"{var}_absoluta"] = get_base64_image()

    plt.figure(figsize=(6,4))
    plt.pie(counts, labels=etiquetas, autopct='%1.1f%%', colors=sns.color_palette('Blues', 6))
    plt.title(f'Frecuencias Relativas - {var.capitalize()}')
    plt.tight_layout()
    IMGS[f"{var}_relativa"] = get_base64_image()

    acumuladas = np.cumsum(counts)
    plt.figure(figsize=(6,4))
    plt.step(bins[:-1], acumuladas, where='post', color=COLOR_ACUMULADA, linewidth=2, marker='o')
    plt.fill_between(bins[:-1], acumuladas, step="post", alpha=0.2, color=COLOR_ACUMULADA)
    plt.title(f'Frecuencias Acumuladas - {var.capitalize()}')
    plt.tight_layout()
    IMGS[f"{var}_acumulada"] = get_base64_image()

    plt.figure(figsize=(6,4))
    plt.plot(centros, counts, marker='o', color=COLOR_POLIGONO, linewidth=2)
    plt.title(f'Polígono de Frecuencias - {var.capitalize()}')
    plt.tight_layout()
    IMGS[f"{var}_poligono"] = get_base64_image()

colores = ['Verde', 'Amarillo', 'Blanco', 'Sin color']
frec_abs_color = [12, 9, 7, 1]
paleta_colores = ['#2ecc71', '#f1c40f', '#f5f5f5', '#95a5a6']

plt.figure(figsize=(6,4))
plt.bar(colores, frec_abs_color, color=COLOR_BARRAS, edgecolor='white')
plt.title('Frecuencias Absolutas - Color')
plt.tight_layout()
IMGS["color_absoluta"] = get_base64_image()

plt.figure(figsize=(6,4))
plt.pie(frec_abs_color, labels=colores, autopct='%1.1f%%', colors=paleta_colores)
plt.title('Frecuencias Relativas - Color')
plt.tight_layout()
IMGS["color_relativa"] = get_base64_image()

js_content = f"const IMGS = {json.dumps(IMGS)};\nconst baseDatos = {json.dumps(baseDatos)};"

with open('datos.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print("Imágenes guardadas con éxito")