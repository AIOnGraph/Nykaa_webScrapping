import asyncio
from bs4 import BeautifulSoup
import csv
import time
import aiohttp

count = 0
csvFile = {}

async def productDetailsExtractor(session, url):
    async with session.get(url) as response:
        html_txt = await response.text()
        soup = BeautifulSoup(html_txt, features="html.parser")
        prod_name = soup.find(class_="css-1gc4x7i").text
        image_link = soup.find('div', class_='css-5n0nl4').select_one("img").get('src')
        mrp = soup.find('span', class_="css-u05rr").text
        price = soup.find('span', 'css-1jczs19').text
        rating = soup.find('div', class_='css-m6n3ou')
        if rating:
            rating = rating.text
        return {
            "title": prod_name,
            "image": image_link,
            "mrp": mrp,
            'price': price,
            "rating": rating
        }

async def addToDictionary(obj):
    csvFile['productName'] = obj["title"]
    csvFile['imageLink'] = obj["image"]
    csvFile['productMrp'] = obj["mrp"]
    csvFile['price'] = obj['price']
    csvFile['Ratings'] = obj["rating"]

async def writeToCSV():
    with open('asyncio.csv', mode='a') as file:
        dictKeys = csvFile.keys()
        csvWriter = csv.DictWriter(file, fieldnames=dictKeys)
        global count
        if count == 0:
            csvWriter.writeheader()
            count += 1
        csvWriter.writerow(csvFile)

async def productListExtractor(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            respons = await response.text()
            soup2 = BeautifulSoup(respons, features="html.parser")
            prod_link = []
            links = soup2.find_all(class_='css-qlopj4')
            if links:
                for link in links:
                    prod_link.append("https://www.nykaa.com" + link['href'])
                return prod_link
            return None

async def searchPageExtractor(search_term):
    url = f'https://www.nykaa.com/search/result/?q={search_term}&root=search&searchType=Manual&sourcepage=Category+Page'
    product_links = await productListExtractor(url)
    if product_links:
        tasks = []
        async with aiohttp.ClientSession() as session:
            for product_link in product_links:
                task = asyncio.create_task(productDetailsExtractor(session, product_link))
                tasks.append(task)
            for task in tasks:
                product_details = await task
                await addToDictionary(product_details)
                await writeToCSV()

async def main():
    await searchPageExtractor('eyeliner')

if __name__ == "__main__":
    startTime = time.perf_counter()
    asyncio.run(main())
    endTime = time.perf_counter()
    print(endTime - startTime)