import streamlit as st
import folium
import pandas as pd
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster


st.set_page_config(layout ="wide")

st.markdown('''
## World CO2 Emissions (metric tons per capita)
''')

# st.sidebar.markdown("01_City_Transport_Emissions")

st.write('---')



geo_path = '/Users/cwchen/Projects/fpi-app/data'
data_path = '/Users/cwchen/Projects/fpi-app/data/country-emission-per-capita-2019.csv'

country_geo = f"{geo_path}/My_WB_countries_Admin0_lowres_adde.geojson"
#country_geo = geo
country_data = pd.read_csv(data_path)

city_file = f"{geo_path}/GGMCF_top500cities_latlon.csv"
#city_file = f"{geo_path}/Net_Zero_Tracker_city_all.csv"
city_df = pd.read_csv(city_file)

#bins = list(country_data["2019"].quantile([0, 0.25, 0.5, 0.75, 1]))
bins = [0, 2.29, 5.35, 9.02, 16.13, 32.48]

m = folium.Map(location=[10, 10], tiles="cartodbpositron", zoom_start=2)

folium.Choropleth(
 geo_data=country_geo,
 name="choropleth",
 data=country_data,
 columns=["Country Code", "2019"],
 key_on="properties.ISO_A3_EH",
 #key_on="properties.WB_A3",
 fill_color="GnBu",
 fill_opacity=0.7,
 line_opacity=0.2,
 bins=bins,
 legend_name="GHG emission per capita (tCO2e)",
 ).add_to(m)

#folium.features.GeoJson(country_geo,
#                        name="Country", popup=folium.features.GeoJsonPopup(fields=["NAME_EN"])).add_to(m)

style_function = lambda x: {'fillColor': '#ffffff', 
                            'color':'#000000', 
                            'fillOpacity': 0.1, 
                            'weight': 0.1}
highlight_function = lambda x: {'fillColor': '#000000', 
                                'color':'#000000', 
                                'fillOpacity': 0.50, 
                                'weight': 0.1}

NIL = folium.features.GeoJson(
    country_geo,
    style_function=style_function, 
    control=False,
    highlight_function=highlight_function, 
    tooltip=folium.features.GeoJsonTooltip(
#        fields=['name','id'],  # use fields from the json file
#        aliases=['State: ','ID: '],
        fields=['NAME_EN', 'tCO2e_per_capita_2019'],
        aliases=['', ''],
        style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 5px;") 
    )
)
m.add_child(NIL)
#m.keep_in_front(NIL)

# Create a marker cluster instance
mc = MarkerCluster()

#print(MarkerCluster())

for i, row in city_df.iterrows():
    mc.add_child(folium.Marker(location = [row['Latitude'],row['Longitude']], popup=[row['Urban Cluster'],round(row['Footprint/cap (t CO2)'], 3)]))

m.add_child(mc)

folium.LayerControl().add_to(m)

folium_static(m, width=800, height=600)

st.write('Data Sources: World Bank, Climate Watch, Net Zero Tracker, Our World in Data, Global Gridded Model of Carbon Footprints (GGMCF)')