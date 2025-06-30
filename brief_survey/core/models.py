from typing import List, Optional, Tuple, Callable, Union, Literal
from pydantic import BaseModel, field_validator


class QuestionBase(BaseModel):
    name: str
    text: str
    type: Literal[ "text" , "number" , "choice" , "multi_choice"]   # "text" | "number" | "choice" | "multi_choice"
    validator: Optional[Callable[[str], bool]] = None

    @field_validator('type')
    def type_must_be_known(cls, v):
        allowed = {"text", "number", "choice", "multi_choice"}
        if v not in allowed:
            raise ValueError(f"Type must be one of {allowed}")
        return v


class ChoiceQuestion(QuestionBase):
    choices: List[Tuple[str, str]]
    type: Literal["choice"] = "choice"

    @field_validator("choices")
    def check_choices_non_empty(cls, v, values):
        if not v or not isinstance(v, list):
            raise ValueError("Choices must be a non-empty list")
        return v


class MultiChoiceQuestion(QuestionBase):
    choices: List[Tuple[str, str]]
    type: Literal["choice"] = "multi_choice"

    @field_validator("choices")
    def check_choices_non_empty(cls, v, values):
        if not v or not isinstance(v, list):
            raise ValueError("Choices must be a non-empty list")
        return v


Question = Union[QuestionBase, ChoiceQuestion, MultiChoiceQuestion]


# Пример модели результата, пользователь сам может создать свою
class SurveyResult(BaseModel):
    name: Optional[str]
    age: Optional[int]
    gender: Optional[str]