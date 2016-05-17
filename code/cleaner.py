
import pandas as pd

def cleaner(df):
    
    # convert all boolean columns to int for logistic regression
    
    ## categorical variables
    
    df.loc[:,'3ptr'] = df['shot_type'].str.startswith('3').astype(int)
    
    df.loc[:,'last_3_years'] = (df['season'] > '2013').astype(int)
    
    df.loc[:,'backcourt'] = ((df.shot_zone_area == 'Back Court(BC)') | \
                             (df.shot_zone_basic == 'backcourt')).astype(int)
    df.loc[:,'C+RA'] = ((df.shot_zone_area == 'Center(C)') | \
                        (df.shot_zone_basic == 'Restricted Area')).astype(int)
    
    teams_of_interest = set(['ORL', 'LAC', 'MIL', 'CHI', 'OKC', 'SEA', 'CHA', 'TOR', 'VAN'])
    df.loc[:,'better_when_homefield'] = df.opponent.isin(teams_of_interest).astype(int)
    
    df.drop(['action_type', 'shot_type', 'season', 
             'shot_zone_area', 'shot_zone_basic', 'shot_zone_range',
             'team_name', 'matchup', 'opponent'], 
            inplace=True, axis=1)
    
    cnames_to_dummify = ['combined_shot_type']
    df = pd.concat([df.drop(cnames_to_dummify, axis=1), 
                    pd.get_dummies(df[cnames_to_dummify], drop_first=True)], 
                   axis=1)
    
    
    ## numerical variables    
    df.loc[:,'final_4s'] = ((df.seconds_remaining < 5) & \
                            (df.seconds_remaining > 1) & \
                            (df.minutes_remaining == 0)).astype(int)
    
    df.loc[:,'final_s'] = ((df.seconds_remaining == 1) & \
                           (df.minutes_remaining == 0)).astype(int)
    
    df.loc[:,'4th_period'] = (df.period == 4).astype(int)
    df.loc[:,'extra_time'] = (df.period > 4).astype(int)
    
    df.drop(['game_event_id', 'game_id', 'team_id',
             'loc_y', 'loc_x', 'lat', 'lon', 'shot_distance',
             'seconds_remaining', 'minutes_remaining', 'period'], inplace=True, axis=1)
    
    # convert date to DateTime if not already done so
    if df['game_date'].dtype == 'O':
        df.loc[:,'game_date'] = pd.to_datetime(df['game_date'])
        
    # sort data in chronological order
    df.loc[:,'shot_id'] = df.index
    df = df.sort_values(['game_date', 'shot_id'])
    df.drop('shot_id', inplace=True, axis=1)
    
    
    return df