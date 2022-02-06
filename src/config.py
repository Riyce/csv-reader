from pathlib import Path

from pydantic import BaseSettings


BASE_DIR = Path(__file__).parent.resolve()


class Settings(BaseSettings):
	UPLOAD_FOLDER = BASE_DIR.joinpath("media/new")
	MEDIA_FOLDER = BASE_DIR.joinpath("media")


settings = Settings()
