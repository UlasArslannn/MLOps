FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip \
    && pip install -r requirements.txt \
    && apt-get clean && rm -rf /var/lib/apt/lists/*


COPY . .


# Explicitly copy model (in case .dockerignore excluded mlruns)
# NOTE: destination changed to /app/src/serving/model to match inference.py's path
COPY src/serving/model /app/src/serving/model

# Copy MLflow run (artifacts + metadata) to the flat /app/model convenience path

COPY src/serving/model/974953631381130799/models/m-8806bc140ae444d59e6c2b6609b67b9a/artifacts  /app/model
COPY src/serving/model/974953631381130799/860e768b3baf41e5832ceb20e9b330ba/artifacts/feature_columns.txt /app/model/feature_columns.txt
COPY src/serving/model/974953631381130799/860e768b3baf41e5832ceb20e9b330ba/artifacts/preprocessing.pkl /app/model/preprocessing.pkl

# make "serving" and "app" importable without the "src." prefix
# ensures logs are shown in real-time (no buffering).
# lets you import modules using from app... instead of from src.app....
ENV PYTHONUNBUFFERED=1 \ 
    PYTHONPATH=/app/src


EXPOSE 8000

CMD ["python", "-m", "uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]

