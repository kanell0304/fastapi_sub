from pydantic_settings import BaseSettings
from pydantic import Field
from datetime import timedelta

class Settings(BaseSettings):
    SECRET_KEY: str = Field(..., alias="SECRET_KEY")
    ALGORITHM: str = Field("H256", alias="ALGORITHM")
    ACCESS_TOKEN_EXPIRE:int = Field(900, alias="ACCESS_TOKEN_EXPIRE")
    REFRESH_TOKEN_EXPIRE:int =Field (604800, alias="REFRESH_TOKEN_EXPIRE")

    class Config:
        case_sensitive = True
        extra = "allow"
        populate_by_name = True
        env_file = ".env"
    
    @property
    def access_token_lifetime(self) -> timedelta:
        return timedelta(seconds=self.ACCESS_TOKEN_EXPIRE)
        

    @property
    def refresh_token_lifetime(self) -> timedelta:
        return timedelta(seconds=self.REFRESH_TOKEN_EXPIRE)


settings = Settings()