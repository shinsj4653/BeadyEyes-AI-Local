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



def get_finger_coordinate(uri):
    base_options = python.BaseOptions(model_asset_path='hand_landmarker.task')
    options = vision.HandLandmarkerOptions(base_options=base_options,
                                            num_hands=2)
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
    try:
        right_hand_x_coordinate = int(detection_result.hand_landmarks[0][8].x * image_shape[1])
        right_hand_y_coordinate = int(detection_result.hand_landmarks[0][8].y * image_shape[0])


    except:
        # 손가락 인식 실패
        return -1, -1

    return right_hand_x_coordinate, right_hand_y_coordinate




def text_pointer(uri):
    # 이미지에서 텍스트를 추출

    x, y = get_finger_coordinate(uri)

    if x == -1 and y == -1:
        return ["손가락 인식에 실패했습니다."]

    text = googleOCR.text_pointer(uri, x, y)

    return text



