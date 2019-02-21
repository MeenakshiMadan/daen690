##############################################
####  Web scrapper for slashdot articles #######
####  Author: Meenakshi               ##########
###  Date: 19th Feb 2018              #########
#############################################
import requests
from bs4 import BeautifulSoup
import csv
#collecting the first page for drone related articles
page = requests.get('https://slashdot.org/tag/bitcoin')
page.status_code
page.content

#creating a BeautifulSoup Object to be used and parsing through children
soup=BeautifulSoup(page.text,'html.parser')
list(soup.children)
html=list(soup.children)[4]
list(html.children)
html1=list(soup.children)[6]
[type(item) for item in list(html1.children)]
subset=list(html1.children)[10]


[type(item) for item in list(subset.children)]
subset_data=list(subset.children)

#finding all the actual data from the tags 
actual_data=html1.find_all('td')
len(actual_data)

#making a file to be written
f = csv.writer(open('Bitcoin.csv', 'w'))
f.writerow(['DATE','HEADLINE'])


#parsing through the list and seperating the dates and headlines from the text
for x in range(0,400):
    if(x%2==0):
        headline_date=list(actual_data)[x].get_text()
        head, sep, tail = headline_date.partition('@')  
        #print(head)
    else:
        headline_text=list(actual_data)[x].get_text()
        #print(headline_text)
        #print(head, headline_text)
        f.writerow([head, headline_text])###writting the date and headlines in the file####
        
