from setuptools import setup, find_packages

import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\\n" + fh.read()

setup(
    name='guedesmoney',
    author="João Guedes",
    author_email="joaoguedes.cjp@gmail.com",
    description="A CLI interface for interacting with Portal das Finanças automatically and programmatically",
    keywords="Portal_Das_Finanças CLI Python Typer Selenium Automation",
    long_description=long_description,
    url="https://github.com/JoaoGuedes01/scraper_portal_financas",
    version=open('.bumpversion.cfg').readlines()[1].split('=')[1].strip(),  # Reads version from .bumpversion.cfg
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'guedesmoney=src.main:main'
        ]
    }
)
