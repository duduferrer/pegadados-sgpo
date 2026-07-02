# Script Escala

Script para processamento de escalas operacionais em PDF, gerando um arquivo CSV consolidado com os dados de todos os controladores por turno e data.

---

## Pré-requisitos

Nenhum. O script é distribuído como executável `.exe` e não requer instalação de Python ou dependências.

---

## Estrutura esperada na mesma pasta do executável

```
├── Script-Escala.exe
├── configs.yaml
├── INDICATIVOS.csv
└── app.log           ← gerado automaticamente
```

---

## Configuração

### `configs.yaml`

Define os turnos operacionais. Os nomes devem corresponder exatamente aos identificadores usados na coluna de turno da escala PDF.

```yaml
turnos:
  - M
  - T
  - P
planilha_indicativos: INDICATIVOS.csv
```

> Adicione ou remova turnos conforme a necessidade do órgão.
> Se precisar mudar o nome do arquivo de indicativos, mude aqui também.

---

### `INDICATIVOS.csv`

Arquivo CSV obrigatório contendo o cadastro dos operadores. Deve conter exatamente as seguintes colunas:

| GRADUAÇÃO | NOME | INDICATIVO |
|-----------|------|------------|
| 2S | LUFFY | LFFY |
| 3S | NARUTO | NRTO |


---

## Uso

1. Certifique-se de que `config.yaml` e `INDICATIVOS.csv` estão na mesma pasta que o executável
2. Execute `Script-Escala.exe` com duplo clique
3. Uma janela de seleção de arquivos será aberta — selecione um ou mais PDFs de escala usando **Ctrl+Click** para seleção múltipla
4. Aguarde o processamento — o CSV será gerado na mesma pasta com o nome no formato:

```
escala_dd-mm-yyyy_HH-MM.csv
```

---

## Saída

O CSV gerado contém as seguintes colunas:

| Coluna | Descrição |
|--------|-----------|
| Graduação | Graduação do controlador |
| Nome de Guerra | Nome de guerra |
| Indicativo | Indicativo de licença (LPNA) |
| Manutenção(S/N) | Se o turno é de manutenção |
| Órgão | Órgão responsável pela escala |
| Função | Função do controlador no turno |
| Turno | Identificador do turno (M, T, P...) |
| Data | Data do turno no formato DD/MM/YYYY |
| Início | Horário de início do turno |
| Fim | Horário de fim do turno |
| Duração | Duração do turno em minutos |

---

## Logs

Erros e avisos são registrados automaticamente em `app.log` na mesma pasta do executável, com timestamp e traceback completo.

Caso o script não encontre um indicativo que case entre a escala e o `INDICATIVOS.csv`, o ocorrência será registrada no log e o nome do operador será utilizado como fallback.

## Contato

Caso de dúvidas ou problemas, entre em contato com Eduardo via [duduferrer7@gmail.com](mailto:duduferrer7@gmail.com)