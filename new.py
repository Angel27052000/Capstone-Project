import pandas as pd
import plotly.express as px
import streamlit as st
print("Pandas version:", pd.__version__)
st.set_page_config(page_title='Capstone Dashboard', page_icon='bar_chart', layout='wide')

confirmed_csv_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
deaths_csv_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"
recovered_csv_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"

confirmed_df = pd.read_csv(confirmed_csv_url)
deaths_df = pd.read_csv(deaths_csv_url)
recovered_df = pd.read_csv(recovered_csv_url)

def unpivot_data(df, metric_name):
    df_unpivoted = pd.melt(df, id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'], var_name='Date', value_name=metric_name)
    df_unpivoted['Date'] = pd.to_datetime(df_unpivoted['Date'], format='%m/%d/%y')
    return df_unpivoted

confirmed_unpivoted = unpivot_data(confirmed_df, 'Confirmed')
deaths_unpivoted = unpivot_data(deaths_df, 'Deaths')
recovered_unpivoted = unpivot_data(recovered_df, 'Recovered')

confirmed_unpivoted['Confirmed_Daily'] = confirmed_unpivoted.groupby('Country/Region')['Confirmed'].diff()
deaths_unpivoted['Deaths_Daily'] = deaths_unpivoted.groupby('Country/Region')['Deaths'].diff()
recovered_unpivoted['Recovered_Daily'] = recovered_unpivoted.groupby('Country/Region')['Recovered'].diff()

st.title('COVID-19 Time Series Data')
st.subheader('Confirmed, Deaths, and Recovered Cases')
st.sidebar.header("COVID-19 Data Visualization")

confirmed_unpivoted['Date'] = pd.to_datetime(confirmed_unpivoted['Date'])
confirmed_unpivoted['Year'] = confirmed_unpivoted['Date'].dt.year

deaths_unpivoted['Date'] = pd.to_datetime(deaths_unpivoted['Date'])
deaths_unpivoted['Year'] = deaths_unpivoted['Date'].dt.year

recovered_unpivoted['Date'] = pd.to_datetime(recovered_unpivoted['Date'])
recovered_unpivoted['Year'] = recovered_unpivoted['Date'].dt.year
selected_country = st.sidebar.selectbox("Select Country", confirmed_df['Country/Region'].unique())

selected_year = st.sidebar.selectbox("Select Year", confirmed_unpivoted['Year'].unique())


date_range = st.sidebar.date_input("Select Date Range for Death Count", 
                                         [deaths_unpivoted['Date'].min().date(), deaths_unpivoted['Date'].max().date()])

filtered_deaths_range = deaths_unpivoted[(deaths_unpivoted['Country/Region'] == selected_country) & 
                                        (deaths_unpivoted['Date'] >= pd.to_datetime(date_range[0])) & 
                                        (deaths_unpivoted['Date'] <= pd.to_datetime(date_range[1]))]

filtered_recovered = recovered_unpivoted[(recovered_unpivoted['Country/Region'] == selected_country) & 
                                        (recovered_unpivoted['Date'] >= pd.to_datetime(date_range[0])) & 
                                        (recovered_unpivoted['Date'] <= pd.to_datetime(date_range[1]))]



filtered_confirmed = confirmed_unpivoted[(confirmed_unpivoted['Country/Region'] == selected_country) & 
                                        (confirmed_unpivoted['Date'] >= pd.to_datetime(date_range[0])) & 
                                        (confirmed_unpivoted['Date'] <= pd.to_datetime(date_range[1]))]


filtered_deaths_range = deaths_unpivoted[(deaths_unpivoted['Country/Region'] == selected_country) & 
                                        (deaths_unpivoted['Date'] >= pd.to_datetime(date_range[0])) & 
                                        (deaths_unpivoted['Date'] <= pd.to_datetime(date_range[1]))]

filtered_recovered = recovered_unpivoted[(recovered_unpivoted['Country/Region'] == selected_country) & 
                                        (recovered_unpivoted['Date'] >= pd.to_datetime(date_range[0])) & 
                                        (recovered_unpivoted['Date'] <= pd.to_datetime(date_range[1]))]


fig = px.line(filtered_confirmed, x='Date', y='Confirmed',line_shape='linear')
fig.add_scatter(x=filtered_confirmed['Date'], y=filtered_confirmed['Confirmed'], mode='lines',name='Confirmed')
fig.add_scatter(x=filtered_deaths_range['Date'], y=filtered_deaths_range['Deaths'], mode='lines',name='Death')
fig.add_scatter(x=filtered_recovered['Date'], y=filtered_recovered['Recovered'], mode='lines', name='Recovered')
fig.update_xaxes(title='Date')
fig.update_yaxes(title='No.of cases')
fig.update_layout(legend={'itemsizing': 'constant'})
if filtered_confirmed.empty:
    st.error("No data available for the selected date range.")
else:
    st.plotly_chart(fig)
st.sidebar.header("Death Count for Date Range")

death_count_in_range = filtered_deaths_range['Deaths'].sum()

st.sidebar.write(f"Death Count between {date_range[0]} and {date_range[1]}: {death_count_in_range}")


