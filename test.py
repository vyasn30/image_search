from vectorizer import Vectorizer
from PIL import Image
import json

representaions_json = None

with open("vecdata/representations_final.json") as jsonFile:
    representaions_json = json.load(jsonFile)
    jsonFile.close()

mapping = dict()

for index in representaions_json:
    mapping[index] = list(representaions_json[index].keys())[0]

with open("mappings.json", "w") as outputFile:
    json.dump(mapping, outputFile)


