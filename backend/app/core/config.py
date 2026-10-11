from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    database_url: str
    # Clerk Frontend API URL, e.g. https://your-app.clerk.accounts.dev (Clerk dashboard > API keys).
    clerk_issuer: str
    cors_origins: list[str] = ["http://localhost:3000"]


settings = Settings()
