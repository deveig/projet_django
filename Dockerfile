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
RUN openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/private/nginx.key -out /etc/ssl/certs/nginx.crt -subj "/CN=localhost"
CMD ["gunicorn", "django_project.wsgi", "--bind", "app", "--keyfile", "/etc/ssl/private/nginx.key", "--certfile", "/etc/ssl/certs/nginx.crt"]