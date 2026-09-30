---
name: dataviz
description: Generación automatizada de visualizaciones estadísticas de alta resolución (300 DPI) bajo normas APA 7.ª edición con Matplotlib y Seaborn para SIVAC-THESIS-LAB.
---

# VISUALIZACIÓN DE DATOS ESTADÍSTICOS (DATAVIZ) — NORMA APA 7.ª EDICIÓN

> **Propósito:** Esta habilidad proporciona scripts y configuraciones en Python (`matplotlib`, `seaborn`) para generar figuras estadísticas listas para inserción en Word y PDF, con resolución de 300 DPI, legibilidad académica, paleta accesible y formato APA 7.

---

## 1. Parámetros de Diseño y Configuración Global APA 7

```python
import matplotlib.pyplot as plt
import seaborn as sns

def configurar_estilo_apa7():
    """
    Configura el entorno de Matplotlib para cumplir con los estándares de APA 7.
    """
    plt.rcParams.update({
        'font.family': 'serif',
        'font.serif': ['Times New Roman', 'DejaVu Serif'],
        'font.size': 10,
        'axes.labelsize': 11,
        'axes.titlesize': 12,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'legend.fontsize': 10,
        'figure.titlesize': 12,
        'figure.dpi': 300,
        'savefig.dpi': 300,
        'savefig.bbox': 'tight',
        'savefig.pad_inches': 0.1,
        'axes.spines.top': False,      # Eliminar lomo superior
        'axes.spines.right': False,    # Eliminar lomo derecho
        'axes.grid': True,
        'grid.color': '#E0E0E0',
        'grid.linestyle': '--',
        'grid.linewidth': 0.5,
        'grid.alpha': 0.7
    })
```

---

## 2. Tipos de Gráficos Canónicos para la Tesis SIVAC

### 2.1. Gráfico de Cajas Pareado con Puntos Individuales (Boxplot + Strip)
Ideal para comparar tiempos de procesamiento ($T_{reg}$, $T_{vale}$) entre Pretest y Postest ($n=14$).

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def generar_boxplot_pareado(pre, post, nombre_indicador, unidad, ruta_salida):
    configurar_estilo_apa7()
    fig, ax = plt.subplots(figsize=(6.5, 4.5))
    
    df_plot = pd.DataFrame({
        'Momento': ['Pretest'] * len(pre) + ['Postest'] * len(post),
        'Valor': list(pre) + list(post)
    })
    
    # Paleta sobria institucional (Azul pizarra y Gris azulado)
    paleta = ['#4A6FA5', '#166088']
    
    # Boxplot
    sns.boxplot(
        x='Momento', y='Valor', data=df_plot,
        palette=paleta, width=0.4, showcaps=True,
        boxprops=dict(alpha=0.8),
        medianprops=dict(color='white', linewidth=2),
        whiskerprops=dict(linewidth=1.2),
        showmeans=True,
        meanprops=dict(marker='D', markeredgecolor='black', markerfacecolor='yellow', markersize=6),
        ax=ax
    )
    
    # Puntos individuales (Strip plot con dispersión)
    sns.stripplot(
        x='Momento', y='Valor', data=df_plot,
        color='black', size=5, jitter=0.15, alpha=0.6, ax=ax
    )
    
    # Conectar pares con líneas grises tenues
    for i in range(len(pre)):
        ax.plot([0, 1], [pre[i], post[i]], color='gray', linestyle=':', alpha=0.5, linewidth=0.8)
        
    ax.set_ylabel(f'{nombre_indicador} ({unidad})', fontweight='bold')
    ax.set_xlabel('Momento de Evaluación', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(ruta_salida, dpi=300)
    plt.close()
```

### 2.2. Gráfico de Barras Divergentes para Escala Likert (Modelo TAM)
Ideal para los 10 ítems del Cuestionario de Satisfacción del Usuario (Aceptación y Utilidad Percibida).

---

## 3. Jerarquía y Formato APA 7 en el Documento de Word

Cuando el maquetador inserte una figura generada:
1. **Número de Figura:** Párrafo superior en negrita: `Figura 1` (Times New Roman 12 pt).
2. **Título de la Figura:** Párrafo siguiente en cursiva: `*Comparación del tiempo de registro de movimientos de vacunas en pretest y postest*`.
3. **Imagen:** Centrada, a ancho completo de texto (máximo 6.5 pulgadas / 16.5 cm).
4. **Nota de la Figura:** Párrafo inferior en Times New Roman 10 pt: `*Nota.* Los rombos amarillos representan la media aritmética y las líneas blancas la mediana. Los puntos negros representan los 14 registros individuales pareados. Elaboración propia.`
