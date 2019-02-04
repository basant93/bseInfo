import requests 
from bs4 import BeautifulSoup 
import time
import csv
from zipfile import ZipFile
import json
from redis_server import FilterRedis

bse_url = "https://www.bseindia.com/markets/MarketInfo/BhavCopy.aspx" 

def download_zip_file():

    store = FilterRedis()
    file_name = "ankit" + time.strftime("%Y%m%d-%H%M%S")


    page = requests.get(bse_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    r = soup.find_all(id="ContentPlaceHolder1_btnhylZip")
    href_val = ""
    for a in r:
        if a.text:
            href_val =a['href']
    zip_file = requests.get(href_val, stream = True)

    with open(file_name, 'wb') as f:
        for chunk in zip_file.iter_content(chunk_size=1024 * 1024):
            if(chunk):
                f.write(chunk)

    print(href_val)
    with ZipFile(file_name, 'r') as zip:
        zip.extractall()
        print("Done")

    csv_file = "/home/basant/Desktop/WebInfo/EQ010219.CSV"
    with open(csv_file, 'r') as csvfile: 
    # creating a csv reader object 
        #csvreader = csv.reader(csvfile) 
        csvreader = csv.DictReader(csvfile)
        
        # extracting field names through first row 
        fields = next(csvreader) 
        print(fields)
    
        # extracting each data row one by one 
        for row in csvreader: 
            data = {
                'SC_CODE': row['SC_CODE'],
                'SC_NAME': row['SC_NAME'],
                'OPEN': row['OPEN'],
                'HIGH': row['HIGH'],
                'LOW' : row['LOW'],
                'CLOSE' : row['CLOSE']
            }
            store.push(data)

    
        print(row['SC_CODE'],row['SC_NAME'], row['OPEN'], row['HIGH'], row['LOW'], row['CLOSE']) 
        print(store.fetch_all())
        return store.fetch_all()


def main():

    download_zip_file()



if __name__ == "__main__":
    main()









