from setuptools import setup, find_packages

setup(
    name="brief_survey",
    version="0.1.0",
    description="Dynamic survey/dialog with aiogram_dialog and Pydantic support",
    author="Fugguri",
    url="https://github.com/yourusername/brief_survey",  # тут ссылка на твой репозиторий

    packages=find_packages(),
    install_requires=[
        "aiogram==3.20",
        "aiogram-dialog",
        "pydantic",
    ],
    python_requires='>=3.12',

)