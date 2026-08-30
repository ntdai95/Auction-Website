from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
    user_id: Optional[int] = None
    username: Optional[str] = None
    password: Optional[str] = None
    email: Optional[str] = None
    user_type: Optional[str] = None
    user_status: Optional[str] = None
    user_rating_sum: Optional[int] = None
    user_rating_total: Optional[int] = None
    watchlist_parameter: Optional[str] = None
