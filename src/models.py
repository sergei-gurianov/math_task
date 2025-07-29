from typing import Optional

from pydantic import BaseModel


class Request(BaseModel):
    question: str = ""


class Topic(BaseModel):
    topic: str


class ParsedCylinder(BaseModel):
    height: Optional[float] = None
    radius: Optional[float] = None


class ParsedVectors(BaseModel):
    vec1: Optional[list[float]] = None
    vec2: Optional[list[float]] = None


class Response(BaseModel):
    answer: str = None
