from bs4 import BeautifulSoup
import requests
import csv

url = "https://www.pro-football-reference.com/players/"

alphabetList = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
h = ["Name", "Position", "Years", "URL"]
csvList = []

for letter in alphabetList:
    newUrl = url + letter.capitalize() + '/'
    page = requests.get(newUrl)
    soup = BeautifulSoup(page.content, "html.parser")

    divTag = soup.find('div',{'class':'section_content'})
    pTag = divTag.find_all('p')

    for p in pTag:
        line = p.get_text()
        newLine = line.split(" ")
        urlEnd = p.find('a')
        href = urlEnd.get('href')
        urlCSV = "https://www.pro-football-reference.com" + href
        if int(newLine[len(newLine)-1].split("-")[0]) >= 2010:
            if (len(newLine) == 4):
                csvList.append([str(newLine[0] + " " + newLine[1]), str(newLine[2].replace("(","").replace(")","")), str(newLine[3]), str(urlCSV)])
            if (len(newLine) == 5):
                csvList.append([str(newLine[0] + " " + newLine[1] + " " + newLine[2]), str(newLine[3].replace("(","").replace(")","")), str(newLine[4]), str(urlCSV)])

print(csvList)

with open('/Users/namhlahade/Documents/GitHub/tempScraper/nameAndPosition.csv', 'w', encoding='UTF8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(h)
    for r in csvList:
        writer.writerow(r)
