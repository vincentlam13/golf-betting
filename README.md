# Golf Betting: Project Overview
- Created a tool to predict likely winners of PGA tournaments.
- Scraped PGA stats website for useful determinative data.
- Created new metrics to predict winners based on domain knowledge.
- Created a script to send the DataFrame csv file to google sheets, using gspread (a Python API for Google Sheets).
- Created a function to test model against historic data.

## Code and Resources Used
**Python Version:** 3.8

**Packages:** pandas, beautifulsoup, requests, gspread, oauth2client

## Web Scraping

## Golf Prediction

## Testing Prediction Against Historic Tournaments

| Year  | Tournament  | Golfer  | Predictive Ranking  | Real Position  |
|---|---|---|---|---|
|  2019 | The Open Championship  | Brooks Koepka  |  11 |  4 |
| 2018  | The Open Championship  | Justin Rose  | 4  | 2  |
| 2017  | The Open Championship |  Jordan Spieth | 4  |  1 |
| 2017  | US Open  |  Rickie Fowler | 2  |  5 |
|  2016 | The Open Championship  | Sergio Garcia  | 6  | 5  |
|  2014 | PGA Championship  | Rory Mcllroy  | 1  |  1 |

## To Do List
- Test how successful the predictive score is for historic tournaments and the relevant data at that time. 
- Automate the process of placing bets.
- Keep record of real world results.
- Reiterate metrics and add weightings to improve predictive score.
