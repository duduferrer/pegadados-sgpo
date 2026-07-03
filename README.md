git# Script Escala

Script para processamento de escalas operacionais em PDF, gerando um arquivo CSV consolidado com os dados de todos os controladores por turno e data.

---

## Pré-requisitos

Nenhum. O script é distribuído como arquivo compactado `.zip` e não requer instalação de Python ou dependências.

---

## Instalação

1. Extraia o arquivo `.zip` em uma pasta de sua escolha
2. Não mova o executável para fora da pasta — ele depende dos arquivos ao redor

Após extrair, a estrutura deve ficar assim:

```
Script-Escala/
├── Script-Escala.exe
├── configs.yaml
├── INDICATIVOS.csv
└── app.log           ← gerado automaticamente na primeira execução
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

1. Extraia o `.zip` e abra a pasta `Script-Escala`
2. Preencha o `INDICATIVOS.csv` com os operadores do seu órgão
3. Ajuste os turnos no `configs.yaml` conforme necessário
4. Execute `Script-Escala.exe` com duplo clique
5. Uma janela de seleção de arquivos será aberta — selecione um ou mais PDFs de escala usando **Ctrl+Click** para seleção múltipla
6. Aguarde o processamento — o CSV será gerado na mesma pasta com o nome no formato:

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

Caso o script não encontre um indicativo que case entre a escala e o `INDICATIVOS.csv`, a ocorrência será registrada no log e o nome do operador será utilizado como fallback.

---

## Contato

Caso de dúvidas ou problemas, entre em contato com Eduardo via [duduferrer7@gmail.com](mailto:duduferrer7@gmail.com)