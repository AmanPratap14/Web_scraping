from bs4 import BeautifulSoup
import requests
from csv import DictReader
import json 
import time

start_time = time.time()
csv_file = open("Amazn_Scraping_sheet.csv","r",encoding="utf-8")
csv_data = DictReader(csv_file)
master_data = {}
for row in csv_data:
    url = "https://www.amazon."+row['country']+"/dp/"+row['Asin']
    print(url)
    x = requests.get(url)
    if (x.status_code == 200):
        soup = BeautifulSoup(x.text, 'html.parser')
        try:
            images = soup.find(id="imgBlkFront").get('data-a-dynamic-image')
        except AttributeError:
            images = "Not found"

        try:
            price = soup.find(
                "span",
                class_="a-size-base a-color-price a-color-price").get_text()
        except AttributeError:
            price = "Not found"
        
        try:
            desc = soup.find(
            "div",
            class_="a-section a-spacing-small a-padding-small").get_text()
        except AttributeError:
            desc = "Not found"

        try:
            title = soup.find(id="productTitle").get_text()
        except AttributeError:
            title = "Not found"
        data = {"url":url,"httpd-code":x.status_code,"image":images,"title":title,"price":price,"description":desc,"status":"success","error":"False"}
        # print(data)
        master_data[row['id']]= data
    else:
        # print("CANT EXTRACT THIS SITE:", url, "SCode: ", x.status_code)
        data = {"id":row['id'],"url":url,"httpd-code":x.status_code,"image":"","title":"","price":"","description":"","status":"Not Found","error":"True"}
        master_data[row['id']]= data

with open('result.json', 'w') as fp:
    json.dump(master_data, fp)
end_time = time.time()
print('Execution time:', end_time - start_time, 'seconds')