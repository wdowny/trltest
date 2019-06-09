FROM alpine
RUN apk add --no-cache --update python3
RUN /usr/bin/pip3 install werkzeug
COPY app /app
CMD /usr/bin/python3 /app/app.py