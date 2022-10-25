import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def get_forum_threads(url, max_pages=None):
    board = urlparse(url).path.split("/")[-1]
    print("Scraping board: ", board)
    page = 1
    threads = []
    while not max_pages or page <= max_pages:
        print("scraping forum page: ", page)
        r = requests.get(url, params={"page": page})
        bs = BeautifulSoup(r.text, "lxml")
        links = bs.find_all("a", attrs={"href": re.compile('^\/thread\/')})
        threads_on_page = [a.get("href") for a in links if a.get("href") and not "page" in a.get("href") and not "/thread/new" in a.get("href")] 
        threads += threads_on_page
        page += 1
        next_page = bs.find("li", class_="next")
        if "state-disabled" in next_page.get("class"):
            break

    return threads

url = 'http://bpbasecamp.freeforums.net/board/27/gear-closet'
threads = get_forum_threads(url, max_pages=5)
print(threads)