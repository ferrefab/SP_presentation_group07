# %% [markdown]
# # Semesterarbeit Scientific Programming

# %% [markdown]
# ## Libraries and settings

# %%
# Libraries
import os
import pandas as pd
import re
import sqlite3
import pycountry 
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import ttest_ind
import streamlit as st

# %% [markdown]
# ## Auf Ordner zugreifen und daten in einem DF speichern

# %%
# Base path to archive Folder
base_path = 'archive'

# List of all seasonal folders in the archive
season_folders = [folder for folder in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, folder))]

# sort folder by year  
season_folders.sort()

# For each season, load the Excel file and save it in a list of DataFrames
dataframes = []
for season in season_folders:
    file_path = os.path.join(base_path, season, 'champs.csv')
    df = pd.read_csv(file_path)
    df['season'] = season  # optional: add a new column "season" to save each season
    dataframes.append(df)

# Combine all Dataframes into a single DataFrame
combined_df = pd.concat(dataframes, ignore_index=True)
print(combined_df)


# %% [markdown]
# ## "Group" und "Comments" entfernen

# %%
# List of columns to be removed
columns_to_drop = ['Comments', 'Stage']

# Removing the columns from the DataFrame
combined_df = combined_df.drop(columns=columns_to_drop)

# %% [markdown]
# ## Neue Zeile für Verlängerung

# %%
def check_overtime(row):
    overtime = 'no'
    # Edit the "FT" column
    if re.search(r'\(\*\)', row['FT']):
        row['FT'] = re.sub(r' \(\*\)', '', row['FT'])
        overtime = 'yes'
    
    # Edit the "ET" column
    if pd.notna(row['ET']) and re.search(r' \(a\.e\.t\.\)', row['ET']):
        row['ET'] = re.sub(r' \(a\.e\.t\.\)', '', row['ET'])
        overtime = 'yes'
    
    # Edit the "P" column
    if pd.notna(row['P']) and re.search(r' \(pen\.\)', row['P']):
        row['P'] = re.sub(r' \(pen\.\)', '', row['P'])
        overtime = 'penalty'
    
    return overtime

# Update the columns "FT", "ET", and "P" and create the new column "Extra Time"
combined_df['Overtime'] = combined_df.apply(check_overtime, axis=1)
print(combined_df.head())


# %% [markdown]
# ## Neue Spalte für einzelne Tore

# %%
def get_goals(row):
    for col in ['P', 'ET', 'FT']:
        if pd.notna(row[col]):
            return row[col].split('-')

combined_df[['Tore Heimteam', 'Tore Auswärtsteam']] = combined_df.apply(get_goals, axis=1, result_type='expand').astype(int)
print(combined_df.head())

# %% [markdown]
# ## Web application with streamlit

# %%
st.title('Champions League')

# Create a selectbox to choose from the names in the DataFrame
selected_season = st.selectbox('Select a season', combined_df['season'].unique())

# Filter the DataFrame based on the selected name
filtered_df = combined_df[combined_df['season'] == selected_season]

# Display the filtered DataFrame
st.write(filtered_df)

# %% [markdown]
# ## Footer

# %%
import os
import platform
import socket
from platform import python_version
from datetime import datetime

print('-----------------------------------')
print(os.name.upper())
print(platform.system(), '|', platform.release())
print('Datetime:', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
print('Python Version:', python_version())
print('-----------------------------------')


