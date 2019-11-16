FROM python:3.7
RUN pip install fastapi uvicorn jinja2 python-multipart SQLAlchemy
COPY . /app
WORKDIR /app
EXPOSE 8080
RUN ls
CMD [ "python","main.py" ]