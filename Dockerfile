
FROM python:3.9.5


WORKDIR /flaskProject123
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . .
RUN /bin/sh
COPY Pipfile .
COPY Pipfile.lock .
RUN pip install pipenv
RUN pipenv sync
ENTRYPOINT ["bash","docker-entrypoint.sh"]





