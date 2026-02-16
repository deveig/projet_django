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
RUN echo "# Security" >> django_project/settings.py
RUN echo "CSRF_COOKIE_SECURE = True" >> django_project/settings.py
RUN echo "SESSION_COOKIE_SECURE = True" >> django_project/settings.py
RUN echo "SECURE_SSL_REDIRECT = True" >> django_project/settings.py
RUN echo "SECURE_HSTS_SECONDS = 3600" >> django_project/settings.py
RUN echo "SECURE_HSTS_INCLUDE_SUBDOMAINS = True" >> django_project/settings.py
RUN echo "SECURE_PROXY_SSL_HEADER = ('STRICT_TRANSPORT_SECURITY', 'max-age=31536000; includeSubDomains')" >> django_project/settings.py
RUN echo "#SECURE_HSTS_PRELOAD = True" >> django_project/settings.py
RUN openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/private/nginx.key -out /etc/ssl/certs/nginx.crt -subj "/CN=localhost"
CMD ["gunicorn", "django_project.wsgi", "--bind", "app", "--keyfile", "/etc/ssl/private/nginx.key", "--certfile", "/etc/ssl/certs/nginx.crt"]