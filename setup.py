import os
from setuptools import setup, find_packages

setup(
    name='guedesmoney',
    author="João Guedes",
    author_email="joaoguedes.cjp@gmail.com",
    description="A CLI interface for interacting with Portal das Finanças automatically and programmatically",
    keywords="Portal_Das_Finanças CLI Python Typer Selenium Automation",
    url="https://github.com/JoaoGuedes01/scraper_portal_financas",
    version='0.1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'guedesmoney=src.main:main'
        ]
    }
)
