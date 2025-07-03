from typing import Optional, List, Callable

from brief_survey.core.models.question import QuestionBase
from brief_survey.core.exceptions.questions import UnknownQuestionTypeError
from brief_survey.core.models.question import QUESTION_TYPE_MAP


class QuestionBuilder:
    def __init__(self, question: QuestionBase):
        self.question = question

    @staticmethod
    def create(question_type: str, name: str, text: str, choices: Optional[List[tuple]] = None,validator:Callable=None,*args,**kwargs) -> 'QuestionBase':
        model_cls = QUESTION_TYPE_MAP.get(question_type)
        if not model_cls:
            raise UnknownQuestionTypeError
        return model_cls(name=name, text=text, type=question_type,choices=choices,validator=validator, *args,**kwargs)
