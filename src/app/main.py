import os
from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
    Request,
    responses,
    staticfiles,
    templating,
    status,
)
from fastapi.middleware.cors import CORSMiddleware
from dotenv import find_dotenv, load_dotenv
from sqlalchemy.orm import Session
from strawberry.fastapi import GraphQLRouter
from contextlib import asynccontextmanager
from app.core.database import get_db
from app.api.libs.scheduler import start_scheduler, scheduler
from app.api.schema import schema
from app.models.short import Links


_ = load_dotenv(find_dotenv())

dir_path = os.path.dirname(os.path.abspath(__file__))
templates = templating.Jinja2Templates(directory=os.path.join(dir_path, "templates"))


@asynccontextmanager
async def lifespan(app: FastAPI):
    await start_scheduler()
    yield
    scheduler.shutdown(wait=True)


app = FastAPI(
    title="Breviori",
    description="Web App simples para encurta urls.",
    summary="API para encurtador de urls.",
    version="1.0.0",
    lifespan=lifespan,
    contact={
        "name": "Afio Vinícius",
        "url": "https://vicit.studio",
        "email": "afiovinicius@gmail.com",
    },
)

origins = [
    "http://vicit.studio",
    "https://vicit.studio",
    "http://breviori.vicit.studio",
    "https://breviori.vicit.studio",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount(
    "/static",
    staticfiles.StaticFiles(directory=os.path.join(dir_path, "static")),
    name="static",
)

graphql_app = GraphQLRouter(
    schema,
    graphql_ide="apollo-sandbox",
    multipart_uploads_enabled=True,
)

app.include_router(graphql_app, prefix="/api", tags=["Graphql API"])


@app.get(
    "/",
    description="Template",
    include_in_schema=False,
    response_class=responses.HTMLResponse,
)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/{short}", description="Redirecionamento")
async def home(short: str, db: Session = Depends(get_db)):
    try:
        link = db.query(Links).filter(Links.short == short).first()

        if not link:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="URL não encontrada.",
            )

        link.access_count += 1
        db.commit()

        return responses.RedirectResponse(url=link.original_url)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
