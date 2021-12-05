import typer
from format import cformat as class_format

app = typer.Typer()


@app.command()
def hello(name: str):
    typer.echo(f"Hello {name}")


@app.command()
def cformat(path: str):
    class_format(path)


if __name__ == '__main__':
    app()
