# from vectorizer_deepface import Vectorizer
import time
from numpy.lib import emath
from datastore import Datastore
import os
from os import listdir
from os.path import isfile, join
from PIL import Image
import cv2
import numpy as np
from vectorizer_deepface import Vectorizer
from downloader import get_link_maps
import utils

if __name__ == "__main__":
    img_paths = []
    onlyfiles = [f for f in listdir("Downloads") if isfile(join("Downloads", f))]
    embs = []
    # print(onlyfiles)
    vec = Vectorizer()
    err_count = 0
    found = []
    store = Datastore()
    count = 0
    for val in onlyfiles:
        try :
            image = Image.open("Downloads/"+val)
    

            opencvImage = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    
            embedding = np.array(vec.vectorize_single(opencvImage), dtype=np.float32)
            embedding = embedding.reshape(1, 128)
            store.add(embedding, count, "")

            embs.append(embedding)
            found.append("Downloads/"+val)
            count+=1

        except Exception as e:
            # print(e)
            err_count+=1
            # print(err_count)
            continue
    embs = np.array(embs)
    # print(embs.shape)
    # print(embs)
    # print(embs[0])   
    # print(embs[0].shape)
    # print(found)
    query_image = Image.open("test_data/test.jpeg")

    opencv_query_Image = cv2.cvtColor(np.array(query_image), cv2.COLOR_RGB2BGR)

    query_image = np.array(vec.vectorize_single(opencv_query_Image), dtype = np.float32)
    query_image = query_image.reshape(1, 128)

    starttime = time.time()
    Distances, Identifiers = store.search(query_image)
    endtime = time.time()
    # print(f"time taken {endtime-starttime}")
    # print(Distances, Identifiers) 
    link_maps = utils.get_link_maps()
    # print(link_maps)
    for val in Identifiers[0]:
        if val != -1:
            print(found[val])
            print(link_maps[found[val]])