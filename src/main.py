#!/usr/bin/env python
import typer
from pkg_resources import get_distribution
import controllers

app = typer.Typer(add_completion=False)

__version__ = get_distribution('guedesmoney').version

@app.command(name="login", help="Will check if login credentials are correct")
def checkLogin(
    headless: bool = typer.Option(False, "--headless", help="Run in headless mode"),
): 
    controllers.CheckLogin(headless)

@app.command(name="check-fiscal", help="Will check the state of the current fiscal situation")
def checkfiscal(
    headless: bool = typer.Option(False, "--headless", "-hl", help="Run in headless mode"),
    save_file: bool = typer.Option(False, "--save_results", "-sr" , help="Save results to file"),
    screenshot: bool = typer.Option(False, "--screenshot", "-ss" ,  help="Save a screenshot of the of window"),
): 
    controllers.checkFiscalSituation(headless, screenshot, save_file)

@app.command(name="version", help="Returns GuedesMoney version")
def getversion(): print(f'GuedesMoney is running version {__version__}')

@app.command(name="config", help="Will prompt user to setup the CLI configuration")
def Config(
    check_config: bool = typer.Option(False, "--check_config", "-c", help="Checks CLI configuration instead of configuring it"),
    show_password: bool = typer.Option(False, "--show_password", "-sp", help="Show password in CLI configuration"),
):
    
    if check_config:
        controllers.CheckConfig(show_password)
    else:
        user_nif = typer.prompt("Please enter your NIF")
        user_password = typer.prompt("Please enter your Password", hide_input=True)
        controllers.CLIConfig(user_nif, user_password)

def main():
    app()

if __name__ == "__main__":
    main()
