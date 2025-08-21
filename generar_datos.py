# src/generar_datos.py
import pandas as pd, numpy as np
from datetime import datetime, timedelta
import random

def generar_csv_sintetico(out_path, n_sample=1000):
    random.seed(42); np.random.seed(42)
    stations = [
        {'estacion_id':120, 'estacion':'Tláhuac', 'lat':19.2978, 'lon':-99.0123, 'linea':'L12'},
        {'estacion_id':200, 'estacion':'Estadio_Azteca', 'lat':19.3020, 'lon':-99.1500, 'linea':'NA'},
        {'estacion_id':10,  'estacion':'Centro', 'lat':19.4326, 'lon':-99.1332, 'linea':'L1'}
    ]
    start = datetime(2025,6,1,0,0,0)
    end = datetime(2025,6,30,23,0,0)
    all_hours=[]
    t=start
    while t<=end:
        all_hours.append(t)
        t+=timedelta(hours=1)

    rows=[]
    for ts in all_hours:
        for s in stations:
            hour=ts.hour; weekday=ts.weekday()
            base=200
            if hour in (7,8): base*=3.5
            if hour in (17,18,19): base*=4.0
            size_mul = 2.2 if s['estacion']=='Tláhuac' else (1.8 if s['estacion']=='Estadio_Azteca' else 1.0)
            mean = base * size_mul
            total = int(np.round(np.random.poisson(lam=max(10, mean))))
            entradas = int(total * np.random.uniform(0.45,0.55))
            salidas = total - entradas
            rows.append({
                'fecha': ts.strftime('%Y-%m-%d %H:%M:%S'),
                'estacion_id': s['estacion_id'],
                'estacion': s['estacion'],
                'lat': s['lat'],
                'lon': s['lon'],
                'linea': s['linea'],
                'entradas': entradas,
                'salidas': salidas,
                'total': total,
                'hora': hour
            })
    df = pd.DataFrame(rows).sample(n=min(n_sample, len(rows)), random_state=42).reset_index(drop=True)
    df.to_csv(out_path, index=False, encoding='utf-8')
    print("CSV generado:", out_path)

if __name__ == "__main__":
    generar_csv_sintetico("data/diccionario_afluencia_sintetico.csv", n_sample=1000)
