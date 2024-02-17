# GuedesMoney

## Description

GuedesMoney is a CLI tool meant to interact and interface with Portal das Finanças automatically via NIF/Password credentials. GuedesMoney is meant to be used for automation and allows for easy access to any action or information in Portal das Finanças through web scraping.

## Installation
```
pip install guedesmoney
```
or
```
pip install guedesmoney==<any_version> (for instance 0.1.0)
```
## Usage
Like any other CLI tool guedesmoney keeps it simple by asking for a command action and arguments in this order
```
guedesmoney <command> <args> <option>
```
## Documentation
| Command | Arguments | Description |
| -------- | -------- | -------- |
|login|nif;password;opt|Will check if login credentials are correct|
|check-fiscal|nif;password;opt|Will check the state of the current fiscal situation|
|version|*none*|Returns the current version of guedesmoney|

| Argument | Type | Description |
| -------- | -------- | -------- |
|nif|string|user's nif (Fiscal Identification Number)|
|password|string|user's password|
|headless|boolean|Run scraper in headless mode|

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