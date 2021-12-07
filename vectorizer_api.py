from flask import Flask, request, jsonify
from PIL import Image
from vectorizer_deepface import Vectorizer
import uvicorn
from fastapi import FastAPI, File, UploadFile, Response
from starlette.responses import StreamingResponse
from fastapi.responses import FileResponse,HTMLResponse
import io
import cv2
import numpy as np

app = FastAPI()


@app.post("/vectorize/image")
async def vectorize_api(identifier: int, file: UploadFile = File(...)):
    ret = {}
    extension = file.filename.split(".")[-1] in ("jpg", "jpeg", "png","jfif")
    if not extension:
        return "Image must be of proper format!"
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))
    opencvImage = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    vec = Vectorizer()    
    embeddings = vec.vectorize_single(opencvImage)
    ret["id"] = identifier
    ret["embeddings"] = embeddings
        
    return ret 


if __name__ == "__main__":
    uvicorn.run(app, debug=True)