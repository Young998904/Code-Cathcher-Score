# 사용할 Python 베이스 이미지 지정
FROM python:3.9.6

# 컨테이너 내에서 코드가 실행될 디렉토리 설정
WORKDIR /app

# 현재 디렉토리의 requirements.txt 파일을 컨테이너의 /app 디렉토리로 복사
COPY requirements.txt ./

# requirements.txt에 명시된 필요한 패키지들 설치
RUN pip install --no-cache-dir -r requirements.txt

# 현재 디렉토리의 나머지 파일들을 컨테이너의 /app 디렉토리로 복사
COPY . .

# 컨테이너가 시작될 때 실행될 명령
CMD ["flask", "run", "--host=0.0.0.0"]
