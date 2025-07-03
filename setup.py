from setuptools import setup, find_packages

setup(
    name="brief_survey",
    version="0.1.8.3",
    description="Dynamic survey/dialog with aiogram_dialog and Pydantic support",
    author="Fugguri",
    url="https://github.com/Fugguri/brief_survey",
    packages=find_packages(),
    install_requires=[
        "aiogram==3.20",
        "aiogram-dialog",
        "pydantic",
    ],
    python_requires='>=3.12',

)
