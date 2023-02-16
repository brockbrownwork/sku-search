import requests
import webbrowser
import threading
from time import sleep, time
from bs4 import BeautifulSoup

def get_title(url, timeout=10):
    response = requests.get(url, timeout=timeout)

    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the title tag and wait until it's present
    elapsed_time = 0
    while elapsed_time < timeout:
        title_tag = soup.find('title')
        if title_tag:
            title = title_tag.string
            return title
        else:
            elapsed_time += 1
            time.sleep(1)

    raise TimeoutError("Timeout reached while waiting for title")

def get_titles(urls, timeout=10):
    threads = []
    results = {}
    for url in urls:
        t = threading.Thread(target=lambda: results.update({url: get_title(url, timeout=timeout)}))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    return results

stores = ['zales', 'zalesoutlet', 'jared', 'kay', 'peoplesjewellers']

def search_sku(store_name, sku):
    urls = [f"http://www.{store_name}.com/search?text={sku}" for store_name in stores]
    titles = get_titles(urls)
    for url, title in titles.items():
        if "Search" not in title:
            webbrowser.open(url)

while True:
    print("Type in the SKU you'd like to search for.")
    sku = input("> ")
    start = time()
    if sku == 'q':
        break
    threads = []
    print("Loading...")
    thread = threading.Thread(target = search_sku, args = (stores, sku))
    threads.append(thread)
    thread.start()
    for thread in threads:
        thread.join()
    print("Done!")
    end = time()
    print(f"Time taken: {end - start} seconds.")
    google = input("Would you like to run a google query of the SKU? (y/n) > ")
    if google.lower() == "y":
        webbrowser.open(f'https://www.google.com/search?q="{sku}"')
