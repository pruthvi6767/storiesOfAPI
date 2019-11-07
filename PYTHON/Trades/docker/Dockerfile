FROM alpine:3.9
RUN apk update \
    && apk add htop
ENTRYPOINT ["/usr/bin/htop"]
#default entrypoint arg
CMD [""]
LABEL "HTOP"="0.1.0"