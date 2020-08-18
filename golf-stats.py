# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 17:39:21 2020

@author: vinhe
"""

import pandas as pd


# load the data
path = 'C:/users/vinhe/code/projects/golf/'
sg_ott_df = pd.read_csv(path + 'sg_ott.csv')
sg_putting_df = pd.read_csv(path + 'sg_putting.csv')
green_in_reg_df = pd.read_csv(path + 'green_in_reg.csv')


# rename columns
sg_ott_df = sg_ott_df.rename(columns={'AVERAGE': 'AVERAGE SG:OTT'})
sg_putting_df = sg_putting_df.rename(columns={'AVERAGE': 'AVERAGE SG:PUTTING'})
green_in_reg_df = green_in_reg_df.rename(columns={'%': 'GREENS %'})


# merge columns on player name
combined = sg_ott_df.merge(sg_putting_df, on='PLAYER NAME').merge(green_in_reg_df, on='PLAYER NAME')


# add additional metrics
# calculate how many additional green we expect each player to make in regulation compared to the average
AVERAGE_GREEN_PERCENTAGE = combined['GREENS %'].mean() / 100
combined['GIR% - AVG%'] = (combined['GREENS %']/100 - AVERAGE_GREEN_PERCENTAGE) * 72

# calculate total strokes gained putting
combined['TOTAL SG:PUTTING'] = combined['AVERAGE SG:PUTTING'] * 4

# calculate total strokes gained off the tee
combined['TOTAL SG:OTT'] = combined['AVERAGE SG:OTT'] * 4

# calculate the predictive score
combined['PREDICTIVE SCORE'] = combined['GIR% - AVG%'] + combined['TOTAL SG:PUTTING'] + combined['AVERAGE SG:OTT']


# sort by new metric
combined = combined.sort_values(by='PREDICTIVE SCORE', ascending=False)

# export combined to csv
combined.to_csv('golf_stats.csv', index=False)