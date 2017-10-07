FROM polyhx/python-seed

RUN pip install requests

ADD . .

EXPOSE 3000
EXPOSE 8080

CMD ["python", "ai.py"]
