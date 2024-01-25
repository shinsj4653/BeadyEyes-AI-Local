import io # 이미지를 불러오기 위한 라이브러리 import
import os # 환경변수를 사용하기 위한 라이브러리 import

# 구글 클라우드 플랫폼에서 받은 인증키를 환경변수에 등록 (Window 환경)

"""
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "gdsc-sc-team4-pointer-0d2a3b269fad.json"
"""

from PIL import Image, ImageDraw # 이미지를 불러오고, 편집하기 위한 라이브러리 import
import requests

def detect_text_uri(uri):
    from google.cloud import vision # 구글 클라우드 비전 API를 사용하기 위한 라이브러리 import


    # 클라이언트 초기화
    client = vision.ImageAnnotatorClient()


    # 이미지 파일 링크로 넣음
    image = vision.Image()
    image.source.image_uri = uri


    # 이미지 파일을 구글 비전 API에 넣어서 라벨을 추출
    response = client.label_detection(image=image)
    labels = response.label_annotations

    # 라벨 출력 (그냥 출력이므로 헷갈리지 않게 생략)
    """
    print('Labels:')
    for label in labels:
        print(label.description)
    """    

    # 이미지 파일을 구글 비전 API에 넣어서 텍스트를 추출
    response = client.text_detection(image=image)
    texts = response.text_annotations

    # # 이미지파일 불러오기 (바운딩 박스 그리기용)
    response = requests.get(uri, stream=True)
    response.raise_for_status()
    img = Image.open(response.raw)
    draw = ImageDraw.Draw(img)

    # 이미지 크기 출력
    """
    img_width, img_height = img.size
    print(f"Image Size: {img_width} x {img_height}")
    """

    print('Texts:')
    for text in texts:
        print(text.description) # 텍스트 출력
        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in text.bounding_poly.vertices])
        print('bounds: {}'.format(','.join(vertices))) # 바운딩 박스 좌표 출력

        
        # TODO: 이부분이 내가 그리는게 맞는지 확인 필요
        # 바운딩 박스 그리기 
        draw.polygon([
            (text.bounding_poly.vertices)[0].x, (text.bounding_poly.vertices)[0].y,
            (text.bounding_poly.vertices)[1].x, (text.bounding_poly.vertices)[1].y,
            (text.bounding_poly.vertices)[2].x, (text.bounding_poly.vertices)[2].y,
            (text.bounding_poly.vertices)[3].x, (text.bounding_poly.vertices)[3].y], 
            None, 
            outline='green',
            width=3)

    # 바운딩 박스가 그려진 이미지 저장 
    img.save('./images/image' + '_bounding_box.jpg') # TODO: 파일 경로 수정 필요

    # 바운딩 박스가 그려진 이미지 보여주기
    """
    img.show() 
    """


    # 총 문자 개수 출력
    print("Total Texts: ", len(texts))




def detect_text_dir(file_dir):
    from google.cloud import vision # 구글 클라우드 비전 API를 사용하기 위한 라이브러리 import


    # 클라이언트 초기화
    client = vision.ImageAnnotatorClient()


    # (이미지 파일을 직접 넣음)
    
    # 이미지 파일 경로 설정
    file_name = os.path.abspath(file_dir)

    # 이미지 파일을 읽어옴 

    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()
    # 이미지 파일을 구글 비전 API에 넣기 위한 객체 생성
    image = vision.Image(content=content)
    



    # 이미지 파일을 구글 비전 API에 넣어서 라벨을 추출
    response = client.label_detection(image=image)
    labels = response.label_annotations

    # 라벨 출력 (그냥 출력이므로 헷갈리지 않게 생략)
    """
    print('Labels:')
    for label in labels:
        print(label.description)
    """    

    # 이미지 파일을 구글 비전 API에 넣어서 텍스트를 추출
    response = client.text_detection(image=image)
    texts = response.text_annotations

    # 이미지파일 불러오기 (바운딩 박스 그리기용)
    img = Image.open(file_name)
    draw = ImageDraw.Draw(img)

    # 이미지 크기 출력
    """
    img_width, img_height = img.size
    print(f"Image Size: {img_width} x {img_height}")
    """

    print('Texts:')
    for text in texts:
        print(text.description) # 텍스트 출력
        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in text.bounding_poly.vertices])
        print('bounds: {}'.format(','.join(vertices))) # 바운딩 박스 좌표 출력

        
        # TODO: 이부분이 내가 그리는게 맞는지 확인 필요
        # 바운딩 박스 그리기 
        draw.polygon([
            (text.bounding_poly.vertices)[0].x, (text.bounding_poly.vertices)[0].y,
            (text.bounding_poly.vertices)[1].x, (text.bounding_poly.vertices)[1].y,
            (text.bounding_poly.vertices)[2].x, (text.bounding_poly.vertices)[2].y,
            (text.bounding_poly.vertices)[3].x, (text.bounding_poly.vertices)[3].y], 
            None, 
            outline='green',
            width=3)

    # 바운딩 박스가 그려진 이미지 저장 
    img.save('./images/image' + '_bounding_box.jpg') # TODO: 파일 경로 수정 필요

    # 바운딩 박스가 그려진 이미지 보여주기
    """
    img.show() 
    """


    # 총 문자 개수 출력
    print("Total Texts: ", len(texts))




image_uri = os.environ.get("IMAGE_URI", "https://cloud.google.com/static/vision/docs/images/sign_small.jpg")
# image_uri = "https://storage.ganpoom.com/ganpoom/jpg/4124294744043775.jpg"
detect_text_uri(image_uri)
# detect_text_dir("./images/cafe.jpg")