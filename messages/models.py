from typing import Optional
from pydantic import BaseModel


class Message(BaseModel):
    message_id: Optional[int] = None
    sending_user_id: Optional[int] = None
    message: Optional[str] = None
