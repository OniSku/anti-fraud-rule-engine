from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Класс для загрузки и валидации переменных окружения.
    Если ADMIN_SECRET_KEY не будет найден в файле .env,
    Pydantic не даст приложению запуститься и выдаст ошибку.
    """
    ADMIN_SECRET_KEY: str
    DEBUG: bool = True

    # Указываем Pydantic, что переменные нужно брать из файла .env
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

# Создаем единственный экземпляр настроек (Singleton),
# который будем импортировать в другие файлы, если понадобится.
settings = Settings()