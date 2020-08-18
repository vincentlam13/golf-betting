"""
The purpose of this tool is to help predict future winners of golf tournaments.
This pga web scraper takes the metrics that I am interested in:
- strokes gained off the tee
- strokes gained putting
- green in regulation %

"""
# import libraries
from bs4 import BeautifulSoup
import requests
import pandas as pd

sg_ott = 'https://www.pgatour.com/stats/stat.02567.html'
sg_putting = 'https://www.pgatour.com/stats/stat.02564.html'
green_in_reg = 'https://www.pgatour.com/stats/stat.103.html'

urls = [sg_ott, sg_putting, green_in_reg]

for url in urls:
    r = requests.get(url)
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
    if url == sg_ott:
        df_clean.to_csv('sg_ott.csv', index=False)
    elif url == sg_putting:
        df_clean.to_csv('sg_putting.csv', index=False)
    else:
        df_clean.to_csv('green_in_reg.csv', index=False)
    
