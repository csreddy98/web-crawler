
# get metadata from a webpage

import requests
from bs4 import BeautifulSoup as bs
from classes.database import *

# create a function to get the metadata from a webpage and list of all the links on the page and keep track of the number of links that are not visited

BASE_URL = "<YOUR BASE URL>"
QUEUE = Links(BASE_URL)
db = Database()
CURRENT_URL_INDEX = 1
print("1")


def get_content(url):
    try:
        r = requests.get(url, timeout=10)
        return bs(r.text, "html.parser")
    except Exception as e:
        print(f"SSL Error: {e}")
        return None
    
    
def get_links(url):
    soup = get_content(url)
    links = []
    for a in soup.find_all("a"):
        links.append(a.get("href"))
        QUEUE.add_link_to_queue(a.get("href"))
    return links

def get_metadata(url):
    soup = get_content(url)
    metadata = {}
    metadata["title"] = soup.title.string if soup.title != None else ""
    metadata["meta_description"] = soup.find("meta", {"name": "description"}).get("content") if soup.find("meta", {"name": "description"}) != None else ""
    metadata["meta_title"] = soup.find("meta", {"name": "title"}).get("content") if soup.find("meta", {"name": "title"}) != None else ""
    metadata["og_title"] = soup.find("meta", {"property": "og:title"}).get("content") if soup.find("meta", {"property": "og:title"}) != None else ""
    metadata["og_description"] = soup.find("meta", {"property": "og:description"}).get("content") if soup.find("meta", {"property": "og:description"}) else ""
    metadata["og_image"] =  soup.find("meta", {"property": "og:image"}).get("content") if soup.find("meta", {"property": "og:image"}) != None else ""
    metadata["og_url"] = soup.find("meta", {"property": "og:url"}).get("content") if soup.find("meta", {"property": "og:url"}) != None else ""
    metadata["og_site_name"] = soup.find("meta", {"property": "og:site_name"}).get("content") if soup.find("meta", {"property": "og:site_name"}) != None else "" 
    db.insert_metadata(metadata["title"], metadata["meta_description"], metadata["og_description"], metadata["og_image"], metadata["og_url"], metadata["og_site_name"])
    return metadata

def get_body_content(url):
    soup = get_content(url)
    paragraphs = "" # seperate paragraphs with a <STOP> tag
    for p in soup.find_all("p"):
        paragraphs += p.text + "<STOP>"
    spans = "" # seperate spans with a <STOP> tag
    for span in soup.find_all("span"):
        spans += span.text + "<STOP>"
    headings = "" # seperate headings with a <STOP> tag
    for h in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"]):
        headings += h.text + "<STOP>"
    lists = "" # seperate lists with a <STOP> tag
    for li in soup.find_all("li"):
        lists += li.text + "<STOP>"
    title = soup.title.string if soup.title != None else ""
    db.insert_body_content(db.get_url_id(url), title, paragraphs, spans, headings, lists)
    
    return paragraphs, spans, headings, lists

def get_images(url):
    soup = get_content(url)
    images = []
    for img in soup.find_all("img"):
        images.append({
            "src": img.get("src") if img.get("src") != None else "",
            "alt": img.get("alt") if img.get("alt") != None else "",
            "page_title": soup.title.string if soup.title != None else "",
            "page_url": url
        })
        title = soup.title.string if soup.title != None else ""
        if img.get("src") != None and img.get("src") != "" and img.get("src").startswith("data:image") == False:
            db.insert_images(img.get("src"), img.get("alt"), title, url)
    return images

# get all the links on the page and add them to the queue



# start the crawler

if __name__ == "__main__":
    print("2")
    while QUEUE.has_links():
        print(len(QUEUE.get_unvisited_links()))
        url = QUEUE.get_next_link()
        print(url)
        if get_content(url) != None and db.is_page_indexed(url) == False:
            print("STARTED")
            CURRENT_URL_INDEX += 1
            if url is not None:
                print("Crawling URL: " + url)
                if "uta.edu" in url:
                    get_links(url)
                if db.is_page_indexed(url) == False:
                    get_metadata(url)
                    get_body_content(url)
                    get_images(url)
                    db.update_link_status(url, 1)
                print("Crawled URL: " + url)
                print("Number of links in queue: " + str(len(QUEUE.queue)) + " Number of links crawled: "+ str(CURRENT_URL_INDEX) + f"/{len(db.get_unvisited_links())}" )
            else:
                print("URL is None")



