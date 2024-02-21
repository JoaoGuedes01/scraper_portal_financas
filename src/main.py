import typer
from pkg_resources import get_distribution
from . import controllers

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

@app.command(name="check-alerts", help="Will check the current alerts")
def checkAlerts(
    headless: bool = typer.Option(False, "--headless", "-hl", help="Run in headless mode"),
    save_file: bool = typer.Option(False, "--save_results", "-sr" , help="Save results to file"),
    screenshot: bool = typer.Option(False, "--screenshot", "-ss" ,  help="Save a screenshot of the of window"),
): controllers.checkAlerts(headless, screenshot, save_file)

@app.command(name="check-messages", help="Will check the current messages")
def checkMessages(
    headless: bool = typer.Option(False, "--headless", "-hl", help="Run in headless mode"),
    save_file: bool = typer.Option(False, "--save_results", "-sr" , help="Save results to file"),
    screenshot: bool = typer.Option(False, "--screenshot", "-ss" ,  help="Save a screenshot of the of window"),
): controllers.checkMessages(headless, screenshot, save_file)

@app.command(name="check-interactions", help="Will check the current interactions")
def checkInteractions(
    headless: bool = typer.Option(False, "--headless", "-hl", help="Run in headless mode"),
    save_file: bool = typer.Option(False, "--save_results", "-sr" , help="Save results to file"),
    screenshot: bool = typer.Option(False, "--screenshot", "-ss" ,  help="Save a screenshot of the of window"),
): controllers.checkInteractions(headless, screenshot, save_file)

@app.command(name="check-payments", help="Will check state of the current payments")
def checkPayments(
    headless: bool = typer.Option(False, "--headless", "-hl", help="Run in headless mode"),
    save_file: bool = typer.Option(False, "--save_results", "-sr" , help="Save results to file"),
    screenshot: bool = typer.Option(False, "--screenshot", "-ss" ,  help="Save a screenshot of the of window"),
    current_payments: bool = typer.Option(False, "--current", "-c" ,  help="Check the state of the current payments"),
    missing_payments: bool = typer.Option(False, "--missing", "-m" ,  help="Check the state of the missing payments"),
    refund_payments: bool = typer.Option(False, "--refund", "-r" ,  help="Check the state of the refund payments")
): controllers.checkPayments(headless, screenshot, save_file, current_payments, missing_payments, refund_payments)

@app.command(name="run", help="Can run all commands in GuedesMoney (recommended for pipeline integration)")
def RunGeneral(
    headless: bool = typer.Option(False, "--headless", "-hl", help="Run in headless mode"),
    save_file: bool = typer.Option(False, "--save_results", "-sr" , help="Save results to file"),
    screenshot: bool = typer.Option(False, "--screenshot", "-ss" ,  help="Save a screenshot of the of window"),
    check_fiscal: bool = typer.Option(False, "--check-fiscal", "-cf" ,  help="Run Check Fiscal Command"),
    check_alerts: bool = typer.Option(False, "--check-alerts", "-ca" ,  help="Run Check Alerts Command"),
    check_messages: bool = typer.Option(False, "--check-messages", "-cm" ,  help="Run Check Messages Command"),
    check_interactions: bool = typer.Option(False, "--check-interactions", "-ci" ,  help="Run Check Interactions Command"),
    check_payments: bool = typer.Option(False, "--check-payments", "-cp" ,  help="Run Check Payments Command"),
    current_payments: bool = typer.Option(False, "--current", "-c" ,  help="Check the state of the current payments"),
    missing_payments: bool = typer.Option(False, "--missing", "-m" ,  help="Check the state of the missing payments"),
    refund_payments: bool = typer.Option(False, "--refund", "-r" ,  help="Check the state of the refund payments"),
    send_email: bool = typer.Option(False, "--send-email", "-e" ,  help="Send an email with the results of the run"),
    attach_screenshots: bool = typer.Option(False, "--attach-screenshots", "-as" ,  help="Attach the screenshots to the email")
): controllers.RunGeneral(headless, screenshot, save_file, check_fiscal,check_alerts, check_messages, check_interactions, check_payments, current_payments, missing_payments, refund_payments, send_email, attach_screenshots)

@app.command(name="version", help="Returns GuedesMoney version")
def getversion(): print(f'GuedesMoney is running version {__version__}')

@app.command(name="config", help="Will prompt user to setup the CLI configuration")
def Config(
    check_config: bool = typer.Option(False, "--check_config", "-c", help="Checks CLI configuration instead of configuring it"),
    show_password: bool = typer.Option(False, "--show_password", "-shp", help="Show password in CLI configuration"),
    user_nif: str = typer.Option(None, "--user_nif", "-un", help="User NIF"),
    user_password: str = typer.Option(None, "--user_password", "-up", help="User Password"),
    email_type: str = typer.Option(None, "--email_type", "-et", help="Sender email provider"),
    sender_email: str = typer.Option(None, "--sender_email", "-se", help="Sender email"),
    sender_password: str = typer.Option(None, "--sender_password", "-sp", help="Sender email password"),
    recipient_list: str = typer.Option(None, "--recipient_list", "-rl", help="Recipient list (comma-separated)")
):
    
    if check_config:
        controllers.CheckConfig(show_password)
    else:
        user_nif = user_nif or typer.prompt("Please enter your NIF")
        user_password = user_password or typer.prompt("Please enter your Password", hide_input=True)
        email_type = email_type or typer.prompt("Please enter your sender email provider", show_choices=["gmail"], default="gmail")
        sender_email = sender_email or typer.prompt("Please enter your sender email")
        sender_password = sender_password or typer.prompt("Please enter your sender email password", hide_input=True)
        recipient_list = recipient_list or typer.prompt("Please enter your recipient list (comma-separated)")
        controllers.CLIConfig(user_nif, user_password, sender_email, sender_password, recipient_list.split(','), email_type)

@app.command(name="email", help="Sends a test email to the configured email list")
def SendEmail(): controllers.SendEmail()


def main():
    app()

if __name__ == "__main__":
    main()
