import requests
import pyfiglet
from halo import Halo
from bs4 import BeautifulSoup
import urllib
# spinner = Halo(text='\nScanning\n', spinner='...')
def getlinks():
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
        #socialmedia=["instagram","facebook","twitter","linkedin","github"]
        linklist=[]
        print(G+"[+] Scan started......")
        print(G+"Checking the image :")
    #     print(G+"Scanning started in Instagram")
    #     print(G+"Scanning started in Github")
    #     print(G+"Scanning started in Facebook")
    #     print(G+"Scanning started in Twitter")
    #     print(G+"Scanning started in Linkedin")           
        if(req.status_code == 200): 
            print("status code 200")       
            soup = BeautifulSoup(req.content,'html.parser')
            #print(soup)
            c=0
            for g in soup.find_all('div', class_='g'):
                anchors = g.find_all('a')
                #print(anchors)
                #for x in anchors:
                #print("anchor :",c,'::')
                c+=1
                
                if 'href' in str(anchors[0]):
                    linklist.append(anchors[0]['href'])
    #             if 'imgurl' in str(anchors):
    #                 url=anchors[0]['imgurl']
    #                 #print(url)
    #                 urllib.request.urlretrieve(url, 'url')
    #                 #print(linklist)
        return linklist

        # c=0
        # for x in linklist:
            # print(x)
            # c+=1
#         c=0
#         for i in socialmedia:
#             sm=str(i)
#             #print(sm)
#             for j in linklist:
#                 if sm in str(j):
#                     c=c+1
#                     print(C+"[+]"+j)
        # if c == 0:
            # print(R+"No links associated with this image")
    # spinner.stop()
    except Exception as e:
        print(e)
