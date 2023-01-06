from pathlib import Path

from fastapi import UploadFile

from app.config import settings


def save_user_image(user_id: int, image: UploadFile) -> str:
    storage_path = Path(settings.storage_dir) / "user_images" / str(user_id)
    storage_path.mkdir(parents=True, exist_ok=True)

    with open(storage_path / image.filename, "wb") as f:
        f.write(image.file.read())

    return str(storage_path / image.filename)
