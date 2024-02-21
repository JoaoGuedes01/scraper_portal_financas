# GuedesMoney

## Description

GuedesMoney is a CLI tool meant to interact and interface with Portal das Finanças automatically via NIF/Password credentials. GuedesMoney is meant to be used for automation and allows for easy access to any action or information in Portal das Finanças through web scraping.

## Installation
```
pip install guedesmoney
```
or
```
pip install guedesmoney==<any_version> (for instance 1.0.1)
```
## Usage
Like any other CLI tool guedesmoney keeps it simple by asking for a command action and arguments in this order
```
guedesmoney <command> <args> <option>
```
## Documentation
| Command | Arguments | Description |
| -------- | -------- | -------- |
|check-alerts|headless, save_results, screenshot|Will check the current alerts|
|check-fiscal|headless, save_results, screenshot|Will check the state of the current fiscal situation|
|check-interactions|headless, save_results, screenshot|Will check the current interactions|
|check-messages|headless, save_results, screenshot|Will check the current messages|
|check-payments|headless, save_results, screenshot, current, missing, refund|Will check state of the current payments|
|config|check_config, show_password|Will prompt user to setup the CLI configuration|
|login|headless|Will check if login credentials are correct|
|run|headless, save_results, screenshot,check-fiscal,check-alerts, check-messages, check-interactions, check-payments ,current, missing, refund, send-email, attach-screenshots|Can run all commands in GuedesMoney (recommended for pipeline integration)|
|version|*none*|Returns the current version of guedesmoney|

| Argument |small | Type | Description |
| -------- | -------- | -------- | -------- |
|headless|hl|boolean|Run scraper in headless mode|
|save_results|sr|boolean|Save results to file|
|screenshot|ss|boolean|Save a screenshot of the of window|
|check-fiscal|cf|boolean|Run Check Fiscal Command|
|check-alerts|ca|boolean|Run Check Alerts Command|
|check-messages|cm|boolean|Run Check Messages Command|
|check-interactions|ci|boolean|Run Check Interactions Command|
|check-payments|cp|boolean|Run Check Payments Command|
|current|c|boolean|Check the state of the current payments|
|missing|m|boolean|Check the state of the missing payments|
|refund|r|boolean|Check the state of the refund payments|
|send-email|e|boolean|Sends an email with the results of the run|
|attach-screenshots|as|boolean|Attach the screenshots to the email|
|check_config|c|boolean|Checks CLI configuration instead of configuring it|
|show_password|shp|boolean|Show password in CLI configuration check|
|user_nif|un|text|User NIF|
|user_password|up|text|User Password|
|email_type|et|text|Sender email provider|
|sender_email|se|text|Sender email|
|sender_password|sp|text|Sender email password|
|recipient_list|rl|text|Recipient list (comma-separated)|

## Example
The following example will run every command and verify every check in guedesmoney through the command run:
```
guedesmoney run --headless --save_results --screenshot --check-fiscal --check-alerts --check-messages --check-interactions --check-payments --current --missing --refund
```

## Tools
- Typer
- Selenium
- bumpversion

## Contributing
You must clone the repo
```
git clone https://github.com/JoaoGuedes01/scraper_portal_financas.git
```
Create a new feature branch (keep it simple and to the point as to follow gitflow)
```
git checkout <your_new_branch>
```
Then you need to merge onto dev branch, which will need CODEOWNER's approval and then your change can be featured in the next version of guedesmoney.
## License
```
MIT License
```