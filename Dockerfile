FROM ubuntu:latest
LABEL authors="nikol"

ENTRYPOINT ["top", "-b"]