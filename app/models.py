from datetime import datetime as dt
from typing import List, Optional

from sqlalchemy import Column, DateTime
from sqlmodel import Field, Relationship, SQLModel, DateTime, Text


class UserRoleLink(SQLModel, table=True):
    __tablename__ = "users_roles"

    user_id: int = Field(primary_key=True, foreign_key="users.id")
    role_id: int = Field(primary_key=True, foreign_key="roles.id")


class UserBase(SQLModel):
    username: str = Field(max_length=32, unique=True, index=True)
    fullname: str = Field(max_length=64)
    age: Optional[int]


class User(UserBase, table=True):
    __tablename__ = "users"

    id: int = Field(primary_key=True, default=None)
    password: str = Field(max_length=256, nullable=True)
    image_path: str = Field(max_length=256, nullable=True)
    is_active: bool = Field(default=True)

    roles: List["Role"] = Relationship(
        back_populates="users", link_model=UserRoleLink
    )
    
    raffles: List["Raffle"] = Relationship(back_populates="user")


class UserRead(UserBase):
    id: int
    image_path: Optional[str]
    is_active: bool
    roles: List["Role"]


class UserCreate(UserBase):
    password: str = Field(max_length=256, nullable=True)
    role_ids: List[int] = []


class UserUpdate(SQLModel):
    username: Optional[str] = Field(max_length=32)
    fullname: Optional[str] = Field(max_length=64)
    age: Optional[int]
    image_path: Optional[str]
    is_active: Optional[bool]
    role_ids: Optional[List[int]]


class RoleBase(SQLModel):
    name: str = Field(max_length=32, unique=True, index=True)


class Role(RoleBase, table=True):
    __tablename__ = "roles"

    id: int = Field(primary_key=True, default=None)
    is_active: bool = Field(default=True)

    users: List["User"] = Relationship(
        back_populates="roles", link_model=UserRoleLink
    )


class RoleCreate(RoleBase):
    pass


class RoleUpdate(SQLModel):
    name: Optional[str] = Field(max_length=32)
    is_active: Optional[bool]


class APIToken(SQLModel):
    access_token: str
    token_type: str


class PasswordChange(SQLModel):
    old_password: str
    new_password: str


class RewardUserLink(SQLModel, table=True):
    __tablename__ = "winned_rewards"

    id: int = Field(primary_key=True, nullable=False, default=None)
    #raffle_id: int = Field(primary_key=True, foreign_key="raffles.id")
    reward_id: int = Field(primary_key=True, foreign_key="raffles_rewards.id")
    user_id: int = Field(primary_key=True, foreign_key="users.id")


class RaffleRewards(SQLModel, table=True):
    __tablename__ = "raffles_rewards"

    raffle_id: int = Field(primary_key=True, foreign_key="raffles.id")
    id: int = Field(primary_key=True, default=None, nullable=False)
    name: str = Field(max_length=32, unique=True, index=True)
    
    raffles: List["Raffle"] = Relationship(back_populates="rewards")

class RaffleUserLink(SQLModel, table=True):
    __tablename__ = "raffles_numbers"

    id: int = Field(default=None, primary_key=True, nullable=False)
    price: int = Field(default=0)
    buyed_number: int = Field(default=0)
    
    raffle_id: int = Field(primary_key=True, foreign_key="raffles.id")
    user_id: int = Field(primary_key=True, foreign_key="users.id")


class RaffleBase(SQLModel):
    title: str = Field(max_length=64, unique=True, index=True)
    details: str = Field(max_length=256)
    numbers: int = Field(default=0)


class Raffle(RaffleBase, table=True):
    __tablename__ = "raffles"

    id: int = Field(default=None, primary_key=True, nullable=False)
    state: bool = Field(default=True)

    rewards: List["RaffleRewards"] = Relationship(back_populates="raffles")
    user: List["User"] = Relationship(back_populates="raffles")
   
    created_by: int = Field(foreign_key="users.id")
    #creator: "User" = Relationship(back_populates="raffles_created")


class RaffleCreate(RaffleBase):
    rewards: List[str] = []


class UserRaffles(RaffleBase):
    pass

#class RaffleRead(RaffleBase):
#    id: int


UserRead.update_forward_refs()
