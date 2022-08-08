from pydantic import BaseModel


class Dictionary(BaseModel):
    id: int
    uzbek: str
    russian: str
    english: str
