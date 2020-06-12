import json

import dash

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table

from plotly import tools
import plotly.graph_objs as go
import plotly.figure_factory as ff

import pandas as pd
import numpy as np

import re

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

df = pd.read_csv('PorePermDensity.csv')
df = df.reset_index()
df = df.rename(columns={'index': 'Sample Number'})

gamma_df = pd.read_csv('CoreGamma.csv')

available_indicators = ['Kinf','Porosity','Gdensity','Depth']

app.layout = html.Div([
    html.Div([
        html.Div([
            html.H1(
                'Plug Data Explorer',
                className='eight columns'
            ),
            html.Img(
                src="https://images.squarespace-cdn.com/content/v1/58a4b31dbebafb6777c575b4/1552228857222-IT0RG669ZUOLLLR597EU/ke17ZwdGBToddI8pDm48kLPswmMOqQZ9-Q6KHLjvbpZ7gQa3H78H3Y0txjaiv_0fDoOvxcdMmMKkDsyUqMSsMWxHk725yiiHCCLfrh8O1z5QPOohDIaIeljMHgDF5CVlOqpeNLcJ80NK65_fV7S1UcaEU9usEQgaPMYSSHCLDdjcUDfwtSR5qjoqJbWx-aCIZDqXZYzu2fuaodM4POSZ4w/swung_round_no_text.png?format=200w",
                className='one columns',
                style={
                    'height': '50',
                    'float': 'right',
                    'position': 'relative',
                },
            ),
        ],className='row'),
        html.Div([
            html.Label('X Axis'),
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value=available_indicators[1]
            ),
            dcc.RadioItems(
                id='xaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],
        style={'width': '30%', 'display': 'inline-block'}),

        html.Div([
            html.Label('Y Axis'),
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value=available_indicators[0]
            ),
            dcc.RadioItems(
                id='yaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Log',
                labelStyle={'display': 'inline-block'}
            )
        ],style={'width': '30%','display': 'inline-block'}),
    ]),

    html.Div([
        html.Label('Select Cores to Include'),
        dcc.Graph(id='cross-plot'),
    ], style={'width': '60%', 'display': 'inline-block', 'padding': '0 20'}),


    html.Div([
        html.Label('Core Gamma'),
        dcc.Graph(id='well-log-plot'),
    ], style={'display': 'inline-block', 'width': '40%','float': 'right' }),
])

@app.callback(
    Output('cross-plot', 'figure'),
    [Input('xaxis-column', 'value'),
     Input('yaxis-column', 'value'),
     Input('xaxis-type', 'value'),
     Input('yaxis-type', 'value'),
     ])
def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type):

    dff = df 

    traces = []

    df_by_color = dff
    traces.append(dict(
        x=df_by_color[xaxis_column_name],
        y=df_by_color[yaxis_column_name],
        customdata=df_by_color['Sample Number'],
        text=['Sample Number: {}<br>Kinf: {}<br>Porosity: {}<br>Grain Density: {}<br>Depth: {}'.format(int(n), lf, d, c, ltrf) for n, lf, d, c, ltrf in zip(df_by_color['Sample Number'],df_by_color['Kinf'], df_by_color['Porosity'], df_by_color['Gdensity'],df_by_color['Depth'] ) ],
        hovertemplate = '%{text}<extra></extra>', # the extra bit is for the area beside the main tooltip.  make it blank so name doesn't appear
        mode='markers',
        marker={
            'size': 15,
            'opacity': 0.5,
        },
        hoverinfo='skip',
    ))
    return {
        'data': traces,
        'layout': dict(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear' if xaxis_type == 'Linear' else 'log'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear' if yaxis_type == 'Linear' else 'log'
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }

@app.callback(
    Output('well-log-plot', 'figure'),
    [Input('cross-plot', 'selectedData')])
def generate_log_curves(selectedData):

    height=500
    width=300
    bg_color='white'
    font_size=10
    tick_font_size=8
    line_width=1.0

    selectedpoints = df['Sample Number']
    ind1 = selectedpoints.index.values

    if selectedData is not None:

        for selected_data in [selectedData]:

            if selected_data and selected_data['points']:
                selectedpoints, ind1, ind2 = np.intersect1d(selectedpoints,
                    [p['customdata'] for p in selected_data['points']], return_indices=True)

    fig = tools.make_subplots(rows=1, cols=1,
                              shared_yaxes=True,
                              horizontal_spacing=0)

    fig.append_trace(go.Scatter(
        x=gamma_df['Gamma'],
        y=gamma_df['Depth'],
        xaxis='x',
        name='CoreGamma',
        line={'width': line_width,
                'dash': 'dashdot'},
        showlegend = False,
        hoverinfo='skip',
        
    ), row=1, col=1)
    fig.append_trace(go.Scatter(
        x=df['Kinf'],
        y=df['Depth'],
        xaxis='x2',
        selectedpoints= ind1, #selected_indices,
        name='PERM-plug',
        mode='markers',
        hovertemplate=
            "Depth: %{y:.2f}m<br>" +
            "PERM: %{x:.3e}md<br>" +
            "<extra></extra>",
        marker={
            'size': 8,
            'line': {'width': 0.5, 'color': 'white'}
        },
        unselected={
            'marker': { 'opacity': 0.2 },
            # make text transparent when not selected
            'textfont': { 'color': 'rgba(0, 0, 0, 0)' }
        },
        showlegend = False,
    ),row=1, col=1)
    
    fig['layout']['xaxis'].update(
        title='Gamma',
        type='log',
        side='bottom'
    )
    fig['layout'].update(
        xaxis2={"title": "Kinf", "side": "top"},
    )
    # y axis title
    fig['layout']['yaxis'].update(
        title='Depth<br>[m]',
        autorange='reversed'
    )

    fig['layout'].update(

        plot_bgcolor=bg_color,
        paper_bgcolor=bg_color,
        hovermode='closest',
        legend={
            'font': {
                'size': tick_font_size
            }
        },
        margin=go.layout.Margin(
            l=20,r=20, t=10, b= 40
        )
    )

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)