FROM alpine:3.19

RUN apk add --no-cache python3 docker-cli

COPY receiver.py /app/receiver.py

CMD ["python3", "/app/receiver.py"]
