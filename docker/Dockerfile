FROM python:3.8-alpine3.18

WORKDIR /exporter

COPY . .
# apk add --update --no-cache --virtual build-base gcc python3-dev musl-dev libffi-dev openssl-dev cargo &&\
RUN pip install --upgrade pip &&\
    apk add --update --no-cache --virtual build-base gcc python3-dev musl-dev libffi-dev openssl-dev &&\
    addgroup -g 1000 exporter && \
    adduser -u 1000 -D -G exporter exporter -h /exporter &&\
    chown -R exporter:exporter /exporter && \
    pip install -r requirements.txt

EXPOSE 9191

USER exporter

ENTRYPOINT [ "python3", "src/sau/__main__.py" ]

CMD ["-c", "configs/config.yaml"]
