FROM python:3.11-slim
EXPOSE 8000
WORKDIR /api
COPY . /api
RUN apt update && \
    python -m pip install --upgrade pip && \
    python -m pip install --no-cache-dir -r requirements.txt
CMD ["uvicorn", "--factory", "app.main:create_app", "--host", "0.0.0.0", "--port", "8000"]