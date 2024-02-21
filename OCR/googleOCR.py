import io # 이미지를 불러오기 위한 라이브러리 import
import os # 환경변수를 사용하기 위한 라이브러리 import
import math # 두 점간 거리 값 구하기 위한 라이브러리 import

# 구글 클라우드 플랫폼에서 받은 인증키를 환경변수에 등록 (Window 환경)


# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "ocrAccountKey.json"


from PIL import Image, ImageDraw # 이미지를 불러오고, 편집하기 위한 라이브러리 import
import requests

# /image/toText API에 사용될 image to text 함수
def image_to_text(uri) :
    from google.cloud import vision

    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    image.source.image_uri = uri

    response = client.text_detection(image=image)
    texts = response.text_annotations
    print("Texts:")

    text_string = []

    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )

    for i, text in enumerate(texts):
        print(f'\n"{text.description}"')
        #text_string.append(text.description.strip())

        # 개행 문자 및 공백 제거
        text_string += text.description.strip()

        # texts 배열 내 첫번째 원소가 사진의 전체 텍스트 이므로, for문 전체 순회 필요 X
        if i == 0 :
            break

    # 문자 배열
    print(text_string)

    # 개행 문자 및 공백 제거된 문자열로 변환
    result_string = get_cleaned_str(text_string)
    print(result_string)

    return result_string

def get_cleaned_str(text_string):
    # Remove ' ' and '\n' characters
    cleaned_array = [char.replace(' ', '').replace('\n', '') for char in text_string]

    # Concatenate the characters into a single string
    result_string = ''.join(cleaned_array)
    return result_string

def text_bounding_poly(uri):
    from google.cloud import vision  # 구글 클라우드 비전 API를 사용하기 위한 라이브러리 import

    # 최종 반환 데이터 + Poly 배열
    class FinalResponse() :
        pass

    # 텍스트 + 좌표 값 배열
    class PolyData():
        pass

    # 좌표 값 배열 내 객체 데이터
    class Vertex():
        pass

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
    img_width, img_height = img.size
    print(f"Image Size: {img_width} x {img_height}")

    print('Texts:')

    finalResponse = FinalResponse()

    # 이미지 가로, 세로 크기
    finalResponse.img_width = img_width
    finalResponse.img_height = img_height

    poly_arr = []


    for i, text in enumerate(texts):
        # 전체 텍스트는 제외, 텍스트 각각의 조각들만 필요하기 때문!
        if i == 0 :
            continue
        #print(text.description)  # 텍스트 출력
        polyData = PolyData()
        print(text.description)
        polyData.text = text.description

        # 좌표 정보 배열
        vertices_arr = []

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                     for vertex in text.bounding_poly.vertices])
        #print('bounds: {}'.format(','.join(vertices)))  # 바운딩 박스 좌표 출력

        for vertex in text.bounding_poly.vertices :
            v = Vertex()
            v.x = vertex.x
            v.y = vertex.y

            vertices_arr.append(v)

        polyData.vertices = vertices_arr
        poly_arr.append(polyData)

    finalResponse.boundingPoly = poly_arr

    print("finalResponse")
    print(finalResponse.img_width)
    print(finalResponse.img_height)

    #print(finalResponse.boundingPoly[0].vertices[0].x)
    # print(finalResponse.boundingPoly[0])
    return finalResponse

def text_pointer(uri, x, y):
    from google.cloud import vision  # 구글 클라우드 비전 API를 사용하기 위한 라이브러리 import


    # 클라이언트 초기화
    client = vision.ImageAnnotatorClient()

    # 이미지 파일 링크로 넣음
    image = vision.Image()
    image.source.image_uri = uri

    x = int(x)
    y = int(y)

    # 이미지 파일을 구글 비전 API에 넣어서 라벨을 추출
    response = client.label_detection(image=image)
    labels = response.label_annotations


    # 이미지 파일을 구글 비전 API에 넣어서 텍스트를 추출
    response = client.text_detection(image=image)
    texts = response.text_annotations

    # # 이미지파일 불러오기 (바운딩 박스 그리기용)
    response = requests.get(uri, stream=True)
    response.raise_for_status()
    img = Image.open(response.raw)
    draw = ImageDraw.Draw(img)

    # 이미지 크기 출력

    img_width, img_height = img.size
    print(f"Image Size: {img_width} x {img_height}")

    print('Texts:')

    # 손가락 x, y 좌표에 해당하는 단어 배열
    words = []

    for i, text in enumerate(texts):
        # 전체 텍스트는 제외, 텍스트 각각의 조각들만 필요하기 때문!
        if i == 0 :
            continue

        word = text.description
        print(word)

        x_set = set()
        y_set = set()

        for vertex in text.bounding_poly.vertices :
            x_set.add(vertex.x)
            y_set.add(vertex.y)


        min_x = min(x_set)
        max_x = max(x_set)

        min_y = min(y_set)
        max_y = max(y_set)

        mid_x = max_x - min_x
        mid_y = max_y - min_y

        if min_x <= x <= max_x and min_y <= y <= max_y :
            words.append((word, math.sqrt((abs(x - mid_x) ** 2) + (abs(y - mid_y) ** 2)))) # (단어, 단어의 가운데 좌표 값과 손 좌표 간 거리)

    print(words)
    words.sort(key=lambda x: x[1]) # 손과 가장 가까운 단어를 반환
    # 가장 긴 문자열 찾기
    if words:
        result_string = words[0]
    else:
        result_string = "해당위치에 문자열이 없습니다."
    #print(finalResponse.boundingPoly[0].vertices[0].x)
    # print(finalResponse.boundingPoly[0])
    return result_string

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
    img_width, img_height = img.size
    print(f"Image Size: {img_width} x {img_height}")

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


#image_uri = "https://storage.googleapis.com/gdcs-sc-beadyeyes-bucket/140d792f-7fe6-4ef9-b062-0583aa39c05e"
#image_uri = os.environ.get("IMAGE_URI", "https://cloud.google.com/static/vision/docs/images/sign_small.jpg")
# image_uri = "https://storage.ganpoom.com/ganpoom/jpg/4124294744043775.jpg"
#detect_text_uri(image_uri)
# detect_text_dir("./images/cafe.jpg")
