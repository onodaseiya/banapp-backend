from pydantic import BaseModel

class BaitLog(BaseModel):
    user_id: int
    continueday: int
    totalcount: int