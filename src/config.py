from pydantic_settings import BaseSettings


class _Settings(BaseSettings):
    OPENXBL_API_KEY: str


Settings = _Settings(_env_file=".env")  # type: ignore
