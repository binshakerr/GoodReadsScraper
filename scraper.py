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

if __name__ == "__main__":
    results = scrape_quotes("https://www.goodreads.com/quotes")
    print(results)