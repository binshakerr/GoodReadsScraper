import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup

load_dotenv()
PROXY = os.getenv("PROXY")
proxies = {
    "http": PROXY,
    "https": PROXY
}

def scrape_quotes(url):
    r = requests.get(url, proxies=proxies)
    soup = BeautifulSoup(r.text, features="html.parser")
    quotes_container = soup.find("div", class_="quotes")
    quotes = quotes_container.find_all("div", class_="quote")
    
    results = []
    for quote in quotes:
        quoteText = quote.find("div", class_="quoteText").text
        details = {}
        details["quote"] = quoteText.split("―")[0].strip()
        details["author"] = quoteText.split("―")[1].strip()

        tags_container = quote.find("div", class_="smallText")
        try:
            tag_links = tags_container.find_all("a")
            tag_list = [x.text for x in tag_links]
            details["tags"] = ", ".join(tag_list)
        except:
            pass 
        
        results.append(details)
    
    return results


def scrape_all_quotes():
    results = []
    i = 1
    while True:
        try:
            url = "https://www.goodreads.com/quotes?page=" + str(i)
            sub_results = scrape_quotes(url)
            print("scraping page: " + str(i))
            # Goodreads page size = 30, and it duplicates last page results after reaching end of pages 
            if results[-30:] == sub_results:
                break 
            results += sub_results
            i+= 1
        except Exception as e:
            print(e)
            break 


    return results


if __name__ == "__main__":
   result = scrape_all_quotes()
   print(result[99])