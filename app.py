'''
file: app.py
author: @vincit0re @yashanand1000
brief: This file contains the main code flow for the web portal which is a flask app.
date: 2023-04-27
'''
# import dependencies
from dependencies import *
from utils import *   # import all the helper unctions and prepared data

# define app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG], meta_tags=[
    {"name": "viewport", "content": "width=device-width, initial-scale=1"},
    {"property": "og:title", "content": "India Covid-19 Dashboard"},
    {"property": "og:type", "content": "website"},
    {"property": "og:url", "content": "https://India-covid19-dashboard.herokuapp.com/"},
    {"property": "og:image",
        "content": "https://live.staticflickr.com/65535/51830937951_6dd1027bee_k.jpg"},
    {"property": "og:description",
     "content": "A dashboard that shows the overall statistics of Covid-19 in the India."}
])
app.title = "Data Visualization Project: Covid-19 Visualization (India)"
server = app.server


world_total_cases = df_cases_sum.iloc[-1]
india_total_cases = df_covid_cases_deaths['Total Confirmed'].iloc[0]
world_total_deaths = df_death_sum.iloc[-1]
india_total_deaths = df_covid_global_transposed['India'].iloc[-1]

left_card_body = dbc.CardBody([
    html.H3(f"Total Cases in World: {world_total_cases}", style={
            "color": "orange", "text-align": "center"}),
    html.H3(f"Total Cases in India: {india_total_cases}", style={
            "color": "orange", "text-align": "center"})
])

right_card_body = dbc.CardBody([
    html.H3(f"Total Deaths in World: {world_total_deaths}", style={
            "color": "red", "text-align": "center"}),
    html.H3(f"Total Deaths in India: {india_total_deaths}", style={
            "color": "red", "text-align": "center"})
])

left_card_body_1 = dbc.CardBody(
    [html.H2(['Global Covid-19'], style={'font-size': '30px', 'font-weight': 'bold', 'text-align': 'center'}),
     dcc.Tabs(
        [dcc.Tab(label="Global Cases",                        children=[html.Div([html.Label(['Select Country'], style={'font-weight': 'bold'}),
                                                                                  dcc.Dropdown(
            id='country-dropdown-cases',
            options=[{'label': i, 'value': i}
                     for i in features_cases],
            value=['India', 'Germany'],
            multi=True,
            style={'background-color': '#282828'}
        )
        ],
            style={'padding': '40px'}
        ),

            dcc.Graph(
            id='global-covid-cases',
            config={'displaylogo': False,
                    'displayModeBar': False}
        )

        ],
            style=tab_style,
            selected_style=tab_selected_style
        ),
            dcc.Tab(label="Global Deaths",
                    children=[html.Div([html.Label(['Select Country'], style={'font-weight': 'bold'}),
                                        dcc.Dropdown(
                        id='country-dropdown',
                        options=[{'label': i, 'value': i}
                              for i in features_deaths],
                        value=['India', 'Germany'],
                        multi=True,
                        style={'background-color': '#282828'}
                    )

                    ],
                        style={'padding': '40px'}
                    ),

                        dcc.Graph(
                        id='global-covid',
                        config={'displaylogo': False,
                                'displayModeBar': False}
                    )

                    ],
                    style=tab_style,
                    selected_style=tab_selected_style
                    )
        ],
        style=tabs_styles
    )

    ]
)

right_card_body_1 = dbc.CardBody(
    [html.H2(['Headlines | Covid-19 as of Today In all over World'], style={'font-size': '30px', 'font-weight': 'bold', 'text-align': 'center'}),
     html.Div(
        id="news",
        children=[html.Ul(className='timeline', children=[html.Li(i) for i in news])
                  ]
    )

    ],
    style={'height': '720px', 'overflow': 'auto'}
)

left_body_card_2 = dbc.Card(
    dbc.CardBody(
        [

            dcc.Graph(id='covid-pie-v',
                      figure={'data': [
                          go.Pie(
                              labels=[
                                  'Complete', '1st Dose', '2nd Dose'],
                              values=vaccinated_values
                          )
                      ], 'layout': go.Layout(title='Vaccination Stats', paper_bgcolor='#282828', plot_bgcolor='#282828', font=dict(color='#adafae'))}, config={'displaylogo': False, 'displayModeBar': False}),

            dcc.Graph(id='covid-pie-t',
                      figure={'data': [
                          go.Pie(
                              labels=[
                                  'Total Confirmed', 'Total Recovered', 'Total Deceased'],
                              values=pillar_values
                          )
                      ], 'layout': go.Layout(title='Testing Stats', paper_bgcolor='#282828', plot_bgcolor='#282828', font=dict(color='#adafae'))}, config={'displaylogo': False, 'displayModeBar': False})

        ]
    )
)

right_body_card_2 = dbc.Card(
    dbc.CardBody(
        [
            html.H2(['Heatmap for Deaths in Indian States'], style={
                    'font-size': '30px', 'font-weight': 'bold', 'text-align': 'center'}),
            dcc.Graph(id='covid-heat-d', figure=fig_deaths,
                      config={'displaylogo': False, 'displayModeBar': False}),
            dcc.Graph(id='covid-heat-c', figure=fig_cases,
                      config={'displaylogo': False, 'displayModeBar': False})
        ]
    )
)


# layout
app.layout = dbc.Container([

    html.Div([
        html.H1(['Data Visualization Project: Covid-19 Visualization (India)'],
                style={'text-align': 'center', 'color': '#adafae'}),
        html.Hr(style={'background-color': 'rgba(61,61,61,0.5)'}),
    ], style={'margin-top': '10px'}),



    dbc.Row([
        dbc.Col(left_card_body, md=6),
        dbc.Col(right_card_body, md=6)
    ], align="center", style={"margin-bottom": "20px"}),

    dbc.Row([
        dbc.Col(left_card_body_1, md=8),
        dbc.Col(right_card_body_1, md=4)],
        style={'margin-bottom': '20px'}, align="center"
    ),

    dbc.Row(
        [
            dbc.Col(
                [
                    dbc.Card(
                        [
                            dbc.CardHeader(
                                html.H2('Covid-19 Vaccination Progress')),
                            left_body_card_2,
                        ]
                    )
                ], md=4
            ),
            dbc.Col(
                [
                    dbc.Card(
                        [
                            dbc.CardHeader(
                                html.H2('Heatmap for Deaths in Indian States')),
                            right_body_card_2,
                        ]
                    )
                ], md=8
            ),
        ], style={'margin-bottom': '20px'},
        align="center",
    ),


    dbc.Row(
        [

            dbc.Col(
                [
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H2(['Covid-19 Transmission Rate'], style={
                                        'font-size': '30px', 'font-weight': 'bold', 'text-align': 'center'}),
                                dcc.Graph(id='covid-bar-transmission', figure=fig_transmission,
                                          config={'displaylogo': False, 'displayModeBar': False})


                            ]
                        )
                    )

                ], md=6
            ),
            dbc.Col(
                [
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H2(['Planned Daily Hospitalization Capacity for Covid-19 Patients'], style={
                                        'font-size': '30px', 'font-weight': 'bold', 'text-align': 'center'}),
                                dcc.Graph(id='covid-hospital',
                                          figure={'data': [
                                              go.Scatter(
                                                  x=df_covid_hospital_cap['date'],
                                                  y=df_covid_hospital_cap['plannedCapacityByPublishDate'],
                                                  mode='lines',
                                              )
                                          ], 'layout': go.Layout(paper_bgcolor='#282828', plot_bgcolor='#282828', font=dict(color='#adafae'), yaxis=dict(title='Capacity', gridcolor='rgba(61,61,61,0.2)'), xaxis=dict(gridcolor='rgba(61,61,61,0.2)'))}, config={'displaylogo': False, 'displayModeBar': False})

                            ]
                        )
                    )

                ], md=6
            ),
        ], style={'margin-bottom': '20px'},
        align="center",
    ),


    dbc.Row(
        [

            dbc.Col(
                [
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H2(['Covid-19 Patients Data for Indian States'], style={
                                        'font-size': '30px', 'font-weight': 'bold', 'text-align': 'center'}),
                                html.Div([
                                    html.Label(['Select Region'], style={
                                               'font-weight': 'bold', 'margin-right': '5px'}),
                                    dcc.Dropdown(id='selectedRegion',
                                                 options=[
                                                     {'label': i, 'value': i} for i in df_region_covid['areaName'].unique()],
                                                 value='Rajasthan',
                                                 style={'background-color': '#282828', 'margin-right': '5px'})
                                ], style={'width': '50%', 'display': 'inline-block'}),
                                html.Div([
                                    html.Label(['Select Parameter'], style={
                                               'font-weight': 'bold', 'margin-left': '5px'}),
                                    dcc.Dropdown(id='selectedParameter',
                                                 options=[{'label': 'Cases', 'value': 'cumCasesBySpecimenDate'}, {
                                                     'label': 'Deaths', 'value': 'cumDeaths60DaysByDeathDate'}],
                                                 value='cumDeaths60DaysByDeathDate',
                                                 style={'background-color': '#282828', 'margin-left': '5px'})
                                ], style={'width': '50%', 'display': 'inline-block'}),
                                dcc.Graph(
                                    id='region-graph', config={'displaylogo': False, 'displayModeBar': False})


                            ]
                        )
                    ),


                ], md=12
            )

        ], style={'margin-bottom': '20px'}
    ),



    dbc.Row(
        [

            dbc.Col(
                [
                    dbc.Card([
                        dbc.CardBody(
                            [
                                html.H2(['Covid-19 Age Demographics'], style={
                                        'font-size': '30px', 'font-weight': 'bold', 'text-align': 'center'}),
                                dcc.Graph(id='covid-age', figure=update_graph_age(),
                                          config={'displaylogo': False, 'displayModeBar': False})

                            ]
                        )
                    ], style={'margin-bottom': '20px'}),
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H2(['Covid-Patients Occupied MV Beds'], style={
                                        'font-size': '30px', 'font-weight': 'bold', 'text-align': 'center'}),
                                dcc.Graph(id='covid-bar',
                                          figure={'data': [
                                              go.Scatter(
                                                  x=df_occupied_beds['date'],
                                                  y=df_occupied_beds['covidOccupiedMVBeds'],
                                                  fill='tozeroy',
                                                  marker_color='rgb(26, 118, 255)',
                                              )
                                          ], 'layout': go.Layout(bargap=0.5, paper_bgcolor='#282828', plot_bgcolor='#282828', font=dict(color='#adafae'), yaxis=dict(title='Number of MV Beds Occupied', gridcolor='rgba(61,61,61,0.2)'), xaxis=dict(showgrid=False))}, config={'displaylogo': False, 'displayModeBar': False})

                            ]
                        )
                    ),
                ], md=6
            ),
            dbc.Col(
                [
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H2(['Covid-19 Infections in Indian States Map'], style={
                                        'font-size': '30px', 'font-weight': 'bold', 'text-align': 'center'}),
                                dcc.Graph(id='map', figure=update_map(), config={
                                          'displaylogo': False, 'displayModeBar': False})
                            ]
                        )
                    )
                ], style={'height': '100%'}, md=6
            )
        ], style={'margin-bottom': '20px'},
        align="center",
    ),


], style={'font-family': 'Oswald'},
    fluid=True)


@app.callback(Output('global-covid', 'figure'),
              [Input('country-dropdown', 'value')])
def update_graph(country_name):
    fig = px.line(df_covid_global_transposed, x='date', y=country_name,
                  labels={'date': 'Date', 'value': 'Deaths'}, title='Death Trends by Country')
    fig.update_layout(paper_bgcolor='#282828', plot_bgcolor='#282828',
                      font=dict(color="#adafae"),
                      xaxis=dict(gridcolor='rgba(61,61,61,0.2)',
                                 zerolinecolor='rgb(61,61,61)', zeroline=True, zerolinewidth=2),
                      yaxis=dict(gridcolor='rgba(61,61,61,0.2)',
                                 zerolinecolor='rgb(61,61,61)', zeroline=True, zerolinewidth=2))
    return fig


@app.callback(Output('global-covid-cases', 'figure'),
              [Input('country-dropdown-cases', 'value')])
def update_graph(country_name):
    fig = go.Figure()
    for tic in country_name:
        fig.add_trace(go.Scatter(x=df_covid_global_cases_transposed['date'],
                                 y=df_covid_global_cases_transposed[tic],
                                 name=tic,
                                 mode='lines'))

        fig.update_layout(yaxis=dict(title="Cases"),
                          paper_bgcolor='#282828',
                          plot_bgcolor='#282828',
                          font=dict(color="#adafae"))
        fig.update_xaxes(gridcolor='rgba(61,61,61,0.2)',
                         zerolinecolor='rgb(61,61,61)', zeroline=True, zerolinewidth=2)
        fig.update_yaxes(gridcolor='rgba(61,61,61,0.2)',
                         zerolinecolor='rgb(61,61,61)', zeroline=True, zerolinewidth=2)

    return fig


@app.callback(Output('region-graph', 'figure'),
              [Input('selectedRegion', 'value')],
              [Input('selectedParameter', 'value')])
def update_figure(region, parameter):

    if parameter == "cumDeaths60DaysByDeathDate":
        yaxis_title = "Deaths"
    elif parameter == "cumCasesBySpecimenDate":
        yaxis_title = "Cases"
    for region_name in df_region_covid['areaName'].unique():
        df_by_region = df_region_covid[df_region_covid['areaName'] == region]

    return {'data': [go.Scatter(
        x=df_by_region['date'],
        y=df_by_region[parameter],
        fill='tozeroy',
        marker_color='rgb(26, 118, 255)'

    )], 'layout': go.Layout(
        yaxis={'title': yaxis_title, 'gridcolor': 'rgba(61,61,61,0.2)'},
        hovermode='closest',
        paper_bgcolor='#282828',
        plot_bgcolor='#282828',
        font=dict(color='#adafae')
    )
    }


if __name__ == "__main__":
    app.run_server()
