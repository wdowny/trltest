FROM alpine
RUN apk add --no-cache --update python3
RUN /usr/bin/pip3 install werkzeug
COPY app /app
HEALTHCHECK --interval=60s --timeout=2s --start-period=10s --retries=2 CMD /usr/bin/wget http://localhost:8080/ || exit 1
CMD /usr/bin/python3 /app/app.py
