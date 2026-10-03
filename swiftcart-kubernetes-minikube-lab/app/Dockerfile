# syntax=docker/dockerfile:1
FROM python:3.12-slim
LABEL org.opencontainers.image.title="SwiftCart Logistics Kubernetes API" \
      org.opencontainers.image.version="3.0.0" \
      org.opencontainers.image.description="Kubernetes/Minikube training application"
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
RUN useradd --create-home --shell /usr/sbin/nologin appuser
USER appuser
EXPOSE 5000
HEALTHCHECK --interval=15s --timeout=5s --start-period=20s --retries=5 CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:5000/health', timeout=3).read()"
CMD ["gunicorn","--bind","0.0.0.0:5000","--workers","2","app:app"]
