from typing import List, Optional

from fastapi import APIRouter, Depends, UploadFile
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlmodel import Session

from app.crud import (
    insert_role,
    insert_note,
    insert_user,
    select_role_by_id,
    select_roles,
    select_note_by_id,
    select_notes,
    select_public_notes,
    select_user_by_id,
    select_user_notes,
    select_users,
    update_note,
    update_password,
    update_user,
)
from app.database import get_session
from app.models import (
    APIToken,
    Role,
    RoleCreate,
    Note,
    NoteCreate,
    NoteUpdate,
    PasswordChange,
    User,
    UserCreate,
    UserRead,
    UserUpdate,
)
from app.security import (
    RoleChecker,
    authenticate_user,
    create_jwt,
    get_current_active_user,
)
from app.utilities import save_user_image

router = APIRouter()

allow_manage_users = RoleChecker(allowed_roles=["user_manager"])
allow_create_raffles = RoleChecker(allowed_roles=["raffle_creator"])
allow_buy_raffles = RoleChecker(allowed_roles=["raffle_buyer"])

@router.get(
    "/users/", response_model=List[UserRead], dependencies=[Depends(allow_manage_users)]
)
async def get_users(
    session: Session = Depends(get_session),
):
    return select_users(session)


@router.post(
    "/users/", response_model=UserRead, #dependencies=[Depends(allow_manage_users)]
)
async def create_user(
    user_data: UserCreate,
    session: Session = Depends(get_session),
):
    try:
        return insert_user(user_data, session)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Username already exists")


@router.get("/users/me", response_model=UserRead)
async def get_user_me(
    user: User = Depends(get_current_active_user),
):
    return user


@router.post("/users/me/change-password/", response_model=UserRead)
async def change_password_me(
    password_change_data: PasswordChange,
    user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session),
):
    user = update_password(user.id, password_change_data, session)
    return user


@router.get(
    "/users/{user_id}",
    response_model=UserRead,
    dependencies=[Depends(allow_manage_users)],
)
async def get_user(user_id: int, session: Session = Depends(get_session)):
    try:
        return select_user_by_id(user_id, session)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="User not found")


@router.patch(
    "/users/{user_id}",
    response_model=UserRead,
    dependencies=[Depends(allow_manage_users)],
)
async def edit_user(
    user_id: int, user_data: UserUpdate, session: Session = Depends(get_session)
):
    try:
        return update_user(user_id, user_data, session)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="User not found")


@router.post(
    "/users/{user_id}/image",
    response_model=UserRead,
    dependencies=[Depends(allow_manage_users)],
)
async def set_user_image(
    user_id: int, file: UploadFile, session: Session = Depends(get_session)
):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File is not an image")
    image_path = save_user_image(user_id, file)

    return update_user(user_id, UserUpdate(image_path=f"/{image_path}"), session)


@router.get("/roles/", response_model=List[Role])
async def get_roles(session: Session = Depends(get_session)):
    return select_roles(session)


@router.get("/roles/{role_id}", response_model=Role)
async def get_role(role_id: int, session: Session = Depends(get_session)):
    try:
        return select_role_by_id(role_id, session)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Role not found")


@router.post(
    "/roles/", response_model=Role, #dependencies=[Depends(allow_manage_users)]
)
async def create_role(
    role_data: RoleCreate, session: Session = Depends(get_session)
):
    try:
        return insert_role(role_data, session)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Role already exists")


@router.post("/token", response_model=APIToken)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    user = authenticate_user(form_data.username, form_data.password, session)
    token = create_jwt({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/notes/", response_model=Note)
async def create_note(
    note_data: NoteCreate,
    user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session),
):
    return insert_note(note_data, user, session)


@router.patch("/notes/{note_id}", response_model=Note)
async def edit_note(
    note_id: int,
    note_data: NoteUpdate,
    user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session),
):
    note_db = select_note_by_id(note_id, session)
    if note_db.user != user:
        allow_create_raffles(user)
    return update_note(note_id, note_data, session)


@router.get(
    "/notes/", response_model=List[Note], dependencies=[Depends(allow_create_raffles)]
)
async def get_notes(
    session: Session = Depends(get_session),
):
    return select_notes(session)


@router.get("/notes/public", response_model=List[Note])
async def get_public_notes(
    session: Session = Depends(get_session),
):
    return select_public_notes(session)


@router.get("/me/notes/", response_model=List[Note])
async def get_notes_me(
    user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session),
    archived: Optional[bool] = None,
):
    return select_user_notes(user.id, session, archived)


@router.get(
    "/{user_id}/notes",
    response_model=List[Note],
    dependencies=[Depends(allow_create_raffles)],
)
async def get_user_notes(
    user_id: int,
    session: Session = Depends(get_session),
    archived: Optional[bool] = None,
):
    return select_user_notes(user_id, session, archived)


@router.get("/notes/{note_id}", response_model=Note)
async def get_note(
    note_id: int,
    user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session),
):
    note = select_note_by_id(note_id, session)
    if not note.is_public and note.user != user:
        allow_create_raffles(user)
    return note
