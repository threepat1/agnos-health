import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def scrape_forum():
    base_url = "http://www.agnoshealth.com"
    forum_url = f"{base_url}/forums"

    response = requests.get(forum_url)
    if response.status_code != 200:
        print("Error fetching main page:", response.status_code)
        return []

    soup = BeautifulSoup(response.content, "html.parser")
    posts = []
    visited = set()

    for a in soup.find_all("a", href=True):
        link = a["href"]

        # Only keep /forums/... links that look like threads
        if link.startswith("/forums/") and "search" not in link and "list" not in link:
            full_url = urljoin(base_url, link)
            if full_url not in visited:
                visited.add(full_url)
                print("Scraping:", full_url)

                res = requests.get(full_url)
                if res.status_code == 200:
                    thread_soup = BeautifulSoup(res.content, "html.parser")
                    text = thread_soup.get_text(separator=" ", strip=True)
                    if text:
                        posts.append(text)

    print(f"Scraped {len(posts)} threads")
    return posts

if __name__ == "__main__":
    scrape_forum()
