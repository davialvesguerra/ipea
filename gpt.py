from openai import OpenAI
import random 
import pandas as pd
import re

client = OpenAI(api_key=OPENAI_API_KEY, organization=ORGANIZATION_OPENAI_API_KEY)

n_topicos = 7
tipo_topicos = ["tópico " + str(i) for i in range(n_topicos)]

lista_de_sub_topicos = [
  {
    # "Ingestão de dados estruturados, semiestruturados e não estruturados": 1,
    "Ingestão de dados em lote (batch)": 1,
    "Ingestão de dados em streaming": 1,
    "Armazenamento de big data": 1,
    "Conceitos de processamento massivo e paralelo": 1,
    "Processamento distribuído": 1,
    "Soluções de big data: Arquitetura do ecossistema Spark": 1,
    "Arquitetura de cloud computing para ciência de dados (AWS, Azure, GCP)": 1,
  },
{
    "Álgebra relacional e SQL (padrão ANSI)": 1,
    "Banco de dados relacional: SQL Server, PostgreSQL, MySQL": 3,
    "Banco de dados NoSQL": 2,
    "Banco de dados e formatos de arquivo orientado a colunas: Parquet, MonetDB, duckDB": 3,
},
{
    "Contexto de IA: Normalização numérica": 1,
    "Contexto de IA: Discretização": 1,
    "Contexto de IA: Tratamento de dados ausentes": 1,
    "Contexto de IA: Tratamento de outliers e agregações": 1,
    "Contexto de IA: Matching - Tratamento dos dados": 1,
    "Contexto de IA: Deduplicação": 1,
    "Contexto de IA: Data cleansing": 1,
    "Contexto de IA: Enriquecimento": 1,
    "Contexto de IA: Desidentificação de dados sensíveis": 1,
    "Contexto de IA: Algoritmos fuzzy matching e stemming": 1,
},
{
    "Linguagem de programação Scala": 1,
    "Programação funcional": 1,
    "Programação orientada a objetos": 1,
    "R ou Python: Classes de objetos e suas propriedades (vetores, listas, data.frames)": 1,
    "Manipulação e tabulação de dados (numpy, pandas, tidyr,verse, data.table)": 1,
    "Visualização de dados ggplot, matplotlib": 1,
},
{
    "Probabilidade e probabilidade condicional": 1,
    "Independência de eventos, teorema de Bayes e teorema da probabilidade total": 1,
    "Variáveis aleatórias e funções de probabilidade": 1,
    "Principais distribuições de probabilidade discretas e contínuas: distribuição uniforme, distribuição binomial, distribuição Poisson e distribuição normal": 1,
    "Medidas de tendência central e dispersão e correlação": 1,
    "Teorema do limite central": 1,
    "Regra empírica (regra de três sigma) da distribuição normal": 1
},
{
    "Técnicas de classificação: Naive Bayes; Árvores de decisão (algoritmos ID3 e C4.5); Florestas aleatórias (random forest); Máquinas de vetores de suporte (SVM – support vector machines); K vizinhos mais próximos (KNN – K-nearest neighbours)": 1,
    "Avaliação de modelos de classificação: treinamento, teste, validação; validação cruzada": 1, 
    "métricas de avaliação - matriz de confusão, acurácia, precisão, revocação, F1-score e curva ROC": 1,
    "Técnicas de regressão: Árvores de decisão para regressão; Máquinas de vetores de suporte para regressão": 1,
    "Ajuste de modelos dentro e fora de amostra e overfitting": 1,
    "Técnicas de agrupamento: Agrupamento por partição, por densidade e hierárquico": 1,
    "Técnicas de redução de dimensionalidade: Seleção de características (feature selection); Análise de componentes principais (PCA – principal component analysis)": 1,
    "Processamento de linguagem natural: Normalização textual - stop words, estemização, lematização e análise de frequência de termos;":1 ,
    "Rotulação de partes do discurso, part-of-speech tagging": 1, 
    "Modelos de representação de texto - N-gramas, modelos vetoriais de palavras (CBOW, Skip-Gram e GloVe)":1 ,
    "modelos vetoriais de documentos (booleano, TF e TF-IDF, média de vetores de palavras e Paragraph Vector);":1, 
    "Métricas de similaridade textual - similaridade do cosseno, distância euclidiana, similaridade de Jaccard, distância de Manhattan e coeficiente de Dice": 1,
    "Redes neurais convolucionais e recorrentes": 1
},
{
    "Diagramas causais: gráficos acíclicos dirigidos; variáveis confundidoras, colisoras e de mediação": 3,
    "Métodos e técnicas de identificação causal: Métodos experimentais RCT e de identificação quase-experimental": 3,
    "Tipos de viés no processo gerador dos dados e soluções: Sampling bias; Selection bias; Attrition bias; Reporting bias; Measurement bias.":3,
    "Modelos probabilísticos gráficos: cadeias de Markov; filtros de Kalman; Redes bayesianas":4,
    "Testes de hipóteses: teste-z; teste-t; valorp; testes para uma amostra; testes de comparação de duas amostras; teste de normalidade (chi square); e intervalos de confiança.": 1
}
]


tipo_questoes = {key: value for key, value in zip(tipo_topicos, lista_de_sub_topicos)}

import random

# Definindo as classes
classes = list(tipo_questoes['tópico 4'].keys())

# Sorteando cada classe 20 vezes
sorteios = []
for _ in range(1):
    sorteios.extend(random.sample(classes, len(classes)))


for tema in sorteios:

  # topico_sorteado = random.choices(tipo_topicos,[3, 3, 1.44, 1.58, 1.44, 1.33, 3])[0]
  topico_sorteado = 'tópico 4'
  # lista_tema_sorteado = tipo_questoes[topico_sorteado]
  # tema_sorteado = random.choices(list(lista_tema_sorteado.keys()),list(lista_tema_sorteado.values()))[0]
  tema_sorteado = tema

  token = "#####"
# gerar questão que afirmativas positivas


  while True:
    try:
      completion = client.chat.completions.create(
    model="gpt-4-1106-preview",
    messages=[
      {"role": "system", "content": f'''Simule um questão difícil da prova CESGRANRIO. O resultado gerado deve conter 3 partes: a questão, 
                                      a alternativa correta(somente a letra do item, sem parentêses) e uma breve explicação dos itens.
                                      Evite usar palavras tendencioas nas alternativas(ex: nunca, totalmente).
                                      o resultado deve ser separado pelo token {token}. 
                                    '''},
      {"role": "user", "content": "Crie uma questão sobre " + tema}
    ]
  )
      resposta_gpt = completion.choices[0].message.content
      print(resposta_gpt)
      enunciado, resposta_certa, explicacao = resposta_gpt.split(token)
      resposta_certa = re.sub(r"\n| ", "", resposta_certa).upper()
      
      break

    except Exception as e:
      print("############ERRO################")
      print(e) 



  dados_cru = {'id': random.randint(0,10000000),
              'topico': topico_sorteado,
              'tema': tema_sorteado,
              'enunciado': enunciado,
              'resposta_certa': resposta_certa,
              'explicacao': explicacao}


  dados_cru = pd.DataFrame(dados_cru, index=[0])
  data_cru = pd.read_csv('dados_cru.csv', index_col=False)

  data_cru = pd.concat([data_cru, dados_cru])
  data_cru.to_csv('dados_cru.csv', index=False)













