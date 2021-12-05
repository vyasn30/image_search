import json

from numpy.lib.utils import source

with open("vecdata/representations_final.json") as outputFile:
        representaions = json.load(outputFile)
        outputFile.close()

with open("mappings.json") as outputFile:
        mappings = json.load(outputFile)
        outputFile.close()
 
def get_mappings():
        return mappings

def yield_pairs(index): 
    return mappings[str(index)], representaions[str(index)][mappings[str(index)]]

    

    
