FROM python:3.9

WORKDIR /playlify

COPY requirements.txt .
COPY /src /src

RUN pip3 install -r requirements.txt

CMD ["python3", "/src/app.py"]