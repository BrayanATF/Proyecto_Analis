import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import folium

def generar_figuras(clean_csv, out_dir="report/figures"):
    df = pd.read_csv(clean_csv, parse_dates=['fecha'])
    # serie diaria
    df_daily = df.groupby(df['fecha'].dt.date)['total'].sum().reset_index()
    df_daily.columns=['fecha','total']
    fig = px.line(df_daily, x='fecha', y='total', title='Afluencia diaria')
    fig.write_image(f"{out_dir}/ts_afluencia.png", scale=2)
    # heatmap simple con matplotlib
    pivot = df.pivot_table(values='total', index=df['fecha'].dt.date, columns='hora', aggfunc='sum', fill_value=0)
    plt.figure(figsize=(12,6)); plt.imshow(pivot.values, aspect='auto'); plt.colorbar()
    plt.savefig(f"{out_dir}/heatmap_afluencia.png", bbox_inches='tight'); plt.close()
    # mapa folium
    st_sum = df.groupby(['estacion','lat','lon'])['total'].sum().reset_index()
    m = folium.Map(location=[19.32,-99.13], zoom_start=11)
    for _, r in st_sum.iterrows():
        folium.CircleMarker([r['lat'], r['lon']], radius=max(4,int(r['total']/15000)),
                            popup=f"{r['estacion']} - {int(r['total'])}").add_to(m)
    m.save(f"{out_dir}/mapa_estaciones.html")
    print("Figuras creadas en", out_dir)

if __name__ == "__main__":
    generar_figuras("data/afluencia_limpia.csv")
