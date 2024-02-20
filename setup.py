from setuptools import setup, find_packages
from pathlib import Path
import codecs
import os

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='guedesmoney',
    author="João Guedes",
    author_email="joaoguedes.cjp@gmail.com",
    description="A CLI interface for interacting with Portal das Finanças automatically and programmatically",
    keywords="Portal_Das_Finanças CLI Python Typer Selenium Automation",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/JoaoGuedes01/scraper_portal_financas",
    version=open('.bumpversion.cfg').readlines()[1].split('=')[1].strip(),  # Reads version from .bumpversion.cfg
    packages=["src"],
    install_requires=["setuptools", "selenium", "typer"],
    entry_points={
        'console_scripts': [
            'guedesmoney=src.main:main'
        ]
    }
)
