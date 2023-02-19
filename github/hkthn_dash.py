import os
import sys
import pandas as pd
import numpy as np
import datetime
from datetime import datetime
from datetime import timedelta
import calendar
import math
import time
import dash
from dash import Dash, html, dcc, Output, Input, State, dash_table
import plotly.express as px
import base64
import io

#model realted libraries

# import sklearn
from sklearn.linear_model import Ridge
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures

external_stylesheets = [
    'https://fonts.googleapis.com/css2?family=Permanent+Marker&family=Roboto&display=swap',
    {
        'href' : 'https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/css/bootstrap.min.css',
        'rel' : 'stylesheet',
        'integrity' : 'sha384-Zenh87qX5JnK2Jl0vWa8Ck2rdkQ2Bzep5IDxbcnCeuOxjzrPF/et3URy9Bv1WTRi',
        'crossorigin' : 'anonymous'
    },
]

external_scripts = [
    'https://polyfill.io/v3/polyfill.min.js?features=default',
    {
        'src':"https://code.jquery.com/jquery-3.6.1.slim.min.js",
        'integrity':"sha256-w8CvhFs7iHNVUtnSP0YKEg00p9Ih13rlL9zGqvLdePA=",
        'crossorigin':"anonymous"
    },
    {
        'src': 'https://kit.fontawesome.com/eaf19bdbb6.js',
        'crossorigin' : 'anonymous'
    },
    {
        'src' : 'https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/js/bootstrap.bundle.min.js',
        'integrity' : 'sha384-OERcA2EqjJCMA+/3y+gxIOqMEjwtxJY7qPCqsdltbNJuaOe923+mo//f6V8Qbsw3',
        'crossorigin' : 'anonymous'
    }
]

app = Dash(__name__, external_scripts=external_scripts, external_stylesheets=external_stylesheets)


app.layout = html.Div(className='row', children=[html.Div(className='col-4', id='fileUploadColumn', children=[html.Div(className='row', style={'justifyContent':'center'}, children=[html.Div(className='col-12', id='meatMachine', children =[html.H1('MEAT GPT')]), html.Div(id='uiColumn', className='col-12', children=[dcc.Upload(id='upload-data',children=html.Div(['Drag CSV Here To Upload...']), multiple=True)]), html.Div(id='output-data-upload'), html.Div(className='col-12', id='submitButton', children=[html.Button('Submit', id='submit-val', n_clicks=0)]), html.Div(className='col-12', id='coef-dropdown')], ), ]), html.Div(className='col-8', id='DataDisplayColumn', children=[html.Div(className='row', children=[html.Div(className='col-12', children=[html.Div(id='dataframe-head', children=[])]), html.Img(src='assets/1.png', id='Logo')]), ]), ])


test_df = ''

@app.callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'))
def extract_contents(contents):
    contents = str(contents)
    content_list = contents.split(',')
    content_type = content_list[0]
    content_string = content_list[1]
    # print(content_type)
    # print(content_string)
    decoded = base64.b64decode(content_string)
    df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
    df.columns = list(df.loc[0].values)
    df.drop(index=0, inplace=True)
    df.reset_index(inplace=True, drop=True)
    print(df.head())
    print(len(df))
    if len(df) > 0:
        global test_df
        test_df = df
        print(test_df.columns)
        return html.Div(className='upload-message', children=[
            'Uploaded'
        ])
    else:
        return html.Div(className='upload-message', children=[
            'Failed'
        ])



@app.callback(
    Output('dataframe-head', 'children'),
    Output('coef-dropdown', 'children'),
    Input('submit-val', 'n_clicks'),
)
def update_output(n_clicks):
    global test_df
    if n_clicks > 0:
        coef_df = ai_model(test_df)
        coef_df.reset_index(inplace=True, drop=True)
        good_data = coef_df.iloc[:10]
        indiv_data = good_data.copy()
        good_data = good_data.iloc[::-1]
        # good_data.sort_values(by='Coefficient', ascending=False, inplace=True)
        good_data_chart = px.histogram(good_data, x=good_data['Coefficient'], y=good_data['Variable'],  template='plotly_white', width=630, height=500)
        good_data_chart.update_layout(
            font=dict(
                        family="verdana",
                        size=12,
                        color='black'
                    ),
            title_x = 0.5,
            title_xanchor='center',
            showlegend=True,
            plot_bgcolor= 'rgba(253, 66, 147, 0.1)',
            paper_bgcolor = 'rgba(0,0,0,0.0)',
            modebar = dict(
                bgcolor = 'rgba(234,240,240,0.2)',
                orientation = 'v'
            ),
            margin = dict(
                l=0,
                r=0,
                b=0,
                t=20
            )
            )
        good_data_chart.update_xaxes(showgrid=True, gridwidth=0.1, gridcolor='rgba(255,255,255,0.1)')
        good_data_chart.update_yaxes(showgrid=True, gridwidth=0.1, gridcolor='rgba(255,255,255,0.1)', visible=True, showticklabels=True)
        good_data_chart.update_layout(transition_duration=500)
        test_df.drop(columns=['Month', 'DOW'], inplace=True)
        test_df = test_df.astype(float)
        mini_df = test_df.sort_values(by='Avg conversions per user')
        mini_df.reset_index(inplace=True, drop=True)
        indiv_var_test = px.line(mini_df, x=mini_df['Avg conversions per user'], y=mini_df[indiv_data.iloc[0]['Variable']], height=400, width=400)
        return html.Div(className='col-12', children=[html.H4(id='graphTitle', children=['Top 10 Variables By Magnitude']), dcc.Graph(figure=good_data_chart)]), html.Div(className='row', children=[html.Div(className='col-12', id='dropDown', children=[dcc.Dropdown(list(indiv_data['Variable']), value=indiv_data['Variable'].values[0],multi=False, id='variableDropdown')]), html.Div(className='col-12', children=[dcc.Graph(figure=indiv_var_test, id='variableChart')])])

@app.callback(
    Output('variableChart', 'figure'),
    Input('variableDropdown', 'value')
)
def update_figure(selected_variable):
    mini_df = test_df.sort_values(by='Avg conversions per user')
    mini_df.reset_index(inplace=True, drop=True)
    fig = px.line(mini_df, x=mini_df['Avg conversions per user'], y=mini_df[selected_variable])
    fig.update_layout(
    font=dict(
                family="verdana",
                size=12,
                color='black'
            ),
    title_x = 0.5,
    title_xanchor='center',
    showlegend=True,
    plot_bgcolor= 'rgba(253, 66, 147, 0.1)',
    paper_bgcolor = 'rgba(0,0,0,0.0)',
    modebar = dict(
        bgcolor = 'rgba(234,240,240,0.2)',
        orientation = 'v'
    ),
    margin = dict(
        l=0,
        r=0,
        b=0,
        t=20
    )
    )
    fig.update_xaxes(showgrid=True, gridwidth=0.1, gridcolor='rgba(255,255,255,0.1)')
    fig.update_yaxes(showgrid=True, gridwidth=0.1, gridcolor='rgba(255,255,255,0.1)', visible=True, showticklabels=True)
    fig.update_layout(transition_duration=500)
    return fig

def ai_model(df):
    df = df.drop(columns=['Month', 'DOW'])
    df = df.astype(float)
    continuous_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(include=[object, bool]).columns.tolist()
    continuous_cols.remove('Avg conversions per user')
    transformers = [
        ('continuous', StandardScaler(), continuous_cols),
        ('categorical', 'passthrough', categorical_cols)
    ]
    ct = ColumnTransformer(transformers)
    ct.fit(df)
    df_scaled = ct.transform(df)
    df_scaled = pd.DataFrame(df_scaled, columns=continuous_cols + categorical_cols)
    X = df_scaled
    y = df['Avg conversions per user']
    alpha = 0.1  # regularization parameter
    model = Ridge(alpha=alpha)
    model.fit(X, y)
    coef = model.coef_
    names = X.columns
    coef_df = pd.DataFrame({'Variable': names, 'Coefficient': coef})
    coef_df = coef_df.reindex(coef_df['Coefficient'].abs().sort_values(ascending=False).index)
    y_pred = model.predict(X)
    mse = mean_squared_error(y, y_pred)
    print(coef_df.head())
    return coef_df

if __name__ == '__main__':
    app.run_server(debug=False)

