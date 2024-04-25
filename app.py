import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium

APP_TITLE = 'Basic Needs and Nutrition Basket (BNNB) Cost Distributions by Major Cities'
APP_SUB_TITLE = 'Source jctr.org.zm'


def display_avg_bnb(data, year, city, metric):
    data = data[(data['Year'] == year)]
    if city:
        data = data[data['City'] == city]
        avg = data[metric].mean()
        st.metric(f"## Average BNNB in \n {year} : ", 'ZMW {:,.2f}'.format(avg))




def display_max_bnb(data, year, city, metric):
    data = data[(data['Year'] == year)]
    if city:
        data = data[data['City'] == city]
        maxbnb = (data[metric].max())
        data = data[data[metric] == maxbnb]
        month = data['Month'].values[0]
        st.metric(f"## Highest BNNB Amount in {year} \n was recorded in {month} : ", 'ZMW {:,.2f}'.format(maxbnb))

def display_min_bnb(data, year, city, metric):
    data = data[(data['Year'] == year)]
    if city:
        data = data[data['City'] == city]
        minbnb = (data[metric].min())
        data = data[data[metric] == minbnb]
        month = data['Month'].values[0]
        st.metric(f"## Lowest BNNB Amount in {year} \n was recorded in {month} : ", 'ZMW {:,.2f}'.format(minbnb))


def display_map(data, year, month):
    data = data[(data['Year'] == year) & (data['Month'] == month)]

    map = folium.Map(location=(-13.133897, 27.849332), zoom_start=6, scrollWheelZoom=False, tiles='CartoDB positron')

    choropleth = folium.Choropleth(
        geo_data='districts.geojson',
        data=data,
        columns=('City', 'TotalBNBImputed'),
        key_on='feature.properties.NAME',
        line_opacity=0.8,
        highlight=True,

    )
    choropleth.geojson.add_to(map)

    data = data.set_index('City')

    for feature in choropleth.geojson.data['features']:
        city = feature['properties']['NAME']
        if city in data.index:
            bnb = str('ZMW {:,}'.format(data.loc[city, 'TotalBNBImputed']))
        else:
            bnb = 'nil'

        feature['properties']['living cost'] = 'Living Cost: ' + bnb

    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(['NAME', 'living cost'], labels=False)
    )

    st_map = st_folium(map, width=700, height=450)

    if st_map['last_active_drawing']:
        return st_map['last_active_drawing']['properties']['NAME']
    else:
        return ''


def display_filters(data):
    year_list = sorted(np.array(data['Year'].unique(),dtype=int))
    year = st.sidebar.selectbox('Year',year_list,len(year_list)-1)

    month_list = np.array(data['Month'].unique())
    month = st.sidebar.selectbox('Month',month_list)

    return year,month
def display_city_filter(data,city):
    city_list =[''] + list(data['City'].unique())
    city_index = city_list.index(city)
    st.write(city_index)

    return st.sidebar.selectbox('City',city_list,city_index)



def main():
    st.set_page_config(APP_TITLE)
    st.title(APP_TITLE)
    st.caption(APP_SUB_TITLE)

    #Load Data
    data = pd.read_csv("JCTR BNNB Data.csv")
    data = data.drop("Monthly change in BNB", axis=1)
    metric = 'TotalBNBImputed'


    #Display Filters & Map
    year, month = display_filters(data)
    city = display_map(data, year, month)
    city = display_city_filter(data, city)






    #Display Metrics

    st.subheader(f'{city} {year} BNNB Facts and Figures')

    col1, col2, col3 = st.columns(3)
    with col1:
        try:
            display_max_bnb(data, year, city, metric)
        except:
            st.write('Oops! Data is not available')
    with col2:
        try:
            display_avg_bnb(data, year, city, metric)
        except:
            st.write('Oops! Data is not available')
    with col3:
        try:
            display_min_bnb(data, year, city, metric)
        except:
            st.write('Oops! Data is not available')


if __name__ == "__main__":
    main()
