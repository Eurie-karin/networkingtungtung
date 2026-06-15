FROM alpine:3.19

RUN apk add --no-cache openssh curl bash

RUN adduser -D -s /usr/local/bin/detection 4rch1v3 && \
    echo '4rch1v3:scythe' | chpasswd

RUN ssh-keygen -A

COPY detection.sh /usr/local/bin/detection
RUN chmod +x /usr/local/bin/detection

COPY sshd_config /etc/ssh/sshd_config

EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]
