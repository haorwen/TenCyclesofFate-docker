from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # OpenAI API Settings
    OPENAI_API_KEY: str | None = None # Allow key to be optional to enable server startup
    OPENAI_BASE_URL: str = "https://api.openai.com/v1"
    OPENAI_MODEL: str = "gpt-3.5-turbo"
    OPENAI_MODEL_CHEAT_CHECK: str = "qwen3-235b-a22b"

    # JWT Settings for OAuth2
    SECRET_KEY: str = "some_random_secret_key_change_me" # Provide a default for container environments
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 600

    # Database URL
    DATABASE_URL: str = "sqlite:///./veloera.db"

    # Linux.do OAuth Settings
    LINUXDO_CLIENT_ID: str | None = None
    LINUXDO_CLIENT_SECRET: str | None = None
    LINUXDO_SCOPE: str = "read"
    LINUXDO_AUTHORIZE_URL: str = "https://connect.linux.do/oauth2/authorize"
    LINUXDO_TOKEN_URL: str = "https://connect.linux.do/oauth2/token"
    LINUXDO_API_BASE_URL: str = "https://connect.linux.do/"

    # Server Settings
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    UVICORN_RELOAD: bool = True

    # Feature Flags
    ENABLE_LINUXDO_LOGIN: bool = False
    ENABLE_REDEMPTION: bool = False

    # Prioritize system environment variables, but allow fallback to .env for local development
    # Pydantic will ignore the env_file if it is not found.
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

# Create a single instance of the settings
settings = Settings()