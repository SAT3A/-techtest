from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI, HTTPException

from app.inference import InferenceError, ModelNotReadyError, service
from app.schemas import PredictRequest, PredictResponse


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    service.load()
    yield


app = FastAPI(title="Sentiment Analysis API", lifespan=lifespan)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "healthy"}


@app.post("/predict", response_model=PredictResponse)
def predict(payload: PredictRequest) -> PredictResponse:
    try:
        label, confidence = service.predict(payload.text)
    except ModelNotReadyError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except InferenceError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return PredictResponse(
        text=payload.text,
        sentiment=label,
        confidence=confidence,
    )
