import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

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


url = 'http://bpbasecamp.freeforums.net/board/27/gear-closet'
thread = '/thread/2131/before-asking-which-pack-boot'
# thread_url = urljoin(url, thread)
thread_url = "https://bpbasecamp.freeforums.net/thread/17578/sleeping-pads"

posts = get_thread_posts(thread_url)
print(posts)