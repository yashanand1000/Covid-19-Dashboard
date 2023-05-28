from dependencies import *

pd.options.mode.chained_assignment = None
news_headline = []
news = []

# scrape the news


def news_scrape():
    '''This function scrapes the news from BBC news website and returns the news headlines as a list'''
    for i in range(1, 5):
        news_url = "https://www.bbc.co.uk/search?q=covid+19&page="+str(i)
        session = HTMLSession()
        response = session.get(news_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        ul = soup.find('ul', attrs={'class': 'ssrcss-1020bd1-Stack e1y4nx260'})
        for p in ul.findAll('p', attrs={'class': 'ssrcss-1q0x1qg-Paragraph eq5iqo00'}):
            news_headline.append(p.text)
    return news_headline




# Further from here i am reading the csv files from the github provided by you

df_covid_global = pd.read_csv(
    'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')

df_covid_global.fillna(0)

# Had to formate the dataset in order to make it a square matrix.
for i in range(len(df_covid_global.index)):
    # Did this for both the global datasets further with other datasets.
    if (pd.isna(df_covid_global['Province/State'].iloc[i]) != True):
        df_covid_global['Country/Region'][i] = df_covid_global['Country/Region'][i] + \
            ' ' + df_covid_global['Province/State'][i]


df_covid_global.drop('Province/State', axis=1, inplace=True)
df_covid_global.drop('Lat', axis=1, inplace=True)
df_covid_global.drop('Long', axis=1, inplace=True)
df_covid_global.set_index('Country/Region', inplace=True)

df_covid_global_transposed = df_covid_global.transpose()

df_death_sum = df_covid_global_transposed.sum(axis=1, skipna=True)


# Formatting the Time in correct foramt for the Dash to understand.Did this couple of times further.
for i in range(len(df_covid_global_transposed.index)):
    df_covid_global_transposed.index.values[i] = pd.to_datetime(
        df_covid_global_transposed.index.values[i]).strftime('%Y-%m-%d')

df_covid_global_transposed['date'] = df_covid_global_transposed.index




df_covid_global_cases = pd.read_csv(
    'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')

df_covid_global_cases.fillna(0)

# Some of the Countries had data represented as Province wise. So i just dropped the Province column and concatenated it with the country name.

for i in range(len(df_covid_global_cases.index)):
    if (pd.isna(df_covid_global_cases['Province/State'].iloc[i]) != True):
        df_covid_global_cases['Country/Region'][i] = df_covid_global_cases['Country/Region'][i] + \
            ' ' + df_covid_global_cases['Province/State'][i]


df_covid_global_cases.drop('Province/State', axis=1, inplace=True)
df_covid_global_cases.drop('Lat', axis=1, inplace=True)
df_covid_global_cases.drop('Long', axis=1, inplace=True)
df_covid_global_cases.set_index('Country/Region', inplace=True)

df_covid_global_cases_transposed = df_covid_global_cases.transpose()

df_cases_sum = df_covid_global_cases_transposed.sum(axis=1, skipna=True)

for i in range(len(df_covid_global_cases_transposed.index)):
    df_covid_global_cases_transposed.index.values[i] = pd.to_datetime(
        df_covid_global_cases_transposed.index.values[i]).strftime('%Y-%m-%d')

df_covid_global_cases_transposed['date'] = df_covid_global_cases_transposed.index



df_deaths = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'data/nation_level_daily.csv')

df_covid_cases_deaths = pd.read_csv(df_deaths)


df_covid_hospital_cap = pd.read_csv(
    'https://api.coronavirus.data.gov.uk/v2/data?areaType=overview&metric=plannedCapacityByPublishDate&format=csv')


df_covid_age_path = os.path.join(os.path.dirname(os.path.abspath(
    __file__)), 'data/111 Online Covid-19 data_2021-11-18.csv')

df_covid_age = pd.read_csv(df_covid_age_path)

df_covid_transmission = pd.read_csv(
    'https://api.coronavirus.data.gov.uk/v2/data?areaType=overview&metric=transmissionRateMax&metric=transmissionRateMin&format=csv')


fig_transmission = go.Figure()
fig_transmission.add_trace(go.Bar(x=df_covid_transmission['date'],
                                  y=df_covid_transmission['transmissionRateMin'],
                                  name='Minimum Transmission Rate',
                                  marker_color='rgb(55, 83, 109)'
                                  ))
fig_transmission.add_trace(go.Bar(x=df_covid_transmission['date'],
                                  y=df_covid_transmission['transmissionRateMax'],
                                  name='Maximum Transmission Rate',
                                  marker_color='rgb(26, 118, 255)'
                                  ))

fig_transmission.update_layout(
    yaxis=dict(
        title='Rate',
    ),
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15,
    bargroupgap=0.1,
    paper_bgcolor='#282828',
    plot_bgcolor='#282828',
    font=dict(color='#adafae')
)

fig_transmission.update_xaxes(gridcolor='rgba(61,61,61,0.2)',
                              zerolinecolor='rgb(61,61,61)', zeroline=True, zerolinewidth=2)
fig_transmission.update_yaxes(gridcolor='rgba(61,61,61,0.2)',
                              zerolinecolor='rgb(61,61,61)', zeroline=True, zerolinewidth=2)

df_covid_age.drop('ccgcode', axis=1, inplace=True)
df_covid_age.drop('ccgname', axis=1, inplace=True)


def update_graph_age():
    traces = []
    for sex in df_covid_age['sex'].unique():
        df_by_Type = df_covid_age[df_covid_age['sex'] == sex]
        traces.append(go.Histogram(
            x=df_by_Type['ageband'],
            y=df_by_Type['Total'],
            name=sex
        ))
    fig = {
        'data': traces,
        'layout': {'update_layout': {'barmode': 'stack'}, 'paper_bgcolor': '#282828', 'plot_bgcolor': '#282828', 'font': {'color': '#adafae'}, 'yaxis': {'title': 'Cases', 'gridcolor': 'rgba(61,61,61,0.2)'}, 'xaxis': {'showgrid': False}, 'legend': {'title': {'text': 'Age Bands'}}}
    }

    return fig


df_vaccinated = pd.read_csv(
    'https://api.coronavirus.data.gov.uk/v2/data?areaType=overview&metric=cumPeopleVaccinatedCompleteByPublishDate&metric=cumPeopleVaccinatedFirstDoseByPublishDate&metric=cumPeopleVaccinatedSecondDoseByPublishDate&format=csv')

vaccinated_values = [df_vaccinated['cumPeopleVaccinatedCompleteByPublishDate'].iloc[0],
                     df_vaccinated['cumPeopleVaccinatedFirstDoseByPublishDate'].iloc[0], df_vaccinated['cumPeopleVaccinatedSecondDoseByPublishDate'].iloc[0]]

df_pillar = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'data/nation_level_daily.csv')

df_pillar_test = pd.read_csv(df_pillar)


pillar_values = [df_pillar_test['Total Confirmed'].iloc[0], df_pillar_test['Total Recovered'].iloc[0],
                 df_pillar_test['Total Deceased'].iloc[0]]


Andaman_Nicobar = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'State_Wise/Andaman and Nicobar Islands.csv')

#Andhra_Pradesh = os.path.join(os.path.dirname(
#    os.path.abspath(__file__)), 'State_Wise/Andhra_Pradesh.csv')

Arunachal_Pradesh = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'State_Wise/Arunachal Pradesh.csv')

Assam = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'State_Wise/Assam.csv')

Bihar = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'State_Wise/Bihar.csv')

Dadra = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'State_Wise/Dadra and Nagar Haveli and Daman and Diu.csv')

Delhi = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'State_Wise/Delhi.csv')

Goa = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'State_Wise/Goa.csv')

Gujarat = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'State_Wise/Gujarat.csv')

Haryana = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'State_Wise/Haryana.csv')

Himachal_Pradesh = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'State_Wise/Himachal Pradesh.csv')

Jammu = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'State_Wise/Jammu and kashmir.csv')

Jharkhand = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'State_Wise/Jharkhand.csv')

Karnataka = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'State_Wise/Karnataka.csv')

Kerala = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'State_Wise/Kerala.csv')

Ladakh = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'State_Wise/Ladakh.csv')

Madhya_Pradesh = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'State_Wise/Madhya Pradesh.csv')

Maharashtra = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'State_Wise/Maharashtra.csv')

Manipur = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'State_Wise/Manipur.csv')

Meghalaya = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'State_Wise/Meghalaya.csv')

Mizoram = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'State_Wise/Mizoram.csv')

Nagaland = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'State_Wise/Nagaland.csv')

Odhisa = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'State_Wise/Odhisa.csv')

Puducherry = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'State_Wise/Puducherry.csv')

Punjab = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'State_Wise/Punjab.csv')

Rajasthan = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'State_Wise/Rajasthan.csv')

Sikkim = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'State_Wise/Sikkim.csv')

Tamil_Nadu = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'State_Wise/Tamil Nadu.csv')

Telangana = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'State_Wise/Telangana.csv')

Tripura = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'State_Wise/Tripura.csv')

Utc = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'State_Wise/Union Territory of Chandigarh.csv')

Utj = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'State_Wise/Union Territory of Jammu and Kashmir.csv')

Utl = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'State_Wise/Union Territory of Ladakh.csv')

Uttar_Pradesh = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'State_Wise/Uttar Pradesh.csv')

Uttarakhand = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'State_Wise/Uttarakhand.csv')

West_Bengal = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'State_Wise/West Bengal.csv')


df_occupied_beds = pd.read_csv(
    'https://api.coronavirus.data.gov.uk/v2/data?areaType=overview&metric=covidOccupiedMVBeds&format=csv')

map_gj = os.path.join(os.path.dirname(os.path.abspath(
    __file__)), 'data/india_state.geojson')
map_csv = os.path.join(os.path.dirname(os.path.abspath(
    __file__)), 'data/state_level_latest.csv')

df_map_cases = pd.read_csv(map_csv)

with open(map_gj) as f:
    gj = geojson.load(f)
    
#merged_df = pd.merge(map_csv, pd.DataFrame(gj), on='ID_1')


Andaman_Nicobar_covid = pd.read_csv(Andaman_Nicobar)
#Andhra_Pradesh_covid = pd.read_csv(Andhra_Pradesh)
Arunachal_Pradesh_covid = pd.read_csv(Arunachal_Pradesh)
Assam_covid = pd.read_csv(Assam)
Bihar_covid = pd.read_csv(Bihar)
Dadra_covid = pd.read_csv(Dadra)
Delhi_covid = pd.read_csv(Delhi)
Goa_covid = pd.read_csv(Goa)
Gujarat_covid = pd.read_csv(Gujarat)
Haryana_covid = pd.read_csv(Haryana)
Himachal_Pradesh_covid = pd.read_csv(Himachal_Pradesh)
Jammu_covid = pd.read_csv(Jammu)
Jharkhand_covid = pd.read_csv(Jharkhand)
Karnataka_covid = pd.read_csv(Karnataka)
Kerala_covid = pd.read_csv(Kerala)
Ladakh_covid = pd.read_csv(Ladakh)
Madhya_Pradesh_covid = pd.read_csv(Madhya_Pradesh)
Maharashtra_covid = pd.read_csv(Maharashtra)
Manipur_covid = pd.read_csv(Manipur)
Meghalaya_covid = pd.read_csv(Meghalaya)
Mizoram_covid = pd.read_csv(Mizoram)
Nagaland_covid = pd.read_csv(Nagaland)
Odhisa_covid = pd.read_csv(Odhisa)
Puducherry_covid = pd.read_csv(Puducherry)
Punjab_covid = pd.read_csv(Punjab)
Rajasthan_covid = pd.read_csv(Rajasthan)
Sikkim_covid = pd.read_csv(Sikkim)
Tamil_Nadu_covid = pd.read_csv(Tamil_Nadu)
Telangana_covid = pd.read_csv(Telangana)
Tripura_covid = pd.read_csv(Tripura)
Utc_covid = pd.read_csv(Utc)
Utj_covid = pd.read_csv(Utj)
Utl_covid = pd.read_csv(Utl)
Uttar_Pradesh_covid = pd.read_csv(Uttar_Pradesh)
Uttarakhand_covid = pd.read_csv(Uttarakhand)
West_Bengal_covid = pd.read_csv(West_Bengal)

frames = [Andaman_Nicobar_covid, Arunachal_Pradesh_covid, Assam_covid, Bihar_covid,
          Dadra_covid, Delhi_covid, Goa_covid, Gujarat_covid, Haryana_covid, Himachal_Pradesh_covid, Jammu_covid,
          Jharkhand_covid, Karnataka_covid, Kerala_covid, Ladakh_covid, Madhya_Pradesh_covid, Maharashtra_covid, 
          Manipur_covid, Meghalaya_covid, Mizoram_covid, Nagaland_covid, Odhisa_covid, Puducherry_covid, Punjab_covid,
          Rajasthan_covid, Sikkim_covid, Tamil_Nadu_covid, Telangana_covid, Tripura_covid, Utc_covid, Utj_covid, 
          Utl_covid, Uttar_Pradesh_covid, Uttarakhand_covid, West_Bengal_covid]


df_region_covid = pd.concat(frames, ignore_index=True)


def update_map():

    fig = px.choropleth(df_map_cases, geojson=gj, color="cumCasesBySpecimenDate",
                        locations="ID_1", featureidkey="properties.ID_1",
                        projection="mercator", hover_data={'areaName': True, 'cumCasesBySpecimenDate': True, 'ID_1': False}
                        )
    fig.update_geos(fitbounds="locations", visible=False, bgcolor="#282828")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, height=1000, paper_bgcolor="#282828",
                      plot_bgcolor="#282828", font=dict(color='#adafae'), coloraxis_colorbar_title="Total Cases")
    return fig


fig_deaths = go.Figure(data=go.Heatmap(
    z=df_region_covid['cumDeaths60DaysByDeathDate'],
    x=df_region_covid['date'],
    y=df_region_covid['areaName'],
    colorscale='Viridis',
    connectgaps=True))

fig_deaths.update_layout(
    title='Deaths in Indian States',
    xaxis_nticks=36,
    paper_bgcolor='#282828',
    plot_bgcolor='#282828',
    font=dict(color='#adafae'))

fig_deaths.update_xaxes(gridcolor='rgba(61,61,61,0.2)',
                        zerolinecolor='rgb(61,61,61)', zeroline=True, zerolinewidth=2)
fig_deaths.update_yaxes(gridcolor='rgba(61,61,61,0.2)',
                        zerolinecolor='rgb(61,61,61)', zeroline=True, zerolinewidth=2)


fig_cases = go.Figure(data=go.Heatmap(
    z=df_region_covid['cumCasesBySpecimenDate'],
    x=df_region_covid['date'],
    y=df_region_covid['areaName'],
    colorscale='Viridis'))

fig_cases.update_layout(
    title='Cases in Indian States',
    xaxis_nticks=36,
    paper_bgcolor='#282828',
    plot_bgcolor='#282828',
    font=dict(color='#adafae'))

fig_cases.update_xaxes(gridcolor='rgba(61,61,61,0.2)',
                       zerolinecolor='rgb(61,61,61)', zeroline=True, zerolinewidth=2)
fig_cases.update_yaxes(gridcolor='rgba(61,61,61,0.2)',
                       zerolinecolor='rgb(61,61,61)', zeroline=True, zerolinewidth=2)


features_deaths = df_covid_global_transposed.columns
features_cases = df_covid_global_cases_transposed.columns


news = news_scrape()
news.pop()
news.pop()
news.pop()


tabs_styles = {
    'height': '44px',
    'align-items': 'center',
    'margin': '10px'
}
tab_style = {
    'borderBottom': '1px solid #adafae',
    'padding': '6px',
    'fontWeight': 'bold',
    'border-radius': '15px',
    'background-color': '#282828',
    'box-shadow': '0px 4px 8px 0px #adafae',
    'margin': '10px'

}

tab_selected_style = {
    'borderTop': '1px solid #adafae',
    'borderBottom': '1px solid #adafae',
    'backgroundColor': '#adafae',
    'color': '#282828',
    'padding': '6px',
    'border-radius': '15px',
}
