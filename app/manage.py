import typer
import uvicorn

from app.config import settings

cli = typer.Typer()


@cli.command()
def run_server() -> None:
    uvicorn.run(
        "app.main:app",
        host=settings.API.HOST,
        port=settings.API.PORT,
        reload=False,
    )


if __name__ == "__main__":
    cli()
