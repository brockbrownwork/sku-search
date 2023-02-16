import requests
import webbrowser
from concurrent.futures import ThreadPoolExecutor, as_completed
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
            return url, title
        else:
            elapsed_time += 1
            time.sleep(1)

    raise TimeoutError("Timeout reached while waiting for title")

stores = ['zales', 'zalesoutlet', 'jared', 'kay', 'peoplesjewellers']

def search_sku(sku):
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(get_title, f"http://www.{store}.com/search?text={sku}") for store in stores]
        for future in as_completed(futures):
            url, title = future.result()
            if "Search" not in title:
                webbrowser.open(url)

while True:
    print("Type in the SKU you'd like to search for.")
    sku = input("> ")
    start = time()
    if sku == 'q':
        break
    search_sku(sku)
    print("Done!")
    end = time()
    print(f"Time taken: {end - start} seconds.")
    google = input("Would you like to run a Google query of the SKU? (y/n) > ")
    if google.lower() == "y":
        webbrowser.open(f'https://www.google.com/search?q="{sku}"')
