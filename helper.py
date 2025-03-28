import numpy as np


def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(subset = ['Team' ,'NOC' , 'Sport' , 'Year' , 'Event' , 'Medal']) #, 'Games'
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['Team'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == year) & (medal_df['Team'] == country)]

    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:
        x = temp_df.groupby('Team').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                      ascending=False).reset_index()

    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']

    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')
    x['total'] = x['total'].astype('int')

    return x


def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    country = np.unique(df['Team'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return years,country

def data_over_time(df,col):

    nations_over_time = df.drop_duplicates(['Year' , 'Team'])['Year'].value_counts().reset_index().sort_values('Year')
    nations_over_time.rename(columns = {'Year':'Year' , 'count' :'No. of countries' }, inplace = True)
    return nations_over_time

def event_over_time(df,col):

    event_over_time = df.drop_duplicates(['Year' , 'Event'])['Year'].value_counts().reset_index().sort_values('Year')

    event_over_time.rename(columns = {'Year':'Year' , 'count' :'No. of event' }, inplace = True)
    return event_over_time


def athletes_over_time(df,col):

    athletes_over_time = df.drop_duplicates(['Year' , 'Name'])['Year'].value_counts().reset_index().sort_values('Year')
    athletes_over_time.rename(columns = {'Year':'Year' , 'count' :'Name' }, inplace = True)
    return athletes_over_time


# def most_successful(df, sport):
#     temp_df = df.dropna(subset=['Medal'])

#     if sport != 'Overall':
#         temp_df = temp_df[temp_df['Sport'] == sport]

#     x = temp_df['Name'].value_counts().reset_index().head(15).merge(df, left_on='index', right_on='Name', how='left')[
#         ['index', 'Name_x', 'Sport', 'region']].drop_duplicates('index')
#     x.rename(columns={'index': 'Name', 'Name_x': 'Medals'}, inplace=True)
#     return x

def most_successful(df , sport):
    temp_df = df[df['Medal'].notna() & (df['Medal'] != 'No medal')]
    
    if sport != 'overall':
        temp_df = temp_df[temp_df['Sport'] == sport]
        
    x = temp_df['Name'].value_counts().reset_index().head(15).merge(df , on = 'Name' , how ='left')[['Name' ,'count' , 'Sport' ,'Team']].drop_duplicates('Name')
    return x

def yearwise_medal_tally(df,country):
    temp_df = df[df['Medal'] != 'No medal']
    #temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)


    new_df = temp_df[temp_df['Team'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()

    return final_df

def country_event_heatmap(df,country):
    temp_df = df[df['Medal'] != 'No medal']
    temp_df.drop_duplicates(subset=['Team', 'NOC',  'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)  #'Games',

    new_df = temp_df[temp_df['Team'] == country]

    pt = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    return pt


# def most_successful_countrywise(df, country):
#     temp_df = df.dropna(subset=['Medal'])

#     temp_df = temp_df[temp_df['Team'] == country]

#     x = temp_df['Name'].value_counts().reset_index().head(10).merge(df, left_on='index', right_on='Name', how='left')[
#         ['index', 'Name_x', 'Sport']].drop_duplicates('index')
#     x.rename(columns={'index': 'Name', 'Name_x': 'Medals'}, inplace=True)
#     return x

def most_successful_country(df , country):
    temp_df = df[df['Medal'].notna() & (df['Medal'] != 'No medal')]
    
    if country != 'overall':
        temp_df = temp_df[temp_df['Team'] == country]
        
    x=  temp_df['Name'].value_counts().reset_index().head(15).merge(df , on = 'Name' , how ='left')[['Name' ,'count' , 'Sport' ,'Team']].drop_duplicates('Name')
    return x


def weight_v_height(df,sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'Team'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df

def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'Team'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    final.fillna(0, inplace=True)

    return final