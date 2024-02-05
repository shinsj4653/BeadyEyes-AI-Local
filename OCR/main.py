from fastapi import FastAPI
from pydantic import BaseModel

import googleOCR

app = FastAPI()

class Image(BaseModel) :
	imageUrl: str

@app.get("/")
async def read_root() :
	return "This is root path from FastAPI Backend v3"

@app.post("/image/toText")
async def image_to_text(image: Image):
	return googleOCR.image_to_text(image.imageUrl)

@app.post("/image/boundingPoly")
async def image_to_text(image: Image):
	return googleOCR.detect_text_uri(image.imageUrl)