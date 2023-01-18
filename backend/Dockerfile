FROM python:3.9.12

WORKDIR /code

COPY requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY logging.yaml /code/logging.yaml

COPY repograph /code/repograph

CMD ["python3", "-m", "repograph.api.main"]
