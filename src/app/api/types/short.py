import strawberry
from datetime import datetime


@strawberry.input(description="Tipagem para gerar o encurtamento da url")
class ShortGenerate:
    original_url: str


@strawberry.input(description="Tipagem para pegar a url original.")
class ShortLink:
    short: str


@strawberry.type(description="Retorno de como estão no banco de dados.")
class ShortDB:
    short: str
    short_url: str
    original_url: str
    access_count: int
    created_at: datetime
    expired_at: datetime
    updated_at: datetime
