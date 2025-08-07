from brief_survey import BriefSurvey
from pydantic import BaseModel
from typing import Optional


# Модель результата опроса
class SurveyResult(BaseModel):
    name: Optional[str]


# Обработчик сохранения результата
async def save_handler(user_id: int, result: SurveyResult):
    print(f"Пользователь {user_id} ответил: {result}")

survey = BriefSurvey(

        save_handler=save_handler,
        result_model=SurveyResult,
    )


survey.add_question(
    text='Укажите ИНН',
    name="name",
    question_type='with_confirm',
    confirm_field_name="Имя:"

)