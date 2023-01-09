from datetime import datetime
from typing import List, Optional

from sqlalchemy import Column, DateTime
from sqlmodel import Field, Relationship, SQLModel


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
    notes: List["Note"] = Relationship(back_populates="user")


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


class NoteBase(SQLModel):
    title: str = Field(max_length=32)
    detail: str = Field(max_length=256)
    is_public: bool = Field(default=False)


class NoteCreate(NoteBase):
    pass


class Note(NoteBase, table=True):
    __tablename__ = "notes"

    id: int = Field(primary_key=True, default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime,
            default=datetime.utcnow,
            onupdate=datetime.utcnow,
            nullable=False,
        )
    )
    is_archived: bool = Field(default=False)

    user_id: int = Field(foreign_key="users.id", nullable=False)

    user: "User" = Relationship(back_populates="notes")


class NoteUpdate(SQLModel):
    title: Optional[str] = Field(max_length=32)
    detail: Optional[str] = Field(max_length=256)
    is_public: Optional[bool]
    is_archived: Optional[bool]


class APIToken(SQLModel):
    access_token: str
    token_type: str


class PasswordChange(SQLModel):
    old_password: str
    new_password: str


UserRead.update_forward_refs()
