

### Window 에서 실행방법

1. X-server를 설치해야함
   Window용 X-server중 Xming 설치 후 실행 (참고문서: https://continuetochallenge.tistory.com/43)

2. Docekr 실행 명령어 (몇분 기다려야함..) :
  docker run -e DISPLAY=host.docker.internal:0 money_test2


![image](https://github.com/GDSC-Solution-Challenge-Team-4/BeadyEye-AI/assets/79080825/20d5abb5-eb4c-4a2e-b71b-f6e8b523f464)


### 해야할것
코드 중간에 보면 video_reference 라는 부분이 있다.
이곳에 video 경로 혹은 webcam의 device_id 혹은 RTSP이라는 stream url  등을 넣으라는 주석이 있는데...
아마 저부분에 카메라 정보를 받아 넣는게 아닐까 하는...
![image](https://github.com/GDSC-Solution-Challenge-Team-4/BeadyEye-AI/assets/79080825/b7f13a32-43e8-4d07-8119-f250a9e01f0d)
