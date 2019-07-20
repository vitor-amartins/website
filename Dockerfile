FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /vitor
WORKDIR /vitor
COPY requirements.txt /vitor/
RUN pip install -r requirements.txt

COPY . /vitor/
RUN python manage.py migrate --noinput
RUN python manage.py collectstatic --noinput
CMD ["gunicorn", "website.wsgi"]