FROM alpine:3.5

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r /usr/src/app/requirements.txt
RUN python -m spacy download en

# Copy the current directory contents into the container at /app
COPY aether_pipeline.py /usr/src/app/
COPY templates/form.html /usr/src/app/templates/

# Make port 80 available to the world outside this container
EXPOSE 5000

# Run app.py when the container launches
CMD ["python", "/usr/src/app/aether_pipeline.py"]
