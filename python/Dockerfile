FROM python:3.8

RUN mkdir /app
COPY requirements.txt /app/requirements.txt
COPY gunicorn_settings.py /app/gunicorn_settings.py
COPY app.py /app/app.py
COPY config.py /app/config.py
COPY firebase-adminsdk.json /app/firebase-adminsdk.json

COPY models /app/models
COPY sentence_transformers /app/sentence_transformers
COPY data /app/data

ENV FIREBASE_CONFIG="./firebase-adminsdk.json"
ENV GOOGLE_APPLICATION_CREDENTIALS="./firebase-adminsdk.json"

RUN mkdir /app/training_bert_japanese

RUN pip install --upgrade pip
RUN pip install torch==1.9.0+cpu torchvision==0.10.0+cpu torchaudio==0.9.0 -f https://download.pytorch.org/whl/torch_stable.html
RUN pip install -r /app/requirements.txt

EXPOSE 9876

WORKDIR /app

ENTRYPOINT [ "gunicorn", "app:app" ]
CMD [ "-c", "/app/gunicorn_settings.py" ]

