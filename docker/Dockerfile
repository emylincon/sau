FROM python:3.8-alpine3.18

ARG VERSION="0.0.0"

ARG MAIN_FILE="src/sau/__main__.py"

WORKDIR /exporter

COPY . .

RUN current_date=$(date '+%Y-%m-%d %H:%M:%S') &&\
    sed -i -E "s/BUILD_DATE =.*/BUILD_DATE = \"${current_date}\"/" ${MAIN_FILE}  &&\
    sed -i -E "s/VERSION =.*/VERSION = \"${VERSION}\"/" ${MAIN_FILE} &&\
    pip install --upgrade pip &&\
    apk add --update --no-cache --virtual build-base gcc python3-dev musl-dev libffi-dev openssl-dev cargo &&\
    addgroup -g 1000 exporter && \
    adduser -u 1000 -D -G exporter exporter -h /exporter &&\
    chown -R exporter:exporter /exporter && \
    pip install -r requirements.txt

USER exporter

EXPOSE 9191

ENTRYPOINT [ "python3", "src/sau/__main__.py" ]

CMD ["-c", "configs/config.yaml"]
