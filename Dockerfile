FROM python:3.12
MAINTAINER PeStory@clarku.edu

# Directories for the source code and socket
RUN mkdir /uwsgi && mkdir -p /var/www/uwsgi

# Install OS dependencies
RUN apt-get update && apt-get install -y postgresql-client

# Next, install the Python modules
ADD uwsgi/requirements.txt /uwsgi/requirements.txt
RUN pip install -r /uwsgi/requirements.txt

WORKDIR /uwsgi
ENV PYTHONPATH=/uwsgi
ENTRYPOINT ["uwsgi", "--socket", "/var/www/uwsgi/uwsgi.sock", "--chmod-socket=666", "--workers", "4", "--logto", "/uwsgi/uwsgi.log", "--wsgi-file"]
CMD ["/uwsgi/hello_world.py"] 
