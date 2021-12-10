import time
from bs4 import *
import json
import requests
import os
from Scrapper import Scrapper

class Downloader:
    def __init__(self) -> None:
        self.scrapper = Scrapper()
        self.main_urls = self.scrapper.links_target
        self.img_links = self.scrapper.img_links
        self.link_imagePath_maps = dict()

    def download(self, dir_name):
        img_count = 0
        for link in self.img_links:
            if link.split(".")[-1] in ("jpg", "jpeg", "png","jfif"):
                try:
                    time.sleep(0.1)
                    r = requests.get(link)
                    image_path = os.path.join("Downloads", dir_name, str(img_count)+".jpg") 
                    img_count+=1
                    
                    with open(image_path, "wb") as outFile:
                        outFile.write(r.content)
                        outFile.close()
                    
                    self.link_imagePath_maps[link] = image_path
            

                except Exception as e:
                    print(e)




if __name__ == "__main__":
    downloader = Downloader()
    dir_name = input("Enter the dir name to store results  ==> ")
    os.mkdir("Downloads/"+dir_name)
    downloader.download(dir_name)
    # print(downloader.imageList)