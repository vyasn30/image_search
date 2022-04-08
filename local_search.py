from charset_normalizer import utils
from datastore import Datastore
from vectorizer_deepface import Vectorizer
from PIL import Image
import cv2
import numpy as np
from os import listdir
from os.path import isfile, join
import time
import tensorflow as tf
from vectorizer_deepface import Vectorizer
import utils
import faiss


class Searcher:
    def __init__(self, dir_path) -> None:
        self.dir_path = dir_path
        self.query_image = None
        self.data_store = Datastore()
        self.found = []
        self.results = []        
        self.query_image_path = None
        self.store = None
        self.vec = None
        self.mappings = None
        self.representations = None
        self.file_name_maps = None
        self.names = None
        self.vectors = None

    def input_query_image(self, img_file):
        self.query_image = img_file

    def search(self, query_img):
        opencvImage = cv2.cvtColor(np.array(query_img), cv2.COLOR_RGB2BGR)

        emb_2 = self.vec.vectorize_single(opencvImage)
        emb_2 = np.array(emb_2, dtype=np.float32)
        emb_2 = emb_2.reshape(1, 128)

        D, I = self.store.search(emb_2)
        ret = dict()
        rank=0
        file_names = []
        for id in I[0]:
            rank+=1
            ret[str(rank)] = {str(rank) : {self.names[id]:self.file_name_maps[str(id)]}}
            file_names.append(self.file_name_maps[str(id)])
        return ret, file_names


    def initialize_data_store(self):
        self.vec = Vectorizer()
        self.vec.vectorize_lfw("data/lfw-deepfunneled/lfw-deepfunneled")
        
        self.store = Datastore()
        self.mappings  = utils.get_mappings()
        self.representations = utils.get_representations()
        self.file_name_maps = utils.get_file_name_mappings()
        self.names, self.vectors = utils.get_vectors()
        
        idx = 0
        for name, vector in zip(self.names, self.vectors):
            name = np.array(name)
            vector = np.array(vector)
            # print(idx)
            # print(vector.shape)
            # print(name)
            
            self.store.add(vector, idx, name)
            idx+=1
        
        faiss.write_index(self.store.index, "vecdata/vector.index")
            
        # onlyfiles = [f for f in listdir(self.dir_path) if isfile(join(self.dir_path, f))]
        # self.found = []
        # err_count = 0
        # count = 0 
        # for val in onlyfiles:
        #     try :
        #         image = Image.open(self.dir_path+"/"+val)
    

        #         opencvImage = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    
        #         embedding = np.array(self.vec.vectorize_single(opencvImage), dtype=np.float32)
        #         embedding = embedding.reshape(1, 128)
        #         self.data_store.add(embedding, count, "")

        #         self.found.append(self.dir_path+"/"+val)
        #         count+=1

        #     except Exception as e:
        #         print(e)
        #         err_count+=1
        #         # print(err_count)
        #         continue
    
    # def search(self):
    #     # ret = dict()
    #     # print(type(self.query_image))
    #     # Distances, Identifiers = self.data_store.search(self.query_image)
    #     # endtime = time.time()
    #     # # print(f"time taken {endtime-starttime}")
    #     # # print(Distances, Identifiers) 
    #     # # print(link_maps)
        
    #     # for val, dis in zip(Identifiers[0], Distances[0]):
    #     #     if val != -1:
    #     #         self.results.append((self.found[val]))
    #     #         print(self.found[val], dis)
    #     #         ret[self.found[val]] = [str(dis)]
        
    #     # return ret 
    #     # for val in self.results:
    #         # metrics = DeepFace.verify(img1_path=self.query_image_path, img2_path=val)
    #         # print(metrics)
            

        
if __name__ == "__main__":
    # dir_path = input("\n\nEnter Directory Path ===> ")
    dir_path = "Downloads/mukes"
    searcher = Searcher(dir_path)
    # query_image_path = input("\n\nEnter query iamge path ===> ")
    query_image_path = "test_data/muk.jpg"
    searcher.input_query_image(query_image_path)
    searcher.initialize_data_store()
    searcher.search()

