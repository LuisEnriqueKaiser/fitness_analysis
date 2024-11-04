import os
import pandas as pd
import numpy as np
import pickle as pkl

def find_all_csv_files(path): 
    ''''
    This function returns a list of all csv files in a directory
    '''
    
    csv_files = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.csv'):
                csv_files.append(file)
    return csv_files

def parse_and_get_data(path):
    '''
    This function opens all csv files in a directory and returns a dictionary of dataframes
    '''
    
    csv_files = find_all_csv_files(path)
    result_dataframe = pd.DataFrame()

    for file in csv_files:
        datestring = file [:-4]
        date = pd.to_datetime(datestring, format='%Y-%m-%d')
        df = pd.read_csv(path + "/" + file)
        activity_minutes = calculate_sum(df = df, column = "Anzahl der Aktivitätsminuten")
        distance_meters = calculate_sum(df = df, column = "Distanz (m)")
        walk_min = calculate_sum(df = df, column = "Gehen – Dauer (ms)") / 60000
        run_min = calculate_sum(df = df, column = "Laufen – Dauer (ms)") /60000
        hf = calculate_mean(df = df, column = "Durchschnittliche Herzfrequenz (bpm)")
        new_row = pd.DataFrame({'date': [date]
                    ,'activity_minutes': [activity_minutes]
                    ,'distance_meters': [distance_meters]
                    ,'walk_min': [walk_min]
                    , 'hf_avg': [hf]
                    ,'run_min': [run_min]})
        result_dataframe = pd.concat([result_dataframe, new_row], ignore_index=True)
    return result_dataframe


def extract_date(df): 
    '''
    This function extracts the date from a dataframe
    '''
    
    date = df['date']
    return date

def calculate_sum(df, column):
    '''
    This function calculates the sum of a column in a dataframe
    '''
    try:
        sum = df[column].sum()
    except KeyError:
        sum = 0
        return sum
    return sum

def calculate_mean(df, column):
    '''
    This function calculates the mean of a column in a dataframe
    '''
    try:
        mean = df[column].mean()
    except KeyError:
        mean = 0
        return mean 
    return mean 


path = "/Users/luisenriquekaiser/Documents/Fitness_Analysis/Data/Takeout/Google Fit/Tägliche Aktivitätswerte"
csv_files = find_all_csv_files(path = path)
summary_stats = parse_and_get_data(path = path)
# safe summary stats dataframe to csv in the path of the file 
# safe as pickle 
summary_stats.to_pickle("/Users/luisenriquekaiser/Documents/Fitness_Analysis/Data/Takeout/Google Fit/summary_stats.pkl")


