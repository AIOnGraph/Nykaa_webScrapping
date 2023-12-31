'''Importing the required modules'''
import requests
from bs4 import BeautifulSoup 
import csv
import time 

count= 0 
csvFile = {}

'''This function will extract the details of the each single product'''
def productDetailsExtractor(url):    
    html_txt = requests.get(url)
    soup = BeautifulSoup(html_txt.text,features="html.parser")
    prod_name = soup.find(class_="css-1gc4x7i").text
    image_link = soup.find('div',class_= 'css-5n0nl4').select_one("img").get('src')
    mrp = soup.find('span',class_="css-u05rr").text
    price= soup.find('span','css-1jczs19').text
    rating=soup.find('div',class_='css-m6n3ou')
    if rating:
        rating=rating.text
    return {
        "title": prod_name,
        "image": image_link,
        "mrp": mrp,
        'price':price,
        "rating": rating
    }
'''This function will append the product deatils to the dictionary'''   
def addToDictionary(obj):
    csvFile['productName']=obj["title"]
    csvFile['imageLink']=obj["image"]
    csvFile['productMrp']=obj["mrp"]
    csvFile['price']=obj['price']
    csvFile['Ratings']=obj["rating"]
    # print(csvFile)

'''this function will append the all extracted data to the csv file'''    
def writeToCSV():
    with open('Scrape.csv', mode='a') as file:
        dictKeys = csvFile.keys()  
        csvWriter = csv.DictWriter(file,fieldnames=dictKeys)
        global count
        if count==0:
            csvWriter.writeheader()            
            count+=1            
        csvWriter.writerow(csvFile)


'''It will extract all the  product list from the url and return the product url'''
def productListExtractor(url):
    respons = requests.get(url).content
    soup2 = BeautifulSoup(respons,features="html.parser")
    prod_link=[]
    links= soup2.find_all(class_='css-qlopj4')
    if links:
        for link in links:
            prod_link.append("https://www.nykaa.com"+link['href'])
        return prod_link
    return None

# keyword based search
def searchPageExtractor(searchTerm):
        url=f'https://www.nykaa.com/search/result/?q={searchTerm}&root=search&searchType=Manual&sourcepage=Category+Page'
        # Appending the list of url in productDetailsExtractor for getting product details
        productLinks=productListExtractor(url)        
        if productLinks:
            for productLink in productLinks:
                productDetails= productDetailsExtractor(productLink)
                addToDictionary(productDetails)
                writeToCSV() 




def main():
    searchPageExtractor('lipstick')
    
    

if __name__=="__main__":
    startTime= time.perf_counter()
    main()
    endTime= time.perf_counter()
    print(endTime-startTime)






