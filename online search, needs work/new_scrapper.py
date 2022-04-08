import requests
import pyfiglet
from halo import Halo
from bs4 import BeautifulSoup
import urllib
spinner = Halo(text='\nScanning\n', spinner='...')
R = '\033[31m' 
G = '\033[32m'
C = '\033[36m'
W = '\033[0m' 
image=input(C+"Enter the image path : ")
try:
    #spinner.start()
    headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
    }
    url='http://www.google.co.in/searchbyimage/upload'
    secondurl={'encoded_image': (image, open(image, 'rb')), 'image_content': ''}
    #print(secondurl)
    response = requests.post(url, files=secondurl,allow_redirects=False)
    fetch=response.headers['Location']
    
    print(fetch)
    req=requests.get(fetch,headers=headers)
    print(req)
    linklist=[]
    linklist2=[]
    print(G+"[+] Scan started......")
    print(G+"Checking the image :")         
    if(req.status_code == 200):        
        soup = BeautifulSoup(req.content,'html.parser')
        #print(soup)
        for x in soup.find_all('a', class_='ekf0x hSQtef'):
            x=x['href']
            final_url='http://www.google.co.in'+x
            print(final_url)
            req2=requests.get(final_url,headers=headers)
            print(req2)
            if(req2.status_code == 200):        
                soup2 = BeautifulSoup(req2.content,'html.parser')
                #print(soup2)
                for g2 in soup2.find_all('a',class_="VFACy kGQAp sMi44c lNHeqe WGvvNb"):
                    #print(g2['href'])
                    linklist2.append(g2['href'])
        print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')          
        c=0
        for g in soup.find_all('div',class_='g'):
            anchors = g.find_all('a')
            c+=1         
            if 'href' in str(anchors[0]):
                print(anchors[0]['href'])
                linklist.append(anchors[0]['href'])
        if c == 0:
            print(R+"No links associated with this image")
#     spinner.stop()
except Exception as e:
    print(e)
    
    
scrapper_getlinks=linklist+linklist2

print(len(linklist),len(linklist2),len(scrapper_getlinks))


from bs4 import *
import json
import requests
import os
#import scrapper
# import urllib.request
# CREATE FOLDER
image_count = 0
link_maps = dict()

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
                #print(image_count)
                #print(url)
                try :
                    r = requests.get(url)
                except Exception as e:
                    r =requests.get('http:'+url)
                image_path = os.path.join("Downloads", str(image_count)+".jpg") 
                with open(image_path, "wb") as outFile:
                    outFile.write(r.content)
                    outFile.close()
                
                link_maps[image_path] = single_url




                # urllib.request.urlretrieve(url, os.path.join("Downloads", str(image_count)+".jpg"))    
                image_count+=1

            except Exception as e:
                
                #print(e)
                continue
    with open("link_maps.json", "w") as outputFile:
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
 
            image_links.append(image_link)

        #print(image_links) 
        download_images_from_links(image_links, url) 

# MAIN FUNCTION START
def main(url):
   
    # content of URL
    r = requests.get(url,verify=False)
 
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
    countx=0
    for url in scrapper_getlinks:
        countx+=1
        print("images scann started in link "+str(countx)+" :", url)

        main(url)