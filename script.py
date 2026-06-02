from bs4 import BeautifulSoup
import requests
import time
from urllib.parse import urljoin
import pandas as pd

url = "https://books.toscrape.com/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests":  "1",
    "Referer": "https://www.google.com/"
}
starConverter = {
    "One": 1, 
    "Two": 2, 
    "Three": 3, 
    "Four": 4, 
    "Five": 5
}

data = []

print("Welcome to the Book Scraper!")
price_input = float(input("Enter your maximum budget: £"))
star_input = int(input("Enter your minimum rating you want: "))

i = 0

main_page = requests.get(url, headers=headers, timeout=10)
main_soup = BeautifulSoup(main_page.content, "html.parser")

category_list = main_soup.find("ul", class_="nav-list")
categories = category_list.find_all("a")[1:]

for category in categories:
    genre = category.text.strip()
    mergeUrl = urljoin(url, category['href'])

    flag = False 

    while True:
        response = requests.get(mergeUrl, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")
        books = soup.find_all("article", class_="product_pod")
        for book in books:
            title = book.h3.a["title"]

            star_tag = book.find("p", class_="star-rating")
            if star_tag:
                classList = star_tag["class"]
                rating = starConverter[classList[1]]

            price_tag = book.find("p", class_="price_color")
            if price_tag:
                rawPrice_tag = price_tag.text.strip()
                price = float(rawPrice_tag[1:])
                if price <= price_input and rating >= star_input:
                    if not flag:
                        print()
                        print(genre)
                        flag = True
                    print(f"{title} | Price: £{price} | Rating: {rating} | Genre: {genre}")
                    
                    dataItem = {
                        "Title" : title,
                        "Price" : price,
                        "Rating" : rating,
                        "Genre" : genre
                    }

                    data.append(dataItem)  
                    i += 1

        nextButton = soup.find("li", class_="next") 
        if nextButton:
            next = nextButton.find("a")["href"]
            mergeUrl = urljoin(mergeUrl, nextButton.a['href']) 
            time.sleep(1)
        else:
            break

        
    time.sleep(1)

print()
df = pd.DataFrame(data)
df.to_csv("scraped_data.csv", index=False)

print(f"Total perfect matches found across all genres: {i}")   
print("Done! Saved to scraped_data.csv")         
