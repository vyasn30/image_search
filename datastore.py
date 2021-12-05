import numpy as np
import json
import faiss

# GPU = faiss.StandardGPUResources()
class Datastore:

    def __init__(self, vectors=None, identifiers=None, dimensions=512, gpu=False, inbuilt_index=False):
        self.__dimensions = dimensions
        self.__vectors = vectors
        self.__identifiers = identifiers
        self.index = faiss.IndexFlatIP(self.__dimensions)

    def __add()
