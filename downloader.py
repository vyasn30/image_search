from bs4 import *
import json
import requests
import os
import scrapper
# import urllib.request

# CREATE FOLDER
image_count = 0
link_maps = dict()
def folder_create(images):
    try:
        folder_name = input("Enter Folder Name:- ")
        # folder creation
        os.mkdir(folder_name)
 
    # if folder exists with that name, ask another name
    except:
        print("Folder Exist with that name!")
        folder_create()
 
    # image downloading start
    download_images(images, folder_name)
    


def download_images_from_links(links, single_url):
    # os.mkdir("Downloads")
    print("downloading")
    # link_maps = dict()
    global link_maps
    
    global image_count
    for url in links:
        if image_count == 100:
            break
        if url.split(".")[-1] in ("jpg", "jpeg", "png","jfif"):
            try:
                print(image_count)
                print(url)
                r = requests.get(url)
                image_path = os.path.join("Downloads", str(image_count)+".jpg") 
                with open(image_path, "wb") as outFile:
                    outFile.write(r.content)
                    outFile.close()
                
                link_maps[image_path] = single_url




                # urllib.request.urlretrieve(url, os.path.join("Downloads", str(image_count)+".jpg"))    
                image_count+=1

            except Exception as e:
                print(e)
                continue
    with open("vecdata/link_maps.json", "w") as outputFile:
        json.dump(link_maps, outputFile)
        
    print(link_maps)



# DOWNLOAD ALL IMAGES FROM THAT URL
def download_images(images, url):
   
    # initial count is zero
    count = 0
 
    # print total images found in URL
    print(f"Total {len(images)} Image Found!")
    image_links = []
    # checking if images is not zero
    if len(images) != 0:
        for i, image in enumerate(images):
            # From image tag ,Fetch image Source URL
 
                        # 1.data-srcset
                        # 2.data-src
                        # 3.data-fallback-src
                        # 4.src
 
            # Here we will use exception handling
 
            # first we will search for "data-srcset" in img tag
            try:
                # In image tag ,searching for "data-srcset"
                image_link = image["data-srcset"]
                 
            # then we will search for "data-src" in img
            # tag and so on..
            except:
                try:
                    # In image tag ,searching for "data-src"
                    image_link = image["data-src"]
                except:
                    try:
                        # In image tag ,searching for "data-fallback-src"
                        image_link = image["data-fallback-src"]
                    except:
                        try:
                            # In image tag ,searching for "src"
                            image_link = image["src"]
                        except:
                            try:
                                image_link = image['imgurl']
 
                        # if no Source URL found
                            except:
                                pass
 
            # After getting Image Source URL
            # We will try to get the content of image
            # print(image_link)
            image_links.append(image_link)

        print(image_links) 
        download_images_from_links(image_links, url) 

# MAIN FUNCTION START
def main(url):
   
    # content of URL
    r = requests.get(url)
 
    # Parse HTML Code
    soup = BeautifulSoup(r.text, 'html.parser')
 
    # find all images in URL
    images = soup.findAll('img')
     
    download_images(images, url)
 
def get_link_maps():
    return link_maps

# take url
#url = input("Enter URL:- ")
if __name__ == "__main__":
    for url in scrapper.getlinks():
        print("link images scann started:", url)

        main(url)
    
    
