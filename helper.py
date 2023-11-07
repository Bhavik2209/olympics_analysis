import pandas as pd
import numpy as np
def find_medal_tally(df,year,country):
      medal_df = df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
      flag=0
      if year=='Overall' and country=='Overall':
        temp_df=medal_df
      if year=='Overall' and country!='Overall':
        flag=1
        temp_df = medal_df[medal_df['region']==country]
      if year!='Overall' and country=='Overall':
        temp_df = medal_df[medal_df['Year']==year]
      if year!='Overall' and country!='Overall':
        temp_df = medal_df[(medal_df['Year']==year) & (medal_df['region']==country)]
      if flag ==  1:
        x = temp_df.groupby('Year').sum()[['Gold','Silver','Bronze']].sort_values('Year').reset_index()
      else:
        x = temp_df.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()
      x['Total']= x['Gold'] + x['Silver'] + x['Bronze']

      x['Gold'] = x['Gold'].astype('int')
      x['Silver'] = x['Silver'].astype('int')
      x['Bronze'] = x['Bronze'].astype('int')
      x['Total'] = x['Total'].astype('int')


      return x


def medal_tally(df):
    medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    medal_tally = medal_tally.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values("Gold",ascending=False).reset_index()

    medal_tally['Total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']

    return medal_tally

def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')
    return years,country

def participating_nations_over_time(df,col):
    nations_over_time = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index()
    # nations_over_time.sort_values(nations_over_time.index,inplace=True)
    return nations_over_time

def mostSuccessful(df,sport):
    temp_df=df.dropna(subset=['Medal'])

    if(sport!='Overall'):
        temp_df=temp_df[temp_df['Sport']==sport]

    x= temp_df[['Name','region']].value_counts().reset_index()
    x['index']=x.index
    x.drop_duplicates('index')
    # x['Sport']=['Sport']
    # x['region']=temp_df.region

    return x.head(15)

def year_wise_medals(df,country):
    temp_df = df.dropna(subset=["Medal"])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()

    return final_df
def county_wise_heatmap(df,country):
    temp_df = df.dropna(subset=["Medal"])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]
    pt = new_df.pivot_table(index='Sport',columns="Year",values='Medal',aggfunc='count').fillna(0)
    return pt

def mostSuccessful_athlete_countrywise(df,country):
  temp_df=df.dropna(subset=['Medal'])

  temp_df=temp_df[temp_df['region'] == country]
  x= temp_df[['Name','Sport']].value_counts().reset_index().head(10)
  x.rename(columns={'count':'Medals'},inplace=True)
  return x