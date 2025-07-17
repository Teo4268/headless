# Dockerfile

FROM python:3.10-slim
WORKDIR /app

COPY server.py ./
RUN pip install fastapi uvicorn

EXPOSE 10000
CMD ["python", "server.py"]
