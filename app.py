import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load data
data = pd.read_csv('data.csv')  # Ganti dengan path file Anda jika berbeda

# Layout Dash app
app = dash.Dash(__name__)
app.title = "School Data Visualization"

app.layout = html.Div([
    html.H1("School Data Visualization", style={'textAlign': 'center'}),

    dcc.Tabs([
        dcc.Tab(label='Jumlah Sekolah per Provinsi', children=[
            html.Div([
                dcc.Graph(id='bar-chart-province'),
            ])
        ]),

        dcc.Tab(label='Sebaran Sekolah di Peta', children=[
            html.Div([
                dcc.Graph(id='map-distribution'),
            ])
        ]),
    ])
])


# Callback untuk visualisasi bar chart
@app.callback(
    Output('bar-chart-province', 'figure'),
    Input('bar-chart-province', 'id')  # Dummy input
)
def update_bar_chart(_):
    # Hitung jumlah sekolah per provinsi berdasarkan jenjang
    schools_per_province = (
        data.groupby(['province_name', 'stage'])
        .size()
        .reset_index(name='Jumlah')
    )

    # Buat stacked bar chart
    fig = px.bar(
        schools_per_province,
        x='province_name',
        y='Jumlah',
        color='stage',
        title="Jumlah Sekolah di Setiap Provinsi Berdasarkan Jenjang",
        labels={'Jumlah': 'Jumlah Sekolah', 'province_name': 'Provinsi', 'stage': 'Jenjang Pendidikan'},
        barmode='stack'
    )
    fig.update_layout(xaxis_title='Provinsi', yaxis_title='Jumlah Sekolah', legend_title='Jenjang Pendidikan')
    return fig


# Callback untuk visualisasi sebaran peta
@app.callback(
    Output('map-distribution', 'figure'),
    Input('map-distribution', 'id')  # Dummy input
)
def update_map(_):
    # Filter data dengan kolom latitude dan longitude
    map_data = data[['school_name', 'stage', 'status', 'lat', 'long']].dropna()

    # Buat scatter map
    fig = px.scatter_mapbox(
        map_data,
        lat='lat',
        lon='long',
        color='stage',
        hover_name='school_name',
        hover_data={'lat': False, 'long': False, 'status': True},
        title="Sebaran Sekolah Berdasarkan Jenjang Pendidikan",
        mapbox_style='open-street-map',
        zoom=4
    )
    fig.update_layout(legend_title='Jenjang Pendidikan')
    return fig


# Run app
if __name__ == '__main__':
    app.run_server(debug=True)
