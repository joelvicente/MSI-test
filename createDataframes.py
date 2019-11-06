import pandas as pd

def CreateDataFrameProfileMatrix(df_q1, df_q2, df_q3, df_filters, filters):
  # Cria DataFrame preparado para gerar a tabela do Profile Matrix
  # Recebe 3 dataframes: das questões 1 ao 3 e recebe o dataframe dos filtros (idade, género, educação, rendimento, ...)

  # Q1
  df_q1_filtrado = DevolveDataFrameFiltrado(df_q1, df_filters,filters)
  medias = []
  colunas = list(df_q1_filtrado)
  for col in colunas:
    media = df_q1_filtrado[col].mean()
    medias.append([col, media, media / 5]) # divide por 5 pois só existem 5 possibilidades, pelo que 5 corresponde a 100% e 1 a 20%
   
  df_profile = pd.DataFrame(medias, columns = ['Questao_Q1', 'Media_Q1', 'Percentagem'])
  df_profile['Ponderacao'] = df_profile['Percentagem'] / df_profile['Percentagem'].sum()
  
  
  
  # Q2
  df_q2_filtrado = DevolveDataFrameFiltrado(df_q2, df_filters,filters)
  medias_q2 = []
  colunas_q2 = list(df_q2_filtrado)
  for col in colunas_q2:
    media = df_q2_filtrado[col].mean()
    medias_q2.append([col, media])
  
  df_profile_Q2 = pd.DataFrame(medias_q2, columns = ['Questao_Q2', 'Media_Q2'])
  result = pd.concat([df_profile, df_profile_Q2], axis=1, sort=False)
  result['OWN COMPANY'] = result['Ponderacao'] * result['Media_Q2']
  
  
  
  #Q3
  df_q3_filtrado = DevolveDataFrameFiltrado(df_q3, df_filters,filters)
  medias_q3 = []
  colunas_q3 = list(df_q3_filtrado)
  for col in colunas_q3:
    own_project = df_q3_filtrado[col][df_q3_filtrado[col] == 1].count()
    competitor_A = df_q3_filtrado[col][df_q3_filtrado[col] == 2].count()
    competitor_B = df_q3_filtrado[col][df_q3_filtrado[col] == 3].count()
    equally_good = df_q3_filtrado[col][df_q3_filtrado[col] == 4].count()
    medias_q3.append([col, own_project,competitor_A,competitor_B,equally_good])
   
  df_profile_Q3 = pd.DataFrame(medias_q3, columns = ['Questao_Q3', 'OWN COMPANY', 'COMPETITOR A', 'COMPETITOR B', 'EQUALLY GOOD'])
  n_repostas = df_q3.shape[0]
  
  df_profile_Q3['OWN COMPANY_%'] = df_profile_Q3['OWN COMPANY'] / n_repostas
  df_profile_Q3['COMPETITOR A_%'] = df_profile_Q3['COMPETITOR A'] / n_repostas
  df_profile_Q3['COMPETITOR B_%'] = df_profile_Q3['COMPETITOR B'] / n_repostas
  df_profile_Q3['EQUALLY GOOD_%'] = df_profile_Q3['EQUALLY GOOD'] / n_repostas
  
  df_profile_Q3['GAP Proj-A'] = df_profile_Q3['OWN COMPANY_%'] - df_profile_Q3['COMPETITOR A_%']
  df_profile_Q3['GAP Proj-B'] = df_profile_Q3['OWN COMPANY_%'] - df_profile_Q3['COMPETITOR B_%']
  
  # DataFrame com os dados necessários para terminar o Profile Matrix
  df_all_calculations = pd.concat([result, df_profile_Q3[['Questao_Q3', 'GAP Proj-A', 'GAP Proj-B']]], axis=1, sort=False)
  
  df_all_calculations['COMPETITOR A'] = df_all_calculations['OWN COMPANY'] - df_all_calculations['GAP Proj-A']
  df_all_calculations['COMPETITOR B'] = df_all_calculations['OWN COMPANY'] - df_all_calculations['GAP Proj-B']
  
  # DataFrame final. Tem apenas os valores que compõem o Profile Matrix sem as colunas auxiliares de cálculo
  df_profile_final = df_all_calculations.drop(columns=['Media_Q1', 'Percentagem', 'Questao_Q2', 'Media_Q2', 'Questao_Q3', 'GAP Proj-A','GAP Proj-B' ])
  
  return df_profile_final


def CreateDataFrameSWOT(df_q4, df_q5,df_filters, filters):
  # Cria um DataFrame preparado para gerar o gráfico SWOT
  # Q4
  df_q4_filtrado = DevolveDataFrameFiltrado(df_q4, df_filters,filters)
  
  medias_q4 = []
  colunas_q4 = list(df_q4_filtrado)
  for col in colunas_q4:
    media = df_q4_filtrado[col].mean()
    medias_q4.append([col, media - 4])
  

  df_profile_Q4 = pd.DataFrame(medias_q4, columns = ['Questao_Q4', 'Media_Q4'])

  
  # Q5
  df_q5_filtrado = DevolveDataFrameFiltrado(df_q5, df_filters,filters)
  
  medias_q5 = []
  colunas_q5 = list(df_q5_filtrado)
  for col in colunas_q5:
    media = df_q5_filtrado[col].mean()
    medias_q5.append([col, media - 4])
  
  df_profile_Q5 = pd.DataFrame(medias_q5, columns = ['Questao_Q5', 'Media_Q5'])

  
  df_q4_q5 = df_profile_Q4.join(df_profile_Q5)# pd.concat([df_profile_Q4, df_profile_Q5], axis=1, sort=False)
  
  return df_q4_q5




def CreateDataFrameCustomerWindow(df_q1, df_q2, df_filters, filters):
  # Cria DataFrame preparado para gerar a tabela do Customer Window
  # Recebe 3 dataframes: das questões 1 ao 3 e recebe o dataframe dos filtros (idade, género, educação, rendimento, ...)


  # Q1
  df_q1_filtrado = DevolveDataFrameFiltrado(df_q1, df_filters,filters)
  medias = []
  colunas = list(df_q1_filtrado)
  for col in colunas:
    media = df_q1_filtrado[col].mean()
    medias.append([col, media, media / 5]) # divide por 5 pois só existem 5 possibilidades, pelo que 5 corresponde a 100% e 1 a 20%
   
  df_profile = pd.DataFrame(medias, columns = ['Questao_Q1', 'Media_Q1', 'Percentagem'])
  
  
  # Q2
  df_q2_filtrado = DevolveDataFrameFiltrado(df_q2, df_filters,filters)
  medias_q2 = []
  colunas_q2 = list(df_q2_filtrado)
  for col in colunas_q2:
    media = df_q2_filtrado[col].mean()
    medias_q2.append([col, media])
  
  df_profile_Q2 = pd.DataFrame(medias_q2, columns = ['Questao_Q2', 'Media_Q2'])
  
  
  # DataFrame com os dados necessários para terminar o Profile Matrix
  df_all_calculations = pd.concat([df_profile, df_profile_Q2], axis=1, sort=False)
  df_all_calculations['Media_Q1'] = df_all_calculations['Media_Q1'] - 3 # Para centralizar os dados
  df_all_calculations['Media_Q2'] = df_all_calculations['Media_Q2'] - 3


  return df_all_calculations

def DevolveDataFrameFiltrado(df_nao_filtrado, df_filters, filters):
  # Recebe um dataframe por filtrar, o dataframe com as colunas de filtro, e os parâmetros por filtrar. Isto faz uma transformação onde aplica as condições do filtro e devolve o mesmo df do nao filtrado mas com menos linhas
  
  df_completo = pd.concat([df_nao_filtrado, df_filters], axis=1, sort=False)
  
  
  if filters['age'] != None:
    if filters['age'] > 0:
      df_completo = df_completo[df_completo['Q8'] == filters['age']]
    
  if filters['gender'] != None:
    if filters['gender'] > 0:
      df_completo = df_completo[df_completo['Q9'] == filters['gender']] 

  if filters['educacao'] != None:
    if filters['educacao'] > 0:
      df_completo = df_completo[df_completo['Q10'] == filters['educacao']] 

  if filters['Rendimento'] != None:
    if filters['Rendimento'] > 0:
      df_completo = df_completo[df_completo['Q9'] == filters['Rendimento']] 

  if filters['Cluster'] != None:
    if filters['Cluster'] > 0:
      df_completo = df_completo[df_completo['Cluster'] == filters['Cluster']]
  
  df_final = df_completo.drop(columns=list(df_filters))
  
  return df_final


def ObtemSlicePerguntas(df,questao):
  colunas = list(df)
  colunas_questao = []
  for x in colunas:
    if ((questao + "_") in x):
      colunas_questao.append(x)
      
  return slice(colunas_questao[0], colunas_questao[-1])

def DevolveDataFrameQuestao(df, questao):
  return df.loc[:, ObtemSlicePerguntas(df,questao)]

def ObtemTodasAsQuestoes(colunas):
  lista_questoes = []
  for col in colunas:
    _index = col.find('_')
    
    q = ''
    if _index > 0:
      q = col[0:_index]
    else:
      q = col
    
    
    if q[0] == 'Q':
      if q not in lista_questoes:
        lista_questoes.append(q)
  
  return lista_questoes