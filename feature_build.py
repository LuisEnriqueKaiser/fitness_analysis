import os
import pandas as pd
import numpy as np
from config_data import TIMEFRAMES_IMPUTATION, TIMEFRAMES_ROLLINGS

def sort_by_date(df): 
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(by='date')
    return df

def rolling_average (sorted_df ,timeframe, column): 
    '''
    This function calculates the rolling average of a column in a dataframe

    '''
    # create rolling average varable 
    name_rolling = 'rolling_average_'+column+'_'+str(timeframe)+'_days'
    sorted_df[name_rolling] = np.nan
    
    for index, row in sorted_df.iterrows():
        # if any of the columns is NaN then we will impute the missing data
        # Define the specific center date and number of days for the range
        center_date = row['date']
        days = timeframe
        # Define the range of dates to consider
        start_date = center_date - pd.Timedelta(days=days)
        end_date = center_date + pd.Timedelta(days=days)
            # Subset the data
        subset = sorted_df[(sorted_df['date'] >= start_date) & (sorted_df['date'] <= end_date)]
        # Impute the missing data
        sorted_df.at[index,name_rolling] = subset[column].mean()
    return sorted_df



def calculate_rolling_standard_deviation(sorted_df, timeframe, column): 
    '''
    This function calculates the rolling standard deviation of a column in a dataframe

    '''
    name_rolling = 'rolling_sd_'+column+'_'+str(timeframe)+'_days'
    sorted_df[name_rolling] = np.nan
    
    for index, row in sorted_df.iterrows():
        # if any of the columns is NaN then we will impute the missing data
        # Define the specific center date and number of days for the range
        center_date = row['date']
        days = timeframe
        # Define the range of dates to consider
        start_date = center_date - pd.Timedelta(days=days)
        end_date = center_date + pd.Timedelta(days=days)
            # Subset the data
        subset = sorted_df[(sorted_df['date'] >= start_date) & (sorted_df['date'] <= end_date)]
        # Impute the missing data
        sorted_df.at[index,name_rolling] = subset[column].std()
    return sorted_df
    


def imputation_missing_data(timeframe, sorted_df, column):
    '''
    This function imputes missing data in a dataframe

    '''
    # Define the specific center date and number of days for the range
    for index, row in sorted_df.iterrows():
        # if any of the columns is NaN then we will impute the missing data
        if np.isnan(row[column]):
            # Define the specific center date and number of days for the range
            center_date = row['date']
            days = timeframe
            # Define the range of dates to consider
            start_date = center_date - pd.Timedelta(days=days)
            end_date = center_date + pd.Timedelta(days=days)
            # Subset the data
            subset = sorted_df[(sorted_df['date'] >= start_date) & (sorted_df['date'] <= end_date)]
            # Impute the missing data
            sorted_df.at[index, column] = subset[column].mean()
    return sorted_df

def harmonize_missings_for_imputation(sorted_df, columnlist): 
    '''
    This function harmonizes the missing data in a dataframe
    '''
    for column in columnlist:
        sorted_df[column] = sorted_df[column].replace(0, np.nan)
        sorted_df[column] = sorted_df[column].replace('0', np.nan)
        sorted_df[column] = sorted_df[column].replace(' ', np.nan)
        sorted_df[column] = sorted_df[column].replace('', np.nan)
        sorted_df[column] = sorted_df[column].replace('NaN', np.nan)
    return sorted_df



def subset_data_by_year(df, timeframe_column, year):
    '''
    This function subsets the data by year

    '''
    # create subset  
    subset = df[df[timeframe_column].dt.year == year]
    return subset




# open the summary pickle 
summary_pickle = pd.read_pickle("/Users/luisenriquekaiser/Documents/Fitness_Analysis/Data/Takeout/Google Fit/summary_stats.pkl")
sorted_summary = sort_by_date(df =  summary_pickle)
sorted_summary= sorted_summary[sorted_summary['date'] > '2020-01-01']
sorted_summary = harmonize_missings_for_imputation(sorted_df=sorted_summary, columnlist=['activity_minutes','distance_meters', 'walk_min', 'hf_avg'])
# impute the NaN values with monthly averages 
for col in ['activity_minutes','distance_meters', 'walk_min', 'hf_avg', 'run_min']:
    sorted_summary = imputation_missing_data(timeframe=TIMEFRAMES_IMPUTATION[0], sorted_df=sorted_summary, column=col)
    for timeframe in TIMEFRAMES_ROLLINGS:
        sorted_summary = rolling_average(sorted_df=sorted_summary, timeframe=timeframe, column=col)
        sorted_summary = calculate_rolling_standard_deviation(sorted_df=sorted_summary, timeframe=timeframe, column=col)

# safe summary stats dataframe to csv in the path of the file
sorted_summary.to_pickle("/Users/luisenriquekaiser/Documents/Fitness_Analysis/Data/Takeout/Google Fit/summary_stats.pkl")