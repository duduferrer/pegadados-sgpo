import pandas as pd
def create_operator_df(df_legenda: pd.DataFrame):
    df_operadores = pd.DataFrame(columns=['grad','nome', 'legenda'])

    # COLOCA OS DADOS DE OPERADORES E LEGENDA NO DATAFRAME df_operadores
    for idx, row in df_legenda.iterrows():
        df_operadores.loc[idx,['grad', 'nome', 'legenda']] = (row[1][:2], row[1][3:], row[0])

    # ADICIONA INDICATIVO LPNA
    df_indicativo = pd.read_csv('INDICATIVOS.csv', sep=',')
    df_operadores['nome'] = df_operadores['nome'].str.strip()
    df_indicativo['NOME'] = df_indicativo['NOME'].str.strip()
    df_indicativo['INDICATIVO'] = df_indicativo['INDICATIVO'].str.strip()
    df_operadores_fnl = df_operadores.merge(
        df_indicativo[['NOME','INDICATIVO']].rename(columns={'INDICATIVO':'lpna'}),
        left_on='nome',
        right_on='NOME',
        how='left'
    ).drop(columns=['NOME'])
    return df_operadores_fnl
