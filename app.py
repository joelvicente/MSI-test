import base64
import datetime
import io
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output, State
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import createDataframes as cdf


############################################
# Preparar Dados
############################################
url = 'https://raw.githubusercontent.com/joelvicenteDimatur/CSV/master/MSI-questionario.csv'
df_initial = pd.read_csv(url)

questoes = [] # Aparecerá numa base de dados

for q in cdf.ObtemTodasAsQuestoes(df_initial):
    option = {
        'label': q,
        'value': q
    }
    questoes.append(option)

df = df_initial.drop(columns=['IPAddress', 'RecipientLastName', 'RecipientFirstName', 'RecipientEmail','ExternalReference', 'UserLanguage'])
df = df.drop(columns=['Progress', 'Finished', 'LocationLatitude', 'LocationLongitude'])
df = df.drop(columns=['Status','Duration (in seconds)', 'Q9_3_TEXT'])
df = df.dropna()

# Os valores desta variável poderão ser alterados consoante o input do utilizador
questoes_graficos = ['Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7']

# DataFrame por questao
df_q1 = cdf.DevolveDataFrameQuestao(df, questoes_graficos[0])
df_q2 = cdf.DevolveDataFrameQuestao(df, questoes_graficos[1])
df_q3 = cdf.DevolveDataFrameQuestao(df, questoes_graficos[2])
df_q4 = cdf.DevolveDataFrameQuestao(df, questoes_graficos[3])
df_q5 = cdf.DevolveDataFrameQuestao(df, questoes_graficos[4])
df_q6 = cdf.DevolveDataFrameQuestao(df, questoes_graficos[5])
df_q7 = cdf.DevolveDataFrameQuestao(df, questoes_graficos[6])

#############
## Filtros ##
#############

colunas_filtros = ['Q8','Q9', 'Q10']
df_filters = df[colunas_filtros]
cluster_array = np.random.randint(1, 4, df_filters.shape[0]) ## Só para testar
df_filters = df_filters.assign(Cluster=cluster_array)

filters = {
    "age": None,
    "gender": None,
    "educacao": None,
    "Rendimento": None,
    "Cluster": None
}



# Competitive Profile Matrix & Strategy Canvas
df_profile_final = cdf.CreateDataFrameProfileMatrix(df_q1, df_q2, df_q3,df_filters, filters) 


own_company_rating = df_profile_final['OWN COMPANY'].sum()
print("Own Company Rating: " + str(own_company_rating))
      
competitor_A_rating = df_profile_final['COMPETITOR A'].sum()
print("Competitor A Rating: " + str(competitor_A_rating))

competitor_B_rating = df_profile_final['COMPETITOR B'].sum()
print("Competitor B Rating: " + str(competitor_B_rating))


fig_profile = {
    'data': [
        go.Table(header=dict(values=list(df_profile_final.columns), align='left'),
                cells=dict(
                    values=[df_profile_final['Questao_Q1'], df_profile_final['Ponderacao'].round(2), df_profile_final['OWN COMPANY']        .round(2),df_profile_final['COMPETITOR A'].round(2), df_profile_final['COMPETITOR B'].round(2)],
                    align='left',
                    height=22))
    ],
    'layout': {
        'title': 'Competitive Profile Matrix'
    }
}
                

fig_strategy_canvas =  {
    "data": [
        go.Scatter(x=df_profile_final['Questao_Q1'], y=df_profile_final['OWN COMPANY'],
            mode='lines',
            name='OWN COMPANY'),

        go.Scatter(x=df_profile_final['Questao_Q1'], y=df_profile_final['COMPETITOR A'],
            mode='lines',
            name='COMPETITOR A'),

        go.Scatter(x=df_profile_final['Questao_Q1'], y=df_profile_final['COMPETITOR B'],
            mode='lines',
            name='COMPETITOR B')
    ],
    "layout": go.Layout(
        title = "Strategy Canvas",
        xaxis = {"title": "Factors"},
        yaxis = {"title": "Median" }
    )
}

                    

# SWOT
df_swot = cdf.CreateDataFrameSWOT(df_q4, df_q5,df_filters, filters)

fig_swot = {
    'data': [
        go.Scatter(x=df_swot['Media_Q4'], y=df_swot['Media_Q5'],
            mode='markers',
        name='SWOT')
    ],
    'layout': go.Layout(
        title = "SWOT",
        xaxis = {"range": [-0.5,0.5]},
        yaxis = {"range": [-0.5,0.5]}
    )
}
            

# Customer Window
df_customer_window = cdf.CreateDataFrameCustomerWindow(df_q1, df_q2, df_filters, filters)

fig_customer_window = {
    'data': [
        go.Scatter(x=df_customer_window['Media_Q2'], y=df_customer_window['Media_Q1'],
        mode='markers',
        name='Customer Window')
    ],
    'layout': go.Layout(
        title = "Customer Window",
        xaxis = {"title": "Satisfaction"},
        yaxis = {"title": "Importnace" }
    )
}


# ##################################################################################################################################### 
# -------------------------------------------------------------------------------------------------------------------------------------
# #####################################################################################################################################




######################
# DASH
######################

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', "/assets/styles.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[



    html.Div(className="top",
        children=[
            html.H1(children='AIMS Canvas')
            ],
    ),

    html.Div(className="content", children=[

        dcc.Tabs(id="tabs", children=[


            dcc.Tab(label='Dataset', children=[
                    html.Div([
                        dcc.Upload(
                            id='upload-data',
                            children=html.Div([
                                'Drag and Drop or ',
                                html.A('Select Files')
                            ]),
                            style={
                                'width': '100%',
                                'height': '60px',
                                'lineHeight': '60px',
                                'borderWidth': '1px',
                                'borderStyle': 'dashed',
                                'borderRadius': '5px',
                                'textAlign': 'center',
                                'margin': '10px'
                            },
                            # Allow multiple files to be uploaded
                            multiple=True
                        ),
                        html.Div(id='output-data-upload'),
                    ])

            ]),


            dcc.Tab(label='Definitions', children=[

                 html.Div(className="row", children=[
                    html.H2("Profile Matrix"),
                    html.Div(className="row", children=[
                        html.P('Q - What is important for you'),
                        html.Div(className="two columns no-mg-left", children=[
                            dcc.Dropdown(
                                id='q1',
                                options=questoes,
                                value='Q1'
                            )
                        ])
                    ]),
                    html.Div(className="row", children=[
                        html.P('Q - How do you evaluate it compared to the options available in the XXX area'),
                        html.Div(className="two columns no-mg-left", children=[
                            dcc.Dropdown(
                                id='q2',
                                options=questoes,
                                value='Q2'
                            )
                        ])
                    ]),
                    html.Div(className="row", children=[
                        html.P('Q - Who do you think is best in each category?'),
                        html.Div(className="two columns no-mg-left", children=[
                            dcc.Dropdown(
                                id='q3',
                                options=questoes,
                                value='Q3'
                            )
                        ])
                    ])
                ]),

                html.Div(className="row", children=[
                    html.H2("SWOT"),
                    html.Div(className="row", children=[
                        html.P('Strentghs and Weaknesses'),
                        html.Div(className="two columns no-mg-left", children=[
                            dcc.Dropdown(
                                id='q4',
                                options=questoes,
                                value='Q4'
                            )
                        ])
                    ]),
                    html.Div(className="row", children=[
                        html.P('Opportunities and Threats'),
                        html.Div(className="two columns no-mg-left", children=[
                            dcc.Dropdown(
                                id='q5',
                                options=questoes,
                                value='Q5'
                            )
                        ])
                    ])
                ])
      
            ]),

            dcc.Tab(label='Graphs', children=[
                html.Div([
                    
                    html.H4('Gender'),
                    html.Div(className="row drpClusters", children=[
                        html.Div(className="two columns", children=[
                            dcc.Dropdown(
                                id='drpSexo',
                                options=[
                                    {'label': 'All', 'value': '0'},
                                    {'label': 'Male', 'value': '1'},
                                    {'label': 'Female', 'value': '2'},
                                    {'label': 'Other', 'value': '3'}
                                ],
                                value='Género'
                            ),
                        ]),
                    ]),
                    
                    html.H4('Education'),
                    html.Div(className="row drpClusters", children=[
                        html.Div(className="two columns", children=[
                            dcc.Dropdown(
                                id='drpEducacao',
                                options=[
                                    {'label': 'All', 'value': '0'},
                                    {'label': 'Up to high school', 'value': '1'},
                                    {'label': 'Undergraduate / University', 'value': '2'},
                                    {'label': 'Master level', 'value': '3'},
                                    {'label': 'PhD level', 'value': '4'}
                                ],
                                value='Educacao'
                            ),
                        ]),
                    ]),

                    #html.H4('Income'),
                    #html.Div(className="row drpClusters", children=[
                    #    html.Div(className="two columns", children=[
                    #        dcc.Dropdown(
                    #            id='drpIncome',
                    #            options=[
                    #                {'label': 'All', 'value': '0'},
                    #                {'label': 'Until 600 euros', 'value': '1'},
                    #                {'label': 'From 601 to 1200 euros', 'value': '2'},
                    #                {'label': 'From 1201 to 1800 euros', 'value': '3'},
                    #                {'label': 'From 1801 to 2400 euros', 'value': '4'},
                    #                {'label': 'From 2401 to 3600 euros', 'value': '5'},
                    #                {'label': 'More than 3601 euros', 'value': '6'}
                    #            ],
                    #            value='Income'
                    #        ),
                    #    ]),
                    #]),

                    html.H4('Clusters'),
                    html.Div(className="row drpClusters", children=[
                        html.Div(className="two columns", children=[
                            dcc.Dropdown(
                                id='drpDownClusters',
                                options=[
                                    {'label': 'All', 'value': '0'},
                                    {'label': 'Cluster 1', 'value': '1'},
                                    {'label': 'Cluster 2', 'value': '2'},
                                    {'label': 'Cluster 3', 'value': '3'}
                                ],
                                value='MTL'
                            ),
                        ]),
                    ]),



                    html.Div([

                        # Strategy Canvas
                        html.Div([
                            dcc.Graph(
                                id="scatter_strategy",
                                figure = fig_strategy_canvas
                            )
                            
                        ], className="six columns"),


                        # SWOT
                        html.Div([
                            dcc.Graph(
                                id='swot',
                                figure=fig_swot
                            )
                            
                        ], className="six columns")



                    ], className="row"),


                    html.Div([
                    
                            # Customer Window
                           html.Div([
                                dcc.Graph(
                                    id='customer_window',
                                    figure=fig_customer_window
                                )
                               
                            ], className="six columns"),


                            html.Div([
                                dcc.Graph(
                                    id='profile_matrix',
                                    figure=fig_profile
                                )
                                
                            ], className="six columns"),


                        ], className="row")

                    ], className="graphics"),


            ]),



            dcc.Tab(label='Clusters', children=[
                    dcc.Graph(
                        id='example-graph-2',
                        figure={
                            'data': [
                                {'x': [1, 2, 3], 'y': [2, 4, 3],
                                    'type': 'bar', 'name': 'SF'},
                                {'x': [1, 2, 3], 'y': [5, 4, 3],
                                 'type': 'bar', 'name': u'Montréal'},
                            ]
                        }
                    )
            ]),
    ])
    
    ])



])


# ##################################################################################################################################### 
# -------------------------------------------------------------------------------------------------------------------------------------
# #####################################################################################################################################



def Refresh(filters_new):

    filters = filters_new

    df_q1 = cdf.DevolveDataFrameQuestao(df, questoes_graficos[0])
    df_q2 = cdf.DevolveDataFrameQuestao(df, questoes_graficos[1])
    df_q3 = cdf.DevolveDataFrameQuestao(df, questoes_graficos[2])
    df_q4 = cdf.DevolveDataFrameQuestao(df, questoes_graficos[3])
    df_q5 = cdf.DevolveDataFrameQuestao(df, questoes_graficos[4])
    df_q6 = cdf.DevolveDataFrameQuestao(df, questoes_graficos[5])
    df_q7 = cdf.DevolveDataFrameQuestao(df, questoes_graficos[6])

    # Competitive Profile Matrix
    df_profile_final = cdf.CreateDataFrameProfileMatrix(df_q1, df_q2, df_q3,df_filters, filters) 
    own_company_rating = df_profile_final['OWN COMPANY'].sum()    
    competitor_A_rating = df_profile_final['COMPETITOR A'].sum()
    competitor_B_rating = df_profile_final['COMPETITOR B'].sum()

    # SWOT
    df_swot = cdf.CreateDataFrameSWOT(df_q4, df_q5,df_filters, filters)

    # Customer Window
    df_customer_window = cdf.CreateDataFrameCustomerWindow(df_q1, df_q2, df_filters, filters)

    return [df_profile_final, df_swot, df_customer_window]



def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),

        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns]
        ),

        html.Hr(),  # horizontal line

        # For debugging, display the raw contents provided by the web browser
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])



# ##################################################################################################################################### 
# -------------------------------------------------------------------------------------------------------------------------------------
# #####################################################################################################################################


###############
## Callbacks ##
###############

@app.callback(Output('output-data-upload', 'children'),
              [Input('upload-data', 'contents')],
              [State('upload-data', 'filename'),
               State('upload-data', 'last_modified')])
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children



@app.callback(
    [Output('scatter_strategy', 'figure'),
    Output('swot', 'figure'),
    Output('profile_matrix', 'figure'),
    Output('customer_window', 'figure')],
    [Input('drpSexo', 'value'),
    Input('drpEducacao', 'value'),
    Input('drpDownClusters', 'value'),
    Input('q1', 'value'),
    Input('q2', 'value'),
    Input('q3', 'value'),
    Input('q4', 'value'),
    Input('q5', 'value')]
)
def update_output_sexo(dropValue, dropEducation, dropCluster, q1, q2, q3, q4, q5):

    lista_df = [df_profile_final, df_swot, df_customer_window]

    questoes_graficos[0] = q1
    questoes_graficos[1] = q2
    questoes_graficos[2] = q3
    questoes_graficos[3] = q4
    questoes_graficos[4] = q5

    gender = None
    education = None
    cluster = None

    if dropValue != None:
        if dropValue.isdigit():
            gender = int(dropValue)

    if dropEducation != None:
        if dropEducation.isdigit():
            education = int(dropEducation)

    if dropCluster != None:
        if dropCluster.isdigit():
            cluster = int(dropCluster)
    
    filters_new = {
        "age": None,
        "gender": gender,
        "educacao": education,
        "Rendimento": None,
        "Cluster": cluster
    }

    lista_df = Refresh(filters_new)


    fig_profile = {
        'data': [
            go.Table(header=dict(values=list(df_profile_final.columns), align='left'),
                    cells=dict(
                        values=[lista_df[0]['Questao_Q1'], lista_df[0]['Ponderacao'].round(2), lista_df[0]['OWN COMPANY'].round(2),lista_df[0]['COMPETITOR A'].round(2), lista_df[0]['COMPETITOR B'].round(2)],
                        align='left',
                        height=22))
        ],
        'layout': {
            'title': 'Competitive Profile Matrix'
        }
    }
            

    fig_strategy_canvas = {
        "data": [
            go.Scatter(x=lista_df[0]['Questao_Q1'], y=lista_df[0]['OWN COMPANY'],
                mode='lines',
                name='OWN COMPANY'),

            go.Scatter(x=lista_df[0]['Questao_Q1'], y=lista_df[0]['COMPETITOR A'],
                mode='lines',
                name='COMPETITOR A'),

            go.Scatter(x=lista_df[0]['Questao_Q1'], y=lista_df[0]['COMPETITOR B'],
                mode='lines',
                name='COMPETITOR B')
        ],
        "layout": go.Layout(
            title = "Strategy Canvas",
            xaxis = {"title": "Factors"},
            yaxis = {"title": "Median" }
        )
    }

    
    fig_swot = {
        'data': [
            go.Scatter(x=lista_df[1]['Media_Q4'], y=lista_df[1]['Media_Q5'],
                mode='markers',
            name='SWOT')
        ],
        'layout': go.Layout(
            title = "SWOT",
            xaxis = {"range": [-0.5,0.5]},
            yaxis = {"range": [-0.5,0.5]}
        )
    }


    fig_customer_window = {
        'data': [
            go.Scatter(x=lista_df[2]['Media_Q2'], y=lista_df[2]['Media_Q1'],
            mode='markers',
            name='Customer Window')
        ],
        'layout': go.Layout(
            title = "Customer Window",
            xaxis = {"title": "Satisfaction"},
            yaxis = {"title": "Importnace" }
        )
    }


    return fig_strategy_canvas, fig_swot, fig_profile, fig_customer_window


if __name__ == '__main__':
    app.run_server(debug=True)




