import strawberry
from fastapi import HTTPException, status
from src.app.core.database import get_db
from src.app.models.short import Links
from src.app.api.types.short import ShortGenerate, ShortLink, ShortDB


@strawberry.type
class Query:
    @strawberry.field(
        name="getUrlShort",
        description="Pega a URL original a partir dá URL encurtada.",
    )
    async def get_short(
        self,
        req: ShortLink,
    ) -> ShortDB:
        try:
            db = next(get_db())
            link = db.query(Links).filter(Links.short == req.short).first()

            if not link:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="URL não encontrada.",
                )

            link.access_count += 1
            db.commit()

            return ShortDB(
                short=link.short,
                short_url=link.short_url,
                original_url=link.original_url,
                access_count=link.access_count,
                created_at=link.created_at,
                expired_at=link.expired_at,
                updated_at=link.updated_at,
            )
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e),
            )

    @strawberry.field(
        name="deleteLink",
        description="Deleta um link diretamente.",
    )
    async def delete_link(
        self,
        req: ShortLink,
    ) -> str:
        try:
            db = next(get_db())
            link = db.query(Links).filter(Links.short == req.short).first()

            if not link:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="URL não encontrada.",
                )

            db.delete(link)
            db.commit()

            return "Link deletado com sucesso"
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e),
            )


@strawberry.type
class Mutation:
    @strawberry.mutation(
        name="generateShort",
        description="Gerar uma URL encurtada a partir da URL original.",
    )
    async def generate_short(
        self,
        req: ShortGenerate,
    ) -> ShortDB:
        try:
            link = Links(original_url=req.original_url)
            db = next(get_db())
            db.add(link)
            db.commit()
            db.refresh(link)

            return ShortDB(
                short=link.short,
                short_url=link.short_url,
                original_url=link.original_url,
                access_count=link.access_count,
                created_at=link.created_at,
                expired_at=link.expired_at,
                updated_at=link.updated_at,
            )
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e),
            )
