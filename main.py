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
from local_search import Searcher



searcher = Searcher("data/lfw-deepfunneled/lfw-deepfunneled")
searcher.initialize_data_store()

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

    contents = await file.read()
    image = Image.open(io.BytesIO(contents))
    image.save("query_data/test.jpg")
    ret, files = searcher.search(image)
    # downloader = Downloader("query_data/test.jpg")


    return ret

if __name__ == "__main__":
    uvicorn.run(app, debug=True)