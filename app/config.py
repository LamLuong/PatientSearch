import secrets
from typing import Any

from pydantic import (
  AnyHttpUrl,
  HttpUrl,
  PostgresDsn,
  ValidationInfo,
  computed_field,
  field_validator,
)
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
  API_V1_STR: str = "/api/v1"
  SECRET_KEY: str = secrets.token_urlsafe(32)
  # 60 minutes * 24 hours * 8 days = 8 days
  ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
#   SERVER_HOST: AnyHttpUrl
  # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
  # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
  # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
  BACKEND_CORS_ORIGINS: list[AnyHttpUrl] | str = []

  @field_validator("BACKEND_CORS_ORIGINS", mode="before")
  @classmethod
  def assemble_cors_origins(cls, v: str | list[str]) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
      return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
      return v
    raise ValueError(v)

  PROJECT_NAME: str = "PatientSearch"
  SENTRY_DSN: HttpUrl | None = None

  @field_validator("SENTRY_DSN", mode="before")
  @classmethod
  def sentry_dsn_can_be_blank(cls, v: str) -> str | None:
    if not v:
      return None
    return v

  POSTGRES_SERVER: str = "localhost"
  POSTGRES_USER: str = "admin"
  POSTGRES_PASSWORD: str = "123qwe"
  POSTGRES_DB: str = "patient_mr"
  POSTGRES_PORT: int = 5432
  @computed_field  # type: ignore[misc]
  @property
  def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
    return MultiHostUrl.build(
      scheme="postgresql+psycopg",
      username=self.POSTGRES_USER,
      password=self.POSTGRES_PASSWORD,
      host=self.POSTGRES_SERVER,
      port=self.POSTGRES_PORT,
      path=self.POSTGRES_DB,
    )

  SMTP_TLS: bool = True
  SMTP_PORT: int | None = None
  SMTP_HOST: str | None = None
  SMTP_USER: str | None = None
  SMTP_PASSWORD: str | None = None
  # TODO: update type to EmailStr when sqlmodel supports it
  EMAILS_FROM_EMAIL: str | None = None
  EMAILS_FROM_NAME: str | None = None

#   @field_validator("EMAILS_FROM_NAME")
#   def get_project_name(cls, v: str | None, info: ValidationInfo) -> str:
#     if not v:
#       return info.data["PROJECT_NAME"]
#     return v

  EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48
  EMAIL_TEMPLATES_DIR: str = "/app/app/email-templates/build"
  EMAILS_ENABLED: bool = False

  @field_validator("EMAILS_ENABLED", mode="before")
  def get_emails_enabled(cls, v: bool, info: ValidationInfo) -> bool:
    return bool(
      info.data.get("SMTP_HOST")
      and info.data.get("SMTP_PORT")
      and info.data.get("EMAILS_FROM_EMAIL")
    )

  # TODO: update type to EmailStr when sqlmodel supports it
  EMAIL_TEST_USER: str = "test@example.com"
  # TODO: update type to EmailStr when sqlmodel supports it
#   FIRST_SUPERUSER: str
#   FIRST_SUPERUSER_PASSWORD: str
  USERS_OPEN_REGISTRATION: bool = False
  model_config = SettingsConfigDict(case_sensitive=True)


settings = Settings()