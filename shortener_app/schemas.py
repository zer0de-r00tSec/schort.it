from pydantic import BaseModel, HttpUrl, validator
import datetime


class URLBase(BaseModel):
    target_url: HttpUrl

    @validator("target_url", pre=True)
    def add_https_scheme(cls, v):
        if isinstance(v, str) and "://" not in v:
            return f"https://{v}"
        return v

class URL(URLBase):
    is_active: bool
    clicks: int
    date: int
    date_readable: str

    @classmethod
    def from_orm(cls, obj):
        return cls(
            target_url=obj.target_url,
            is_active=obj.is_active,
            clicks=obj.clicks,
            date=obj.date,
            date_readable=datetime.datetime.fromtimestamp(float(obj.date)).strftime("%d.%m.%Y %H:%M:%S")
        )


    class Config:
        orm_mode = True

class URLInfo(URL):
    url: str
    admin_url: str
    secret_key: str

    @classmethod
    def from_orm(cls, obj):
        return cls(
            target_url=obj.target_url,
            is_active=obj.is_active,
            clicks=obj.clicks,
            date=obj.date,
            date_readable=datetime.datetime.fromtimestamp(float(obj.date)).strftime("%d.%m.%Y %H:%M:%S"),
            url=f"https://schort.it/{obj.key}",
            admin_url=f"https://schort.it/admin/{obj.secret_key}",
            secret_key=obj.secret_key,
        )
