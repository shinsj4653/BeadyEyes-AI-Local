from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel


import googleOCR
import handLandmark

app = FastAPI()

class Image(BaseModel) :
	imageUrl: str

class Pointer(BaseModel) :
	# imagefile: UploadFile
	imageUrl: str
	# x : int
	# y : int

@app.get("/")
async def read_root() :
	return "This is root path from FastAPI Backend v3"

@app.post("/image/toText")
async def image_to_text(image: Image):
	return googleOCR.image_to_text(image.imageUrl)

@app.post("/image/boundingPoly")
async def image_to_text(image: Image):
	return googleOCR.text_bounding_poly(image.imageUrl)

# @app.post("/image/pointer")
# async def image_to_text(pointer: Pointer):
# 	return googleOCR.text_pointer(pointer.imageUrl, pointer.x, pointer.y)


# URL 로 이미지를 받아서 텍스트로 변환
@app.post("/image/pointer")
async def image_to_text(pointer: Pointer):
	return handLandmark.text_pointer_uri(pointer.imageUrl)


# 이미지 파일을 받아서 텍스트로 변환
# @app.post("/image/pointer")
# async def image_to_text(pointer: Pointer):
# 	return handLandmark.text_pointer_file(pointer.imagefile)

