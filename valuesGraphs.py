import pandas as pd

def get_redundant_pairs(df):
    '''Get diagonal and lower triangular pairs of correlation matrix'''
    pairs_to_drop = set()
    cols = df.columns
    for i in range(0, df.shape[1]):
        for j in range(0, i+1):
            pairs_to_drop.add((cols[i], cols[j]))
    
    for i in range(0, df.shape[1]):
        for j in range(0, df.shape[1]):
          if cols[i][0:2] == cols[j][0:2]:
            pairs_to_drop.add((cols[i], cols[j]))
    return pairs_to_drop


def get_top_abs_correlations(df):
    au_corr = df.corr().abs().unstack()
    labels_to_drop = get_redundant_pairs(df)
    au_corr = au_corr.drop(labels=labels_to_drop).sort_values(ascending=False)
    
    return au_corr


# GROWTH
# x: Positive
# y: Positive

def Get_Growth_Columns(df_medias):
  df_growth_medians = df_medias[(df_medias['Media_Q4'] > 0) & (df_medias['Media_Q5'] > 0)]
  questoes4 = df_growth_medians['Questao_Q4'].tolist()
  questoes5 = df_growth_medians['Questao_Q5'].tolist()
  joined_list = questoes4 + questoes5
  return joined_list



# CONTROL
# x: Positive
# y: Negative

def Get_Control_Columns(df_medias):
  df_control_medians = df_medias[(df_medias['Media_Q4'] > 0) & (df_medias['Media_Q5'] < 0)]
  questoes4 = df_control_medians['Questao_Q4'].tolist()
  questoes5 = df_control_medians['Questao_Q5'].tolist()
  joined_list = questoes4 + questoes5
  return joined_list



# DEFENSIVE
# x: Negative
# y: Negative

def Get_Defensive_Columns(df_medias):
  df_defensive_medians = df_medias[(df_medias['Media_Q4'] < 0) & (df_medias['Media_Q5'] < 0)]
  questoes4 = df_defensive_medians['Questao_Q4'].tolist()
  questoes5 = df_defensive_medians['Questao_Q5'].tolist()
  joined_list = questoes4 + questoes5
  return joined_list



# IMPROVE
# x: Negative
# y: Positive

def Get_Improve_Columns(df_medias):
  df_improve_medians = df_medias[(df_medias['Media_Q4'] < 0) & (df_medias['Media_Q5'] > 0)]
  questoes4 = df_improve_medians['Questao_Q4'].tolist()
  questoes5 = df_improve_medians['Questao_Q5'].tolist()
  joined_list = questoes4 + questoes5
  return joined_list