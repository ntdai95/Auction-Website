from pydantic import BaseModel


class Message(BaseModel):
    message_id: int = None
    sending_user_id: int = None
    message: str = None
