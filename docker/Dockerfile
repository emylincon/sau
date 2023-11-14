FROM python:3.8-alpine3.18

WORKDIR /sau

COPY . .

RUN pip install --upgrade pip &&\
    apk add --update --no-cache --virtual build-base gcc python3-dev musl-dev libffi-dev openssl-dev cargo &&\
    pip install -r requirements.txt

EXPOSE 9191

ENTRYPOINT [ "python3", "src/sau/__main__.py" ]
