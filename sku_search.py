import requests
import webbrowser
import threading
from time import sleep, time

stores = ['zales', 'jared', 'kay', 'peoplesjewellers']

def search_sku(store_name, sku):
    r = requests.get(f"http://www.{store}.com/search?text={sku}")
    if not "search" in r.url:
        webbrowser.open(r.url)

while True:
    print("Type in the SKU you'd like to search for.")
    sku = input("> ")
    start = time()
    if sku == 'q':
        break
    threads = []
    for store in stores:
        thread = threading.Thread(target = search_sku, args = (store, sku))
        threads.append(thread)
        thread.start()
    while any([i.is_alive() for i in threads]):
        pass
    print("Done!")
    end = time()
    print(f"Time taken: {end - start} seconds.")
