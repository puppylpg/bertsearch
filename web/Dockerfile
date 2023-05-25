FROM python:3.8.6-slim-buster
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -U pip
RUN pip install -r requirements.txt
# download the model in advanced at build time
RUN python -c 'from sentence_transformers import SentenceTransformer; SentenceTransformer("sentence-transformers/paraphrase-multilingual-mpnet-base-v2")'
COPY . /app
ENTRYPOINT ["python"]
CMD ["app.py"]
