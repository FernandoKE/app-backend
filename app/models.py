from sqlmodel import SQLModel


class APIToken(SQLModel):
    access_token: str
    token_type: str