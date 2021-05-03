# docker build -t google-api:latest .
# docker run -it --name api --rm  -v $(pwd):/usr/src/app  google-api:latest

FROM python:3

RUN mkdir -p /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /usr/src/app
COPY app /usr/src/app

#CMD [ "python", "./app/app.sh" ]
#ENTRYPOINT ["tail", "-f", "/dev/null"]
