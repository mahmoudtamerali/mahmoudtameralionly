#this script is to scrap facebook pages to detect new post

#librarys
from facebook_page_scraper import Facebook_scraper
import json
import time
import random
import requests


# Read the proxy list from the JSON file
with open("Free_Proxy_List.json") as proxyfile:
    proxies = json.load(proxyfile)
num_of_proxies = len(proxies)-1

#the properties of each calls to librarys
posts_count = 1
browser = "chrome"
timeout = 210 #210 seconds
headless = True


pages_to_be_fetched = [["ITI.eg",""],["nti.egypt",""],["Stunion",""],["MCITEgypt",""]]
#pages_to_be_fetched = [["t3chroh",""]]

def make_warning():
    esp_url = "http://192.168.0.150/H"
    response = requests.get(esp_url)
    counter = 0
    while (response.status_code != 200) and counter < 2 :
        response = requests.get(esp_url)
        counter += 1





#this function returns the content of the post got
def get_last_post_content (id_of_page):
        
    #start fetching the page for the last post
    print(f"\nfetching {id_of_page} ...") 
    
    #loop until valid output
    while (True):
        
        #set the proxy to not got banned
        random_number = random.randint(0, num_of_proxies)
        proxy_ip = proxies[random_number]["ip"]
        proxy_port = proxies[random_number]["port"]
        proxy = f"{proxy_ip}:{proxy_port}"
        print(f"we used proxy {proxy}")                                     #not neccessary


        meta_ai = Facebook_scraper(id_of_page, posts_count, browser, timeout=timeout, headless=headless)

        #reading the output of fetching
        try:
            json_data = meta_ai.scrap_to_json()
        except Exception as e:
            json_data = -1
        #check that it could fetch the page
        if (json_data != -1):
            break #if correct leave the loop
        else:
            print("failed to fetch, retrying...")
            time.sleep(3)
        

    # Parse JSON data
    data = json.loads(json_data)

    # Get the content from the post got
    for id, item in data.items():
        gotcontent = item['content']

    # Print the extracted key
    print("we got the content")                                         #not neccessary
    
    return gotcontent


#initialize the content that we store
for page in pages_to_be_fetched:
    page[1] = get_last_post_content(page[0])

#here the life time loop of the program to search in all pages
while True:
    for page in pages_to_be_fetched: #loop over all pages
        last_post_content = get_last_post_content(page[0])
        if((last_post_content)[:150] != page[1][:150]):

            #here we found out that there is new post arrived, do whatever you want here
            print("found new post!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            make_warning()
            #setting up the new post as our latest
            page[1] = last_post_content

        time.sleep(5)
