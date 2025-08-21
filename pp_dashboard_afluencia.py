# dashboard/app_dashboard_afluencia.py
import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium

st.set_page_config(layout="wide", page_title="Afluencia Azteca")
st.title("Dashboard: Afluencia — Estadio Azteca / Tláhuac")

df = pd.read_csv("data/afluencia_limpia.csv", parse_dates=["fecha"])

with st.sidebar:
    estaciones = sorted(df['estacion'].unique())
    estacion_sel = st.multiselect("Selecciona estación(es)", estaciones, default=['Tláhuac'] if 'Tláhuac' in estaciones else estaciones[:1])
    fecha_range = st.date_input("Rango de fechas", value=(df['fecha'].dt.date.min(), df['fecha'].dt.date.max()))

start, end = pd.to_datetime(fecha_range[0]), pd.to_datetime(fecha_range[1])
df_f = df[(df['estacion'].isin(estacion_sel)) & (df['fecha']>=start) & (df['fecha']<=end)]

st.metric("Total periodo", f"{int(df_f['total'].sum()):,}")
# serie temporal
df_daily = df_f.groupby(df_f['fecha'].dt.date)['total'].sum().reset_index()
fig = px.line(df_daily, x='fecha', y='total', title='Afluencia diaria')
st.plotly_chart(fig, use_container_width=True)

# mapa
st.subheader("Mapa estaciones")
st_data = st_folium(folium.Map(location=[19.32,-99.13], zoom_start=11), width=700)
