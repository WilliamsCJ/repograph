FROM python:3.9.12

WORKDIR /code

COPY requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY logging.yaml /code/logging.yaml

COPY repograph /code/repograph

#CMD ["repograph.api.main", "--host", "0.0.0.0", "--port", "3000", "--log-config", "/code/logging.yaml"]

CMD ["python3", "-m", "repograph.api.main"]
