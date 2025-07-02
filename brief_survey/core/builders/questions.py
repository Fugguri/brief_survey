from typing import Optional, List

from brief_survey.core.models import QuestionBase
from brief_survey.core.exceptions.questions import UnknownQuestionTypeError
from brief_survey.core.models import QUESTION_TYPE_MAP


class QuestionBuilder:
    def __init__(self, question: QuestionBase):
        self.question = question

    @staticmethod
    def create(question_type: str, name: str, text: str, choices: Optional[List[tuple]] = None,*args,**kwargs) -> 'QuestionBase':
        model_cls = QUESTION_TYPE_MAP.get(question_type)
        if not model_cls:
            raise UnknownQuestionTypeError
        if question_type in ("choice", "multi_choice"):
            return model_cls(name=name, text=text, choices=choices or [],*args,**kwargs)
        else:
            return model_cls(name=name, text=text, type=question_type,choices=choices, *args,**kwargs)
