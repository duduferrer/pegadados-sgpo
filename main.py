import camelot
import pandas as pd
from getOperators import create_operator_df
from getEscala import create_escala_df
from dataclasses import dataclass
from config import CONFIG
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import filedialog
import logging
import traceback

MESES = {
    "JANEIRO": 1, "FEVEREIRO": 2, "MARÇO": 3, "ABRIL": 4,
    "MAIO": 5, "JUNHO": 6, "JULHO": 7, "AGOSTO": 8,
    "SETEMBRO": 9, "OUTUBRO": 10, "NOVEMBRO": 11, "DEZEMBRO": 12
}
logging.basicConfig(
    filename="app.log",
    level=logging.WARNING,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def main():
    root = tk.Tk()
    root.withdraw()

    arquivos = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])

    dfs = []
    for arquivo in arquivos:
        try:
            df = processar_escala(arquivo)
            dfs.append(df)
        except Exception as e:
            logging.error(traceback.format_exc())


    df_final = pd.concat(dfs, ignore_index=True)
    now = datetime.now().strftime("%d-%m-%Y_%H-%M")
    df_final.to_csv(''.join(["escala_", now, '.csv']), index=False, encoding="utf-8-sig")

def processar_escala(arquivo: str):
    df_escala, df_legenda, meta = create_dfs(arquivo)
    operadores = create_operator_df(df_legenda)
    escala = create_escala_df(df_escala)
    data, horarios_turnos = date_manipulation(df_escala, meta['mes'], meta['ano'])
    return create_complete_df(operadores, escala, meta, data, horarios_turnos)



def create_dfs(arquivo: str) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    tables = camelot.read_pdf(arquivo, pages='all')
    dfs = [table.df for table in tables]
    try:
        dfs[1] = dfs[1].drop(columns=[2, 6, 11])
        dfs[1].columns = range(len(dfs[1].columns))
    except:
        pass
    df_final = pd.concat(dfs, ignore_index=True)
    orgao = get_info(df_final, 'ORGÃO')
    funcao = " ".join(get_info(df_final, 'HT/FUNÇÃO').split()[-2:])
    mes =  get_info(df_final, 'ESCALA CUMPRIDA (MÊS/ANO)').split()[0]
    ano =  get_info(df_final, 'ESCALA CUMPRIDA (MÊS/ANO)').split()[-1]
    # BUSCAR O TITULO E SOMAR UMA LINHA PARA ACHAR FUNCAO, ORGAO, MES E ANO
    meta = {"ano": ano,
            "mes": mes,
            "funcao": funcao,
            "orgao": orgao}
    # DIVIDE OS DADOS EM 3 DATAFRAMES: df_escala, df_legenda e df_operadores
    operador_idx = df_final[df_final[0]=='Operador'].index[0]
    legenda_idx = df_final[df_final[0]=='LEGENDA'].index[0]
    alteracoes_idx = df_final[df_final[0]=='ALTERAÇÕES NA ESCALA'].index[0]
    df_escala = df_final.iloc[:legenda_idx]
    df_legenda = df_final.iloc[operador_idx+1:alteracoes_idx]
    return df_escala, df_legenda, meta

def create_complete_df(operadores: pd.DataFrame, escala: pd.DataFrame, meta:dict, data:datetime, horarios: dict)->pd.DataFrame:
    df_completo = pd.DataFrame(columns=["Graduação", "Nome de Guerra", "Indicativo", "Manutençao(S/N)", "Orgão", "Função", "Turno", "Data", "Inicio", "Fim", "Duração"])
    for _, row in escala.iterrows():
        op = operadores[operadores.isin([row['legenda']]).any(axis=1)]
        nome = op["nome"].values[0]
        grad = op["grad"].values[0]
        if pd.notna(op["lpna"].values[0]):
            ind = op["lpna"].values[0]
        else:
          ind = op["nome"].values[0]
          logging.warning(''.join([op["nome"].values[0]," nao encontrou indicativo. Provavelmente a tabela Indicativos nao bate com a escala."]))
        isManutencao = 'S' if 'M'in row["legenda"] else 'N'
        nova_linha = {
            "Graduação":grad,
            "Nome de Guerra": nome,
            "Indicativo":ind,
            "Manutençao(S/N)": isManutencao, 
            "Orgão": meta['orgao'], 
            "Função": meta['funcao'], 
            "Turno": row['turno'], 
            "Data": data.replace(day=int(row["dia"])).strftime("%d/%m/%Y"), 
            "Inicio": horarios[row["turno"]].inicio, 
            "Fim": horarios[row["turno"]].fim, 
            "Duração": horarios[row["turno"]].duracao
        }
        df_completo = pd.concat([df_completo, pd.DataFrame([nova_linha])], ignore_index=True)
    return df_completo

def date_manipulation(df_escala: pd.DataFrame, mes: str, ano: str):
    turnos = CONFIG['turnos']
    @dataclass
    class Turno:
        inicio: str
        fim: str
        duracao: int
    horarios_turnos: dict[str, Turno] = {}
    cab_idx = df_escala[df_escala[0]=='DIA DO MÊS / SEM.'].index[0]
    df_escala_limpo = df_escala[cab_idx:]
    df_escala_limpo = df_escala_limpo.reset_index(drop=True)
    df_escala_limpo.columns = df_escala_limpo.iloc[0]
    df_escala_limpo = df_escala_limpo[1:]
    for col in df_escala_limpo.columns:
        if(type(col)==str):
            turno = col.split(" ")[0]
            if(turno in turnos):
                inicio = col.split()[1]
                fim = col.split()[3]
                inicio_asTime = datetime.strptime(inicio, "%H:%M")
                fim_asTime = datetime.strptime(fim, "%H:%M")

                if fim_asTime < inicio_asTime:  # virada de meia noite
                    fim_asTime += timedelta(days=1)

                duracao = int((fim_asTime - inicio_asTime).total_seconds() / 60)
                horarios_turnos[turno] = Turno(inicio=inicio, fim=fim, duracao=duracao)
    data = datetime(int(ano), MESES[mes.upper()], 1)
    return (data, horarios_turnos)    


def get_info(df: pd.DataFrame,info: str)->str:
    row = df[df.isin([info]).any(axis=1)].iloc[0]
    col = row[row==info].index[0]
    return df[col][row.name+1]

if __name__ == "__main__":
    main()