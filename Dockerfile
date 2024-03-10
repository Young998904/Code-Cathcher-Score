# Python 베이스 이미지를 지정합니다.
FROM python:3.9.6

# /app 디렉토리를 작업 디렉토리로 설정합니다.
WORKDIR /app

# 현재 디렉토리의 파일들을 Docker 컨테이너의 /app 디렉토리로 복사합니다.
COPY . /app

# requirements.txt를 사용하여 필요한 Python 패키지들을 설치합니다.
RUN pip install --no-cache-dir -r requirements.txt

# Java 17 설치
RUN apt-get update && \
    apt-get install -y openjdk-17-jdk && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 환경변수 설정
ENV JAVA_HOME /usr/lib/jvm/java-17-openjdk-amd64

# 컨테이너가 시작될 때 실행될 명령어를 지정합니다. Gunicorn을 사용하여 Flask 앱을 실행합니다.
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:app"]