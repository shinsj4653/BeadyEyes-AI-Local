

Window 에서 실행방법

1. X-server를 설치해야함
   Window용 X-server중 Xming 설치 후 실행 (참고문서: https://continuetochallenge.tistory.com/43)

2. Docekr 실행 명령어 (몇분 기다려야함..) :
  docker run -e DISPLAY=host.docker.internal:0 money_test2
