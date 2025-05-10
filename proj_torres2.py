import pandas as pd
import numpy as np
import json
import os

def calcular_alcance(frequencia_mhz, fspl=100):
    if pd.isna(frequencia_mhz) or frequencia_mhz <= 0:
        return None

    c = 3e8 
    frequencia_hz = frequencia_mhz * 1e6 

    d_km = 10 ** ((fspl - 20 * np.log10(frequencia_hz) - 20 * np.log10(4 * np.pi / c)) / 20) / 1000
    
    return round(d_km, 2) 


df = pd.read_excel("ERBs_Out_24.xlsx")


def processar_faixa(faixa):
    if pd.isna(faixa):
        return None
    
    try:
        valores = [float(f) for f in faixa.replace(" ", "").split("-") if f.replace(".", "").isdigit()]
        if valores:
            menor_frequencia = min(valores) 
            return calcular_alcance(menor_frequencia)
        return None
    except:
        return None


df["Alcance Estimado (km)"] = df["Faixa"].apply(processar_faixa)

print(df[["Alcance Estimado (km)"]])


def extrair_menor_frequencia(faixa):
    if pd.isna(faixa):
        return None
    try:
        valores = [float(f) for f in faixa.replace(" ", "").split("-") if f.replace(".", "").isdigit()]
        return min(valores) if valores else None
    except:
        return None

def gerar_lista_torres(df):
    torres = []
    for _, row in df.iterrows():
        freq = extrair_menor_frequencia(row.get("Faixa"))
        torre = {
            "ID": str(row.get("NumEstacao")).strip(),
            "LAT": round(row.get("Latitude"), 6),
            "LNG": round(row.get("Longitude"), 6),
            "EMPRESA": row.get("Operadora"),
            "FREQUENCIA": freq,
            "DISTANCIA": calcular_alcance(freq)
        }
        torres.append(torre)
    return torres

torres_atualizadas = gerar_lista_torres(df)


with open("torres.json", "w", encoding="utf-8") as f:
    json.dump(torres_atualizadas, f, indent=4, ensure_ascii=False)

