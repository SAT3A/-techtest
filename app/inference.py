from __future__ import annotations

from threading import Lock
from typing import Literal

from transformers import pipeline

MODEL_NAME = "distilbert-base-uncased-finetuned-sst-2-english"

Label = Literal["positive", "negative"]

_LABEL_MAP: dict[str, Label] = {
    "POSITIVE": "positive",
    "NEGATIVE": "negative",
}


class ModelNotReadyError(RuntimeError):
    pass


class InferenceError(RuntimeError):
    pass


class SentimentService:
    def __init__(self, model_name: str = MODEL_NAME) -> None:
        self._model_name = model_name
        self._pipeline = None
        self._lock = Lock()

    @property
    def is_ready(self) -> bool:
        return self._pipeline is not None

    def load(self) -> None:
        with self._lock:
            if self._pipeline is not None:
                return
            self._pipeline = pipeline(
                task="sentiment-analysis",
                model=self._model_name,
                truncation=True,
                max_length=512,
            )

    def predict(self, text: str) -> tuple[Label, float]:
        if self._pipeline is None:
            raise ModelNotReadyError("Model belum dimuat.")

        try:
            result = self._pipeline(text)[0]
        except Exception as exc:
            raise InferenceError("Gagal menjalankan inference.") from exc

        label = _LABEL_MAP.get(str(result["label"]).upper())
        if label is None:
            raise InferenceError(f"Label tidak dikenal: {result['label']}")

        return label, round(float(result["score"]), 4)


service = SentimentService()
