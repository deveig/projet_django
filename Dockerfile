FROM python:3.14-rc-bookworm
ARG SECRET_KEY
ENV SECRET_KEY=$SECRET_KEY
WORKDIR /usr/local/app/
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN echo "SECRET_KEY=${SECRET_KEY}" > .env
RUN python3 manage.py migrate
RUN python3 manage.py makemigrations recipe
RUN python3 manage.py migrate 
CMD ["gunicorn", "django_project.wsgi", "--bind", "app"]