from pathlib import Path

from dill import settings
from pydantic import  Field
from pydantic_settings import BaseSettings
from functools import lru_cache

from llm_server.launcher.utils.logger import logger


class Settings(BaseSettings):
    model_type: str = Field(..., env="MODEL_TYPE")
    model_path: str = Field(..., env="MODEL_PATH")
    n_ctx: int = Field(4096, env="N_CTX")
    n_threads: int = Field(8, env="N_THREADS")
    n_gpu_layers: int = Field(0, env="N_GPU_LAYERS")
    host: str = Field("0.0.0.0", env="HOST")
    port: int = Field(8001, env="PORT")
    api_base_url: str = Field(..., env="API_BASE_URL")
    api_key: str = Field(..., env="API_KEY")  # If not using auth, you can skip auth header


    class Config:
        env_file = Path(__file__).resolve().parent.parent / ".env"
        env_file_encoding = "utf-8"

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()
print(settings.dict())