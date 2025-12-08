from brief_survey import BriefSurvey
from pydantic import BaseModel
from typing import Optional


# Модель результата опроса
class SurveyResult(BaseModel):
    multi_select: Optional[list[str]]


# Обработчик сохранения результата
async def save_handler(user_id: int, result: SurveyResult):
    print(f"Пользователь {user_id} ответил: {result}")

survey = BriefSurvey(

        save_handler=save_handler,
        result_model=SurveyResult,
    )


# survey.add_question(
#     text='Укажите ИНН',
#     name="name",
#     question_type='with_confirm',
#     confirm_field_name="Имя:"
#
# )
#
# survey.add_question(
#     text='Укажите ИНН',
#     name="multi_select",
#     question_type='choice',
#     choices=["1", "2", "3"]
# )
survey.add_question(
    text='Укажите ИНН',
    name="multi_select",
    question_type='multi_choice',
    multy_choice_len=3,
    choices={
        'monday': 'Понедельник',
        'tuesday': 'Вторник',
        'wednesday': 'Среда',
        'thursday': 'Четверг',
        'friday': 'Пятница',
        'saturday': 'Суббота',
        'sunday': 'Воскресенье'
    }
)
# survey.add_question(
#     text='Укажите ИНН',
#     name="multi_select3",
#     question_type='multi_choice',
#     choices=["1", "2", "3"]
# )