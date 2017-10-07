FROM polyhx/python-seed

RUN pip install requests

ADD . .

EXPOSE 8080

CMD ["python", "ai.py"]
