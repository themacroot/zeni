from dill import settings
from pydantic import  Field
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    model_type: str = Field(..., env="MODEL_TYPE")
    model_path: str = Field(..., env="MODEL_PATH")
    n_ctx: int = Field(4096, env="N_CTX")
    n_threads: int = Field(8, env="N_THREADS")
    n_gpu_layers: int = Field(0, env="N_GPU_LAYERS")
    host: str = Field("0.0.0.0", env="HOST")
    port: int = Field(8001, env="PORT")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()
