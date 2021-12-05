import numpy as np
import json
import faiss

# GPU = faiss.StandardGPUResources()
class Datastore:

    def __init__(self, vectors=None, identifiers=None, dimensions=512, gpu=False, inbuilt_index=False):
        self.__dimensions = dimensions
        self.__vectors = None
        self.__identifiers = None

        self.representations = dict()
        self.__mappings = dict()
        self.index = faiss.IndexFlatIP(self.__dimensions)


    def add(self,vector, identifier, name):
        self.representations[str(identifier)] = vector
        self.__mappings[str(identifier)] = name

        to_add = []
        to_add.append(vector)
        to_add = np.array(to_add)
        to_add = to_add.reshape(1, self.__dimensions)
        # print(to_add)
        print(f"To add shape is {to_add.shape}")

        # print(to_add)
        self.index.add(to_add)
        
    
    def search(self, emb):
        D, I = self.index.search(emb, 5)
        # return [self.__mappings[str(val)] for val in I[0]]
        print(I)

    

        
