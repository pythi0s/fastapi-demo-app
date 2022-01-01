# Shopping Items Demo App

This is a demo app written in Fastapi. It has CRUD operations using which one can create, update and delete items.

## Install all dependencies:

```
cd src
poetry install
```

## Run application locally

```
cd src/app
uvicorn main:app --reload
```

## Docker

You can pull and run following docker image:

```
docker pull pythi0s/fastapi:shopitems
docker run -it --rm -p 8000:8000 pythi0s/fastapi:shopitems uvicorn --host 0.0.0.0 --reload main:app
```

OR if you want to build a docker image yourself, run following:

```
docker build --build-arg BASE=python:3.9-slim -t <docker repo> .
```