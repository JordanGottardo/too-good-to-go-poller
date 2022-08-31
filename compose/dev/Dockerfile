FROM python:3.10.6
WORKDIR /code
COPY requirements/dev.txt /code/requirements.txt

RUN python3 -m ensurepip
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]