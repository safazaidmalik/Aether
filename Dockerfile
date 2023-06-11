FROM python:3.8.7-slim


COPY requirements.txt /app/
COPY aether_pipeline.py /app/
WORKDIR /app/

RUN pip install -r requirements.txt
RUN python -m spacy download en

EXPOSE 5000

CMD ["python", "aether_pipeline.py"]
