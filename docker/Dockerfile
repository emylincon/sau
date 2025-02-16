FROM python:3.12-alpine3.21 as builder

WORKDIR /exporter

COPY requirements.txt .

RUN apk add --update --no-cache --virtual build-base gcc python3-dev musl-dev libffi-dev openssl-dev cargo &&\
    pip install --upgrade pip &&\
    pip install --no-cache-dir --target=/exporter/requirements -r requirements.txt

FROM python:3.12-alpine3.21

ARG VERSION="0.0.0"

ARG MAIN_FILE="src/sau/__main__.py"

WORKDIR /exporter

COPY --from=builder /exporter/requirements /usr/local/lib/python3.12/site-packages/

COPY . .

RUN current_date=$(date '+%Y-%m-%d %H:%M:%S') &&\
    sed -i -E "s/BUILD_DATE =.*/BUILD_DATE = \"${current_date}\"/" ${MAIN_FILE}  &&\
    sed -i -E "s/VERSION =.*/VERSION = \"${VERSION}\"/" ${MAIN_FILE} &&\
    addgroup -g 1000 exporter && \
    adduser -u 1000 -D -G exporter exporter -h /exporter &&\
    chown -R exporter:exporter /exporter

USER exporter

EXPOSE 9191

ENTRYPOINT [ "python3", "src/sau/__main__.py" ]

CMD ["-c", "configs/config.yaml"]
