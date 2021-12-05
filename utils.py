import json
import numpy as np
from numpy.lib.utils import source

with open("vecdata/representations_final.json") as outputFile:
        representaions = json.load(outputFile)
        outputFile.close()

with open("vecdata/mappings.json") as outputFile:
        mappings = json.load(outputFile)
        outputFile.close()

def get_representations():
        return representaions

def get_vectors():
        mappings = get_mappings()
        vectors = []
        names = []
        identifiers = list(mappings.keys())
        identifiers = np.array(identifiers, dtype=np.float32)

        print(identifiers) 

        for index in mappings:
                name, vector = yield_pairs(index)
                vector = np.array(vector, dtype=np.float32)
                vectors.append(vector)
                names.append(name)
        
        return names, vectors
 
def get_mappings():
        return mappings

def yield_pairs(index): 
    return mappings[str(index)], representaions[str(index)][mappings[str(index)]]


    

    
