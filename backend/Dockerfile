FROM python:3.10.8

WORKDIR /code

COPY requirements.txt /code/requirements.txt

# inspect4py hard-pins an old setuptools version in its own metadata, which conflicts
# with the setuptools pin in requirements.txt. Install it separately with --no-deps
# so it doesn't get resolved together with the rest (see requirements.txt).
RUN pip install --no-cache-dir --no-deps "inspect4py==0.0.6"
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY api_config.yaml /config.yaml

COPY repograph /code/repograph

CMD ["python3", "-m", "repograph.api"]