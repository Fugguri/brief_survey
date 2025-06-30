# BriefSurvey

Универсальный динамический опросник для Telegram-ботов на базе `aiogram_dialog` с поддержкой Pydantic-моделей вопросов и результатов.

---

## Описание

BriefSurvey — это модуль для быстрой и гибкой реализации диалоговых опросников в Telegram с помощью `aiogram` и `aiogram_dialog`.

- Вопросы описываются Pydantic-моделями для строгой типизации и валидации.
- Итоговые ответы автоматически сериализуются обратно в Pydantic-модель результата.
- Легко расширяется и настраивается.
- Позволяет реализовать опросник с разными типами вопросов: текст, число, выбор одного или нескольких вариантов.
- Простое подключение и регистрация обработчиков.

---

## Установка

```bash
pip install brief_survey

pip install -e path/to/brief_survey
```
## Быстрый старт
### 1. Определите вопросы (используйте Pydantic-модели):
```from brief_survey import QuestionBase, ChoiceQuestion

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
    )
]
2. Определите модель результата:
from pydantic import BaseModel
from typing import Optional

class SurveyResult(BaseModel):
    name: Optional[str]
    gender: Optional[str]
3. Создайте функцию для сохранения результатов:
async def save_handler(user_id: int, result: SurveyResult):
    # Логика сохранения, например, в базу
    print(f"Результат опроса пользователя {user_id}: {result}")
4. Инициализируйте и зарегистрируйте опросник:
from brief_survey import BriefSurvey

survey = BriefSurvey(
    questions=questions,
    save_handler=save_handler,
    result_model=SurveyResult,
)

# в основном файле с ботом (Dispatcher dp)
survey.register_handlers(dp)
5. Запускайте команду в Telegram:
/start_survey
