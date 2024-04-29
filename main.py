import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, Input, Output
import mysql.connector

app = Dash(__name__)

# Connect to the database
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Polomaua#pi2',
    database='pi2ubs'
)

#Pesquisar na tabela ubs
query = 'SELECT* from ubs'

df = pd.read_sql(query, con=conn)

conn.close()

fig = px.bar(df, x="vacina_ubs", y="estoque_ubs", color="unidade_ubs", barmode="group")

opcoes = list(df['unidade_ubs'].unique())
opcoes.append("Todas as UBS")

app.layout = html.Div(children=[
    html.H1(children='Busca de vacinas para a comunidade do município de Mauá'),

    html.Div(children='''
        Selecione a unidade básica de saúde:'''),
#Selecionar as unidades UBS
    dcc.Dropdown(opcoes, value='Todas as UBS', id='unidade_ubs'),

    dcc.Graph(
        id='grafico_ubs',
        figure=fig
    )
])
#Selecionar os dados e fazer os graficos
@app.callback(

    Output('grafico_ubs', 'figure'),

    Input('unidade_ubs', 'value')

)

def update_output(value):

    if value == "Todas as UBS":

        fig = px.bar(df, x="vacina_ubs", y="estoque_ubs", color="unidade_ubs", barmode="group")

    else:
#Filtro de UBS
        tabela_filtrada = df.loc[df['unidade_ubs']==value, :]

        fig = px.bar(tabela_filtrada, x="vacina_ubs", y="estoque_ubs", color="unidade_ubs", barmode="group")

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)