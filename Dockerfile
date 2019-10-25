FROM python:3

RUN mkdir /tmp

COPY requirements.txt /tmp

WORKDIR /tmp


ADD app.py /tmp

ADD createDataframes.py /tmp

ADD assets /tmp

ENV NAME DashMSI

RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 85


CMD [ "python", "./app.py" ]