FROM alpine:3.19
RUN apk add --no-cache netcat-openbsd
COPY send.sh /send.sh
RUN chmod +x /send.sh
CMD ["/send.sh"]
