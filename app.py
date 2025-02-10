import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load data
data = pd.read_csv('data_pengangguran.csv') 

# Convert "Periode" to string for consistency
data['Periode'] = data['Periode'].astype(str)

# Layout Dash app
app = dash.Dash(__name__)
app.title = "Visualisasi Data Pengangguran"

app.layout = html.Div([
    html.H1("Visualisasi Data Pengangguran", style={'textAlign': 'center'}),
    
    html.Div([
        dcc.Graph(id='bar-chart-pengangguran', style={'height': '60vh', 'width': '50%'}),
        dcc.Graph(id='pie-chart-pendidikan', style={'height': '60vh', 'width': '50%'})
    ], style={'display': 'flex'}),
    
    dcc.Graph(id='line-chart-trend', style={'height': '60vh'}),
    dcc.Graph(id='stacked-bar-chart', style={'height': '60vh'}),
])

# Bar chart: Perbandingan pengangguran berdasarkan tingkat pendidikan
@app.callback(
    Output('bar-chart-pengangguran', 'figure'),
    Input('bar-chart-pengangguran', 'id')
)
def update_bar_chart(_):
    pendidikan_columns = data.columns[2:-1]  # Ambil kolom pendidikan saja
    pendidikan_counts = data[pendidikan_columns].sum().reset_index()
    pendidikan_counts.columns = ['Tingkat Pendidikan', 'Jumlah']
    
    fig = px.bar(
        pendidikan_counts,
        x='Tingkat Pendidikan',
        y='Jumlah',
        title="Jumlah Pengangguran Berdasarkan Tingkat Pendidikan",
        labels={'Jumlah': 'Jumlah Pengangguran', 'Tingkat Pendidikan': 'Tingkat Pendidikan'},
        text_auto=True
    )
    
    return fig

# Line chart: Tren pengangguran dari tahun ke tahun
@app.callback(
    Output('line-chart-trend', 'figure'),
    Input('line-chart-trend', 'id')
)
def update_line_chart(_):
    trend_data = data.groupby('Periode')['Total'].sum().reset_index()
    
    fig = px.line(
        trend_data,
        x='Periode',
        y='Total',
        title="Tren Pengangguran dari Tahun ke Tahun",
        markers=True,
        labels={'Total': 'Total Pengangguran', 'Periode': 'Tahun'}
    )
    
    return fig

# Pie chart: Proporsi pengangguran berdasarkan tingkat pendidikan
@app.callback(
    Output('pie-chart-pendidikan', 'figure'),
    Input('pie-chart-pendidikan', 'id')
)
def update_pie_chart(_):
    pendidikan_columns = data.columns[2:-1]
    pendidikan_counts = data[pendidikan_columns].sum().reset_index()
    pendidikan_counts.columns = ['Tingkat Pendidikan', 'Jumlah']
    
    fig = px.pie(
        pendidikan_counts,
        names='Tingkat Pendidikan',
        values='Jumlah',
        title="Proporsi Pengangguran Berdasarkan Tingkat Pendidikan"
    )
    
    return fig

# Stacked bar chart: Perbandingan tingkat pendidikan setiap tahun
@app.callback(
    Output('stacked-bar-chart', 'figure'),
    Input('stacked-bar-chart', 'id')
)
def update_stacked_bar_chart(_):
    pendidikan_columns = data.columns[2:-1]
    stacked_data = data.melt(id_vars=['Periode'], value_vars=pendidikan_columns, var_name='Tingkat Pendidikan', value_name='Jumlah')
    
    fig = px.bar(
        stacked_data,
        x='Periode',
        y='Jumlah',
        color='Tingkat Pendidikan',
        title="Perbandingan Tingkat Pendidikan Setiap Tahun",
        labels={'Jumlah': 'Jumlah Pengangguran', 'Periode': 'Tahun'},
        barmode='stack'
    )
    
    return fig

# Run app
if __name__ == '__main__':
    app.run_server(debug=True)
