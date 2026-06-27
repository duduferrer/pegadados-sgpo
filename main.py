import camelot
import pandas as pd
from getOperators import create_operator_df

def main():
    df_escala, df_legenda = create_dfs()
    operadores = create_operator_df(df_legenda)
    
def create_dfs():
    tables = camelot.read_pdf('maio 26 ope.pdf', pages='all')
    dfs = [table.df for table in tables]
    df_final = pd.concat(dfs, ignore_index=True)
    # DIVIDE OS DADOS EM 3 DATAFRAMES: df_escala, df_legenda e df_operadores
    operador_idx = df_final[df_final[0]=='Operador'].index[0]
    legenda_idx = df_final[df_final[0]=='LEGENDA'].index[0]
    alteracoes_idx = df_final[df_final[0]=='ALTERAÇÕES NA ESCALA'].index[0]
    df_escala = df_final.iloc[:legenda_idx]
    df_legenda = df_final.iloc[operador_idx+1:alteracoes_idx]
    return df_escala, df_legenda

if __name__ == "__main__":
    main()