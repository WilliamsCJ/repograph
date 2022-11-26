FROM python:3.9.12

WORKDIR /code

COPY requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY repograph /code/repograph

CMD ["uvicorn", "repograph.api.main:app", "--host", "0.0.0.0", "--port", "80"]
