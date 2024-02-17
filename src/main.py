#!/usr/bin/env python
import typer
from pkg_resources import get_distribution
import src.controllers as controllers

app = typer.Typer(add_completion=False)

__version__ = get_distribution('guedesmoney').version

@app.command(name="login", help="Will check if login credentials are correct")
def checkLogin(
    user_nif: str = typer.Option(..., "--nif", "-n", help="User NIF"),
    user_pass: str = typer.Option(..., "--password", "-p", help="User Password"),
    headless: bool = typer.Option(False, "--headless", help="Run in headless mode"),
): 
    controllers.CheckLogin(user_nif, user_pass, headless)

@app.command(name="check-fiscal", help="Will check the state of the current fiscal situation")
def checkfiscal(
    user_nif: str = typer.Option(..., "--nif", "-n", help="User NIF"),
    user_pass: str = typer.Option(..., "--password", "-p", help="User Password"),
    headless: bool = typer.Option(False, "--headless", help="Run in headless mode"),
): 
    controllers.checkFiscalSituation(user_nif, user_pass, headless)

@app.command(name="version", help="Returns GuedesMoney version")
def getversion(): print(f'GuedesMoney is running version {__version__}')

def main():
    app()

if __name__ == "__main__":
    main()
