import requests
import webbrowser

stores = ['zales', 'jared', 'kay', 'peoplesjewellers']

while True:
    print("Type in the SKU you'd like to search for.")
    sku = input("> ")
    if sku == 'q':
        break
    found = False
    for store in stores:
        r = requests.get(f"http://www.{store}.com/search?text={sku}")
        if "search" in r.url:
            print(f"Couldn't find it at {store}")
        else:
            print(f"Found it at {store}, opening browser...")
            webbrowser.open(r.url)
            found = True
            break
    if not found:
        print(f"Couldn't {sku} anywhere.\n")
