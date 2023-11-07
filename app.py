import streamlit as st
import pandas as pd
import preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout="wide")

df=pd.read_csv("athlete_events.csv")
df_rgn=pd.read_csv("noc_regions.csv")

df=preprocessor.preprocess(df,df_rgn)
st.sidebar.title("Olympics Analysis")
st.sidebar.image('download.png')

user_menu=st.sidebar.radio(
    'Select an option',
    ('Medal Tally','Overall Analysis','Country-Wise Analysis')
)

if user_menu== 'Medal Tally':

    st.sidebar.header("Medal Tally")
    years,country = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox("Select Year",years)
    selected_country = st.sidebar.selectbox("Select Counrty",country)

    medal_tally=helper.find_medal_tally(df,selected_year,selected_country)

    if selected_country=="Overall" and selected_year=="Overall":
        st.title("Overall Tally")
    if selected_country=="Overall" and selected_year!="Overall":
        st.title("Medal Tally In " + str(selected_year))
    if selected_country!="Overall" and selected_year=="Overall":
        st.title("Medal Tally Of " + str(selected_country))
    if selected_country!="Overall" and selected_year!="Overall":
        st.title("Medal Tally Of " + selected_country + " In " + str(selected_year))
    st.table(medal_tally)

if user_menu== 'Overall Analysis':
    editions = df['Year'].unique().shape[0]
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]
    st.title("Top Statistics")

    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Athletes")
        st.title(athletes)

    nations_over_time = helper.participating_nations_over_time(df,'region')
    nations_over_time.sort_values('Year',ascending=True,inplace=True)
    plt.rcParams.update({'font.size':6})
    fig = plt.figure(figsize=(7,7))
    fig.set_figwidth(4)
    fig.set_figheight(2)
    plt.plot(nations_over_time.Year,nations_over_time['count'])
    plt.grid()
    plt.xlabel("Years",fontsize=6)
    plt.ylabel("No Of Countries",fontsize=6)
    plt.title("Participation Of Coutries",fontsize=6)
    st.pyplot(fig)

    events_over_time = helper.participating_nations_over_time(df, 'Event')
    events_over_time.sort_values('Year', ascending=True, inplace=True)
    plt.rcParams.update({'font.size': 6})
    fig = plt.figure(figsize=(7, 7))
    fig.set_figwidth(4)
    fig.set_figheight(2)
    plt.plot(events_over_time.Year, events_over_time['count'])
    plt.grid()
    plt.xlabel("Years", fontsize=6)
    plt.ylabel("No Of Events", fontsize=6)
    plt.title("Events Over The Years", fontsize=6)
    st.pyplot(fig)

    athletes_over_time = helper.participating_nations_over_time(df, 'Name')
    athletes_over_time.sort_values('Year', ascending=True, inplace=True)
    plt.rcParams.update({'font.size': 6})
    fig = plt.figure(figsize=(7, 7))
    fig.set_figwidth(4)
    fig.set_figheight(2)
    plt.plot(athletes_over_time.Year, athletes_over_time['count'])
    plt.grid()
    plt.xlabel("Years", fontsize=6)
    plt.ylabel("No Of Athletes", fontsize=6)
    plt.title("Athletes Over The Years", fontsize=6)
    st.pyplot(fig)

    st.title("No of Events over time (every sports)")
    fig,ax=plt.subplots(figsize = (20,20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'))
    st.pyplot(fig)

    st.title("Most Successful Athletes")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')

    selected_sport = st.selectbox('Seect a Sport',sport_list)
    x=helper.mostSuccessful(df,selected_sport)
    st.table(x)

if  user_menu == 'Country-Wise Analysis':

    st.sidebar.title("Counrty-wise Analysis")

    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox('Select a Country',country_list)

    country_df = helper.year_wise_medals(df,selected_country)
    fig = plt.figure(figsize=(7, 7))
    plt.grid()
    fig.set_figwidth(4)
    fig.set_figheight(2)
    plt.plot(country_df['Year'], country_df['Medal'])
    plt.rcParams.update({'font.size': 1})
    plt.xlabel("YEARS",fontsize=6)
    plt.ylabel("MEDALS",fontsize=6)
    plt.show()
    st.title(selected_country + " Medal Tally Over the Years")
    st.set_option('deprecation.showPyplotGlobalUse', False)
    #  to remove the warning for not passing the argument in st.pyplot()
    st.pyplot(fig)

    st.title(selected_country + " Excels in the following Sports")
    pt = helper.county_wise_heatmap(df, selected_country)
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_xlabel("Year", fontsize=20)
    ax.set_ylabel("Sports", fontsize=20)
    ax = sns.heatmap(pt)
    st.pyplot(fig)

    st.title("Top 10 athletes of "+ selected_country)
    top_10_df = helper.mostSuccessful_athlete_countrywise(df,selected_country)
    st.table(top_10_df)