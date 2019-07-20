FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /vitor
WORKDIR /vitor
COPY requirements.txt /vitor/
RUN pip install -r requirements.txt

COPY . /vitor/
CMD ["gunicorn", "website.wsgi"]