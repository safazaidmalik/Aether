FROM python:3.8.7-slim


COPY requirements.txt /usr/src/app/
COPY aether_pipeline.py /usr/src/app/
WORKDIR /usr/src/app/

RUN pip install --no-cache-dir -r /usr/src/app/requirements.txt
RUN python -m spacy download en


EXPOSE 5000

CMD ["python", "/usr/src/app/aether_pipeline.py"]
