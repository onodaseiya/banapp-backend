from pydantic import BaseModel


class Achievement(BaseModel):
    user_id: int
    achievement_id: int
