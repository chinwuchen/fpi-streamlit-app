import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# import cufflinks as cf
import datetime
#import altair as alt
#import numpy as np

st.markdown('''
## City Transport Emissions
''')

# st.sidebar.markdown("01_City_Transport_Emissions")

st.write('---')

# Create sidebar for query input
#st.sidebar.subheader('Query parameters')

# Create a menu with options - later

#start_date = st.sidebar.date_input("Start date", datetime.date(2019, 1, 1))
#end_date = st.sidebar.date_input("End date", datetime.date(2021, 10, 31))

# Read csv file
df_orig = pd.read_csv('data/transport-emissions-city-density.csv')

# df with emissions data
df = df_orig[~df_orig['Transport emissions per capita (tCO2)'].isnull()]

#st.dataframe(df_emissions)

# matplotlib scatterplot
def static_plot():
    fig, ax = plt.subplots(1,1)
    ax.scatter(x=df['Population density'], y=df['Transport emissions per capita (tCO2)'])
    ax.set_xlabel('Population density (person/km2)')
    ax.set_ylabel('Transport emissions per capita (tCO2)')

    st.pyplot(fig)

    st.write('Data source: Our World in Data')
    st.write('Currently contains 53 cities')

# interactive plotly scatterplot
def interactive_plot():
    col1, col2 = st.columns(2)

    x_axis_val = col1.selectbox('Select the X-axis:', options=df.columns)
    y_axis_val = col2.selectbox('Select the Y-axis:', options=df.columns)

    plot = px.scatter(df, x=x_axis_val, y=y_axis_val, text=df['Entity'])
    st.plotly_chart(plot, use_container_width=True)

    st.write('Data source: Our World in Data')
    st.write('Currently contains 53 cities')


# Sidebar setup
# st.sidebar.title('Sidebar')
st.sidebar.title('Options')
options = st.sidebar.radio('Select what to display:', ['static', 'interactive'])

if options == 'static':
    static_plot()
if options == 'interactive':
    interactive_plot()


# Vega lite scatterplot
# st.vega_lite_chart(df, {
#      'mark': {'type': 'circle', 'tooltip': True},
#      'encoding': {
#          'x': {'field': 'Population density', 'type': 'quantitative'},
#          'y': {'field': 'Transport emissions per capita (tCO2)', 'type': 'quantitative'}
# #         'size': {'field': 'c', 'type': 'quantitative'},
# #         'color': {'field': 'c', 'type': 'quantitative'},
#      },
#  })

# Altair scatterplot 
#c = alt.Chart(df).mark_circle().encode(
#     x='Population density', y='Transport emissions per capita (tCO2)', tooltip=['Entity', 'Population density', 'Transport emissions per capita (tCO2)'])
#st.altair_chart(c, use_container_width=True)

# Retrieve ticker data
#ticker_list = pd.read_csv('stock_ticker_list.txt')
#tickerSymbol = st.sidebar.selectbox('Stock ticker', ticker_list)
#tickerData = yf.Ticker(tickerSymbol)
#tickerDf = tickerData.history(period='1d', start=start_date, end=end_date)

# Ticker info
#string_logo = '<img src=%s>' % tickerData.info['logo_url']
#st.markdown(string_logo, unsafe_allow_html=True)

# string_name = tickerData.info['longName']
# st.header('**%s**' % string_name)

# string_summary = tickerData.info['longBusinessSummary']
# st.info(string_summary)

# # Ticker data
# st.header('**Ticker data**')
# st.write(tickerDf)

# # Bollinger bands
# st.header('**Bollinger Bands**')
# qf = cf.QuantFig(tickerDf, title='First Quant Figure', legend='top', name='GS')
# qf.add_bollinger_bands()
# fig = qf.iplot(asFigure=True)
# st.plotly_chart(fig)

# st.write('---')
