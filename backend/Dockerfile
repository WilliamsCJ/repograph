FROM python:3.9.12

WORKDIR /code

COPY requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY logging.yaml /code/logging.yaml

COPY api_config.yaml /code/config.yaml

COPY repograph /code/repograph

CMD ["uvicorn", "repograph.api:app", "--host", "0.0.0.0", "--port", "3000", "--reload"]

#CMD ["python3", "-m", "repograph.api", "config.yaml"]
