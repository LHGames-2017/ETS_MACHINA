FROM polyhx/python-seed

RUN pip install requests

ADD . .

EXPOSE 3000

CMD ["python", "ai.py"]
