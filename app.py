import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

st.set_page_config(page_title="Employee Dashboard", layout="wide")
st.title("Employee Insights Dashboard")
st.markdown("Gráficas seleccionadas por zona, correlaciones y comportamiento organizacional.")
st.caption("Análisis elaborado por **Janeth Valdivia** **Valeria Ramírez** y **Esther Apaza**")

# Cargar datos
df = pd.read_csv("work.csv")

# Colores tipo ejecutivo
executive_palette = px.colors.qualitative.Set2

# 🟡 Sunburst por zona geográfica
st.subheader("Sunburst por Zona Geográfica")
zonas = df["zona_geografica"].dropna().unique()

for zona in zonas:
    df_zona = df[df['zona_geografica'] == zona].copy()
    df_zona['departamento'] = df_zona['departamento'].fillna('Desconocido')
    df_zona['modalidad_trabajo'] = df_zona['modalidad_trabajo'].fillna('Desconocido')
    
    fig = px.sunburst(
        df_zona,
        path=['departamento', 'modalidad_trabajo'],
        title=f'Distribution by Department and Work Arrangement – Area: {zona}',
        color='departamento',
        color_discrete_sequence=px.colors.qualitative.Vivid
    )
    
    fig.update_traces(textinfo='label+percent root')
    fig.update_layout(
        margin=dict(t=50, l=0, r=0, b=0),
        font=dict(family='Georgia', size=12),
        title_font=dict(size=16, family='Georgia')
    )
    
    st.plotly_chart(fig, use_container_width=True)

# 🔥 Heatmap de correlaciones con Plotly Express
st.subheader("Matriz de Correlación General")

corr = df.select_dtypes(include=['float64', 'int64']).corr()

fig = px.imshow(
    corr,
    text_auto=True,
    color_continuous_scale='RdBu',
    title='Correlation Matrix',
    aspect='auto'
)
fig.update_layout(
    height=500,
    font=dict(family='Georgia', size=12),
    title_font=dict(size=16, family='Georgia'),
    coloraxis_colorbar=dict(title="Correlation")
)
st.plotly_chart(fig, use_container_width=True)

# 🌳 Dendrograma
st.subheader("Dendrograma: Bienestar, Ocio y Productividad")
selected_cols = [
    'horas_ejercicio_semana',
    'horas_videojuegos_semana',
    'horas_ocio_semana',
    'horas_sueno_noche',
    'nivel_estres',
    'satisfaccion_laboral',
    'productividad_score'
]
if all(col in df.columns for col in selected_cols):
    df_subset = df[selected_cols].dropna()
    scaler = StandardScaler()
    df_scaled = pd.DataFrame(scaler.fit_transform(df_subset), columns=selected_cols)
    df_for_dendrogram = df_scaled.T
    fig_insight_dendro = ff.create_dendrogram(
        df_for_dendrogram,
        labels=selected_cols,
        orientation='left',
        color_threshold=100
    )
    fig_insight_dendro.update_layout(
        title='Dendrogram: Relationships between Well-being, Leisure, and Productivity',
        xaxis_title='Distance (Similarity)',
        yaxis_title='Selected Variables',
        font=dict(family='Georgia', size=12)
    )
    st.plotly_chart(fig_insight_dendro, use_container_width=True)
else:
    st.warning("Faltan columnas necesarias para generar el dendrograma.")

# 📊 Boxplot de salario por zona geográfica
st.subheader("Distribución Salarial por Zona Geográfica")
if 'zona_geografica' in df.columns and 'salario_anual' in df.columns:
    fig = px.box(
        df,
        x='zona_geografica',
        y='salario_anual',
        color='zona_geografica',
        title='Salary Distribution by Region',
        color_discrete_sequence=executive_palette
    )
    fig.update_layout(
        height=500,
        font=dict(family='Georgia', size=12),
        title_font=dict(size=16, family='Georgia')
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No hay datos suficientes para mostrar el boxplot de salario por zona.")

# 📊 Gráfica de barras: satisfacción por departamento
st.subheader("Satisfacción Promedio por Departamento")
if 'satisfaccion_laboral' in df.columns and 'departamento' in df.columns:
    avg_satisfaction = df.groupby('departamento')['satisfaccion_laboral'].mean().reset_index()
    fig_bar = px.bar(
        avg_satisfaction,
        x='departamento',
        y='satisfaccion_laboral',
        color='departamento',
        title='Average Job Satisfaction by Department',
        color_discrete_sequence=executive_palette
    )
    fig_bar.update_layout(
        xaxis_tickangle=-45,
        height=400,
        font=dict(family='Georgia', size=12),
        title_font=dict(size=16, family='Georgia')
    )
    st.plotly_chart(fig_bar, use_container_width=True)
else:
    st.warning("No se encontraron datos de satisfacción laboral por departamento.")
