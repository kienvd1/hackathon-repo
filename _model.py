from pydantic import BaseModel, Field
from typing import Literal

# Pydantic model for request validation
class ImageRequest(BaseModel):
    prompt: str = Field(..., example="A beautiful landscape with mountains and a lake")
    seed: int = Field(default=42, example=42)
    width: int = Field(default=16, ge=1, example=16)
    height: int = Field(default=9, ge=1, example=9)
    safety_tolerance: int = Field(default=2, ge=0, le=5, example=2)
    output_format: Literal["jpeg", "png"] = Field(default="jpeg", example="jpeg")
    raw: bool = Field(default=True, example=True)


class ResultRequest(BaseModel):
    id: str = Field(..., example="123e4567-e89b-12d3-a456-426614174000")


class FaceSwapRequest(BaseModel):
    target_image: str = Field(..., example="https://example.com/target.jpg")
    swap_image: str = Field(..., example="https://example.com/source.jpg")
