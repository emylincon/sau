FROM python:3.8-alpine3.18

COPY . .

WORKDIR /sau

RUN pip install -r requirements.txt

EXPOSE 9191

ENTRYPOINT [ "python3", "src/sau/__main__.py" ]
