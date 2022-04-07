from re import I
from PIL import Image
import cv2
import faiss
from datastore import Datastore
import utils
import numpy as np
from vectorizer_deepface import Vectorizer
from flask import Flask, request, jsonify
import uvicorn
from fastapi import FastAPI, File, UploadFile, Response
from starlette.responses import StreamingResponse
from fastapi.responses import FileResponse,HTMLResponse
import os
import io
from os import getcwd


store = Datastore()
vec = Vectorizer()
# representations, file_name_mappings = vec.vectorize_lfw("data/lfw-deepfunneled/lfw-deepfunneled")

# print(representations)
# print(file_name_mappings)    


mappings = utils.get_mappings()
representations = utils.get_representations()
file_name_maps = utils.get_file_name_mappings()
names, vectors = utils.get_vectors()

print(len(names))
print(len(vectors))


idx = 0
for name, vector in zip(names, vectors):
    name = np.array(name)
    vector = np.array(vector)
    # print(vector.shape)
    
    store.add(vector, idx, name)
    idx+=1

faiss.write_index(store.index, "vecdata/vector.index")




def search(query_img):
    
    # image = Image.open("test_data/muk.jpg")
    opencvImage = cv2.cvtColor(np.array(query_img), cv2.COLOR_RGB2BGR)

    emb_2 = vec.vectorize_single(opencvImage) 
    emb_2 = np.array(emb_2, dtype=np.float32)
    emb_2 = emb_2.reshape(1, 128)
    # print(emb_2.shape)
    



    D, I = store.search(emb_2)
    # print(D , I)
    ret = dict()
    rank=0
    file_names = []
    for id in I[0]:
        # print(id)
        # print(names[id])
        # print(file_name_maps[str(id)])
        rank+=1
        ret[str(rank)] = {str(rank) : {names[id]:file_name_maps[str(id)]}}
        file_names.append(file_name_maps[str(id)])
    return ret, file_names



app = FastAPI()
@app.post("/image/search")
async def search_api(file: UploadFile = File(...)):
    dir_name = "temp"
    if not os.path.isdir("Downloads/"+dir_name):
        os.mkdir("Downloads/"+dir_name)

    if len(os.listdir("Downloads/"+dir_name)) != 0:
        for f in os.listdir("Downloads/"+dir_name):
            os.remove(os.path.join("Downloads/"+dir_name, f))

    extension = file.filename.split(".")[-1] in ("jpg", "jpeg", "png","jfif")
    if not extension:
        return "Image must be of proper format!"

    vec = Vectorizer()
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))
    image.save("query_data/test.jpg")
    ret, files = search(image) 
    # downloader = Downloader("query_data/test.jpg")
    
    
    return ret

@app.get("/")
def get_file(name_file: str):
    print(getcwd()+"/"+name_file)
    return FileResponse(name_file)

if __name__ == "__main__":
    uvicorn.run(app, debug=True)

