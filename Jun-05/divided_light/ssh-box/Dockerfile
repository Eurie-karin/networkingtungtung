FROM alpine:3.19

RUN apk add --no-cache openssh curl bash netcat-openbsd

RUN adduser -D -s /usr/local/bin/notify-shell 4rch1v3 && \
    echo '4rch1v3:password' | chpasswd

RUN ssh-keygen -A

COPY notify-shell.sh /usr/local/bin/notify-shell
RUN chmod +x /usr/local/bin/notify-shell

COPY files/ /home/4rch1v3/
RUN chown -R 4rch1v3:4rch1v3 /home/4rch1v3/

RUN chmod -rwx /home/4rch1v3/classified

COPY sshd_config /etc/ssh/sshd_config

EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]
