from flask import Flask, request, jsonify
from PIL import Image
from vectorizer import Vectorizer
import uvicorn
from fastapi import FastAPI, File, UploadFile, Response
from starlette.responses import StreamingResponse
from fastapi.responses import FileResponse,HTMLResponse
import io

app = FastAPI()


@app.post("/vectorize/image")
async def vectorize_api(file: UploadFile = File(...)):
    
    extension = file.filename.split(".")[-1] in ("jpg", "jpeg", "png","jfif")
    if not extension:
        return "Image must be of proper format!"
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert('RGB')
    vec = Vectorizer(image)    
    embeddings = vec.vectorize()
    return embeddings


if __name__ == "__main__":
    uvicorn.run(app, debug=True)