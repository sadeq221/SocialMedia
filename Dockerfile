FROM python:3

WORKDIR /usr/src/app

# See the output
ENV PYTHONUNBUFFERED 1

# Python interpreter compiles source code to bytecode
# Don't write bytecode files (.pyc files)
# This will compile at every run (read the pos and neg of it)
ENV PYTHONDONTWRITEBYTECODE 1

COPY . /usr/src/app

RUN pip install -r requirements.txt
