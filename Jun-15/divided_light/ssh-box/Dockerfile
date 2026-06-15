FROM alpine:3.19

RUN apk add --no-cache openssh-server openssh curl bash netcat-openbsd

RUN adduser -D -s /bin/sh outpost-04 && \
	echo "outpost-04:cyclops" | chpasswd

RUN adduser -D -s /usr/local/bin/notify-shell 4rch1v3 && \
    echo '4rch1v3:scythe' | chpasswd

RUN ssh-keygen -A

COPY notify-shell.sh /usr/local/bin/notify-shell
RUN chmod +x /usr/local/bin/notify-shell


COPY files/outpost-04/ /home/outpost-04
COPY files/4rch1v3/ /home/4rch1v3/

RUN chown -R outpost-04:outpost-04 /home/outpost-04
RUN chown -R 4rch1v3:4rch1v3 /home/4rch1v3/

RUN chmod -rwx /home/4rch1v3/classified

COPY sshd_config /etc/ssh/sshd_config

RUN mkdir -p /run/sshd

EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]
