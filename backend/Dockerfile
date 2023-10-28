FROM python:3.9

RUN apt-get update && \
    apt-get install -y locales && \
    sed -i -e 's/# es_CL.UTF-8 UTF-8/es_CL.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales

ENV LANG es_CL.UTF-8
ENV LC_ALL es_CL.UTF-8

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
