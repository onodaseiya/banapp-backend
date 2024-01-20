from pydantic import BaseModel


class PetCreate(BaseModel):
    user_id: int
    name: str
    hunger: int = 0


class HungerUpdate(BaseModel):
    hunger: int
