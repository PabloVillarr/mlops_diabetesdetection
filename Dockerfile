FROM python:3.13

WORKDIR /opt/app

COPY . .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

EXPOSE 5000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]