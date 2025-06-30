# 🇺🇸 English

# BriefSurvey
Universal Dynamic Survey for Telegram Bots with `aiogram_dialog` and Pydantic
## Description
BriefSurvey is a module for quick and flexible creation of dialog-based surveys in Telegram using aiogram v3 and aiogram_dialog.

- Questions are defined using Pydantic models to enforce strong typing and validation.
- Final answers are automatically serialized back into a Pydantic result model.
- Easy to extend and customize.
- Supports different question types: text, number, single-choice, multiple-choice.
- Simple integration and handler registration.

---
# Installation
## From GitHub Repository

```bash
pip install git+https://github.com/Fugguri/brief_survey.git 
```
## Download Locally and Install

```bash
git clone https://github.com/Fugguri/brief_survey.git
pip install -e brief_survey 
```


## Quick Start
### 1. Define your questions using Pydantic models:

```python
from brief_survey import QuestionBase, ChoiceQuestion, MultiChoiceQuestion

questions = [
    QuestionBase(
        name="name",
        text="What is your name?",
        type="text",
        validator=lambda x: bool(x.strip()),
    ),
    ChoiceQuestion(
        name="gender",
        text="Select your gender",
        type="choice",
        choices=[("1", "Male"), ("2", "Female")],
    ),
    MultiChoiceQuestion(
        name="profession",
        text="Select your profession",
        type="multi_choice",
        choices=[
            ("1", "Athlete"),
            ("2", "Entrepreneur"),
            ("3", "Worker"),
        ],
    ),
]
```
# 2. Define a result model:
``` python
from pydantic import BaseModel
from typing import Optional

class SurveyResult(BaseModel):
    name: Optional[str]
    gender: Optional[str]
    profession: Optional[list[str]]
```
# 3. Create a function to save results:
``` python
async def save_handler(user_id: int, result: SurveyResult):
    # Save logic, e.g., store in database
    print(f"User {user_id} survey result: {result}")

```
# 4. Initialize and register the survey:
``` python
from brief_survey import BriefSurvey

survey = BriefSurvey(
    questions=questions,
    save_handler=save_handler,
    result_model=SurveyResult,
)

# In your main bot file with Dispatcher dp
survey.register_handlers(
    dp=dp,
    command_start='start_survey',     # optional
    text='Start survey',               # optional
    callback_data="start_survey"       # optional
)
```
# 5. Launch the survey in Telegram with the command:
 /start_survey

# Important
If you have global handlers in your bot, filter states explicitly using StateFilter to avoid conflicts that can break the survey after the first message:
``` python
from aiogram.filters import StateFilter

dp.message.register(handle, StateFilter(None))          # Only outside states
dp.callback_query.register(handle_callback, StateFilter(None))
```

# 🇷🇺 Русский

# BriefSurvey

Универсальный динамический опросник для Telegram-ботов на базе `aiogram_dialog` с поддержкой Pydantic-моделей вопросов и результатов.

---

## Описание

BriefSurvey — это модуль для быстрой и гибкой реализации диалоговых опросников в Telegram с помощью `aiogram` 3-й версии и `aiogram_dialog`.

- Вопросы описываются Pydantic-моделями для строгой типизации и валидации.
- Итоговые ответы автоматически сериализуются обратно в Pydantic-модель результата.
- Легко расширяется и настраивается.
- Позволяет реализовать опросник с разными типами вопросов: текст, число, выбор одного или нескольких вариантов.
- Простое подключение и регистрация обработчиков.

---

# Установка
## Github Repo
```bash
pip install git+https://github.com/Fugguri/brief_survey.git 
```
## Скачать локально и установить
```bash
git clone https://github.com/Fugguri/brief_survey.git
pip install -e brief_survey 
```


## Быстрый старт
### 1. Определите вопросы (используйте Pydantic-модели):

```python
from brief_survey import QuestionBase, ChoiceQuestion, MultiChoiceQuestion

questions = [
    QuestionBase(
        name="name",
        text="Как вас зовут?",
        type="text",
        validator=lambda x: bool(x.strip()),
    ),
    ChoiceQuestion(
        name="gender",
        text="Выберите пол",
        type="choice",
        choices=[("1", "Мужской"), ("2", "Женский")],
    ),
    MultiChoiceQuestion(
        name="gender",
        text="Выберите род деятельности",
        type="multi_choice",
        choices=[("1", "Спортсмен"), 
                 ("2", "Предприниматель"),
                 ("3", "Простой работник")
                 ],
    )
]
```
# 2. Определите модель результата:
``` python
from pydantic import BaseModel
from typing import Optional


class SurveyResult(BaseModel):
    name: Optional[str]
    gender: Optional[str]
```
# 3. Создайте функцию для сохранения результатов:
```python
async def save_handler(user_id: int, result: SurveyResult):
    # Логика сохранения, например, в базу
    print(f"Результат опроса пользователя {user_id}: {result}")
```
# 4. Инициализируйте и зарегистрируйте опросник:
``` python
from brief_survey import BriefSurvey

survey = BriefSurvey(
    questions=questions,
    save_handler=save_handler,
    result_model=SurveyResult,
)

# в основном файле с ботом (Dispatcher dp) регистрация в Dispatcher
survey.register_handlers(dp=dp,
                         command_start='start_survey', #опционально
                         text='Начать опрос', #опционально
                         callback_data="start_survey" #опционально
                         )
```
# 5.Запускайте команду в Telegram:
/start_survey

# Важно.
Если у вас есть глобальный handler, фильтруйте state вручную, при помощи StateFilter.Неясные конфликты и после первого сообщения опросник перестает работать.

``` python
from aiogram.filters import StateFilter
dp.message.register(handle,StateFilter(None))  # только вне состояний!
dp.callback_query.register(handle_callback,StateFilter(None))
```


# ToDo
- Функция добавления поля `survey.add_field(*args,**kwargs)` с автоматической валидацией.(Но это не точно😇)