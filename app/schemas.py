from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, field_validator

MAX_TEXT_LENGTH = 5000


class PredictRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=MAX_TEXT_LENGTH)

    @field_validator("text")
    @classmethod
    def not_blank(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("text tidak boleh kosong atau hanya spasi.")
        return cleaned


class PredictResponse(BaseModel):
    text: str
    sentiment: Literal["positive", "negative"]
    confidence: float = Field(..., ge=0.0, le=1.0)
