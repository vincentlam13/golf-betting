from bs4 import BeautifulSoup
import requests
import pandas as pd
import time

# test 2018 The Open Championship

tournament_codes = {"Masters Tournament": "t014", 
                     "PGA Championship": "t033",
                     "U.S. Open": "t026",
                     "The Open Championship": "t100"}

stat_code_list = ['02567', '02564', '103']
stat_list = ['sg_ott', 'sg_putting', 'green_in_reg']
tournament_list = ["Masters Tournament", "PGA Championship", "U.S. Open", "The Open Championship"]

def golf_scraper(year, tournament):
    for i in range(len(stat_code_list)):
        new_link = 'https://www.pgatour.com/content/pgatour/stats/stat.' + stat_code_list[i] + '.y' + year + '.eoff.' + tournament_codes.get(tournament) + '.html'
               
        time.sleep(1)
    
        r = requests.get(new_link)
        soup = BeautifulSoup(r.content, 'lxml')
        
        # get table headings
        table_headers = []
        for tx in soup.find_all('th'):
            table_headers.append(tx.text)
        
        # get table data
        data = []
        table = soup.find('table', attrs={'class':'table-styled'})
        table_body = table.find('tbody')
        
        rows = table_body.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele])
       
       
        df = pd.DataFrame(data, columns=table_headers)
        
        # only select the player name and the desired metric
        df_clean = df.iloc[:, [2,4]]
                
        # export to csv
        df_clean.to_csv(year + '_' + tournament + '_' + stat_list[i] + '.csv', index=False)
        
    # load the data
    path = 'C:/users/vinhe/code/projects/golf/testing/'
    sg_ott_df = pd.read_csv(path + year + '_' + tournament + '_sg_ott.csv')
    sg_putting_df = pd.read_csv(path + year + '_' + tournament + '_sg_putting.csv')
    green_in_reg_df = pd.read_csv(path + year + '_' + tournament + '_green_in_reg.csv')
    
    # rename columns
    sg_ott_df = sg_ott_df.rename(columns={'AVERAGE': 'AVERAGE SG:OTT'})
    sg_putting_df = sg_putting_df.rename(columns={'AVERAGE': 'AVERAGE SG:PUTTING'})
    green_in_reg_df = green_in_reg_df.rename(columns={'%': 'GREENS %'})
    
    
    # merge columns on player name
    combined = sg_ott_df.merge(sg_putting_df, on='PLAYER NAME').merge(green_in_reg_df, on='PLAYER NAME')
    
    # drop rows where PLAYER NAME is a number
    combined = combined[~combined['PLAYER NAME'].str.isnumeric()]
    
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
    combined.to_csv(year + '_' + tournament + '_golf_stats.csv', index=False)
    

golf_scraper('2014', 'PGA Championship') 
