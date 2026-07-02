import pandas as pd
from config import CONFIG

def create_escala_df(df_escala: pd.DataFrame):
    cab_idx = df_escala[df_escala[0]=='DIA DO MÊS / SEM.'].index[0]
    df_escala_limpo = df_escala[cab_idx:]
    df_escala_limpo = df_escala_limpo.reset_index(drop=True)
    df_escala_limpo.columns = df_escala_limpo.iloc[0]
    df_escala_limpo = df_escala_limpo[1:]

    turnos = CONFIG['turnos']
    df_lista_turnos_legenda = pd.DataFrame(columns=["dia", "turno", "legenda"])

    for col in df_escala_limpo.columns:
        if(type(col)==str):
            turno = col.split(" ")[0]
            if(turno in turnos):
                for idx, legendas in df_escala_limpo[col].items():
                    legendas_list = legendas.split()
                    for legenda in legendas_list:
                        linha = {
                            "dia": idx,
                            "turno": turno,
                            "legenda": legenda
                        }
                        df_lista_turnos_legenda = pd.concat([df_lista_turnos_legenda, pd.DataFrame([linha])], ignore_index=True)
    return df_lista_turnos_legenda