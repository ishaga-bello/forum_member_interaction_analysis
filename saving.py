import json
import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

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

def get_thread_posts(url, max_pages=None):
    page = 1
    posts = []
    while not max_pages or page <= max_pages:
        print("Scraping thread url/page", url, page)
        r = requests.get(url, params={"page": page})
        bs = BeautifulSoup(r.text, "lxml")
        content = bs.find(class_="content")

        for post in content.find_all("tr", class_="item"):
            info = {}
            user = post.find("a", class_="user-link")
            if not user:
                # user might be deleted, skip...
                continue
            user = user.text
            info["user"] = user
            quotes = []
            for quote in post.find_all(class_="quote_header"):
                quoted_user = quote.find("a", class_="user-link")
                if quoted_user:
                    quotes.append(quoted_user.text)
                    info["quoted"] = quotes
            # posts.append((user, quotes))
            posts.append(info)

        page += 1
        next_page = bs.find("li", class_="next")
        if "state-disabled" in next_page.get("class"):
            break
    return posts

url = "http://bpbasecamp.freeforums.net/board/27/gear-closet"

threads = get_forum_threads(url, max_pages=2)
all_posts = []

for thread in threads:
    thread_url = urljoin(url, thread)
    posts = get_thread_posts(thread_url)
    all_posts.append(posts)

print(all_posts)

with open("forum_posts.json", "w") as file:
    json.dump(all_posts, file)