# src/limpieza.py
import pandas as pd

def limpiar_afluencia(in_path, out_path):
    df = pd.read_csv(in_path)
    df.columns = [c.strip().lower().replace(' ','_') for c in df.columns]
    df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')
    if 'hora' not in df.columns or df['hora'].isna().all():
        df['hora'] = df['fecha'].dt.hour
    if 'total' not in df.columns or df['total'].isna().all():
        if 'entradas' in df.columns and 'salidas' in df.columns:
            df['total'] = df['entradas'].fillna(0) + df['salidas'].fillna(0)
        else:
            df['total'] = pd.to_numeric(df.get('total',0), errors='coerce').fillna(0)
    df['estacion'] = df['estacion'].astype(str).str.strip()
    df = df[~df['fecha'].isna() & ~df['estacion'].isna()]
    df.to_csv(out_path, index=False, encoding='utf-8')
    print("Limpieza completada. Guardado:", out_path)

if __name__ == "__main__":
    limpiar_afluencia("data/diccionario_afluencia_sintetico.csv","data/afluencia_limpia.csv")