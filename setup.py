from setuptools import setup, find_packages

setup(
    name="brief_survey",
    version="0.2.2.2b",
    description="Dynamic survey/dialog with aiogram_dialog and Pydantic support",
    author="Fugguri",
    url="https://github.com/Fugguri/brief_survey",
    packages=find_packages(),
    install_requires=[
        "aiogram>=3.20",
        "aiogram_dialog>=2.3.1",
        "phonenumbers>=9.0.10",
        "pydantic>=2.11.7",
    ],
    python_requires='>=3.12',

)
