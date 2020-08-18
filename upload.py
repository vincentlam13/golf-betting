# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 18:53:02 2020

@author: vinhe

I followed below tutorial to push newly created csv to google sheets:
https://medium.com/craftsmenltd/from-csv-to-google-sheet-using-python-ef097cb014f9

"""


import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds", 
         "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file", 
         "https://www.googleapis.com/auth/drive"]

credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(credentials)

spreadsheet = client.open('golf-csv-to-sheets')

with open('C:/users/vinhe/code/projects/golf/golf_stats.csv', 'r') as file_obj:
    content = file_obj.read()
    client.import_csv(spreadsheet.id, data=content)


