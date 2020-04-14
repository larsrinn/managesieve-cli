from pathlib import Path

import typer
from sievelib.managesieve import Client
from wasabi import msg

app = typer.Typer()

client: Client


@app.command()
def putscript(
    path: Path = typer.Argument(
        ...,
        exists=True,
        readable=True,
        file_okay=True,
        dir_okay=False,
        resolve_path=True,
    ),
):
    content = path.read_text()
    if client.putscript(path.name, content):
        msg.good(f"Put script {path.name}")
    else:
        msg.fail(f"Failed while putting script {path.name}")


@app.command()
def deletescript(name: str):
    if client.deletescript(name):
        msg.good(f"Deleted script {name}")
    else:
        msg.fail(f"Failed while deleting script {name}")


@app.command()
def listscripts():
    scripts = client.listscripts()
    if not scripts:
        msg.fail("Could not list scripts")
        raise typer.Exit(code=1)
    msg.text(scripts)


@app.callback()
def connect_to_server(
    host: str = typer.Option(...),
    username: str = typer.Option(...),
    tls: bool = True,
    password: str = typer.Option(..., prompt=True, hide_input=True),
):
    global client
    client = Client(host)
    if not client.connect(username, password, starttls=tls):
        msg.fail("Couldn't connect to server. Wrong password?")
        raise typer.Exit(code=1)


def main():
    try:
        app()
    except Exception:
        # todo does not catch typer.Exit()-exceptions
        try:
            client.logout()
        except NameError:
            pass
        raise
