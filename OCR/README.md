## Text Recognition (OCR) (Official Code in Google-Cloud-API)

### Environment
- This application is designed to run in a Docker environment. Ensure that you have Docker installed on your system before proceeding with the setup.
- 이 어플리케이션은 Docker 환경에서 실행되도록 설계되었습니다. 설정을 진행하기 전에 시스템에 Docker가 설치되어 있는지 확인하세요.




### Reference
- <a href='https://cloud.google.com/vision/docs/ocr?hl=ko#vision_text_detection_gcs-python'>google-cloud-vision-OCR</a>



### How to do?

```
$ git clone https://github.com/GDSC-Solution-Challenge-Team-4/BeadyEye-AI.git && cd BeadyEye-AI/OCR
```
```
$ docker build -t your_image_name .
```
```
$ docker run -e IMAGE_URI="your_image_uri.jpg" your_image_name
```
```
# You need to have a Google Cloud Platform (GCP) key prepared.

$ docker run -e GOOGLE_APPLICATION_CREDENTIALS="KEY_PATH" -e IMAGE_URI="your_image_uri_here" your_image_name
```




### Output  (Update coming shortly)

- **Text Detection Results**

<img src=''></src>


- **bounding positions**

<img src=''></img>


