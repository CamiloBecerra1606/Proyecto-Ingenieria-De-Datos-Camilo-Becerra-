import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import psycopg2
import pandas as pd

# Conexión a la base de datos PostgreSQL
def connect_to_db():
    conn = psycopg2.connect(
        host="localhost",  # Nombre del host (o dirección IP) de tu servidor PostgreSQL
        database="Proyecto",
        user="postgres",
        password="1606"
    )
    return conn

# Crear la aplicación Dash
app = dash.Dash(__name__)

# Layout de la aplicación
app.layout = html.Div([
    html.H1("Análisis de Datos de Estudiantes"),
    dcc.Dropdown(
        id='analysis-dropdown',
        options=[
            {'label': 'Segmentación demográfica y sociodemográfica', 'value': 'demographic'},
            {'label': 'Análisis de tendencias de matriculación', 'value': 'enrollment'},
            {'label': 'Evaluación de la vulnerabilidad y necesidades especiales', 'value': 'vulnerability'},
            {'label': 'Análisis de la movilidad y migración estudiantil', 'value': 'mobility'}
        ],
        value=None
    ),
    dcc.Graph(id='analysis-graph')
])

# Callback para mostrar el análisis seleccionado
@app.callback(
    Output('analysis-graph', 'figure'),
    [Input('analysis-dropdown', 'value')]
)
def display_analysis(analysis):
    conn = connect_to_db()
    if analysis == 'demographic':
        df = pd.read_sql("SELECT edad, genero, estrato, lugar FROM Persona", conn)
        fig = px.histogram(df, x="edad", color="genero", facet_row="estrato", facet_col="lugar", height=600)
    elif analysis == 'vulnerability':
        df = pd.read_sql("SELECT pob_vulnerable, COUNT(*) as num_students FROM Persona GROUP BY pob_vulnerable", conn)
        fig = px.bar(df, x="pob_vulnerable", y="num_students")
    elif analysis == 'mobility':
        df = pd.read_sql("SELECT lugar, COUNT(*) as num_students FROM Persona GROUP BY lugar", conn)
        fig = px.area(df, x="lugar", y="num_students", title="Número de estudiantes por lugar")
    else:
        fig = {}
    conn.close()
    return fig

if __name__ == '__main__':
    app.run_server(debug=True, port ='8085')
