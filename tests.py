from brief_survey import BriefSurvey

def a():
    return
if __name__ == '__main__':
    brief = BriefSurvey(save_handler=a,result_model=None)
    brief.add_question(
    text="Вопрос ",
    question_type='photo',
    choices=("да","нет")

    )