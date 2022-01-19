from pydantic import BaseModel


class User(BaseModel):
    user_id: int = None
    username: str = None
    password: str = None
    email: str = None
    user_type: str = None
    user_status: str = None
    user_rating_sum: int = None
    user_rating_total: int = None
    watchlist_parameter: str = None
