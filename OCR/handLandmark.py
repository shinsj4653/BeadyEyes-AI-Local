from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

import numpy as np
# import cv2
import urllib.request

import googleOCR
from PIL import Image
import requests
from io import BytesIO

from PIL import Image, ImageDraw # 이미지를 불러오고, 편집하기 위한 라이브러리 import


# def read_image_from_uri(uri):
#     try:
#         # URI로부터 이미지 다운로드
#         req = urllib.request.urlopen(uri)
#         arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
#         img = cv2.imdecode(arr, cv2.IMREAD_COLOR)

#         local_path = "temp.jpg"
#         # 로컬에 이미지 저장
#         cv2.imwrite(local_path, img)

#         return img


#     except Exception as e:
#         print(f"Error reading image from {uri}: {e}")
#         return None




def read_image_from_uri(uri):
    try:
        # URI로부터 이미지 다운로드
        response = requests.get(uri)
        img = Image.open(BytesIO(response.content))

        local_path = "temp.jpg"
        # 로컬에 이미지 저장
        img.save(local_path)

        return np.array(img)
    except Exception as e:
        print(f"Error reading image from {uri}: {e}")
        return None

def printImageInfo(uri) :

    from google.cloud import vision
    # 클라이언트 초기화
    client = vision.ImageAnnotatorClient()

    # 이미지 파일 링크로 넣음
    image = vision.Image()
    image.source.image_uri = uri

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

def get_finger_coordinate(uri):
    base_options = python.BaseOptions(model_asset_path='hand_landmarker.task')
    options = vision.HandLandmarkerOptions(base_options=base_options,
                                            num_hands=1)
    detector = vision.HandLandmarker.create_from_options(options)

    # STEP 3: Load the input image.
    
    local_path = "temp.jpg"
    read_image_from_uri(uri)
    image = mp.Image.create_from_file(local_path)


    # uri로부터 이미지를 읽어옴
    # image = read_image_from_uri(uri)
    # image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image)

    image_shape = image.numpy_view().shape

    # STEP 4: Detect hand landmarks from the input image.
    detection_result = detector.detect(image)

    right_hand_x_coordinate = 0
    right_hand_y_coordinate = 0



    # cv2.imshow("Annotated Image", image.numpy_view())
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # print(image_shape)
    # print(detection_result.hand_landmarks[0][8])
    printImageInfo(uri)
    print('image_shape[1] : ', image_shape[1])
    print('image_shape[0] : ', image_shape[0])

    try:

        #handXset = set()
        handYset = set()

        for i, value in detection_result.hand_landmarks[0]:
            print("index : ", i)
            print("hand x : ", value.x * image_shape[1])
            print("hand y : ", value.y * image_shape[0])

            #handXset.add(value.x)
            handYset.add(value.y)

        #min_x = max(handXset)
        min_y = max(handYset)

        right_hand_x_coordinate = int(detection_result.hand_landmarks[0][8].x * image_shape[1])
        right_hand_y_coordinate = int(min_y * image_shape[0])

        #right_hand_x_coordinate = int(detection_result.hand_landmarks[0][8].x * image_shape[1])
        #right_hand_y_coordinate = int(detection_result.hand_landmarks[0][8].y * image_shape[0])
        #print('detection_result.hand_landmarks')
        #print(detection_result.hand_landmarks)

        print("selected hand x 좌표 : ", right_hand_x_coordinate)
        print("selected hand y 좌표 : ", right_hand_y_coordinate)

    except:
        # 손가락 인식 실패
        return -1, -1

    return right_hand_x_coordinate, right_hand_y_coordinate


def text_pointer_uri(uri):
    # 이미지에서 텍스트를 추출

    x, y = get_finger_coordinate(uri)

    if x == -1 and y == -1:
        return "손가락 인식에 실패했습니다."

    text = googleOCR.text_pointer(uri, x, y)

    return text



###################################################################################################################
# here the code for file upload



def get_finger_coordinate_file(imagefile):
    base_options = python.BaseOptions(model_asset_path='hand_landmarker.task')
    options = vision.HandLandmarkerOptions(base_options=base_options,
                                            num_hands=1)
    detector = vision.HandLandmarker.create_from_options(options)

    # STEP 3: Load the input image.

    image = mp.Image.create_from_file(imagefile)


    # uri로부터 이미지를 읽어옴
    # image = read_image_from_uri(uri)
    # image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image)

    image_shape = image.numpy_view().shape

    # STEP 4: Detect hand landmarks from the input image.
    detection_result = detector.detect(image)

    right_hand_x_coordinate = 0
    right_hand_y_coordinate = 0


    # import cv2
    # cv2.imshow("Annotated Image", image.numpy_view())
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # print(image_shape)
    # print(detection_result.hand_landmarks[0][8])
    try:

        right_hand_x_coordinate = int(detection_result.hand_landmarks[0][8].x * image_shape[1])
        right_hand_y_coordinate = int(detection_result.hand_landmarks[0][8].y * image_shape[0])


    except:
        # 손가락 인식 실패
        return -1, -1

    return right_hand_x_coordinate, right_hand_y_coordinate


def text_pointer_file(imagefile):
    # 이미지에서 텍스트를 추출
    x, y = get_finger_coordinate_file(imagefile)

    if x == -1 and y == -1:
        return "손가락 인식에 실패했습니다."

    text = googleOCR.detect_text_dir(imagefile, x, y)

    return text




# aa = text_pointer_file("/home/gardenjun/바탕화면/STUDY/gdsc_pointer/OCR/images/finger.jpg")

# print(aa)