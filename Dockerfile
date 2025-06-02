FROM python:3.10
WORKDIR /IS_PROJEKT
COPY reqs.txt req.txt
RUN pip3 install -r req.txt
COPY . .
EXPOSE 8080
CMD ["python3", "main.py"]
