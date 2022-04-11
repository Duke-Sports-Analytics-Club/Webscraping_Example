from bs4 import BeautifulSoup
import csv
import requests
import pandas as pd

df = pd.read_csv(r'/Users/namhlahade/Documents/GitHub/DSAC-Fantasy-Football/WebScraping/nameAndPosition.csv')
qbDf = df.loc[df["Position"] == "QB"]

qbUrlList = qbDf['URL'].tolist()
qbNameList = qbDf['Name'].tolist()

res = {}
for key in qbUrlList:
    for value in qbNameList:
        res[key] = value
        qbNameList.remove(value)
        break 

header = ["Name", "Year", "Team","Age", "No.", "G", "GS", "QBrec", "Cmp", "Att", "Cmp%", "Yds", "TD", "TD%", "Int", "Int%", "1D", "Lng", "Y/A", "AY/A", "Y/C", "Y/G", "Rate", "QBR", "Sk", "Yds", "Sk%", "NY/A", "ANY/A", "4QC", "GWD", "AV"]
with open('/Users/namhlahade/Documents/GitHub/DSAC-Fantasy-Football/WebScraping/rbStats.csv', 'w', encoding='UTF8') as f:
    
    writer = csv.writer(f)
    writer.writerow(header)
    for qb in qbUrlList:
        try:
            page = requests.get(qb)
            soup = BeautifulSoup(page.content, "html.parser")
            table = soup.find('table', {'id':'passing'})
            tbody = table.find('tbody')

            rows = tbody.find_all('tr')
            for row in rows:
                data1 = row.find_all('td', {'class':'right'})
                newData = []
                newData.append(res[qb])
                newData.append(row.find('th').find('a').get_text()) #adding year to newData
                newData.append(row.find('td', {'class':'left'}).find('a').get_text()) #Adding team to newData
                for data in data1:
                    newData.append(data.get_text())
                writer.writerow(newData)

            print('done')
        
        except AttributeError:
            print(qb)